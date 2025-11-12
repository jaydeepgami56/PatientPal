# Documentation Index

Quick navigation to all documentation files.

## 📁 Documentation Files (13+ files)

### 1. 📖 [README.md](README.md) - Start Here
**142 lines | 5 min read**

Overview of documentation structure and how to use it.
- Which document to use when
- Quick start guide for developers
- Documentation stats and search tips

### 2. 📚 [PROMPT_STRATEGY.md](PROMPT_STRATEGY.md) - Complete Guide
**1,721 lines | 30-45 min read | 49 KB**

Comprehensive strategy documentation covering:
- ✅ Australian health standards (ATS, RACGP)
- ✅ Prompt architecture & design philosophy
- ✅ Guardrail system (8 global rules)
- ✅ All 5 prompt specifications
- ✅ Validation strategies with code
- ✅ Clinical safety measures
- ✅ Troubleshooting guide
- ✅ Complete validation suite (Appendix A)
- ✅ Testing examples (Appendix B)

### 3. ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Cheat Sheet
**203 lines | 5-10 min read | 6.4 KB**

At-a-glance reference for daily use:
- ✅ DO's and DON'Ts checklist
- ✅ ATS quick reference table
- ✅ Output format templates
- ✅ Validation checklist
- ✅ Red flag triggers
- ✅ Australian terminology
- ✅ Common errors & fixes

### 4. 🎨 [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Visual Guide
**576 lines | 10-15 min read | 29 KB**

Visual diagrams and flowcharts:
- ✅ System architecture overview
- ✅ Prompt flow diagrams
- ✅ Guardrail enforcement layers
- ✅ ATS decision tree
- ✅ Mode separation patterns
- ✅ Validation pipeline
- ✅ Constrained choice enforcement

### 5. 🚀 [FASTAPI_REACT_INTEGRATION.md](FASTAPI_REACT_INTEGRATION.md) - API & Web UI ⭐ NEW
**~400 lines | 15-20 min read**

FastAPI + React integration guide:
- ✅ REST API architecture
- ✅ Backend setup (FastAPI)
- ✅ Frontend setup (React + Vite)
- ✅ API endpoints documentation
- ✅ Request/response models
- ✅ Development workflow
- ✅ Deployment guide

### 6. ⚡ [MULTI_AGENT_ARCHITECTURE_STRATEGY.md](MULTI_AGENT_ARCHITECTURE_STRATEGY.md) - Agent System
**~1,100 lines | 25-30 min read | 32 KB**

Multi-agent orchestration architecture:
- ✅ Lead agent orchestrator design
- ✅ Specialist agent modules
- ✅ Routing strategy
- ✅ Parallel & sequential execution
- ✅ Three-tier memory system

### 7. 📝 [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What We Built
**~500 lines | 15-20 min read | 16 KB**

Implementation summary and features:
- ✅ Agent modules created
- ✅ FastAPI backend implementation ⭐ NEW
- ✅ React frontend implementation ⭐ NEW
- ✅ Orchestrator capabilities
- ✅ Usage examples
- ✅ Testing checklist

### 8-12. Additional Documentation

- [ATS_OFFICIAL_CRITERIA.md](ATS_OFFICIAL_CRITERIA.md) - Australasian Triage Scale official criteria
- [CHATBOT_FEATURES.md](CHATBOT_FEATURES.md) - Chatbot features and capabilities
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - Logging and debugging guide
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Quick start for Lead Agent
- [TEST_CASES.md](TEST_CASES.md) - Test cases and scenarios

---

## 🔍 Find What You Need

### By Role

| Your Role | Start With | Then Read |
|-----------|-----------|-----------|
| **New Developer** | README.md → ../QUICKSTART.md | FASTAPI_REACT_INTEGRATION.md |
| **Frontend Developer** | ../QUICKSTART.md | FASTAPI_REACT_INTEGRATION.md |
| **Backend Developer** | ../README_INTEGRATION.md | MULTI_AGENT_ARCHITECTURE_STRATEGY.md |
| **Prompt Engineer** | PROMPT_STRATEGY.md | ARCHITECTURE_DIAGRAM.md |
| **QA/Tester** | QUICK_REFERENCE.md | TEST_CASES.md |
| **System Architect** | ARCHITECTURE_DIAGRAM.md | MULTI_AGENT_ARCHITECTURE_STRATEGY.md |
| **Clinical Reviewer** | QUICK_REFERENCE.md (ATS) | ATS_OFFICIAL_CRITERIA.md |

### By Task

