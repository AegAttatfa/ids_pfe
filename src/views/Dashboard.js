import React from "react";
import axios from "axios";

import { Card, CardBody, CardFooter, CardTitle, Row, Col } from "reactstrap";
// core components
import NewAttacks from "./NewAttacks";

class Dashboard extends React.Component {
  state = { attacksCount: 0, recentAttacks: [], interval: 0 };

  componentDidMount() {
    const config = {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    const interval = setInterval(() => {
      axios.get("/intrusions/recents", config).then((res) => {
        this.setState({
          recentAttacks: [...res.data],
          attacksCount: res.data.length,
        });
      });
    }, 3000);
    this.setState({ interval: interval });
  }
  componentWillUnmount() {
    clearInterval(this.state.interval);
  }

  render() {
    return (
      <div className="content">
        <Row>
          <Col lg="5" md="6" sm="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col md="4" xs="5">
                    <div className="icon-big text-center icon-warning">
                      <i className="nc-icon nc-money-coins text-success" />
                    </div>
                  </Col>
                  <Col md="8" xs="7">
                    <div className="numbers">
                      <p className="card-category">Intrusions</p>
                      <CardTitle tag="p">{this.state.attacksCount}</CardTitle>
                      <p />
                    </div>
                  </Col>
                </Row>
              </CardBody>
              <CardFooter>
                <hr />
                <div className="stats">
                  <i className="far fa-calendar" /> Most Recents
                </div>
              </CardFooter>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col md="12">
            <Card>
              <NewAttacks recentAttacks={this.state.recentAttacks} />
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Dashboard;
