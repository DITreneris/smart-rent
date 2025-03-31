import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Web3Provider, useWeb3Context } from '../contexts/Web3Context';

// Mock ethereum provider
const mockEthereum = {
  request: jest.fn(),
  on: jest.fn(),
  removeListener: jest.fn(),
};

// Component that uses Web3Context
const TestComponent = () => {
  const { account, isConnected, connect, disconnect } = useWeb3Context();
  
  return (
    <div>
      <div data-testid="connection-status">
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>
      {account && <div data-testid="account">{account}</div>}
      <button onClick={connect} data-testid="connect-button">
        Connect
      </button>
      <button onClick={disconnect} data-testid="disconnect-button">
        Disconnect
      </button>
    </div>
  );
};

describe('Web3Context', () => {
  beforeEach(() => {
    // Setup global ethereum object
    global.ethereum = mockEthereum;
    
    // Reset mocks
    jest.clearAllMocks();
  });
  
  it('should show disconnected state initially', () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Disconnected');
    expect(screen.queryByTestId('account')).not.toBeInTheDocument();
  });
  
  it('should connect to wallet when connect button is clicked', async () => {
    // Mock successful connection
    mockEthereum.request
      .mockResolvedValueOnce(['0x123456789abcdef']) // eth_requestAccounts
      .mockResolvedValueOnce('0x1'); // eth_chainId
    
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    // Click connect button
    fireEvent.click(screen.getByTestId('connect-button'));
    
    // Wait for connection to complete
    await waitFor(() => {
      expect(screen.getByTestId('connection-status')).toHaveTextContent('Connected');
    });
    
    expect(screen.getByTestId('account')).toHaveTextContent('0x123456789abcdef');
    expect(mockEthereum.request).toHaveBeenCalledTimes(2);
  });
  
  it('should disconnect when disconnect button is clicked', async () => {
    // Setup initial connected state
    mockEthereum.request
      .mockResolvedValueOnce(['0x123456789abcdef'])
      .mockResolvedValueOnce('0x1');
    
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    // Connect first
    fireEvent.click(screen.getByTestId('connect-button'));
    await waitFor(() => {
      expect(screen.getByTestId('connection-status')).toHaveTextContent('Connected');
    });
    
    // Now disconnect
    fireEvent.click(screen.getByTestId('disconnect-button'));
    
    // Check disconnected state
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Disconnected');
    expect(screen.queryByTestId('account')).not.toBeInTheDocument();
  });
}); 
    // Mock ethereum provider
    global.ethereum = {
      request: jest.fn(),
      on: jest.fn(),
      removeListener: jest.fn(),
    };
  });

  it('should connect wallet successfully', async () => {
    global.ethereum.request
      .mockImplementationOnce(() => Promise.resolve(['0x123']))
      .mockImplementationOnce(() => Promise.resolve('0x1'));

    const { result } = renderHook(() => useContext(Web3Context), {
      wrapper: Web3Provider,
    });

    await act(async () => {
      await result.current.connect();
    });

    expect(result.current.account).toBe('0x123');
    expect(result.current.isConnected).toBe(true);
  });
}); 