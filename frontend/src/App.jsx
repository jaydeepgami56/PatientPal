import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import TriageAgent from './pages/TriageAgent';
import LeadAgent from './pages/LeadAgent';

// Create a client for react-query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/triage" element={<TriageAgent />} />
              <Route path="/lead-agent" element={<LeadAgent />} />
              <Route path="/config" element={<PlaceholderPage title="Agent Configuration" />} />
              <Route path="/dashboard" element={<PlaceholderPage title="Results Dashboard" />} />
            </Routes>
          </Layout>
        </Router>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

// Placeholder component for pages not yet implemented
function PlaceholderPage({ title }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12 text-center transition-colors duration-300">
      <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">{title}</h2>
      <p className="text-gray-600 dark:text-gray-400">This page is coming soon...</p>
    </div>
  );
}
