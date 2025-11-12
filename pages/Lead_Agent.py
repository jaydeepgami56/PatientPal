"""
Lead Agent - Intelligent Medical Chatbot
=========================================
AI-powered medical chatbot that routes conversations to specialist agents.
Conversational interface with context-aware multi-agent orchestration.
"""

import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import io

# Page configuration MUST be first
st.set_page_config(
    page_title="Lead Agent - Medical Chatbot",
    page_icon="🧠",
    layout="wide"
)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Import all agent modules
from agents.medgemma_agent import create_medgemma_agent
from agents.txgemma_agent import create_txgemma_agent
from agents.derm_agent import create_derm_agent
from agents.cxr_agent import create_cxr_agent
from agents.pathology_agent import create_pathology_agent

# Import orchestrator and utilities
from utils.orchestrator import LeadAgentOrchestrator
from utils.agent_base import AgentConfig
from langchain_openai import ChatOpenAI

# Load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'styles', 'app_style.css')
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# ============================================================================
# INITIALIZE ORCHESTRATOR & AGENTS
# ============================================================================

@st.cache_resource
def initialize_orchestrator():
    """
    Initialize the Lead Agent Orchestrator with all specialist agents
    """
    # Check for OpenAI API key (for orchestrator LLM)
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        st.error("❌ OPENAI_API_KEY not found in .env file. Required for Lead Agent orchestration.")
        st.stop()

    # Create orchestrator LLM (for routing and synthesis)
    orchestrator_llm = ChatOpenAI(
        temperature=0.3,  # Lower temperature for more consistent routing
        model_name="gpt-4o-mini",
        openai_api_key=openai_key
    )

    # Create all specialist agents
    agents = {
        "MedGemma": create_medgemma_agent(),
        "TxGemma": create_txgemma_agent(),
        "Derm Foundation": create_derm_agent(),
        "CXR Foundation": create_cxr_agent(),
        "Pathology": create_pathology_agent()
    }

    # Create orchestrator
    orchestrator = LeadAgentOrchestrator(agents=agents, llm=orchestrator_llm)

    return orchestrator


# Initialize orchestrator
try:
    orchestrator = initialize_orchestrator()
except Exception as e:
    st.error(f"❌ Failed to initialize orchestrator: {str(e)}")
    st.stop()

# Initialize session state for chatbot
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'show_routing_details' not in st.session_state:
    st.session_state.show_routing_details = False  # Default off for cleaner chat

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = {}

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="hero-title">🧠 Lead Agent - Medical Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Your intelligent medical assistant. Ask me anything about health, symptoms, treatments, or upload images for analysis.</p>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR - CHATBOT STATUS
# ============================================================================

with st.sidebar:
    st.title("💬 Chat Status")
    st.markdown("---")

    # Agent availability
    st.markdown("### 🤖 Available Specialists")
    agent_status = orchestrator.get_agent_status()

    agents_initialized = sum(1 for status in agent_status.values() if status)
    total_agents = len(agent_status)

    st.metric("Active Specialists", f"{agents_initialized}/{total_agents}")

    with st.expander("View Agent Details"):
        for agent_name, is_initialized in agent_status.items():
            status_icon = "🟢" if is_initialized else "⚪"
            st.markdown(f"{status_icon} **{agent_name}**")

    st.markdown("---")

    # Conversation statistics
    st.markdown("### 📊 Conversation Stats")
    memory = orchestrator.get_memory()
    stats = memory.get_orchestration_stats()

    message_count = len(st.session_state.chat_messages)
    st.metric("Messages", message_count)
    st.metric("Queries Processed", stats.get("total_queries", 0))

    if stats.get("agents_used"):
        st.markdown("**Specialists Consulted:**")
        for agent in stats["agents_used"]:
            st.markdown(f"• {agent}")

    st.markdown("---")

    # Settings
    st.markdown("### ⚙️ Settings")

    st.session_state.show_routing_details = st.checkbox(
        "Show routing details",
        value=st.session_state.show_routing_details,
        help="Display which agents were consulted for each response"
    )

    # Clear conversation button
    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.uploaded_images = {}
        orchestrator.get_memory().clear_conversation()
        st.success("Conversation cleared!")
        st.rerun()

    # Quick Actions
    st.markdown("---")
    st.markdown("### 💡 Quick Actions")

    example_queries = [
        "What is diabetes?",
        "Symptoms of flu",
        "Treatment for high blood pressure"
    ]

    st.markdown("**Example queries:**")
    for example in example_queries:
        if st.button(f"📝 {example}", key=f"example_{example}", use_container_width=True):
            # Add to chat input by setting a session state variable
            st.session_state.pending_message = example
            st.rerun()

