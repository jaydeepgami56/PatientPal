"""
Pre-Visit AI Agent with Triage Integration (Australian Standards)
==================================================================
An intelligent agent that conducts pre-visit interviews, generates RACGP-compliant reports,
and determines triage urgency levels using the Australasian Triage Scale (ATS).

Features:
- Comprehensive logging for each step
- All prompts from utils/prompts.py
- Australian health standards (ATS, RACGP)
- Validation with logging
- Step-by-step debugging
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from datetime import datetime
import os
import sys
import time
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration MUST be first
st.set_page_config(
    page_title="Pre-Visit AI Agent (ATS)",
    page_icon="🏥",
    layout="wide"
)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import prompts (using the ones we need)
from utils.prompts import (
    TRIAGE_PROMPT,
    INTERVIEW_PROMPT,
    REPORT_PROMPT
)

# Import logging utilities
from utils.logger import (
    app_logger,
    debug_prompt_flow,
    log_llm_interaction,
    log_validation,
    log_error,
    initialize_logging
)

from utils.common_utils import log_message, clear_all_caches

# Initialize logging with verbose mode (set to False for production)
initialize_logging(verbose=True)

app_logger.info("=" * 60)
app_logger.info("Pre-Visit AI Agent (Australian Standards) - Starting")
app_logger.info("=" * 60)

# Load CSS
def load_css():
    debug = debug_prompt_flow("CSS Loading")
    debug.step("Loading custom CSS")

    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'styles', 'custom.css')

    if not os.path.exists(css_file):
        css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'styles', 'triage_agent_style.css')

    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        debug.checkpoint("CSS loaded successfully", {"file": css_file})
    except Exception as e:
        log_error(e, "CSS Loading", {"file": css_file})
        log_message("error", f"Error loading CSS: {e}")

load_css()

# Clear cache on app startup
if 'app_initialized' not in st.session_state:
    app_logger.info("Initializing application for first time")
    clear_all_caches()
    st.session_state.app_initialized = True

# Initialize session state
if 'phase' not in st.session_state:
    st.session_state.phase = 'welcome'  # welcome, interview, report, triage
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_data' not in st.session_state:
    st.session_state.interview_data = {
        'chief_complaint': None,
        'symptoms': [],
        'duration': None,
        'severity': None,
        'medical_history': [],
        'medications': [],
        'allergies': [],
        'vital_signs': {},
        'additional_info': []
    }
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'pre_visit_report' not in st.session_state:
    st.session_state.pre_visit_report = None
if 'triage_assessment' not in st.session_state:
    st.session_state.triage_assessment = None
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = {}

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_triage_output(output: str) -> dict:
    """Validate triage output against Australian standards"""
    debug = debug_prompt_flow("Triage Validation")
    debug.step("Starting validation")

    errors = []
    warnings = []

    # Check starts correctly
    debug.step("Checking output format")
    if not output.strip().startswith("ATS CATEGORY:"):
        errors.append("Does not start with 'ATS CATEGORY:'")

    # Check required fields
    debug.step("Checking required fields")
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

    # Extract ATS category
    debug.step("Extracting ATS category")
    category_match = re.search(r'ATS CATEGORY:\s*([1-5])', output)
    if category_match:
        category = int(category_match.group(1))
        debug.variable("ats_category", category)

        # Check for 000 in ATS 1
        if category == 1 and "000" not in output:
            warnings.append("ATS 1 should include 'Call 000' instruction")
    else:
        errors.append("Invalid or missing ATS category (must be 1-5)")

    # Check for Australian terminology
    debug.step("Checking Australian terminology")
    american_terms = {
        "911": "000",
        "ER": "Emergency Department",
        "pediatric": "paediatric"
    }

    for american, australian in american_terms.items():
        if american in output:
            warnings.append(f"American term '{american}' found (should be '{australian}')")

    validation_result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "category": category_match.group(1) if category_match else None
    }

    debug.checkpoint("Validation complete", validation_result)

    log_validation(
        validation_type="triage_output_ats",
        input_data=output[:500],
        result=validation_result,
        passed=validation_result["valid"]
    )

    return validation_result


def validate_report_structure(report: str) -> dict:
    """Validate clinical report structure against RACGP standards"""
    debug = debug_prompt_flow("Report Validation")
    debug.step("Starting report validation")

    errors = []
    warnings = []

    # Required sections for RACGP compliance
    required_sections = [
        "## Presenting Complaint",
        "## History of Presenting Complaint (HPC)",
        "## Pertinent Negatives",
        "## Relevant Medical History",
        "## Functional Impact",
        "## Patient Concerns or Questions"
    ]

    debug.step("Checking required sections")
    for section in required_sections:
        if section not in report:
            errors.append(f"Missing section: {section}")

    # Check starts correctly (no preamble)
    debug.step("Checking for preamble")
    if not report.strip().startswith("## Presenting Complaint"):
        errors.append("Report should start with '## Presenting Complaint'")

    # Check for Australian spelling
    debug.step("Checking Australian terminology")
    american_spellings = {
        "pediatric": "paediatric",
        "hemoptysis": "haemoptysis",
        "edema": "oedema"
    }

    for american, australian in american_spellings.items():
        if american in report.lower():
            warnings.append(f"American spelling '{american}' found (should be '{australian}')")

    validation_result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "sections_found": len([s for s in required_sections if s in report])
    }

    debug.checkpoint("Report validation complete", validation_result)

    log_validation(
        validation_type="clinical_report_racgp",
        input_data=report[:500],
        result=validation_result,
        passed=validation_result["valid"]
    )

    return validation_result


# ============================================================================
# LLM INITIALIZATION
# ============================================================================

@st.cache_resource
def get_llm(_api_key):
    """Initialize LLM with logging"""
    debug = debug_prompt_flow("LLM Initialization")
    debug.step("Creating ChatOpenAI instance")
    debug.variable("model", "gpt-4o-mini")

    try:
        llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4o-mini",
            openai_api_key=_api_key
        )
        debug.checkpoint("LLM initialized successfully")
        app_logger.info("LLM initialized: gpt-4o-mini")
        return llm
    except Exception as e:
        log_error(e, "LLM Initialization", {"model": "gpt-4o-mini"})
        raise


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("🏥 Pre-Visit Agent (ATS)")
    st.markdown("---")

    # Progress indicator
    st.markdown("### 📋 Assessment Progress")

    phases = [
        ("Welcome", "welcome"),
        ("Interview (15Q)", "interview"),
        ("RACGP Report", "report"),
        ("ATS Triage", "triage")
    ]

    for phase_name, phase_key in phases:
        current_phase_index = [p[1] for p in phases].index(st.session_state.phase)
        this_phase_index = [p[1] for p in phases].index(phase_key)

        if st.session_state.phase == phase_key:
            st.markdown(f'<div class="progress-step">✓ {phase_name} (Current)</div>', unsafe_allow_html=True)
        elif this_phase_index < current_phase_index:
            st.markdown(f'<div class="progress-step completed-step">✓ {phase_name}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="progress-step">○ {phase_name}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**Questions Asked:** {st.session_state.question_count}/15")

    if st.session_state.interview_data['symptoms']:
        st.markdown("**Symptoms Detected:**")
        for symptom in st.session_state.interview_data['symptoms'][:5]:
            st.markdown(f"• {symptom}")

    # Validation status
    if st.session_state.validation_results:
        st.markdown("---")
        st.markdown("### ✅ Validation Status")
        for val_type, result in st.session_state.validation_results.items():
            status = "✅ Pass" if result.get("valid") else "❌ Fail"
            st.markdown(f"**{val_type}:** {status}")
            if result.get("warnings"):
                st.markdown(f"⚠️ {len(result['warnings'])} warnings")

    st.markdown("---")
    if st.button("🔄 Start New Assessment", use_container_width=True):
        app_logger.info("User requested new assessment - clearing session")
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        clear_all_caches()
        log_message("success", "Assessment reset successfully!")
        st.rerun()


# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title("🏥 Pre-Visit AI Agent (Australian Standards)")

# Check API key
if not api_key:
    log_message("error", "Please set your OPENAI_API_KEY in the .env file")
    app_logger.error("Missing OPENAI_API_KEY")
    st.stop()

# Initialize LLM
llm = get_llm(api_key)


# ============================================================================
# WELCOME PHASE
# ============================================================================

if st.session_state.phase == 'welcome':
    app_logger.info("Displaying welcome screen")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="info-card">
            <h2 style="color: #8b5cf6; text-align: center;">Welcome to Pre-Visit Assessment</h2>
            <p style="text-align: center; font-size: 18px; color: #c0c0d0;">
                I'll conduct a structured 15-question interview to gather information for your GP appointment.
                This follows RACGP standards and uses the Australasian Triage Scale (ATS).
            </p>
            <br>
            <p style="text-align: center; color: #a0a0c0;">
                ✓ Systematic 15-question clinical interview<br>
                ✓ RACGP-compliant report generation<br>
                ✓ ATS triage assessment (Categories 1-5)<br>
                ✓ All information is confidential<br>
                ✓ Australian health standards applied
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Pre-Visit Interview", use_container_width=True):
            debug = debug_prompt_flow("Interview Start")
            debug.step("User started interview")

            st.session_state.phase = 'interview'

            # Opening question from INTERVIEW_PROMPT
            opening_msg = "Thank you for booking your GP appointment. I'll ask a few questions to help your doctor prepare. What brings you in today?"

            st.session_state.messages.append({
                "role": "assistant",
                "content": opening_msg
            })

            debug.checkpoint("Interview initialized", {"opening_sent": True})
            app_logger.info("Interview started - opening question sent")
            st.rerun()


# ============================================================================
# INTERVIEW PHASE
# ============================================================================

elif st.session_state.phase == 'interview':
    debug = debug_prompt_flow("Interview Phase")
    debug.step("Rendering interview interface")
    debug.variable("question_count", st.session_state.question_count)

    st.markdown('<div class="section-header">Pre-Visit Interview (RACGP Standards)</div>', unsafe_allow_html=True)
    st.markdown(f"**Progress:** {st.session_state.question_count}/15 questions")

    # Display conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Check if interview should end
    if st.session_state.question_count >= 15:
        debug.checkpoint("Interview limit reached", {"questions": 15})
        app_logger.info("Interview complete - 15 questions reached")

        # Send closing statement
        closing_msg = "Thank you for answering my questions. I have everything needed to prepare your GP's report. End interview."
        st.session_state.messages.append({
            "role": "assistant",
            "content": closing_msg
        })

        st.info("✅ Interview complete! Click below to generate your report.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Generate RACGP Report", use_container_width=True):
                st.session_state.phase = 'report'
                st.rerun()

    # Chat input (only if not complete)
    elif user_input := st.chat_input("Type your response here..."):
        debug.step(f"Processing user input for question {st.session_state.question_count + 1}")
        debug.variable("user_input_length", len(user_input))

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.question_count += 1

        # Extract information
        if st.session_state.question_count == 1:
            st.session_state.interview_data['chief_complaint'] = user_input
            debug.variable("chief_complaint", user_input[:50])

        # Simple symptom extraction
        symptom_keywords = ['pain', 'fever', 'cough', 'headache', 'nausea', 'dizzy',
                           'bleeding', 'swelling', 'rash', 'tired', 'weak', 'chest',
                           'breathing', 'stomach', 'back', 'vomiting', 'diarrhoea']
        for keyword in symptom_keywords:
            if keyword in user_input.lower() and keyword not in st.session_state.interview_data['symptoms']:
                st.session_state.interview_data['symptoms'].append(keyword)
                debug.variable("symptom_detected", keyword)

        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate next question using INTERVIEW_PROMPT
        with st.chat_message("assistant"):
            with st.spinner("Generating next question..."):
                debug.step("Calling LLM for next question")
                start_time = time.time()

                try:
                    # Format conversation history
                    conversation_context = []
                    for msg in st.session_state.messages[-10:]:  # Last 10 messages
                        if msg["role"] == "user":
                            conversation_context.append(HumanMessage(content=msg["content"]))
                        else:
                            conversation_context.append(AIMessage(content=msg["content"]))

                    # Add system message with INTERVIEW_PROMPT
                    system_context = [SystemMessage(content=INTERVIEW_PROMPT)] + conversation_context

                    response = llm.invoke(system_context)
                    assistant_msg = response.content
                    duration = time.time() - start_time

                    debug.variable("response_length", len(assistant_msg))
                    debug.checkpoint("Question generated", {"duration": duration})

                    # Log LLM interaction
                    log_llm_interaction(
                        prompt_name="INTERVIEW_PROMPT",
                        prompt_text=INTERVIEW_PROMPT[:500] + "...",
                        response=assistant_msg,
                        model="gpt-4o-mini",
                        duration=duration,
                        metadata={
                            "question_number": st.session_state.question_count,
                            "total_questions": 15
                        }
                    )

                    st.markdown(assistant_msg)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

                except Exception as e:
                    log_error(e, "Interview question generation", {
                        "question_count": st.session_state.question_count
                    })
                    st.error(f"Error generating question: {str(e)}")

    # Option to complete interview early
    if st.session_state.question_count >= 5:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Complete Interview Early & Generate Report", use_container_width=True):
                app_logger.info(f"Interview ended early at {st.session_state.question_count} questions")
                st.session_state.phase = 'report'
                st.rerun()


# ============================================================================
# REPORT PHASE
# ============================================================================

elif st.session_state.phase == 'report':
    debug = debug_prompt_flow("Report Generation")
    debug.step("Starting report generation phase")

    st.markdown('<div class="section-header">Generating RACGP-Compliant Clinical Report</div>', unsafe_allow_html=True)

    if not st.session_state.pre_visit_report:
        with st.spinner("Analyzing conversation and generating comprehensive RACGP report..."):
            debug.step("Formatting conversation for report")

            # Format conversation
            conversation = "\n".join([
                f"{'Patient' if msg['role'] == 'user' else 'AI Agent'}: {msg['content']}"
                for msg in st.session_state.messages
            ])

            debug.variable("conversation_length", len(conversation))

            # Use REPORT_PROMPT
            debug.step("Calling LLM for report generation")
            start_time = time.time()

            try:
                # Prepare full context
                full_context = f"""
