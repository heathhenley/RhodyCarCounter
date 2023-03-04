import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider} from "react-router-dom";

import TablePage from './TablePage';
import MapPage from './MapPage';

const getCamList = async (status) => {
  const response = await fetch("https://rhodycarcounter-production.up.railway.app/api/cameras/?status=" + status);
  const data = await response.json();
  return data;
}

async function camListLoader() {
  const cameras = await getCamList(true);
  return { cameras };
}

async function camListLoaderNoStatus() {
  const cameras = await getCamList(false);
  return { cameras };
}

const router = createBrowserRouter([
  {
    path: "/RhodyCarCounter",
    element: <TablePage />,
    loader: camListLoader,
  },
  {
    path: "/RhodyCarCounter/map",
    element: <MapPage />,
    loader: camListLoaderNoStatus,
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>
);
