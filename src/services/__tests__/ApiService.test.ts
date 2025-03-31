import axios from 'axios';
import apiService from '../ApiService';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('gets properties with filters', async () => {
    const mockProperties = [
      { id: '1', title: 'Property 1' },
      { id: '2', title: 'Property 2' }
    ];
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockProperties });
    
    const filters = { minPrice: 1, maxPrice: 5, bedrooms: 2 };
    const result = await apiService.getProperties(filters);
    
    expect(result).toEqual(mockProperties);
    expect(mockedAxios.get).toHaveBeenCalledWith('/properties', { params: filters });
  });

  it('creates a new property', async () => {
    const newProperty = {
      title: 'New Property',
      description: 'Test',
      price: 2
    };
    
    const createdProperty = {
      id: '1',
      ...newProperty,
      createdAt: '2023-01-01'
    };
    
    mockedAxios.post.mockResolvedValueOnce({ data: createdProperty });
    
    const result = await apiService.createProperty(newProperty);
    
    expect(result).toEqual(createdProperty);
    expect(mockedAxios.post).toHaveBeenCalledWith('/properties', newProperty);
  });

  it('handles authentication errors', async () => {
    mockedAxios.post.mockRejectedValueOnce({
      isAxiosError: true,
      response: {
        status: 401,
        data: { detail: 'Invalid credentials' }
      }
    });
    
    await expect(apiService.login('user@example.com', 'password'))
      .rejects
      .toThrow('Your session has expired');
  });
}); 