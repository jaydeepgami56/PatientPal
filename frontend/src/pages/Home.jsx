import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  const features = [
    {
      title: 'Triage Agent',
      description: 'AI-powered pre-visit interview and triage assessment using Australian ATS standards',
      icon: '🏥',
      link: '/triage',
      color: 'from-indigo-500 to-purple-500',
    },
    {
      title: 'Lead Agent',
      description: 'Intelligent multi-agent orchestrator that routes queries to specialist medical AI agents',
      icon: '🧠',
      link: '/lead-agent',
      color: 'from-pink-500 to-rose-500',
    },
    {
      title: 'Agent Configuration',
      description: 'Configure and manage individual specialist agents (MedGemma, TxGemma, Derm, CXR, Pathology)',
      icon: '⚙️',
      link: '/config',
      color: 'from-cyan-500 to-blue-500',
    },
    {
      title: 'Results Dashboard',
      description: 'View analytics, insights, and historical data from agent interactions',
      icon: '📊',
      link: '/dashboard',
      color: 'from-green-500 to-teal-500',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-500 to-pink-500 rounded-xl p-8 text-white">
        <div className="md:flex md:items-center md:justify-between">
          <div>
            <h2 className="text-4xl font-extrabold">
              Intelligent Medical AI System
            </h2>
            <p className="mt-4 text-lg max-w-2xl">
              A comprehensive multi-agent healthcare AI platform with triage capabilities,
              specialist medical agents, and intelligent orchestration
            </p>
          </div>
          <div className="mt-6 md:mt-0">
            <Link
              to="/triage"
              className="inline-flex items-center px-6 py-3 bg-white text-indigo-600 rounded-md font-medium shadow-lg hover:bg-gray-100 transition-colors"
            >
              Start Triage
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section>
        <h3 className="text-2xl font-semibold text-gray-900 mb-6">Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
            >
              <div className={`h-2 bg-gradient-to-r ${feature.color}`}></div>
              <div className="p-6">
                <div className="text-4xl mb-3">{feature.icon}</div>
                <h4 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h4>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Info Section */}
      <section className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          About This System
        </h3>
        <div className="prose prose-indigo">
          <p className="text-gray-600">
            This Healthcare AI Agent system combines multiple specialized medical AI models
            with intelligent orchestration to provide comprehensive medical assessment capabilities.
          </p>
          <ul className="mt-4 space-y-2 text-gray-600">
            <li>✓ <strong>Triage Agent:</strong> Pre-visit interviews with ATS classification</li>
            <li>✓ <strong>Specialist Agents:</strong> MedGemma, TxGemma, Dermatology, Radiology, Pathology</li>
            <li>✓ <strong>Intelligent Routing:</strong> Automatic query routing to appropriate specialists</li>
            <li>✓ <strong>Multi-agent Collaboration:</strong> Parallel and sequential agent execution</li>
            <li>✓ <strong>Memory Management:</strong> Three-tier memory for context retention</li>
          </ul>
        </div>
      </section>
    </div>
  );
}
