"""
Agent Configuration Page
=========================
Configure and manage specialist healthcare AI agents.
Set API keys, model parameters, and agent preferences.
"""

import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv, set_key, find_dotenv

# Page configuration MUST be first
st.set_page_config(
    page_title="Agent Configuration",
    page_icon="⚙️",
    layout="wide"
)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'styles', 'app_style.css')
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize session state for agent configurations
if 'agent_configs' not in st.session_state:
    st.session_state.agent_configs = {
        'MedGemma': {
            'model_id': 'google/medgemma-7b',
            'enabled': True,
            'temperature': 0.7,
            'max_tokens': 512,
            'priority': 1
        },
        'TxGemma': {
            'model_id': 'google/txgemma-7b',
            'enabled': True,
            'temperature': 0.7,
            'max_tokens': 512,
            'priority': 1
        },
        'Path Foundation': {
            'model_id': 'google/path-foundation',
            'enabled': True,
            'temperature': 0.5,
            'max_tokens': 512,
            'priority': 1
        },
        'Derm Foundation': {
            'model_id': 'google/derm-foundation',
            'enabled': True,
            'temperature': 0.5,
            'max_tokens': 512,
            'priority': 1
        },
        'CXR Foundation': {
            'model_id': 'google/cxr-foundation',
            'enabled': True,
            'temperature': 0.5,
            'max_tokens': 512,
            'priority': 1
        }
    }

# Header
st.markdown('<h1 class="hero-title">⚙️ Agent Configuration</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Configure and manage your healthcare AI specialist agents</p>', unsafe_allow_html=True)

st.markdown("---")

# API Keys Info
st.info("""
**💡 API Keys Setup:** To use the specialist agents, you need to configure API keys in your `.env` file:
- **HUGGINGFACE_API_KEY**: Required for MedGemma, TxGemma, Path, Derm, and CXR Foundation models (Get it from https://huggingface.co/settings/tokens)
- **OPENAI_API_KEY**: Required for Triage Agent (Get it from https://platform.openai.com/api-keys)

Add these keys to the `.env` file in your project root directory.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Agent Configuration Section
st.markdown('<h2 class="section-title">🤖 Specialist Agent Settings</h2>', unsafe_allow_html=True)

for agent_name, config in st.session_state.agent_configs.items():
    with st.expander(f"{'✅' if config['enabled'] else '❌'} {agent_name}", expanded=False):
        col1, col2 = st.columns([2, 1])

        with col1:
            # Model ID
            new_model_id = st.text_input(
                "Model ID",
                value=config['model_id'],
                key=f"{agent_name}_model_id",
                help="Hugging Face model identifier"
            )

            # Temperature
            new_temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=config['temperature'],
                step=0.1,
                key=f"{agent_name}_temp",
                help="Controls randomness: 0 = deterministic, 2 = very random"
            )

            # Max Tokens
            new_max_tokens = st.number_input(
                "Max Tokens",
                min_value=128,
                max_value=2048,
                value=config['max_tokens'],
                step=128,
                key=f"{agent_name}_tokens",
                help="Maximum length of generated response"
            )

        with col2:
            # Enable/Disable
            new_enabled = st.toggle(
                "Enabled",
                value=config['enabled'],
                key=f"{agent_name}_enabled"
            )

            # Priority
            new_priority = st.selectbox(
                "Priority",
                options=[1, 2, 3, 4, 5],
                index=config['priority'] - 1,
                key=f"{agent_name}_priority",
                help="Higher priority agents are preferred when multiple agents can handle a query"
            )

            # Status indicator
            if config['enabled']:
                st.success("🟢 Active")
            else:
                st.warning("🔴 Inactive")

        # Update button
        if st.button(f"Update {agent_name}", key=f"{agent_name}_update"):
            st.session_state.agent_configs[agent_name] = {
                'model_id': new_model_id,
                'enabled': new_enabled,
                'temperature': new_temperature,
                'max_tokens': new_max_tokens,
                'priority': new_priority
            }
            st.success(f"✅ {agent_name} configuration updated!")
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Supervisor Agent Configuration
st.markdown('<h2 class="section-title">🎯 Supervisor Agent Settings</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #8b5cf6; margin-bottom: 15px;">Routing Configuration</h3>
        <p class="content-text" style="margin-bottom: 20px;">
            Configure how the Supervisor Agent routes queries to specialist agents.
        </p>
    </div>
    """, unsafe_allow_html=True)

    routing_mode = st.radio(
        "Routing Mode",
        options=["Keyword-Based (Fast)", "LLM-Based (Accurate)", "Hybrid"],
        index=0,
        help="Choose how queries are routed to specialist agents"
    )

    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Minimum confidence required for routing decision"
    )

    enable_multi_agent = st.checkbox(
        "Enable Multi-Agent Responses",
        value=False,
        help="Allow multiple agents to process the same query for comprehensive analysis"
    )

    if st.button("Save Supervisor Settings"):
        st.session_state.supervisor_config = {
            'routing_mode': routing_mode,
            'confidence_threshold': confidence_threshold,
            'enable_multi_agent': enable_multi_agent
        }
        st.success("✅ Supervisor configuration saved!")

st.markdown("<br>", unsafe_allow_html=True)

# System Status
st.markdown('<h2 class="section-title">📊 System Status</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

enabled_count = sum(1 for config in st.session_state.agent_configs.values() if config['enabled'])

with col1:
    st.metric("Active Agents", f"{enabled_count}/5")

with col2:
    st.metric("Total Configurations", "5")

with col3:
    st.metric("Routing Mode", "Keyword-Based")

with col4:
    st.metric("System Status", "🟢 Ready")

st.markdown("<br>", unsafe_allow_html=True)

# Export/Import Configuration
st.markdown('<h2 class="section-title">💾 Configuration Management</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Export Configuration", use_container_width=True):
        import json
        config_export = {
            'agent_configs': st.session_state.agent_configs,
            'timestamp': datetime.now().isoformat()
        }
        st.download_button(
            label="Download Configuration JSON",
            data=json.dumps(config_export, indent=2),
            file_name=f"agent_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col2:
    uploaded_file = st.file_uploader("📤 Import Configuration", type=['json'])
    if uploaded_file is not None:
        import json
        config_data = json.load(uploaded_file)
        if 'agent_configs' in config_data:
            st.session_state.agent_configs = config_data['agent_configs']
            st.success("✅ Configuration imported successfully!")
            st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #606080; border-top: 1px solid rgba(139, 92, 246, 0.2);">
    <p style="font-size: 12px;">⚙️ Agent Configuration | Securely manage your AI agents</p>
</div>
""", unsafe_allow_html=True)
