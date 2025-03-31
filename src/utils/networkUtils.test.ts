import { NetworkValidator, SUPPORTED_NETWORKS } from './networkUtils';

describe('NetworkUtils', () => {
  it('has correct supported networks', () => {
    expect(SUPPORTED_NETWORKS).toHaveProperty('1');
    expect(SUPPORTED_NETWORKS[1]).toBe('Ethereum Mainnet');
  });
  
  it('validates network correctly', async () => {
    const mockProvider = {
      getNetwork: jest.fn().mockResolvedValue({ chainId: 1 })
    };
    
    const result = await NetworkValidator.validateNetwork(mockProvider);
    
    expect(result).toBe(true);
  });
  
  it('throws error for unsupported network', async () => {
    const mockProvider = {
      getNetwork: jest.fn().mockResolvedValue({ chainId: 999 })
    };
    
    await expect(NetworkValidator.validateNetwork(mockProvider))
      .rejects
      .toThrow('Unsupported network');
  });
  
  it('switches network', async () => {
    const mockProvider = {
      send: jest.fn().mockResolvedValue(true)
    };
    
    await NetworkValidator.switchNetwork(mockProvider, 1);
    
    expect(mockProvider.send).toHaveBeenCalledWith(
      'wallet_switchEthereumChain',
      [expect.any(Object)]
    );
  });
}); 