import { useState, useEffect } from 'react';
import { useWeb3 } from './useWeb3';
import { Transaction, TransactionType } from '../types/transactions';
import { TransactionStatus } from '../utils/transactionTracker';
import { ethers } from 'ethers';

interface UseTransactionReturn {
  transaction: Transaction | null;
  isLoading: boolean;
  error: string | null;
  executeTransaction: (
    txPromise: Promise<ethers.ContractTransaction>,
    details: {
      type: TransactionType;
      description: string;
      amount?: string;
      to?: string;
      metadata?: Record<string, any>;
    }
  ) => Promise<Transaction>;
  generateReceipt: () => Promise<string | null>;
}

export const useTransaction = (transactionId?: string): UseTransactionReturn => {
  const { transactions, trackTransaction, generateReceipt } = useWeb3();
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Find the transaction in the transactions array
  useEffect(() => {
    if (transactionId) {
      const tx = transactions.find(t => t.id === transactionId);
      setTransaction(tx || null);
    }
  }, [transactionId, transactions]);
  
  // Execute a transaction and track its status
  const executeTransaction = async (
    txPromise: Promise<ethers.ContractTransaction>,
    details: {
      type: TransactionType;
      description: string;
      amount?: string;
      to?: string;
      metadata?: Record<string, any>;
    }
  ): Promise<Transaction> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const tx = await trackTransaction(txPromise, details);
      setTransaction(tx);
      
      if (tx.status === TransactionStatus.FAILED) {
        setError(tx.error || 'Transaction failed');
      }
      
      return tx;
    } catch (err) {
      setError(err.message || 'Failed to execute transaction');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };
  
  // Generate a receipt for the current transaction
  const generateTransactionReceipt = async (): Promise<string | null> => {
    if (!transaction) {
      setError('No transaction to generate receipt for');
      return null;
    }
    
    if (transaction.status !== TransactionStatus.COMPLETED) {
      setError('Cannot generate receipt for incomplete transaction');
      return null;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const receiptUrl = await generateReceipt(transaction.id);
      return receiptUrl;
    } catch (err) {
      setError(err.message || 'Failed to generate receipt');
      return null;
    } finally {
      setIsLoading(false);
    }
  };
  
  return {
    transaction,
    isLoading,
    error,
    executeTransaction,
    generateReceipt: generateTransactionReceipt
  };
};

export default useTransaction; 