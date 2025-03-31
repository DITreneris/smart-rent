// Define simple utility functions for testing
function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

function truncateText(text: string, maxLength: number): string {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

describe('Format Utilities', () => {
  describe('formatCurrency', () => {
    it('formats numbers as USD currency', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
      expect(formatCurrency(0)).toBe('$0.00');
      expect(formatCurrency(-99.99)).toBe('-$99.99');
    });
  });

  describe('truncateText', () => {
    it('truncates text longer than maxLength', () => {
      expect(truncateText('This is a long text', 10)).toBe('This is a...');
    });

    it('does not truncate text shorter than maxLength', () => {
      expect(truncateText('Short', 10)).toBe('Short');
    });

    it('handles edge cases', () => {
      expect(truncateText('', 5)).toBe('');
      expect(truncateText('Exactly', 7)).toBe('Exactly');
    });
  });
}); 