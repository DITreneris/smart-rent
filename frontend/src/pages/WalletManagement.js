import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useWeb3 } from '../contexts/Web3Context';
import { useAuth } from '../contexts/AuthContext';
import WalletConnect from '../components/wallet/WalletConnect';
import { FaEthereum, FaExchangeAlt, FaCopy, FaCheckCircle } from 'react-icons/fa';

const WalletManagement = () => {
  const { currentUser } = useAuth();
  const { 
    account, 
    balance, 
    isConnected, 
    connectWallet, 
    disconnectWallet, 
    getBalance,
    formatAddress,
    signMessage
  } = useWeb3();
  const [walletHistory, setWalletHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [signResult, setSignResult] = useState(null);
  const [message, setMessage] = useState('');
  const [transaction, setTransaction] = useState(null);
  
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect if not authenticated
    if (!currentUser) {
      navigate('/login');
    }
    
    // Fetch wallet balance if connected
    const fetchBalance = async () => {
      if (isConnected && account) {
        await getBalance(account);
      }
    };
    
    fetchBalance();
    
    // Basic wallet history (simplified for MVP)
    if (isConnected && account) {
      setWalletHistory([
        { 
          date: new Date().toISOString().split('T')[0], 
          action: 'Connected Wallet', 
          details: `Connected wallet ${formatAddress(account)}`
        }
      ]);
    }
  }, [currentUser, navigate, isConnected, account, getBalance, formatAddress]);

  const handleWalletConnected = (walletData) => {
    setWalletHistory([
      {
        date: new Date().toISOString().split('T')[0],
        action: 'Connected Wallet',
        details: `Connected wallet ${formatAddress(walletData.address)}`
      }
    ]);
  };

  const handleDisconnectWallet = () => {
    disconnectWallet();
  };

  const handleCopyAddress = () => {
    if (account) {
      navigator.clipboard.writeText(account);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleSignMessage = async () => {
    if (!message) return;
    
    setLoading(true);
    try {
      const result = await signMessage(message);
      setSignResult(result);
    } catch (err) {
      console.error('Error signing message:', err);
      setSignResult({ success: false, error: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleTestTransaction = async () => {
    setLoading(true);
    // In a real app, this would send a real transaction
    // For demo, we'll just simulate one
    try {
      setTimeout(() => {
        setTransaction({
          hash: '0x' + Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
          success: true,
          timestamp: new Date().toISOString()
        });
        setLoading(false);
      }, 2000);
    } catch (err) {
      console.error('Error with test transaction:', err);
      setTransaction({ success: false, error: 'Transaction failed' });
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Crypto Wallet Management</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Left column - Wallet Status */}
        <div className="md:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Wallet Status</h2>
            
            {isConnected ? (
              <div>
                <div className="flex items-center justify-between mb-6 p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Connected Address</p>
                    <div className="flex items-center">
                      <p className="font-mono text-sm mr-2">{formatAddress(account)}</p>
                      <button 
                        onClick={handleCopyAddress}
                        className="text-blue-500 hover:text-blue-700"
                        title="Copy address"
                      >
                        {copied ? <FaCheckCircle className="text-green-500" /> : <FaCopy />}
                      </button>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500 mb-1">Balance</p>
                    <div className="flex items-center text-lg font-semibold">
                      <FaEthereum className="mr-1 text-blue-500" />
                      <span>{balance ? parseFloat(balance).toFixed(4) : '0.0000'} ETH</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex space-x-4">
                  <button
                    onClick={handleTestTransaction}
                    disabled={loading}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md font-medium flex items-center justify-center"
                  >
                    <FaExchangeAlt className="mr-2" />
                    {loading ? 'Processing...' : 'Test Transaction'}
                  </button>
                  
                  <button
                    onClick={handleDisconnectWallet}
                    className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 px-4 rounded-md font-medium"
                  >
                    Disconnect Wallet
                  </button>
                </div>
                
                {transaction && (
                  <div className={`mt-6 p-4 rounded-md ${transaction.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <h3 className={`font-medium ${transaction.success ? 'text-green-800' : 'text-red-800'}`}>
                      {transaction.success ? 'Transaction Successful' : 'Transaction Failed'}
                    </h3>
                    {transaction.success && (
                      <div className="mt-2">
                        <p className="text-sm text-gray-600">Hash: <span className="font-mono">{transaction.hash.substring(0, 20)}...</span></p>
                        <p className="text-sm text-gray-600">Time: {new Date(transaction.timestamp).toLocaleString()}</p>
                      </div>
                    )}
                    {!transaction.success && <p className="mt-2 text-sm text-red-700">{transaction.error}</p>}
                  </div>
                )}
                
                <div className="mt-8 border-t pt-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Sign Message</h3>
                  <div className="mb-4">
                    <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                    <textarea
                      id="message"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder="Enter a message to sign"
                      className="w-full p-2 border border-gray-300 rounded-md"
                      rows={3}
                    ></textarea>
                  </div>
                  <button
                    onClick={handleSignMessage}
                    disabled={!message || loading}
                    className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md font-medium disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Signing...' : 'Sign Message'}
                  </button>
                  
                  {signResult && (
                    <div className={`mt-4 p-4 rounded-md ${signResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                      {signResult.success ? (
                        <div>
                          <p className="font-medium text-green-800 mb-2">Message signed successfully!</p>
                          <p className="text-xs font-mono break-all text-gray-600">{signResult.signature}</p>
                        </div>
                      ) : (
                        <p className="text-red-700">{signResult.error}</p>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div>
                <p className="text-gray-600 mb-4">
                  Connect your Ethereum wallet to interact with smart contracts for property rentals.
                </p>
                <button
                  onClick={connectWallet}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-md font-medium flex items-center justify-center"
                >
                  <FaEthereum className="mr-2" />
                  Connect Wallet
                </button>
              </div>
            )}
          </div>
          
          {/* Help section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Need Help?</h2>
            <p className="text-gray-600 mb-4">
              New to crypto wallets? Here are some resources to get you started:
            </p>
            <ul className="text-sm text-gray-600 space-y-2">
              <li>
                <a href="https://metamask.io/download/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                  • Download MetaMask
                </a>
              </li>
              <li>
                <a href="https://ethereum.org/en/wallets/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                  • Learn about Ethereum wallets
                </a>
              </li>
              <li>
                <a href="https://ethereum.org/en/what-is-ethereum/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                  • What is Ethereum?
                </a>
              </li>
            </ul>
          </div>
        </div>
        
        {/* Right column - About Smart Contracts & Wallet Activity */}
        <div className="md:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Smart Rent & Blockchain</h2>
            <p className="text-gray-600 mb-4">
              The Smart Rent platform uses blockchain technology to provide secure, transparent rental agreements without intermediaries.
            </p>
            
            <h3 className="font-semibold mb-2">Benefits of connecting your wallet:</h3>
            <ul className="list-disc pl-5 mb-4 text-gray-600">
              <li>Create and sign rental contracts directly on the blockchain</li>
              <li>Make secure rental payments with cryptocurrency</li>
              <li>Verify your identity through your wallet</li>
              <li>Access rental history that's immutable and transparent</li>
            </ul>
            
            <Link to="/properties" className="btn-primary inline-block mt-2">
              Browse Available Properties
            </Link>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Recent Wallet Activity</h2>
            
            {walletHistory.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {walletHistory.map((activity, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{activity.date}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{activity.action}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{activity.details}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-6 border-2 border-dashed border-gray-200 rounded-lg">
                <p className="text-gray-500">No wallet activity to display. Connect your wallet to get started.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WalletManagement; 