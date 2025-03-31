import React from 'react';
import { SUPPORTED_NETWORKS } from '../../utils/networkUtils';
import { useWeb3Context } from '../../contexts/Web3Context';

export const NetworkSwitch: React.FC = () => {
  const { chainId, networkError } = useWeb3Context();
  const provider = new ethers.providers.Web3Provider(window.ethereum);

  const handleNetworkSwitch = async (targetChainId: number) => {
    try {
      await NetworkValidator.switchNetwork(provider, targetChainId);
    } catch (error) {
      console.error('Failed to switch network:', error);
    }
  };

  return (
    <div className="network-switch">
      <select
        value={chainId || ''}
        onChange={(e) => handleNetworkSwitch(Number(e.target.value))}
        className="network-select"
      >
        <option value="">Select Network</option>
        {Object.entries(SUPPORTED_NETWORKS).map(([id, name]) => (
          <option key={id} value={id}>
            {name}
          </option>
        ))}
      </select>
      {networkError && (
        <div className="network-error">
          {networkError}
        </div>
      )}
    </div>
  );
}; 