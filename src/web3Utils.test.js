// Web3 utility functions
function formatAddress(address) {
  if (!address) return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
}

function isValidEthereumAddress(address) {
  if (!address) return false;
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

function formatEther(wei) {
  if (!wei) return '0';
  const etherValue = Number(wei) / 1e18;
  return etherValue.toFixed(2);
}

// Tests
describe('Web3 Utilities', () => {
  test('formats Ethereum addresses correctly', () => {
    const address = '0x1234567890123456789012345678901234567890';
    expect(formatAddress(address)).toBe('0x1234...7890');
  });
  
  test('returns empty string for null/undefined addresses', () => {
    expect(formatAddress(null)).toBe('');
    expect(formatAddress(undefined)).toBe('');
    expect(formatAddress('')).toBe('');
  });
  
  test('validates Ethereum addresses correctly', () => {
    expect(isValidEthereumAddress('0x1234567890123456789012345678901234567890')).toBe(true);
    expect(isValidEthereumAddress('0x123')).toBe(false);
    expect(isValidEthereumAddress(null)).toBe(false);
  });
  
  test('formats wei to ether correctly', () => {
    expect(formatEther('1000000000000000000')).toBe('1.00');
    expect(formatEther('500000000000000000')).toBe('0.50');
    expect(formatEther(null)).toBe('0');
  });
}); 