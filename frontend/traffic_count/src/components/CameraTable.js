import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import Badge from 'react-bootstrap/Badge';
import ModalImage from 'react-modal-image';
import camera_icon from '../assets/camera_icon.png';
import PlotModal from './PlotModal';
import { cameraNameToAWSLink } from '../utils/utils';


export default CameraTable;



const StatusBadge = ({ id, status }) => {

  if (!status) return null;

  // Using bootstrap built in colors
  let statusColor = "success";
  if (status.status === "busy") {
    statusColor = "danger";
  }
  if (status.status === "normal") {
    statusColor = "warning";
  }
  return (
    <Badge pill bg={statusColor} key={id}> {status.status} </Badge>
  );
}


function CameraTable({ cameras}) {
  cameras = cameras.sort((a, b) => (a.id > b.id) ? 1 : -1);
  return (
    <Container
      className="mt-4 p-4 pt-2 shadow rounded"
      style={{ backgroundColor: 'white'}}>
      <div className="">
        <h2>Camera Table</h2>
      </div>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Data for Camera</th>
          </tr>
        </thead>
        <tbody>
          {cameras.map((cam) => (
            <tr key={cam.id}>
              <td>{cam.id}</td>
              <td>
                <div className="d-flex justify-content-start">
                  <div>
                    {cam.name}
                    <span className="ps-1"></span>
                    <StatusBadge
                      id={cam.id}
                      status={cam.status}
                    />
                  </div>
                  <div className='ps-1'>
                    <ModalImage
                      small={camera_icon}
                      large={cameraNameToAWSLink(cam.name)}
                      alt={cam.description}
                    />
                  </div>
                </div>
              </td>
              <td>{cam.description.replace("Camera at", "")}</td>
              <td><PlotModal
                    camera_name={cam.name}
                    camera_id={cam.id}/>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  )
}