// Utility function
function formatAddress(address: string | null | undefined): string {
  if (!address) return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
}

describe('Web3 Utils', () => {
  it('formats Ethereum addresses correctly', () => {
    const address = '0x1234567890123456789012345678901234567890';
    expect(formatAddress(address)).toBe('0x1234...7890');
  });

  it('returns empty string for null/undefined addresses', () => {
    expect(formatAddress(null)).toBe('');
    expect(formatAddress(undefined)).toBe('');
  });
}); 