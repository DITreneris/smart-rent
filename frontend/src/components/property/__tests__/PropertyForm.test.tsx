import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../../utils/test-utils';
import { PropertyForm } from '../PropertyForm';
import { useWeb3Context } from '../../../contexts/Web3Context';

jest.mock('../../../contexts/Web3Context');

describe('PropertyForm', () => {
  beforeEach(() => {
    (useWeb3Context as jest.Mock).mockReturnValue({
      isConnected: true,
      account: '0x123'
    });
  });

  it('validates required fields', async () => {
    render(<PropertyForm onSubmit={jest.fn()} />);
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
      expect(screen.getByText('Price is required')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    const onSubmit = jest.fn();
    render(<PropertyForm onSubmit={onSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Test Property' }
    });
    
    fireEvent.change(screen.getByLabelText(/price/i), {
      target: { value: '1' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Test Property',
          price: 1
        })
      );
    });
  });
}); 