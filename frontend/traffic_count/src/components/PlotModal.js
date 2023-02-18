import React, { useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import TrafficChart from "./TrafficChart";


function PlotModal(props) {
  const [timeSeries, setTimeSeries] = useState(null);
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => {
    const getTimeSeries = async () => {
      const response = await fetch(
        "https://rhodycarcounter-production.up.railway.app/api/cameras/" + props.camera_id + "/datapoints?skip=0&limit=100");
      const data = await response.json();
      setTimeSeries(data);
    };
    getTimeSeries();
    setShow(true);
  }

  return (
    <>
      <Button variant="link" onClick={handleShow}>
        Show Data
      </Button>

      <Modal size="lg" show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{props.camera_name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {timeSeries ? <TrafficChart data={timeSeries} /> : <p> No data, or still loading...</p>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default PlotModal;