import React, { lazy, Suspense, useMemo } from 'react';
import { useAuth } from '../../contexts/AuthContext';

// Lazy load dashboard components
const LandlordDashboard = lazy(() => import('./LandlordDashboard'));
const TenantDashboard = lazy(() => import('./TenantDashboard'));
const AdminDashboard = lazy(() => import('./AdminDashboard'));

// Loading fallback component
const DashboardLoader = () => (
  <div className="flex justify-center items-center min-h-[60vh]">
    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>
  </div>
);

const RoleBasedDashboard = () => {
  const { user } = useAuth();
  
  // Memoize user role check to prevent unnecessary re-calculations
  const userRole = useMemo(() => {
    if (!user) return null;
    return user.role || 'tenant'; // Default to tenant if role is not specified
  }, [user]);

  // Render appropriate dashboard based on user role
  const renderDashboard = () => {
    switch (userRole) {
      case 'landlord':
        return <LandlordDashboard />;
      case 'tenant':
        return <TenantDashboard />;
      case 'admin':
        return <AdminDashboard />;
      default:
        // If no role or unknown role, show tenant dashboard as default
        return <TenantDashboard />;
    }
  };

  // If no user is logged in, show a message
  if (!user) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-3">
          Please log in to view your dashboard
        </h2>
        <p className="text-gray-600">
          You need to be logged in to access this feature.
        </p>
      </div>
    );
  }

  return (
    <Suspense fallback={<DashboardLoader />}>
      {renderDashboard()}
    </Suspense>
  );
};

export default React.memo(RoleBasedDashboard); 