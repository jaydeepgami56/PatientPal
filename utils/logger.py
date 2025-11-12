"""
Medical Triage AI - Comprehensive Logging System
=================================================
Provides detailed logging for debugging each step of the triage and report generation process.

Features:
- Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Structured logging with context
- LLM interaction logging (prompts, responses, tokens)
- Validation logging
- Performance metrics
- Rotating file logs
- Colored console output
"""

import logging
import logging.handlers
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from functools import wraps
import traceback


# ============================================================================
# LOGGER CONFIGURATION
# ============================================================================

class LoggerConfig:
    """Central configuration for all logging"""

    # Log levels
    CONSOLE_LEVEL = logging.INFO  # What shows in console
    FILE_LEVEL = logging.DEBUG    # What goes to file (everything)

    # Log directories
    LOG_DIR = Path("logs")
    LOG_DIR.mkdir(exist_ok=True)

    # Log files
    MAIN_LOG = LOG_DIR / "triage_app.log"
    LLM_LOG = LOG_DIR / "llm_interactions.log"
    VALIDATION_LOG = LOG_DIR / "validation.log"
    ERROR_LOG = LOG_DIR / "errors.log"
    PERFORMANCE_LOG = LOG_DIR / "performance.log"

    # Rotation settings
    MAX_BYTES = 10 * 1024 * 1024  # 10MB per file
    BACKUP_COUNT = 5  # Keep 5 backup files

    # Formatting
    DETAILED_FORMAT = (
        "%(asctime)s | %(name)s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
    )
    SIMPLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
    JSON_FORMAT = True  # Use JSON for structured logs


