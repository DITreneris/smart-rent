import React, { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
// Comment out Web3Provider import to disable it temporarily
// import { Web3Provider } from './contexts/Web3Context';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Lazy load pages to reduce initial bundle size
const Home = lazy(() => import('./pages/Home'));
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const PropertyDetail = lazy(() => import('./pages/PropertyDetail'));
const PropertyListing = lazy(() => import('./pages/PropertyListing'));
const WalletManagement = lazy(() => import('./pages/WalletManagement'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Loading spinner for lazy-loaded components
const PageLoadingSpinner = () => (
  <div className="flex justify-center items-center h-[70vh]">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <PageLoadingSpinner />;
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <Suspense fallback={<PageLoadingSpinner />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/properties" 
              element={<PropertyListing />} 
            />
            <Route 
              path="/properties/:id" 
              element={<PropertyDetail />} 
            />
            <Route 
              path="/wallet" 
              element={
                <ProtectedRoute>
                  <WalletManagement />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}

// Wrap with providers
const AppWithProviders = () => {
  return (
    // Removed Web3Provider temporarily to fix build issues
    // <Web3Provider>
      <App />
    // </Web3Provider>
  );
};

export default AppWithProviders; 