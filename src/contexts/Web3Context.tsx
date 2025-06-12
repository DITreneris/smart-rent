import React, { useState, useEffect } from 'react';
import { NetworkValidator, SUPPORTED_NETWORKS } from '../utils/networkUtils';
import { ethers } from 'ethers';
import { Transaction, TransactionType } from '../types/transactions';
import eventMonitoringService from '../services/EventMonitoringService';
import receiptService from '../services/ReceiptService';
import { v4 as uuidv4 } from 'uuid';
import { TransactionStatus, TransactionTracker } from '../utils/transactionTracker';

interface Web3ContextType {
  account: string | null;
  chainId: number | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  isConnected: boolean;
  networkError: string | null;
  transactions: Transaction[];
  addTransaction: (tx: Omit<Transaction, 'id' | 'timestamp'>) => void;
  trackTransaction: (
    txPromise: Promise<ethers.ContractTransaction>,
    metadata: { 
      type: TransactionType; 
      description: string;
      amount?: string;
      to?: string;
      metadata?: Record<string, any>;
    }
  ) => Promise<Transaction>;
  generateReceipt: (transactionId: string) => Promise<string | null>;
  getTransaction: (id: string) => Transaction | undefined;
  clearTransaction: (id: string) => void;
}

export const Web3Context = React.createContext<Web3ContextType | undefined>(undefined);

export const Web3Provider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [account, setAccount] = useState<string | null>(null);
  const [chainId, setChainId] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [networkError, setNetworkError] = useState<string | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [provider, setProvider] = useState<ethers.providers.Web3Provider | null>(null);

  const connect = async () => {
    try {
      setNetworkError(null);
      
      const accounts = await window.ethereum.request({ 
        method: 'eth_requestAccounts' 
      });
      
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      await NetworkValidator.validateNetwork(provider);

      const chainId = await window.ethereum.request({ 
        method: 'eth_chainId' 
      });

      setAccount(accounts[0]);
      setChainId(parseInt(chainId, 16));
      setIsConnected(true);
      setProvider(provider);
    } catch (error) {
      setNetworkError(error.message);
      console.error('Error connecting wallet:', error);
      throw error;
    }
  };

  const disconnect = () => {
    setAccount(null);
    setChainId(null);
    setIsConnected(false);
    setProvider(null);
  };

  // Add event listeners for account/chain changes
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        setAccount(accounts[0] || null);
        setIsConnected(!!accounts[0]);
      });

      window.ethereum.on('chainChanged', (chainId: string) => {
        setChainId(parseInt(chainId, 16));
      });
    }

    return () => {
      if (window.ethereum) {
        window.ethereum.removeListener('accountsChanged', () => {});
        window.ethereum.removeListener('chainChanged', () => {});
      }
    };
  }, []);

  // Load transactions from localStorage on init
  useEffect(() => {
    const savedTxs = localStorage.getItem('transactions');
    if (savedTxs) {
      try {
        const parsedTxs = JSON.parse(savedTxs);
        setTransactions(parsedTxs);
      } catch (error) {
        console.error('Error parsing transactions:', error);
      }
    }
  }, []);

  // Save transactions to localStorage when they change
  useEffect(() => {
    if (transactions.length > 0) {
      localStorage.setItem('transactions', JSON.stringify(transactions));
    }
  }, [transactions]);

  // Start/stop event monitoring when connection changes
  useEffect(() => {
    if (isConnected) {
      // Start monitoring blockchain events
      eventMonitoringService.startMonitoring();
    } else {
      // Stop monitoring when disconnected
      eventMonitoringService.stopMonitoring();
    }
    
    return () => {
      // Cleanup on unmount
      eventMonitoringService.stopMonitoring();
    };
  }, [isConnected]);

  // Method to add a transaction to the state
  const addTransaction = (tx: Omit<Transaction, 'id' | 'timestamp'>) => {
    const newTransaction: Transaction = {
      ...tx,
      id: uuidv4(),
      timestamp: Date.now()
    };
    
    setTransactions(prev => [newTransaction, ...prev].slice(0, 50)); // Keep last 50 transactions
    return newTransaction;
  };

  // Method to track a transaction through its lifecycle
  const trackTransaction = async (
    txPromise: Promise<ethers.ContractTransaction>,
    metadata: { 
      type: TransactionType; 
      description: string;
      amount?: string;
      to?: string;
      metadata?: Record<string, any>;
    }
  ): Promise<Transaction> => {
    // Create initial transaction record
    const initialTx: Omit<Transaction, 'id' | 'timestamp'> = {
      hash: '',
      status: TransactionStatus.PENDING,
      description: metadata.description,
      type: metadata.type,
      amount: metadata.amount,
      from: account || '',
      to: metadata.to || '',
      metadata: metadata.metadata
    };
    
    // Add to transactions
    const newTx = addTransaction(initialTx);
    
    try {
      // Start tracking the transaction
      const txState = await TransactionTracker.trackTransaction(txPromise);
      
      // Update transaction with new state
      const updatedTx: Transaction = {
        ...newTx,
        status: txState.status,
        hash: txState.hash,
        confirmations: txState.confirmations,
        error: txState.error
      };
      
      // Update transaction in state
      setTransactions(prev => 
        prev.map(tx => tx.id === newTx.id ? updatedTx : tx)
      );
      
      return updatedTx;
    } catch (error) {
      // Handle failure
      const failedTx: Transaction = {
        ...newTx,
        status: TransactionStatus.FAILED,
        error: error.message
      };
      
      // Update transaction in state
      setTransactions(prev => 
        prev.map(tx => tx.id === newTx.id ? failedTx : tx)
      );
      
      return failedTx;
    }
  };

  // Method to generate a receipt for a completed transaction
  const generateReceipt = async (transactionId: string): Promise<string | null> => {
    const tx = transactions.find(t => t.id === transactionId);
    if (!tx || tx.status !== TransactionStatus.COMPLETED) {
      console.error('Cannot generate receipt: Transaction not found or not completed');
      return null;
    }
    
    try {
      // Use the receipt service to generate a receipt
      const receiptUrl = await receiptService.generateReceipt(tx);
      
      // Update transaction with receipt info
      if (receiptUrl) {
        setTransactions(prev => 
          prev.map(t => t.id === transactionId 
            ? { ...t, receipt: { url: receiptUrl, generatedAt: Date.now() } } 
            : t
          )
        );
      }
      
      return receiptUrl;
    } catch (error) {
      console.error('Error generating receipt:', error);
      return null;
    }
  };

  // Method to get a transaction by ID
  const getTransaction = (id: string): Transaction | undefined => {
    return transactions.find(tx => tx.id === id);
  };

  // Method to clear a transaction
  const clearTransaction = (id: string) => {
    setTransactions(prev => prev.filter(tx => tx.id !== id));
  };

  return (
    <Web3Context.Provider value={{ 
      account, 
      chainId, 
      connect, 
      disconnect, 
      isConnected,
      networkError,
      transactions,
      addTransaction,
      trackTransaction,
      generateReceipt,
      getTransaction,
      clearTransaction
    }}>
      {children}
    </Web3Context.Provider>
  );
}; 