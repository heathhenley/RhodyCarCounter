import NavBarTraffic from './NavBarTraffic';

const PageHeader = () => {
  return (
    <header className="App-header ">
      <div className="p-5 d-flex flex-column justify-content-center align-items-center">
        <h1>Traffic Cams in Providence, RI</h1>
        <h4>Streams from <a href="https://www.dot.ri.gov/travel/index.php" >RIDOT</a> - processed using <a href="https://arxiv.org/pdf/1612.08242v1.pdf">YOLOv2</a></h4>
      </div>
      <NavBarTraffic />
    </header>
  );
}

export default PageHeader;