import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { PropertyCard } from '../PropertyCard';

describe('PropertyCard', () => {
  const defaultProperty = {
    id: '1',
    title: 'Luxury Apartment',
    description: 'Beautiful apartment in downtown',
    price: 2.5,
    bedrooms: 2,
    bathrooms: 2,
    area: 1200,
    images: ['image1.jpg'],
    amenities: ['wifi', 'gym'],
    address: {
      street: '123 Main St',
      city: 'San Francisco',
      state: 'CA',
      postalCode: '94105',
      country: 'USA'
    }
  };

  it('renders property details correctly', () => {
    render(<PropertyCard property={defaultProperty} />);
    
    expect(screen.getByText('Luxury Apartment')).toBeInTheDocument();
    expect(screen.getByText('Beautiful apartment in downtown')).toBeInTheDocument();
    expect(screen.getByText('2.5 ETH/month')).toBeInTheDocument();
    expect(screen.getByText('2 bedrooms')).toBeInTheDocument();
    expect(screen.getByText('2 bathrooms')).toBeInTheDocument();
    expect(screen.getByText('1200 sq ft')).toBeInTheDocument();
    expect(screen.getByText('San Francisco, CA 94105')).toBeInTheDocument();
  });
}); 