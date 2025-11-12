# FastAPI + React Integration Documentation

**Date Created:** 2025-11-12
**Status:** ✅ Complete - Ready for Testing
**Architecture:** Modern REST API + React SPA Frontend

---

## 📌 Overview

This document describes the **FastAPI + React** integration layer that provides a modern web interface for the Healthcare AI Agent system. This integration sits alongside the existing Streamlit application, providing a production-ready API and responsive frontend.

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 5173)                    │
│  - Modern UI with Tailwind CSS                                   │
│  - React Router for navigation                                   │
│  - Axios for API communication                                   │
│  - React Query for state management                              │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP REST API (JSON)
                         │ CORS enabled
┌────────────────────────┴────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                    │
│  - REST API endpoints with OpenAPI docs                          │
│  - Pydantic models for validation                                │
│  - Service layer for business logic                              │
│  - CORS middleware                                                │
└────────────────────────┬────────────────────────────────────────┘
                         │ Direct imports
                         │ Function calls
┌────────────────────────┴────────────────────────────────────────┐
│              Existing Streamlit Application                      │
│  - Agent modules (MedGemma, TxGemma, Derm, CXR, Pathology)      │
│  - Orchestrator (LeadAgentOrchestrator)                         │
│  - Utilities (prompts, memory, logging)                          │
│  - Triage logic                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Action (React)
    ↓
API Call (Axios)
    ↓
FastAPI Router
    ↓
Pydantic Validation
    ↓
Service Layer
    ↓
Existing Agent/Orchestrator Logic
    ↓
Response (Pydantic Model)
    ↓
JSON Response
    ↓
React State Update
    ↓
UI Re-render
```

---

## 📁 Project Structure

### Backend Structure

```
backend/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration with Pydantic Settings
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
│
├── models/                      # Pydantic request/response models
│   ├── __init__.py
│   ├── triage.py               # Triage session, interview, analysis
│   ├── agent.py                # Agent info, query, configuration
│   └── orchestrator.py         # Orchestrator query, routing
│
├── routers/                     # API endpoint handlers
│   ├── __init__.py
│   ├── health.py               # Health check endpoints
│   ├── triage.py               # Triage workflow endpoints
│   ├── agents.py               # Agent management endpoints
│   └── orchestrator.py         # Multi-agent orchestration
│
└── services/                    # Business logic layer
    ├── __init__.py
    ├── triage_service.py       # Extracted from Triage_agent.py
    ├── agent_service.py        # Agent initialization & queries
    └── orchestrator_service.py # Lead agent orchestration
```

### Frontend Structure

```
frontend/src/
├── main.jsx                     # React entry point
├── App.jsx                      # Router & React Query setup
├── index.css                    # Tailwind CSS & custom styles
│
├── api/
│   └── client.js               # Axios client with all API methods
│
├── components/
│   ├── Layout.jsx              # Main layout with navigation
│   ├── ChatMessage.jsx         # Chat bubble component
│   └── LoadingSpinner.jsx      # Loading state component
│
└── pages/
    ├── Home.jsx                # Landing page
    ├── TriageAgent.jsx         # Multi-step triage interview
    └── LeadAgent.jsx           # Chat interface with orchestrator
```

---

## 🔌 API Endpoints

### Base URL
- **Development**: `http://localhost:8000/api`
- **Production**: Configure via `VITE_API_BASE_URL`

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/ready` | Readiness check |

### Triage Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/triage/start` | Start new triage session |
| POST | `/api/triage/interview` | Continue interview conversation |
| POST | `/api/triage/analyze` | Perform triage analysis |
| GET | `/api/triage/session/{id}` | Get session information |

### Agent Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents/list` | List all available agents |
| GET | `/api/agents/{name}` | Get specific agent info |
| POST | `/api/agents/query` | Query a specific agent |
| PATCH | `/api/agents/{name}/config` | Update agent configuration |

### Orchestrator Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orchestrator/query` | Query lead agent orchestrator |
| GET | `/api/orchestrator/memory/summary` | Get memory summary |
| POST | `/api/orchestrator/memory/clear` | Clear orchestrator memory |

---

## 🎯 Key Features

### Backend Features

✅ **RESTful API Design**
- Resource-based endpoints
- Standard HTTP methods
- JSON request/response

✅ **Automatic API Documentation**
- Swagger UI at `/api/docs`
- ReDoc at `/api/redoc`
- OpenAPI 3.0 specification

✅ **Data Validation**
- Pydantic models for all requests/responses
- Automatic validation errors
- Type safety throughout

✅ **CORS Support**
- Configured for frontend origins
- Credential support
- Flexible headers

✅ **Service Layer Pattern**
- Separation of concerns
- Reusable business logic
- Easy to test

✅ **Error Handling**
- Global exception handler
- User-friendly error messages
- Debug mode for development

### Frontend Features

✅ **Modern React**
- Functional components with hooks
- React Router for navigation
- Context for state management

