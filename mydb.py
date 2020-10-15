from flask import Flask, flash, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import logging
import joblib
import pandas as pd
from werkzeug.security import safe_str_cmp
from sqlalchemy import create_engine


from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

engine = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}".format(
        user="", pw="", db=""
    )
)


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


app.config["MYSQL_USER"] = ""
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = ""
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["JWT_SECRET_KEY"] = "secret"

mysql = MySQL(app)

CORS(app)

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"csv", "pcap"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != "admin" or password != "sudo root":
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route("/pro", methods=["GET"])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def predict(file):
    print(file)
    df_init = file

    # drop the incessary features from the input
    df_init.columns = df_init.columns.str.strip()
    df_init.columns = df_init.columns.str.replace(" ", "_")

    df_init.columns = map(str.lower, df_init.columns)

    df_init = df_init[df_init.flow_id != "Flow ID"]

    # preprocessing
    # delete the invalid rows from the incoming traffic

    # print(df_init.columns)

    df_init.rename(columns={"dst_port": "destination_port"}, inplace=True)

    features = [
        "destination_port",
        "flow_duration",
        "total_fwd_packet",
        "total_bwd_packets",
        "total_length_of_fwd_packet",
        "total_length_of_bwd_packet",
        "fwd_packet_length_max",
        "fwd_packet_length_min",
        "fwd_packet_length_mean",
        "fwd_packet_length_std",
        "bwd_packet_length_max",
        "bwd_packet_length_min",
        "bwd_packet_length_mean",
        "bwd_packet_length_std",
        "flow_bytes/s",
        "flow_packets/s",
        "flow_iat_mean",
        "flow_iat_std",
        "flow_iat_max",
        "flow_iat_min",
        "fwd_iat_total",
        "fwd_iat_mean",
        "fwd_iat_std",
        "fwd_iat_max",
        "fwd_iat_min",
        "bwd_iat_total",
        "bwd_iat_mean",
        "bwd_iat_std",
        "bwd_iat_max",
        "bwd_iat_min",
        "fwd_psh_flags",
        "bwd_psh_flags",
        "fwd_urg_flags",
        "bwd_urg_flags",
        "fwd_header_length",
        "bwd_header_length",
        "fwd_packets/s",
        "bwd_packets/s",
        "packet_length_mean",
        "packet_length_std",
        "packet_length_variance",
        "fin_flag_count",
        "syn_flag_count",
        "rst_flag_count",
        "psh_flag_count",
        "ack_flag_count",
        "urg_flag_count",
        "cwr_flag_count",
        "ece_flag_count",
        "down/up_ratio",
        "average_packet_size",
        "fwd_segment_size_avg",
        "bwd_segment_size_avg",
        "fwd_bytes/bulk_avg",
        "fwd_packet/bulk_avg",
        "fwd_bulk_rate_avg",
        "bwd_packet/bulk_avg",
        "bwd_bulk_rate_avg",
        "subflow_fwd_packets",
        "subflow_fwd_bytes",
        "subflow_bwd_packets",
        "subflow_bwd_bytes",
        "fwd_init_win_bytes",
        "bwd_init_win_bytes",
        "fwd_act_data_pkts",
        "fwd_seg_size_min",
        "active_mean",
        "active_std",
        "active_max",
        "active_min",
        "idle_mean",
        "idle_std",
        "idle_max",
        "idle_min",
    ]

    df = df_init[features]

    file_name = "models/RF_final.sav"
    print(".......................Loading Model .......................\n")
    loaded_model = joblib.load(file_name)
    print("....................... Model Loaded .......................\n")
    if df.size == 0:
        print("No Attack")
        return df
    result = loaded_model.predict(df)
    df1 = df_init.assign(label=result)
    # print(df1)
    print("*" * 100)
    df1 = df1.loc[df1["label"] == 1]
    print(df1)
    print("........................Predected ..........................\n")
    print("*" * 100)
    print("\n...................... Detected.............................\n")
    if not df1.empty:
        df2 = df1[["src_ip", "dst_ip", "destination_port"]]
        print(df2)
        print("Inserting to database")
        df2.to_sql(
            "INTRUSION", con=engine, if_exists="append", chunksize=1000, index=False
        )
        print("INSERTED")
        return df2


@app.route("/upload", methods=["POST"])
def fileUpload():
    print("I'm here")
    target = os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files["file"]
    filename = secure_filename(file.filename)
    if filename.rsplit(".", 1)[1].lower() == "csv":
        destination = "/".join([target, filename])
        file.save(destination)
        session["uploadFilePath"] = destination
        data = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
        response = predict(data)
        if not response.empty:
            return "This packets contains malicious traffic"
        else:
            return "This packets is clean"
    return "Not Allowed"


@app.route("/intrusions/recents", methods=["GET"])
@jwt_required
def get_recents():
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "SELECT * FROM INTRUSION WHERE timestamp >= (SELECT MAX(timestamp) FROM INTRUSION)"
        )
        rv = cur.fetchall()
        return jsonify(rv)
    except Exception as e:
        print(e)
    finally:
        cur.close()


@app.route("/intrusions", methods=["GET"])
@jwt_required
def get_all():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM INTRUSION LIMIT 200")
    rv = cur.fetchall()
    # print(rv)
    return jsonify(rv)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, use_reloader=False)
