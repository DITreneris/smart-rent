import { render, screen } from '@testing-library/react';
import App from './App';
import { BrowserRouter } from 'react-router-dom';

// Mock the Web3Context
jest.mock('./contexts/Web3Context', () => ({
  Web3Provider: ({ children }) => <>{children}</>,
  useWeb3Context: () => ({
    isConnected: false,
    account: null,
    connect: jest.fn(),
    disconnect: jest.fn(),
    chainId: '1'
  })
}));

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    // Check for something basic that should always be in your app
    expect(document.body).toBeInTheDocument();
  });
}); 