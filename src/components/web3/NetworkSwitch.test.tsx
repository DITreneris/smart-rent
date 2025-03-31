import React from 'react';
import { render, screen, fireEvent } from '../../test-utils';
import { NetworkSwitch } from './NetworkSwitch';

// Mock the network utilities
jest.mock('../../utils/networkUtils', () => ({
  SUPPORTED_NETWORKS: {
    '1': 'Ethereum Mainnet',
    '5': 'Goerli Testnet'
  },
  NetworkValidator: {
    switchNetwork: jest.fn().mockResolvedValue(undefined),
    isNetworkSupported: jest.fn().mockImplementation(chainId => ['1', '5'].includes(chainId)),
    getNetworkName: jest.fn().mockImplementation(chainId => 
      chainId === '1' ? 'Ethereum Mainnet' : 
      chainId === '5' ? 'Goerli Testnet' : 
      'Unknown Network'
    )
  }
}));

// Mock the Web3Context hook
jest.mock('../../contexts/Web3Context', () => ({
  useWeb3Context: jest.fn().mockReturnValue({
    chainId: '1',
    isConnected: true
  })
}));

describe('NetworkSwitch', () => {
  it('renders the network selector', () => {
    render(<NetworkSwitch />);
    expect(screen.getByText(/select network/i)).toBeInTheDocument();
  });

  it('displays the current network', () => {
    render(<NetworkSwitch />);
    expect(screen.getByText(/ethereum mainnet/i)).toBeInTheDocument();
  });
}); 