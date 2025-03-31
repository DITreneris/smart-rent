import { ContractService } from '../contractUtils';

// Mock ethers
jest.mock('ethers', () => ({
  Contract: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    })
  })),
  providers: {
    Web3Provider: jest.fn().mockImplementation(() => ({
      getSigner: jest.fn()
    }))
  },
  utils: {
    parseEther: jest.fn()
  }
}));

describe('ContractService', () => {
  it('initializes correctly', () => {
    const service = new ContractService('0x123', []);
    expect(service).toBeDefined();
  });
}); 