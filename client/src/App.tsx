import React from 'react';
import './App.css';
import Landing from './public/Landing';
import HomePage from './user/HomePage';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './contexts/ProtectedRoute';
import PublicRoute from './contexts/PublicRoute';
import EmailVerification from './components/EmailVerification';
import Onboard from './components/Onboard';

const App : React.FC = () => {

  return (
    
      <BrowserRouter>
        <AuthProvider>
        <Routes>
          <Route path="/home" element={<ProtectedRoute component={HomePage} />} />
          <Route path="/" element={<PublicRoute component={Landing} />} />
        </Routes>
        </AuthProvider>
      </BrowserRouter>
  );
}

export default App;