import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ 
  children, 
  roles = [], // Optional roles array for role-based access
  redirectPath = '/login' 
}) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  const location = useLocation();
  
  // Show loading indicator while auth state is being determined
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  // Check if user is authenticated
  if (!isAuthenticated) {
    // Redirect to login but save the location they tried to access
    return <Navigate to={redirectPath} state={{ from: location }} replace />;
  }
  
  // If roles are specified, check if user has required role
  if (roles.length > 0 && user && !roles.includes(user.role)) {
    // User doesn't have required role
    return <Navigate to="/unauthorized" replace />;
  }
  
  // User is authenticated and has required role
  return children;
};

export default ProtectedRoute; 