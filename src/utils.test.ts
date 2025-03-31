// Define functions in the test file
function add(a: number, b: number): number {
  return a + b;
}

function multiply(a: number, b: number): number {
  return a * b;
}

describe('Math Utils', () => {
  test('adds two numbers correctly', () => {
    expect(add(1, 2)).toBe(3);
  });

  test('multiplies two numbers correctly', () => {
    expect(multiply(2, 3)).toBe(6);
  });
}); 