✅ **Responsive Design**
- Tailwind CSS utilities
- Mobile-first approach
- Adaptive layouts

✅ **API Integration**
- Axios with interceptors
- React Query for caching
- Automatic retries

✅ **User Experience**
- Loading states
- Error boundaries
- Real-time feedback

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API Key
- HuggingFace API Key (optional)

### Backend Setup

1. **Install dependencies**:
```bash
pip install -r backend/requirements.txt
pip install -r requirements.txt  # Existing dependencies
```

2. **Configure environment**:
```bash
cp backend/.env.example .env
# Edit .env and add:
# OPENAI_API_KEY=your_key_here
```

3. **Run backend**:
```bash
cd backend
python main.py
# Or: uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/api/docs`

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure environment** (optional):
```bash
cp .env.example .env
# VITE_API_BASE_URL=http://localhost:8000/api
```

3. **Run frontend**:
```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 💡 Usage Examples

### Triage Workflow (Frontend)

1. Navigate to `/triage`
2. Click "Begin Triage Interview"
3. Answer AI questions
4. Click "Complete Interview & Analyze"
5. View ATS classification and report

### Lead Agent Chat (Frontend)

1. Navigate to `/lead-agent`
2. Type a medical query
3. View synthesized response
4. See which agents were consulted

### Direct API Usage (cURL)

```bash
# Health check
curl http://localhost:8000/api/health

# Start triage session
curl -X POST http://localhost:8000/api/triage/start \
  -H "Content-Type: application/json" \
  -d '{"patient_name": "John Doe"}'

# Query orchestrator
curl -X POST http://localhost:8000/api/orchestrator/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are symptoms of diabetes?"}'

# List agents
curl http://localhost:8000/api/agents/list
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/config.py`:

```python
class Settings(BaseSettings):
    # App settings
    app_name: str = "Healthcare AI Agent API"
    debug: bool = False

    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
```

### Frontend Configuration

Edit `frontend/vite.config.js`:

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

---

## 🔐 Security Considerations

### Production Checklist

- [ ] Use HTTPS for all communication
- [ ] Implement authentication (JWT tokens)
- [ ] Add rate limiting
- [ ] Validate all inputs server-side
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Implement proper session management
- [ ] Add audit logging
- [ ] Use secure headers middleware
- [ ] Implement CSRF protection

### Development vs Production

**Development:**
- Debug mode enabled
- Detailed error messages
- CORS allows localhost
- No authentication required

**Production:**
- Debug mode disabled
- Generic error messages
- CORS restricted to production domain
- Authentication required
- HTTPS enforced

---

## 📊 Performance

### Response Times (Approximate)

| Operation | Time | Tokens |
|-----------|------|--------|
| Triage interview message | 2-5s | 200-500 |
| Triage analysis | 10-20s | 2000-3000 |
| Orchestrator query | 3-10s | 1000-2000 |
| Agent query (single) | 2-5s | 500-1000 |

### Optimization Tips

1. **Backend**:
   - Use async/await for I/O operations
   - Implement caching (Redis)
   - Connection pooling
   - Background tasks for long operations

2. **Frontend**:
   - React Query caching
   - Code splitting
   - Lazy loading
   - Memoization

---

## 🐛 Troubleshooting

### CORS Errors

**Problem**: Browser blocks API requests
**Solution**:
- Check backend CORS settings in `config.py`
- Verify frontend proxy in `vite.config.js`
- Ensure backend is running on port 8000

### Import Errors (Backend)

**Problem**: `ModuleNotFoundError`
**Solution**:
```bash
# Ensure parent directory is in Python path
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%\..          # Windows
```

### API Connection Refused

**Problem**: Frontend can't reach backend
**Solution**:
- Verify backend is running: `curl http://localhost:8000/api/health`
- Check firewall settings
- Verify ports 8000 and 5173 are not in use

---

## 📚 Related Documentation

- [QUICKSTART.md](../QUICKSTART.md) - 5-minute setup guide
- [README_INTEGRATION.md](../README_INTEGRATION.md) - Detailed architecture
- [INTEGRATION_SUMMARY.md](../INTEGRATION_SUMMARY.md) - Complete feature list
- [MULTI_AGENT_ARCHITECTURE_STRATEGY.md](MULTI_AGENT_ARCHITECTURE_STRATEGY.md) - Agent system design

---

## 🎯 Next Steps

### Immediate
1. Test triage workflow end-to-end
2. Test lead agent chat interface
3. Verify all API endpoints

### Short Term
1. Implement Agent Configuration page
2. Build Results Dashboard
3. Add image upload capability
4. Implement authentication

### Long Term
1. Add WebSocket support for real-time updates
2. Implement session persistence (Redis/PostgreSQL)
3. Add comprehensive test suite
4. Deploy to production (Docker + CI/CD)

---

**Last Updated:** 2025-11-12
**Version:** 1.0.0
**Status:** Production Ready for Testing
