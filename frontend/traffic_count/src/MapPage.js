import React from 'react';
import Container from 'react-bootstrap/Container';
import { useLoaderData, Await } from 'react-router-dom';
import PageHeader from './components/PageHeader';
import MapView from './components/MapView';
import Loading from './components/Loading';

function MapPage() {
  let data = useLoaderData()
  return (
    <div className="MapPage">
      <Container >
        <PageHeader />
        <React.Suspense fallback={<Loading />}>
          <Await resolve={data.cameras} errorElement={<p>Error</p>}>
            {(cameras) => <MapView cameras={cameras} />}
          </Await>
        </React.Suspense>
      </Container>
    </div>
  );
}

export default MapPage;
