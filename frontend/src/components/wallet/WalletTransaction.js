import React, { useState, useEffect } from 'react';
import { useWeb3 } from '../../contexts/Web3Context';
import { formatEther, parseEther } from 'ethers';

const WalletTransaction = ({ 
  agreementId, 
  actionType = 'payRent', 
  amount, 
  onComplete, 
  onError 
}) => {
  const { isConnected, account, createRentalAgreement, payRent, getBalance } = useWeb3();
  const [isProcessing, setIsProcessing] = useState(false);
  const [transactionHash, setTransactionHash] = useState('');
  const [error, setError] = useState('');
  const [balance, setBalance] = useState(null);

  useEffect(() => {
    // Get wallet balance when connected
    if (isConnected && account) {
      fetchBalance();
    }
  }, [isConnected, account]);

  const fetchBalance = async () => {
    try {
      const ethBalance = await getBalance();
      setBalance(ethBalance);
    } catch (err) {
      console.error('Error fetching balance:', err);
    }
  };

  const handleTransaction = async () => {
    if (!isConnected) {
      setError('Please connect your wallet first');
      return;
    }

    setIsProcessing(true);
    setError('');
    setTransactionHash('');

    try {
      let result;

      if (actionType === 'payRent' && agreementId) {
        // Convert amount from ETH to Wei
        const amountInWei = parseEther(amount.toString());
        result = await payRent(agreementId, amountInWei);
      } else {
        setError('Invalid action type or missing parameters');
        setIsProcessing(false);
        return;
      }

      if (result.success) {
        setTransactionHash(result.transactionHash);
        if (onComplete) {
          onComplete(result);
        }
        // Refresh balance after transaction
        fetchBalance();
      } else {
        setError(result.error || 'Transaction failed');
        if (onError) {
          onError(result.error);
        }
      }
    } catch (err) {
      const errorMsg = err.message || 'Transaction failed';
      setError(errorMsg);
      if (onError) {
        onError(errorMsg);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const getActionLabel = () => {
    switch (actionType) {
      case 'payRent':
        return 'Pay Rent';
      case 'signContract':
        return 'Sign Contract';
      default:
        return 'Execute Transaction';
    }
  };

  if (!isConnected) {
    return (
      <div className="wallet-transaction p-4 bg-white rounded-md border border-gray-200">
        <p className="text-red-500">Please connect your wallet to proceed with this transaction.</p>
      </div>
    );
  }

  return (
    <div className="wallet-transaction p-4 bg-white rounded-md border border-gray-200">
      <div className="mb-4">
        <h3 className="text-lg font-medium">{getActionLabel()}</h3>
        
        {balance !== null && (
          <div className="mt-2 text-sm text-gray-600">
            <span>Wallet Balance: {Number(balance).toFixed(4)} ETH</span>
          </div>
        )}
        
        {amount && (
          <div className="mt-1 text-sm">
            <span className="text-gray-600">Transaction Amount: </span>
            <span className="font-medium">{amount} ETH</span>
          </div>
        )}
      </div>
      
      <button
        onClick={handleTransaction}
        disabled={isProcessing}
        className={`
          w-full px-4 py-2 rounded-md text-white font-medium transition
          ${isProcessing 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800'}
        `}
      >
        {isProcessing ? 'Processing...' : getActionLabel()}
      </button>
      
      {error && (
        <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-red-600 text-sm">
          <p>Error: {error}</p>
        </div>
      )}
      
      {transactionHash && (
        <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded text-green-700 text-sm">
          <p>Transaction Successful!</p>
          <p className="mt-1 text-xs font-mono break-all">
            Transaction Hash: {transactionHash}
          </p>
          <a 
            href={`https://etherscan.io/tx/${transactionHash}`}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-1 inline-block text-indigo-600 hover:underline"
          >
            View on Etherscan
          </a>
        </div>
      )}
    </div>
  );
};

export default WalletTransaction; 