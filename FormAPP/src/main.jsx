import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRoutes from './Routes';  // Update this import
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AppRoutes />  {/* Use AppRoutes instead of App */}
  </React.StrictMode>
);

// index.js
// import React from 'react';
// import ReactDOM from 'react-dom';
// import Routes from './Routes';  // Import the Routes component
// import './index.css';

// ReactDOM.render(
//   <React.StrictMode>
//     <Routes />
//   </React.StrictMode>,
//   document.getElementById('root')
// );
