import React, { useState } from 'react';
import { triageAPI } from '../api/client';
import ChatMessage from '../components/ChatMessage';
import LoadingSpinner from '../components/LoadingSpinner';

export default function TriageAgent() {
  const [sessionId, setSessionId] = useState(null);
  const [phase, setPhase] = useState('welcome'); // welcome, interview, analysis, complete
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const startSession = async () => {
    setIsLoading(true);
    try {
      const response = await triageAPI.startSession();
      setSessionId(response.session_id);
      setPhase('interview');
      setMessages([
        {
          role: 'assistant',
          content: 'Hello! I\'m your AI triage agent. I\'ll ask you some questions about your condition. What brings you in today?',
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      alert(`Error starting session: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!userInput.trim() || !sessionId) return;

    const userMessage = {
      role: 'user',
      content: userInput,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setUserInput('');
    setIsLoading(true);

    try {
      const response = await triageAPI.interview(sessionId, userInput);

      const assistantMessage = {
        role: 'assistant',
        content: response.agent_message,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (response.is_complete) {
        setPhase('analysis');
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const performAnalysis = async () => {
    setIsLoading(true);
    try {
      const response = await triageAPI.analyze(sessionId, messages);
      setAnalysis(response);
      setPhase('complete');
    } catch (error) {
      alert(`Error performing analysis: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const resetSession = () => {
    setSessionId(null);
    setPhase('welcome');
    setMessages([]);
    setAnalysis(null);
    setUserInput('');
  };

  if (phase === 'welcome') {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">🏥</div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            AI Triage Agent
          </h2>
          <p className="text-gray-600 mb-8">
            Start a pre-visit interview to assess your condition and determine triage priority
            using the Australasian Triage Scale (ATS)
          </p>
          <button
            onClick={startSession}
            disabled={isLoading}
            className="px-6 py-3 bg-indigo-600 text-white rounded-md font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50"
          >
            {isLoading ? 'Starting...' : 'Begin Triage Interview'}
          </button>
        </div>
      </div>
    );
  }

  if (phase === 'interview') {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg">
          {/* Header */}
          <div className="border-b border-gray-200 px-6 py-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Triage Interview
            </h2>
            <p className="text-sm text-gray-500">Session: {sessionId}</p>
          </div>

          {/* Messages */}
          <div className="h-96 overflow-y-auto px-6 py-4 bg-gray-50">
            {messages.map((msg, index) => (
              <ChatMessage
                key={index}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />
            ))}
            {isLoading && <LoadingSpinner message="Agent is thinking..." />}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 px-6 py-4">
            <div className="flex space-x-4">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your response..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !userInput.trim()}
                className="px-6 py-2 bg-indigo-600 text-white rounded-md font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50"
              >
                Send
              </button>
            </div>
            <div className="mt-4 text-center">
              <button
                onClick={performAnalysis}
                className="px-6 py-2 bg-green-600 text-white rounded-md font-medium hover:bg-green-700 transition-colors"
              >
                Complete Interview & Analyze
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (phase === 'analysis') {
    return (
      <div className="max-w-4xl mx-auto">
        <LoadingSpinner message="Performing triage analysis..." />
      </div>
    );
  }

  if (phase === 'complete' && analysis) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Results Header */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Triage Analysis Complete
          </h2>
          <p className="text-gray-600">Session: {sessionId}</p>
        </div>

        {/* ATS Classification */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            ATS Classification
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="text-sm text-red-600 font-medium">Category</div>
              <div className="text-2xl font-bold text-red-700">
                {analysis.ats_category}
              </div>
            </div>
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="text-sm text-orange-600 font-medium">Urgency</div>
              <div className="text-lg font-semibold text-orange-700">
                {analysis.urgency}
              </div>
            </div>
          </div>
        </div>

        {/* Chief Complaint & Symptoms */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Assessment Summary
          </h3>
          <div className="space-y-4">
            <div>
              <div className="text-sm font-medium text-gray-600">Chief Complaint</div>
              <div className="text-gray-900">{analysis.chief_complaint}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-600">Symptoms</div>
              <div className="flex flex-wrap gap-2">
                {analysis.symptoms.map((symptom, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    {symptom}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-600">Recommended Action</div>
              <div className="text-gray-900">{analysis.recommended_action}</div>
            </div>
          </div>
        </div>

        {/* RACGP Report */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            RACGP Clinical Report
          </h3>
          <div className="prose max-w-none">
            <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded">
              {analysis.report}
            </pre>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow-lg p-6 text-center">
          <button
            onClick={resetSession}
            className="px-6 py-3 bg-indigo-600 text-white rounded-md font-medium hover:bg-indigo-700 transition-colors"
          >
            Start New Triage
          </button>
        </div>
      </div>
    );
  }

  return null;
}
