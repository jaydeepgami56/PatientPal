# Medical Triage AI - Quick Reference Guide

## Guardrail Cheat Sheet

### ✅ DO's

| Aspect | Correct Approach |
|--------|------------------|
| **Starting output** | Begin IMMEDIATELY with first required field |
| **Field selection** | Select ONLY from provided options |
| **Missing info** | Use "None", "Not discussed", or "N/A" |
| **Questions** | ONE question only, max 20 words |
| **Sections** | ALL mandatory sections required |
| **Terminology** | Australian spelling (paediatric, haemoptysis) |
| **Units** | Metric (°C, kg, cm) |
| **Emergency** | "Call 000" (Australian emergency number) |
| **Person** | Third person ("Patient reports...") |
| **Tone** | Professional, objective, factual |

### ❌ DON'Ts

| Violation | Examples to Avoid |
|-----------|------------------|
| **Preamble** | ❌ "Here is...", "Based on...", "I will..." |
| **Postamble** | ❌ "I hope this helps...", "Let me know..." |
| **Mixed modes** | ❌ Asking question AND providing assessment |
| **Medical advice** | ❌ "You should take...", "Try this medication..." |
| **Diagnosis** | ❌ "You have...", "It's probably..." |
| **Free-form choices** | ❌ Making up new ATS descriptors |
| **Skipping sections** | ❌ Omitting mandatory report sections |
| **Repeating** | ❌ Asking same question twice |
| **Numbering** | ❌ "Question 1:", "## 1. Presenting..." |
| **First person** | ❌ "I have...", "My symptoms..." |

---

## ATS Quick Reference

| ATS | Descriptor | Time | Action | Examples |
|-----|-----------|------|--------|----------|
| **1** | Immediately life-threatening | Immediate | Call 000 NOW | Cardiac arrest, unconscious, severe haemorrhage |
| **2** | Imminently life-threatening | 10 min | Emergency Dept / 000 | Chest pain (cardiac), stroke, severe pain (8-10) |
| **3** | Potentially life-threatening | 30 min | ED / Urgent Care | Moderate pain (5-7), persistent vomiting |
| **4** | Potentially serious | 60 min | GP same day | Minor fractures, moderate pain (3-4) |
| **5** | Less urgent | 120 min | GP routine | Minor wounds, chronic issues, prescriptions |

---

## Output Format Quick Templates

### Triage Assessment
```
ATS CATEGORY: [1-5]
CLINICAL DESCRIPTOR: [Select one: Immediately/Imminently/Potentially life-threatening/Potentially serious/Less urgent]
TO BE SEEN WITHIN: [Immediate/10 minutes/30 minutes/60 minutes/120 minutes]
CARE PATHWAY: [Call 000/Emergency Department/Urgent Care/GP Appointment/Telehealth]
RED FLAGS IDENTIFIED: [Yes/No - if yes, list]
KEY CLINICAL FEATURES: [2-3 bullet points]
SPECIAL CONSIDERATIONS: [Age/pregnancy/comorbidities or "None"]
RECOMMENDED IMMEDIATE ACTIONS: [One sentence]
CLINICAL REASONING: [2-3 sentences maximum]
```

### Clinical Report
```markdown
## Presenting Complaint
[One sentence]

## History of Presenting Complaint (HPC)
[Full chronological account with OPQRST elements]

## Pertinent Negatives
• [Symptom denied]
• [Symptom denied]

## Relevant Medical History
• Past medical conditions: [list]
• Current medications: [list]
• Known drug allergies: [list]
• Social history: [smoking, alcohol]

## Functional Impact
[How symptoms affect daily life]

## Patient Concerns or Questions
[Patient's specific concerns]
```

### Question Format
```
[Single question max 20 words]?
```

**Examples:**
- ✅ "When did your symptoms begin?"
- ✅ "On a scale of 0-10, how severe is your pain?"
- ❌ "I'd like to ask you about when this started - could you tell me?"

---

## Validation Checklist

### Before Deployment
- [ ] Test with ATS 1-5 scenarios
- [ ] Verify red flags trigger correct response
- [ ] Check Australian terminology used
- [ ] Confirm no medical advice generated
- [ ] Validate all sections present
- [ ] Test constrained choices respected

### Runtime Checks
- [ ] Output starts correctly (no preamble)
- [ ] All required fields present
- [ ] Values within constrained choices
- [ ] No prohibited phrases detected
- [ ] Correct terminology and units
- [ ] Safety rules followed

---

## Red Flags (Always ATS 1 or 2)

### ATS 1 Triggers
- ⚠️ Cardiac arrest
- ⚠️ Respiratory arrest
- ⚠️ Unconscious
- ⚠️ Severe respiratory distress + cyanosis
- ⚠️ Uncontrollable major haemorrhage

### ATS 2 Triggers
- ⚠️ Chest pain with cardiac features
- ⚠️ Severe breathing difficulty
- ⚠️ Stroke symptoms (FAST)
- ⚠️ Severe pain (8-10/10)
- ⚠️ Anaphylaxis

**Action Required:** Immediate assessment + "Call 000"

---

## Australian Terminology

| Use ✅ | Not ❌ |
|--------|--------|
| Paediatric | Pediatric |
| Haemoptysis | Hemoptysis |
| Oedema | Edema |
| Anaesthetic | Anesthetic |
| Haemorrhage | Hemorrhage |
| GP | PCP / Primary Care Physician |
| 000 | 911 |
| °C | °F |
| kg | lbs |
| Standard drinks/week | Drinks per week |

---

## Common Validation Errors & Fixes

| Error | Fix |
|-------|-----|
| "Output has preamble" | Start immediately with first required field name |
| "Invalid ATS category" | Use only numbers 1, 2, 3, 4, or 5 |
| "Missing required section" | Include ALL 6 sections even if "Not discussed" |
| "Section out of order" | Follow exact order from template |
| "Question too long" | Maximum 20 words |
| "Multiple questions" | ONE question per output in question mode |
| "Medical advice detected" | Triage only - no treatment recommendations |
| "American spelling" | Use Australian spelling throughout |

---

## Safety Principles

1. **Precautionary Principle**: When uncertain, triage higher
2. **Special Populations**: Lower threshold for paeds, pregnancy, elderly, immunocompromised
3. **Chest Pain Rule**: Always assume cardiac → minimum ATS 2
4. **Scope Limitation**: Triage and documentation ONLY - no diagnosis or treatment
5. **Emergency Protocol**: Red flag → immediate ATS 1/2 + "Call 000"

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| **Prompts** | `utils/prompts.py` | All prompt definitions |
| **Full Documentation** | `docs/PROMPT_STRATEGY.md` | Complete strategy guide |
| **Quick Reference** | `docs/QUICK_REFERENCE.md` | This file |
| **Validators** | `utils/validators.py` | Output validation functions |

---

## Need Help?

1. **Check full documentation**: `docs/PROMPT_STRATEGY.md`
2. **Review prompt file**: `utils/prompts.py`
3. **Run validation tests**: Test outputs against validators
4. **Check examples**: See Appendix B in PROMPT_STRATEGY.md

---

**Version:** 1.0 | **Last Updated:** October 2024
