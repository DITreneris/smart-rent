const React = require('react');
const { render, screen, fireEvent } = require('@testing-library/react');

// Simple PropertyCard component
function PropertyCard(props) {
  const { property, onClick } = props;
  
  const handleClick = () => {
    if (onClick) onClick(property);
  };
  
  return React.createElement(
    'div',
    { 
      'data-testid': 'property-card',
      onClick: handleClick,
      className: 'property-card'
    },
    [
      React.createElement('h3', { key: 'title' }, property.title),
      React.createElement('p', { key: 'price' }, `${property.price} ETH`),
      React.createElement('p', { key: 'desc' }, property.description)
    ]
  );
}

describe('PropertyCard Component', () => {
  const mockProperty = {
    id: '1',
    title: 'Luxury Apartment',
    description: 'Beautiful view',
    price: '1.5',
    owner: '0x1234567890123456789012345678901234567890'
  };
  
  test('renders property details', () => {
    render(React.createElement(PropertyCard, { property: mockProperty }));
    
    expect(screen.getByText('Luxury Apartment')).toBeInTheDocument();
    expect(screen.getByText('Beautiful view')).toBeInTheDocument();
    expect(screen.getByText('1.5 ETH')).toBeInTheDocument();
  });
  
  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(React.createElement(PropertyCard, { 
      property: mockProperty,
      onClick: handleClick
    }));
    
    fireEvent.click(screen.getByTestId('property-card'));
    expect(handleClick).toHaveBeenCalledWith(mockProperty);
  });
}); 