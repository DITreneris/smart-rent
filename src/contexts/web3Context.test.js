const React = require('react');
const { render, screen, fireEvent, act } = require('@testing-library/react');

// Mock ethereum object
const ethereumMock = {
  request: jest.fn(),
  on: jest.fn(),
  removeListener: jest.fn(),
  isMetaMask: true
};

// Save original window.ethereum
const originalEthereum = window.ethereum;

beforeEach(() => {
  // Reset mocks
  jest.clearAllMocks();
  
  // Setup ethereum mock
  ethereumMock.request.mockImplementation((request) => {
    if (request.method === 'eth_requestAccounts') {
      return Promise.resolve(['0x1234567890123456789012345678901234567890']);
    }
    if (request.method === 'eth_chainId') {
      return Promise.resolve('0x1');
    }
    return Promise.resolve(null);
  });
  
  // Set window.ethereum
  window.ethereum = ethereumMock;
});

afterEach(() => {
  // Restore window.ethereum
  window.ethereum = originalEthereum;
});

// Simple Web3 context
const Web3Context = React.createContext({
  isConnected: false,
  account: null,
  connect: () => {},
  disconnect: () => {}
});

// Web3 provider component
function Web3Provider({ children }) {
  const [isConnected, setIsConnected] = React.useState(false);
  const [account, setAccount] = React.useState(null);
  
  const connect = async () => {
    try {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      if (accounts && accounts.length > 0) {
        setAccount(accounts[0]);
        setIsConnected(true);
      }
    } catch (error) {
      console.error(error);
    }
  };
  
  const disconnect = () => {
    setAccount(null);
    setIsConnected(false);
  };
  
  const value = {
    isConnected,
    account,
    connect,
    disconnect
  };
  
  return React.createElement(
    Web3Context.Provider,
    { value },
    children
  );
}

// Simple test component
function TestComponent() {
  const { isConnected, account, connect, disconnect } = React.useContext(Web3Context);
  
  return React.createElement(
    'div',
    null,
    [
      React.createElement(
        'div',
        { 'data-testid': 'connection-status', key: 'status' },
        isConnected ? 'Connected' : 'Not Connected'
      ),
      account && React.createElement(
        'div',
        { 'data-testid': 'account', key: 'account' },
        account
      ),
      React.createElement(
        'button',
        { onClick: connect, key: 'connect' },
        'Connect'
      ),
      React.createElement(
        'button',
        { onClick: disconnect, key: 'disconnect' },
        'Disconnect'
      )
    ]
  );
}

describe('Web3Context', () => {
  test('initializes with disconnected state', () => {
    render(React.createElement(
      Web3Provider,
      null,
      React.createElement(TestComponent)
    ));
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Not Connected');
    expect(screen.queryByTestId('account')).not.toBeInTheDocument();
  });
  
  test('connects to wallet when connect is called', async () => {
    render(React.createElement(
      Web3Provider,
      null,
      React.createElement(TestComponent)
    ));
    
    await act(async () => {
      fireEvent.click(screen.getByText('Connect'));
    });
    
    expect(window.ethereum.request).toHaveBeenCalledWith({ method: 'eth_requestAccounts' });
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Connected');
    expect(screen.getByTestId('account')).toHaveTextContent('0x1234567890123456789012345678901234567890');
  });
  
  test('disconnects from wallet when disconnect is called', async () => {
    render(React.createElement(
      Web3Provider,
      null,
      React.createElement(TestComponent)
    ));
    
    // First connect
    await act(async () => {
      fireEvent.click(screen.getByText('Connect'));
    });
    
    // Then disconnect
    await act(async () => {
      fireEvent.click(screen.getByText('Disconnect'));
    });
    
    expect(screen.getByTestId('connection-status')).toHaveTextContent('Not Connected');
    expect(screen.queryByTestId('account')).not.toBeInTheDocument();
  });
}); 