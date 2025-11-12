# Medical Triage AI - Logging & Debugging Guide

**Version:** 1.0
**Last Updated:** October 2024

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Logging System Architecture](#logging-system-architecture)
4. [Log Files](#log-files)
5. [Using Loggers](#using-loggers)
6. [Debugging Step-by-Step](#debugging-step-by-step)
7. [Log Levels](#log-levels)
8. [Advanced Features](#advanced-features)
9. [Log Analysis](#log-analysis)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Medical Triage AI logging system provides comprehensive debugging capabilities to track every step of the application, from LLM interactions to validation and error handling.

### Key Features

✅ **Multi-level logging** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
✅ **Specialized log files** (LLM, validation, errors, performance)
✅ **Colored console output** for easy reading
✅ **Automatic timing** for all operations
✅ **Step-by-step debugging** with DebugLogger
✅ **JSON structured logging** for LLM interactions
✅ **Rotating log files** (10MB max, 5 backups)
✅ **Decorators** for automatic function logging
✅ **Context managers** for operation tracking

---

## Quick Start

### Basic Usage

```python
from utils.logger import app_logger

# Simple logging
app_logger.info("Application started")
app_logger.debug("Debug information")
app_logger.warning("Something to watch")
app_logger.error("An error occurred")
```

### Step-by-Step Debugging

```python
from utils.logger import debug_prompt_flow

# Create debug logger
debug = debug_prompt_flow("Triage Assessment")

# Log steps
debug.step("Validating input")
debug.variable("report_length", len(report))
debug.checkpoint("Input validated", {"status": "ok"})
```

### Using Decorators

```python
from utils.logger import log_function_call, log_prompt_execution

@log_function_call()
def my_function(arg1, arg2):
    """Function with automatic logging"""
    return arg1 + arg2

@log_prompt_execution("TRIAGE_PROMPT")
def execute_triage(report: str):
    """Prompt execution with automatic timing and logging"""
    # Your code here
    return result
```

---

## Logging System Architecture

```
┌──────────────────────────────────────────────┐
│         LOGGING SYSTEM                       │
└──────────────────────────────────────────────┘
                     │
      ┌──────────────┴──────────────┐
      │                             │
┌─────▼─────┐                ┌──────▼──────┐
│  CONSOLE  │                │  LOG FILES  │
│  OUTPUT   │                │  (Rotating) │
│ (Colored) │                └──────┬──────┘
└───────────┘                       │
                    ┌───────────────┼───────────────┐
                    │               │               │
           ┌────────▼───┐  ┌────────▼───┐  ┌───────▼────┐
           │ MAIN LOG   │  │  LLM LOG   │  │ ERROR LOG  │
           │ (Detailed) │  │   (JSON)   │  │ (Errors)   │
           └────────────┘  └────────────┘  └────────────┘
                    │               │
           ┌────────▼───┐  ┌────────▼───────┐
           │VALIDATION  │  │ PERFORMANCE    │
           │    LOG     │  │      LOG       │
           └────────────┘  └────────────────┘
```

---

## Log Files

All logs are stored in the `logs/` directory:

| File | Purpose | Format | Content |
|------|---------|--------|---------|
| **triage_app.log** | Main application log | Detailed | All application events, function calls, operations |
| **llm_interactions.log** | LLM calls | JSON | Full prompts, responses, tokens, timing |
| **validation.log** | Validation results | Standard | Input validation, output validation, pass/fail |
| **errors.log** | Errors only | Detailed | Exceptions, stack traces, error context |
| **performance.log** | Performance metrics | Standard | Operation timing, token counts, durations |

### Log Rotation

- **Max file size:** 10 MB
- **Backup count:** 5 files
- **Naming:** `logfile.log`, `logfile.log.1`, `logfile.log.2`, etc.
- **Automatic:** Old logs rotated automatically

---

## Using Loggers

### Available Loggers

```python
from utils.logger import (
    app_logger,           # Main application logger
    llm_logger,           # LLM interaction logger
    validation_logger,    # Validation logger
    error_logger,         # Error logger
    perf_logger          # Performance logger
)
```

### 1. Main Application Logger

```python
from utils.logger import app_logger

# General application logging
app_logger.info("Starting triage assessment")
app_logger.debug(f"Report length: {len(report)}")
app_logger.warning("No EHR data available")
app_logger.error("Failed to parse response")
```

### 2. LLM Interaction Logger

```python
from utils.logger import log_llm_interaction

log_llm_interaction(
    prompt_name="TRIAGE_PROMPT",
    prompt_text=full_prompt,
    response=llm_response,
    model="claude-3-sonnet",
    tokens_used=150,
    duration=1.2,
    metadata={"patient_id": "P12345"}
)
```

**Logged data:**
- Full prompt text
- Full response text
- Model name
- Token count
- Duration
- Previews (first 200 chars)
- Custom metadata

### 3. Validation Logger

```python
from utils.logger import log_validation

log_validation(
    validation_type="triage_output",
    input_data=llm_output,
    result={
        "valid": True,
        "errors": [],
        "warnings": ["Minor formatting issue"]
    },
    passed=True
)
```

### 4. Error Logger

```python
from utils.logger import log_error

try:
    risky_operation()
except Exception as e:
    log_error(
        error=e,
        context="Triage assessment",
        additional_info={
            "report_length": len(report),
            "attempt": 2
        }
    )
```

### 5. Performance Logger

```python
from utils.logger import log_performance

import time
start = time.time()
# ... operation ...
duration = time.time() - start

log_performance(
    operation="triage_assessment",
    duration=duration,
    metadata={
        "tokens_used": 150,
        "model": "claude-3"
    }
)
```

---

## Debugging Step-by-Step

### Using DebugLogger

The `DebugLogger` provides step-by-step tracking with automatic numbering:

```python
from utils.logger import debug_prompt_flow

# Create debug logger
debug = debug_prompt_flow("Triage Assessment")

# Log steps (automatically numbered)
debug.step("Starting triage assessment")
# → [STEP 1] Triage Assessment: Starting triage assessment

debug.step("Validating input report")
# → [STEP 2] Triage Assessment: Validating input report

# Log variables
debug.variable("report_length", len(report))
# → [VAR] Triage Assessment.report_length = 245

debug.variable("prompt_text", prompt[:100])
# → [VAR] Triage Assessment.prompt_text = You are a Medical...

# Log checkpoints with data
debug.checkpoint("Input validated", {
    "report_length": 245,
    "status": "valid"
})
# → [CHECKPOINT] Triage Assessment.Input validated
#   + JSON data: {"report_length": 245, "status": "valid"}
```

### Complete Example

```python
from utils.logger import debug_prompt_flow

def execute_triage(report: str):
    debug = debug_prompt_flow("Triage Assessment")

    # Step 1
    debug.step("Validating input")
    if not report:
        debug.variable("validation_error", "Empty report")
        raise ValueError("Empty report")
    debug.variable("report_length", len(report))

    # Step 2
    debug.step("Formatting prompt")
    prompt = TRIAGE_PROMPT.format(report=report)
    debug.variable("prompt_length", len(prompt))
    debug.checkpoint("Prompt formatted", {"length": len(prompt)})

    # Step 3
    debug.step("Calling LLM")
    response = llm_client.generate(prompt)
    debug.variable("response_length", len(response))

    # Step 4
    debug.step("Parsing response")
    parsed = parse_response(response)
    debug.variable("ats_category", parsed.get("category"))

    # Final checkpoint
    debug.checkpoint("Assessment complete", {
        "category": parsed.get("category"),
        "valid": True
    })

    return parsed
```

**Output in logs:**
```
[STEP 1] Triage Assessment: Validating input
[VAR] Triage Assessment.report_length = 245
[STEP 2] Triage Assessment: Formatting prompt
[VAR] Triage Assessment.prompt_length = 1523
[CHECKPOINT] Triage Assessment.Prompt formatted
[STEP 3] Triage Assessment: Calling LLM
[VAR] Triage Assessment.response_length = 389
[STEP 4] Triage Assessment: Parsing response
[VAR] Triage Assessment.ats_category = 3
[CHECKPOINT] Triage Assessment.Assessment complete
```

---

## Log Levels

### Understanding Log Levels

| Level | Usage | Example | Appears In |
|-------|-------|---------|------------|
| **DEBUG** | Detailed debugging info | Variable values, step tracking | File only |
| **INFO** | General information | Operation start/complete | Console + File |
| **WARNING** | Warnings, non-critical issues | Validation warnings | Console + File |
| **ERROR** | Errors, exceptions | Failed operations | Console + File + errors.log |
| **CRITICAL** | Critical failures | System failures | Console + File + errors.log |

### Setting Log Levels

**In code:**
```python
from utils.logger import initialize_logging

# Verbose mode (DEBUG to console)
initialize_logging(verbose=True)

# Normal mode (INFO to console)
initialize_logging(verbose=False)
```

**Change after initialization:**
```python
import logging
from utils.logger import app_logger

# Set to DEBUG
app_logger.setLevel(logging.DEBUG)

# Set console handler to DEBUG
for handler in app_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.DEBUG)
```

---

## Advanced Features

### 1. Context Managers

Automatic operation tracking with timing:

```python
from utils.logger import LogContext, app_logger

with LogContext(app_logger, "Processing patient data", patient_id="P12345"):
    # Your code here
    process_patient()
```

**Output:**
```
INFO | Starting: Processing patient data
INFO | Completed: Processing patient data (duration: 1.23s)
```

If error occurs:
```
ERROR | Failed: Processing patient data (duration: 0.45s)
[Full stack trace]
```

### 2. Function Decorators

Automatic function entry/exit logging:

```python
from utils.logger import log_function_call

@log_function_call()
def calculate_ats_category(pain_level: int, symptoms: list) -> int:
    # Function code
    return category
```

**Output:**
```
DEBUG | → Entering: calculate_ats_category
DEBUG | ← Exiting: calculate_ats_category (duration: 0.002s)
```

### 3. Prompt Execution Decorator

Specialized for prompt execution:

```python
from utils.logger import log_prompt_execution

@log_prompt_execution("TRIAGE_PROMPT")
def execute_triage_assessment(report: str):
    # Execution code
    return result
```

**Output:**
```
INFO | Executing prompt: TRIAGE_PROMPT
INFO | Prompt execution completed: TRIAGE_PROMPT (duration: 1.45s)
```

Plus performance logging and error handling.

### 4. Colored Console Output

Console output is automatically colored:

- 🔵 **DEBUG** - Cyan
- 🟢 **INFO** - Green
- 🟡 **WARNING** - Yellow
- 🔴 **ERROR** - Red
- 🟣 **CRITICAL** - Magenta

---

## Log Analysis

### View Recent Logs

```python
from utils.logger import (
    get_recent_logs,
    get_error_summary,
    get_llm_summary,
    LoggerConfig
)

# Get last 100 lines from main log
recent = get_recent_logs(LoggerConfig.MAIN_LOG, lines=100)
print(recent)

# Get error summary
errors = get_error_summary()
print(errors)

# Get LLM interaction summary
llm_summary = get_llm_summary(interactions=10)
print(llm_summary)
```

### Parse JSON Logs

LLM interaction logs are in JSON format:

```python
import json

with open("logs/llm_interactions.log", "r") as f:
    for line in f:
        try:
            log_entry = json.loads(line)
            print(f"Prompt: {log_entry['extra']['prompt_name']}")
            print(f"Duration: {log_entry['extra']['duration_seconds']}s")
            print(f"Tokens: {log_entry['extra'].get('tokens_used', 'N/A')}")
        except:
            continue
```

### Search Logs

**Using grep (Linux/Mac):**
```bash
# Find all errors
grep "ERROR" logs/triage_app.log

# Find specific prompt executions
grep "TRIAGE_PROMPT" logs/llm_interactions.log

# Find validation failures
grep "FAILED" logs/validation.log
```

**Using Python:**
```python
def search_logs(log_file: str, search_term: str):
    """Search for term in log file"""
    with open(log_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if search_term.lower() in line.lower():
                print(f"Line {line_num}: {line.strip()}")

search_logs("logs/triage_app.log", "validation")
```

---

## Troubleshooting

### Issue 1: No Logs Appearing

**Problem:** Nothing appears in log files

**Solutions:**
```python
# 1. Check logging is initialized
from utils.logger import initialize_logging
initialize_logging(verbose=True)

# 2. Check log directory exists
from utils.logger import LoggerConfig
print(f"Log directory: {LoggerConfig.LOG_DIR}")
print(f"Exists: {LoggerConfig.LOG_DIR.exists()}")

# 3. Test logger directly
from utils.logger import app_logger
app_logger.info("Test log message")
```

### Issue 2: Too Much Debug Output

**Problem:** Console flooded with DEBUG messages

**Solution:**
```python
import logging
from utils.logger import app_logger

# Reduce console verbosity
for handler in app_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.WARNING)  # Only warnings and above
```

### Issue 3: Log Files Growing Too Large

**Problem:** Log files exceed disk space

**Solutions:**
```python
# 1. Reduce max file size
from utils.logger import LoggerConfig
LoggerConfig.MAX_BYTES = 5 * 1024 * 1024  # 5MB instead of 10MB

# 2. Reduce backup count
LoggerConfig.BACKUP_COUNT = 2  # Keep only 2 backups

# 3. Clean old logs
import shutil
shutil.rmtree("logs/")
LoggerConfig.LOG_DIR.mkdir()
```

### Issue 4: Can't Find Specific Log Entry

**Problem:** Need to find when specific operation occurred

**Solution:**
```python
# Use timestamps and grep
# Log entries have timestamps: 2024-10-16 14:30:25,123

# Search by time range
def find_logs_in_timerange(log_file: str, start_time: str, end_time: str):
    """Find logs between start and end time"""
    with open(log_file, 'r') as f:
        for line in f:
            if start_time <= line[:19] <= end_time:
                print(line.strip())

find_logs_in_timerange(
    "logs/triage_app.log",
    "2024-10-16 14:00",
    "2024-10-16 15:00"
)
```

### Issue 5: JSON Parse Errors in LLM Log

**Problem:** Can't parse LLM log JSON

**Solution:**
```python
import json

def safe_parse_llm_log(log_file: str):
    """Safely parse LLM log with error handling"""
    with open(log_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                log_entry = json.loads(line)
                yield log_entry
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: JSON parse error - {e}")
                continue

# Use it
for entry in safe_parse_llm_log("logs/llm_interactions.log"):
    print(entry.get('message'))
```

---

## Complete Examples

### Example 1: Full Triage Assessment with Logging

```python
from utils.logger import (
    debug_prompt_flow,
    log_llm_interaction,
    log_validation,
    log_error,
    LogContext,
    app_logger
)
from utils.prompts import TRIAGE_PROMPT
import time

def execute_triage_with_full_logging(report: str, llm_client):
    """Execute triage assessment with comprehensive logging"""

    debug = debug_prompt_flow("Triage Assessment")

    with LogContext(app_logger, "Triage Assessment", report_length=len(report)):
        try:
            # Step 1: Validate input
            debug.step("Validating input report")
            debug.variable("report_length", len(report))

            if len(report) < 10:
                raise ValueError("Report too short")

            debug.checkpoint("Input validated")

            # Step 2: Format prompt
            debug.step("Formatting prompt")
            prompt_text = TRIAGE_PROMPT.format(report=report)
            debug.variable("prompt_length", len(prompt_text))

            # Step 3: Call LLM
            debug.step("Executing LLM call")
            start_time = time.time()

            response = llm_client.generate(
                prompt=prompt_text,
                model="claude-3-sonnet"
            )

            duration = time.time() - start_time
            debug.variable("response_length", len(response))
            debug.checkpoint("LLM response received", {"duration": duration})

            # Step 4: Log LLM interaction
            debug.step("Logging LLM interaction")
            log_llm_interaction(
                prompt_name="TRIAGE_PROMPT",
                prompt_text=prompt_text,
                response=response,
                model="claude-3-sonnet",
                duration=duration
            )

            # Step 5: Validate output
            debug.step("Validating output")
            validation_result = validate_triage_output(response)

            log_validation(
                validation_type="triage_output",
                input_data=response,
                result=validation_result,
                passed=validation_result["valid"]
            )

            if not validation_result["valid"]:
                app_logger.warning(f"Validation issues: {validation_result['errors']}")

            debug.checkpoint("Assessment complete", {
                "valid": validation_result["valid"],
                "category": parse_category(response)
            })

            return response

        except Exception as e:
            log_error(e, "Triage assessment execution", {
                "report_length": len(report)
            })
            raise
```

### Example 2: Interview Loop with Logging

```python
from utils.logger import debug_prompt_flow, log_llm_interaction

def conduct_interview_with_logging(llm_client):
    """Conduct 15-question interview with full logging"""

    debug = debug_prompt_flow("Interview Process")
    conversation = []

    debug.step("Starting interview")
    debug.checkpoint("Interview initialized", {"max_questions": 15})

    for question_num in range(15):
        debug.step(f"Generating question {question_num + 1}")

        # Format conversation
        chat_history = format_history(conversation)

        # Get question
        question = llm_client.generate(
            prompt=INTERVIEW_PROMPT + f"\n\n{chat_history}",
            model="claude-3"
        )

        log_llm_interaction(
            prompt_name="INTERVIEW_PROMPT",
            prompt_text=INTERVIEW_PROMPT,
            response=question,
            model="claude-3",
            metadata={"question_number": question_num + 1}
        )

        conversation.append({"role": "assistant", "content": question})

        # Check for end
        if "End interview" in question:
            debug.checkpoint("Interview ended early", {
                "questions_asked": question_num + 1
            })
            break

        # Get patient response (simulated)
        patient_response = get_patient_input()
        conversation.append({"role": "user", "content": patient_response})

        debug.variable(f"q{question_num + 1}_response", patient_response[:50])

    debug.checkpoint("Interview completed", {
        "total_questions": len([t for t in conversation if t["role"] == "assistant"])
    })

    return conversation
```

---

## Best Practices

### DO's ✅

- ✅ Use `debug_prompt_flow()` for step-by-step tracking
- ✅ Log all LLM interactions with `log_llm_interaction()`
- ✅ Use decorators for automatic function logging
- ✅ Log validation results (pass or fail)
- ✅ Include context in error logs
- ✅ Use appropriate log levels
- ✅ Log performance metrics for operations
- ✅ Include timestamps naturally (automatic)

### DON'Ts ❌

- ❌ Don't log sensitive patient data in plain text
- ❌ Don't use print() statements instead of logging
- ❌ Don't log passwords or API keys
- ❌ Don't disable logging in production
- ❌ Don't ignore log rotation settings
- ❌ Don't use DEBUG level for everything
- ❌ Don't forget to log errors with context

---

## Quick Reference

### Import Statements

```python
from utils.logger import (
    # Loggers
    app_logger,
    llm_logger,
    validation_logger,
    error_logger,
    perf_logger,

    # Helpers
    log_llm_interaction,
    log_validation,
    log_error,
    log_performance,

    # Decorators
    log_function_call,
    log_prompt_execution,

    # Debugging
    debug_prompt_flow,
    DebugLogger,
    LogContext,

    # Analysis
    get_recent_logs,
    get_error_summary,
    get_llm_summary,

    # Config
    LoggerConfig,
    initialize_logging
)
```

### Common Patterns

```python
# Pattern 1: Step-by-step debugging
debug = debug_prompt_flow("Operation Name")
debug.step("Doing something")
debug.variable("var_name", value)
debug.checkpoint("Milestone reached", {"data": "value"})

# Pattern 2: LLM interaction
log_llm_interaction(
    prompt_name="PROMPT_NAME",
    prompt_text=prompt,
    response=response,
    model="model-name",
    duration=duration
)

# Pattern 3: Validation
log_validation(
    validation_type="output_type",
    input_data=data,
    result=validation_result,
    passed=is_valid
)

# Pattern 4: Error handling
try:
    risky_operation()
except Exception as e:
    log_error(e, "Operation context", {"extra": "info"})
    raise

# Pattern 5: Context manager
with LogContext(app_logger, "Operation", key="value"):
    do_work()
```

---

**For more information:**
- See [utils/logger.py](../utils/logger.py) for implementation
- See [utils/prompt_executor.py](../utils/prompt_executor.py) for integration examples
- Check `logs/` directory for actual log files

**Last Updated:** October 2024
