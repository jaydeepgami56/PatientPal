import { forwardRef } from 'react';

const Input = forwardRef(({
  label,
  error,
  helperText,
  icon,
  fullWidth = false,
  className = '',
  ...props
}, ref) => {
  const widthClass = fullWidth ? 'w-full' : '';

  return (
    <div className={`space-y-2 ${widthClass}`}>
      {label && (
        <label className="block text-sm font-semibold text-white uppercase tracking-wider">
          {label}
        </label>
      )}

      <div className="relative">
        {icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
            {icon}
          </div>
        )}

        <input
          ref={ref}
          className={`
            w-full px-4 py-3
            ${icon ? 'pl-12' : ''}
            bg-zinc-900/50 backdrop-blur-sm
            border border-white/10
            rounded-2xl
            text-white placeholder-gray-500
            focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50
            transition-all duration-200
            ${error ? 'border-red-500/50 focus:ring-red-500/50' : ''}
            ${className}
          `}
          {...props}
        />
      </div>

      {error && (
        <p className="text-sm text-red-400">{error}</p>
      )}

      {helperText && !error && (
        <p className="text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;
