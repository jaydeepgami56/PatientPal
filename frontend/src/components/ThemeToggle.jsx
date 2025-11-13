import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function ThemeToggle({ className = '' }) {
  const { theme, toggleTheme } = useTheme();

  const handleClick = () => {
    console.log('ThemeToggle clicked!', { theme });
    toggleTheme();
    console.log('After toggle, document classList:', document.documentElement.classList.toString());
  };

  return (
    <button
      onClick={handleClick}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      className={`p-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors ${className}`}
      title={`Current theme: ${theme}. Click to toggle.`}
    >
      {theme === 'light' ? (
        <Moon className="w-5 h-5" strokeWidth={2} />
      ) : (
        <Sun className="w-5 h-5" strokeWidth={2} />
      )}
    </button>
  );
}
