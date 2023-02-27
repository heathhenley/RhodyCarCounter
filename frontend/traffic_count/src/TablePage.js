import React from 'react';
import { useLoaderData } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import CameraTable from './components/CameraTable';
import PageHeader from './components/PageHeader';

function TablePage() {

  let camList = useLoaderData().cameras.sort((a, b) => (a.id > b.id) ? 1 : -1);

  return (
    <div className="App">
      <Container>
        <PageHeader />
        {camList ? <CameraTable data={camList}/> : <p>Loading...</p>}
      </Container>
    </div>
  );
}

export default TablePage;
