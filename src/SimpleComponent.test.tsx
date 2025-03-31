import React from 'react';
import { render, screen } from '@testing-library/react';

// Super simple component
const SimpleComponent = () => <div>Simple Component</div>;

describe('SimpleComponent', () => {
  it('renders without crashing', () => {
    render(<SimpleComponent />);
    expect(screen.getByText('Simple Component')).toBeInTheDocument();
  });
}); 