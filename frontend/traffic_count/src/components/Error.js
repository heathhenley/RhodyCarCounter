import { useRouteError } from "react-router-dom";

const Error = () => {
  const error = useRouteError();
  return (
    <div className="Loading d-flex flex-column justify-content-center align-items-center"
         style={{ height: "50vh"}}>      
      <div style={{ fontSize: "2em"}}>
        <h1> Oops!</h1>
        <p> <strong>Error:</strong> something went wrong... </p>
        <p>
          <i>{error.statusText || error.message}</i>
        </p>
      </div>
    </div>
  );
}

export default Error;