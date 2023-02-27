import React from 'react';
import Container from 'react-bootstrap/Container';
import { useLoaderData } from 'react-router-dom';
import PageHeader from './components/PageHeader';

function MapPage() {
  let camList = useLoaderData().cameras;
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
