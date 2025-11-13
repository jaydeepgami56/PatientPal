import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Stethoscope, Brain, Settings, BarChart3, Menu, X, Activity } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

/**
 * Professional Healthcare Layout
 * - Clean white navigation with blue accents
 * - Excellent contrast and accessibility
 * - Mobile-first responsive design
 * - Dark/Light mode toggle
 */
export default function Layout({ children }) {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Triage Agent', path: '/triage', icon: Stethoscope },
    { name: 'Lead Agent', path: '/lead-agent', icon: Brain },
    { name: 'Configuration', path: '/config', icon: Settings },
    { name: 'Dashboard', path: '/dashboard', icon: BarChart3 },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col transition-colors duration-300">
      {/* Skip link for keyboard users */}
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:bg-blue-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg focus:z-50"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-teal-600 rounded-lg flex items-center justify-center shadow-md">
                <Activity className="w-5 h-5 text-white" strokeWidth={2.5} />
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900 dark:text-white tracking-tight leading-none">
                  Healthcare AI
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400 -mt-0.5">Clinical Intelligence Platform</p>
              </div>
            </Link>

            {/* Desktop nav and theme toggle */}
            <div className="hidden md:flex items-center space-x-1">
              <nav aria-label="Primary" className="flex items-center space-x-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      aria-current={isActive(item.path) ? 'page' : undefined}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        isActive(item.path)
                          ? 'bg-blue-600 text-white shadow-md'
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <Icon className="w-4 h-4" strokeWidth={2} />
                      <span>{item.name}</span>
                    </Link>
                  );
                })}
              </nav>

              {/* Theme Toggle Button */}
              <ThemeToggle className="ml-2" />
            </div>

            {/* Mobile menu and theme toggle */}
            <div className="md:hidden flex items-center gap-2">
              {/* Theme Toggle Button - Mobile */}
              <ThemeToggle />

              {/* Mobile Menu Button */}
              <button
                aria-label="Toggle navigation"
                aria-expanded={mobileMenuOpen}
                onClick={() => setMobileMenuOpen((s) => !s)}
                className="p-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {mobileMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-1 border-t border-gray-200 dark:border-gray-700 mt-2">
              <ul role="menu">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <li key={item.path} role="none">
                      <Link
                        to={item.path}
                        onClick={() => setMobileMenuOpen(false)}
                        role="menuitem"
                        className={`flex items-center gap-3 px-4 py-3 rounded-lg text-base font-medium transition-all ${
                          isActive(item.path)
                            ? 'bg-blue-600 text-white shadow-md'
                            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                        }`}
                      >
                        <Icon className="w-5 h-5" strokeWidth={2} />
                        <span>{item.name}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </div>
      </header>

      {/* Main content wrapper */}
      <main id="main" role="main" className="flex-1">
        {children}
      </main>

      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-16 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center gap-3">
                <Activity className="w-5 h-5 text-blue-600 dark:text-blue-400" strokeWidth={2} />
                <div>
                  <div className="text-sm font-bold text-gray-900 dark:text-white">Healthcare AI</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Clinical Intelligence Platform</div>
                </div>
              </div>
              <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                Professional AI-powered clinical decision support for modern healthcare.
              </p>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wide">Platform</h4>
              <ul className="mt-3 space-y-2 text-sm">
                {navItems.slice(1, 4).map((item) => (
                  <li key={item.path}>
                    <Link to={item.path} className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wide">System Status</h4>
              <div className="mt-3 flex items-center gap-2">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400">All Systems Operational</span>
              </div>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-gray-600 dark:text-gray-400">© 2025 Healthcare AI. All rights reserved.</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Powered by <span className="text-gray-900 dark:text-white font-semibold">FastAPI</span> & <span className="text-gray-900 dark:text-white font-semibold">React</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
