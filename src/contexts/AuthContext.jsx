import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

// Create context
const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();
  
  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          // Get user from localStorage initially
          const storedUser = authService.getCurrentUser();
          setUser(storedUser);
          setIsAuthenticated(true);
          
          // Refresh user data from API
          try {
            const freshUserData = await authService.refreshUserData();
            setUser(freshUserData);
          } catch (refreshError) {
            console.error('Error refreshing user data:', refreshError);
            // If token is invalid, logout
            if (refreshError.response && refreshError.response.status === 401) {
              logout();
            }
          }
        }
      } catch (err) {
        console.error('Auth initialization error:', err);
        setError('Failed to initialize authentication');
      } finally {
        setIsLoading(false);
      }
    };
    
    initAuth();
  }, []);
  
  const login = async (email, password) => {
    setError(null);
    try {
      setIsLoading(true);
      const data = await authService.login(email, password);
      
      // Set user state
      setUser(data.user || { email });
      setIsAuthenticated(true);
      
      // If successful, refresh user data
      try {
        const userData = await authService.refreshUserData();
        setUser(userData);
      } catch (refreshError) {
        console.error('Error getting user details after login:', refreshError);
      }
      
      return data;
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || err.message || 'Login failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };
  
  const register = async (userData) => {
    setError(null);
    try {
      setIsLoading(true);
      const data = await authService.register(userData);
      return data;
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.detail || err.message || 'Registration failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };
  
  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
    navigate('/login');
  };
  
  const updateProfile = async (userData) => {
    setError(null);
    try {
      setIsLoading(true);
      const updatedUser = await authService.updateProfile(userData);
      setUser(updatedUser);
      return updatedUser;
    } catch (err) {
      console.error('Profile update error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to update profile');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };
  
  const changePassword = async (currentPassword, newPassword) => {
    setError(null);
    try {
      setIsLoading(true);
      return await authService.changePassword(currentPassword, newPassword);
    } catch (err) {
      console.error('Password change error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to change password');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };
  
  const value = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    setError
  };
  
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Custom hook for using the auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 