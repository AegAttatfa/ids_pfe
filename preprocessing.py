import pandas as pd
import joblib
import sys
import mysql
from sqlalchemy import create_engine


engine = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}".format(
        user="aeg", pw="sudo root", db="PFE"
    )
)


print("......................... Welcome to my detector .....................\n")

file = sys.argv[1]

if file is not None:
    df_init = pd.read_csv(file)


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
print(df)
if df.size == 0:
    print("No Attack")
result = loaded_model.predict(df)
print("############## Result ##################")
print(result)
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
    df2.to_sql("INTRUSION", con=engine, if_exists="append", chunksize=1000, index=False)
    print("INSERTED")
