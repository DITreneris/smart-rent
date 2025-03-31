// Simple utility functions for testing
const formatUtils = {
  formatCurrency: (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  },

  truncateText: (text: string, maxLength: number): string => {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  },
  
  formatDate: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
};

describe('Format Utilities', () => {
  describe('formatCurrency', () => {
    it('formats numbers as USD currency', () => {
      expect(formatUtils.formatCurrency(1234.56)).toBe('$1,234.56');
      expect(formatUtils.formatCurrency(0)).toBe('$0.00');
      expect(formatUtils.formatCurrency(-99.99)).toBe('-$99.99');
    });
  });

  describe('truncateText', () => {
    it('truncates text longer than maxLength', () => {
      expect(formatUtils.truncateText('This is a long text', 10)).toBe('This is a...');
    });

    it('does not truncate text shorter than maxLength', () => {
      expect(formatUtils.truncateText('Short', 10)).toBe('Short');
    });

    it('handles empty input', () => {
      expect(formatUtils.truncateText('', 5)).toBe('');
      expect(formatUtils.truncateText(null as any, 5)).toBe(null);
      expect(formatUtils.truncateText(undefined as any, 5)).toBe(undefined);
    });
  });

  describe('formatDate', () => {
    it('formats date strings correctly', () => {
      // Use a fixed date to avoid locale/timezone issues
      const date = new Date(2023, 0, 15); // January 15, 2023
      const dateStr = date.toISOString();
      
      // This might differ by locale, so using a more flexible test
      const result = formatUtils.formatDate(dateStr);
      expect(result).toContain('2023');
      expect(result).toContain('January');
      expect(result).toContain('15');
    });
  });
}); 