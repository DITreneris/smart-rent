const React = require('react');
const { render, screen, fireEvent } = require('@testing-library/react');

// Simple Button component
function Button(props) {
  const { onClick, children, disabled, className } = props;
  return React.createElement(
    'button',
    {
      onClick: onClick,
      disabled: disabled,
      className: className
    },
    children
  );
}

// Tests
describe('Button Component', () => {
  test('renders with text', () => {
    render(React.createElement(Button, null, 'Click Me'));
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });
  
  test('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(React.createElement(Button, { onClick: handleClick }, 'Click Me'));
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  test('respects disabled prop', () => {
    const handleClick = jest.fn();
    render(React.createElement(Button, { 
      onClick: handleClick, 
      disabled: true 
    }, 'Disabled Button'));
    
    const button = screen.getByText('Disabled Button');
    expect(button).toBeDisabled();
    
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
}); 