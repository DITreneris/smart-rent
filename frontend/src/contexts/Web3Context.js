import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { 
  BrowserProvider, 
  formatEther,
  Contract
} from 'ethers';
import { useAuth } from './AuthContext';

// Smart contract ABIs
import RentalContractABI from '../contracts/RentalContract.json';

// Create context
const Web3Context = createContext();

export function useWeb3() {
  return useContext(Web3Context);
}

// Memoization cache for heavy operations
const contractCallCache = new Map();

export const Web3Provider = ({ children }) => {
  const { user, updateWalletAddress } = useAuth() || {};
  
  // Use refs for ethereum event handlers to avoid recreation
  const accountsChangedHandlerRef = useRef(null);
  const chainChangedHandlerRef = useRef(null);
  
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [account, setAccount] = useState('');
  const [networkId, setNetworkId] = useState(null);
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [userRole, setUserRole] = useState(null); // 'landlord', 'tenant', or 'admin'
  
  // Smart contract instances
  const [rentalContract, setRentalContract] = useState(null);
  
  // Agreement data
  const [landlordAgreements, setLandlordAgreements] = useState([]);
  const [tenantAgreements, setTenantAgreements] = useState([]);
  
  // Contract addresses - should be environment variables in production
  const RENTAL_CONTRACT_ADDRESS = process.env.REACT_APP_RENTAL_CONTRACT_ADDRESS || '';

  // Refs for event handlers to prevent recreation on each render
  const eventHandlersRef = useRef({
    accountsChanged: null,
    chainChanged: null,
    disconnect: null
  });
  
  // Ref for cleanup function to prevent memory leaks
  const cleanupRef = useRef(null);
  
  // Ref for tracking if context is mounted 
  const isMountedRef = useRef(true);
  
  // Initialize contracts with useCallback to avoid recreating the function on every render
  const initializeContracts = useCallback(async (signerOrProvider) => {
    if (!signerOrProvider) return;
    
    try {
      if (RENTAL_CONTRACT_ADDRESS) {
        const contract = new Contract(
          RENTAL_CONTRACT_ADDRESS,
          RentalContractABI,
          signerOrProvider
        );
        setRentalContract(contract);
      }
    } catch (err) {
      console.error('Error initializing contracts:', err);
      setError('Failed to initialize smart contracts');
    }
  }, [RENTAL_CONTRACT_ADDRESS]);

  // Fetch user's balance with throttling to prevent excessive calls
  const fetchBalance = useCallback(async (address, providerToUse) => {
    if (!address || !providerToUse) return;
    
    // Check if we've fetched this balance in the last 30 seconds
    const cacheKey = `balance-${address}`;
    const cachedData = contractCallCache.get(cacheKey);
    const now = Date.now();
    
    if (cachedData && now - cachedData.timestamp < 30000) {
      // Use cached value if recent
      if (isMountedRef.current) {
        setBalance(cachedData.value);
      }
      return cachedData.value;
    }
    
    try {
      const balanceWei = await providerToUse.getBalance(address);
      const balanceEth = formatEther(balanceWei);
      
      // Cache the result
      contractCallCache.set(cacheKey, {
        value: balanceEth,
        timestamp: now
      });
      
      // Only update state if component is still mounted
      if (isMountedRef.current) {
        setBalance(balanceEth);
      }
      
      return balanceEth;
    } catch (error) {
      console.error('Error fetching balance:', error);
      if (isMountedRef.current) {
        setError('Failed to fetch wallet balance');
      }
      return null;
    }
  }, []);

  // Setup MetaMask event handlers
  const setupEventListeners = useCallback(() => {
    if (!window.ethereum) return null;
    
    // Define event handlers
    const handleAccountsChanged = (accounts) => {
      console.log('MetaMask accounts changed:', accounts);
      if (accounts.length === 0) {
        // User disconnected their wallet
        if (isMountedRef.current) {
          setAccount('');
          setSigner(null);
          setRentalContract(null);
          setBalance(null);
          setIsConnected(false);
        }
      } else {
        // User switched accounts
        if (isMountedRef.current) {
          setAccount(accounts[0]);
          if (provider) {
            const signerInstance = provider.getSigner();
            setSigner(signerInstance);
            initializeContracts(signerInstance);
            fetchBalance(accounts[0], provider);
          }
          setIsConnected(true);
        }
      }
    };
    
    const handleChainChanged = (chainIdHex) => {
      console.log('MetaMask chain changed:', chainIdHex);
      // Force page refresh on chain change as recommended by MetaMask
      window.location.reload();
    };
    
    const handleDisconnect = () => {
      console.log('MetaMask disconnected');
      if (isMountedRef.current) {
        setAccount('');
        setSigner(null);
        setRentalContract(null);
        setBalance(null);
        setIsConnected(false);
      }
    };
    
    // Save handlers to ref for cleanup
    eventHandlersRef.current = {
      accountsChanged: handleAccountsChanged,
      chainChanged: handleChainChanged,
      disconnect: handleDisconnect
    };
    
    // Add event listeners
    window.ethereum.on('accountsChanged', handleAccountsChanged);
    window.ethereum.on('chainChanged', handleChainChanged);
    window.ethereum.on('disconnect', handleDisconnect);
    
    // Return cleanup function
    return () => {
      if (window.ethereum?.removeListener) {
        window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
        window.ethereum.removeListener('chainChanged', handleChainChanged);
        window.ethereum.removeListener('disconnect', handleDisconnect);
      }
    };
  }, [provider, initializeContracts, fetchBalance]);

  // Initialize Web3
  useEffect(() => {
    let mounted = true;
    let ethereumProvider = window.ethereum;
    
    const init = async () => {
      try {
        // Check if MetaMask is installed
        if (!ethereumProvider) {
          console.warn('No Ethereum provider detected. Please install MetaMask.');
          if (mounted) setLoading(false);
          return;
        }
        
        // Create provider
        const ethersProvider = new BrowserProvider(ethereumProvider);
        if (!mounted) return;
        setProvider(ethersProvider);
        
        // Get network
        const network = await ethersProvider.getNetwork();
        if (!mounted) return;
        setNetworkId(Number(network.chainId));
        
        // Check for existing accounts
        const accounts = await ethereumProvider.request({ method: 'eth_accounts' });
        
        if (accounts.length > 0) {
          const signerInstance = await ethersProvider.getSigner();
          if (!mounted) return;
          setSigner(signerInstance);
          setAccount(accounts[0]);
          setIsConnected(true);
          
          // Initialize contract instances
          initializeContracts(signerInstance);
          
          // Get account balance 
          const balanceWei = await ethersProvider.getBalance(accounts[0]);
          const balanceEth = formatEther(balanceWei);
          if (!mounted) return;
          setBalance(balanceEth);
        }
        
        // Setup event listeners and store cleanup function
        cleanupRef.current = setupEventListeners();
      } catch (err) {
        console.error('Error initializing Web3:', err);
        if (mounted) {
          setError('Failed to connect to blockchain network');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };
    
    init();
    
    // Clean up
    return () => {
      mounted = false;
      if (ethereumProvider) {
        ethereumProvider.removeListener('accountsChanged', eventHandlersRef.current.accountsChanged);
        ethereumProvider.removeListener('chainChanged', eventHandlersRef.current.chainChanged);
        ethereumProvider.removeListener('disconnect', eventHandlersRef.current.disconnect);
      }
      
      // Clear memoization cache on unmount
      contractCallCache.clear();
    };
  }, [initializeContracts, setupEventListeners]);

  // Connect wallet with proper error handling and loading state management
  const connectWallet = useCallback(async () => {
    const ethereumProvider = window.ethereum;
    
    if (!ethereumProvider) {
      setError('MetaMask is not installed. Please install MetaMask to connect your wallet.');
      return { success: false, error: 'MetaMask not installed' };
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Request accounts from MetaMask
      const accounts = await ethereumProvider.request({
        method: 'eth_requestAccounts'
      });
      
      if (!accounts.length) {
        throw new Error('No accounts found. User may have denied the request.');
      }
      
      // Get signer after connection
      const ethersProvider = new BrowserProvider(ethereumProvider);
      const signerInstance = await ethersProvider.getSigner();
      
      setSigner(signerInstance);
      setAccount(accounts[0]);
      setIsConnected(true);
      setProvider(ethersProvider);
      
      // Initialize contracts with signer
      await initializeContracts(signerInstance);
      
      // Get account balance
      const balanceWei = await ethersProvider.getBalance(accounts[0]);
      const balanceEth = formatEther(balanceWei);
      setBalance(balanceEth);
      
      // Update user's wallet address in database if logged in
      if (user && updateWalletAddress) {
        try {
          await updateWalletAddress(accounts[0]);
        } catch (err) {
          console.error('Error updating wallet address in user profile:', err);
        }
      }
      
      return { success: true, account: accounts[0] };
    } catch (err) {
      console.error('Error connecting wallet:', err);
      setError(err.message || 'Failed to connect wallet');
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [initializeContracts, user, updateWalletAddress]);

  // Disconnect wallet
  const disconnectWallet = useCallback(() => {
    setAccount('');
    setSigner(null);
    setIsConnected(false);
    setRentalContract(null);
    setBalance(null);
  }, []);

  // Get balance function
  const getBalance = useCallback(async (address = account) => {
    try {
      if (!address || !provider) return null;
      
      const balanceWei = await provider.getBalance(address);
      const balanceEth = formatEther(balanceWei);
      setBalance(balanceEth);
      return balanceEth;
    } catch (err) {
      console.error('Error fetching balance:', err);
      return null;
    }
  }, [account, provider]);

  // Sign a message
  const signMessage = useCallback(async (message) => {
    try {
      if (!signer) {
        throw new Error('Wallet not connected');
      }
      
      const signature = await signer.signMessage(message);
      return { success: true, signature };
    } catch (err) {
      console.error('Error signing message:', err);
      return { success: false, error: err.message };
    }
  }, [signer]);

  // Format address for display
  const formatAddress = useCallback((address) => {
    if (!address) return '';
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
  }, []);

  // Check if user is a landlord or tenant based on their wallet address
  const checkUserRole = useCallback(async (walletAddress) => {
    try {
      if (!walletAddress) return;
      
      // In a real app, this would call the API or smart contract
      // For demo purposes, we'll use a simplified check
      if (process.env.REACT_APP_ENABLE_TEST_MODE === 'true') {
        // Simplified role checking for demo (first character of address)
        const addressSum = walletAddress.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
        if (addressSum % 2 === 0) {
          setUserRole('landlord');
        } else {
          setUserRole('tenant');
        }
        return;
      }
      
      // In production, this would call the API to get user role
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/blockchain/user-role/${walletAddress}`
        );
        const data = await response.json();
        if (data.role) {
          setUserRole(data.role);
        }
      } catch (err) {
        console.warn('Failed to fetch user role from API:', err);
        // Fallback to checking contract
        if (rentalContract) {
          try {
            // Check if address has any properties (landlord)
            const properties = await rentalContract.getPropertiesByLandlord(walletAddress);
            if (properties && properties.length > 0) {
              setUserRole('landlord');
              return;
            }
            
            // Check if address has any rental agreements (tenant)
            const agreements = await rentalContract.getAgreementsByTenant(walletAddress);
            if (agreements && agreements.length > 0) {
              setUserRole('tenant');
              return;
            }
          } catch (contractErr) {
            console.warn('Failed to check role from contract:', contractErr);
          }
        }
      }
    } catch (err) {
      console.error('Error checking user role:', err);
    }
  }, [rentalContract]);
  
  // Format agreement data from contract
  const formatAgreement = useCallback((rawAgreement) => {
    return {
      id: rawAgreement.id.toString(),
      propertyId: rawAgreement.propertyId.toString(),
      tenant: rawAgreement.tenant,
      landlord: rawAgreement.landlord,
      startDate: new Date(rawAgreement.startDate * 1000),
      endDate: new Date(rawAgreement.endDate * 1000),
      monthlyRent: formatEther(rawAgreement.monthlyRent),
      securityDeposit: formatEther(rawAgreement.securityDeposit),
      status: ['Pending', 'Active', 'Completed', 'Cancelled'][rawAgreement.status]
    };
  }, []);
  
  // Load agreements for the current user based on their role
  const loadUserAgreements = useCallback(async () => {
    if (!account || !rentalContract || !userRole) return;
    
    try {
      if (userRole === 'landlord') {
        // In a real app, this would call the smart contract
        // For demo, we'll use mock data
        if (process.env.REACT_APP_ENABLE_TEST_MODE === 'true') {
          setLandlordAgreements([
            {
              id: 1,
              propertyId: 101,
              tenant: '0x9473d9b2Ed850a26EFFB2ED0d3D241c664912Bfe',
              landlord: account,
              startDate: new Date('2023-06-01'),
              endDate: new Date('2024-05-31'),
              monthlyRent: '0.5',
              securityDeposit: '1.0',
              status: 'Active'
            },
            {
              id: 2,
              propertyId: 102,
              tenant: '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
              landlord: account,
              startDate: new Date('2023-04-15'),
              endDate: new Date('2023-10-14'),
              monthlyRent: '0.3',
              securityDeposit: '0.6',
              status: 'Active'
            }
          ]);
          return;
        }
        
        // For production app
        const agreements = await rentalContract.getAgreementsByLandlord(account);
        setLandlordAgreements(agreements.map(formatAgreement));
      } else if (userRole === 'tenant') {
        // In a real app, this would call the smart contract
        // For demo, we'll use mock data
        if (process.env.REACT_APP_ENABLE_TEST_MODE === 'true') {
          setTenantAgreements([
            {
              id: 3,
              propertyId: 103,
              tenant: account,
              landlord: '0xe7aF0a922f99c3403Da02F2A396b1444Ff82Fb8E',
              startDate: new Date('2023-07-01'),
              endDate: new Date('2024-06-30'),
              monthlyRent: '0.4',
              securityDeposit: '0.8',
              status: 'Active'
            }
          ]);
          return;
        }
        
        // For production app
        const agreements = await rentalContract.getAgreementsByTenant(account);
        setTenantAgreements(agreements.map(formatAgreement));
      }
    } catch (err) {
      console.error('Error loading user agreements:', err);
    }
  }, [account, rentalContract, userRole, formatAgreement]);
  
  // Update balance when account changes
  useEffect(() => {
    if (isConnected && account) {
      getBalance();
      
      // If user is authenticated, determine their role
      if (user && user.role) {
        setUserRole(user.role);
      } else if (account) {
        // In a real app, you'd check the blockchain or database
        // For demo, we'll check based on test data
        checkUserRole(account);
      }
    }
  }, [isConnected, account, getBalance, user, checkUserRole]);
  
  // Load agreements when role or account changes
  useEffect(() => {
    if (userRole && isConnected) {
      loadUserAgreements();
    }
  }, [userRole, isConnected, loadUserAgreements]);

  // Role-specific functions - memoized to prevent recreation each render
  const isLandlord = useCallback(() => userRole === 'landlord', [userRole]);
  const isTenant = useCallback(() => userRole === 'tenant', [userRole]);
  const isAdmin = useCallback(() => userRole === 'admin', [userRole]);

  // Memoize context value to prevent unnecessary re-renders of all children
  const value = {
    account,
    isConnected,
    balance,
    provider,
    signer,
    networkId,
    loading,
    error,
    rentalContract,
    userRole,
    landlordAgreements,
    tenantAgreements,
    connectWallet,
    disconnectWallet,
    getBalance,
    formatAddress,
    signMessage,
    loadUserAgreements,
    // Role-specific functions
    isLandlord,
    isTenant,
    isAdmin
  };

  return (
    <Web3Context.Provider value={value}>
      {children}
    </Web3Context.Provider>
  );
};

export default Web3Provider; 