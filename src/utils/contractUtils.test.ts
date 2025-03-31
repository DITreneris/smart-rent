import { ContractService } from './contractUtils';

// Mock the ethers library
jest.mock('ethers', () => ({
  Contract: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    }),
    rentProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    })
  })),
  providers: {
    Web3Provider: jest.fn().mockImplementation(() => ({
      getSigner: jest.fn().mockReturnValue({})
    }))
  }
}));

describe('ContractService', () => {
  let contractService;
  const mockProvider = {};
  const mockAddress = '0x1234567890123456789012345678901234567890';

  beforeEach(() => {
    contractService = new ContractService(mockProvider, mockAddress);
  });

  it('initializes with provider and address', () => {
    expect(contractService).toBeDefined();
  });

  it('lists a property', async () => {
    const property = {
      title: 'Test Property',
      description: 'Test Description',
      price: '1.5'
    };

    const result = await contractService.listProperty(property);
    expect(result).toBeDefined();
    expect(result.status).toBe(1);
  });

  it('rents a property', async () => {
    const propertyId = '1';
    const price = '1.5';

    const result = await contractService.rentProperty(propertyId, price);
    expect(result).toBeDefined();
    expect(result.status).toBe(1);
  });
}); 