import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Create axios instance with base settings
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for cookies/auth
});

// Interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized globally
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  register: (userData) => apiClient.post('/auth/register', userData),
  login: (credentials) => apiClient.post('/auth/login', credentials),
  logout: () => apiClient.post('/auth/logout'),
  getCurrentUser: () => apiClient.get('/auth/me'),
};

// Properties services
export const propertyService = {
  getProperties: (filters) => apiClient.get('/properties', { params: filters }),
  getProperty: (id) => apiClient.get(`/properties/${id}`),
  createProperty: (propertyData) => apiClient.post('/properties', propertyData),
  updateProperty: (id, propertyData) => apiClient.put(`/properties/${id}`, propertyData),
  deleteProperty: (id) => apiClient.delete(`/properties/${id}`),
  uploadImage: (id, formData) => apiClient.post(`/properties/${id}/images`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

// Contracts services
export const contractService = {
  getContracts: () => apiClient.get('/contracts'),
  getContract: (id) => apiClient.get(`/contracts/${id}`),
  createContract: (contractData) => apiClient.post('/contracts', contractData),
  terminateContract: (id) => apiClient.post(`/contracts/${id}/terminate`),
  completeContract: (id) => apiClient.post(`/contracts/${id}/complete`),
  payRent: (id, paymentData) => apiClient.post(`/contracts/${id}/pay`, paymentData),
};

export default {
  auth: authService,
  properties: propertyService,
  contracts: contractService,
}; 