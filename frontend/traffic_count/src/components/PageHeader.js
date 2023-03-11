import NavBarTraffic from './NavBarTraffic';

const PageHeader = () => {
  return (
    <header
      className="App-header shadow rounded mt-3"
      style={{ backgroundColor: 'white'}}>
      <div className="p-4 d-flex flex-column justify-content-center align-items-center">
        <h1>Traffic Cams in Providence, RI</h1>
        <h4>Streams from <a href="https://www.dot.ri.gov/travel/index.php" >RIDOT</a> - processed using <a href="https://docs.ultralytics.com/">YOLOv8</a></h4>
      </div>
      <NavBarTraffic />
    </header>
  );
}

export default PageHeader;