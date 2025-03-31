import React from 'react';
import { render } from '@testing-library/react';
import { PropertyListingForm } from '../PropertyListingForm';
import { Web3Provider } from '../../../contexts/Web3Context';
import { AuthProvider } from '../../../contexts/AuthContext';

// Mock the property service
jest.mock('../../../services/PropertyService', () => ({
  usePropertyService: jest.fn().mockReturnValue({
    createProperty: jest.fn()
  })
}));

describe('PropertyListingForm', () => {
  it('renders without crashing', () => {
    render(
      <AuthProvider>
        <Web3Provider>
          <PropertyListingForm />
        </Web3Provider>
      </AuthProvider>
    );
  });
}); 