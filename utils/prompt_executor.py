"""
Prompt Executor with Integrated Logging
========================================
Example of how to integrate the logging system with LLM prompt execution.
"""

import time
from typing import Dict, Any, Optional
from utils.logger import (
    app_logger,
    llm_logger,
    log_llm_interaction,
    log_validation,
    log_error,
    log_performance,
    log_function_call,
    log_prompt_execution,
    debug_prompt_flow,
    LogContext
)
from utils.prompts import (
    TRIAGE_PROMPT,
    CONVERSATIONAL_TRIAGE_PROMPT,
    INTERVIEW_PROMPT,
    REPORT_PROMPT
)


class PromptExecutor:
    """
    Executes prompts with comprehensive logging at every step
    """

    def __init__(self, llm_client, model_name: str = "claude-3-sonnet"):
        """
        Initialize prompt executor

        Args:
            llm_client: LLM client instance
            model_name: Name of the model being used
        """
        self.llm_client = llm_client
        self.model_name = model_name
        app_logger.info(f"PromptExecutor initialized with model: {model_name}")

    @log_prompt_execution("TRIAGE_PROMPT")
    def execute_triage_assessment(self, report: str) -> Dict[str, Any]:
        """
        Execute triage assessment with full logging

        Args:
            report: Pre-visit report text

        Returns:
            Parsed triage assessment
        """
        debug = debug_prompt_flow("Triage Assessment")

        # Step 1: Input validation
        debug.step("Validating input report")
        debug.variable("report_length", len(report))

        if not report or len(report) < 10:
            error_msg = "Report too short or empty"
            app_logger.error(error_msg)
            raise ValueError(error_msg)

        debug.checkpoint("Input validated", {"report_length": len(report)})

        # Step 2: Format prompt
        debug.step("Formatting prompt with report data")
        prompt_text = TRIAGE_PROMPT.format(report=report)
        debug.variable("prompt_length", len(prompt_text))

        # Step 3: Execute LLM call
        debug.step("Calling LLM")
        start_time = time.time()

        try:
            with LogContext(app_logger, "LLM API Call", model=self.model_name):
                response = self.llm_client.generate(
                    prompt=prompt_text,
                    model=self.model_name
                )

            duration = time.time() - start_time
            debug.checkpoint("LLM response received", {
                "duration": duration,
                "response_length": len(response)
            })

            # Step 4: Log LLM interaction
            debug.step("Logging LLM interaction")
            log_llm_interaction(
                prompt_name="TRIAGE_PROMPT",
                prompt_text=prompt_text,
                response=response,
                model=self.model_name,
                tokens_used=getattr(self.llm_client, 'last_token_count', None),
                duration=duration,
                metadata={"report_length": len(report)}
            )

            # Step 5: Parse response
            debug.step("Parsing LLM response")
            parsed = self._parse_triage_response(response)
            debug.variable("parsed_category", parsed.get("category"))

            # Step 6: Validate output
            debug.step("Validating output format")
            validation_result = self._validate_triage_output(response)
            debug.checkpoint("Validation complete", validation_result)

            log_validation(
                validation_type="triage_output",
                input_data=response,
                result=validation_result,
                passed=validation_result.get("valid", False)
            )

            if not validation_result.get("valid"):
                app_logger.warning(
                    f"Validation failed: {validation_result.get('errors')}"
                )

            # Step 7: Return result
            debug.step("Returning parsed result")
            return {
                "raw_response": response,
                "parsed": parsed,
                "validation": validation_result,
                "metadata": {
                    "duration": duration,
                    "model": self.model_name,
                    "prompt_length": len(prompt_text)
                }
            }

        except Exception as e:
            log_error(e, "Triage assessment execution", {
                "report_length": len(report),
                "model": self.model_name
            })
            raise

    @log_prompt_execution("CONVERSATIONAL_TRIAGE_PROMPT")
    def execute_conversational_triage(
        self,
        user_input: str,
        chat_history: str = "",
        symptoms: str = ""
    ) -> Dict[str, Any]:
        """
        Execute conversational triage with logging

        Args:
            user_input: Current user message
            chat_history: Previous conversation
            symptoms: Symptoms collected so far

        Returns:
            Response (question or assessment)
        """
        debug = debug_prompt_flow("Conversational Triage")

        debug.step("Starting conversational triage")
        debug.variable("user_input", user_input)
        debug.variable("chat_history_length", len(chat_history))
        debug.variable("symptoms", symptoms)

        # Format prompt
        debug.step("Formatting conversational prompt")
        prompt_text = CONVERSATIONAL_TRIAGE_PROMPT.format(
            chat_history=chat_history,
            symptoms=symptoms,
            input=user_input
        )

        # Execute
        debug.step("Executing LLM call")
        start_time = time.time()

        try:
            response = self.llm_client.generate(
                prompt=prompt_text,
                model=self.model_name
            )

            duration = time.time() - start_time

            # Log interaction
            log_llm_interaction(
                prompt_name="CONVERSATIONAL_TRIAGE_PROMPT",
                prompt_text=prompt_text,
                response=response,
                model=self.model_name,
                duration=duration,
                metadata={
                    "chat_history_length": len(chat_history),
                    "user_input": user_input[:100]
                }
            )

            # Determine if question or assessment
            is_assessment = "TRIAGE ASSESSMENT:" in response
            debug.checkpoint("Response type determined", {
                "is_assessment": is_assessment
            })

            return {
                "response": response,
                "is_assessment": is_assessment,
                "duration": duration
            }

        except Exception as e:
            log_error(e, "Conversational triage", {
                "user_input": user_input[:100]
            })
            raise

    @log_prompt_execution("INTERVIEW_PROMPT")
    def execute_interview_question(
        self,
        conversation_history: list,
        question_count: int
    ) -> str:
        """
        Execute interview question generation

        Args:
            conversation_history: List of conversation turns
            question_count: Number of questions asked so far

        Returns:
            Next question or closing statement
        """
        debug = debug_prompt_flow("Interview")

        debug.step("Generating interview question")
        debug.variable("question_count", question_count)
        debug.variable("history_length", len(conversation_history))

        # Check if we should end
        if question_count >= 15:
            debug.checkpoint("Interview limit reached", {"question_count": 15})
            return (
                "Thank you for answering my questions. "
                "I have everything needed to prepare your GP's report. "
                "End interview."
            )

        # Format conversation for prompt
        chat_history = self._format_chat_history(conversation_history)
        debug.variable("chat_history_length", len(chat_history))

        # Execute
        start_time = time.time()

        try:
            response = self.llm_client.generate(
                prompt=INTERVIEW_PROMPT + f"\n\nConversation so far:\n{chat_history}",
                model=self.model_name
            )

            duration = time.time() - start_time

            log_llm_interaction(
                prompt_name="INTERVIEW_PROMPT",
                prompt_text=INTERVIEW_PROMPT[:500] + "...",
                response=response,
                model=self.model_name,
                duration=duration,
                metadata={
                    "question_number": question_count + 1,
                    "total_questions": 15
                }
            )

            debug.checkpoint("Question generated", {
                "question_preview": response[:100]
            })

            return response

        except Exception as e:
            log_error(e, "Interview question generation", {
                "question_count": question_count
            })
            raise

    @log_prompt_execution("REPORT_PROMPT")
    def execute_report_generation(
        self,
        interview_transcript: str,
        ehr_data: Optional[str] = None
    ) -> str:
        """
        Execute clinical report generation

        Args:
            interview_transcript: Complete interview conversation
            ehr_data: Electronic health record data

        Returns:
            Generated clinical report
        """
        debug = debug_prompt_flow("Report Generation")

        debug.step("Starting report generation")
        debug.variable("transcript_length", len(interview_transcript))
        debug.variable("has_ehr_data", ehr_data is not None)

        # Prepare input
        full_context = f"""
Interview Transcript:
{interview_transcript}

EHR Data:
{ehr_data if ehr_data else "No EHR data available"}
"""

        debug.variable("full_context_length", len(full_context))

        # Execute
        debug.step("Calling LLM for report generation")
        start_time = time.time()

        try:
            response = self.llm_client.generate(
                prompt=REPORT_PROMPT + f"\n\nPatient Data:\n{full_context}",
                model=self.model_name
            )

            duration = time.time() - start_time

            log_llm_interaction(
                prompt_name="REPORT_PROMPT",
                prompt_text=REPORT_PROMPT[:500] + "...",
                response=response,
                model=self.model_name,
                duration=duration,
                metadata={
                    "transcript_length": len(interview_transcript),
                    "has_ehr": ehr_data is not None
                }
            )

            # Validate report structure
            debug.step("Validating report structure")
            validation = self._validate_report_structure(response)
            debug.checkpoint("Report validated", validation)

            log_validation(
                validation_type="clinical_report",
                input_data=response[:500],
                result=validation,
                passed=validation.get("valid", False)
            )

            if not validation.get("valid"):
                app_logger.warning(
                    f"Report validation issues: {validation.get('errors')}"
                )

            return response

        except Exception as e:
            log_error(e, "Report generation", {
                "transcript_length": len(interview_transcript)
            })
            raise

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @log_function_call()
    def _parse_triage_response(self, response: str) -> Dict[str, Any]:
        """Parse triage response into structured data"""
        import re

        parsed = {}

        # Extract ATS category
        category_match = re.search(r'ATS CATEGORY:\s*([1-5])', response)
        if category_match:
            parsed["category"] = int(category_match.group(1))

        # Extract clinical descriptor
        descriptor_match = re.search(
            r'CLINICAL DESCRIPTOR:\s*(.+?)(?:\n|$)',
            response
        )
        if descriptor_match:
            parsed["descriptor"] = descriptor_match.group(1).strip()

        # Extract care pathway
        pathway_match = re.search(
            r'CARE PATHWAY:\s*(.+?)(?:\n|$)',
            response
        )
        if pathway_match:
            parsed["pathway"] = pathway_match.group(1).strip()

        app_logger.debug(f"Parsed triage data: {parsed}")
        return parsed

    @log_function_call()
    def _validate_triage_output(self, output: str) -> Dict[str, Any]:
        """Validate triage output format"""
        errors = []
        warnings = []

        # Check starts correctly
        if not output.strip().startswith("ATS CATEGORY:"):
            errors.append("Does not start with 'ATS CATEGORY:'")

        # Check required fields
        required_fields = [
            "ATS CATEGORY:",
            "CLINICAL DESCRIPTOR:",
            "TO BE SEEN WITHIN:",
            "CARE PATHWAY:",
            "RED FLAGS IDENTIFIED:"
        ]

        for field in required_fields:
            if field not in output:
                errors.append(f"Missing field: {field}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    @log_function_call()
    def _validate_report_structure(self, report: str) -> Dict[str, Any]:
        """Validate clinical report structure"""
        errors = []

        required_sections = [
            "## Presenting Complaint",
            "## History of Presenting Complaint (HPC)",
            "## Pertinent Negatives",
            "## Relevant Medical History",
            "## Functional Impact",
            "## Patient Concerns or Questions"
        ]

        for section in required_sections:
            if section not in report:
                errors.append(f"Missing section: {section}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _format_chat_history(self, history: list) -> str:
        """Format conversation history for prompt"""
        formatted = []
        for i, turn in enumerate(history):
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            formatted.append(f"{role.capitalize()}: {content}")

        return "\n".join(formatted)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """Example of using PromptExecutor with logging"""

    # Mock LLM client for demonstration
    class MockLLMClient:
        def generate(self, prompt: str, model: str) -> str:
            # Simulate response
            time.sleep(0.5)
            return """ATS CATEGORY: 3
CLINICAL DESCRIPTOR: Potentially life-threatening
TO BE SEEN WITHIN: 30 minutes
CARE PATHWAY: Emergency Department
RED FLAGS IDENTIFIED: No
KEY CLINICAL FEATURES:
• Moderate pain (6/10)
• Recent onset
SPECIAL CONSIDERATIONS: None
RECOMMENDED IMMEDIATE ACTIONS: Attend ED within 30 minutes
CLINICAL REASONING: Moderate pain with recent onset warrants urgent assessment."""

    # Initialize
    client = MockLLMClient()
    executor = PromptExecutor(client, "claude-3-sonnet")

    # Execute triage
    print("\n" + "=" * 60)
    print("Executing Triage Assessment with Full Logging")
    print("=" * 60 + "\n")

    result = executor.execute_triage_assessment(
        report="Patient reports chest discomfort for 2 hours. Pain 6/10."
    )

    print("\nResult:")
    print(f"  Category: {result['parsed'].get('category')}")
    print(f"  Valid: {result['validation'].get('valid')}")
    print(f"  Duration: {result['metadata'].get('duration'):.2f}s")

    print("\n" + "=" * 60)
    print("Check log files in ./logs/ directory for detailed logging")
    print("=" * 60)
