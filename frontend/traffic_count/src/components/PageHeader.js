import NavBarTraffic from './NavBarTraffic';

const PageHeader = () => {
  return (
    <header className="App-header">
      <div className="p-5 d-flex flex-column justify-content-center align-items-center">
        <h1>Traffic Cams in Providence, RI</h1>
        <h4>Streams from RIDOT - processed using YOLO </h4>
      </div>
      <NavBarTraffic />
    </header>
  );
}

export default PageHeader;