Interview Transcript:
{conversation}

EHR Data:
No prior EHR data available for this session.

Please generate a RACGP-compliant clinical report based on this interview.
"""

                prompt_text = REPORT_PROMPT + "\n\n" + full_context

                response = llm.invoke([HumanMessage(content=prompt_text)])
                st.session_state.pre_visit_report = response.content
                duration = time.time() - start_time

                debug.variable("report_length", len(st.session_state.pre_visit_report))
                debug.checkpoint("Report generated", {"duration": duration})

                # Log LLM interaction
                log_llm_interaction(
                    prompt_name="REPORT_PROMPT",
                    prompt_text=REPORT_PROMPT[:500] + "...",
                    response=st.session_state.pre_visit_report,
                    model="gpt-4o-mini",
                    duration=duration,
                    metadata={
                        "conversation_length": len(conversation),
                        "question_count": st.session_state.question_count
                    }
                )

                # Validate report
                debug.step("Validating report structure")
                validation_result = validate_report_structure(st.session_state.pre_visit_report)
                st.session_state.validation_results['report'] = validation_result

                if not validation_result['valid']:
                    app_logger.warning(f"Report validation failed: {validation_result['errors']}")
                else:
                    app_logger.info("Report validation passed")

            except Exception as e:
                log_error(e, "Report generation", {
                    "conversation_length": len(conversation)
                })
                st.error(f"Error generating report: {str(e)}")
                st.stop()

    # Display report
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown(st.session_state.pre_visit_report)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show validation results
    if 'report' in st.session_state.validation_results:
        result = st.session_state.validation_results['report']

        if result['valid']:
            st.success(f"✅ Report validation passed - {result['sections_found']}/6 sections found")
        else:
            st.warning("⚠️ Report validation issues found:")
            for error in result['errors']:
                st.write(f"- {error}")

        if result['warnings']:
            st.info(f"ℹ️ {len(result['warnings'])} warnings:")
            for warning in result['warnings']:
                st.write(f"- {warning}")

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Download RACGP Report",
            data=st.session_state.pre_visit_report,
            file_name=f"racgp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        if st.button("🏥 Generate ATS Triage Assessment", use_container_width=True):
            app_logger.info("User requested triage assessment")
            st.session_state.phase = 'triage'
            st.rerun()


# ============================================================================
# TRIAGE PHASE
# ============================================================================

elif st.session_state.phase == 'triage':
    debug = debug_prompt_flow("Triage Assessment")
    debug.step("Starting ATS triage assessment")

    st.markdown('<div class="section-header">Australasian Triage Scale (ATS) Assessment</div>', unsafe_allow_html=True)

    if not st.session_state.triage_assessment:
        with st.spinner("Analyzing urgency using Australasian Triage Scale (ATS)..."):
            debug.step("Calling LLM for triage assessment")
            start_time = time.time()

            try:
                # Use TRIAGE_PROMPT with the report
                prompt_text = TRIAGE_PROMPT.format(report=st.session_state.pre_visit_report)

                response = llm.invoke([HumanMessage(content=prompt_text)])
                st.session_state.triage_assessment = response.content
                duration = time.time() - start_time

                debug.variable("assessment_length", len(st.session_state.triage_assessment))
                debug.checkpoint("Triage assessment generated", {"duration": duration})

                # Log LLM interaction
                log_llm_interaction(
                    prompt_name="TRIAGE_PROMPT",
                    prompt_text=prompt_text[:500] + "...",
                    response=st.session_state.triage_assessment,
                    model="gpt-4o-mini",
                    duration=duration,
                    metadata={
                        "report_length": len(st.session_state.pre_visit_report)
                    }
                )

                # Validate triage output
                debug.step("Validating triage assessment")
                validation_result = validate_triage_output(st.session_state.triage_assessment)
                st.session_state.validation_results['triage'] = validation_result

                if not validation_result['valid']:
                    app_logger.warning(f"Triage validation failed: {validation_result['errors']}")
                else:
                    app_logger.info(f"Triage validation passed - ATS Category: {validation_result.get('category')}")

            except Exception as e:
                log_error(e, "Triage assessment generation", {
                    "report_available": bool(st.session_state.pre_visit_report)
                })
                st.error(f"Error generating triage assessment: {str(e)}")
                st.stop()

    # Parse ATS category
    ats_category = "3"
    category_match = re.search(r'ATS CATEGORY:\s*([1-5])', st.session_state.triage_assessment)
    if category_match:
        ats_category = category_match.group(1)

    debug.variable("ats_category", ats_category)

    # Display with appropriate styling
    triage_class = f"triage-level-{ats_category if ats_category in ['1','2','3','4','5'] else '3'}"

    st.markdown(f'<div class="{triage_class}">', unsafe_allow_html=True)
    st.markdown(st.session_state.triage_assessment)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show validation results
    if 'triage' in st.session_state.validation_results:
        result = st.session_state.validation_results['triage']

        if result['valid']:
            st.success(f"✅ ATS validation passed - Category: {result.get('category')}")
        else:
            st.error("❌ ATS validation failed:")
            for error in result['errors']:
                st.write(f"- {error}")

        if result['warnings']:
            st.warning(f"⚠️ {len(result['warnings'])} warnings:")
            for warning in result['warnings']:
                st.write(f"- {warning}")

    # Alert for critical cases
    if ats_category == '1':
        log_message("error", "🚨 ATS 1 - IMMEDIATELY LIFE-THREATENING: Call 000 NOW!")
        app_logger.critical(f"ATS 1 assessment generated - IMMEDIATE action required")
    elif ats_category == '2':
        log_message("warning", "⚠️ ATS 2 - IMMINENTLY LIFE-THREATENING: Go to Emergency Department or call 000")
        app_logger.error(f"ATS 2 assessment generated - URGENT action required")
    elif ats_category == '3':
        log_message("warning", "ℹ️ ATS 3 - POTENTIALLY LIFE-THREATENING: Attend ED/Urgent Care within 30 minutes")
        app_logger.warning(f"ATS 3 assessment generated")
    else:
        app_logger.info(f"ATS {ats_category} assessment generated")

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="📄 Download RACGP Report",
            data=st.session_state.pre_visit_report,
            file_name=f"racgp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        st.download_button(
            label="🏥 Download ATS Triage",
            data=st.session_state.triage_assessment,
            file_name=f"ats_triage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col3:
        if st.button("🔄 New Assessment", use_container_width=True):
            app_logger.info("Starting new assessment - clearing all data")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #606080; font-size: 0.85em; padding: 20px;'>
    <p>⚕️ Pre-Visit AI Agent - Australian Health Standards (ATS, RACGP)</p>
    <p style="font-size: 0.75em; margin-top: 10px;">
        This system follows the Australasian Triage Scale (ATS) and RACGP Standards (5th edition).<br>
        All assessments should be reviewed by qualified medical professionals.<br>
        <strong>For medical emergencies in Australia, call 000 immediately.</strong>
    </p>
    <p style="font-size: 0.7em; margin-top: 10px; color: #808090;">
        Logging enabled - All interactions logged to logs/ directory for debugging and audit purposes.
    </p>
</div>
""", unsafe_allow_html=True)

app_logger.info("Page render complete")
