import React from 'react';

interface ButtonProps {
  onClick?: () => void;
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  children,
  disabled = false,
  className = '',
  type = 'button'
}) => {
  return (
    <button 
      type={type}
      onClick={onClick} 
      disabled={disabled}
      className={className}
      data-testid="button"
    >
      {children}
    </button>
  );
};

export default Button; 