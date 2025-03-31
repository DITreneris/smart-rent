import apiService from './ApiService';

// Mock global fetch
global.fetch = jest.fn();

describe('ApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('gets properties', async () => {
    const mockProperties = [{ id: '1', title: 'Property 1' }];
    
    // Mock implementation for this test
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockProperties)
    });

    const result = await apiService.getProperties();
    
    expect(result).toEqual(mockProperties);
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/properties'), expect.any(Object));
  });

  it('gets a property by id', async () => {
    const mockProperty = { id: '1', title: 'Property 1' };
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockProperty)
    });

    const result = await apiService.getProperty('1');
    
    expect(result).toEqual(mockProperty);
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/properties/1'), expect.any(Object));
  });
}); 