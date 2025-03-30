import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Web3Provider } from './contexts/Web3Context';
import { AuthProvider } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import LoadingSpinner from './components/ui/LoadingSpinner';

// Lazy load components for better performance
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Home = lazy(() => import('./pages/Home'));
const Properties = lazy(() => import('./pages/Properties'));
const PropertyDetails = lazy(() => import('./pages/PropertyDetails'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const LandlordDashboard = lazy(() => import('./pages/dashboard/LandlordDashboard'));
const TenantDashboard = lazy(() => import('./pages/dashboard/TenantDashboard'));
const AdminDashboard = lazy(() => import('./pages/dashboard/AdminDashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const CreateProperty = lazy(() => import('./pages/CreateProperty'));
const EditProperty = lazy(() => import('./pages/EditProperty'));
const NotFound = lazy(() => import('./pages/NotFound'));
const Unauthorized = lazy(() => import('./pages/Unauthorized'));

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Web3Provider>
          <AuthProvider>
            <div className="flex flex-col min-h-screen bg-gray-50">
              <Navbar />
              
              <main className="flex-grow container mx-auto px-4 py-8">
                <Suspense fallback={<LoadingSpinner />}>
                  <Routes>
                    {/* Public routes */}
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/properties" element={<Properties />} />
                    <Route path="/properties/:id" element={<PropertyDetails />} />
                    <Route path="/unauthorized" element={<Unauthorized />} />
                    
                    {/* Protected routes */}
                    <Route path="/dashboard" element={
                      <ProtectedRoute>
                        <Dashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/landlord" element={
                      <ProtectedRoute roles={['landlord', 'admin']}>
                        <LandlordDashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/tenant" element={
                      <ProtectedRoute roles={['tenant', 'admin']}>
                        <TenantDashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/admin" element={
                      <ProtectedRoute roles={['admin']}>
                        <AdminDashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/profile" element={
                      <ProtectedRoute>
                        <Profile />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/properties/create" element={
                      <ProtectedRoute roles={['landlord', 'admin']}>
                        <CreateProperty />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/properties/edit/:id" element={
                      <ProtectedRoute roles={['landlord', 'admin']}>
                        <EditProperty />
                      </ProtectedRoute>
                    } />
                    
                    {/* Fallback routes */}
                    <Route path="/404" element={<NotFound />} />
                    <Route path="*" element={<Navigate to="/404" replace />} />
                  </Routes>
                </Suspense>
              </main>
              
              <Footer />
            </div>
          </AuthProvider>
        </Web3Provider>
      </Router>
    </ErrorBoundary>
  );
}

export default App; 