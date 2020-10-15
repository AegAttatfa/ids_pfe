import axios from "axios";
import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";

const BaseURL = "http://localhost:5000";
export default class Login extends Component {
  state = { username: "", password: "", message: "" };

  handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      username: this.state.username,
      password: this.state.password,
    };

    axios
      .post(`${BaseURL}/login`, data)
      .then((res) => {
        localStorage.setItem("token", res.data.access_token);
        this.props.history.push("/admin/dashboard");
      })
      .catch((err) => {
        this.setState({ message: "username or password are not valid" });
      });
  };
  render() {
    return (
      <Container>
        <Row
          className="text-center"
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "5%",
          }}
        >
          <Col xs={6} md={4}>
            <form onSubmit={this.handleSubmit}>
              <h3>Login</h3>

              <div className="form-group">
                <label>Username</label>
                <input
                  type="username"
                  className="form-control"
                  placeholder="Enter username"
                  onChange={(e) => this.setState({ username: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  className="form-control"
                  placeholder="Enter password"
                  onChange={(e) => this.setState({ password: e.target.value })}
                />
              </div>
              <button type="submit" className="btn btn-primary btn-block">
                Login
              </button>
              <div className="form-group has-error">
                <span id="passwordHelp" className="text-danger">
                  {this.state.message}
                </span>
              </div>
            </form>
          </Col>
        </Row>
      </Container>
    );
  }
}
