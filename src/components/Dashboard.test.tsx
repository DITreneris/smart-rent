import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

// Mock the dependencies
jest.mock('../contexts/Web3Context', () => ({
  useWeb3Context: jest.fn().mockReturnValue({
    isConnected: true,
    account: '0x123',
    connect: jest.fn(),
    disconnect: jest.fn()
  })
}));

jest.mock('../components/web3/NetworkSwitch', () => ({
  NetworkSwitch: () => <div data-testid="network-switch">Network Switch</div>
}));

jest.mock('../components/property/PropertyListingForm', () => ({
  PropertyListingForm: () => <div data-testid="property-form">Property Form</div>
}));

describe('Dashboard', () => {
  it('renders dashboard when connected', () => {
    render(<Dashboard />);
    
    expect(screen.getByTestId('network-switch')).toBeInTheDocument();
    expect(screen.getByTestId('property-form')).toBeInTheDocument();
  });
}); 