import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import ModalImage from 'react-modal-image';
import camera_icon from '../assets/camera_icon.png';
import PlotModal from './PlotModal';


function cameraNameToAWSLink(name) {
  let aws = "https://rhodycarcounter.s3.amazonaws.com/";
  return aws + name.toLowerCase().replace('/', '_') + ".jpg";
}

function CameraTable(props) {
  let data = props.data;
  return (
    <Container>
      <h2>Camera Table</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Latest Labeled</th>
            <th>Data for Camera</th>
          </tr>
        </thead>
        <tbody>
          {data.map((cam) => (
            <tr key={cam.id}>
              <td>{cam.id}</td>
              <td>{cam.name} <a href={cam.url}>(RIDOT)</a></td>
              <td>{cam.description.replace("Camera at", "")}</td>
              <td><ModalImage
                    small={camera_icon}
                    large={cameraNameToAWSLink(cam.name)}
                    alt={cam.description}/>
              </td>
              <td><PlotModal
                    camera_name={cam.name}
                    camera_id={cam.id}/>
              </td>
            </tr>
          ))}
        </tbody>

          
      </Table>
    </Container>
  );
}

export default CameraTable;
