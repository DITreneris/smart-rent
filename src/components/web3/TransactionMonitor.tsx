import React from 'react';
import { useWeb3 } from '../../hooks/useWeb3';
import { TransactionStatus as TxStatus } from '../../utils/transactionTracker';
import { Transaction } from '../../types/transactions';

const TransactionMonitor: React.FC = () => {
  const { transactions } = useWeb3();
  
  // Filter for active transactions (pending or mining)
  const activeTransactions = transactions.filter(
    tx => tx.status === TxStatus.PENDING || tx.status === TxStatus.MINING
  );
  
  if (activeTransactions.length === 0) {
    return null; // Don't render anything if no active transactions
  }
  
  return (
    <div className="transaction-monitor fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 max-w-md border border-gray-200 z-50">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold">Active Transactions</h3>
        <div className="text-sm text-gray-500">
          {activeTransactions.length} transactions in progress
        </div>
      </div>
      
      <div className="divide-y divide-gray-200">
        {activeTransactions.map((tx: Transaction) => (
          <div key={tx.id} className="py-3">
            <div className="flex justify-between items-center mb-1">
              <div className="font-medium">{tx.description}</div>
              <div className="text-sm">
                {tx.status === TxStatus.PENDING ? (
                  <span className="text-yellow-500 flex items-center">
                    <span className="animate-pulse mr-1">●</span> Pending
                  </span>
                ) : (
                  <span className="text-blue-500 flex items-center">
                    <span className="animate-pulse mr-1">●</span> Mining
                  </span>
                )}
              </div>
            </div>
            
            {tx.hash && (
              <div className="text-xs text-gray-500">
                <a 
                  href={`https://etherscan.io/tx/${tx.hash}`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  {`${tx.hash.substring(0, 8)}...${tx.hash.substring(tx.hash.length - 8)}`}
                </a>
              </div>
            )}
            
            {tx.status === TxStatus.MINING && (
              <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
                <div 
                  className="bg-blue-600 h-1.5 rounded-full animate-pulse" 
                  style={{ width: `${Math.min((tx.confirmations || 0) * 50, 100)}%` }} 
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TransactionMonitor; 