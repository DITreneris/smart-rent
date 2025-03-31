import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Mock Web3 context values
const mockWeb3Context = {
  isConnected: false,
  account: null,
  connect: jest.fn().mockResolvedValue(undefined),
  disconnect: jest.fn(),
  chainId: '1',
  balance: '0',
  isConnecting: false,
  error: null
};

// Create Web3Context
export const Web3Context = React.createContext(mockWeb3Context);

// All providers wrapper
const AllProviders = ({ children }) => {
  return (
    <BrowserRouter>
      <Web3Context.Provider value={mockWeb3Context}>
        {children}
      </Web3Context.Provider>
    </BrowserRouter>
  );
};

// Custom render with all providers
const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllProviders, ...options });

// Export everything
export * from '@testing-library/react';
export { customRender as render };

// Commonly used test data
export const mockProperties = [
  {
    id: '1',
    title: 'Luxury Apartment',
    description: 'Beautiful apartment in downtown',
    price: '1.5',
    image: 'https://example.com/apartment.jpg',
    owner: '0x1234567890123456789012345678901234567890'
  },
  {
    id: '2',
    title: 'Beach House',
    description: 'Relaxing beach house with ocean view',
    price: '2.5',
    image: 'https://example.com/beach.jpg',
    owner: '0x1234567890123456789012345678901234567890'
  }
];

// Mock contract interactions
export const mockContractMethods = {
  listProperty: jest.fn().mockResolvedValue({
    wait: jest.fn().mockResolvedValue({ status: 1 })
  }),
  rentProperty: jest.fn().mockResolvedValue({
    wait: jest.fn().mockResolvedValue({ status: 1 })
  })
}; 