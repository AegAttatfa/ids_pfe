import React from "react";
import "../assets/css/table.css";

import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Table,
  Row,
  Col,
} from "reactstrap";

class NewAttatcks extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const renderedList = this.props.recentAttacks
      .slice(0)
      .reverse()
      .map((attack, index) => {
        if (index < 4) {
          return (
            <tr key={index}>
              <td>{attack.src_ip}</td>
              <td>{attack.dst_ip}</td>
              <td>{attack.destination_port}</td>
              <td className="text-right">{attack.timestamp}</td>
            </tr>
          );
        }
      });
    return (
      <div className="content">
        <Row>
          <Col md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h4">Recent Attacks</CardTitle>
              </CardHeader>
              <CardBody>
                <Table responsive>
                  <thead className="text-primary">
                    <tr>
                      <th className="sticky-column">Attacker</th>
                      <th className="sticky-column">Victim</th>
                      <th className="sticky-column">Port</th>
                      <th className="text-center sticky-column">Date</th>
                    </tr>
                  </thead>
                  <tbody>{renderedList}</tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default NewAttatcks;