# ============================================================================
# WELCOME MESSAGE
# ============================================================================

if len(st.session_state.chat_messages) == 0:
    # Display welcome message
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #8b5cf6; margin-bottom: 15px;">👋 Welcome to Lead Agent Medical Chatbot</h3>
        <p class="content-text">
            I'm your intelligent medical assistant powered by multiple specialist AI agents. I can help you with:
        </p>
        <br>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <p class="content-text" style="font-size: 14px;">
                    <strong>🩺 General Medical Questions</strong><br>
                    Ask about symptoms, conditions, diseases
                </p>
            </div>
            <div>
                <p class="content-text" style="font-size: 14px;">
                    <strong>💊 Treatment Recommendations</strong><br>
                    Learn about medications and therapies
                </p>
            </div>
            <div>
                <p class="content-text" style="font-size: 14px;">
                    <strong>🔬 Image Analysis</strong><br>
                    Upload skin lesions or chest X-rays
                </p>
            </div>
            <div>
                <p class="content-text" style="font-size: 14px;">
                    <strong>📋 Pathology Reports</strong><br>
                    Help understand biopsy results
                </p>
            </div>
        </div>
        <br>
        <p class="content-text" style="font-size: 13px; color: #a0a0c0;">
            💡 <em>I automatically route your questions to the most appropriate specialist. Just type naturally!</em>
        </p>
        <br>
        <p class="content-text" style="font-size: 12px; color: #ff6b6b;">
            ⚠️ <strong>Important:</strong> I'm for informational purposes only. Always consult qualified healthcare professionals for medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# CHAT INTERFACE
# ============================================================================

# Display chat history
for idx, message in enumerate(st.session_state.chat_messages):
    with st.chat_message(message["role"]):
        # Display message content
        st.markdown(message["content"])

        # Display image if attached
        if "image" in message and message["image"] is not None:
            st.image(message["image"], caption="Uploaded Image", width=300)

        # Display routing info if available and enabled
        if st.session_state.show_routing_details and "routing_info" in message:
            with st.expander("🔍 Routing Details"):
                routing = message["routing_info"]
                st.markdown(f"**Agent(s):** {routing.get('agents', 'N/A')}")
                st.markdown(f"**Mode:** {routing.get('mode', 'N/A')}")
                st.markdown(f"**Confidence:** {routing.get('confidence', 'N/A')}")
                st.markdown(f"**Time:** {routing.get('time', 'N/A')}")

# ============================================================================
# IMAGE UPLOAD (Before chat input)
# ============================================================================

st.markdown("---")
uploaded_file = st.file_uploader(
    "📎 Attach Image (Optional - for skin or X-ray analysis)",
    type=['png', 'jpg', 'jpeg'],
    help="Upload if you need dermatological or radiological image analysis",
    key="image_uploader"
)

# Preview uploaded image
current_image = None
if uploaded_file is not None:
    current_image = Image.open(uploaded_file)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(current_image, caption="Image ready to send", use_container_width=True)

# ============================================================================
# CHAT INPUT
# ============================================================================

# Check if there's a pending message from quick actions
if 'pending_message' in st.session_state:
    user_input = st.session_state.pending_message
    del st.session_state.pending_message
else:
    # Chat input
    user_input = st.chat_input("Type your medical question here... (e.g., 'What causes diabetes?')")

# ============================================================================
# PROCESS USER INPUT
# ============================================================================

