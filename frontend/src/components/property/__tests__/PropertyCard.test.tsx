import React from 'react';
import { render, screen, fireEvent } from '../../../utils/test-utils';
import { PropertyCard } from '../PropertyCard';

describe('PropertyCard', () => {
  const mockProperty = {
    id: '1',
    title: 'Test Property',
    description: 'Test Description',
    price: 1,
    images: ['test.jpg'],
    bedrooms: 2,
    bathrooms: 1,
    area: 100,
    address: {
      street: '123 Test St',
      city: 'Test City',
      state: 'TS',
      postalCode: '12345',
      country: 'Test Country'
    }
  };

  it('renders property details correctly', () => {
    render(<PropertyCard property={mockProperty} />);

    expect(screen.getByText('Test Property')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('1 