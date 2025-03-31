require('@testing-library/jest-dom');

// Mock window.ethereum
Object.defineProperty(window, 'ethereum', {
  value: {
    request: jest.fn().mockResolvedValue(['0x1234567890123456789012345678901234567890']),
    on: jest.fn(),
    removeListener: jest.fn()
  },
  writable: true
});

// Mock localStorage
Object.defineProperty(window, 'localStorage', {
  value: {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn()
  },
  writable: true
});

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
  }))
});

// Silence console errors in tests
const originalConsoleError = console.error;
console.error = (...args) => {
  if (args[0] && args[0].includes && (
    args[0].includes('Warning:') || 
    args[0].includes('Error:') ||
    args[0].includes('Not implemented')
  )) {
    return;
  }
  originalConsoleError(...args);
}; 