import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';

import './index.css';
import App from './Routes/App/App';
import reportWebVitals from './reportWebVitals';

import { AppProvider } from './Context/AppContext';
import { loader as appLoader } from './Routes/App/App';
import Dashborad from './Components/Dashboard';
import Login from './Components/Login';
import AccountList from './Components/AccountList';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    loader: appLoader,
    children: [
      {
        path: '/dashboard',
        element: <Dashborad />
      },
      {
        path: '/login',
        element: <Login />
      },
      {
        path: '/accounts',
        element: <AccountList />
      },
    ],
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AppProvider>
      <RouterProvider router={router}/>
    </AppProvider> 
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
