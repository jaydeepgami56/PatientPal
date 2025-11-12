/**
 * API Client
 * ===========
 * Axios-based API client for communicating with FastAPI backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject(new Error(errorMessage));
  }
);

// ============================================================================
// TRIAGE API
// ============================================================================

export const triageAPI = {
  /**
   * Start a new triage session
   */
  startSession: async (patientName = null) => {
    return apiClient.post('/triage/start', { patient_name: patientName });
  },

  /**
   * Continue interview conversation
   */
  interview: async (sessionId, userMessage) => {
    return apiClient.post('/triage/interview', {
      session_id: sessionId,
      user_message: userMessage,
    });
  },

  /**
   * Perform triage analysis
   */
  analyze: async (sessionId, messages) => {
    return apiClient.post('/triage/analyze', {
      session_id: sessionId,
      messages: messages,
    });
  },

  /**
   * Get session info
   */
  getSession: async (sessionId) => {
    return apiClient.get(`/triage/session/${sessionId}`);
  },
};

// ============================================================================
// AGENTS API
// ============================================================================

export const agentsAPI = {
  /**
   * List all available agents
   */
  listAgents: async () => {
    return apiClient.get('/agents/list');
  },

  /**
   * Get specific agent info
   */
  getAgent: async (agentName) => {
    return apiClient.get(`/agents/${agentName}`);
  },

  /**
   * Query a specific agent
   */
  queryAgent: async (agentName, query, context = null, imageData = null) => {
    return apiClient.post('/agents/query', {
      agent_name: agentName,
      query: query,
      context: context,
      image_data: imageData,
    });
  },

  /**
   * Update agent configuration
   */
  updateConfig: async (agentName, config) => {
    return apiClient.patch(`/agents/${agentName}/config`, config);
  },
};

// ============================================================================
// ORCHESTRATOR API
// ============================================================================

export const orchestratorAPI = {
  /**
   * Query the lead agent orchestrator
   */
  query: async (query, context = null, imageData = null, showRouting = false) => {
    return apiClient.post('/orchestrator/query', {
      query: query,
      context: context,
      image_data: imageData,
      show_routing: showRouting,
    });
  },

  /**
   * Get memory summary
   */
  getMemorySummary: async () => {
    return apiClient.get('/orchestrator/memory/summary');
  },

  /**
   * Clear orchestrator memory
   */
  clearMemory: async () => {
    return apiClient.post('/orchestrator/memory/clear');
  },
};

// ============================================================================
// HEALTH API
// ============================================================================

export const healthAPI = {
  /**
   * Health check
   */
  check: async () => {
    return apiClient.get('/health');
  },

  /**
   * Readiness check
   */
  ready: async () => {
    return apiClient.get('/ready');
  },
};

export default apiClient;
