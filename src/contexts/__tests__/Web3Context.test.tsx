import React from 'react';
import { render, act, waitFor, screen } from '@testing-library/react';
import { Web3Provider, Web3Context } from '../Web3Context';
import { TransactionStatus } from '../../utils/transactionTracker';
import { TransactionType } from '../../types/transactions';

// Mock ethers.js
jest.mock('ethers', () => {
  return {
    ethers: {
      providers: {
        Web3Provider: jest.fn().mockImplementation(() => ({
          getNetwork: jest.fn().mockResolvedValue({ chainId: 1 }),
          getSigner: jest.fn().mockReturnValue({
            getAddress: jest.fn().mockResolvedValue('0x1234'),
          }),
        })),
      },
      ContractTransaction: jest.fn(),
    },
  };
});

// Mock the uuid library
jest.mock('uuid', () => ({
  v4: jest.fn().mockReturnValue('test-uuid-1234'),
}));

// Mock the services
jest.mock('../../services/EventMonitoringService', () => ({
  __esModule: true,
  default: {
    startMonitoring: jest.fn(),
    stopMonitoring: jest.fn(),
  },
}));

jest.mock('../../services/ReceiptService', () => ({
  __esModule: true,
  default: {
    generateReceipt: jest.fn().mockResolvedValue('https://test.com/receipt.pdf'),
    getTransactionDetails: jest.fn().mockResolvedValue({
      hash: '0xabc123',
      blockNumber: 12345,
      from: '0x1234',
      to: '0x5678',
      value: '1.5 ETH',
    }),
  },
}));

// Mock the transaction tracker
jest.mock('../../utils/transactionTracker', () => ({
  TransactionStatus: {
    PENDING: 'PENDING',
    MINING: 'MINING',
    COMPLETED: 'COMPLETED',
    FAILED: 'FAILED',
  },
  TransactionTracker: {
    trackTransaction: jest.fn().mockImplementation(async (txPromise) => {
      try {
        const tx = await txPromise;
        return {
          status: 'COMPLETED',
          hash: tx?.hash || '0xabc123',
          confirmations: 3,
        };
      } catch (error) {
        return {
          status: 'FAILED',
          hash: '',
          error: error.message,
          confirmations: 0,
        };
      }
    }),
  },
}));

// Mock window.ethereum
const mockEthereum = {
  request: jest.fn().mockImplementation(({ method }) => {
    if (method === 'eth_requestAccounts') {
      return Promise.resolve(['0x1234567890123456789012345678901234567890']);
    }
    if (method === 'eth_chainId') {
      return Promise.resolve('0x1'); // Mainnet
    }
    return Promise.reject(new Error('Method not implemented'));
  }),
  on: jest.fn(),
  removeListener: jest.fn(),
};

// Mock localStorage
const mockLocalStorage = (() => {
  let store = {};
  return {
    getItem: jest.fn(key => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();

Object.defineProperty(window, 'ethereum', {
  value: mockEthereum,
  writable: true,
});

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

// Test component that uses Web3Context
const TestComponent = () => {
  const context = React.useContext(Web3Context);
  
  if (!context) {
    return <div>No context</div>;
  }
  
  return (
    <div>
      <div data-testid="connection-status">
        {context.isConnected ? 'Connected' : 'Not Connected'}
      </div>
      <div data-testid="account">{context.account || 'No account'}</div>
      <div data-testid="chain-id">{context.chainId || 'No chain ID'}</div>
      <div data-testid="transaction-count">{context.transactions.length}</div>
      <button data-testid="connect-btn" onClick={context.connect}>
        Connect
      </button>
      <button
        data-testid="add-transaction-btn"
        onClick={() =>
          context.addTransaction({
            hash: '0xabc123',
            status: TransactionStatus.COMPLETED,
            description: 'Test Transaction',
            type: TransactionType.PROPERTY_LISTING,
          })
        }
      >
        Add Transaction
      </button>
      <button
        data-testid="track-transaction-btn"
        onClick={() =>
          context.trackTransaction(
            Promise.resolve({
              hash: '0xabc123',
              wait: jest.fn().mockResolvedValue({
                confirmations: 3,
              }),
            }),
            {
              type: TransactionType.PROPERTY_LISTING,
              description: 'Track Test Transaction',
            }
          )
        }
      >
        Track Transaction
      </button>
      <button
        data-testid="generate-receipt-btn"
        onClick={() => {
          const tx = context.transactions[0];
          if (tx) {
            context.generateReceipt(tx.id);
          }
        }}
      >
        Generate Receipt
      </button>
    </div>
  );
};

describe('Web3Context', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.clear();
  });

  it('initializes with disconnected state', () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Not Connected');
    expect(screen.getByTestId('account')).toHaveTextContent('No account');
    expect(screen.getByTestId('chain-id')).toHaveTextContent('No chain ID');
    expect(screen.getByTestId('transaction-count')).toHaveTextContent('0');
  });

  it('connects to wallet when connect is called', async () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    await act(async () => {
      screen.getByTestId('connect-btn').click();
    });
    
    expect(window.ethereum.request).toHaveBeenCalledWith({ method: 'eth_requestAccounts' });
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Connected');
    expect(screen.getByTestId('account')).toHaveTextContent('0x1234567890123456789012345678901234567890');
    expect(screen.getByTestId('chain-id')).toHaveTextContent('1');
  });

  it('adds a transaction', async () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    expect(screen.getByTestId('transaction-count')).toHaveTextContent('0');
    
    await act(async () => {
      screen.getByTestId('add-transaction-btn').click();
    });
    
    expect(screen.getByTestId('transaction-count')).toHaveTextContent('1');
    expect(mockLocalStorage.setItem).toHaveBeenCalled();
  });

  it('tracks a transaction through its lifecycle', async () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    await act(async () => {
      screen.getByTestId('track-transaction-btn').click();
    });
    
    expect(screen.getByTestId('transaction-count')).toHaveTextContent('1');
  });

  it('generates a receipt for a completed transaction', async () => {
    render(
      <Web3Provider>
        <TestComponent />
      </Web3Provider>
    );
    
    // First add a transaction
    await act(async () => {
      screen.getByTestId('add-transaction-btn').click();
    });
    
    // Then generate a receipt
    await act(async () => {
      screen.getByTestId('generate-receipt-btn').click();
    });
    
    // Check that the receipt service was called
    expect(require('../../services/ReceiptService').default.generateReceipt).toHaveBeenCalled();
  });
}); 