# ============================================================================
# CUSTOM FORMATTERS
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """Colored console output for better readability"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }

        # Add custom fields if present
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data, indent=2 if LoggerConfig.JSON_FORMAT else None)


# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: int = logging.DEBUG,
    use_json: bool = False
) -> logging.Logger:
    """
    Create and configure a logger

    Args:
        name: Logger name
        log_file: Path to log file (None for console only)
        level: Logging level
        use_json: Use JSON formatting

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LoggerConfig.CONSOLE_LEVEL)
    console_formatter = ColoredFormatter(LoggerConfig.SIMPLE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=LoggerConfig.MAX_BYTES,
            backupCount=LoggerConfig.BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(LoggerConfig.FILE_LEVEL)

        if use_json:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(LoggerConfig.DETAILED_FORMAT)

        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# ============================================================================
# SPECIALIZED LOGGERS
# ============================================================================

# Main application logger
app_logger = setup_logger('triage_app', LoggerConfig.MAIN_LOG)

# LLM interaction logger (JSON formatted)
llm_logger = setup_logger('llm', LoggerConfig.LLM_LOG, use_json=True)

# Validation logger
validation_logger = setup_logger('validation', LoggerConfig.VALIDATION_LOG)

# Error logger
error_logger = setup_logger('errors', LoggerConfig.ERROR_LOG)

# Performance logger
perf_logger = setup_logger('performance', LoggerConfig.PERFORMANCE_LOG)


# ============================================================================
# LOGGING HELPERS
# ============================================================================

class LogContext:
    """Context manager for structured logging with automatic timing"""

    def __init__(self, logger: logging.Logger, operation: str, **kwargs):
        self.logger = logger
        self.operation = operation
        self.context = kwargs
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(
            f"Starting: {self.operation}",
            extra={'extra_data': {'context': self.context}}
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time

        if exc_type:
            self.logger.error(
                f"Failed: {self.operation} (duration: {duration:.2f}s)",
                extra={'extra_data': {
                    'context': self.context,
                    'duration_seconds': duration,
                    'error': str(exc_val)
                }},
                exc_info=True
            )
        else:
            self.logger.info(
                f"Completed: {self.operation} (duration: {duration:.2f}s)",
                extra={'extra_data': {
                    'context': self.context,
                    'duration_seconds': duration
                }}
            )


def log_llm_interaction(
    prompt_name: str,
    prompt_text: str,
    response: str,
    model: str = "unknown",
    tokens_used: Optional[int] = None,
    duration: Optional[float] = None,
    metadata: Optional[Dict] = None
):
    """
    Log LLM interaction with full details

    Args:
        prompt_name: Name/type of prompt (e.g., "TRIAGE_PROMPT")
        prompt_text: Full prompt sent to LLM
        response: LLM response
        model: Model name
        tokens_used: Token count
        duration: Response time in seconds
        metadata: Additional metadata
    """
    log_data = {
        'prompt_name': prompt_name,
        'model': model,
        'prompt_length': len(prompt_text),
        'response_length': len(response),
        'prompt_preview': prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text,
        'response_preview': response[:200] + "..." if len(response) > 200 else response,
        'full_prompt': prompt_text,
        'full_response': response,
    }

    if tokens_used:
        log_data['tokens_used'] = tokens_used
    if duration:
        log_data['duration_seconds'] = duration
    if metadata:
        log_data['metadata'] = metadata

    llm_logger.info(
        f"LLM Interaction: {prompt_name}",
        extra={'extra_data': log_data}
    )


def log_validation(
    validation_type: str,
    input_data: str,
    result: Dict[str, Any],
    passed: bool
):
    """
    Log validation results

    Args:
        validation_type: Type of validation (e.g., "triage_output")
        input_data: Data being validated
        result: Validation result dict
        passed: Whether validation passed
    """
    log_level = logging.INFO if passed else logging.WARNING

    validation_logger.log(
        log_level,
        f"Validation {validation_type}: {'PASSED' if passed else 'FAILED'}",
        extra={'extra_data': {
            'type': validation_type,
            'input_preview': input_data[:200],
            'result': result,
            'passed': passed
        }}
    )


def log_performance(operation: str, duration: float, metadata: Optional[Dict] = None):
    """
    Log performance metrics

    Args:
        operation: Operation name
        duration: Duration in seconds
        metadata: Additional performance data
    """
    perf_data = {
        'operation': operation,
        'duration_seconds': duration,
        'duration_ms': duration * 1000
    }

    if metadata:
        perf_data.update(metadata)

    perf_logger.info(
        f"Performance: {operation} ({duration:.3f}s)",
        extra={'extra_data': perf_data}
    )


def log_error(
    error: Exception,
    context: str,
    additional_info: Optional[Dict] = None
):
    """
    Log errors with full context

    Args:
        error: Exception object
        context: Description of what was happening
        additional_info: Additional debugging info
    """
    error_data = {
        'context': context,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc()
    }

    if additional_info:
        error_data['additional_info'] = additional_info

    error_logger.error(
        f"Error in {context}: {str(error)}",
        extra={'extra_data': error_data},
        exc_info=True
    )


# ============================================================================
# DECORATORS FOR AUTOMATIC LOGGING
# ============================================================================

def log_function_call(logger: logging.Logger = app_logger):
    """
    Decorator to automatically log function entry/exit and timing

    Usage:
        @log_function_call()
        def my_function(arg1, arg2):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # Log entry
            logger.debug(
                f"→ Entering: {func_name}",
                extra={'extra_data': {
                    'function': func_name,
                    'args': str(args)[:100],
                    'kwargs': str(kwargs)[:100]
                }}
            )

            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # Log exit
                logger.debug(
                    f"← Exiting: {func_name} (duration: {duration:.3f}s)",
                    extra={'extra_data': {
                        'function': func_name,
                        'duration_seconds': duration,
                        'success': True
                    }}
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                # Log error
                logger.error(
                    f"✗ Failed: {func_name} (duration: {duration:.3f}s)",
                    extra={'extra_data': {
                        'function': func_name,
                        'duration_seconds': duration,
                        'error': str(e),
                        'success': False
                    }},
                    exc_info=True
                )
                raise

        return wrapper
    return decorator


def log_prompt_execution(prompt_name: str):
    """
    Decorator specifically for prompt execution logging

    Usage:
        @log_prompt_execution("TRIAGE_PROMPT")
        def execute_triage(report_text: str):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            logger.info(f"Executing prompt: {prompt_name}")

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                logger.info(
                    f"Prompt execution completed: {prompt_name}",
                    extra={'extra_data': {
                        'prompt_name': prompt_name,
                        'duration_seconds': duration,
                        'result_length': len(str(result)) if result else 0
                    }}
                )

                log_performance(f"prompt_{prompt_name}", duration)

                return result

            except Exception as e:
                duration = time.time() - start_time
                log_error(e, f"Prompt execution: {prompt_name}", {
                    'duration_seconds': duration,
                    'args': str(args)[:200]
                })
                raise

        return wrapper
    return decorator


# ============================================================================
# DEBUGGING UTILITIES
# ============================================================================

class DebugLogger:
    """Enhanced debugging logger with step-by-step tracking"""

    def __init__(self, name: str):
        self.logger = app_logger
        self.name = name
        self.step_number = 0

    def step(self, message: str, data: Optional[Dict] = None):
        """Log a debug step with automatic numbering"""
        self.step_number += 1
        step_msg = f"[STEP {self.step_number}] {self.name}: {message}"

        if data:
            self.logger.debug(step_msg, extra={'extra_data': data})
        else:
            self.logger.debug(step_msg)

    def checkpoint(self, name: str, data: Optional[Dict] = None):
        """Log a checkpoint with data snapshot"""
        checkpoint_msg = f"[CHECKPOINT] {self.name}.{name}"

        if data:
            self.logger.info(checkpoint_msg, extra={'extra_data': data})
        else:
            self.logger.info(checkpoint_msg)

    def variable(self, var_name: str, value: Any):
        """Log a variable value for debugging"""
        self.logger.debug(
            f"[VAR] {self.name}.{var_name} = {str(value)[:200]}",
            extra={'extra_data': {
                'variable': var_name,
                'value': value,
                'type': type(value).__name__
            }}
        )


def debug_prompt_flow(flow_name: str) -> DebugLogger:
    """
    Create a debug logger for tracking prompt flow

    Usage:
        debug = debug_prompt_flow("Triage Assessment")
        debug.step("Validating input")
        debug.variable("report_length", len(report))
        debug.checkpoint("Input validated", {"status": "ok"})
    """
    return DebugLogger(flow_name)


# ============================================================================
# LOG ANALYSIS HELPERS
# ============================================================================

def get_recent_logs(log_file: Path, lines: int = 100) -> str:
    """Get recent log entries from a file"""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            return ''.join(all_lines[-lines:])
    except FileNotFoundError:
        return f"Log file not found: {log_file}"


def get_error_summary() -> str:
    """Get summary of recent errors"""
    return get_recent_logs(LoggerConfig.ERROR_LOG, 50)


def get_llm_summary(interactions: int = 10) -> str:
    """Get summary of recent LLM interactions"""
    return get_recent_logs(LoggerConfig.LLM_LOG, interactions * 30)  # ~30 lines per interaction


# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_logging(verbose: bool = False):
    """
    Initialize logging system

    Args:
        verbose: If True, set console to DEBUG level
    """
    if verbose:
        LoggerConfig.CONSOLE_LEVEL = logging.DEBUG
        for logger in [app_logger, llm_logger, validation_logger, error_logger, perf_logger]:
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.DEBUG)

    app_logger.info("=" * 60)
    app_logger.info("Medical Triage AI - Logging System Initialized")
    app_logger.info(f"Log directory: {LoggerConfig.LOG_DIR.absolute()}")
    app_logger.info(f"Console level: {logging.getLevelName(LoggerConfig.CONSOLE_LEVEL)}")
    app_logger.info(f"File level: {logging.getLevelName(LoggerConfig.FILE_LEVEL)}")
    app_logger.info("=" * 60)


# Auto-initialize on import
initialize_logging()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """Example usage of logging system"""

    # Basic logging
    app_logger.info("Application started")
    app_logger.debug("Debug information")
    app_logger.warning("Warning message")

    # Context manager for operations
    with LogContext(app_logger, "Processing patient data", patient_id="P12345"):
        time.sleep(0.1)  # Simulate work

    # LLM interaction logging
    log_llm_interaction(
        prompt_name="TRIAGE_PROMPT",
        prompt_text="Sample prompt text...",
        response="ATS CATEGORY: 3\nCLINICAL DESCRIPTOR: Potentially life-threatening",
        model="claude-3",
        tokens_used=150,
        duration=1.2
    )

    # Validation logging
    log_validation(
        validation_type="triage_output",
        input_data="ATS CATEGORY: 3...",
        result={"valid": True, "errors": []},
        passed=True
    )

    # Debug flow tracking
    debug = debug_prompt_flow("Interview Process")
    debug.step("Starting interview")
    debug.variable("question_count", 0)
    debug.checkpoint("Interview initialized")

    # Function decorator example
    @log_function_call()
    def sample_function(x: int, y: int) -> int:
        return x + y

    result = sample_function(5, 3)

    # Error logging
    try:
        raise ValueError("Sample error for demonstration")
    except ValueError as e:
        log_error(e, "Sample operation", {"data": "test"})

    print("\n" + "=" * 60)
    print("Logs written to:")
    print(f"  - {LoggerConfig.MAIN_LOG}")
    print(f"  - {LoggerConfig.LLM_LOG}")
    print(f"  - {LoggerConfig.VALIDATION_LOG}")
    print(f"  - {LoggerConfig.ERROR_LOG}")
    print(f"  - {LoggerConfig.PERFORMANCE_LOG}")
    print("=" * 60)
