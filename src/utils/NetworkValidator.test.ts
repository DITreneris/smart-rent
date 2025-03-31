import { NetworkValidator, SUPPORTED_NETWORKS } from '../utils/NetworkValidator';

describe('Network Validator', () => {
  it('returns supported networks', () => {
    expect(SUPPORTED_NETWORKS).toEqual(
      expect.objectContaining({
        '1': expect.any(String),
        '5': expect.any(String)
      })
    );
  });

  describe('isNetworkSupported', () => {
    it('returns true for supported networks', () => {
      expect(NetworkValidator.isNetworkSupported('1')).toBe(true);
      expect(NetworkValidator.isNetworkSupported('5')).toBe(true);
    });

    it('returns false for unsupported networks', () => {
      expect(NetworkValidator.isNetworkSupported('0')).toBe(false);
      expect(NetworkValidator.isNetworkSupported('10')).toBe(false);
    });
  });
}); 