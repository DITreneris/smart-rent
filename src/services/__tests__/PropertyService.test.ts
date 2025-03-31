import { PropertyService } from '../PropertyService';
import { ContractService } from '../../utils/contractUtils';
import apiService from '../ApiService';
import { TransactionStatus } from '../../utils/transactionTracker';

// Mock dependencies
jest.mock('../../utils/contractUtils');
jest.mock('../ApiService', () => ({
  getProperties: jest.fn(),
  getPropertyById: jest.fn(),
  createProperty: jest.fn(),
  updateProperty: jest.fn()
}));

describe('PropertyService', () => {
  let service: PropertyService;
  
  beforeEach(() => {
    jest.clearAllMocks();
    service = new PropertyService('0x123', []);
  });
  
  it('fetches properties from API', async () => {
    const mockProperties = [{ id: '1', title: 'Test Property' }];
    (apiService.getProperties as jest.Mock).mockResolvedValue(mockProperties);
    
    const result = await service.getProperties();
    
    expect(result).toEqual(mockProperties);
    expect(apiService.getProperties).toHaveBeenCalled();
  });
  
  it('creates property and lists on blockchain', async () => {
  });
}); 