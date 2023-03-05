import Spinner from 'react-bootstrap/Spinner';

const Loading = () => {
  return (
    <div className="Loading d-flex flex-column justify-content-center align-items-center"
         style={{ height: "100vh"}}>
      <div style={{ fontSize: "2em"}}>
        <p> Loading <strong>ALL THE CAMERAS...</strong> </p>
      </div>
      <Spinner animation="border"
               role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  );
}

export default Loading;