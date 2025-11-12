"""
Style Loader Utility
====================
Helper functions to load external CSS files into Streamlit apps
"""

import streamlit as st
import os


def load_css(file_path):
    """
    Load CSS from an external file and inject it into the Streamlit app.

    Args:
        file_path (str): Path to the CSS file (relative or absolute)

    Returns:
        None
    """
    try:
        # Normalize the path for Windows
        file_path = os.path.normpath(file_path)

        if not os.path.exists(file_path):
            st.error(f"❌ CSS file not found: {file_path}")
            st.info(f"Current working directory: {os.getcwd()}")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"❌ CSS file not found: {file_path}")
    except Exception as e:
        st.error(f"❌ Error loading CSS: {str(e)}")


def load_triage_agent_style():
    """
    Load the CSS for the triage agent application.
    Looks for triage_agent_style.css in the styles directory.

    Returns:
        None
    """
    # Get the base directory (parent of utils)
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except:
        base_dir = os.getcwd()

    css_path = os.path.join(base_dir, 'styles', 'triage_agent_style.css')


    load_css(css_path)


def load_app_style():
    """
    Load the landing page CSS for the main app.
    Looks for app_style.css in the styles directory.

    Returns:
        None
    """
    # Get the base directory (parent of utils)
    # First try using __file__, then fall back to current working directory
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except:
        base_dir = os.getcwd()

    css_path = os.path.join(base_dir, 'styles', 'app_style.css')

    

    load_css(css_path)


# Backwards compatibility aliases
def load_custom_css():
    """Alias for load_triage_agent_style() - kept for backwards compatibility"""
    load_triage_agent_style()


def load_landing_css():
    """Alias for load_app_style() - kept for backwards compatibility"""
    load_app_style()
