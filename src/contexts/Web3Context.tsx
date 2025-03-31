import React, { useState, useEffect } from 'react';
import { NetworkValidator, SUPPORTED_NETWORKS } from '../utils/networkUtils';
import { ethers } from 'ethers';
import { Transaction } from '../types/transactions';
import eventMonitoringService from '../services/EventMonitoringService';

interface Web3ContextType {
  account: string | null;
  chainId: number | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  isConnected: boolean;
  networkError: string | null;
  transactions: Transaction[];
  addTransaction: (tx: Omit<Transaction, 'id' | 'timestamp'>) => void;
}

export const Web3Context = React.createContext<Web3ContextType | undefined>(undefined);

export const Web3Provider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [account, setAccount] = useState<string | null>(null);
  const [chainId, setChainId] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [networkError, setNetworkError] = useState<string | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);

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

  return (
    <Web3Context.Provider value={{ 
      account, 
      chainId, 
      connect, 
      disconnect, 
      isConnected,
      networkError,
      transactions,
      addTransaction: (tx: Omit<Transaction, 'id' | 'timestamp'>) => {
        // Implementation of addTransaction method
      }
    }}>
      {children}
    </Web3Context.Provider>
  );
}; 