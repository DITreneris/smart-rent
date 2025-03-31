import React from 'react';
import { render, screen } from '../testUtils';

const SimpleComponent = () => <div>Simple Test Component</div>;

describe('SimpleComponent', () => {
  it('renders without crashing', () => {
    render(<SimpleComponent />);
    expect(screen.getByText('Simple Test Component')).toBeInTheDocument();
  });
}); 