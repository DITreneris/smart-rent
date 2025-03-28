import React, { useState } from 'react';
import { useWeb3 } from '../../contexts/Web3Context';

const WalletConnect = ({ onWalletConnected }) => {
  const { isConnected, account, connectWallet, disconnectWallet, formatAddress, error } = useWeb3();
  const [connecting, setConnecting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleConnect = async () => {
    try {
      setConnecting(true);
      setErrorMessage('');
      
      const result = await connectWallet();
      
      if (result?.success) {
        if (onWalletConnected) {
          onWalletConnected({ address: result.address });
        }
      } else if (result?.error) {
        setErrorMessage(result.error);
      }
    } catch (err) {
      setErrorMessage('Failed to connect wallet. Please try again.');
      console.error(err);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = () => {
    disconnectWallet();
  };

  return (
    <div className="wallet-connect p-4 bg-white rounded-md">
      {!window.ethereum ? (
        <div className="mb-4">
          <p className="text-red-500 mb-2">MetaMask is not installed</p>
          <a 
            href="https://metamask.io/download.html" 
            target="_blank" 
            rel="noopener noreferrer"
            className="btn-primary inline-block"
          >
            Install MetaMask
          </a>
        </div>
      ) : isConnected ? (
        <div>
          <div className="mb-4 p-3 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-600">Connected Wallet</p>
            <p className="font-mono">{formatAddress(account)}</p>
          </div>
          
          <button 
            onClick={handleDisconnect}
            className="btn-secondary w-full"
          >
            Disconnect Wallet
          </button>
        </div>
      ) : (
        <div>
          <button 
            onClick={handleConnect}
            className="btn-primary w-full"
            disabled={connecting}
          >
            {connecting ? 'Connecting...' : 'Connect MetaMask'}
          </button>
          
          {(errorMessage || error) && (
            <p className="mt-2 text-red-500 text-sm">{errorMessage || error}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default WalletConnect; 