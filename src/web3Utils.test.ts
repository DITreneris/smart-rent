// Web3 utility functions for testing
const web3Utils = {
  formatAddress: (address: string | null | undefined): string => {
    if (!address) return '';
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
  },

  isValidEthereumAddress: (address: string): boolean => {
    if (!address) return false;
    return /^0x[a-fA-F0-9]{40}$/.test(address);
  },
  
  formatEther: (wei: string): string => {
    if (!wei) return '0';
    const etherValue = Number(wei) / 1e18;
    return etherValue.toFixed(4);
  },
  
  parseEther: (ether: string): string => {
    if (!ether) return '0';
    const weiValue = Number(ether) * 1e18;
    return weiValue.toString();
  }
};

describe('Web3 Utilities', () => {
  describe('formatAddress', () => {
    it('formats Ethereum addresses correctly', () => {
      const address = '0x1234567890123456789012345678901234567890';
      expect(web3Utils.formatAddress(address)).toBe('0x1234...7890');
    });
    
    it('returns empty string for null or undefined address', () => {
      expect(web3Utils.formatAddress(null)).toBe('');
      expect(web3Utils.formatAddress(undefined)).toBe('');
      expect(web3Utils.formatAddress('')).toBe('');
    });
  });
  
  describe('isValidEthereumAddress', () => {
    it('validates correct Ethereum addresses', () => {
      const validAddress = '0x1234567890123456789012345678901234567890';
      expect(web3Utils.isValidEthereumAddress(validAddress)).toBe(true);
    });
    
    it('rejects invalid Ethereum addresses', () => {
      expect(web3Utils.isValidEthereumAddress('0x123')).toBe(false);
      expect(web3Utils.isValidEthereumAddress('not-an-address')).toBe(false);
      expect(web3Utils.isValidEthereumAddress('')).toBe(false);
      expect(web3Utils.isValidEthereumAddress(null as any)).toBe(false);
    });
  });
  
  describe('formatEther', () => {
    it('converts wei to ether', () => {
      expect(web3Utils.formatEther('1000000000000000000')).toBe('1.0000');
      expect(web3Utils.formatEther('500000000000000000')).toBe('0.5000');
      expect(web3Utils.formatEther('0')).toBe('0.0000');
    });
    
    it('handles empty input', () => {
      expect(web3Utils.formatEther('')).toBe('0');
      expect(web3Utils.formatEther(null as any)).toBe('0');
      expect(web3Utils.formatEther(undefined as any)).toBe('0');
    });
  });
  
  describe('parseEther', () => {
    it('converts ether to wei', () => {
      expect(web3Utils.parseEther('1')).toBe('1000000000000000000');
      expect(web3Utils.parseEther('0.5')).toBe('500000000000000000');
    });
    
    it('handles empty input', () => {
      expect(web3Utils.parseEther('')).toBe('0');
      expect(web3Utils.parseEther(null as any)).toBe('0');
      expect(web3Utils.parseEther(undefined as any)).toBe('0');
    });
  });
}); 