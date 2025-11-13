# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Stack: Python 3.12 (Pydantic v2), Streamlit UI [`app.py`](app.py:10), FastAPI backend [`backend/main.py`](backend/main.py:7), React (Vite) frontend [`frontend/package.json`](frontend/package.json:5).
- Run backend (from repo root): uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 (see [`backend/main.py`](backend/main.py:71)).
- Run frontend (from repo root): cd frontend && npm install && npm run dev. Vite dev ports 5173–5176 are allowed by CORS in [`backend/config.py`](backend/config.py:24).
- Run Streamlit UI: streamlit run [`app.py`](app.py:1). CSS loaded from [`styles/app_style.css`](styles/app_style.css:1).
- Tests are standalone scripts (not pytest). Run [`test_lead_agent.py`](test_lead_agent.py:7) or [`test_api.py`](test_api.py:4). They require OPENAI_API_KEY in `.env` (fatal).
- Run a single test function (example): python -c "from test_lead_agent import initialize_orchestrator,test_basic_routing; o=initialize_orchestrator(); print(test_basic_routing(o))"

Non-obvious, project-specific rules:
- Agents must subclass [`utils/agent_base.py`](utils/agent_base.py:55) BaseHealthcareAgent and implement initialize(), validate_input(), process(); initialize() MUST set agent._is_initialized=True and return True (see [`utils/orchestrator.py`](utils/orchestrator.py:256)).
- LLM interface mismatch: orchestrator expects llm.invoke(...) returning an object with .content, while PromptExecutor uses llm_client.generate(...) returning a string — provide an adapter or use the langchain wrapper used in tests (see [`utils/prompt_executor.py`](utils/prompt_executor.py:81)).
- Prompt templates in [`utils/prompts.py`](utils/prompts.py:40) are authoritative; DO NOT change exact headings/case/field names — regex parsers in [`utils/orchestrator.py`](utils/orchestrator.py:190) depend on verbatim strings.
- Image-only agents (Derm/CXR) must only be selected when image context is present; router and prompts enforce this (see [`utils/prompts.py`](utils/prompts.py:722)).
- Logging auto-creates ./logs/ on import and writes LLM interactions to `logs/llm_interactions.log` (see [`utils/logger.py`](utils/logger.py:39)); inspect logs for LLM prompt/response payloads.
- Memory is three-tiered (user convo, agent consultations, orchestration audit) implemented in [`utils/memory.py`](utils/memory.py:53); use get_full_context() for concise snapshots.
- Pydantic models define external interfaces; do not rename fields (RoutingDecision, AgentResponse) as serializers, memory, and tests rely on .dict() shapes.
- Running scripts: many scripts expect being run from repo root (tests and uvicorn) because code appends parent dir to sys.path — run from project root to avoid import errors.
- Regex parsers (routing, triage parsing) map textual labels to numeric/confidence mappings; if you change prompt wording, update parser regexes and confidence_map together (see [`utils/orchestrator.py`](utils/orchestrator.py:213)).
- Use the logging decorators (e.g., @log_prompt_execution, @log_function_call) for new prompt code to integrate with existing logs and performance metrics (`utils/logger.py`).
- Minimal formatting/style notes (non-obvious): prefer Pydantic BaseModel for API shapes, include explicit types on public function signatures, and ensure datetimes use datetime.now() patterns consistent with existing models to avoid serialization differences.

Every line above is derived from repository files and is essential to avoid common mistakes when modifying routing, prompts, agents, or tests.