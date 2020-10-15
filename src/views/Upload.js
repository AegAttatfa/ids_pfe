import React, { useState } from "react";
import { Col, Container, Row } from "reactstrap";
import UploadService from "../services/FileUploadService";

const UploadFiles = () => {
  const [selectedFiles, setSelectedFiles] = useState(undefined);
  const [currentFile, setCurrentFile] = useState(undefined);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");

  const selectFile = (event) => {
    setSelectedFiles(event.target.files);
  };

  const upload = () => {
    let currentFile = selectedFiles[0];

    setProgress(0);
    setCurrentFile(currentFile);

    UploadService.upload(currentFile, (event) => {
      setProgress(Math.round((100 * event.loaded) / event.total));
    })
      .then((response) => {
        console.log(response);
        setMessage(response);
        return UploadService.getFiles();
      })
      .catch(() => {
        setProgress(0);
        setCurrentFile(undefined);
      });

    setSelectedFiles(undefined);
  };

  return (
    <div className="content">
      <Container>
        <Row className="text-center">
          <Col md="12">
            {currentFile && (
              <div className="progress">
                <div
                  className="progress-bar progress-bar-info progress-bar-striped"
                  role="progressbar"
                  aria-valuenow={progress}
                  aria-valuemin="0"
                  aria-valuemax="100"
                  style={{ width: progress + "%" }}
                >
                  {progress}%
                </div>
              </div>
            )}

            <label className="btn btn-default">
              <input type="file" onChange={selectFile} />
            </label>

            <button
              className="btn btn-success"
              disabled={!selectedFiles}
              onClick={upload}
            >
              Upload
            </button>
            <h4> {message} </h4>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default UploadFiles;
