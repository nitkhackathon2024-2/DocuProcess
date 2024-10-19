// Routes.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './HomePage';
import App from './App';
import Form from './Form';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/upload" element={<App />} />
        <Route path="/SimpleForm" element={<Form />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
