export const mockPropertyService = {
  getProperties: jest.fn().mockResolvedValue([]),
  getProperty: jest.fn().mockResolvedValue({}),
  createProperty: jest.fn().mockResolvedValue({}),
  updateProperty: jest.fn().mockResolvedValue({}),
  deleteProperty: jest.fn().mockResolvedValue({}),
};

export const mockAuthService = {
  login: jest.fn().mockResolvedValue({ token: 'fake
} 