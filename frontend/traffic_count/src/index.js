import React from 'react';
import ReactDOM from 'react-dom/client';
import { createHashRouter, RouterProvider, defer} from "react-router-dom";
import Error from './components/Error';

import TablePage from './TablePage';
import MapPage from './MapPage';

const getCamList = async (status) => {
  const response = await fetch("https://rhodycarcounter-production.up.railway.app/api/cameras/?status=" + status);
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
