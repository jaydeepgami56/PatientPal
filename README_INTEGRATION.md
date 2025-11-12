# FastAPI + React Integration Guide

This document describes the integration between the React frontend and FastAPI backend for the Healthcare AI Agent system.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           React Frontend (Vite)                 │
│  - Modern UI with Tailwind CSS                  │
│  - React Router for navigation                  │
│  - Axios for API calls                          │
│  - React Query for state management             │
└─────────────────┬───────────────────────────────┘
                  │ HTTP REST API
                  │ (JSON)
┌─────────────────┴───────────────────────────────┐
│           FastAPI Backend                       │
│  - REST API endpoints                           │
│  - Pydantic models for validation               │
│  - Service layer with business logic            │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────┐
│      Existing Streamlit Application             │
│  - Agent logic (MedGemma, TxGemma, etc.)        │
│  - Orchestrator (utils/orchestrator.py)         │
│  - Prompts (utils/prompts.py)                   │
│  - Memory system (utils/memory.py)              │
└─────────────────────────────────────────────────┘
```

## Directory Structure

### Backend (FastAPI)
```
backend/
├── main.py                   # FastAPI app entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── models/                   # Pydantic request/response models
│   ├── triage.py
│   ├── agent.py
│   └── orchestrator.py
├── routers/                  # API route handlers
│   ├── health.py
│   ├── triage.py
│   ├── agents.py
│   └── orchestrator.py
└── services/                 # Business logic layer
    ├── triage_service.py
    ├── agent_service.py
    └── orchestrator_service.py
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── main.jsx             # React app entry
│   ├── App.jsx              # Router setup
│   ├── api/
│   │   └── client.js        # Axios API client
│   ├── components/
│   │   ├── Layout.jsx       # Main layout with navigation
│   │   ├── ChatMessage.jsx  # Chat bubble component
│   │   └── LoadingSpinner.jsx
│   └── pages/
│       ├── Home.jsx         # Landing page
│       ├── TriageAgent.jsx  # Triage interface
│       ├── LeadAgent.jsx    # Chat interface
│       ├── AgentConfig.jsx  # Agent configuration
│       └── Dashboard.jsx    # Results dashboard
├── package.json
├── vite.config.js           # Vite config with proxy
└── tailwind.config.cjs
```

## API Endpoints

### Triage Endpoints (`/api/triage`)
- `POST /start` - Start new triage session
- `POST /interview` - Continue interview conversation
- `POST /analyze` - Perform triage analysis
- `GET /session/{session_id}` - Get session info

### Agent Endpoints (`/api/agents`)
- `GET /list` - List all available agents
- `GET /{agent_name}` - Get specific agent info
- `POST /query` - Query a specific agent
- `PATCH /{agent_name}/config` - Update agent configuration

### Orchestrator Endpoints (`/api/orchestrator`)
- `POST /query` - Query lead agent orchestrator
- `GET /memory/summary` - Get memory summary
- `POST /memory/clear` - Clear orchestrator memory

### Health Endpoints (`/api`)
- `GET /health` - Health check
- `GET /ready` - Readiness check

## Setup Instructions

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r backend/requirements.txt
pip install -r requirements.txt  # Existing Streamlit dependencies

# Copy environment file
cp backend/.env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here

# Run FastAPI server
cd backend
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/api/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### 3. Running Both Together

**Terminal 1 (Backend):**
```bash
cd backend
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Development Workflow

### Adding a New API Endpoint

1. **Define Pydantic models** in `backend/models/`
2. **Create router** in `backend/routers/`
3. **Implement service logic** in `backend/services/`
4. **Register router** in `backend/main.py`
5. **Add API client method** in `frontend/src/api/client.js`
6. **Use in React component**

### Example: Adding a New Feature

**Backend (FastAPI):**
```python
# backend/models/example.py
from pydantic import BaseModel

class ExampleRequest(BaseModel):
    data: str

class ExampleResponse(BaseModel):
    result: str

# backend/routers/example.py
from fastapi import APIRouter
router = APIRouter(prefix="/example")

@router.post("/process")
async def process(request: ExampleRequest):
    return ExampleResponse(result=f"Processed: {request.data}")

# backend/main.py
from backend.routers import example
app.include_router(example.router, prefix="/api", tags=["Example"])
```

**Frontend (React):**
```javascript
// frontend/src/api/client.js
export const exampleAPI = {
  process: async (data) => {
    return apiClient.post('/example/process', { data });
  },
};

// In a React component
import { exampleAPI } from '../api/client';

const result = await exampleAPI.process('test data');
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_hf_api_key
DEBUG=False
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## CORS Configuration

The backend is configured to allow CORS from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative React port)

Update `backend/config.py` if you need to add more origins.

## Deployment

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
# Output will be in frontend/dist/
```

**Backend:**
```bash
# Use a production ASGI server
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment (Optional)

Create `docker-compose.yml` to run both services together.

## Troubleshooting

### CORS Errors
- Check that backend CORS origins include frontend URL
- Verify Vite proxy configuration in `vite.config.js`

### API Connection Issues
- Ensure backend is running on port 8000
- Check `VITE_API_BASE_URL` in frontend `.env`
- Verify network/firewall settings

### Import Errors
- Ensure all Python dependencies are installed
- Verify `sys.path` includes parent directory in services

## Next Steps

1. Implement Agent Configuration page
2. Build Results Dashboard with charts
3. Add authentication/authorization
4. Implement WebSocket for real-time updates
5. Add file upload for images (dermatology, radiology)
6. Implement session persistence (Redis/PostgreSQL)
7. Add unit and integration tests
8. Set up CI/CD pipeline

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React Query Documentation](https://tanstack.com/query/latest)
