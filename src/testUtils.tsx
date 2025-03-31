import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AllProviders } from './__mocks__/SmartRentContext';

// Custom render function that includes all providers
const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: ({ children }) => (
  <BrowserRouter>
    <AllProviders>{children}</AllProviders>
  </BrowserRouter>
), ...options });

// Export everything from testing-library
export * from '@testing-library/react';

// Override render method
export { customRender as render };

// Common test data
export const mockProperties = [
  {
    id: '1',
    title: 'Luxury Apartment',
    description: 'A beautiful apartment in the city center',
    price: '1.5',
    image: 'https://example.com/image.jpg',
    owner: '0x1234567890123456789012345678901234567890'
  },
  {
    id: '2',
    title: 'Cozy House',
    description: 'A cozy house in the suburbs',
    price: '2.5',
    image: 'https://example.com/image2.jpg',
    owner: '0x1234567890123456789012345678901234567890'
  }
];

export const mockUser = {
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
  wallet: '0x1234567890123456789012345678901234567890'
};

// Mock contract interface
export const mockContract = {
  listProperty: jest.fn().mockResolvedValue({
    wait: jest.fn().mockResolvedValue({ status: 1 })
  }),
  rentProperty: jest.fn().mockResolvedValue({
    wait: jest.fn().mockResolvedValue({ status: 1 })
  })
}; 