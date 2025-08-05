#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for Zara Streamlit app.
Customized by Bushra for Zara Entrepreneur chatbot.
"""

import os
import streamlit as st
from openai import OpenAI

# Importing the tab-specific modules, including general_flow where the main LLM logic resides.
from tabs import I_WE, partners_interest, general_flow

def main():
    st.set_page_config(page_title="Zara | زارا", layout="centered")
    st.title("Zara || زارا - Family Support Assistant")

    # Initialize OpenAI API with secret key or environment variable
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found.")
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return

    # Initialize Groq API key, if needed for specific backend logic
    try:
        groq_key = st.secrets.get("GROQ_KEY")
        if not groq_key:
            raise ValueError("Groq API key not found.")
        os.environ["GROQ_API_KEY"] = groq_key
    except Exception as e:
        st.error(f"Failed to set Groq API key: {e}")
        return

    # Set default session state if not already present
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "o4-mini-2025-04-16"  # Model version can be swapped here
    if "messages" not in st.session_state:
        st.session_state["messages"] = {}

    # Each label corresponds to a custom conversation flow in its own file
    # Max: The actual prompt logic lives inside these modules (e.g., general_flow.py).
    label_map = {
        "Understanding Your Partner’s Interests/Communication Help ": partners_interest,
        "‘I We’ Statements ": I_WE,
        "General Flow ": general_flow  # <- This is the one where the base prompt logic is defined
    }

    # UI to select which flow to run
    choice = st.radio("Which topic do you want to try first?", list(label_map.keys()))

    # Dynamically load and run the chosen module
    module = label_map[choice]
    module.render(client)  # Max: This is where control passes to general_flow.py (or another tab).
    # That script defines what prompt is used, how user input is handled, and what gets sent to the LLM.

if __name__ == "__main__":
    main()
