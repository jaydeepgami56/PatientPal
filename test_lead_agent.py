"""
Automated Test Script for Lead Agent Orchestrator
=================================================
Run automated tests on the Lead Agent system without needing Streamlit UI.

Usage:
    python test_lead_agent.py
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import required modules
from agents.medgemma_agent import create_medgemma_agent
from agents.txgemma_agent import create_txgemma_agent
from agents.derm_agent import create_derm_agent
from agents.cxr_agent import create_cxr_agent
from agents.pathology_agent import create_pathology_agent
from utils.orchestrator import LeadAgentOrchestrator
from langchain_openai import ChatOpenAI


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_test_result(test_name, passed, details=""):
    """Print test result with color"""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {test_name}")
    if details:
        print(f"      {details}")


def initialize_orchestrator():
    """Initialize the orchestrator with all agents"""
    print_header("INITIALIZING LEAD AGENT ORCHESTRATOR")

    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    hf_key = os.getenv("HUGGINGFACE_API_KEY")

    if not openai_key:
        print(f"{Colors.RED}ERROR: OPENAI_API_KEY not found in .env file{Colors.RESET}")
        sys.exit(1)

    if not hf_key:
        print(f"{Colors.YELLOW}WARNING: HUGGINGFACE_API_KEY not found (some agents may fail){Colors.RESET}")

    print(f"{Colors.GREEN}✓ API keys found{Colors.RESET}")

    # Create orchestrator LLM
    orchestrator_llm = ChatOpenAI(
        temperature=0.3,
        model_name="gpt-4o-mini",
        openai_api_key=openai_key
    )
    print(f"{Colors.GREEN}✓ Orchestrator LLM initialized{Colors.RESET}")

    # Create all specialist agents (don't initialize yet - lazy initialization)
    agents = {
        "MedGemma": create_medgemma_agent(),
        "TxGemma": create_txgemma_agent(),
        "Derm Foundation": create_derm_agent(),
        "CXR Foundation": create_cxr_agent(),
        "Pathology": create_pathology_agent()
    }
    print(f"{Colors.GREEN}✓ Created {len(agents)} specialist agents{Colors.RESET}")

    # Create orchestrator
    orchestrator = LeadAgentOrchestrator(agents=agents, llm=orchestrator_llm)
    print(f"{Colors.GREEN}✓ Orchestrator created successfully{Colors.RESET}")

    return orchestrator


def test_basic_routing(orchestrator):
    """Test basic routing logic"""
    print_header("TEST SUITE 1: BASIC ROUTING LOGIC")

    test_cases = [
        {
            "name": "TC-001: Route to MedGemma",
            "query": "What are the symptoms of Type 2 diabetes?",
            "expected_agent": "MedGemma",
            "expected_mode": "single"
        },
        {
            "name": "TC-002: Route to TxGemma",
            "query": "What are the treatment options for high blood pressure?",
            "expected_agent": "TxGemma",
            "expected_mode": "single"
        },
        {
            "name": "TC-003: Route to Pathology",
            "query": "Explain what a biopsy showing adenocarcinoma means",
            "expected_agent": "Pathology",
            "expected_mode": "single"
        }
    ]

    results = []

    for test in test_cases:
        try:
            # Analyze query (routing only, don't execute)
            routing = orchestrator.analyze_query(test["query"])

            # Check routing decision
            agent_match = routing.primary_agent == test["expected_agent"]
            mode_match = routing.execution_mode == test["expected_mode"]
            passed = agent_match and mode_match

            details = f"Routed to: {routing.primary_agent} ({routing.execution_mode})"
            if routing.confidence < 0.7:
                details += f" - Low confidence: {routing.confidence:.0%}"

            print_test_result(test["name"], passed, details)
            results.append(passed)

        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")
            results.append(False)

    return results


def test_emergency_detection(orchestrator):
    """Test emergency detection logic"""
    print_header("TEST SUITE 2: EMERGENCY DETECTION")

    test_cases = [
        {
            "name": "TC-301: Detect chest pain emergency",
            "query": "Severe chest pain, crushing sensation, difficulty breathing",
            "should_detect": True
        },
        {
            "name": "TC-302: Detect stroke emergency",
            "query": "Sudden facial droop, can't move left arm, speech slurred",
            "should_detect": True
        },
        {
            "name": "TC-304: Non-emergency headache",
            "query": "I've had a mild headache for 2 weeks",
            "should_detect": False
        }
    ]

    results = []

    for test in test_cases:
        try:
            routing = orchestrator.analyze_query(test["query"])

            is_emergency = routing.urgency_level == "emergency"
            passed = is_emergency == test["should_detect"]

            status = "EMERGENCY" if is_emergency else "ROUTINE"
            details = f"Detected as: {status}"
            if is_emergency:
                details += f" - Flags: {routing.safety_flags}"

            print_test_result(test["name"], passed, details)
            results.append(passed)

        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")
            results.append(False)

    return results


def test_multi_agent_detection(orchestrator):
    """Test multi-agent query detection"""
    print_header("TEST SUITE 3: MULTI-AGENT DETECTION")

    test_cases = [
        {
            "name": "TC-201: Detect multi-domain query",
            "query": "I have chest pain and a rash on my arms",
            "should_be_multi": True
        }
    ]

    results = []

    for test in test_cases:
        try:
            routing = orchestrator.analyze_query(test["query"])

            is_multi = len(routing.additional_agents) > 0 or routing.execution_mode in ["parallel", "sequential"]
            passed = is_multi == test["should_be_multi"]

            details = f"Mode: {routing.execution_mode}, Agents: {routing.primary_agent}"
            if routing.additional_agents:
                details += f" + {routing.additional_agents}"

            print_test_result(test["name"], passed, details)
            results.append(passed)

        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")
            results.append(False)

    return results


def test_full_orchestration(orchestrator):
    """Test full end-to-end orchestration (WARNING: This will call actual agents)"""
    print_header("TEST SUITE 4: FULL ORCHESTRATION (E2E)")

    print(f"{Colors.YELLOW}⚠️  WARNING: This test will initialize and call actual agents{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️  This may take time and consume API credits{Colors.RESET}")

    response = input("\nProceed with E2E tests? (y/n): ")
    if response.lower() != 'y':
        print(f"{Colors.YELLOW}Skipping E2E tests{Colors.RESET}")
        return []

    test_cases = [
        {
            "name": "TC-E2E-001: Full orchestration - Simple query",
            "query": "What is pneumonia?",
            "expected_agent": "MedGemma"
        }
    ]

    results = []

    for test in test_cases:
        try:
            print(f"\nExecuting: {test['query']}")
            start_time = datetime.now()

            # Full orchestration
            response = orchestrator.orchestrate(test["query"])

            processing_time = (datetime.now() - start_time).total_seconds()

            # Check result
            passed = not response.error and len(response.synthesized_output) > 0

            details = f"Time: {processing_time:.2f}s, Agents: {response.agents_consulted}"
            if response.error:
                details += f" - Error: {response.error}"

            print_test_result(test["name"], passed, details)

            # Print response preview
            if passed:
                preview = response.synthesized_output[:200] + "..." if len(response.synthesized_output) > 200 else response.synthesized_output
                print(f"      Response preview: {preview}\n")

            results.append(passed)

        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")
            results.append(False)

    return results


def test_image_requirement_detection(orchestrator):
    """Test detection of image requirements"""
    print_header("TEST SUITE 5: IMAGE REQUIREMENT DETECTION")

    test_cases = [
        {
            "name": "TC-103: Detect skin lesion needs image",
            "query": "Analyze this skin rash",
            "should_require_image": True
        },
        {
            "name": "TC-103: Detect chest X-ray needs image",
            "query": "What does this chest X-ray show?",
            "should_require_image": True
        },
        {
            "name": "TC-103: General query doesn't need image",
            "query": "What causes diabetes?",
            "should_require_image": False
        }
    ]

    results = []

    for test in test_cases:
        try:
            routing = orchestrator.analyze_query(test["query"])

            requires_image = routing.requires_image
            passed = requires_image == test["should_require_image"]

            details = f"Requires image: {requires_image}, Agent: {routing.primary_agent}"

            print_test_result(test["name"], passed, details)
            results.append(passed)

        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")
            results.append(False)

    return results


def print_summary(all_results):
    """Print test summary"""
    print_header("TEST SUMMARY")

    total = len(all_results)
    passed = sum(all_results)
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0

    print(f"Total Tests:  {total}")
    print(f"{Colors.GREEN}Passed:       {passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed:       {failed}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Pass Rate:    {pass_rate:.1f}%{Colors.RESET}\n")

    if pass_rate >= 90:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ EXCELLENT - System ready for use{Colors.RESET}")
    elif pass_rate >= 70:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ GOOD - Minor issues to address{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ NEEDS WORK - Critical issues found{Colors.RESET}")


def main():
    """Main test execution"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   LEAD AGENT ORCHESTRATOR - AUTOMATED TEST SUITE                  ║")
    print("║   Version 1.0                                                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    # Initialize
    try:
        orchestrator = initialize_orchestrator()
    except Exception as e:
        print(f"\n{Colors.RED}FATAL ERROR: Failed to initialize orchestrator{Colors.RESET}")
        print(f"{Colors.RED}{str(e)}{Colors.RESET}")
        sys.exit(1)

    # Run test suites
    all_results = []

    # Suite 1: Basic Routing
    results_1 = test_basic_routing(orchestrator)
    all_results.extend(results_1)

    # Suite 2: Emergency Detection
    results_2 = test_emergency_detection(orchestrator)
    all_results.extend(results_2)

    # Suite 3: Multi-Agent Detection
    results_3 = test_multi_agent_detection(orchestrator)
    all_results.extend(results_3)

    # Suite 4: Image Requirement Detection
    results_4 = test_image_requirement_detection(orchestrator)
    all_results.extend(results_4)

    # Suite 5: Full E2E (optional)
    results_5 = test_full_orchestration(orchestrator)
    all_results.extend(results_5)

    # Print summary
    print_summary(all_results)

    # Exit with appropriate code
    if sum(all_results) == len(all_results):
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed


if __name__ == "__main__":
    main()
