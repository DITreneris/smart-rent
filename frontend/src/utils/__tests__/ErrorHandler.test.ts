import { AppError, ErrorType, handleError } from '../ErrorHandler';

describe('ErrorHandler', () => {
  it('creates AppError with correct type', () => {
    const error = new AppError('Test error', ErrorType.AUTH_ERROR);
    
    expect(error.type).toBe(ErrorType.AUTH_ERROR);
    expect(error.message).toBe('Test error');
  });

  it('handles Web3 errors correctly', () => {
    const web3Error = {
      code: 4001,
      message: 'User rejected'
    };
    
    const handle 