if user_input:
    # Add user message to chat
    user_message = {
        "role": "user",
        "content": user_input,
        "image": current_image,
        "timestamp": datetime.now()
    }
    st.session_state.chat_messages.append(user_message)

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
        if current_image:
            st.image(current_image, caption="Uploaded Image", width=300)

    # Prepare context for orchestrator
    context = {}
    if current_image is not None:
        context['image'] = current_image
        context['has_image'] = True
        # Detect image type from query
        query_lower = user_input.lower()
        if any(word in query_lower for word in ['skin', 'lesion', 'rash', 'mole', 'dermatology', 'derm']):
            context['image_type'] = 'dermatology'
        elif any(word in query_lower for word in ['chest', 'xray', 'x-ray', 'lung', 'cxr', 'thorax']):
            context['image_type'] = 'chest_xray'
    else:
        context['has_image'] = False

    # Display assistant thinking message
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing your question and consulting specialists..."):
            try:
                # Orchestrate!
                response = orchestrator.orchestrate(user_input, context)

                # Prepare assistant message
                if response.error:
                    assistant_content = f"❌ I encountered an error: {response.error}\n\nPlease try rephrasing your question or check if images are properly uploaded."
                else:
                    assistant_content = response.synthesized_output

                # Prepare routing info
                routing_info = None
                if response.routing_decision:
                    agents_consulted = ", ".join(response.agents_consulted) if response.agents_consulted else "None"
                    routing_info = {
                        "agents": agents_consulted,
                        "mode": response.routing_decision.execution_mode,
                        "confidence": f"{response.routing_decision.confidence:.0%}",
                        "time": f"{response.processing_time:.2f}s",
                        "urgency": response.routing_decision.urgency_level
                    }

                # Display response
                st.markdown(assistant_content)

                # Display routing info if enabled
                if st.session_state.show_routing_details and routing_info:
                    with st.expander("🔍 Routing Details"):
                        st.markdown(f"**Agent(s):** {routing_info['agents']}")
                        st.markdown(f"**Mode:** {routing_info['mode']}")
                        st.markdown(f"**Confidence:** {routing_info['confidence']}")
                        st.markdown(f"**Processing Time:** {routing_info['time']}")

                        # Show urgency if not routine
                        if routing_info['urgency'] != 'routine':
                            urgency_icon = "🚨" if routing_info['urgency'] == "emergency" else "⚠️"
                            st.markdown(f"**Urgency:** {urgency_icon} {routing_info['urgency'].upper()}")

                # Add assistant message to chat history
                assistant_message = {
                    "role": "assistant",
                    "content": assistant_content,
                    "routing_info": routing_info,
                    "timestamp": datetime.now()
                }
                st.session_state.chat_messages.append(assistant_message)

            except Exception as e:
                error_content = f"❌ An unexpected error occurred: {str(e)}\n\nPlease try again or rephrase your question."
                st.markdown(error_content)

                # Add error to chat history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_content,
                    "timestamp": datetime.now()
                })

    # Rerun to update the chat display
    st.rerun()

# ============================================================================
# HELPFUL TIPS (shown when no messages)
# ============================================================================

if len(st.session_state.chat_messages) == 0:
    st.markdown("""
    <div class="glass-card" style="margin-top: 20px;">
        <h4 style="color: #8b5cf6; margin-bottom: 10px;">💡 Tips for Best Results</h4>
        <ul class="content-text" style="font-size: 14px; line-height: 1.8;">
            <li><strong>Be specific:</strong> Instead of "I feel bad", try "I have a headache for 3 days with nausea"</li>
            <li><strong>Mention image type:</strong> When uploading, say "analyze this skin rash" or "interpret this chest X-ray"</li>
            <li><strong>Ask follow-ups:</strong> I remember our conversation, so you can ask "What about treatment for that?"</li>
            <li><strong>Multiple concerns:</strong> You can ask about multiple things, I'll consult multiple specialists if needed</li>
            <li><strong>Emergency?</strong> If you're experiencing severe symptoms like chest pain or difficulty breathing, call 000 immediately!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #606080; border-top: 1px solid rgba(139, 92, 246, 0.2);">
    <p style="font-size: 12px;">🧠 Lead Agent Medical Chatbot | Powered by Multi-Agent AI Orchestration</p>
    <p style="font-size: 10px; margin-top: 5px; color: #a0a0c0;">
        Using hybrid Anthropic + AWS Agent Squad architecture
    </p>
    <p style="font-size: 11px; margin-top: 10px; color: #ff6b6b;">
        ⚠️ For medical emergencies in Australia, call 000 immediately
    </p>
</div>
""", unsafe_allow_html=True)
