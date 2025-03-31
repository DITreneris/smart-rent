import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Define a simple Button component for testing
interface ButtonProps {
  onClick?: () => void;
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

function Button({ onClick, children, disabled, className }: ButtonProps) {
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={className}
    >
      {children}
    </button>
  );
}

describe('Button Component', () => {
  it('renders with children', () => {
    render(<Button>Test Button</Button>);
    expect(screen.getByText('Test Button')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('respects disabled prop', () => {
    const handleClick = jest.fn();
    render(
      <Button onClick={handleClick} disabled>
        Disabled Button
      </Button>
    );
    
    const button = screen.getByText('Disabled Button');
    expect(button).toBeDisabled();
    
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Styled Button</Button>);
    const button = screen.getByText('Styled Button');
    expect(button).toHaveClass('custom-class');
  });
}); 