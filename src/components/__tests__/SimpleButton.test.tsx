import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Simple Button component for testing
const SimpleButton = ({ 
  onClick = () => {}, 
  children = 'Click me',
  className = '' 
}) => (
  <button 
    onClick={onClick} 
    className={className}
  >
    {children}
  </button>
);

describe('SimpleButton', () => {
  it('renders correctly', () => {
    render(<SimpleButton>Test Button</SimpleButton>);
    expect(screen.getByText('Test Button')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<SimpleButton onClick={handleClick}>Click Me</SimpleButton>);
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies custom className', () => {
    render(<SimpleButton className="custom-class">Test Button</SimpleButton>);
    expect(screen.getByText('Test Button')).toHaveClass('custom-class');
  });
}); 