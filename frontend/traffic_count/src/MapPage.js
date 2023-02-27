import React from 'react';
import Container from 'react-bootstrap/Container';
import { useLoaderData } from 'react-router-dom';
import PageHeader from './components/PageHeader';
import MapView from './components/MapView';

function MapPage() {
  let data = useLoaderData()
  return (
    <div className="MapPage">
      <Container  >
        <PageHeader />
        <MapView cameras={data.cameras}/>
      </Container>
    </div>
  );
}

export default MapPage;
