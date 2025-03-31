const React = require('react');
const { render } = require('@testing-library/react');

test('renders a div', () => {
  const { container } = render(<div>Hello</div>);
  expect(container.textContent).toBe('Hello');
}); 