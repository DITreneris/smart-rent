import React from 'react';
import { TransactionStatus as TxStatus } from '../../utils/transactionTracker';

interface TransactionStatusProps {
  status: TxStatus;
  hash?: string;
  error?: string;
  confirmations?: number;
}

export const TransactionStatus: React.FC<TransactionStatusProps> = ({
  status,
  hash,
  error,
  confirmations
}) => {
  const getStatusIcon = () => {
    switch (status) {
      case TxStatus.PENDING:
        return '⏳';
      case TxStatus.MINING:
        return '⚡';
      case TxStatus.COMPLETED:
        return '✅';
      case TxStatus.FAILED:
        return '❌';
      default:
        return '❓';
    }
  };

  return (
    <div className="transaction-status">
      <div className="status-header">
        <span className="status-icon">{getStatusIcon()}</span>
        <span className="status-text">{status}</span>
      </div>
      {hash && (
        <div className="hash-container">
          <a 
            href={`https://etherscan.io/tx/${hash}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            View on Etherscan
          </a>
        </div>
      )}
      {confirmations && (
        <div className="confirmations">
          Confirmations: {confirmations}
        </div>
      )}
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
    </div>
  );
}; 