import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Define Button right in the test
function Button({ onClick = () => {}, children = 'Click me' }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}

describe('Button Component', () => {
  it('renders with text', () => {
    render(<Button>Test Button</Button>);
    expect(screen.getByText('Test Button')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
}); 