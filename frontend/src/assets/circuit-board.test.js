import circuitBoardImage from './circuit-board';

describe('Circuit board image', () => {
  test('should be a valid data URL', () => {
    expect(circuitBoardImage).toBeDefined();
    expect(typeof circuitBoardImage).toBe('string');
    expect(circuitBoardImage).toMatch(/^data:image\/(png|jpeg);base64,/);
  });
}); 