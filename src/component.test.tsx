import React from 'react';
import { render, screen } from '@testing-library/react';

// Define the component right in the test file
function HelloWorld() {
  return <div>Hello, world!</div>;
}

describe('Hello World Component', () => {
  it('renders without crashing', () => {
    render(<HelloWorld />);
    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
  });
}); 