export enum ErrorType {
  // Authentication errors
  AUTH_ERROR = 'AUTH_ERROR',
  SESSION_EXPIRED = 'SESSION_EXPIRED',
  PERMISSION_DENIED = 'PERMISSION_DENIED',
  
  // Network errors
  NETWORK_ERROR = 'NETWORK_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',
  API_ERROR = 'API_ERROR',
  
  // Web3 errors
  WEB3_CONNECTION_ERROR = 'WEB3_CONNECTION_ERROR',
  WEB3_TRANSACTION_ERROR = 'WEB3_TRANSACTION_ERROR',
  WALLET_ERROR = 'WALLET_ERROR',
  CONTRACT_ERROR = 'CONTRACT_ERROR',
  
  // Validation errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
} 