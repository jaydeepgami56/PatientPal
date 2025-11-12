# Medical Triage AI - Architecture & Flow Diagrams

Visual representation of the system architecture, prompt flow, and guardrail enforcement.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEDICAL TRIAGE AI SYSTEM                     │
│                  (Australian Standards Compliant)                │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐       ┌───────▼────────┐
            │  PRE-VISIT     │       │   REAL-TIME    │
            │  REPORT PATH   │       │   TRIAGE PATH  │
            └───────┬────────┘       └───────┬────────┘
                    │                        │
        ┌───────────┴───────────┐   ┌────────┴─────────┐
        │                       │   │                  │
    ┌───▼──────┐         ┌──────▼───▼────┐     ┌──────▼───────┐
    │ INTERVIEW│         │ TRIAGE         │     │ CONVERSATIONAL│
    │ PROMPT   │────────▶│ ASSESSMENT     │◀────│ TRIAGE       │
    │ (15 Q's) │         │ (ATS 1-5)      │     │ (Interactive)│
    └───┬──────┘         └────────┬───────┘     └──────────────┘
        │                         │
        │                         │
    ┌───▼──────────┐             │
    │ REPORT       │             │
    │ GENERATION   │             │
    │ (RACGP)      │             │
    └───┬──────────┘             │
        │                        │
        └────────────┬───────────┘
                     │
              ┌──────▼──────┐
              │  GUARDRAIL  │
              │  VALIDATION │
              │  LAYER      │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │   OUTPUT    │
              │ (Validated) │
              └─────────────┘
```

---

## Prompt Flow Diagram

### 1. Interview → Report Flow

```
┌─────────────┐
│   START     │
│  Interview  │
└──────┬──────┘
       │
       │ Question 1: Opening + Chief Complaint
       ▼
┌──────────────────────────────────────┐
│  INTERVIEW_PROMPT                    │
│  ┌────────────────────────────────┐ │
│  │ Guardrails:                    │ │
│  │ • Max 15 questions             │ │
│  │ • Max 20 words per question    │ │
│  │ • No repetition                │ │
│  │ • No medical advice            │ │
│  └────────────────────────────────┘ │
└──────┬───────────────────────────────┘
       │
       │ Questions 2-14: Systematic info gathering
       │ ┌─────────────────────────┐
       │ │ • Symptom details       │
       │ │ • Associated symptoms   │
       │ │ • Medical history       │
       │ │ • Functional impact     │
       │ └─────────────────────────┘
       ▼
   ┌────────┐ No
   │ Q = 15 ├────┐
   │ or done│    │
   └───┬────┘    │
       │ Yes     │
       │        │
       │        └─────┐ Loop back
       ▼              │ for next Q
┌──────────────┐      │
│ END INTERVIEW│      │
│ (Exact phrase)◀─────┘
└──────┬───────┘
       │
       │ Collect: Interview transcript + EHR
       ▼
┌──────────────────────────────────────┐
│  REPORT_PROMPT                       │
│  ┌────────────────────────────────┐ │
│  │ Guardrails:                    │ │
│  │ • Start: ## Presenting Complaint│ │
│  │ • All 6 sections mandatory     │ │
│  │ • Australian terminology       │ │
│  │ • Third person                 │ │
│  │ • No diagnosis/advice          │ │
│  └────────────────────────────────┘ │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────┐
│  CLINICAL REPORT     │
│  (RACGP compliant)   │
│                      │
│  ## Presenting...    │
│  ## History of...    │
│  ## Pertinent Neg... │
│  ## Relevant Med...  │
│  ## Functional...    │
│  ## Patient Conc...  │
└──────────────────────┘
```

### 2. Conversational Triage Flow

```
┌─────────────┐
│   START     │
│   Triage    │
└──────┬──────┘
       │
       │ Patient describes symptoms
       ▼
┌──────────────────────────────────────┐
│ CONVERSATIONAL_TRIAGE_PROMPT         │
│                                      │
│  ┌─────────────────────────────────┐│
│  │ Decision Point:                 ││
│  │ Have we collected?              ││
│  │ ✓ Chief complaint              ││
│  │ ✓ Onset/duration               ││
│  │ ✓ Severity                     ││
│  │ ✓ Red flag screen              ││
│  │ ✓ Associated symptoms          ││
│  └─────────────────────────────────┘│
└──────┬───────────────────────────────┘
       │
       ├─No──▶ MODE A: ASK QUESTION
       │       │
       │       │ • Single question only
       │       │ • Max 20 words
       │       │ • No preamble
       │       │
       │       └──┐ Loop back with
       │          │ patient answer
       │          │
       └─Yes─▶ MODE B: PROVIDE ASSESSMENT
                │
                │ Immediate if RED FLAG detected
                │
                ▼
         ┌──────────────────┐
         │ TRIAGE ASSESSMENT│
         │                  │
         │ ATS Category: X  │
         │ Clinical Urgency │
         │ Recommended Action│
         │ Reasoning        │
         └──────────────────┘
```

### 3. Pre-Visit Report Triage Flow

```
┌─────────────────────┐
│  Pre-Visit Report   │
│  (Already completed)│
└──────┬──────────────┘
       │
       │ Full report text
       ▼
┌────────────────────────────────────────┐
│  TRIAGE_PROMPT                         │
│  ┌──────────────────────────────────┐ │
│  │ ATS Assessment Logic:            │ │
│  │                                  │ │
│  │ RED FLAGS?─Yes─▶ ATS 1 or 2     │ │
│  │      │                           │ │
│  │      No                          │ │
│  │      ▼                           │ │
│  │ SEVERE PAIN (8-10)?─Yes─▶ ATS 2/3│ │
│  │      │                           │ │
│  │      No                          │ │
│  │      ▼                           │ │
│  │ MODERATE PAIN (5-7)?─Yes─▶ ATS 3/4│ │
│  │      │                           │ │
│  │      No                          │ │
│  │      ▼                           │ │
│  │ MINOR ISSUES───────────▶ ATS 4/5│ │
│  └──────────────────────────────────┘ │
└────────┬───────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ STRUCTURED TRIAGE OUTPUT            │
│                                     │
│ ATS CATEGORY: [1-5]                │
│ CLINICAL DESCRIPTOR: [...]         │
│ TO BE SEEN WITHIN: [time]          │
│ CARE PATHWAY: [Call 000/ED/etc]   │
│ RED FLAGS IDENTIFIED: [Yes/No]     │
│ KEY CLINICAL FEATURES: [2-3]       │
│ SPECIAL CONSIDERATIONS: [...]      │
│ RECOMMENDED IMMEDIATE ACTIONS: [...] │
│ CLINICAL REASONING: [2-3 sentences]│
└─────────────────────────────────────┘
```

---

## Guardrail Enforcement Layers

```
┌─────────────────────────────────────────────────────────────┐
│               LLM OUTPUT GENERATION                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │  LAYER 1: PROMPT DESIGN   │
         │  ┌─────────────────────┐  │
         │  │ • Role definition   │  │
         │  │ • Clear instructions│  │
         │  │ • Decision criteria │  │
         │  │ • Format template   │  │
         │  │ • Prohibitions list │  │
         │  └─────────────────────┘  │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │  LAYER 2: OUTPUT RULES    │
         │  ┌─────────────────────┐  │
         │  │ • "Start with X"    │  │
         │  │ • "Select ONLY..."  │  │
         │  │ • "Max X sentences" │  │
         │  │ • "Must include..." │  │
         │  │ • Prohibited phrases│  │
         │  └─────────────────────┘  │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │  LAYER 3: EXAMPLES        │
         │  ┌─────────────────────┐  │
         │  │ ✅ Good: "ATS..."   │  │
         │  │ ❌ Bad: "Based..."  │  │
         │  │ Example outputs     │  │
         │  └─────────────────────┘  │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │ LAYER 4: POST-VALIDATION  │
         │  ┌─────────────────────┐  │
         │  │ validate_output()   │  │
         │  │ • Regex matching    │  │
         │  │ • Field presence    │  │
         │  │ • Choice validation │  │
         │  │ • Safety check      │  │
         │  └─────────────────────┘  │
         └───────────┬───────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   Valid│                    Invalid│
        ▼                         ▼
┌───────────────┐      ┌──────────────────┐
│ ACCEPT OUTPUT │      │ RETRY or ERROR   │
└───────────────┘      │ • Clean & retry  │
                       │ • Add clarification│
                       │ • Raise error    │
                       └──────────────────┘
```

---

## ATS Decision Tree

```
                    ┌─────────────────┐
                    │ PATIENT SYMPTOMS│
                    └────────┬────────┘
                             │
                  ┌──────────▼──────────┐
                  │ RED FLAG SCREENING  │
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
           ┌────▼─────┐             ┌────▼─────┐
           │ RED FLAG │             │    NO    │
           │ DETECTED │             │ RED FLAG │
           └────┬─────┘             └────┬─────┘
                │                        │
    ┌───────────┴───────────┐           │
    │                       │           │
┌───▼────┐            ┌─────▼────┐      │
│IMMEDIATELY│          │IMMINENTLY│      │
│LIFE-      │          │LIFE-     │      │
│THREATENING│          │THREATENING│     │
│(Arrest,   │          │(Chest pain│     │
│ Unconscious)│        │ Stroke)   │     │
└───┬────┘            └─────┬────┘      │
    │                       │           │
    │                       │           │
┌───▼────┐            ┌─────▼────┐      │
│ ATS 1  │            │  ATS 2   │      │
│Immediate│           │ 10 min   │      │
│Call 000 │           │Call 000 │      │
│NOW      │           │or ED     │      │
└─────────┘           └──────────┘      │
                                        │
                            ┌───────────▼─────────────┐
                            │ ASSESS PAIN SEVERITY     │
                            └───────────┬─────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
            ┌───────▼──────┐    ┌──────▼─────┐    ┌───────▼──────┐
            │SEVERE (8-10) │    │MODERATE(5-7)│    │ MILD (1-4)  │
            │Major trauma  │    │Moderate pain│    │Minor issues │
            └───────┬──────┘    └──────┬─────┘    └───────┬──────┘
                    │                  │                   │
            ┌───────▼──────┐    ┌──────▼─────┐    ┌───────▼──────┐
            │   ATS 2/3    │    │  ATS 3/4   │    │   ATS 4/5    │
            │ ED/Urgent Care│   │Urgent/GP   │    │  GP/Routine  │
            │  10-30 min   │    │ 30-60 min  │    │  60-120 min  │
            └──────────────┘    └────────────┘    └──────────────┘

SPECIAL POPULATION ADJUSTMENTS:
├─ Paediatric: Lower threshold for fever, dehydration, respiratory
├─ Pregnant: Lower threshold for abdominal pain, bleeding
├─ Elderly: Lower threshold for falls, confusion, infection
└─ Immunocompromised: Lower threshold for any infection signs
```

---

## Mode Separation Pattern

### Conversational/Interactive Prompts

```
┌─────────────────────────────────────────────────────┐
│          LLM RECEIVES PATIENT INPUT                 │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   DECISION LOGIC      │
         │                       │
         │ Sufficient info?      │
         │ Red flag present?     │
         │ Max questions reached?│
         └───────────┬───────────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
┌───────▼────────┐         ┌────────▼───────┐
│  MODE A        │         │   MODE B       │
│  QUESTION      │         │  ASSESSMENT    │
└───────┬────────┘         └────────┬───────┘
        │                           │
        │                           │
    ┌───▼───────────────┐   ┌───────▼──────────────┐
    │ OUTPUT:           │   │ OUTPUT:              │
    │                   │   │                      │
    │ [Question]?       │   │ TRIAGE ASSESSMENT:   │
    │                   │   │ ATS Category: X      │
    │ RULES:            │   │ Clinical Urgency...  │
    │ • Max 20 words    │   │                      │
    │ • No preamble     │   │ RULES:               │
    │ • No explanation  │   │ • Start immediately  │
    │ • Just question   │   │ • All fields present │
    │                   │   │ • 2-3 sentence max   │
    └───────────────────┘   └──────────────────────┘

    ❌ INVALID: Mixing modes
    "Let me ask about your pain. Based on what you said,
     it seems like ATS 3. On a scale of 0-10, how severe?"
```

---

## Constrained Choice Enforcement

```
┌─────────────────────────────────────┐
│  PROMPT INSTRUCTION                 │
│                                     │
│  ATS CATEGORY:                      │
│  [Select ONLY one number:          │
│   1, 2, 3, 4, or 5]                │
└────────────┬────────────────────────┘
             │
   ┌─────────▼─────────────────┐
   │   LLM GENERATION          │
   └─────────┬─────────────────┘
             │
   ┌─────────▼──────────────────┐
   │   POST-VALIDATION          │
   │                            │
   │   category = extract(...)  │
   │                            │
   │   if category not in       │
   │      [1, 2, 3, 4, 5]:     │
   │      raise ValidationError │
   └─────────┬──────────────────┘
             │
     ┌───────┴────────┐
     │                │
 Valid│           Invalid│
     ▼                ▼
┌─────────┐    ┌──────────────┐
│ ACCEPT  │    │ REJECT       │
│         │    │ • Log error  │
│ Continue│    │ • Retry with │
│ to next │    │   constraint │
│ step    │    │   reminder   │
└─────────┘    └──────────────┘

VALID OPTIONS MUST BE:
• Explicitly listed in prompt
• Exact string match
• Case-sensitive
• No variations allowed

EXAMPLE VALID SETS:
• ATS Categories: [1, 2, 3, 4, 5]
• Care Pathways: [Call 000, Emergency Department,
                   Urgent Care, GP Appointment, Telehealth]
• Urgency: [Immediately life-threatening,
            Imminently life-threatening, ...]
```

---

## Validation Pipeline

```
┌──────────────┐
│ LLM OUTPUT   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ 1. STRIP COMMON ARTIFACTS    │
│    • Markdown code blocks    │
│    • Extra whitespace        │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ 2. PREAMBLE DETECTION        │
│    Check starts with:        │
│    • "ATS CATEGORY:" OR      │
│    • "## Presenting..." OR   │
│    • First required field    │
└──────┬───────────────────────┘
       │
       ├─Found preamble─▶ CLEAN or REJECT
       │
       ▼
┌──────────────────────────────┐
│ 3. FIELD PRESENCE CHECK      │
│    All required fields?      │
│    • ATS CATEGORY            │
│    • CLINICAL DESCRIPTOR     │
│    • ... (all fields)        │
└──────┬───────────────────────┘
       │
       ├─Missing fields─▶ REJECT
       │
       ▼
┌──────────────────────────────┐
│ 4. CONSTRAINED CHOICE CHECK  │
│    Values in valid options?  │
│    • Category in [1-5]      │
│    • Descriptor in list     │
│    • Pathway in list        │
└──────┬───────────────────────┘
       │
       ├─Invalid choice─▶ REJECT
       │
       ▼
┌──────────────────────────────┐
│ 5. SAFETY CHECK              │
│    • No medical advice?      │
│    • No diagnosis?           │
│    • ATS 1 has "000"?       │
│    • Chest pain = ATS 2+?   │
└──────┬───────────────────────┘
       │
       ├─Safety violation─▶ REJECT
       │
       ▼
┌──────────────────────────────┐
│ 6. FORMAT-SPECIFIC CHECKS    │
│    Report: All sections?     │
│    Triage: Reasoning length? │
│    Question: Word count?     │
└──────┬───────────────────────┘
       │
       ├─Format error─▶ REJECT
       │
       ▼
┌──────────────────────────────┐
│ 7. AUSTRALIAN STANDARDS      │
│    • Correct spelling?       │
│    • "000" not "911"?       │
│    • Metric units?           │
└──────┬───────────────────────┘
       │
       ├─Standard violation─▶ WARNING (accept but log)
       │
       ▼
┌──────────────────────────────┐
│ ✅ VALIDATION PASSED         │
│    Return validated output   │
└──────────────────────────────┘
```

---

## Document Cross-Reference Map

```
┌─────────────────────────────────────────────────────┐
│              DOCUMENTATION ECOSYSTEM                 │
└─────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼───────┐  ┌────▼────────┐
│ ARCHITECTURE │  │   PROMPT     │  │    QUICK    │
│  DIAGRAM.md  │  │ STRATEGY.md  │  │ REFERENCE.md│
│ (This file)  │  │ (Complete)   │  │ (Cheat sheet)│
└───────┬──────┘  └──────┬───────┘  └────┬────────┘
        │                │                │
        │    Visual      │  Detailed      │  At-a-glance
        │    flows       │  explanations  │  lookups
        │                │                │
        └────────────────┴────────────────┘
                         │
              ┌──────────▼──────────┐
              │   IMPLEMENTATION    │
              │   utils/prompts.py  │
              │   (Source of truth) │
              └─────────────────────┘
```

**Use this diagram file for:**
- Understanding system flow
- Visualizing decision logic
- Onboarding new team members
- Presentations and reviews
- Architecture documentation

**For detailed specifications:** See PROMPT_STRATEGY.md
**For quick reference:** See QUICK_REFERENCE.md
**For code implementation:** See `utils/prompts.py`

---

**Version:** 1.0 | **Last Updated:** October 2024
