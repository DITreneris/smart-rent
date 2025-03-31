import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { AppError, handleError } from '../utils/ErrorHandler';
import { Property, PropertyFilter, PropertyCreate } from '../types/property';
import { UserProfile } from '../types/user';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for authentication
    this.api.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  setToken(token: string): void {
    this.token = token;
  }

  clearToken(): void {
    this.token = null;
  }

  // Property Endpoints
  async getProperties(filters?: PropertyFilter): Promise<Property[]> {
    try {
      const response: AxiosResponse<Property[]> = await this.api.get('/properties', {
        params: filters,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching properties:', error);
      throw new Error('Failed to fetch properties');
    }
  }

  async getPropertyById(id: string): Promise<Property> {
    try {
      const response: AxiosResponse<Property> = await this.api.get(`/properties/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching property ${id}:`, error);
      throw new Error('Failed to fetch property details');
    }
  }

  async createProperty(propertyData: PropertyCreate): Promise<Property> {
    try {
      const response: AxiosResponse<Property> = await this.api.post('/properties', propertyData);
      return response.data;
    } catch (error) {
      console.error('Error creating property:', error);
      throw new Error('Failed to create property');
    }
  }

  async updateProperty(id: string, propertyData: Partial<PropertyCreate>): Promise<Property> {
    try {
      const response: AxiosResponse<Property> = await this.api.patch(`/properties/${id}`, propertyData);
      return response.data;
    } catch (error) {
      console.error(`Error updating property ${id}:`, error);
      throw new Error('Failed to update property');
    }
  }

  async deleteProperty(id: string): Promise<void> {
    try {
      await this.api.delete(`/properties/${id}`);
    } catch (error) {
      console.error(`Error deleting property ${id}:`, error);
      throw new Error('Failed to delete property');
    }
  }

  // User Endpoints
  async getUserProfile(): Promise<UserProfile> {
    try {
      const response: AxiosResponse<UserProfile> = await this.api.get('/users/me');
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      throw new Error('Failed to fetch user profile');
    }
  }

  async updateUserProfile(userData: Partial<UserProfile>): Promise<UserProfile> {
    try {
      const response: AxiosResponse<UserProfile> = await this.api.patch('/users/me', userData);
      return response.data;
    } catch (error) {
      console.error('Error updating user profile:', error);
      throw new Error('Failed to update user profile');
    }
  }

  // Authentication Endpoints
  async login(email: string, password: string): Promise<{ token: string; user: UserProfile }> {
    try {
      const response = await this.api.post('/auth/login', { email, password });
      this.setToken(response.data.token);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw new Error('Authentication failed');
    }
  }

  async register(userData: {
    email: string;
    password: string;
    name: string;
    role: 'tenant' | 'landlord';
  }): Promise<{ token: string; user: UserProfile }> {
    try {
      const response = await this.api.post('/auth/register', userData);
      this.setToken(response.data.token);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw new Error('Registration failed');
    }
  }

  async logout(): Promise<void> {
    this.clearToken();
  }
}

// Create a singleton instance
const apiService = new ApiService();
export default apiService; 