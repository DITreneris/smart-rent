import React, { ReactElement } from 'react';
import { render as rtlRender } from '@testing-library/react';
import { Web3Provider } from '../contexts/Web3Context';
import { AuthProvider } from '../contexts/AuthContext';
import { BrowserRouter } from 'react-router-dom';

function render(ui: ReactElement, { ...renderOptions } = {}) {
  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <BrowserRouter>
        <AuthProvider>
          <Web3Provider>
            {children}
          </Web3Provider>
        </AuthProvider>
      </BrowserRouter>
    );
  }
  return rtlRender(ui, { wrapper: Wrapper, ...renderOptions });
}

// Mock Web3 provider
export const mockWeb3Provider = {
  request: jest.fn(),
  on: jest.fn(),
  removeListener: jest.fn(),
};

// Mock contract responses
export const mockContractCalls = {
  listProperty: jest.fn(),
  rentProperty: jest.fn(),
  getProperties: jest.fn(),
};

export * from '@testing-library/react';
export { render }; 