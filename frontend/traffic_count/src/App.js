import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import CameraTable from './components/CameraTable';
import PageHeader from './components/PageHeader';

function App() {
  let [camList, setCamList] = useState(null);

  useEffect(
    () => {
      const getCamList = async () => {
        const response = await fetch("https://rhodycarcounter-production.up.railway.app/api/cameras/");
        const data = await response.json();
        setCamList(data);
      };
      getCamList();
    },
  []);

  return (
    <div className="App">
      <Container>
        <PageHeader />
        {camList ? <CameraTable data={camList}/> : <p>Loading...</p>}
      </Container>
    </div>
  );
}

export default App;
