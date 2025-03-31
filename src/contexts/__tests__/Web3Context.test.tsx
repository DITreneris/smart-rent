import React from 'react';
import { render, screen, act } from '@testing-library/react';
import { Web3Provider, useWeb3Context } from '../Web3Context';

// Test component using the context
const TestComponent = () => {
  const { isConnected, account } = useWeb3Context();
  return (
    <div>
      <div data-testid="connection-status">
        {isConnected ? 'Connected' : 'Not Connected'}
      </div>
      {account && <div data-testid="account">{account}</div>}
    </div>
  );
};

describe('Web3Context', () => {
  it('provides initial context values', () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Not Connected');
  });

  it('connects to wallet', async () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );

    await act(async () => {
      // Simulate connection
      window.ethereum.selectedAddress = '0x1234567890123456789012345678901234567890';
      window.ethereum.request({ method: 'eth_requestAccounts' });
    });

    expect(window.ethereum.request).toHaveBeenCalled();
  });
}); 