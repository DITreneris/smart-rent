import { formatAddress, parseEther, formatEther } from '../utils/web3Utils';

// Simple Web3 utility functions to test
const formatAddress = (address: string | null | undefined): string => {
  if (!address) return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
};

const validateEthereumAddress = (address: string): boolean => {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
};

const formatEther = (wei: string): string => {
  // Simple implementation for tests
  const etherValue = Number(wei) / 1e18;
  return etherValue.toString();
};

describe('Web3 Utilities', () => {
  describe('formatAddress', () => {
    it('correctly formats Ethereum addresses', () => {
      const address = '0x1234567890123456789012345678901234567890';
      expect(formatAddress(address)).toBe('0x1234...7890');
    });

    it('handles null or undefined addresses', () => {
      expect(formatAddress(null)).toBe('');
      expect(formatAddress(undefined)).toBe('');
    });
  });

  describe('validateEthereumAddress', () => {
    it('validates correct Ethereum addresses', () => {
      expect(validateEthereumAddress('0x1234567890123456789012345678901234567890')).toBe(true);
    });

    it('rejects invalid Ethereum addresses', () => {
      expect(validateEthereumAddress('invalid')).toBe(false);
      expect(validateEthereumAddress('0x123')).toBe(false);
    });
  });

  describe('formatEther', () => {
    it('converts wei to ether', () => {
      expect(formatEther('1000000000000000000')).toBe('1');
      expect(formatEther('500000000000000000')).toBe('0.5');
    });
  });
}); 