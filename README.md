# 🏥 Multi-Agent Healthcare AI System

A comprehensive multi-agent healthcare AI platform built with Streamlit, LangChain, and Hugging Face. The system features specialized AI agents for medical diagnostics, treatment recommendations, radiology analysis, dermatology assessment, and patient triage—all orchestrated through an intelligent Supervisor Agent.

## 📋 Table of Contents

- [Overview](#overview)
- [System Workflow](#system-workflow)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Technologies](#technologies)

---

## 🎯 Overview

The Medical Triage AI Agent is a multi-phase intelligent system that:
- Conducts structured patient interviews using conversational AI
- Collects comprehensive medical information systematically
- Generates detailed pre-visit reports for healthcare providers
- Assigns triage priority levels (1-5) based on urgency
- Provides actionable recommendations for appropriate care pathways

**⚠️ DISCLAIMER**: This is a prototype for educational purposes. Always consult healthcare professionals for medical advice.

---

## 🔄 System Workflow

### Overall System Flow

```mermaid
flowchart TD
    Start([User Opens App]) --> Init[Initialize Application<br/>Load env, CSS, Clear Cache]
    Init --> Landing[Landing Page<br/>app.py]

    Landing --> |Click Launch| Welcome[Phase 1: Welcome<br/>Show Instructions]

    Welcome --> |Start Interview| Interview[Phase 2: Interview<br/>AI-Powered Q&A]
    Interview --> |Ask Questions| AI1[GPT-4 Analysis<br/>Extract Symptoms]
    AI1 --> |Generate Next Question| Interview
    Interview --> |8-12 Questions Complete| Report

    Report[Phase 3: Report Generation] --> AI2[GPT-4 Report Creation<br/>Structure Medical Data]
    AI2 --> ReportDisplay[Display Pre-Visit Report<br/>Download Option]

    ReportDisplay --> |Generate Triage| Triage[Phase 4: Triage Assessment]
    Triage --> AI3[GPT-4 Triage Analysis<br/>Assign Priority Level]
    AI3 --> TriageDisplay[Display Triage Results<br/>Level 1-5 Classification]

    TriageDisplay --> Download[Download Reports]
    Download --> Decision{New Assessment?}
    Decision --> |Yes| Welcome
    Decision --> |No| End([Session Complete])

    style Start fill:#10b981,stroke:#059669,color:#fff
    style Landing fill:#3b82f6,stroke:#2563eb,color:#fff
    style Welcome fill:#8b5cf6,stroke:#6d28d9,color:#fff
    style Interview fill:#f59e0b,stroke:#d97706,color:#fff
    style Report fill:#ec4899,stroke:#db2777,color:#fff
    style Triage fill:#ef4444,stroke:#dc2626,color:#fff
    style AI1 fill:#fbbf24,stroke:#f59e0b,color:#000
    style AI2 fill:#f472b6,stroke:#ec4899,color:#fff
    style AI3 fill:#fca5a5,stroke:#ef4444,color:#000
```

### Triage Level Classification

```mermaid
graph TD
    A[Patient Symptoms] --> B{AI Analysis}

    B --> |Life-threatening| L1[Level 1: CRITICAL<br/>Immediate 911<br/>Examples: Chest pain, Stroke]
    B --> |Severe/Urgent| L2[Level 2: EMERGENCY<br/>Within 30 min<br/>Examples: High fever, Severe pain]
    B --> |Moderate| L3[Level 3: URGENT<br/>Within 2 hours<br/>Examples: Persistent vomiting]
    B --> |Mild| L4[Level 4: SEMI-URGENT<br/>1-2 hours<br/>Examples: Minor injuries]
    B --> |Non-urgent| L5[Level 5: NON-URGENT<br/>Same day<br/>Examples: Chronic issues]

    style L1 fill:#ef4444,stroke:#dc2626,color:#fff
    style L2 fill:#f97316,stroke:#ea580c,color:#fff
    style L3 fill:#eab308,stroke:#ca8a04,color:#000
    style L4 fill:#84cc16,stroke:#65a30d,color:#000
    style L5 fill:#22c55e,stroke:#16a34a,color:#fff
```

### Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant LangChain
    participant OpenAI
    participant SessionState

    User->>Streamlit: Opens Application
    Streamlit->>SessionState: Initialize State
    Streamlit->>User: Display Landing Page

    User->>Streamlit: Start Interview
    Streamlit->>SessionState: Store Phase: Interview

    loop Interview Questions
        User->>Streamlit: Provide Answer
        Streamlit->>LangChain: Process Answer
        LangChain->>OpenAI: Send Prompt + Context
        OpenAI-->>LangChain: AI Response
        LangChain-->>Streamlit: Next Question
        Streamlit->>SessionState: Update interview_data
        Streamlit->>User: Display Question
    end

    User->>Streamlit: Complete Interview
    Streamlit->>LangChain: Generate Report
    LangChain->>OpenAI: REPORT_PROMPT + Transcript
    OpenAI-->>LangChain: Structured Report
    LangChain-->>Streamlit: Report Content
    Streamlit->>SessionState: Store Report
    Streamlit->>User: Display Report

    User->>Streamlit: Generate Triage
    Streamlit->>LangChain: Analyze Urgency
    LangChain->>OpenAI: TRIAGE_PROMPT + Report
    OpenAI-->>LangChain: Triage Assessment
    LangChain-->>Streamlit: Level + Reasoning
    Streamlit->>SessionState: Store Assessment
    Streamlit->>User: Display Triage Level
```

---

## 🏗️ Architecture

### System Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Streamlit UI<br/>HTML/CSS/Markdown]
    end

    subgraph "Application Layer"
        APP[app.py<br/>Landing Page]
        TRIAGE[Triage_agent.py<br/>Main Application]
        STATE[Session State<br/>Data Storage]
    end

    subgraph "Utility Layer"
        PROMPTS[prompts.py<br/>AI Templates]
        UTILS[common_utils.py<br/>Helper Functions]
        STYLES[style_loader.py<br/>CSS Manager]
    end

    subgraph "AI Layer"
        LC[LangChain<br/>Framework]
        MEMORY[ConversationBufferMemory]
    end

    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4]
    end

    subgraph "Static Assets"
        CSS1[app_style.css]
        CSS2[triage_agent_style.css]
    end

    UI --> APP
    UI --> TRIAGE
    TRIAGE --> STATE
    TRIAGE --> PROMPTS
    TRIAGE --> UTILS
    TRIAGE --> STYLES
    STYLES --> CSS1
    STYLES --> CSS2
    TRIAGE --> LC
    LC --> MEMORY
    LC --> OPENAI
    PROMPTS --> LC

    style UI fill:#3b82f6,stroke:#2563eb,color:#fff
    style APP fill:#8b5cf6,stroke:#6d28d9,color:#fff
    style TRIAGE fill:#ec4899,stroke:#db2777,color:#fff
    style LC fill:#f59e0b,stroke:#d97706,color:#fff
    style OPENAI fill:#10b981,stroke:#059669,color:#fff
```

### Component Architecture

```mermaid
classDiagram
    class App {
        +display_landing()
        +load_css()
        +render_features()
    }

    class TriageAgent {
        -session_state
        -interview_data
        -llm: ChatOpenAI
        +conduct_interview()
        +generate_report()
        +assess_triage()
        +reset_assessment()
    }

    class Prompts {
        +TRIAGE_PROMPT
        +INTERVIEW_PROMPT
        +REPORT_PROMPT
        +INTERACTIVE_TRIAGE_PROMPT
    }

    class CommonUtils {
        +get_env_variable()
        +log_message()
        +clear_all_caches()
    }

    class StyleLoader {
        +load_css()
        +load_app_style()
        +load_triage_agent_style()
    }

    class LangChainWrapper {
        -llm: ChatOpenAI
        -memory: ConversationBufferMemory
        +process_input()
        +generate_response()
    }

    TriageAgent --> Prompts
    TriageAgent --> CommonUtils
    TriageAgent --> StyleLoader
    TriageAgent --> LangChainWrapper
    App --> StyleLoader
    LangChainWrapper --> OpenAI
```

### Technology Stack

```mermaid
graph LR
    subgraph "Frontend"
        A[Streamlit 1.29.0]
        B[Custom CSS]
        C[HTML/Markdown]
    end

    subgraph "Backend"
        D[Python 3.8+]
        E[LangChain 0.0.300+]
        F[LangChain-OpenAI 0.0.2+]
    end

    subgraph "AI/ML"
        G[OpenAI GPT-4]
        H[tiktoken]
    end

    subgraph "Utilities"
        I[python-dotenv]
    end

    A --> D
    D --> E
    E --> F
    F --> G
    D --> I
    E --> H
```

---

## ✨ Features

### 🎨 Landing Page
- Modern, futuristic UI with gradient backgrounds
- Interactive feature cards with hover effects
- Clear explanation of triage AI capabilities
- Step-by-step process visualization
- Responsive design for mobile and desktop

### 🤖 AI-Powered Interview System
- Natural language conversation with GPT-4
- Context-aware follow-up questions
- Automatic symptom extraction
- Real-time data collection and tracking
- Progress indicator in sidebar
- 8-12 adaptive questions based on responses

### 📊 Intelligent Report Generation
- Comprehensive structured reports
- Medical terminology and formatting
- Sections include:
  - Chief Complaint
  - Present Illness
  - Symptom Analysis (onset, duration, severity)
  - Medical History
  - Current Medications
  - Allergies
  - Red Flags Identified
  - Provider Recommendations
- Downloadable as text files

### 🏥 Clinical Triage Assessment
- 5-level triage system (ESI/CTAS compliant)
- AI-powered urgency classification
- Color-coded visual indicators
- Critical alert system for emergencies
- Evidence-based reasoning
- Specific recommendations for each level

### 🎛️ Utility Features
- Automatic cache clearing on startup
- Session state management
- Custom CSS styling system
- Error handling with user-friendly messages
- Logging utilities for debugging
- Responsive design

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Streamlit-App
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**How to get an OpenAI API key:**
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key
5. Copy and paste into `.env` file

---

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Navigation

1. **Landing Page** (`app.py`)
   - Learn about the triage AI system
   - Click "🚀 Launch Triage Agent" or use sidebar navigation

2. **Triage Agent** (sidebar: "Triage agent")
   - Start pre-visit interview
   - Answer questions naturally
   - Review generated report
   - View triage assessment

### Workflow Steps

1. **Start Interview**: Click "🚀 Start Pre-Visit Interview"
2. **Answer Questions**: Respond to AI questions about symptoms (8-12 questions)
3. **Complete Interview**: Click "✅ Complete Interview & Generate Report"
4. **Review Report**: Read the generated pre-visit report
5. **Download Report**: Save the report for your records
6. **Generate Triage**: Click "🏥 Generate Triage Assessment"
7. **Review Assessment**: View urgency level (1-5) and recommendations
8. **Download Assessment**: Save triage results
9. **New Assessment**: Click "🔄 Start New Assessment" to begin again

---

## 📁 Project Structure

```
Streamlit-App/
│
├── app.py                          # Landing page
├── .env                            # Environment variables (create this)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── pages/                          # Streamlit multi-page app
│   └── Triage_agent.py            # Main triage application
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── prompts.py                 # AI prompt templates
│   ├── common_utils.py            # Helper functions
│   └── style_loader.py            # CSS loading utilities
│
└── styles/                         # CSS styling files
    ├── app_style.css              # Landing page styles
    └── triage_agent_style.css     # Triage agent styles
```

### Key Files Description

| File | Purpose | Lines |
|------|---------|-------|
| `app.py` | Main landing page with project overview | ~264 |
| `pages/Triage_agent.py` | Core triage workflow implementation | ~330 |
| `utils/prompts.py` | AI prompt templates for interview/report/triage | ~193 |
| `utils/common_utils.py` | Utility functions (logging, cache management) | ~81 |
| `utils/style_loader.py` | CSS loading and management | ~68 |
| `styles/app_style.css` | Landing page styling | ~278 |
| `styles/triage_agent_style.css` | Triage agent page styling | ~87 |

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes | None |

### Streamlit Configuration

```python
# Page configuration (app.py)
st.set_page_config(
    page_title="Triage AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Model Configuration

```python
# Current configuration (Triage_agent.py)
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4o-mini",
    openai_api_key=api_key
)
```

**Available Models:**
- `gpt-4` - Most capable, higher cost
- `gpt-4o-mini` - Balanced performance and cost (current)
- `gpt-3.5-turbo` - Faster, lower cost

**Temperature Settings:**
- `0.0-0.3` - More focused and deterministic
- `0.7` - Balanced creativity (current)
- `0.8-1.0` - More creative and varied

---

## 🛠️ Technologies

### Core Framework
- **Streamlit** (v1.29.0): Web application framework
- **Python** (3.8+): Programming language

### AI/ML
- **LangChain** (>=0.0.300): LLM application framework
- **LangChain-OpenAI** (>=0.0.2): OpenAI integration
- **OpenAI API** (>=0.27.8): GPT-4 access
- **tiktoken** (>=0.4.0): Token counting for OpenAI

### Utilities
- **python-dotenv** (v1.0.0): Environment variable management

### UI/UX
- **Custom CSS**: Modern glass morphism design
- **Google Fonts**: Inter font family
- **Responsive Design**: Mobile and desktop support

---

## 🔒 Security & Privacy

- **No data persistence**: All data is session-based and cleared on restart
- **API key security**: Store keys in `.env` file (never commit to Git)
- **Local processing**: All processing happens on your machine
- **No external database**: No patient data is stored externally
- **Automatic cache clearing**: Sensitive data cleared on app restart

**Important**: This is a prototype. For production use:
- Implement proper authentication
- Add encryption for sensitive data
- Comply with HIPAA/healthcare regulations
- Use secure API key management (e.g., AWS Secrets Manager)
- Add audit logging
- Implement data retention policies

---

## 🐛 Troubleshooting

### Common Issues

**1. CSS not loading or page looks unstyled**
```bash
# Solution: Restart the Streamlit app
Ctrl+C  # Stop the app
streamlit run app.py  # Restart
```
Cache is automatically cleared on startup.

**2. "Module not found" errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**3. "API key not found" error**
```bash
# Solution: Check .env file
# 1. Verify .env file exists in root directory
# 2. Check format: OPENAI_API_KEY=sk-...
# 3. Restart the app after creating .env
```

**4. Triage agent page not visible in sidebar**
```bash
# Solution 1: Check sidebar is expanded (arrow in top-left)
# Solution 2: Verify langchain-openai is installed
pip install langchain-openai
# Solution 3: Restart the app
```

**5. Slow response times**
```bash
# Possible causes:
# - OpenAI API rate limits
# - Network latency
# - Large conversation history

# Solutions:
# - Check internet connection
# - Verify API quota at platform.openai.com
# - Start new assessment to clear history
```

**6. Import errors with utils modules**
```bash
# Solution: Python path issues
# The app automatically adds parent directory to path
# If still failing, run from root directory:
cd Streamlit-App
streamlit run app.py
```

---

## 📊 Performance Considerations

### Response Times
- **Interview questions**: 2-5 seconds per response
- **Report generation**: 10-20 seconds
- **Triage assessment**: 5-10 seconds

### Token Usage (Approximate)
- **Interview** (8-12 questions): 3,000-5,000 tokens
- **Report generation**: 2,000-3,000 tokens
- **Triage assessment**: 1,500-2,500 tokens
- **Total per session**: ~7,000-10,000 tokens

### Cost Estimation (GPT-4o-mini)
- **Per session**: $0.01-0.02 USD
- **100 sessions**: $1-2 USD

---

## 📝 License

This project is for educational and demonstration purposes.

---

## 🤝 Contributing

This is a prototype project. To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Update README for new features
- Test with multiple scenarios
- Keep functions small and focused

---

## 📧 Support

For questions or issues:
- Check the [Troubleshooting](#troubleshooting) section
- Review [Streamlit documentation](https://docs.streamlit.io/)
- Check [LangChain documentation](https://python.langchain.com/)
- Review [OpenAI documentation](https://platform.openai.com/docs)

---

## ⚠️ Medical Disclaimer

**THIS IS A PROTOTYPE FOR EDUCATIONAL PURPOSES ONLY**

This application:
- ❌ Is NOT approved for clinical use
- ❌ Is NOT a substitute for professional medical advice
- ❌ Should NOT be used for actual medical decisions
- ❌ Has NOT been validated by healthcare professionals
- ❌ Does NOT comply with HIPAA or medical regulations

**Always:**
- ✅ Consult qualified healthcare professionals
- ✅ Call 911 for emergencies
- ✅ Seek professional medical advice for health concerns
- ✅ Use only for educational and demonstration purposes

---

## 🎯 Future Enhancements

Potential improvements for production version:
- [ ] Multi-language support
- [ ] Voice input/output capabilities
- [ ] Integration with EHR/EMR systems
- [ ] Advanced symptom checker with medical knowledge graphs
- [ ] Patient authentication system
- [ ] Appointment scheduling integration
- [ ] PDF report generation with medical formatting
- [ ] Analytics dashboard for healthcare providers
- [ ] Mobile app version
- [ ] HIPAA compliance features

---

## 🙏 Acknowledgments

- Inspired by **Google's Appoint Ready MedGemma Demo**
- Built with **Streamlit's** amazing framework
- Powered by **OpenAI's GPT-4**
- UI design inspired by modern healthcare applications
- Triage protocols based on ESI and CTAS standards

---

## 📈 Version History

### Version 1.0.0 (January 2025)
- Initial release
- 4-phase triage workflow
- AI-powered interview system
- Report and triage generation
- Multi-page Streamlit app
- Custom CSS styling
- Utility functions and helpers

---

**Version**: 1.0.0
**Last Updated**: January 2025
**Status**: Prototype / Educational Demo
**Maintainer**: [Your Name/Organization]

---

Made with ❤️ for improving healthcare accessibility through AI

🏥 **Medical Triage AI Agent** | 🤖 **Powered by GPT-4** | 🚀 **Built with Streamlit**
