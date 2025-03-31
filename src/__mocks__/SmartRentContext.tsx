import React from 'react';

// Mock all your context providers here
export const Web3Context = React.createContext({
  isConnected: false,
  account: null,
  connect: jest.fn(),
  disconnect: jest.fn(),
  chainId: '1',
  provider: null
});

export const AuthContext = React.createContext({
  isLoggedIn: false,
  user: null,
  login: jest.fn(),
  logout: jest.fn(),
  register: jest.fn()
});

export const PropertyContext = React.createContext({
  properties: [],
  loading: false,
  error: null,
  addProperty: jest.fn(),
  getProperties: jest.fn(),
  getProperty: jest.fn()
});

// Create a wrapper for all providers
export const AllProviders = ({ children }) => (
  <Web3Context.Provider value={{
    isConnected: false,
    account: null,
    connect: jest.fn(),
    disconnect: jest.fn(),
    chainId: '1',
    provider: null
  }}>
    <AuthContext.Provider value={{
      isLoggedIn: false,
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      register: jest.fn()
    }}>
      <PropertyContext.Provider value={{
        properties: [],
        loading: false,
        error: null,
        addProperty: jest.fn(),
        getProperties: jest.fn(),
        getProperty: jest.fn()
      }}>
        {children}
      </PropertyContext.Provider>
    </AuthContext.Provider>
  </Web3Context.Provider>
); 