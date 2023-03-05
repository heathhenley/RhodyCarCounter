import React from 'react';
import { useLoaderData, Await } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import CameraTable from './components/CameraTable';
import PageHeader from './components/PageHeader';
import Loading from './components/Loading';

function TablePage() {

  let data = useLoaderData();

  return (
    <div className="TablePage">
      <Container>
        <PageHeader />
        <React.Suspense fallback={<Loading />}>
          <Await resolve={data.cameras} errorElement={<p>Error</p>}>
            {(cameras) => <CameraTable cameras={cameras}/>}
          </Await>
        </React.Suspense>
      </Container>
    </div>
  );
}

export default TablePage;
