import { AppError, ErrorType, handleError } from '../ErrorHandler';

describe('ErrorHandler', () => {
  it('creates AppError with correct type', () => {
    const error = new AppError('Test error', ErrorType.AUTH_ERROR);
    
    expect(error.type).toBe(ErrorType.AUTH_ERROR);
    expect(error.message).toBe('Test error');
  });

  it('handles Web3 wallet errors', () => {
    const walletError = { code: 4001, message: 'User rejected request' };
    const handled = handleError(walletError);
    
    expect(handled.type).toBe(ErrorType.WALLET_ERROR);
    expect(handled.message).toBe('Transaction rejected by user');
  });

  it('handles API authentication errors', () => {
    const apiError = {
      isAxiosError: true,
      response: {
        status: 401,
        data: { detail: 'Token expired' }
      }
    };
    
    const handled = handleError(apiError);
    
    expect(handled.type).toBe(ErrorType.SESSION_EXPIRED);
  });

  it('handles contract errors', () => {
    const contractError = {
      message: 'execution reverted: Not enough funds',
      code: 'UNPREDICTABLE_GAS_LIMIT'
    };
    
    const handled = handleError(contractError);
    
    expect(handled.type).toBe(ErrorType.CONTRACT_ERROR);
  });
}); 