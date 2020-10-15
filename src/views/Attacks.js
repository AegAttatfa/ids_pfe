import React, { useEffect, useState } from "react";
import getList from "./GetList";
import "../assets/css/table.css";
import { CSVLink } from "react-csv";

import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Table,
  Row,
  Col,
} from "reactstrap";

const Attacks = () => {
  const [attacks, setAttacks] = useState([]);

  const getAll = async () => {
    const res = await getList();
    setAttacks([...res]);
  };
  useEffect(() => {
    const interval = setInterval(() => {
      getAll();
    }, 3000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="content">
      <Row>
        <Col md="12">
          <Card>
            <CardHeader>
              <CardTitle tag="h4">Journal</CardTitle>
              <CardTitle tag="h4">
                <CSVLink data={attacks}>Export to csv</CSVLink>
              </CardTitle>
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
                <tbody>
                  {attacks
                    .splice(0)
                    .reverse()
                    .map((attack, index) => {
                      return (
                        <tr key={index}>
                          <td>{attack.src_ip}</td>
                          <td>{attack.dst_ip}</td>
                          <td>{attack.destination_port}</td>
                          <td className="text-right">{attack.timestamp}</td>
                        </tr>
                      );
                    })}
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Attacks;
