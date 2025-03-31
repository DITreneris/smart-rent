const React = require('react');
const { render, screen, fireEvent, waitFor } = require('@testing-library/react');

// Mock PropertyForm component
function PropertyForm({ onSubmit, initialValues = {} }) {
  const [values, setValues] = React.useState({
    title: initialValues.title || '',
    description: initialValues.description || '',
    price: initialValues.price || ''
  });
  
  const [errors, setErrors] = React.useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
  };
  
  const validate = () => {
    const newErrors = {};
    if (!values.title) newErrors.title = 'Title is required';
    if (!values.price) newErrors.price = 'Price is required';
    if (values.price && isNaN(parseFloat(values.price))) {
      newErrors.price = 'Price must be a number';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(values);
    }
  };
  
  return React.createElement(
    'form',
    { onSubmit: handleSubmit, 'data-testid': 'property-form' },
    [
      // Title field
      React.createElement(
        'div',
        { key: 'title-field' },
        [
          React.createElement(
            'label',
            { htmlFor: 'title', key: 'title-label' },
            'Title'
          ),
          React.createElement(
            'input',
            {
              id: 'title',
              name: 'title',
              value: values.title,
              onChange: handleChange,
              key: 'title-input'
            }
          ),
          errors.title && React.createElement(
            'div',
            { className: 'error', key: 'title-error' },
            errors.title
          )
        ]
      ),
      
      // Description field
      React.createElement(
        'div',
        { key: 'desc-field' },
        [
          React.createElement(
            'label',
            { htmlFor: 'description', key: 'desc-label' },
            'Description'
          ),
          React.createElement(
            'textarea',
            {
              id: 'description',
              name: 'description',
              value: values.description,
              onChange: handleChange,
              key: 'desc-input'
            }
          )
        ]
      ),
      
      // Price field
      React.createElement(
        'div',
        { key: 'price-field' },
        [
          React.createElement(
            'label',
            { htmlFor: 'price', key: 'price-label' },
            'Price (ETH)'
          ),
          React.createElement(
            'input',
            {
              id: 'price',
              name: 'price',
              value: values.price,
              onChange: handleChange,
              key: 'price-input'
            }
          ),
          errors.price && React.createElement(
            'div',
            { className: 'error', key: 'price-error' },
            errors.price
          )
        ]
      ),
      
      // Submit button
      React.createElement(
        'button',
        { type: 'submit', key: 'submit-btn' },
        'Submit'
      )
    ]
  );
}

describe('PropertyForm', () => {
  test('renders form fields', () => {
    render(React.createElement(PropertyForm, { onSubmit: jest.fn() }));
    
    expect(screen.getByLabelText('Title')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByLabelText('Price (ETH)')).toBeInTheDocument();
    expect(screen.getByText('Submit')).toBeInTheDocument();
  });
  
  test('validates required fields', async () => {
    render(React.createElement(PropertyForm, { onSubmit: jest.fn() }));
    
    fireEvent.click(screen.getByText('Submit'));
    
    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
      expect(screen.getByText('Price is required')).toBeInTheDocument();
    });
  });
  
  test('validates price is a number', async () => {
    render(React.createElement(PropertyForm, { onSubmit: jest.fn() }));
    
    fireEvent.change(screen.getByLabelText('Title'), { target: { name: 'title', value: 'My Property' } });
    fireEvent.change(screen.getByLabelText('Price (ETH)'), { target: { name: 'price', value: 'not-a-number' } });
    
    fireEvent.click(screen.getByText('Submit'));
    
    await waitFor(() => {
      expect(screen.getByText('Price must be a number')).toBeInTheDocument();
    });
  });
  
  test('submits form with valid data', async () => {
    const handleSubmit = jest.fn();
    render(React.createElement(PropertyForm, { onSubmit: handleSubmit }));
    
    fireEvent.change(screen.getByLabelText('Title'), { target: { name: 'title', value: 'My Property' } });
    fireEvent.change(screen.getByLabelText('Description'), { 
      target: { name: 'description', value: 'A nice property' } 
    });
    fireEvent.change(screen.getByLabelText('Price (ETH)'), { target: { name: 'price', value: '1.5' } });
    
    fireEvent.click(screen.getByText('Submit'));
    
    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        title: 'My Property',
        description: 'A nice property',
        price: '1.5'
      });
    });
  });
  
  test('initializes form with provided values', () => {
    const initialValues = {
      title: 'Existing Property',
      description: 'An existing property',
      price: '2.0'
    };
    
    render(React.createElement(PropertyForm, { 
      onSubmit: jest.fn(),
      initialValues
    }));
    
    expect(screen.getByLabelText('Title').value).toBe('Existing Property');
    expect(screen.getByLabelText('Description').value).toBe('An existing property');
    expect(screen.getByLabelText('Price (ETH)').value).toBe('2.0');
  });
}); 