import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';


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
            <th>RI DOT Stream</th>
            <th>Latest Labeled</th>
            <th>Data for Camera</th>
          </tr>
        </thead>
        <tbody>
          {data.map((cam) => (
            <tr key={cam.id}>
              <td>{cam.id}</td>
              <td>{cam.name}</td>
              <td>{cam.description.replace("Camera at", "")}</td>
              <td><a href={cam.url}>Link</a></td>
              <td><a href={cameraNameToAWSLink(cam.name)}>Link</a></td>
              <td><a href="#">Show data</a></td>
            </tr>
          ))}
        </tbody>

          
      </Table>
    </Container>
  );
}

export default CameraTable;
