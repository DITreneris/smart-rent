import React, { useState, useEffect } from 'react';
import { useWeb3 } from '../contexts/Web3Context';
import { formatEther, parseEther } from 'ethers';

/**
 * WalletDemo - A component to demonstrate wallet functionality
 * This component shows how to:
 * 1. Connect to MetaMask
 * 2. Display wallet information
 * 3. Create and interact with rental agreements
 * 4. Process payments
 */
const WalletDemo = () => {
  const { 
    isConnected, 
    account, 
    connectWallet, 
    disconnectWallet, 
    getBalance, 
    createRentalAgreement,
    payRent,
    getRentalAgreement,
    formatAddress
  } = useWeb3();

  // State
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [agreementId, setAgreementId] = useState('');
  const [agreement, setAgreement] = useState(null);
  const [transaction, setTransaction] = useState(null);
  
  // Form state for creating agreement
  const [formData, setFormData] = useState({
    propertyId: 'property123',
    landlordAddress: '',
    startDate: new Date().toISOString().split('T')[0], // Today
    endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 30 days from now
    monthlyRent: '0.05',
    securityDeposit: '0.1'
  });

  // Load wallet balance when connected
  useEffect(() => {
    if (isConnected && account) {
      loadBalance();
    } else {
      setBalance(null);
    }
  }, [isConnected, account]);

  // Load wallet balance
  const loadBalance = async () => {
    try {
      const bal = await getBalance();
      setBalance(bal);
    } catch (err) {
      console.error('Error loading balance:', err);
      setError('Failed to load wallet balance');
    }
  };

  // Handle wallet connection
  const handleConnect = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await connectWallet();
      if (!result.success) {
        setError(result.error || 'Failed to connect wallet');
      }
    } catch (err) {
      setError(err.message || 'Failed to connect wallet');
    } finally {
      setLoading(false);
    }
  };

  // Handle wallet disconnection
  const handleDisconnect = () => {
    disconnectWallet();
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle form submission to create agreement
  const handleCreateAgreement = async (e) => {
    e.preventDefault();
    
    if (!isConnected) {
      setError('Please connect your wallet first');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      setTransaction(null);
      
      // Convert dates to timestamps
      const startTimestamp = Math.floor(new Date(formData.startDate).getTime() / 1000);
      const endTimestamp = Math.floor(new Date(formData.endDate).getTime() / 1000);
      
      // Convert ETH values to Wei
      const monthlyRent = parseEther(formData.monthlyRent);
      const securityDeposit = parseEther(formData.securityDeposit);
      
      // Create agreement
      const result = await createRentalAgreement(
        formData.propertyId,
        formData.landlordAddress,
        startTimestamp,
        endTimestamp,
        monthlyRent,
        securityDeposit
      );
      
      if (result.success) {
        setTransaction({
          type: 'Agreement Created',
          hash: result.transactionHash,
          agreementId: result.agreementId
        });
        
        if (result.agreementId) {
          setAgreementId(result.agreementId.toString());
        }
        
        // Refresh balance
        loadBalance();
      } else {
        setError(result.error || 'Failed to create agreement');
      }
    } catch (err) {
      setError(err.message || 'Failed to create agreement');
    } finally {
      setLoading(false);
    }
  };

  // Handle loading agreement details
  const handleLoadAgreement = async () => {
    if (!agreementId) {
      setError('Please enter an agreement ID');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const result = await getRentalAgreement(agreementId);
      
      if (result.success) {
        setAgreement(result.agreement);
      } else {
        setError(result.error || 'Failed to load agreement');
      }
    } catch (err) {
      setError(err.message || 'Failed to load agreement');
    } finally {
      setLoading(false);
    }
  };

  // Handle paying rent
  const handlePayRent = async () => {
    if (!isConnected) {
      setError('Please connect your wallet first');
      return;
    }
    
    if (!agreement) {
      setError('Please load an agreement first');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      setTransaction(null);
      
      // Pay rent with the monthly rent amount from the agreement
      const result = await payRent(agreementId, agreement.monthlyRent);
      
      if (result.success) {
        setTransaction({
          type: 'Rent Payment',
          hash: result.transactionHash
        });
        
        // Refresh balance and agreement details
        loadBalance();
        handleLoadAgreement();
      } else {
        setError(result.error || 'Failed to pay rent');
      }
    } catch (err) {
      setError(err.message || 'Failed to pay rent');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wallet-demo max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Smart Rent Wallet Demo</h2>
      
      {/* Wallet Connection */}
      <div className="mb-8 p-4 border rounded-md bg-gray-50">
        <h3 className="text-xl font-semibold mb-4">Wallet Connection</h3>
        
        {isConnected ? (
          <div>
            <div className="mb-4">
              <p className="text-sm text-gray-600">Connected Address:</p>
              <p className="font-mono bg-gray-100 p-2 rounded">{account}</p>
            </div>
            
            {balance !== null && (
              <div className="mb-4">
                <p className="text-sm text-gray-600">Balance:</p>
                <p className="font-mono bg-gray-100 p-2 rounded">{Number(balance).toFixed(6)} ETH</p>
              </div>
            )}
            
            <button
              onClick={handleDisconnect}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Disconnect Wallet
            </button>
          </div>
        ) : (
          <div>
            <p className="mb-4 text-gray-600">Connect your MetaMask wallet to interact with rental agreements.</p>
            
            <button
              onClick={handleConnect}
              disabled={loading}
              className={`
                px-4 py-2 rounded text-white
                ${loading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'}
              `}
            >
              {loading ? 'Connecting...' : 'Connect MetaMask'}
            </button>
          </div>
        )}
      </div>
      
      {/* Create Agreement Form */}
      <div className="mb-8 p-4 border rounded-md">
        <h3 className="text-xl font-semibold mb-4">Create Rental Agreement</h3>
        
        <form onSubmit={handleCreateAgreement}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Property ID</label>
              <input
                type="text"
                name="propertyId"
                value={formData.propertyId}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Landlord Address</label>
              <input
                type="text"
                name="landlordAddress"
                value={formData.landlordAddress}
                onChange={handleInputChange}
                className="w-full p-2 border rounded font-mono text-sm"
                placeholder="0x..."
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                name="startDate"
                value={formData.startDate}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date"
                name="endDate"
                value={formData.endDate}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Rent (ETH)</label>
              <input
                type="number"
                name="monthlyRent"
                value={formData.monthlyRent}
                onChange={handleInputChange}
                step="0.001"
                min="0"
                className="w-full p-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Security Deposit (ETH)</label>
              <input
                type="number"
                name="securityDeposit"
                value={formData.securityDeposit}
                onChange={handleInputChange}
                step="0.001"
                min="0"
                className="w-full p-2 border rounded"
                required
              />
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading || !isConnected}
            className={`
              px-4 py-2 rounded text-white
              ${(loading || !isConnected) ? 'bg-gray-400' : 'bg-green-500 hover:bg-green-600'}
            `}
          >
            {loading ? 'Creating...' : 'Create Agreement'}
          </button>
        </form>
      </div>
      
      {/* Agreement Details */}
      <div className="mb-8 p-4 border rounded-md">
        <h3 className="text-xl font-semibold mb-4">View Agreement Details</h3>
        
        <div className="flex space-x-4 mb-4">
          <input
            type="text"
            value={agreementId}
            onChange={(e) => setAgreementId(e.target.value)}
            placeholder="Enter Agreement ID"
            className="flex-1 p-2 border rounded"
          />
          
          <button
            onClick={handleLoadAgreement}
            disabled={loading || !agreementId}
            className={`
              px-4 py-2 rounded text-white
              ${(loading || !agreementId) ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'}
            `}
          >
            {loading ? 'Loading...' : 'Load Agreement'}
          </button>
        </div>
        
        {agreement && (
          <div className="bg-gray-50 p-4 rounded-md">
            <h4 className="font-medium mb-2">Agreement Details</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Property ID:</p>
                <p className="font-medium">{agreement.propertyId}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Status:</p>
                <p className="font-medium">
                  {agreement.status === 0 && <span className="text-yellow-600">Pending</span>}
                  {agreement.status === 1 && <span className="text-green-600">Active</span>}
                  {agreement.status === 2 && <span className="text-gray-600">Completed</span>}
                  {agreement.status === 3 && <span className="text-red-600">Cancelled</span>}
                </p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Tenant:</p>
                <p className="font-mono text-sm">{formatAddress(agreement.tenant)}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Landlord:</p>
                <p className="font-mono text-sm">{formatAddress(agreement.landlord)}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Monthly Rent:</p>
                <p className="font-medium">{formatEther(agreement.monthlyRent)} ETH</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Security Deposit:</p>
                <p className="font-medium">{formatEther(agreement.securityDeposit)} ETH</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Start Date:</p>
                <p className="font-medium">{new Date(Number(agreement.startDate) * 1000).toLocaleDateString()}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">End Date:</p>
                <p className="font-medium">{new Date(Number(agreement.endDate) * 1000).toLocaleDateString()}</p>
              </div>
              
              {Number(agreement.lastPaymentDate) > 0 && (
                <div>
                  <p className="text-sm text-gray-600">Last Payment:</p>
                  <p className="font-medium">{new Date(Number(agreement.lastPaymentDate) * 1000).toLocaleDateString()}</p>
                </div>
              )}
            </div>
            
            {/* Pay Rent Button */}
            <div className="mt-4">
              <button
                onClick={handlePayRent}
                disabled={loading || !isConnected || agreement.tenant.toLowerCase() !== account.toLowerCase()}
                className={`
                  px-4 py-2 rounded text-white
                  ${(loading || !isConnected || agreement.tenant.toLowerCase() !== account.toLowerCase()) 
                    ? 'bg-gray-400' 
                    : 'bg-indigo-500 hover:bg-indigo-600'}
                `}
              >
                {loading ? 'Processing...' : `Pay Rent (${formatEther(agreement.monthlyRent)} ETH)`}
              </button>
              
              {agreement.tenant.toLowerCase() !== account.toLowerCase() && (
                <p className="mt-2 text-sm text-red-500">
                  Only the tenant can pay rent for this agreement
                </p>
              )}
            </div>
          </div>
        )}
      </div>
      
      {/* Transaction Receipt */}
      {transaction && (
        <div className="p-4 border border-green-200 bg-green-50 rounded-md">
          <h3 className="text-lg font-medium text-green-800 mb-2">Transaction Successful!</h3>
          
          <div className="mb-2">
            <p className="text-sm text-gray-600">Type:</p>
            <p className="font-medium">{transaction.type}</p>
          </div>
          
          <div className="mb-2">
            <p className="text-sm text-gray-600">Transaction Hash:</p>
            <p className="font-mono text-sm break-all">{transaction.hash}</p>
          </div>
          
          {transaction.agreementId && (
            <div className="mb-2">
              <p className="text-sm text-gray-600">Agreement ID:</p>
              <p className="font-medium">{transaction.agreementId.toString()}</p>
            </div>
          )}
          
          <a 
            href={`https://etherscan.io/tx/${transaction.hash}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-2 text-indigo-600 hover:underline"
          >
            View on Etherscan
          </a>
        </div>
      )}
      
      {/* Error Display */}
      {error && (
        <div className="p-4 border border-red-200 bg-red-50 rounded-md">
          <p className="text-red-600">{error}</p>
        </div>
      )}
    </div>
  );
};

export default WalletDemo; 