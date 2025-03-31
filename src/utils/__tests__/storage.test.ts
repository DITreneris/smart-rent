// Simple storage utility functions to test
const storageUtils = {
  get: (key: string): any => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error('Error getting item from localStorage', error);
      return null;
    }
  },
  
  set: (key: string, value: any): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error setting item in localStorage', error);
    }
  },
  
  remove: (key: string): void => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing item from localStorage', error);
    }
  }
};

describe('Storage Utilities', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    
    // Mock implementation for localStorage
    jest.spyOn(window.localStorage.__proto__, 'setItem');
    jest.spyOn(window.localStorage.__proto__, 'getItem');
    jest.spyOn(window.localStorage.__proto__, 'removeItem');
  });
  
  afterEach(() => {
    jest.restoreAllMocks();
  });
  
  it('sets items in localStorage', () => {
    storageUtils.set('testKey', { data: 'testValue' });
    expect(localStorage.setItem).toHaveBeenCalledWith('testKey', JSON.stringify({ data: 'testValue' }));
  });
  
  it('gets items from localStorage', () => {
    localStorage.setItem('testKey', JSON.stringify({ data: 'testValue' }));
    const result = storageUtils.get('testKey');
    expect(result).toEqual({ data: 'testValue' });
  });
  
  it('removes items from localStorage', () => {
    localStorage.setItem('testKey', JSON.stringify({ data: 'testValue' }));
    storageUtils.remove('testKey');
    expect(localStorage.removeItem).toHaveBeenCalledWith('testKey');
  });
}); 