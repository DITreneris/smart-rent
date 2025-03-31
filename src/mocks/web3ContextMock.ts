export const mockWeb3Context = {
  isConnected: false,
  account: null,
  connect: jest.fn(),
  disconnect: jest.fn(),
  chainId: '1',
  balance: '0',
  provider: null,
  isConnecting: false,
  error: null
};

// This exports a mock module
const mockModule = {
  useWeb3Context: () => mockWeb3Context,
  Web3Provider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  __esModule: true,
};

export default mockModule; 