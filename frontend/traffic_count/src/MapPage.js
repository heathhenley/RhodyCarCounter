import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import PageHeader from './components/PageHeader';

function MapPage() {
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
    <div className="MapPage">
      <Container>
        <PageHeader />
        There will be a map here!
      </Container>
    </div>
  );
}

export default MapPage;
