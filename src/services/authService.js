import api from '../utils/axiosSetup';
import { isValidEmail, validatePassword } from '../utils/securityUtils';

export const authService = {
  // Register a new user
  async register(userData) {
    // Validate inputs before sending
    if (!isValidEmail(userData.email)) {
      throw new Error('Invalid email format');
    }
    
    const passwordValidation = validatePassword(userData.password);
    if (!passwordValidation.valid) {
      throw new Error(passwordValidation.message);
    }
    
    try {
      const { data } = await api.post('/auth/register', userData);
      return data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Login user
  async login(email, password) {
    try {
      const formData = new FormData();
      formData.append('username
} 