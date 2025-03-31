import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Define a property type
interface Property {
  id: string;
  title: string;
  price: string;
}

// Define a PropertyCard component
function PropertyCard({ property, onClick }: { property: Property, onClick?: (p: Property) => void }) {
  const handleClick = () => {
    if (onClick) onClick(property);
  };

  return (
    <div onClick={handleClick} data-testid="property-card">
      <h3>{property.title}</h3>
      <p>{property.price} ETH</p>
    </div>
  );
}

describe('PropertyCard', () => {
  const mockProperty = {
    id: '1',
    title: 'Apartment',
    price: '1.5'
  };

  it('renders property details', () => {
    render(<PropertyCard property={mockProperty} />);
    
    expect(screen.getByText('Apartment')).toBeInTheDocument();
    expect(screen.getByText('1.5 ETH')).toBeInTheDocument();
  });

  it('calls onClick with property when clicked', () => {
    const handleClick = jest.fn();
    render(<PropertyCard property={mockProperty} onClick={handleClick} />);
    
    fireEvent.click(screen.getByTestId('property-card'));
    expect(handleClick).toHaveBeenCalledWith(mockProperty);
  });
}); 