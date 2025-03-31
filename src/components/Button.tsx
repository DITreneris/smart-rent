import React from 'react';

interface ButtonProps {
  onClick?: () => void;
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  children,
  disabled,
  className,
}) => {
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={className}
    >
      {children}
    </button>
  );
};

export default Button; 