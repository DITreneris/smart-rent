import { createContext, useContext, useState, useEffect } from 'react';
import { ethers } from 'ethers';

// Create context
const Web3Context = createContext();

export function Web3Provider({ children }) {
  // State variables
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [account, setAccount] = useState(null);
  const [network, setNetwork] = useState(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Connect wallet function
  const connectWallet = async () => {
    if (!window.ethereum) {
      setError("No Ethereum wallet found. Please install MetaMask.");
      return;
    }
    
    try {
      setIsConnecting(true);
      setError(null);
      
      // Using ethers v6 syntax
      const ethersProvider = new ethers.BrowserProvider(window.ethereum);
      const accounts = await ethersProvider.send("eth_requestAccounts", []);
      const ethersSigner = await ethersProvider.getSigner();
      const network = await ethersProvider.getNetwork();
      
      setProvider(ethersProvider);
      setSigner(ethersSigner);
      setAccount(accounts[0]);
      setNetwork(network);
      setIsConnected(true);
    } catch (err) {
      console.error("Error connecting to wallet:", err);
      setError(err.message || "Failed to connect to wallet");
    } finally {
      setIsConnecting(false);
    }
  };

  // Disconnect wallet function
  const disconnectWallet = () => {
    setProvider(null);
    setSigner(null);
    setAccount(null);
    setNetwork(null);
    setIsConnected(false);
  };

  // Setup event listeners for account and chain changes
  useEffect(() => {
    if (!window.ethereum) return;
    
    const handleAccountsChanged = (accounts) => {
      if (accounts.length === 0) {
        // User disconnected their wallet
        disconnectWallet();
      } else if (accounts[0] !== account) {
        setAccount(accounts[0]);
        if (provider) {
          provider.getSigner().then(setSigner);
        }
      }
    };
    
    const handleChainChanged = () => {
      // The recommended way is to reload the page on chain change
      window.location.reload();
    };
    
    window.ethereum.on("accountsChanged", handleAccountsChanged);
    window.ethereum.on("chainChanged", handleChainChanged);
    
    // Auto-connect if previously connected
    if (localStorage.getItem("walletConnected") === "true") {
      connectWallet();
    }
    
    return () => {
      window.ethereum.removeListener("accountsChanged", handleAccountsChanged);
      window.ethereum.removeListener("chainChanged", handleChainChanged);
    };
  }, [provider, account]);

  // Save connection status to localStorage
  useEffect(() => {
    if (isConnected) {
      localStorage.setItem("walletConnected", "true");
    } else {
      localStorage.removeItem("walletConnected");
    }
  }, [isConnected]);

  // Helper for contract interactions
  const getContract = (address, abi) => {
    if (!signer) return null;
    return new ethers.Contract(address, abi, signer);
  };

  // Context value to expose
  const value = {
    provider,
    signer,
    account,
    network,
    isConnecting,
    isConnected,
    error,
    connectWallet,
    disconnectWallet,
    getContract
  };
  
  return <Web3Context.Provider value={value}>{children}</Web3Context.Provider>;
}

// Custom hook for using the Web3 context
export function useWeb3() {
  const context = useContext(Web3Context);
  if (context === undefined) {
    throw new Error("useWeb3 must be used within a Web3Provider");
  }
  return context;
} 