import React, { useState } from 'react';
import { useWeb3Context } from '../../contexts/Web3Context';
import { TransactionStatus as TxStatus } from '../../utils/transactionTracker';
import { TransactionStatus } from './TransactionStatus';
import { Transaction, TransactionType } from '../../types/transactions';
import LoadingSpinner from '../common/LoadingSpinner';

const TransactionHistory: React.FC = () => {
  const { transactions, generateReceipt, clearTransaction } = useWeb3Context();
  const [isLoading, setIsLoading] = useState<{ [key: string]: boolean }>({});
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  if (!transactions || transactions.length === 0) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-gray-500 text-center">No transaction history available</p>
      </div>
    );
  }

  const handleGenerateReceipt = async (txId: string) => {
    setIsLoading(prev => ({ ...prev, [txId]: true }));
    setError(null);
    setSuccessMessage(null);

    try {
      const receiptUrl = await generateReceipt(txId);
      if (receiptUrl) {
        setSuccessMessage('Receipt generated successfully');
        // Open the receipt in a new tab
        window.open(receiptUrl, '_blank');
      } else {
        setError('Failed to generate receipt');
      }
    } catch (err) {
      setError('An error occurred while generating the receipt');
      console.error('Receipt generation error:', err);
    } finally {
      setIsLoading(prev => ({ ...prev, [txId]: false }));
    }
  };

  const handleClearTransaction = (txId: string) => {
    clearTransaction(txId);
  };

  const getTransactionTypeLabel = (type: TransactionType): string => {
    switch (type) {
      case TransactionType.PROPERTY_LISTING:
        return 'Property Listing';
      case TransactionType.PROPERTY_RENTAL:
        return 'Property Rental';
      case TransactionType.RENTAL_PAYMENT:
        return 'Rental Payment';
      case TransactionType.RENTAL_COMPLETION:
        return 'Rental Completion';
      case TransactionType.CONTRACT_INTERACTION:
        return 'Contract Interaction';
      case TransactionType.WALLET_TRANSFER:
        return 'Wallet Transfer';
      default:
        return 'Transaction';
    }
  };

  return (
    <div className="transaction-history bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold">Transaction History</h2>
      </div>

      {error && (
        <div className="p-3 bg-red-100 text-red-700 border border-red-200 m-4 rounded">
          {error}
        </div>
      )}

      {successMessage && (
        <div className="p-3 bg-green-100 text-green-700 border border-green-200 m-4 rounded">
          {successMessage}
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Hash
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((tx: Transaction) => (
              <tr key={tx.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {getTransactionTypeLabel(tx.type)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {tx.description}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <TransactionStatus 
                    status={tx.status} 
                    hash={tx.hash}
                    error={tx.error}
                    confirmations={tx.confirmations}
                  />
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {tx.hash ? (
                    <a 
                      href={`https://etherscan.io/tx/${tx.hash}`} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800"
                    >
                      {`${tx.hash.substring(0, 6)}...${tx.hash.substring(tx.hash.length - 4)}`}
                    </a>
                  ) : (
                    'Pending...'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(tx.timestamp).toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    {tx.status === TxStatus.COMPLETED && (
                      <button
                        onClick={() => handleGenerateReceipt(tx.id)}
                        disabled={isLoading[tx.id]}
                        className="text-indigo-600 hover:text-indigo-900 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isLoading[tx.id] ? (
                          <LoadingSpinner size="small" />
                        ) : (
                          'Generate Receipt'
                        )}
                      </button>
                    )}
                    <button
                      onClick={() => handleClearTransaction(tx.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Clear
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionHistory; 