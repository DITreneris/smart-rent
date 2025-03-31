import { handleError, ApiError, WalletError } from '../utils/ErrorHandler';

describe('Error Handler', () => {
  it('creates API errors correctly', () => {
    const error = new ApiError('Failed to fetch data', 404);
    expect(error.message).toBe('Failed to fetch data');
    expect(error.statusCode).toBe(404);
    expect(error.name).toBe('ApiError');
  });

  it('creates Wallet errors correctly', () => {
    const error = new WalletError('MetaMask not installed');
    expect(error.message).toBe('MetaMask not installed');
    expect(error.name).toBe('WalletError');
  });

  describe('handleError', () => {
    const originalConsoleError = console.error;
    const mockConsoleError = jest.fn();
    
    beforeEach(() => {
      console.error = mockConsoleError;
    });
    
    afterEach(() => {
      console.error = originalConsoleError;
      mockConsoleError.mockClear();
    });
    
    it('logs API errors correctly', () => {
      const error = new ApiError('API Error', 500);
      handleError(error);
      
      expect(mockConsoleError).toHaveBeenCalledWith(
        '[API ERROR]', 
        expect.objectContaining({
          message: 'API Error', 
          statusCode: 500
        })
      );
    });
    
    it('logs Wallet errors correctly', () => {
      const error = new WalletError('Wallet Error');
      handleError(error);
      
      expect(mockConsoleError).toHaveBeenCalledWith(
        '[WALLET ERROR]', 
        expect.objectContaining({
          message: 'Wallet Error'
        })
      );
    });
    
    it('logs general errors correctly', () => {
      const error = new Error('General Error');
      handleError(error);
      
      expect(mockConsoleError).toHaveBeenCalledWith(
        '[ERROR]', 
        expect.objectContaining({
          message: 'General Error'
        })
      );
    });
  });
}); 