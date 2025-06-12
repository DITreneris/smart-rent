import React, { useState } from 'react';
import { useTransaction } from '../../hooks/useTransaction';
import { TransactionType } from '../../types/transactions';
import { TransactionStatus } from '../../utils/transactionTracker';
import LoadingSpinner from '../common/LoadingSpinner';
import { ethers } from 'ethers';

interface PropertyTransactionProps {
  propertyId?: string;
  contractMethod: 'listProperty' | 'rentProperty';
  onSuccess?: (txHash: string) => void;
  onError?: (error: string) => void;
  contractCall: () => Promise<ethers.ContractTransaction>;
  amount: string;
  description: string;
  recipientAddress?: string;
}

const PropertyTransaction: React.FC<PropertyTransactionProps> = ({
  propertyId,
  contractMethod,
  onSuccess,
  onError,
  contractCall,
  amount,
  description,
  recipientAddress
}) => {
  const { transaction, isLoading, error, executeTransaction, generateReceipt } = useTransaction();
  const [receiptUrl, setReceiptUrl] = useState<string | null>(null);
  
  // Determine the transaction type based on the contract method
  const getTransactionType = (): TransactionType => {
    switch (contractMethod) {
      case 'listProperty':
        return TransactionType.PROPERTY_LISTING;
      case 'rentProperty':
        return TransactionType.PROPERTY_RENTAL;
      default:
        return TransactionType.CONTRACT_INTERACTION;
    }
  };
  
  // Handle the transaction execution
  const handleTransaction = async () => {
    try {
      const tx = await executeTransaction(contractCall(), {
        type: getTransactionType(),
        description,
        amount,
        to: recipientAddress,
        metadata: { propertyId }
      });
      
      if (tx.status !== TransactionStatus.FAILED) {
        if (onSuccess) {
          onSuccess(tx.hash);
        }
      } else {
        if (onError) {
          onError(tx.error || 'Transaction failed');
        }
      }
    } catch (err) {
      if (onError) {
        onError(err.message || 'Unknown error occurred');
      }
    }
  };
  
  // Generate a receipt for a completed transaction
  const handleGenerateReceipt = async () => {
    try {
      const url = await generateReceipt();
      setReceiptUrl(url);
    } catch (err) {
      console.error('Error generating receipt:', err);
    }
  };
  
  // Render based on transaction state
  const renderTransactionStatus = () => {
    if (!transaction) {
      return (
        <button
          onClick={handleTransaction}
          disabled={isLoading}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? <LoadingSpinner size="small" /> : `Execute ${description}`}
        </button>
      );
    }
    
    switch (transaction.status) {
      case TransactionStatus.PENDING:
        return (
          <div className="p-4 border border-yellow-200 bg-yellow-50 rounded-md">
            <p className="flex items-center text-yellow-700">
              <span className="animate-pulse mr-2">●</span>
              Transaction Pending
            </p>
            <p className="text-sm text-gray-600 mt-1">Waiting for transaction to be submitted...</p>
          </div>
        );
        
      case TransactionStatus.MINING:
        return (
          <div className="p-4 border border-blue-200 bg-blue-50 rounded-md">
            <p className="flex items-center text-blue-700">
              <span className="animate-pulse mr-2">●</span>
              Transaction Mining
            </p>
            <p className="text-sm text-gray-600 mt-1">
              Transaction is being mined. Confirmations: {transaction.confirmations || 0}
            </p>
            {transaction.hash && (
              <a 
                href={`https://etherscan.io/tx/${transaction.hash}`} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:text-blue-800 mt-2 inline-block"
              >
                View on Etherscan
              </a>
            )}
          </div>
        );
        
      case TransactionStatus.COMPLETED:
        return (
          <div className="p-4 border border-green-200 bg-green-50 rounded-md">
            <p className="flex items-center text-green-700">
              <span className="mr-2">✓</span>
              Transaction Completed
            </p>
            {transaction.hash && (
              <a 
                href={`https://etherscan.io/tx/${transaction.hash}`} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:text-blue-800 mt-2 inline-block mr-4"
              >
                View on Etherscan
              </a>
            )}
            {!receiptUrl ? (
              <button
                onClick={handleGenerateReceipt}
                className="text-sm text-indigo-600 hover:text-indigo-800 mt-2 inline-block font-medium"
              >
                Generate Receipt
              </button>
            ) : (
              <a 
                href={receiptUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-indigo-600 hover:text-indigo-800 mt-2 inline-block font-medium"
              >
                View Receipt
              </a>
            )}
          </div>
        );
        
      case TransactionStatus.FAILED:
        return (
          <div className="p-4 border border-red-200 bg-red-50 rounded-md">
            <p className="flex items-center text-red-700">
              <span className="mr-2">✗</span>
              Transaction Failed
            </p>
            <p className="text-sm text-gray-600 mt-1">
              {transaction.error || 'An error occurred while processing the transaction'}
            </p>
            <button
              onClick={handleTransaction}
              className="mt-3 py-1.5 px-3 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md shadow-sm"
            >
              Retry
            </button>
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="property-transaction">
      {error && !transaction && (
        <div className="p-3 bg-red-100 text-red-700 border border-red-200 mb-4 rounded">
          {error}
        </div>
      )}
      
      {renderTransactionStatus()}
    </div>
  );
};

export default PropertyTransaction; 