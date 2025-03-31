import React from 'react';
import { render, screen, fireEvent } from '../testUtils';
import PropertyCard from '../components/PropertyCard';

describe('PropertyCard Component', () => {
  const mockProperty = {
    id: '1',
    title: 'Luxury Apartment',
    description: 'A beautiful apartment in the city center',
    price: '1.5',
    image: 'https://example.com/image.jpg',
    owner: '0x1234567890123456789012345678901234567890'
  };

  it('renders property details correctly', () => {
    render(<PropertyCard property={mockProperty} />);
    
    expect(screen.getByText('Luxury Apartment')).toBeInTheDocument();
    expect(screen.getByText('A beautiful apartment in the city center')).toBeInTheDocument();
    expect(screen.getByText('1.5 ETH')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<PropertyCard property={mockProperty} onClick={handleClick} />);
    
    fireEvent.click(screen.getByText('Luxury Apartment'));
    expect(handleClick).toHaveBeenCalledWith(mockProperty);
  });

  it('displays a default image when image fails to load', () => {
    render(<PropertyCard property={{...mockProperty, image: 'invalid-url'}} />);
    
    const img = screen.getByAltText('Luxury Apartment');
    fireEvent.error(img);
    
    // Check if fallback image is used
    expect(img.getAttribute('src')).toContain('default-property.jpg');
  });
}); 