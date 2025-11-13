import { forwardRef } from 'react';

const Card = forwardRef(({
  children,
  variant = 'default',
  hover = true,
  className = '',
  ...props
}, ref) => {
  const baseStyles = 'rounded-xl transition-all duration-300';

  const variants = {
    default: 'bg-white border border-gray-200 shadow-md',
    elevated: 'bg-white border border-gray-200 shadow-lg',
    subtle: 'bg-gray-50 border border-gray-100',
    bordered: 'bg-white border-2 border-blue-100',
  };

  const hoverStyles = hover ? 'hover:shadow-xl hover:-translate-y-1' : '';

  return (
    <div
      ref={ref}
      className={`${baseStyles} ${variants[variant]} ${hoverStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';

// Card subcomponents
export const CardHeader = ({ children, className = '' }) => (
  <div className={`px-6 py-5 border-b border-gray-200 ${className}`}>
    {children}
  </div>
);

export const CardBody = ({ children, className = '' }) => (
  <div className={`px-6 py-5 ${className}`}>
    {children}
  </div>
);

export const CardFooter = ({ children, className = '' }) => (
  <div className={`px-6 py-5 border-t border-gray-200 ${className}`}>
    {children}
  </div>
);

export default Card;