| Task | Document | Section |
|------|----------|---------|
| **Setup FastAPI + React** | ../QUICKSTART.md | All |
| **Understand API architecture** | FASTAPI_REACT_INTEGRATION.md | Architecture |
| **Understand multi-agent system** | MULTI_AGENT_ARCHITECTURE_STRATEGY.md | All |
| **Implement validator** | PROMPT_STRATEGY.md | Appendix A |
| **Write test cases** | TEST_CASES.md | Examples |
| **Quick ATS lookup** | QUICK_REFERENCE.md | ATS Table |
| **Check output format** | QUICK_REFERENCE.md | Format Templates |
| **Troubleshoot issue** | PROMPT_STRATEGY.md | Troubleshooting |
| **API endpoints** | FASTAPI_REACT_INTEGRATION.md | API Endpoints |
| **Frontend components** | FASTAPI_REACT_INTEGRATION.md | Frontend Structure |

---

## 🔗 Related Files (Outside docs/)

| File | Location | Description |
|------|----------|-------------|
| **Prompts Source** | `utils/prompts.py` | All prompt definitions (source of truth) |
| **Main App** | `app.py` | Streamlit application |
| **Project README** | `README.md` (root) | Project overview |
| **Requirements** | `requirements.txt` | Python dependencies |
| **FastAPI Main** | `backend/main.py` | FastAPI application ⭐ NEW |
| **React App** | `frontend/src/App.jsx` | React frontend ⭐ NEW |
| **API Client** | `frontend/src/api/client.js` | Axios API client ⭐ NEW |
| **Integration Guide** | `../QUICKSTART.md` | 5-minute setup ⭐ NEW |
| **Integration Docs** | `../README_INTEGRATION.md` | Detailed API docs ⭐ NEW |
| **Integration Summary** | `../INTEGRATION_SUMMARY.md` | Feature list ⭐ NEW |

---

## 🎯 Recommended Reading Paths

### Path 1: Quick Start with FastAPI + React (20 minutes) ⭐ NEW
1. [../QUICKSTART.md](../QUICKSTART.md) - 5 min
2. [FASTAPI_REACT_INTEGRATION.md](FASTAPI_REACT_INTEGRATION.md) - 15 min

**Result:** FastAPI + React running locally

### Path 2: Full Stack Developer Onboarding (60 minutes) ⭐ NEW
1. [../QUICKSTART.md](../QUICKSTART.md) - 5 min
2. [FASTAPI_REACT_INTEGRATION.md](FASTAPI_REACT_INTEGRATION.md) - 20 min
3. [MULTI_AGENT_ARCHITECTURE_STRATEGY.md](MULTI_AGENT_ARCHITECTURE_STRATEGY.md) - 25 min
4. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - 10 min

**Result:** Complete understanding of entire stack

### Path 3: Streamlit Developer (Traditional) (60 minutes)
1. [README.md](README.md) - 5 min
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 10 min
3. [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - 15 min
4. [PROMPT_STRATEGY.md](PROMPT_STRATEGY.md) - 30 min

**Result:** Full understanding of Streamlit system

### Path 4: Agent System Deep Dive (90 minutes)
1. [MULTI_AGENT_ARCHITECTURE_STRATEGY.md](MULTI_AGENT_ARCHITECTURE_STRATEGY.md) - 30 min
2. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - 20 min
3. [FASTAPI_REACT_INTEGRATION.md](FASTAPI_REACT_INTEGRATION.md) - 20 min
4. [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - 20 min

**Result:** Deep understanding of multi-agent system

---

## 📞 Getting Help

### For FastAPI + React Integration:
1. **Quick setup?** → Check [../QUICKSTART.md](../QUICKSTART.md)
2. **API questions?** → See [FASTAPI_REACT_INTEGRATION.md](FASTAPI_REACT_INTEGRATION.md)
3. **Detailed docs?** → Read [../README_INTEGRATION.md](../README_INTEGRATION.md)

### For Streamlit Application:
1. **Quick question?** → Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Need details?** → Search [PROMPT_STRATEGY.md](PROMPT_STRATEGY.md)
3. **Visual learner?** → See [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)
4. **Not sure where to start?** → Read [README.md](README.md)

### For Multi-Agent System:
1. **Architecture?** → [MULTI_AGENT_ARCHITECTURE_STRATEGY.md](MULTI_AGENT_ARCHITECTURE_STRATEGY.md)
2. **What's implemented?** → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
3. **How to use?** → [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

---

## ✏️ Contributing to Documentation

When updating docs:
1. Update the relevant document
2. Update version/date in document header
3. Update this INDEX.md if adding new sections
4. Keep in sync with implementation
5. Add to version history if major change

---

**Last Updated:** November 12, 2025
**Major Update:** Added FastAPI + React integration documentation
**Total Documentation Coverage:** Complete system coverage (Streamlit + FastAPI + React)
**Standards Alignment:** ATS, RACGP (5th Edition), Australian Privacy Principles
