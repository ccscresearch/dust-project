import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute: React.FC = () => {
  const { isAuthenticated } = React.useContext(AuthContext);

  // Redireciona para a página de login se não estiver autenticado
  return isAuthenticated ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
