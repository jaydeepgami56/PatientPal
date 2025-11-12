# Lead Agent System - Test Cases

**Version:** 1.0
**Date:** 2025-11-11
**Status:** Ready for Testing

---

## 📋 Test Case Overview

This document provides comprehensive test cases for validating the Lead Agent multi-agent orchestration system.

---

## 🧪 Test Categories

1. [Basic Functionality Tests](#1-basic-functionality-tests)
2. [Routing Logic Tests](#2-routing-logic-tests)
3. [Multi-Agent Tests](#3-multi-agent-tests)
4. [Emergency Detection Tests](#4-emergency-detection-tests)
5. [Image Upload Tests](#5-image-upload-tests)
6. [Error Handling Tests](#6-error-handling-tests)
7. [Performance Tests](#7-performance-tests)
8. [Memory & Context Tests](#8-memory--context-tests)

---

## 1. Basic Functionality Tests

### TC-001: Simple Medical Query (MedGemma)

**Objective:** Verify basic query routing to MedGemma agent

**Steps:**
1. Navigate to Lead Agent page
2. Enter query: "What are the symptoms of Type 2 diabetes?"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Routing Decision shows: Primary Agent = "MedGemma"
- ✅ Execution Mode = "single"
- ✅ Urgency = "routine"
- ✅ Response contains diabetes symptoms (polyuria, polydipsia, weight loss, etc.)
- ✅ Processing time < 5 seconds
- ✅ Confidence > 70%

**Test Data:**
```
Query: "What are the symptoms of Type 2 diabetes?"
Expected Agent: MedGemma
Expected Mode: single
```

---

### TC-002: Treatment Query (TxGemma)

**Objective:** Verify routing to TxGemma for treatment questions

**Steps:**
1. Navigate to Lead Agent page
2. Enter query: "What are the treatment options for high blood pressure?"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Routing Decision shows: Primary Agent = "TxGemma"
- ✅ Response contains treatment options (lifestyle, medications)
- ✅ Mentions first-line antihypertensives (ACE inhibitors, diuretics, etc.)
- ✅ Confidence > 70%

**Test Data:**
```
Query: "What are the treatment options for high blood pressure?"
Expected Agent: TxGemma
Expected Mode: single
```

---

### TC-003: Pathology Query

**Objective:** Verify routing to Pathology agent

**Steps:**
1. Navigate to Lead Agent page
2. Enter query: "Explain what a biopsy showing 'adenocarcinoma, moderately differentiated' means"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Primary Agent = "Pathology"
- ✅ Response explains adenocarcinoma terminology
- ✅ Discusses differentiation grading
- ✅ Recommends oncology consultation

**Test Data:**
```
Query: "Explain what a biopsy showing 'adenocarcinoma, moderately differentiated' means"
Expected Agent: Pathology
Expected Mode: single
```

---

## 2. Routing Logic Tests

### TC-101: Routing Confidence - High Confidence

**Objective:** Verify high confidence routing for clear queries

**Test Cases:**

| Query | Expected Agent | Expected Confidence |
|-------|---------------|---------------------|
| "What causes pneumonia?" | MedGemma | >80% |
| "Side effects of metformin" | TxGemma | >80% |
| "How to interpret a pathology report" | Pathology | >80% |

**Steps:**
1. Enter each query
2. Check routing decision confidence

**Expected Result:**
- ✅ Confidence > 80% for all clear, unambiguous queries

---

### TC-102: Routing Confidence - Ambiguous Query

**Objective:** Verify system handles ambiguous queries

**Steps:**
1. Enter query: "I don't feel well"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Routes to MedGemma (default general agent)
- ✅ Confidence may be medium (50-80%)
- ✅ Response asks for more specific symptoms

**Test Data:**
```
Query: "I don't feel well"
Expected Agent: MedGemma (default)
Expected Confidence: Medium (50-80%)
```

---

### TC-103: Image Detection Without Image

**Objective:** Verify system detects when image is needed but not provided

**Steps:**
1. Enter query: "Analyze this skin rash"
2. Do NOT upload image
3. Click "Analyze Query"

**Expected Result:**
- ✅ Routing detects: REQUIRES_IMAGE = Yes
- ✅ Response informs user to upload image
- ✅ OR routes to MedGemma with note about image requirement

**Test Data:**
```
Query: "Analyze this skin rash"
Image Uploaded: No
Expected Behavior: Request image OR inform user
```

---

## 3. Multi-Agent Tests

### TC-201: Parallel Multi-Agent Execution

**Objective:** Verify parallel execution for multi-domain queries

**Steps:**
1. Enter query: "I have chest pain and a rash on my arms. What should I do?"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Routing shows: Primary Agent + Additional Agents
- ✅ Execution Mode = "parallel"
- ✅ Multiple agents consulted (e.g., MedGemma for chest pain)
- ✅ Synthesis combines both concerns
- ✅ Processing time < 6 seconds (faster than sequential)

**Test Data:**
```
Query: "I have chest pain and a rash on my arms. What should I do?"
Expected Mode: parallel
Expected Agents: MedGemma + possibly others
```

---

### TC-202: Sequential Pipeline Execution

**Objective:** Verify sequential execution for dependent tasks

**Steps:**
1. Upload a chest X-ray image (or test image)
2. Enter query: "Analyze this chest X-ray and recommend treatment"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Execution Mode = "sequential"
- ✅ Step 1: CXR Foundation analyzes image
- ✅ Step 2: TxGemma uses CXR findings for treatment recommendations
- ✅ Synthesized response includes both findings and treatment
- ✅ Processing time < 10 seconds

**Test Data:**
```
Query: "Analyze this chest X-ray and recommend treatment"
Image: chest_xray_test.jpg
Expected Mode: sequential
Expected Agents: CXR Foundation → TxGemma
```

---

### TC-203: Multi-Agent Synthesis Quality

**Objective:** Verify synthesis creates coherent unified response

**Steps:**
1. Execute multi-agent query (TC-201 or TC-202)
2. Review synthesized output

**Expected Result:**
- ✅ Response is coherent and unified (not just concatenated)
- ✅ Clearly attributes information to source agents
- ✅ Resolves contradictions or flags disagreements
- ✅ Uses consistent Australian medical terminology
- ✅ Includes consultation summary at bottom

---

## 4. Emergency Detection Tests

### TC-301: Emergency - Chest Pain

**Objective:** Verify emergency detection for cardiac symptoms

**Steps:**
1. Enter query: "Severe chest pain, crushing sensation, difficulty breathing, sweating"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Urgency Level = "emergency"
- ✅ Safety flags detected: ["chest pain", "difficulty breathing"]
- ✅ Response bypasses normal routing (no agent execution)
- ✅ Response shows: "🚨 EMERGENCY DETECTED"
- ✅ Clear instruction: "Call 000 NOW"
- ✅ Processing time < 1 second
- ✅ No agent consultation (emergency bypass)

**Test Data:**
```
Query: "Severe chest pain, crushing sensation, difficulty breathing, sweating"
Expected Urgency: emergency
Expected Response: Call 000 immediately
Expected Time: <1 second
```

---

### TC-302: Emergency - Stroke Symptoms

**Objective:** Verify stroke detection

**Steps:**
1. Enter query: "Sudden facial droop, can't move left arm, speech is slurred"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Emergency detected
- ✅ Safety flags: may include stroke-related keywords
- ✅ Response: Call 000 immediately
- ✅ Mentions FAST (Face, Arm, Speech, Time)

**Test Data:**
```
Query: "Sudden facial droop, can't move left arm, speech is slurred"
Expected: Emergency guidance with stroke recognition
```

---

### TC-303: Emergency - Severe Bleeding

**Objective:** Verify severe bleeding detection

**Steps:**
1. Enter query: "Severe bleeding that won't stop, feeling dizzy and weak"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Emergency detected
- ✅ Safety flags: ["severe bleeding"]
- ✅ Response includes: Call 000, apply pressure, don't drive

**Test Data:**
```
Query: "Severe bleeding that won't stop, feeling dizzy and weak"
Expected: Emergency response
```

---

### TC-304: Non-Emergency - Similar Keywords

**Objective:** Verify system doesn't over-detect emergencies

**Steps:**
1. Enter query: "I've had a headache for 2 weeks, mild chest tightness when stressed"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Urgency = "routine" or "urgent" (not emergency)
- ✅ Routes to MedGemma for assessment
- ✅ May recommend GP appointment
- ✅ Does NOT trigger emergency bypass

**Test Data:**
```
Query: "I've had a headache for 2 weeks, mild chest tightness when stressed"
Expected Urgency: routine or urgent (NOT emergency)
Expected: Normal routing, not emergency bypass
```

---

## 5. Image Upload Tests

### TC-401: Dermatology Image Analysis

**Objective:** Verify Derm Foundation agent with image

**Prerequisites:**
- Prepare test image: skin lesion, mole, or rash photo

**Steps:**
1. Navigate to Lead Agent page
2. Upload dermatology test image
3. Enter query: "Analyze this skin lesion. Is it concerning?"
4. Click "Analyze Query"

**Expected Result:**
- ✅ Routing shows: Primary Agent = "Derm Foundation"
- ✅ REQUIRES_IMAGE = Yes
- ✅ Response includes top findings with confidence scores
- ✅ Mentions ABCDE criteria if applicable
- ✅ Recommends dermatology referral if suspicious features
- ✅ Processing time < 5 seconds

**Test Data:**
```
Query: "Analyze this skin lesion. Is it concerning?"
Image: skin_lesion_test.jpg
Expected Agent: Derm Foundation
Expected: Classification results with confidence
```

---

### TC-402: Chest X-Ray Analysis

**Objective:** Verify CXR Foundation agent with X-ray image

**Prerequisites:**
- Prepare test image: chest X-ray (can use sample from online medical databases)

**Steps:**
1. Upload chest X-ray image
2. Enter query: "What does this chest X-ray show?"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Primary Agent = "CXR Foundation"
- ✅ Response includes radiological findings
- ✅ Mentions lung fields, heart size, etc.
- ✅ Provides differential diagnoses if abnormalities detected

**Test Data:**
```
Query: "What does this chest X-ray show?"
Image: chest_xray_test.jpg
Expected Agent: CXR Foundation
Expected: Radiological interpretation
```

---

### TC-403: Wrong Image Type

**Objective:** Verify system handles mismatched image/query

**Steps:**
1. Upload a skin lesion image
2. Enter query: "Analyze this chest X-ray"
3. Click "Analyze Query"

**Expected Result:**
- ✅ System attempts CXR analysis
- ✅ May produce low confidence results
- ✅ OR system may detect mismatch and warn user

**Test Data:**
```
Query: "Analyze this chest X-ray"
Image: skin_lesion.jpg (wrong type)
Expected: Low confidence or mismatch warning
```

---

### TC-404: Image + Treatment Pipeline

**Objective:** Verify sequential pipeline with image analysis → treatment

**Steps:**
1. Upload chest X-ray showing pneumonia (or test image)
2. Enter query: "What does this show and what treatment is needed?"
3. Click "Analyze Query"

**Expected Result:**
- ✅ Execution Mode = "sequential"
- ✅ Agent 1: CXR Foundation analyzes image
- ✅ Agent 2: TxGemma receives findings and recommends treatment
- ✅ Synthesized response includes: findings + treatment plan

**Test Data:**
```
Query: "What does this show and what treatment is needed?"
Image: chest_xray_pneumonia.jpg
Expected Mode: sequential
Expected Agents: CXR Foundation → TxGemma
```

---

## 6. Error Handling Tests

### TC-501: Missing API Key

**Objective:** Verify graceful handling of missing OpenAI API key

**Steps:**
1. Remove or rename `.env` file
2. Restart application
3. Navigate to Lead Agent page

**Expected Result:**
- ✅ Error message: "OPENAI_API_KEY not found"
- ✅ Application doesn't crash
- ✅ Clear instruction to add API key

---

### TC-502: Invalid API Key

**Objective:** Verify handling of invalid API key

**Steps:**
1. Set OPENAI_API_KEY to invalid value in `.env`
2. Restart application
3. Try to execute a query

**Expected Result:**
- ✅ Error message about authentication failure
- ✅ Suggests checking API key validity
- ✅ No system crash

---

### TC-503: Agent Initialization Failure

**Objective:** Verify handling when specialist agent fails to initialize

**Prerequisites:**
- Remove or set invalid HUGGINGFACE_API_KEY

**Steps:**
1. Enter query that routes to HuggingFace agent (e.g., MedGemma)
2. Click "Analyze Query"

**Expected Result:**
- ✅ Error message: "Failed to initialize agent"
- ✅ Suggests checking HuggingFace API key
- ✅ Error logged in orchestration memory
- ✅ Graceful degradation (doesn't crash entire system)

---

### TC-504: Network Timeout

**Objective:** Verify handling of network issues

**Steps:**
1. Disconnect network OR use very slow connection
2. Execute query

**Expected Result:**
- ✅ Appropriate timeout error
- ✅ User-friendly error message
- ✅ No system crash

---

### TC-505: Very Long Query

**Objective:** Verify handling of excessive input

**Steps:**
1. Enter extremely long query (>5000 characters)
2. Click "Analyze Query"

**Expected Result:**
- ✅ Validation error OR truncation warning
- ✅ System handles gracefully
- ✅ OR processes successfully with potential summarization

---

## 7. Performance Tests

### TC-601: Single Agent Response Time

**Objective:** Measure response time for single agent queries

**Test Cases:**

| Query | Expected Agent | Target Time |
|-------|---------------|-------------|
| "What is diabetes?" | MedGemma | <3s |
| "Treatment for hypertension" | TxGemma | <3s |
| "Explain biopsy results" | Pathology | <3s |

**Steps:**
1. Execute each query
2. Record processing time from response metadata

**Expected Result:**
- ✅ All single-agent queries < 3 seconds (after initial agent warmup)

---

### TC-602: Parallel Multi-Agent Performance

**Objective:** Verify parallel execution is faster than sequential

**Steps:**
1. Execute multi-domain query requiring 2 agents
2. Record processing time

**Expected Result:**
- ✅ Time ≈ max(agent1_time, agent2_time), not sum
- ✅ Processing time < 5 seconds
- ✅ Faster than executing agents sequentially

**Test Data:**
```
Query: "What causes pneumonia and what treatment options exist?"
Expected: Parallel execution of diagnosis + treatment
Expected Time: <5s (not 6s if each agent takes 3s)
```

---

### TC-603: Agent Warmup Time

**Objective:** Measure first-time initialization vs subsequent queries

**Steps:**
1. Restart application (cold start)
2. Execute query to MedGemma (first time)
3. Record time
4. Execute another query to MedGemma (warmed up)
5. Record time

**Expected Result:**
- ✅ First query: May take longer (initialization time)
- ✅ Subsequent queries: Faster (<3s)

---

### TC-604: Memory Usage Over Time

**Objective:** Verify memory doesn't grow excessively

**Steps:**
1. Execute 20 different queries
2. Check memory statistics in sidebar
3. Verify memory size

**Expected Result:**
- ✅ Conversation history grows but manageable
- ✅ No memory leaks
- ✅ Clear history function works

---

## 8. Memory & Context Tests

### TC-701: Conversation Context Retention

**Objective:** Verify system remembers conversation context

**Steps:**
1. Query 1: "What is Type 2 diabetes?"
2. Query 2: "What are the treatment options for it?"
3. Query 3: "What diet would you recommend?"

**Expected Result:**
- ✅ Query 2: System understands "it" = Type 2 diabetes
- ✅ Query 3: System understands context is diabetes management
- ✅ Responses are contextually relevant

**Test Data:**
```
Query 1: "What is Type 2 diabetes?"
Query 2: "What are the treatment options for it?"
Query 3: "What diet would you recommend?"

Expected: Each query builds on previous context
```

---

### TC-702: Agent Consultation Memory

**Objective:** Verify agent consultations are logged

**Steps:**
1. Execute query routing to MedGemma
2. Execute query routing to TxGemma
3. Check statistics in sidebar

**Expected Result:**
- ✅ "Total Queries" increments correctly
- ✅ Both agents show in consultation history (if viewing memory)
- ✅ Timestamps recorded

---

### TC-703: Clear History Function

**Objective:** Verify clear history works correctly

**Steps:**
1. Execute 3-5 queries
2. Verify query history shows them
3. Click "Clear History" button
4. Check history section

**Expected Result:**
- ✅ Query history is empty
- ✅ Conversation memory cleared
- ✅ Statistics reset to 0
- ✅ Page reloads successfully

---

### TC-704: Session Persistence

**Objective:** Verify memory persists within session

**Steps:**
1. Execute several queries
2. Navigate to different page
3. Return to Lead Agent page

**Expected Result:**
- ✅ Query history still visible
- ✅ Statistics maintained
- ✅ Memory not lost on page navigation

---

## 9. UI/UX Tests

### TC-801: Routing Details Visibility

**Objective:** Verify routing details toggle works

**Steps:**
1. Execute a query with "Show Routing Details" checked
2. Verify routing decision displayed
3. Uncheck "Show Routing Details"
4. Execute another query

**Expected Result:**
- ✅ With toggle ON: Routing decision visible
- ✅ With toggle OFF: Routing decision hidden
- ✅ Response always visible regardless of toggle

---

### TC-802: Query History Display

**Objective:** Verify query history shows correctly

**Steps:**
1. Execute 6 queries
2. Scroll to "Query History" section

**Expected Result:**
- ✅ Shows last 5 queries (most recent first)
- ✅ Each item shows: query text, agents consulted, timestamp
- ✅ Expandable items show full details

---

### TC-803: Image Upload Preview

**Objective:** Verify uploaded image displays

**Steps:**
1. Upload an image
2. Check if preview appears

**Expected Result:**
- ✅ Image preview displays below upload button
- ✅ Caption shows "Uploaded Image"
- ✅ Image is visible and properly sized

---

## 10. Edge Cases

### TC-901: Empty Query

**Objective:** Verify handling of empty input

**Steps:**
1. Leave query field empty
2. Click "Analyze Query"

**Expected Result:**
- ✅ Warning message: "Please enter a medical query"
- ✅ No processing occurs
- ✅ No error crash

---

### TC-902: Special Characters in Query

**Objective:** Verify handling of special characters

**Steps:**
1. Enter query with special characters: "What's the treatment for O'Brien's disease?"
2. Click "Analyze Query"

**Expected Result:**
- ✅ Query processed successfully
- ✅ No parsing errors
- ✅ Response generated

---

### TC-903: Non-English Query

**Objective:** Verify handling of non-English input

**Steps:**
1. Enter query in another language (e.g., Spanish: "¿Cuáles son los síntomas de diabetes?")
2. Click "Analyze Query"

**Expected Result:**
- ✅ System processes query
- ✅ May respond in English (LLM default)
- ✅ OR attempts translation
- ✅ No crash

---

### TC-904: Medical Jargon vs Layman Terms

**Objective:** Verify system handles both technical and simple language

**Test Cases:**

| Query Type | Example Query |
|------------|---------------|
| Layman | "I have a really bad headache" |
| Medical | "I'm experiencing severe cephalgia with photophobia" |

**Steps:**
1. Execute both queries
2. Compare responses

**Expected Result:**
- ✅ Both queries processed successfully
- ✅ Responses appropriate to query complexity
- ✅ Medical terms explained in layman response

---

## 📊 Test Summary Template

Use this template to track test execution:

```
Test Date: ___________
Tester: ___________
Environment: Development / Staging / Production

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| TC-001 | Simple Medical Query | ☐ Pass ☐ Fail | |
| TC-002 | Treatment Query | ☐ Pass ☐ Fail | |
| TC-003 | Pathology Query | ☐ Pass ☐ Fail | |
| ... | ... | ... | |

Overall Pass Rate: ____ / ____ (_____%)

Critical Issues Found:
1.
2.

Recommendations:
1.
2.
```

---

## 🔧 Test Environment Setup

### Prerequisites:

1. **API Keys Configured:**
   - ✅ OPENAI_API_KEY in `.env`
   - ✅ HUGGINGFACE_API_KEY in `.env`

2. **Test Data Prepared:**
   - Sample skin lesion image
   - Sample chest X-ray image
   - List of test queries

3. **Application Running:**
   ```bash
   streamlit run app.py
   ```

4. **Browser:** Chrome, Firefox, or Edge (latest version)

---

## 📈 Success Criteria

**System passes testing if:**
- ✅ 95%+ of basic functionality tests pass
- ✅ All emergency detection tests pass (100%)
- ✅ 90%+ of routing logic tests pass
- ✅ All error handling tests handled gracefully (no crashes)
- ✅ Performance targets met (single agent <3s, multi-agent <5s)
- ✅ No critical security issues
- ✅ UI responsive and user-friendly

---

## 🐛 Bug Reporting Template

```markdown
## Bug Report

**Test Case ID:** TC-XXX
**Severity:** Critical / High / Medium / Low
**Date Found:** YYYY-MM-DD

**Description:**
[Brief description of the issue]

**Steps to Reproduce:**
1.
2.
3.

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Screenshots/Logs:**
[Attach if available]

**Environment:**
- OS:
- Browser:
- Python Version:
```

---

## ✅ Quick Test Checklist

**5-Minute Smoke Test:**
- [ ] Application starts without errors
- [ ] Lead Agent page loads
- [ ] Simple query works (e.g., "What is diabetes?")
- [ ] Routing decision displays
- [ ] Response generated successfully
- [ ] No console errors

**15-Minute Regression Test:**
- [ ] All 3 basic functionality tests (TC-001 to TC-003)
- [ ] One multi-agent test (TC-201)
- [ ] One emergency test (TC-301)
- [ ] One image upload test (TC-401)
- [ ] One error handling test (TC-501)

**Full Test Suite:**
- [ ] All test cases in this document
- [ ] Expected duration: 2-3 hours

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** Ready for Use ✅
