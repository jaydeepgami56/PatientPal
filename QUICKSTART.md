# Quick Start Guide - FastAPI + React Integration

## Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API Key

## Setup in 5 Minutes

### 1. Install Backend Dependencies

```bash
# Install all Python dependencies
pip install -r backend/requirements.txt
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment file
cp backend/.env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Run Backend

Open a terminal and run:

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000/api/docs to see the API documentation.

### 5. Run Frontend

Open another terminal and run:

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### 6. Open Application

Open your browser to **http://localhost:5173**

You should see the Healthcare AI Agent home page with options for:
- **Triage Agent** - Pre-visit interview and ATS triage
- **Lead Agent** - Multi-agent chat interface
- **Agent Config** - Configure specialist agents
- **Dashboard** - View results and analytics

## Test the Integration

### Test Triage Agent

1. Click "Triage Agent" or navigate to http://localhost:5173/triage
2. Click "Begin Triage Interview"
3. Describe a medical condition (e.g., "I have a headache and fever")
4. Answer the follow-up questions
5. Click "Complete Interview & Analyze"
6. View the ATS classification and RACGP report

### Test Lead Agent

1. Click "Lead Agent" or navigate to http://localhost:5173/lead-agent
2. Type a medical query (e.g., "What are symptoms of diabetes?")
3. Press Enter or click "Send"
4. The orchestrator will route to appropriate specialist agents
5. View the synthesized response with agent metadata

## Troubleshooting

### Backend won't start

**Error: ModuleNotFoundError**
```bash
# Make sure you're in the backend directory
cd backend

# Make sure parent directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%\..          # Windows
```

**Error: OPENAI_API_KEY not found**
- Check that `.env` file exists in project root
- Verify OPENAI_API_KEY is set correctly
- No spaces around the = sign

### Frontend won't start

**Error: Module not found**
```bash
cd frontend
npm install  # Reinstall dependencies
```

**CORS errors in browser console**
- Ensure backend is running on port 8000
- Check vite.config.js proxy configuration
- Verify backend CORS settings in config.py

### API calls failing

1. **Check backend is running**: Visit http://localhost:8000/api/health
2. **Check API docs**: Visit http://localhost:8000/api/docs
3. **Check browser console**: Open DevTools (F12) and look for errors
4. **Check backend logs**: Look at the terminal running the backend

## Next Steps

- Review [README_INTEGRATION.md](README_INTEGRATION.md) for detailed architecture
- Customize agents in `agents/` directory
- Add new pages in `frontend/src/pages/`
- Implement authentication
- Deploy to production

## Common Development Tasks

### Add a new API endpoint

1. Create model in `backend/models/`
2. Create router in `backend/routers/`
3. Create service in `backend/services/`
4. Register router in `backend/main.py`
5. Add API client method in `frontend/src/api/client.js`

### Add a new page

1. Create component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation link in `frontend/src/components/Layout.jsx`

### Update styling

- Edit `frontend/src/index.css` for global styles
- Use Tailwind utility classes in components
- Customize theme in `frontend/tailwind.config.cjs`

## Port Configuration

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs

## Support

For issues or questions:
1. Check [README_INTEGRATION.md](README_INTEGRATION.md)
2. Review API documentation at http://localhost:8000/api/docs
3. Check browser console for frontend errors
4. Check terminal for backend errors
