""" Utility and helper functions for managing database operations, 
processing data, rendering templates, and running experiments.

This module provides the following functions:

- get_env_variable:
    Fetch environment variables with a fallback mechanism.
- log_message: 
    Logs messages with different severity levels.

"""

# Import the required libraries and modules
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import streamlit as st


def get_env_variable(var_name, default_value=None):
    """ Retrieve the value of an environment variable with an optional 
    default, or raises an error.

    Args:
        var_name (str): The name of the environment variable to retrieve.
            default_value (any, optional): The value to return if the 
            environment variable is not set. Defaults to None.

    Returns:
        any: The value of the environment variable, or the default value 
            if the environment variable is not set.

    Raises:
        EnvironmentError: If the environment variable is not set and no 
            default value is provided.
    """
    value = os.getenv(var_name, default_value)
    if value is None:
        log_message("error", f"Environment variable {var_name} not found")
        if default_value is None:
            raise EnvironmentError(
                f"Missing mandatory environment variable: {var_name}"
            )
    return value


def log_message(level, message):
    """ Log a message using Streamlit's log functions based on the level.

    Args:
        level (str): Log level ('error', 'warning', 'info').
        message (str): Message to log.
        
    Returns:
        None
    """
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)
    elif level == "success":
        st.success(message)
    else:
        st.write(message)


def clear_all_caches():
    """ Clear all caches in the application."""
    st.cache_data.clear()
    st.cache_resource.clear()









        