"""
Triage AI Agent - Futuristic Streamlit Landing Page
===================================================
A modern, visually stunning landing page for Triage AI Agent

Requirements:
pip install streamlit
"""

import streamlit as st
import time
import os

# Page configuration MUST be first
st.set_page_config(
    page_title="AI Agent - Intelligent Medical Assessment",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS from external file
def load_css_from_file():
    css_file = os.path.join(os.path.dirname(__file__), 'styles', 'app_style.css')
    with open(css_file, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css_from_file()

# Hero Section
st.markdown('<h1 class="hero-title">Intelligent Medical Triage<br/>Powered by AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Revolutionary AI-driven patient assessment that saves lives through instant, accurate triage decisions</p>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# What is a Triage AI Agent Section
st.markdown('<h2 class="section-title">What is a Triage AI Agent?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <div class="glass-card">
        <p class="content-text">
            A <strong>Triage AI Agent</strong> is an intelligent software system designed to quickly assess incoming requests,
            cases, or patients, prioritize them based on urgency, and direct them to the right next step.
        </p>
        <br>
        <p class="content-text">
            In <strong>healthcare</strong>, triage AI agents help medical staff determine how urgent a patient's condition is
            and whether they need immediate care or routine follow-up. In <strong>customer service or IT</strong>, these agents
            filter, classify, and route requests so humans spend less time sorting and more time solving.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Definition Box
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <div class="definition-box">
        <p class="definition-title">In Healthcare Context</p>
        <p class="content-text">
            A triage AI agent is an artificial intelligence system that helps healthcare providers quickly assess,
            categorize, and prioritize patients based on the urgency of their medical needs. It uses
            <strong>natural language processing (NLP)</strong>, medical knowledge bases, and predictive algorithms
            to support clinical decision-making, reduce waiting times, and ensure that critical patients get immediate attention.
        </p>
        <br>
        <p class="content-text" style="font-style: italic; color: #8b5cf6; font-size: 20px; font-weight: 600;">
            In simple terms: A triage AI agent acts like a digital nurse assistant that listens to symptoms,
            analyzes them, and routes patients to the right care, faster.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown('<h2 class="section-title">Key Capabilities</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <h3 class="feature-title">Advanced AI Analysis</h3>
        <p class="feature-description">Deep learning models trained on millions of medical cases provide instant,
        accurate symptom assessment and priority classification.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3 class="feature-title">Real-Time Processing</h3>
        <p class="feature-description">Lightning-fast triage decisions, ensuring critical patients receive
        immediate attention without delay.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h3 class="feature-title">Safety First Protocol</h3>
        <p class="feature-description">Built-in safety mechanisms automatically escalate life-threatening
        conditions with fail-safe emergency detection systems.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3 class="feature-title">Intelligent Prioritization</h3>
        <p class="feature-description">5-level triage system based on international medical standards
        (ESI, CTAS) for optimal resource allocation.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <h3 class="feature-title">Seamless Integration</h3>
        <p class="feature-description">FHIR-compliant API connects with existing EHR/EMR systems,
        enabling smooth workflow integration and data synchronization.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3 class="feature-title">Natural Language Understanding</h3>
        <p class="feature-description">Advanced NLP allows patients to describe symptoms in their own words,
        making the process intuitive and accessible.</p>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section
st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col2:
    st.markdown("""
    <div class="glass-card">
        <p class="content-text">
            The Triage AI Agent follows a systematic approach to ensure accurate and reliable patient assessment:
        </p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h3 class="step-title">Patient Input</h3>
        <p class="step-description">Patient describes symptoms through conversational interface or structured forms</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h3 class="step-title">AI Analysis</h3>
        <p class="step-description">Advanced NLP and medical knowledge graphs analyze symptoms and medical history</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h3 class="step-title">Risk Assessment</h3>
        <p class="step-description">Predictive models evaluate severity and assign priority level based on clinical protocols</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">4</div>
        <h3 class="step-title">Smart Routing</h3>
        <p class="step-description">Intelligent recommendations for appropriate care pathway and resource allocation</p>
    </div>
    """, unsafe_allow_html=True)

# Benefits Section
st.markdown('<h2 class="section-title">Why Use a Triage AI Agent?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="content-text">
            <p style="margin-bottom: 20px;">
                <strong style="font-size: 20px; color: #8b5cf6;">⏱️ Reduces Wait Times</strong><br>
                Patients are assessed instantly, allowing healthcare facilities to prioritize urgent cases and
                optimize resource allocation.
            </p>

            <p style="margin-bottom: 20px;">
                <strong style="font-size: 20px; color: #8b5cf6;">🎯 Improves Accuracy</strong><br>
                AI models trained on vast medical datasets can identify patterns and red flags that might be
                missed during busy periods.
            </p>

            <p style="margin-bottom: 20px;">
                <strong style="font-size: 20px; color: #8b5cf6;">👨‍⚕️ Supports Healthcare Workers</strong><br>
                By handling initial assessment, triage AI allows nurses and doctors to focus on treatment rather
                than administrative tasks.
            </p>

            <p>
                <strong style="font-size: 20px; color: #8b5cf6;">📈 Scalable & Consistent</strong><br>
                Can handle thousands of assessments simultaneously while maintaining consistent quality standards
                24/7 without fatigue.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# CTA Section
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style="font-size: 36px; font-weight: 800; color: #ffffff; margin-bottom: 20px;">
            Ready to Experience AI-Powered Triage?
        </h3>
        <p style="font-size: 18px; color: #a0a0c0; margin-bottom: 30px;">
            Discover how intelligent triage can transform your healthcare delivery
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Launch Triage Agent", use_container_width=True):
        st.balloons()
        st.success("Redirecting to Triage Agent interface...")
        time.sleep(1)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 40px 0; color: #606080; border-top: 1px solid rgba(139, 92, 246, 0.2);">
    <p style="font-size: 14px;">⚕️ Triage AI Agent - Next-Generation Medical Intelligence Platform</p>
    <p style="font-size: 12px; margin-top: 10px;">© 2025 All Rights Reserved. For educational and demonstration purposes.</p>
    <p style="font-size: 12px; margin-top: 5px; color: #ff6b6b;">
        ⚠️ This is a prototype system. Always consult healthcare professionals for medical advice.
    </p>
</div>
""", unsafe_allow_html=True)
