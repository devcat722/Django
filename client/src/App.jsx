import React, { useEffect, useState } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ErrorPage from './pages/ErrorPage';
import Home from './pages/Home';
import ApiPage from './pages/ApiPage';
import './App.css'

const router = createBrowserRouter([
  { 
    path: '/',
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <ApiPage /> },
      { path: 'home', element: <Home />},
    ],
  },
])

const App = () => {
  return (
    <RouterProvider router={router} />
  )
}

export default App