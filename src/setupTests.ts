import '@testing-library/jest-dom';
import 'whatwg-fetch';
import { configure } from '@testing-library/react';

// Configure testing library with longer timeout for async operations
configure({
  asyncUtilTimeout: 5000,
});

// Silence React warnings
const originalConsoleError = console.error;
console.error = (...args) => {
  if (args[0]?.includes?.('Warning:') || 
      args[0]?.includes?.('Not implemented:') || 
      args[0]?.includes?.('Error boundaries')) {
    return;
  }
  originalConsoleError(...args);
};

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = String(value);
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    length: 0,
    key: jest.fn((i) => Object.keys(store)[i] || null)
  };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock for window.ethereum
const ethereumMock = {
  isMetaMask: true,
  selectedAddress: '0x1234567890123456789012345678901234567890',
  networkVersion: '1',
  chainId: '0x1',
  request: jest.fn().mockResolvedValue(['0x1234567890123456789012345678901234567890']),
  on: jest.fn(),
  removeListener: jest.fn()
};

Object.defineProperty(window, 'ethereum', { value: ethereumMock });

// Mock fetch API
global.fetch = jest.fn(() => 
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
    status: 200
  })
) as jest.Mock;

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
  })),
});

// Mock Web3Provider props
jest.mock('ethers', () => ({
  Contract: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    }),
    rentProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    })
  })),
  providers: {
    Web3Provider: jest.fn().mockImplementation(() => ({
      getSigner: jest.fn()
    }))
  },
  utils: {
    parseEther: jest.fn().mockReturnValue('1000000000000000000'),
    formatEther: jest.fn().mockReturnValue('1.0')
  }
}));

// Mock contexts
jest.mock('../src/contexts/Web3Context', () => ({
  useWeb3Context: jest.fn().mockReturnValue({
    isConnected: false,
    account: null,
    chainId: null,
    connect: jest.fn(),
    disconnect: jest.fn(),
    networkError: null
  })
}));

// Mock IntersectionObserver
class MockIntersectionObserver {
  observe = jest.fn();
  unobserve = jest.fn();
  disconnect = jest.fn();
  root = null;
  rootMargin = '';
  thresholds = [];
}

Object.defineProperty(window, 'IntersectionObserver', {
  writable: true,
  configurable: true,
  value: MockIntersectionObserver
});

// Mock ResizeObserver
class ResizeObserver {
  observe = jest.fn();
  unobserve = jest.fn();
  disconnect = jest.fn();
}

Object.defineProperty(window, 'ResizeObserver', {
  writable: true,
  configurable: true,
  value: ResizeObserver,
});

// Global beforeEach to clear mocks
beforeEach(() => {
  jest.clearAllMocks();
});

// Clean up after each test
afterEach(() => {
  jest.restoreAllMocks();
});

// Only the absolute essentials
window.matchMedia = window.matchMedia || function() {
  return {
    matches: false,
    addListener: function() {},
    removeListener: function() {}
  };
}; 