import { PropertyService } from './PropertyService';
import apiService from './ApiService';
import { ContractService } from '../utils/contractUtils';

// Mock dependencies
jest.mock('./ApiService', () => ({
  getProperties: jest.fn(),
  getPropertyById: jest.fn(),
  createProperty: jest.fn(),
  updateProperty: jest.fn()
}));

jest.mock('../utils/contractUtils', () => ({
  ContractService: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      status: 'COMPLETED',
      blockchainPropertyId: '123'
    }),
    rentProperty: jest.fn().mockResolvedValue({
      status: 'COMPLETED'
    })
  }))
}));

describe('PropertyService', () => {
  let service;
  
  beforeEach(() => {
    jest.clearAllMocks();
    service = new PropertyService('0x123', []);
  });
  
  it('gets properties from API', async () => {
    const mockProperties = [{ id: '1', title: 'Test' }];
    apiService.getProperties.mockResolvedValue(mockProperties);
    
    const result = await service.getProperties();
    
    expect(result).toEqual(mockProperties);
    expect(apiService.getProperties).toHaveBeenCalled();
  });
  
  it('gets property by ID', async () => {
    const mockProperty = { id: '1', title: 'Test' };
    apiService.getPropertyById.mockResolvedValue(mockProperty);
    
    const result = await service.getPropertyById('1');
    
    expect(result).toEqual(mockProperty);
    expect(apiService.getPropertyById).toHaveBeenCalledWith('1');
  });
  
  it('creates property and lists on blockchain', async () => {
    const propertyData = { title: 'Test', price: 1 };
    const mockProperty = { id: '1', ...propertyData };
    
    apiService.createProperty.mockResolvedValue(mockProperty);
    apiService.updateProperty.mockResolvedValue({
      ...mockProperty,
      blockchain_id: '123'
    });
    
    const result = await service.createProperty(propertyData);
    
    expect(result.property.blockchain_id).toBe('123');
    expect(result.txState.status).toBe('COMPLETED');
  });
}); 