import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { PropertyForm } from './PropertyForm';

describe('PropertyForm', () => {
  it('renders the form', () => {
    render(<PropertyForm onSubmit={() => {}} />);
    // Verify basic form elements
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/price/i)).toBeInTheDocument();
  });
}); 