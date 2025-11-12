import React, { useState } from 'react';
import { orchestratorAPI } from '../api/client';
import ChatMessage from '../components/ChatMessage';
import LoadingSpinner from '../components/LoadingSpinner';

export default function LeadAgent() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showRouting, setShowRouting] = useState(false);

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const userMessage = {
      role: 'user',
      content: userInput,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setUserInput('');
    setIsLoading(true);

    try {
      const response = await orchestratorAPI.query(
        userInput,
        null,
        null,
        showRouting
      );

      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        metadata: {
          agents_consulted: response.agents_consulted,
          confidence: response.confidence,
          processing_time: response.processing_time,
          routing_info: response.routing_info,
        },
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.message}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearConversation = async () => {
    try {
      await orchestratorAPI.clearMemory();
      setMessages([]);
    } catch (error) {
      alert(`Error clearing memory: ${error.message}`);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Lead Agent Chat
              </h2>
              <p className="text-sm text-gray-500">
                Intelligent multi-agent orchestration
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <label className="flex items-center text-sm text-gray-600">
                <input
                  type="checkbox"
                  checked={showRouting}
                  onChange={(e) => setShowRouting(e.target.checked)}
                  className="mr-2"
                />
                Show routing details
              </label>
              <button
                onClick={clearConversation}
                className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
              >
                Clear Chat
              </button>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="h-[500px] overflow-y-auto px-6 py-4 bg-gray-50">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="text-5xl mb-4">🧠</div>
              <p className="text-gray-600">
                Ask me anything about medical conditions, treatments, or diagnostics.
                <br />
                I'll route your query to the appropriate specialist agents.
              </p>
            </div>
          )}

          {messages.map((msg, index) => (
            <div key={index}>
              <ChatMessage
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />

              {/* Show metadata for assistant messages */}
              {msg.role === 'assistant' && msg.metadata && (
                <div className="mb-4 ml-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm">
                    <div className="flex items-center space-x-4 text-blue-800">
                      <span>
                        <strong>Agents:</strong> {msg.metadata.agents_consulted?.join(', ')}
                      </span>
                      <span>
                        <strong>Confidence:</strong> {(msg.metadata.confidence * 100).toFixed(1)}%
                      </span>
                      <span>
                        <strong>Time:</strong> {msg.metadata.processing_time?.toFixed(2)}s
                      </span>
                    </div>

                    {/* Routing details */}
                    {showRouting && msg.metadata.routing_info && (
                      <div className="mt-2 pt-2 border-t border-blue-200">
                        <div className="text-blue-700">
                          <strong>Routing:</strong> {msg.metadata.routing_info.reasoning}
                        </div>
                        <div className="text-blue-600 mt-1">
                          Mode: {msg.metadata.routing_info.execution_mode} |
                          Urgency: {msg.metadata.routing_info.urgency_level}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}

          {isLoading && <LoadingSpinner message="Consulting specialist agents..." />}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 px-6 py-4">
          <div className="flex space-x-4">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about medical conditions, diagnostics, treatments..."
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

          {/* Example queries */}
          <div className="mt-4">
            <div className="text-xs text-gray-500 mb-2">Example queries:</div>
            <div className="flex flex-wrap gap-2">
              {[
                'What are symptoms of diabetes?',
                'How to treat a minor burn?',
                'Interpret chest X-ray findings',
              ].map((example, i) => (
                <button
                  key={i}
                  onClick={() => setUserInput(example)}
                  className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
