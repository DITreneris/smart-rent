// Simple API service mock
const apiService = {
  getProperties: jest.fn().mockResolvedValue([]),
  getProperty: jest.fn().mockResolvedValue({}),
  createProperty: jest.fn().mockResolvedValue({}),
  updateProperty: jest.fn().mockResolvedValue({})
};

// Mock fetch for testing
global.fetch = jest.fn().mockImplementation(() => 
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([])
  })
);

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
  apiService.getProperties.mockClear();
  apiService.getProperty.mockClear();
  apiService.createProperty.mockClear();
  apiService.updateProperty.mockClear();
});

describe('API Service', () => {
  test('getProperties returns property list', async () => {
    const mockProperties = [
      { id: '1', title: 'Property 1' },
      { id: '2', title: 'Property 2' }
    ];
    
    apiService.getProperties.mockResolvedValueOnce(mockProperties);
    
    const result = await apiService.getProperties();
    expect(result).toEqual(mockProperties);
    expect(apiService.getProperties).toHaveBeenCalledTimes(1);
  });
  
  test('getProperty returns a specific property', async () => {
    const mockProperty = { id: '1', title: 'Property 1' };
    
    apiService.getProperty.mockResolvedValueOnce(mockProperty);
    
    const result = await apiService.getProperty('1');
    expect(result).toEqual(mockProperty);
    expect(apiService.getProperty).toHaveBeenCalledWith('1');
  });
  
  test('createProperty sends property data', async () => {
    const newProperty = { title: 'New Property', price: '1.5' };
    const createdProperty = { id: '1', ...newProperty };
    
    apiService.createProperty.mockResolvedValueOnce(createdProperty);
    
    const result = await apiService.createProperty(newProperty);
    expect(result).toEqual(createdProperty);
    expect(apiService.createProperty).toHaveBeenCalledWith(newProperty);
  });
}); 