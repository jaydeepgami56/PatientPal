# Medical Triage AI - Prompt Engineering Strategy & Guardrails

**Version:** 1.0
**Last Updated:** October 2024
**Standards Alignment:** Australian Health Standards (ATS, RACGP)

---

## Table of Contents

1. [Overview](#overview)
2. [Australian Health Standards Compliance](#australian-health-standards-compliance)
3. [Prompt Architecture](#prompt-architecture)
4. [Guardrail System](#guardrail-system)
5. [Individual Prompt Specifications](#individual-prompt-specifications)
6. [Output Format Enforcement](#output-format-enforcement)
7. [Validation Strategies](#validation-strategies)
8. [Clinical Safety Measures](#clinical-safety-measures)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This document details the prompt engineering strategy for the Medical Triage AI system, which uses Large Language Models (LLMs) to conduct patient interviews, assess clinical urgency, and generate documentation compliant with Australian healthcare standards.

### Core Objectives

1. **Clinical Safety**: Prioritize patient safety through conservative triage and clear red flag detection
2. **Standards Compliance**: Align with Australasian Triage Scale (ATS) and RACGP documentation standards
3. **Output Consistency**: Enforce structured, parseable outputs through strict guardrails
4. **Professional Quality**: Generate clinical documentation suitable for GP review and medical records

### System Components

The system consists of **5 main prompts**:

| Prompt | Purpose | Output Type |
|--------|---------|-------------|
| `TRIAGE_PROMPT` | Assess pre-visit reports and assign ATS category | Structured assessment |
| `CONVERSATIONAL_TRIAGE_PROMPT` | Interactive symptom gathering and triage | Questions OR assessment |
| `INTERACTIVE_TRIAGE_PROMPT` | Structured questioning sequence | Single questions |
| `INTERVIEW_PROMPT` | GP pre-visit patient interview | Single questions |
| `REPORT_PROMPT` | Generate clinical documentation | Structured markdown report |

---

## Australian Health Standards Compliance

### Australasian Triage Scale (ATS)

All triage prompts implement the official 5-category ATS system:

| Category | Descriptor | Time Frame | Examples |
|----------|-----------|------------|----------|
| **ATS 1** | Immediately life-threatening | Immediate | Cardiac arrest, respiratory arrest, uncontrollable haemorrhage |
| **ATS 2** | Imminently life-threatening | Within 10 minutes | Chest pain (cardiac features), severe respiratory distress, stroke |
| **ATS 3** | Potentially life-threatening | Within 30 minutes | Moderate-severe pain (5-7/10), persistent vomiting, moderate trauma |
| **ATS 4** | Potentially serious | Within 60 minutes | Minor fractures, moderate pain (3-4/10), urinary retention |
| **ATS 5** | Less urgent | Within 120 minutes | Minor wounds, chronic conditions, prescription requests |

**Key ATS Principles Embedded in Prompts:**

- ✅ Precautionary principle: when uncertain, triage higher
- ✅ Special population considerations: paediatric, pregnancy, elderly, immunocompromised
- ✅ Red flag screening: airway, breathing, circulation, consciousness
- ✅ Pain scales (0-10) aligned with ATS categories
- ✅ Australian emergency number: **000** (not 911)

### RACGP Standards (5th Edition)

Clinical documentation prompts comply with RACGP Standards for General Practices:

**Documentation Requirements:**
- Australian medical terminology and spelling (paediatric, haemoptysis, oedema)
- Australian units (°C, kg, cm)
- Structured clinical sections (History of Presenting Complaint, Pertinent Negatives)
- Factual, objective documentation only
- Australian Privacy Principles compliance
- Third-person medical writing style

**Mandatory Report Sections:**
1. Presenting Complaint
2. History of Presenting Complaint (HPC)
3. Pertinent Negatives
4. Relevant Medical History
5. Functional Impact
6. Patient Concerns or Questions

---

## Prompt Architecture

### Design Philosophy

Each prompt follows a **layered structure**:

```
┌─────────────────────────────────────┐
│  1. ROLE DEFINITION                 │  ← Who the AI is
├─────────────────────────────────────┤
│  2. KNOWLEDGE BASE                  │  ← Clinical guidelines (ATS/RACGP)
├─────────────────────────────────────┤
│  3. TASK INSTRUCTIONS               │  ← What to do
├─────────────────────────────────────┤
│  4. DECISION CRITERIA               │  ← When to switch modes
├─────────────────────────────────────┤
│  5. OUTPUT GUARDRAILS               │  ← How to format output
├─────────────────────────────────────┤
│  6. PROHIBITIONS                    │  ← What NOT to do
└─────────────────────────────────────┘
```

### Common Patterns

**1. Mode Separation**
All conversational prompts separate "questioning mode" from "assessment mode":
- **Questioning Mode**: Output ONLY a single question (max 20 words)
- **Assessment Mode**: Output ONLY structured assessment (no preamble)

**2. Constrained Choices**
Wherever possible, provide explicit options:
- ✅ "Select ONLY one: 1/2/3/4/5"
- ❌ "Assign a category" (too open-ended)

**3. Explicit Examples**
Show both correct and incorrect patterns:
- ✅ Good example: `"ATS CATEGORY: 2"`
- ❌ Bad example: `"Based on the report, I assess..."`

**4. Mandatory Field Enforcement**
- All fields required
- If no information available: "None", "Not discussed", or "N/A"
- Never skip sections

---

## Guardrail System

### Global Validation Rules

These **8 rules** apply across ALL prompts:

```python
# From prompts.py lines 16-29

1. NO PREAMBLE
   ❌ "Here is...", "Based on...", "I will..."
   ✅ Start immediately with required output

2. NO POSTAMBLE
   ❌ "I hope...", "Please let me know...", "Is there..."
   ✅ End immediately after last required field

3. EXACT HEADINGS
   ❌ "Chief Complaint" (when template says "Presenting Complaint")
   ✅ Character-for-character match to template

4. CONSTRAINED CHOICES
   ❌ Inventing new categories or descriptors
   ✅ Select ONLY from provided options

5. MANDATORY FIELDS
   ❌ Skipping sections or fields
   ✅ All fields present, use "None" if not applicable

6. SINGLE MODE
   ❌ Asking question AND providing assessment
   ✅ Choose ONE: question OR assessment

7. NO META-COMMENTARY
   ❌ "I'm going to ask about...", "Let me check..."
   ✅ Just ask or assess directly

8. IMMEDIATE START
   ❌ Any introductory text before first field
   ✅ First character of output = first character of required format
```

### Enforcement Mechanisms

**1. Explicit Start/End Instructions**
```
"Begin your response IMMEDIATELY with 'ATS CATEGORY:'"
"END immediately after '## Patient Concerns or Questions' section"
```

**2. Prohibited Phrase Lists**
```
PROHIBITED OUTPUTS:
❌ "Based on the interview conducted..."
❌ "Here is the clinical report..."
❌ "This report summarizes..."
```

**3. Field Constraints**
```
ATS CATEGORY: [Select ONLY one number: 1, 2, 3, 4, or 5]
KEY CLINICAL FEATURES: [Exactly 2-3 bullet points, one per line]
CLINICAL REASONING: [Maximum 2-3 sentences explaining ATS category assignment]
```

**4. Format Examples**
```
Example: "On a scale of 0-10, how severe is your pain right now?"
NOT: "I'd like to understand your pain level. Could you please tell me..."
```

---

## Individual Prompt Specifications

### 1. TRIAGE_PROMPT

**File Location:** `utils/prompts.py:38-86`

**Purpose:** Analyze pre-visit reports and assign ATS category

**Input Variables:**
- `{report}` - The pre-visit patient report text

**Output Structure:**
```
ATS CATEGORY: [1-5]
CLINICAL DESCRIPTOR: [ATS descriptor]
TO BE SEEN WITHIN: [Timeframe]
CARE PATHWAY: [Call 000/ED/Urgent Care/GP/Telehealth]
RED FLAGS IDENTIFIED: [Yes/No - list if yes]
KEY CLINICAL FEATURES: [2-3 bullet points]
SPECIAL CONSIDERATIONS: [Age/pregnancy/comorbidities or "None"]
RECOMMENDED IMMEDIATE ACTIONS: [Specific action in one sentence]
CLINICAL REASONING: [2-3 sentences]
```

**Key Guardrails:**
- Must start with "ATS CATEGORY:"
- ATS category must be numeric: 1, 2, 3, 4, or 5
- Clinical descriptor must match ATS category exactly
- Maximum 2-3 sentences for reasoning
- Exactly 2-3 key clinical features

**Clinical Logic:**
- Applies precautionary principle (triage higher if uncertain)
- Chest pain → assume cardiac → minimum ATS 2
- Any red flag → escalate immediately
- Special populations (paeds, pregnancy, elderly) → lower threshold

---

### 2. CONVERSATIONAL_TRIAGE_PROMPT

**File Location:** `utils/prompts.py:88-156`

**Purpose:** Interactive symptom gathering with final ATS assessment

**Input Variables:**
- `{chat_history}` - Previous conversation turns
- `{symptoms}` - Collected symptoms so far
- `{input}` - Current patient message

**Output Modes:**

**MODE A - Questioning:**
```
[Single focused question max 20 words]?
```
Examples:
- "When did the chest pain start?"
- "On a scale of 0-10, how severe is your pain?"

**MODE B - Assessment:**
```
TRIAGE ASSESSMENT:
ATS Category: [1-5]
Clinical Urgency: [Descriptor]
Recommended Action: [Specific action]
Reasoning: [Max 2 sentences]
```

**Decision Criteria:**
Provide assessment when collected:
- ✅ Chief complaint
- ✅ Onset/duration
- ✅ Severity (pain scale or intensity)
- ✅ Red flag screening
- ✅ Key associated symptoms

Or after 5-7 questions maximum.

**Key Guardrails:**
- Two-mode system: NEVER mix questioning and assessment
- Questions: no greetings, no explanations, just the question
- Assessment: no preamble, start with "TRIAGE ASSESSMENT:"
- Red flags trigger immediate ATS 1/2 with "Call 000" advice

**Symptom Collection Framework (OPQRST-style):**
- Onset - when did it start?
- Provocation/Palliation - what makes it better/worse?
- Quality - what does it feel like?
- Region/Radiation - where is it? does it move?
- Severity - pain scale 0-10
- Time/Duration - how long?

---

### 3. INTERACTIVE_TRIAGE_PROMPT

**File Location:** `utils/prompts.py:158-225`

**Purpose:** Structured questioning sequence for systematic triage

**Input Variables:**
- `{phase}` - Current interview phase
- `{questions_asked}` - Number of questions asked so far
- `{symptoms}` - Symptoms collected
- `{urgency_indicators}` - Detected urgency signals
- `{chat_history}` - Conversation history
- `{input}` - Current patient message

**Questioning Sequence:**

| Phase | Questions | Focus |
|-------|-----------|-------|
| Red Flag Screening | 1-2 | Life-threatening symptoms |
| Chief Complaint | 3 | Main problem |
| Severity Assessment | 4-5 | Pain scale, functional impact |
| Temporal Factors | 6 | Onset, duration |
| Associated Symptoms | 7-8 | Related symptoms |
| Medical History | 9-10 | Relevant history only |

**Output Modes:**

**MODE 1 - Question (if <5 questions):**
```
[Single question]?
```
- Maximum 20 words
- No greetings, no preamble
- No question numbering

**MODE 2 - Assessment (if ≥5 questions OR red flag):**
```
ATS Category: [1-5]
Clinical Urgency: [Descriptor]
Action Required: [Specific action]
Basis: [1-2 sentences]
```

**Key Guardrails:**
- Priority sequence enforced (red flags first)
- Response handling for unclear/contradictory answers
- Multiple concerns → prioritize most urgent
- "I don't know" → offer examples or move on
- Red flag at any time → immediate ATS 1/2 assessment

---

### 4. INTERVIEW_PROMPT

**File Location:** `utils/prompts.py:213-331`

**Purpose:** GP pre-visit clinical intake interview (15 questions)

**Input Variables:** None (standalone interview)

**Questioning Framework:**

| Questions | Focus Area |
|-----------|------------|
| 1 | Opening + Chief complaint |
| 2-6 | Symptom details (onset, duration, severity, character, triggers) |
| 7-9 | Associated symptoms + pertinent negatives |
| 10-13 | Relevant history (medications, allergies, conditions, social) |
| 14-15 | Functional impact + previous episodes |

**Output Requirements:**

**Opening Statement (Question 1):**
```
"Thank you for booking your GP appointment. I'll ask a few questions to help your doctor prepare. What brings you in today?"
```

**Questions 2-14:**
```
[Single question max 20 words]?
```
- No numbered questions (no "Question 1:")
- No greetings (except opening)
- No explanations

**Closing Statement (After Q15 or completion):**
```
"Thank you for answering my questions. I have everything needed to prepare your GP's report. End interview."
```
- EXACT phrase match required
- No additional text before or after

**Key Guardrails:**
- Maximum 15 questions total
- NEVER repeat questions
- ONE question at a time
- Australian English (GP not PCP, paediatric not pediatric)
- Sensitive topics protocol (non-judgmental language)

**Strict Prohibitions:**
- ❌ NEVER provide medical advice
- ❌ NEVER make diagnostic statements
- ❌ NEVER suggest treatments
- ❌ NEVER provide triage assessments
- ❌ NEVER ask same question twice
- ❌ NEVER enumerate questions ("1.", "Question 5:")

**Sensitive Topics Protocol:**
When asking about mental health, substance use, domestic violence:
- Use non-judgmental, respectful language
- Frame questions matter-of-factly
- Good: "How has your mood been lately?"
- Bad: "Are you depressed?"

---

### 5. REPORT_PROMPT

**File Location:** `utils/prompts.py:334-467`

**Purpose:** Generate RACGP-compliant clinical report from interview + EHR

**Input Variables:**
- Patient interview transcript
- Electronic Health Record (EHR) data

**Output Structure:**

```markdown
## Presenting Complaint
[One concise sentence - chief reason for visit]

## History of Presenting Complaint (HPC)
[Comprehensive chronological account including onset, duration,
character, severity, location, aggravating/relieving factors,
associated symptoms, progression, timing]

## Pertinent Negatives
• [Relevant symptoms patient denies, organized by system]
• [E.g., "Denies fever, haemoptysis, or shortness of breath"]

## Relevant Medical History
• Past medical conditions: [relevant only]
• Current medications: [name, dose, frequency if provided]
• Known drug allergies: [list or "None known"]
• Relevant surgical history: [if applicable]
• Relevant family history: [if applicable]
• Social history: Smoking [status], Alcohol [standard drinks/week]

## Functional Impact
[How symptoms affect daily activities, work, sleep, mobility]

## Patient Concerns or Questions
[Any specific worries or questions patient raised for GP to address]
```

**Documentation Standards:**

**1. Australian Medical Terminology:**
- ✅ paediatric (not pediatric)
- ✅ haemoptysis (not hemoptysis)
- ✅ oedema (not edema)
- ✅ anaesthetic (not anesthetic)
- ✅ haemorrhage (not hemorrhage)

**2. Australian Units:**
- ✅ Temperature in °C (not °F)
- ✅ Weight in kg (not lbs)
- ✅ Height in cm (not feet/inches)
- ✅ Alcohol in standard drinks/week

**3. Clinical Language Conversion:**

| Colloquial | Clinical |
|------------|----------|
| "Sore belly" | "Reports abdominal pain" |
| "Can't breathe properly" | "Describes dyspnoea" |
| "Dizzy spells" | "Episodes of vertigo/light-headedness" |
| "Feeling sick" | "Reports nausea" |

**4. History of Presenting Complaint Elements (OPQRST+):**
- **O**nset: when did symptoms begin? (specific date/time)
- **P**rovocation/Palliation: what makes it worse/better?
- **Q**uality: character of symptoms (sharp, dull, cramping, etc.)
- **R**egion/Radiation: anatomical location, does it move?
- **S**everity: quantify using scales (pain 0-10, mild/moderate/severe)
- **T**ime/Duration: how long present? constant vs intermittent?
- **Progression**: improving, worsening, static?
- **Associated symptoms**: concurrent symptoms

**5. Pertinent Negatives by System:**

| System | Examples |
|--------|----------|
| Respiratory | Denies fever, haemoptysis, chest pain |
| Cardiac | Denies palpitations, syncope, orthopnoea |
| Gastrointestinal | Denies nausea, vomiting, change in bowel habit |
| Neurological | Denies headache, vision changes, weakness |

**Key Guardrails:**

**Critical Output Requirements (10 Absolute Rules):**

1. ✅ BEGIN IMMEDIATELY with "## Presenting Complaint"
2. ❌ No "Here is the report" or similar meta-commentary
3. ❌ No explanatory text before or after report
4. ✅ ALL 6 sections MANDATORY (use "Not discussed" if empty)
5. ❌ No extra sections beyond the 6 mandatory ones
6. ✅ Do NOT number sections (use `##` not `## 1.`)
7. ✅ END immediately after "## Patient Concerns or Questions"
8. ✅ Use EXACTLY these section headings (character-for-character)
9. ✅ If section has no info: "Not discussed" or "None reported"
10. ✅ Output ONLY valid Markdown

**Prohibited Outputs:**
```
❌ "Based on the interview conducted..."
❌ "Here is the clinical report..."
❌ "This report summarizes..."
❌ "I hope this helps..."
❌ "Please let me know if..."
❌ Any text outside structured report sections
```

**Required Output Pattern:**
```
First character: #
First line: ## Presenting Complaint
Last line: Final sentence of ## Patient Concerns or Questions section
```

**Writing Style:**
- Third person ("Patient reports..." not "I have...")
- Professional, objective tone
- Factual only - NO interpretation, diagnosis, or assessment
- If contradictory info: document both
  - "Patient initially stated 2 days, later reported 1 week"
- Use "reports", "describes", "states" for patient-reported info

**Privacy & Compliance:**
- Australian Privacy Principles compliant
- Suitable for permanent medical record
- Clinically relevant information only
- Maintain patient confidentiality

---

## Output Format Enforcement

### Validation Strategies

**1. Regex Patterns for Validation**

```python
# Triage Assessment Validation
TRIAGE_PATTERN = r'^ATS CATEGORY: [1-5]\s*$'

# Report Start Validation
REPORT_START_PATTERN = r'^## Presenting Complaint\s*$'

# Section Header Validation
REQUIRED_SECTIONS = [
    "## Presenting Complaint",
    "## History of Presenting Complaint (HPC)",
    "## Pertinent Negatives",
    "## Relevant Medical History",
    "## Functional Impact",
    "## Patient Concerns or Questions"
]
```

**2. Field Presence Checks**

```python
def validate_triage_output(output: str) -> dict:
    """Validate triage assessment completeness"""
    required_fields = [
        "ATS CATEGORY:",
        "CLINICAL DESCRIPTOR:",
        "TO BE SEEN WITHIN:",
        "CARE PATHWAY:",
        "RED FLAGS IDENTIFIED:",
        "KEY CLINICAL FEATURES:",
        "RECOMMENDED IMMEDIATE ACTIONS:",
        "CLINICAL REASONING:"
    ]

    validation = {
        "valid": True,
        "missing_fields": [],
        "errors": []
    }

    for field in required_fields:
        if field not in output:
            validation["valid"] = False
            validation["missing_fields"].append(field)

    # Check ATS category is 1-5
    import re
    category_match = re.search(r'ATS CATEGORY:\s*([1-5])', output)
    if not category_match:
        validation["valid"] = False
        validation["errors"].append("Invalid ATS category (must be 1-5)")

    return validation
```

**3. Preamble/Postamble Detection**

```python
def has_preamble(output: str, expected_start: str) -> bool:
    """Check if output starts with expected text"""
    return not output.strip().startswith(expected_start)

def has_postamble(output: str, valid_end_keywords: list) -> bool:
    """Check if output has conversational ending"""
    last_line = output.strip().split('\n')[-1].lower()
    postamble_indicators = [
        "hope this helps",
        "let me know",
        "if you need",
        "please feel free",
        "is there anything"
    ]
    return any(indicator in last_line for indicator in postamble_indicators)
```

**4. Constrained Choice Validation**

```python
VALID_ATS_DESCRIPTORS = [
    "Immediately life-threatening",
    "Imminently life-threatening",
    "Potentially life-threatening",
    "Potentially serious",
    "Less urgent"
]

VALID_CARE_PATHWAYS = [
    "Call 000",
    "Emergency Department",
    "Urgent Care",
    "GP Appointment",
    "Telehealth"
]

def validate_constrained_fields(output: str) -> bool:
    """Ensure only valid options are used"""
    # Extract clinical descriptor
    descriptor_match = re.search(
        r'CLINICAL DESCRIPTOR:\s*(.+?)(?:\n|$)',
        output
    )
    if descriptor_match:
        descriptor = descriptor_match.group(1).strip()
        if descriptor not in VALID_ATS_DESCRIPTORS:
            return False

    # Extract care pathway
    pathway_match = re.search(
        r'CARE PATHWAY:\s*(.+?)(?:\n|$)',
        output
    )
    if pathway_match:
        pathway = pathway_match.group(1).strip()
        if pathway not in VALID_CARE_PATHWAYS:
            return False

    return True
```

### Post-Processing Steps

**1. Output Cleaning**
```python
def clean_output(raw_output: str, expected_format: str) -> str:
    """Remove common LLM artifacts"""
    cleaned = raw_output.strip()

    # Remove markdown code blocks if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r'^```(?:markdown)?\n', '', cleaned)
        cleaned = re.sub(r'\n```$', '', cleaned)

    # Remove common preambles
    preamble_patterns = [
        r'^(?:Here is|Based on|I have prepared|I\'ve created|The following is).+?\n\n',
        r'^TRIAGE ASSESSMENT:\s*\n+(?=TRIAGE ASSESSMENT:)',  # Duplicate headers
    ]
    for pattern in preamble_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    return cleaned
```

**2. Retry Logic with Clarification**
```python
def get_validated_output(
    prompt: str,
    input_data: dict,
    max_retries: int = 2
) -> str:
    """Retry with clarification if output invalid"""

    for attempt in range(max_retries):
        output = llm.generate(prompt.format(**input_data))
        validation = validate_output(output, expected_format)

        if validation["valid"]:
            return output

        # Retry with additional constraints
        if attempt < max_retries - 1:
            clarification = f"""
            Your previous output did not follow the required format.
            Issues: {', '.join(validation['errors'])}

            Please output again, starting IMMEDIATELY with the first required field.
            Do NOT add any introductory text.
            """
            input_data["clarification"] = clarification
            prompt = prompt + "\n" + clarification

    raise ValueError(f"Failed to get valid output after {max_retries} attempts")
```

---

## Clinical Safety Measures

### Red Flag Detection

All prompts include consistent red flag screening:

**Life-Threatening Symptoms (Automatic ATS 1):**
- Cardiac or respiratory arrest
- Unconscious or responds only to pain
- Severe respiratory distress with cyanosis
- Uncontrollable major haemorrhage
- Airway obstruction

**Immediately Life-Threatening (Automatic ATS 2):**
- Chest pain with cardiac features
- Severe breathing difficulty or stridor
- Signs of stroke (FAST: Face/Arm/Speech/Time)
- Severe bleeding (controlled but ongoing)
- Anaphylaxis symptoms
- High-risk pregnancy complications

**Action Required:**
- Immediate triage to ATS 1 or 2
- Explicit recommendation: "Call 000 immediately"
- No further questioning - assess immediately

### Safety Principles

**1. Precautionary Principle**
```
"Always apply the precautionary principle - if uncertain, triage higher"
```
- When in doubt between ATS 2 and 3 → choose ATS 2
- Ambiguous chest pain → assume cardiac → minimum ATS 2

**2. Special Population Adjustments**

| Population | Adjustment |
|------------|------------|
| Paediatric | Lower threshold for fever, dehydration, respiratory |
| Pregnancy | Lower threshold for abdominal pain, bleeding, headache |
| Elderly | Lower threshold for falls, confusion, infection |
| Immunocompromised | Lower threshold for fever, infection signs |

**3. Escalation Pathways**

```python
ATS_ESCALATION = {
    1: "Call 000 immediately - do not delay",
    2: "Go to Emergency Department immediately or call 000",
    3: "Attend Emergency Department or Urgent Care within 30 minutes",
    4: "See GP within same day or next available appointment",
    5: "Routine GP appointment within 1-2 days acceptable"
}
```

**4. Scope Limitations**

All prompts explicitly prohibit:
- ❌ Medical diagnosis
- ❌ Treatment recommendations
- ❌ Medication advice
- ❌ Reassurance without triage
- ❌ Dismissing patient concerns

Role limited to:
- ✅ Information gathering
- ✅ Urgency assessment (triage only)
- ✅ Clinical documentation
- ✅ Appropriate referral pathway

### Quality Assurance Checks

**Pre-Deployment Validation:**
1. Test with known ATS 1-5 scenarios
2. Verify all red flags trigger correct response
3. Check constrained choices are respected
4. Validate Australian terminology usage
5. Confirm no medical advice generated

**Runtime Monitoring:**
```python
def safety_check(output: str, category: int) -> dict:
    """Check for safety violations in output"""
    violations = []

    # Check for medical advice
    advice_keywords = [
        "you should take",
        "i recommend taking",
        "try this medication",
        "you probably have",
        "it's likely",
        "diagnosis"
    ]
    output_lower = output.lower()
    for keyword in advice_keywords:
        if keyword in output_lower:
            violations.append(f"Medical advice detected: {keyword}")

    # Check ATS 1 has 000 recommendation
    if category == 1 and "call 000" not in output_lower:
        violations.append("ATS 1 missing 'Call 000' instruction")

    # Check chest pain has minimum ATS 2
    if "chest pain" in output_lower and category > 2:
        violations.append("Chest pain must be minimum ATS 2")

    return {
        "safe": len(violations) == 0,
        "violations": violations
    }
```

---

## Best Practices

### Prompt Maintenance

**1. Version Control**
- Track all prompt changes in git
- Document rationale for changes
- Test prompts before deployment
- Maintain changelog

**2. Regular Review Cycle**
- Quarterly review of prompt effectiveness
- Analyze edge cases and failures
- Update based on clinical feedback
- Align with latest ATS/RACGP updates

**3. Testing Protocol**

```python
# Test cases for each prompt
TEST_CASES = {
    "triage": [
        {
            "scenario": "Chest pain with cardiac features",
            "expected_category": 2,
            "expected_action": "Emergency Department",
            "must_include": ["Call 000", "cardiac"]
        },
        {
            "scenario": "Minor cut requiring cleaning",
            "expected_category": 5,
            "expected_action": "GP Appointment",
            "must_not_include": ["emergency", "urgent"]
        }
    ]
}
```

### Performance Optimization

**1. Token Efficiency**
- Guardrails reduce verbose outputs
- Constrained choices prevent rambling
- Clear examples reduce trial-and-error

**2. Response Time**
- Shorter prompts = faster inference
- Single-mode enforcement reduces backtracking
- Structured outputs parse faster

**3. Cost Control**
- Less verbose outputs = fewer tokens
- Validation prevents wasted regenerations
- Caching common instructions

### Integration Guidelines

**1. Python Integration**

```python
from utils.prompts import (
    TRIAGE_PROMPT,
    CONVERSATIONAL_TRIAGE_PROMPT,
    INTERVIEW_PROMPT,
    REPORT_PROMPT
)

# Triage assessment
def assess_triage(report_text: str) -> dict:
    prompt = TRIAGE_PROMPT.format(report=report_text)
    response = llm.generate(prompt)
    validation = validate_triage_output(response)

    if not validation["valid"]:
        raise ValueError(f"Invalid output: {validation['errors']}")

    return parse_triage_response(response)

# Interview
def conduct_interview() -> list:
    questions_asked = 0
    conversation = []

    # Opening
    opening = "Thank you for booking your GP appointment..."
    conversation.append({"role": "assistant", "content": opening})

    while questions_asked < 15:
        patient_input = get_patient_input()
        conversation.append({"role": "user", "content": patient_input})

        # Generate next question
        response = llm.generate(
            INTERVIEW_PROMPT,
            context=conversation
        )

        # Check for end
        if "End interview." in response:
            break

        conversation.append({"role": "assistant", "content": response})
        questions_asked += 1

    return conversation
```

**2. Error Handling**

```python
class OutputValidationError(Exception):
    """Raised when LLM output doesn't match required format"""
    pass

class SafetyViolationError(Exception):
    """Raised when output contains medical advice or safety issues"""
    pass

def safe_generate(prompt: str, **kwargs) -> str:
    """Generate with validation and safety checks"""
    try:
        output = llm.generate(prompt, **kwargs)

        # Validate format
        if not validate_format(output):
            raise OutputValidationError("Format validation failed")

        # Check safety
        safety = safety_check(output)
        if not safety["safe"]:
            raise SafetyViolationError(
                f"Safety violations: {safety['violations']}"
            )

        return output

    except Exception as e:
        log_error(e)
        return fallback_response()
```

### Localization Considerations

**Current:** Australian English, ATS, RACGP standards

**To Adapt for Other Regions:**

1. **United Kingdom:**
   - Change: 000 → 999
   - Change: GP terminology (mostly compatible)
   - Change: Use NHS triage categories instead of ATS
   - Keep: British spelling (already using "paediatric", "haemoptysis")

2. **United States:**
   - Change: 000 → 911
   - Change: GP → Primary Care Physician (PCP)
   - Change: ATS → ESI (Emergency Severity Index, 5 levels)
   - Change: British spelling → American (pediatric, hemoptysis, edema)
   - Change: Standard drinks → drinks per week
   - Change: °C → °F, kg → lbs

3. **Canada:**
   - Change: 000 → 911
   - Keep: CTAS (Canadian Triage and Acuity Scale, 5 levels - similar to ATS)
   - Keep: British spelling (used in Canadian medical practice)
   - Keep: Metric units

---

## Troubleshooting

### Common Issues & Solutions

#### Issue 1: LLM Adds Preamble Despite Guardrails

**Symptoms:**
```
"Based on the pre-visit report, here is my assessment:

ATS CATEGORY: 2
..."
```

**Solutions:**
1. Add more explicit start instruction:
   ```
   "Your output must be ONLY the assessment.
   The very first characters of your response must be: 'ATS CATEGORY:'
   Do not write ANYTHING before that."
   ```

2. Post-process to strip preamble:
   ```python
   def strip_preamble(output: str, expected_start: str) -> str:
       lines = output.split('\n')
       for i, line in enumerate(lines):
           if line.strip().startswith(expected_start):
               return '\n'.join(lines[i:])
       return output  # Return original if pattern not found
   ```

3. Use few-shot examples showing correct format

#### Issue 2: Inconsistent ATS Category Assignment

**Symptoms:**
- Same symptoms get different categories
- Categories don't match severity

**Solutions:**
1. Add explicit decision tree:
   ```
   IF red flag present → ATS 1 or 2
   ELSE IF severe pain (8-10) → ATS 2 or 3
   ELSE IF moderate pain (5-7) → ATS 3 or 4
   ...
   ```

2. Provide more examples in prompt:
   ```
   Example 1: Chest pain + SOB = ATS 2
   Example 2: Ankle sprain = ATS 4
   Example 3: Medication refill = ATS 5
   ```

3. Use temperature=0 for deterministic outputs

#### Issue 3: Report Missing Sections

**Symptoms:**
```markdown
## Presenting Complaint
Headache

## History of Presenting Complaint (HPC)
Patient reports...

## Relevant Medical History
(skips Pertinent Negatives section)
```

**Solutions:**
1. Strengthen mandatory field language:
   ```
   "ALL 6 sections are REQUIRED. Even if you have no information
   for a section, you MUST include the heading and write 'Not discussed'."
   ```

2. Use numbered checklist:
   ```
   You MUST include these 6 sections in order:
   [1] ## Presenting Complaint
   [2] ## History of Presenting Complaint (HPC)
   [3] ## Pertinent Negatives
   [4] ## Relevant Medical History
   [5] ## Functional Impact
   [6] ## Patient Concerns or Questions
   ```

3. Validate and request regeneration if missing

#### Issue 4: Questions Repeat or Exceed Limit

**Symptoms:**
- Interview asks 20+ questions
- Same question asked twice

**Solutions:**
1. Add question counter to prompt:
   ```python
   prompt = INTERVIEW_PROMPT.format(
       questions_asked=len(conversation) // 2,
       max_questions=15
   )
   ```

2. Explicitly list asked questions:
   ```
   Questions already asked:
   1. What brings you in today?
   2. When did symptoms start?
   ...

   NEVER repeat these questions.
   ```

3. Hard-enforce in code:
   ```python
   if questions_asked >= 15:
       return CLOSING_STATEMENT
   ```

#### Issue 5: Non-Clinical Language in Reports

**Symptoms:**
```
"Patient has a really bad tummy ache that started yesterday"
(should be: "Patient reports severe abdominal pain with onset 24 hours ago")
```

**Solutions:**
1. Provide more conversion examples:
   ```
   REQUIRED CONVERSIONS:
   "bad tummy ache" → "abdominal pain"
   "can't catch my breath" → "dyspnoea"
   "feel dizzy" → "reports vertigo/light-headedness"
   "really bad" → "severe"
   ```

2. Add instruction:
   ```
   "Translate ALL colloquial language to professional medical terminology.
   Use formal medical language throughout."
   ```

3. Post-process with terminology checker

#### Issue 6: LLM Provides Medical Advice

**Symptoms:**
```
"You should take paracetamol for the pain and see a doctor if it worsens"
```

**Solutions:**
1. Reinforce prohibition at multiple points:
   ```
   At start: "Do NOT provide medical advice"
   In middle: "Your role is triage only - NOT diagnosis or treatment"
   At end: "NEVER suggest medications or treatments"
   ```

2. Implement safety filter:
   ```python
   PROHIBITED_PHRASES = [
       "you should take",
       "i recommend",
       "try taking",
       "diagnosis is",
       "you have",
       "it's probably"
   ]

   if any(phrase in output.lower() for phrase in PROHIBITED_PHRASES):
       raise SafetyViolationError()
   ```

3. Use system-level instruction (if supported by LLM):
   ```
   SYSTEM: You are an information gathering assistant ONLY.
   You cannot diagnose or prescribe.
   ```

---

## Appendix

### A. Complete Validation Suite

```python
"""
Complete validation suite for Medical Triage AI outputs
File: utils/validators.py
"""

import re
from typing import Dict, List, Tuple

# Valid options for constrained fields
VALID_ATS_CATEGORIES = [1, 2, 3, 4, 5]
VALID_ATS_DESCRIPTORS = [
    "Immediately life-threatening",
    "Imminently life-threatening",
    "Potentially life-threatening",
    "Potentially serious",
    "Less urgent"
]
VALID_TIMEFRAMES = [
    "Immediate",
    "10 minutes",
    "30 minutes",
    "60 minutes",
    "120 minutes"
]
VALID_CARE_PATHWAYS = [
    "Call 000",
    "Emergency Department",
    "Urgent Care",
    "GP Appointment",
    "Telehealth"
]

# Required sections for clinical report
REQUIRED_REPORT_SECTIONS = [
    "## Presenting Complaint",
    "## History of Presenting Complaint (HPC)",
    "## Pertinent Negatives",
    "## Relevant Medical History",
    "## Functional Impact",
    "## Patient Concerns or Questions"
]


def validate_triage_output(output: str) -> Dict[str, any]:
    """
    Validate triage assessment output against all guardrails

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str],
            "parsed_data": dict
        }
    """
    errors = []
    warnings = []
    parsed_data = {}

    # 1. Check starts correctly (no preamble)
    if not output.strip().startswith("ATS CATEGORY:"):
        errors.append("Output does not start with 'ATS CATEGORY:'")

    # 2. Extract and validate ATS category
    category_match = re.search(r'ATS CATEGORY:\s*([1-5])', output)
    if category_match:
        parsed_data["category"] = int(category_match.group(1))
    else:
        errors.append("Invalid or missing ATS category (must be 1-5)")

    # 3. Check all required fields present
    required_fields = [
        "ATS CATEGORY:",
        "CLINICAL DESCRIPTOR:",
        "TO BE SEEN WITHIN:",
        "CARE PATHWAY:",
        "RED FLAGS IDENTIFIED:",
        "KEY CLINICAL FEATURES:",
        "SPECIAL CONSIDERATIONS:",
        "RECOMMENDED IMMEDIATE ACTIONS:",
        "CLINICAL REASONING:"
    ]

    for field in required_fields:
        if field not in output:
            errors.append(f"Missing required field: {field}")

    # 4. Validate clinical descriptor
    descriptor_match = re.search(
        r'CLINICAL DESCRIPTOR:\s*(.+?)(?:\n|$)',
        output
    )
    if descriptor_match:
        descriptor = descriptor_match.group(1).strip()
        if descriptor not in VALID_ATS_DESCRIPTORS:
            errors.append(
                f"Invalid clinical descriptor: '{descriptor}'. "
                f"Must be one of: {', '.join(VALID_ATS_DESCRIPTORS)}"
            )
        parsed_data["descriptor"] = descriptor

    # 5. Validate care pathway
    pathway_match = re.search(r'CARE PATHWAY:\s*(.+?)(?:\n|$)', output)
    if pathway_match:
        pathway = pathway_match.group(1).strip()
        if pathway not in VALID_CARE_PATHWAYS:
            errors.append(
                f"Invalid care pathway: '{pathway}'. "
                f"Must be one of: {', '.join(VALID_CARE_PATHWAYS)}"
            )
        parsed_data["pathway"] = pathway

    # 6. Check for prohibited preamble/postamble phrases
    prohibited_starts = [
        "here is",
        "based on",
        "i have",
        "i've",
        "the following",
        "this is"
    ]
    first_line = output.strip().split('\n')[0].lower()
    for phrase in prohibited_starts:
        if phrase in first_line and not first_line.startswith("ats category"):
            warnings.append(f"Possible preamble detected: '{phrase}'")

    prohibited_ends = [
        "i hope",
        "please let me know",
        "is there anything",
        "feel free"
    ]
    last_line = output.strip().split('\n')[-1].lower()
    for phrase in prohibited_ends:
        if phrase in last_line:
            warnings.append(f"Possible postamble detected: '{phrase}'")

    # 7. Safety check: ATS 1 should mention 000
    if parsed_data.get("category") == 1:
        if "000" not in output and "call emergency" not in output.lower():
            warnings.append("ATS 1 should include 'Call 000' instruction")

    # 8. Check clinical reasoning length
    reasoning_match = re.search(
        r'CLINICAL REASONING:\s*(.+?)(?:\n[A-Z]|\Z)',
        output,
        re.DOTALL
    )
    if reasoning_match:
        reasoning = reasoning_match.group(1).strip()
        sentence_count = len(re.findall(r'[.!?]+', reasoning))
        if sentence_count > 3:
            warnings.append(
                f"Clinical reasoning has {sentence_count} sentences "
                f"(recommended max: 3)"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "parsed_data": parsed_data
    }


def validate_clinical_report(output: str) -> Dict[str, any]:
    """
    Validate clinical report output against RACGP standards

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }
    """
    errors = []
    warnings = []

    # 1. Check starts with first section (no preamble)
    if not output.strip().startswith("## Presenting Complaint"):
        errors.append(
            "Report does not start with '## Presenting Complaint'"
        )

    # 2. Check all required sections present
    for section in REQUIRED_REPORT_SECTIONS:
        if section not in output:
            errors.append(f"Missing required section: {section}")

    # 3. Check sections are in correct order
    section_positions = []
    for section in REQUIRED_REPORT_SECTIONS:
        pos = output.find(section)
        if pos != -1:
            section_positions.append((section, pos))

    section_positions.sort(key=lambda x: x[1])
    expected_order = [s for s, _ in section_positions]

    if expected_order != REQUIRED_REPORT_SECTIONS:
        errors.append(
            f"Sections not in correct order. "
            f"Expected: {REQUIRED_REPORT_SECTIONS}, "
            f"Got: {expected_order}"
        )

    # 4. Check for numbered sections (prohibited)
    if re.search(r'##\s+\d+\.', output):
        errors.append("Sections should not be numbered")

    # 5. Check for American spellings (should be Australian)
    american_terms = {
        "pediatric": "paediatric",
        "hemoptysis": "haemoptysis",
        "edema": "oedema",
        "anesthetic": "anaesthetic",
        "hemorrhage": "haemorrhage",
        "fetus": "foetus"
    }

    for american, australian in american_terms.items():
        if re.search(r'\b' + american + r'\b', output, re.IGNORECASE):
            warnings.append(
                f"American spelling detected: '{american}' "
                f"(should be '{australian}')"
            )

    # 6. Check for first person (should be third person)
    first_person_patterns = [
        r'\bI have\b',
        r'\bI am\b',
        r'\bmy\b',
        r'\bI feel\b'
    ]

    for pattern in first_person_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            warnings.append(
                f"First person language detected (should be third person)"
            )
            break

    # 7. Check for prohibited preamble
    prohibited_starts = [
        "here is the report",
        "based on the interview",
        "this report summarizes",
        "i have prepared"
    ]

    first_50_chars = output[:50].lower()
    for phrase in prohibited_starts:
        if phrase in first_50_chars:
            errors.append(f"Prohibited preamble detected: '{phrase}'")

    # 8. Check for prohibited postamble
    prohibited_ends = [
        "i hope this helps",
        "please let me know",
        "if you need anything"
    ]

    last_100_chars = output[-100:].lower()
    for phrase in prohibited_ends:
        if phrase in last_100_chars:
            errors.append(f"Prohibited postamble detected: '{phrase}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_question_output(
    output: str,
    max_words: int = 20
) -> Dict[str, any]:
    """
    Validate question output (for interview/interactive triage)

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str],
            "word_count": int
        }
    """
    errors = []
    warnings = []

    # Count words
    word_count = len(output.split())

    # 1. Check word limit
    if word_count > max_words:
        errors.append(
            f"Question exceeds {max_words} words (has {word_count})"
        )

    # 2. Check ends with question mark
    if not output.strip().endswith('?'):
        warnings.append("Question should end with '?'")

    # 3. Check for numbered question format (prohibited)
    if re.match(r'^\d+\.|\bQuestion \d+:', output):
        errors.append("Questions should not be numbered")

    # 4. Check for multiple questions
    question_marks = output.count('?')
    if question_marks > 1:
        errors.append(
            f"Only ONE question allowed per output (found {question_marks})"
        )

    # 5. Check for explanatory preamble
    explanatory_starts = [
        "I'd like to ask",
        "Let me ask",
        "I need to know",
        "Can you tell me"
    ]

    for phrase in explanatory_starts:
        if output.lower().startswith(phrase.lower()):
            warnings.append(
                f"Avoid explanatory preamble: '{phrase}'. "
                f"Ask question directly."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "word_count": word_count
    }


# Example usage
if __name__ == "__main__":
    # Test triage validation
    triage_output = """ATS CATEGORY: 2
CLINICAL DESCRIPTOR: Imminently life-threatening
TO BE SEEN WITHIN: 10 minutes
CARE PATHWAY: Emergency Department
RED FLAGS IDENTIFIED: Yes - chest pain with cardiac features
KEY CLINICAL FEATURES:
• Central chest pain radiating to left arm
• Associated dyspnoea
• Pain severity 8/10
SPECIAL CONSIDERATIONS: Patient aged 65, history of hypertension
RECOMMENDED IMMEDIATE ACTIONS: Call 000 immediately, do not drive to hospital
CLINICAL REASONING: Chest pain with radiation and cardiac risk factors warrants immediate emergency assessment to rule out acute coronary syndrome."""

    result = validate_triage_output(triage_output)
    print("Triage Validation:", result)
```

### B. Testing Examples

```python
"""
Test cases for prompt validation
File: tests/test_prompts.py
"""

import pytest
from utils.validators import (
    validate_triage_output,
    validate_clinical_report,
    validate_question_output
)

# Triage test cases
TRIAGE_TEST_CASES = [
    {
        "name": "Valid ATS 2 cardiac",
        "output": """ATS CATEGORY: 2
CLINICAL DESCRIPTOR: Imminently life-threatening
TO BE SEEN WITHIN: 10 minutes
CARE PATHWAY: Emergency Department
RED FLAGS IDENTIFIED: Yes - chest pain
KEY CLINICAL FEATURES:
• Chest pain
• Dyspnoea
SPECIAL CONSIDERATIONS: None
RECOMMENDED IMMEDIATE ACTIONS: Call 000
CLINICAL REASONING: Chest pain requires immediate assessment.""",
        "expected_valid": True
    },
    {
        "name": "Invalid - has preamble",
        "output": """Here is my assessment:

ATS CATEGORY: 3
...""",
        "expected_valid": False
    },
    {
        "name": "Invalid - missing field",
        "output": """ATS CATEGORY: 4
CLINICAL DESCRIPTOR: Potentially serious
TO BE SEEN WITHIN: 60 minutes
(missing other fields)""",
        "expected_valid": False
    }
]

# Report test cases
REPORT_TEST_CASES = [
    {
        "name": "Valid complete report",
        "output": """## Presenting Complaint
Headache

## History of Presenting Complaint (HPC)
Patient reports bifrontal headache...

## Pertinent Negatives
• Denies fever
• Denies visual changes

## Relevant Medical History
• Past medical conditions: Migraine
• Current medications: None
• Known drug allergies: None known

## Functional Impact
Mild impact on concentration at work

## Patient Concerns or Questions
Concerned about frequency of headaches""",
        "expected_valid": True
    },
    {
        "name": "Invalid - missing section",
        "output": """## Presenting Complaint
Cough

## History of Presenting Complaint (HPC)
Dry cough for 3 days

## Relevant Medical History
None significant""",
        "expected_valid": False
    }
]

@pytest.mark.parametrize("test_case", TRIAGE_TEST_CASES)
def test_triage_validation(test_case):
    result = validate_triage_output(test_case["output"])
    assert result["valid"] == test_case["expected_valid"]

@pytest.mark.parametrize("test_case", REPORT_TEST_CASES)
def test_report_validation(test_case):
    result = validate_clinical_report(test_case["output"])
    assert result["valid"] == test_case["expected_valid"]
```

### C. Prompt Version History

| Version | Date | Changes | Rationale |
|---------|------|---------|-----------|
| 1.0 | Oct 2024 | Initial prompts with basic ATS alignment | Establish baseline |
| 1.1 | Oct 2024 | Added Australian standards (ATS, RACGP) | Compliance with local standards |
| 1.2 | Oct 2024 | Implemented comprehensive guardrails | Improve output consistency |
| 1.3 | Oct 2024 | Added constrained choice enforcement | Reduce parsing errors |
| 1.4 | Oct 2024 | Strengthened safety prohibitions | Prevent medical advice |

### D. Glossary

**ATS**: Australasian Triage Scale - 5-category system for emergency department triage

**RACGP**: Royal Australian College of General Practitioners - professional body setting GP standards

**HPC**: History of Presenting Complaint - detailed chronological account of patient's symptoms

**Pertinent Negatives**: Symptoms patient specifically denies that are relevant to differential diagnosis

**Red Flags**: Critical symptoms indicating immediately/imminently life-threatening conditions

**Guardrails**: Prompt engineering techniques to constrain and validate LLM outputs

**Constrained Choices**: Limiting LLM to select from predefined options rather than free-form generation

**Preamble**: Introductory text before required output (prohibited in our system)

**Postamble**: Concluding text after required output (prohibited in our system)

**FAST**: Face-Arm-Speech-Time - stroke assessment protocol

**OPQRST**: Onset-Provocation-Quality-Region-Severity-Time - symptom assessment framework

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | October 2024 | Development Team | Initial comprehensive documentation |

---

**For questions or updates to this documentation, contact the development team.**

**Last reviewed:** October 2024
**Next review due:** January 2025
