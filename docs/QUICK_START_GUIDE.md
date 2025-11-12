# Quick Start Guide - Lead Agent System

**Last Updated:** 2025-11-11

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd c:\Dev\Streamlit-App
pip install -r requirements.txt
```

Required packages:
- `streamlit`
- `langchain-openai`
- `langchain-huggingface`
- `transformers`
- `pydantic`
- `python-dotenv`
- `Pillow`

---

### Step 2: Configure API Keys

Create or update `.env` file in project root:

```env
# Required for Lead Agent orchestration and routing
OPENAI_API_KEY=sk-your-openai-key-here

# Required for HuggingFace specialist agents
HUGGINGFACE_API_KEY=hf_your-huggingface-key-here
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- HuggingFace: https://huggingface.co/settings/tokens

---

### Step 3: Run the Application

```bash
streamlit run app.py
```

Then navigate to **Lead Agent** in the sidebar! 🎉

---

## 📂 Project Structure (After Implementation)

```
Streamlit-App/
├── app.py                          # Main landing page
├── .env                           # API keys (create this)
├── requirements.txt               # Python dependencies
│
├── agents/                        # ✨ NEW - Specialist agent modules
│   ├── __init__.py
│   ├── medgemma_agent.py          # General medical queries
│   ├── txgemma_agent.py           # Treatment recommendations
│   ├── derm_agent.py              # Dermatology (image required)
│   ├── cxr_agent.py               # Chest X-ray (image required)
│   └── pathology_agent.py         # Histopathology analysis
│
├── pages/                         # Streamlit pages
│   ├── Lead_Agent.py              # ⭐ Main orchestrator UI
│   ├── Triage_agent.py            # Pre-visit triage workflow
│   ├── Agent_Configuration.py     # Agent settings
│   └── Results_Dashboard.py       # Analytics (if exists)
│
├── utils/                         # Utilities
│   ├── agent_base.py              # Base agent classes (existing)
│   ├── memory.py                  # ✨ NEW - Three-tier memory
│   ├── orchestrator.py            # ✨ NEW - Lead Agent orchestrator
│   ├── prompts.py                 # ✨ UPDATED - Added routing prompts
│   └── logger.py                  # Logging utilities (existing)
│
├── docs/                          # Documentation
│   ├── MULTI_AGENT_ARCHITECTURE_STRATEGY.md  # Full architecture
│   ├── IMPLEMENTATION_SUMMARY.md              # What we built
│   └── QUICK_START_GUIDE.md                   # This file
│
└── styles/                        # CSS styling
    └── app_style.css
```

---

## 🎯 How to Use Lead Agent

### 1. Navigate to Lead Agent

After running the app, click **"Lead Agent"** in the sidebar.

---

### 2. Enter Your Query

**Example Queries:**

#### General Medical:
```
"What are the symptoms of Type 2 diabetes?"
"How does high blood pressure affect the heart?"
"Explain the difference between viral and bacterial infections"
```

#### Treatment & Medication:
```
"Treatment options for hypertension"
"How does metformin work?"
"Side effects of antibiotics"
```

#### Multi-Domain:
```
"I have chest pain and a skin rash. What could this be?"
→ Automatically routes to multiple agents in parallel
```

#### With Image (Dermatology):
```
1. Upload skin lesion image
2. Query: "Analyze this skin lesion. Should I be concerned?"
→ Automatically routes to Derm Foundation
```

#### With Image (Radiology):
```
1. Upload chest X-ray
2. Query: "Interpret this chest X-ray and recommend treatment"
→ Automatically routes to CXR Foundation → Treatment agent
```

---

### 3. Review Results

The system will show:
- **Routing Decision:** Which agent(s) were selected and why
- **Agent Responses:** Individual responses (if multiple agents)
- **Synthesized Output:** Unified, coherent response
- **Confidence & Timing:** Processing metrics

---

## 🔥 Key Features

### 1. Automatic Routing
You **don't need to know** which agent to use. The system analyzes your query and routes automatically.

