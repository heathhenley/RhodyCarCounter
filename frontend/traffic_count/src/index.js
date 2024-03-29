import React from 'react';
import ReactDOM from 'react-dom/client';
import { createHashRouter, RouterProvider, defer} from "react-router-dom";
import Error from './components/Error';

import TablePage from './TablePage';
import MapPage from './MapPage';

const getCamList = async (status) => {
  let base_url = process.env.NODE_ENV === 'development' ? process.env.REACT_APP_API_URL_DEVELOPMENT : process.env.REACT_APP_API_URL_PRODUCTION;
  const response = await fetch(`${base_url}cameras/?status=${status}`);
  const data = await response.json();
  return data;
}

async function camListLoader() {
  const cameras = getCamList(true);
  return defer({ cameras });
}

async function camListLoaderNoStatus() {
  const cameras = await getCamList(false);
  return defer({ cameras });
}

// Using the hash router for now so that I can use GitHub pages to host it (it
// doesn't allow all server routes to be redirected to index.html)
const router = createHashRouter(
  [
    {
      path: "/",
      element: <TablePage />,
      loader: camListLoader,
      errorElement: <Error />,
    },
    {
      path: "/map",
      element: <MapPage />,
      loader: camListLoaderNoStatus,
      errorElement: <Error />,
    }
  ]
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>
);
