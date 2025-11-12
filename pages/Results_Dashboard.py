"""
Results Dashboard Page
=======================
Comprehensive dashboard for viewing multi-agent analysis results,
comparing agent responses, and tracking system performance.
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration MUST be first
st.set_page_config(
    page_title="Results Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'styles', 'app_style.css')
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Helper function to aggregate all agent histories
def get_all_agent_results():
    """Aggregate results from all agent histories"""
    results = []

    # MedGemma
    if 'medgemma_history' in st.session_state:
        for item in st.session_state.medgemma_history:
            results.append({
                'agent': 'MedGemma',
                'timestamp': item['timestamp'],
                'query': item['query'],
                'confidence': item.get('confidence', 0),
                'processing_time': item.get('processing_time', 0),
                'error': item.get('error', None)
            })

    # TxGemma
    if 'txgemma_history' in st.session_state:
        for item in st.session_state.txgemma_history:
            results.append({
                'agent': 'TxGemma',
                'timestamp': item['timestamp'],
                'query': item['query'],
                'confidence': item.get('confidence', 0),
                'processing_time': item.get('processing_time', 0),
                'error': item.get('error', None)
            })

    # CXR Foundation
    if 'cxr_history' in st.session_state:
        for item in st.session_state.cxr_history:
            results.append({
                'agent': 'CXR Foundation',
                'timestamp': item['timestamp'],
                'query': item.get('image_name', item['query']),
                'confidence': item.get('confidence', 0),
                'processing_time': item.get('processing_time', 0),
                'error': item.get('error', None)
            })

    # Derm Foundation
    if 'derm_history' in st.session_state:
        for item in st.session_state.derm_history:
            results.append({
                'agent': 'Derm Foundation',
                'timestamp': item['timestamp'],
                'query': item.get('image_name', item['query']),
                'confidence': item.get('confidence', 0),
                'processing_time': item.get('processing_time', 0),
                'error': item.get('error', None),
                'abcde_positive': item.get('abcde_positive', False)
            })

    # Path Foundation (from existing Pathology_agent.py)
    if 'pathology_history' in st.session_state:
        for item in st.session_state.pathology_history:
            results.append({
                'agent': 'Path Foundation',
                'timestamp': item.get('timestamp', datetime.now()),
                'query': item.get('query', 'Pathology query'),
                'confidence': item.get('confidence', 0),
                'processing_time': item.get('processing_time', 0),
                'error': item.get('error', None)
            })

    return results

# Header
st.markdown('<h1 class="hero-title">📊 Results Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Multi-Agent System Performance & Analytics</p>', unsafe_allow_html=True)

st.markdown("---")

# Get all results
all_results = get_all_agent_results()

if not all_results:
    st.info("📭 No results yet. Start using the specialist agents to see analytics here!")
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #8b5cf6;">Get Started</h3>
        <p class="content-text">
            Navigate to any specialist agent page (MedGemma, TxGemma, CXR Foundation, Derm Foundation, or Path Foundation)
            to process queries and generate analytics data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Create DataFrame for easier analysis
df = pd.DataFrame(all_results)

# Overview Metrics
st.markdown('<h2 class="section-title">📈 System Overview</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Queries", len(df))

with col2:
    st.metric("Active Agents", df['agent'].nunique())

with col3:
    avg_conf = df['confidence'].mean()
    st.metric("Avg. Confidence", f"{avg_conf:.1%}")

with col4:
    avg_time = df['processing_time'].mean()
    st.metric("Avg. Processing Time", f"{avg_time:.2f}s")

with col5:
    error_count = df['error'].notna().sum()
    st.metric("Errors", error_count)

st.markdown("<br>", unsafe_allow_html=True)

# Agent Usage Charts
st.markdown('<h2 class="section-title">🤖 Agent Usage Analytics</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Query distribution by agent
    agent_counts = df['agent'].value_counts()

    fig_pie = go.Figure(data=[go.Pie(
        labels=agent_counts.index,
        values=agent_counts.values,
        hole=0.4,
        marker=dict(colors=['#8b5cf6', '#ec4899', '#06b6d4', '#f59e0b', '#10b981'])
    )])

    fig_pie.update_layout(
        title="Query Distribution by Agent",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Agent performance comparison
    agent_stats = df.groupby('agent').agg({
        'confidence': 'mean',
        'processing_time': 'mean'
    }).reset_index()

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        name='Avg. Confidence',
        x=agent_stats['agent'],
        y=agent_stats['confidence'],
        marker_color='#8b5cf6'
    ))

    fig_bar.update_layout(
        title="Average Confidence by Agent",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(title='Confidence', tickformat='.0%'),
        xaxis=dict(title='Agent'),
        height=400
    )

    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Performance Over Time
st.markdown('<h2 class="section-title">⏱️ Performance Trends</h2>', unsafe_allow_html=True)

# Sort by timestamp
df_sorted = df.sort_values('timestamp')

col1, col2 = st.columns(2)

with col1:
    # Processing time over time
    fig_time = px.scatter(
        df_sorted,
        x='timestamp',
        y='processing_time',
        color='agent',
        title='Processing Time Over Time',
        labels={'processing_time': 'Processing Time (s)', 'timestamp': 'Timestamp'},
        color_discrete_sequence=['#8b5cf6', '#ec4899', '#06b6d4', '#f59e0b', '#10b981']
    )

    fig_time.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )

    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Confidence over time
    fig_conf = px.line(
        df_sorted,
        x='timestamp',
        y='confidence',
        color='agent',
        title='Confidence Trends',
        labels={'confidence': 'Confidence', 'timestamp': 'Timestamp'},
        color_discrete_sequence=['#8b5cf6', '#ec4899', '#06b6d4', '#f59e0b', '#10b981']
    )

    fig_conf.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(tickformat='.0%'),
        height=400
    )

    st.plotly_chart(fig_conf, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Detailed Agent Statistics
st.markdown('<h2 class="section-title">📋 Detailed Agent Statistics</h2>', unsafe_allow_html=True)

for agent_name in df['agent'].unique():
    agent_data = df[df['agent'] == agent_name]

    with st.expander(f"📊 {agent_name} Statistics ({len(agent_data)} queries)"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Queries Processed", len(agent_data))

        with col2:
            st.metric("Avg. Confidence", f"{agent_data['confidence'].mean():.1%}")

        with col3:
            st.metric("Avg. Processing Time", f"{agent_data['processing_time'].mean():.2f}s")

        with col4:
            error_rate = (agent_data['error'].notna().sum() / len(agent_data) * 100) if len(agent_data) > 0 else 0
            st.metric("Error Rate", f"{error_rate:.1f}%")

        # Recent queries
        st.markdown("**Recent Queries:**")
        recent = agent_data.nlargest(5, 'timestamp')[['timestamp', 'query', 'confidence', 'processing_time']]

        for _, row in recent.iterrows():
            st.markdown(f"""
            <div class="glass-card" style="margin: 10px 0; padding: 10px;">
                <p style="margin: 0; font-size: 12px; color: #a0a0c0;">
                    {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                </p>
                <p style="margin: 5px 0; color: white;">
                    {row['query'][:100]}{'...' if len(str(row['query'])) > 100 else ''}
                </p>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #8b5cf6;">
                    Confidence: {row['confidence']:.0%} | Time: {row['processing_time']:.2f}s
                </p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent Activity Timeline
st.markdown('<h2 class="section-title">🕒 Recent Activity</h2>', unsafe_allow_html=True)

recent_results = df.nlargest(10, 'timestamp')

for _, result in recent_results.iterrows():
    agent_color = {
        'MedGemma': '#8b5cf6',
        'TxGemma': '#ec4899',
        'CXR Foundation': '#06b6d4',
        'Derm Foundation': '#f59e0b',
        'Path Foundation': '#10b981'
    }.get(result['agent'], '#6366f1')

    st.markdown(f"""
    <div class="glass-card" style="margin: 15px 0; border-left: 4px solid {agent_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="margin: 0; font-size: 14px; color: {agent_color}; font-weight: bold;">
                    {result['agent']}
                </p>
                <p style="margin: 5px 0; color: white;">
                    {result['query'][:150]}{'...' if len(str(result['query'])) > 150 else ''}
                </p>
            </div>
            <div style="text-align: right; min-width: 200px;">
                <p style="margin: 0; font-size: 12px; color: #a0a0c0;">
                    {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                </p>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #8b5cf6;">
                    {result['confidence']:.0%} | {result['processing_time']:.2f}s
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Export Data
st.markdown('<h2 class="section-title">💾 Export Data</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("📥 Export Results to CSV", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"agent_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #606080; border-top: 1px solid rgba(139, 92, 246, 0.2);">
    <p style="font-size: 12px;">📊 Results Dashboard | Multi-Agent Performance Analytics</p>
</div>
""", unsafe_allow_html=True)