### 2. Multi-Agent Consultation
For complex queries spanning multiple domains, the system consults multiple specialists in parallel.

### 3. Emergency Detection
Queries with emergency keywords (chest pain, can't breathe, etc.) automatically bypass to immediate emergency guidance.

### 4. Image Analysis
Upload images for:
- Skin lesion analysis (dermatology)
- Chest X-ray interpretation (radiology)

### 5. Context Memory
The system remembers your conversation for follow-up queries.

---

## 💡 Tips for Best Results

### 1. Be Specific
❌ "I feel bad"
✅ "I have a persistent headache for 3 days with nausea"

### 2. Mention Image Type
When uploading images:
✅ "Analyze this skin rash" (clearly dermatology)
✅ "Interpret this chest X-ray" (clearly radiology)

### 3. Multi-Part Queries
You can ask complex questions:
✅ "What causes pneumonia and what are the treatment options?"
→ System will route to appropriate agents

### 4. Follow-Up Questions
The system maintains context:
```
Query 1: "What is Type 2 diabetes?"
Query 2: "What are the treatment options for it?"
→ System remembers "it" refers to Type 2 diabetes
```

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** Create `.env` file with your OpenAI API key

### Issue: "Failed to initialize agent"
**Solution:** Check HUGGINGFACE_API_KEY in `.env` file

### Issue: "Agent requires image"
**Solution:** Upload image when asking about skin lesions or X-rays

### Issue: Slow first query to each agent
**Expected:** Agents initialize on first use. Subsequent queries are faster.

### Issue: "No module named 'agents'"
**Solution:** Make sure `agents/__init__.py` exists and Python can find the package

---

## 📊 What Happens Behind the Scenes

```
Your Query
    ↓
1. Safety Check (emergency keywords?)
    ↓
2. LLM Routing (which agent(s)?)
    ↓
3. Agent Execution (single/parallel/sequential)
    ↓
4. Result Synthesis (combine if multiple)
    ↓
Your Response
```

---

## 🎓 Example Session

```
User: "What are the symptoms of pneumonia?"

Lead Agent:
├─ Safety Check: ✅ No emergency
├─ Routing: MedGemma (general medical)
├─ Execution: Single agent
└─ Response: [Detailed symptoms of pneumonia]
   Time: ~2 seconds

---

User: "What treatment would you recommend?"

Lead Agent:
├─ Context: Remembers previous query about pneumonia
├─ Routing: TxGemma (treatment recommendations)
├─ Execution: Single agent
└─ Response: [Treatment options for pneumonia]
   Time: ~2 seconds

---

User: "I have this rash too" + [uploads image]

Lead Agent:
├─ Routing: Derm Foundation (image analysis)
├─ Execution: Analyzes skin image
└─ Response: [Dermatological analysis]
   Time: ~3 seconds
```

---

## 🔐 Safety & Disclaimers

### Automatic Safety Features:
- Emergency keyword detection
- Automatic escalation to emergency guidance
- Medical disclaimers on all responses
- Recommends professional consultation

### Important Notes:
⚠️ This is an AI system for **informational purposes only**
⚠️ **Not a substitute** for professional medical advice
⚠️ Always consult qualified healthcare professionals
⚠️ For emergencies in Australia: **Call 000**

---

## 📈 Performance Expectations

| Query Type | Time | Notes |
|------------|------|-------|
| Simple query | ~2s | Single agent |
| Multi-domain | ~4s | Parallel execution |
| Image + treatment | ~8s | Sequential pipeline |
| Emergency | <1s | Bypasses routing |

---

## 🎉 You're Ready!

Run the app and start exploring:

```bash
streamlit run app.py
```

Navigate to **Lead Agent** and ask your first question! 🚀

---

## 📚 Further Reading

- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - What we built and how it works
- **[MULTI_AGENT_ARCHITECTURE_STRATEGY.md](./MULTI_AGENT_ARCHITECTURE_STRATEGY.md)** - Complete architecture details

---

**Last Updated:** 2025-11-11
**Status:** ✅ Production Ready
