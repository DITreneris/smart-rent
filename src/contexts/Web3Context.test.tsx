import React from 'react';
import { render, screen, act, fireEvent } from '@testing-library/react';
import { Web3Provider, useWeb3Context } from './Web3Context';

// Skip this test if Web3Context is too complex for now
jest.mock('ethers', () => ({
  providers: {
    Web3Provider: jest.fn().mockImplementation(() => ({
      getSigner: jest.fn().mockReturnValue({
        getAddress: jest.fn().mockResolvedValue('0x1234567890123456789012345678901234567890'),
        getChainId: jest.fn().mockResolvedValue(1)
      }),
      getNetwork: jest.fn().mockResolvedValue({ chainId: 1, name: 'Mainnet' })
    }))
  },
  Contract: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    })
  }))
}));

// Simple test component using the context
const TestComponent = () => {
  const { isConnected, account, connect, disconnect } = useWeb3Context();
  return (
    <div>
      <div data-testid="connection-status">
        {isConnected ? 'Connected' : 'Not Connected'}
      </div>
      {account && <div data-testid="account">{account}</div>}
      <button onClick={connect}>Connect</button>
      <button onClick={disconnect}>Disconnect</button>
    </div>
  );
};

describe('Web3Context', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    window.ethereum.selectedAddress = null;
  });

  it('provides default context values', () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Not Connected');
  });

  it('connects to wallet when connect is called', async () => {
    window.ethereum.request.mockImplementation((request) => {
      if (request.method === 'eth_requestAccounts') {
        window.ethereum.selectedAddress = '0x1234567890123456789012345678901234567890';
        return Promise.resolve(['0x1234567890123456789012345678901234567890']);
      }
      return Promise.resolve();
    });

    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    await act(async () => {
      fireEvent.click(screen.getByText('Connect'));
    });
    
    expect(window.ethereum.request).toHaveBeenCalledWith({ method: 'eth_requestAccounts' });
  });
}); 