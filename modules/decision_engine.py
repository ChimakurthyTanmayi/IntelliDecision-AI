"""
Decision Engine State Machine for IntelliDecision AI
Manages application session state, step progression, and pipeline transitions.
"""

import streamlit as st
import logging

logger = logging.getLogger("IntelliDecision.Engine")

# Stage constants
STAGE_DEFINE = 1
STAGE_QA = 2
STAGE_HIDDEN = 3
STAGE_TRADEOFFS = 4
STAGE_REPORT = 5

def init_session_state():
    """Initialize all Streamlit session state keys safely."""
    defaults = {
        "current_step": STAGE_DEFINE,
        "decision_title": "",
        "category": "Career & Professional",
        "description": "",
        "options_list": [],
        "initial_analysis": None,
        "followup_questions": [],
        "qna_responses": {},
        "hidden_factors": None,
        "tradeoffs": None,
        "final_report": None,
        "history": [],
    }

    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def reset_decision_state():
    """Reset session state to start a fresh decision analysis."""
    st.session_state.current_step = STAGE_DEFINE
    st.session_state.decision_title = ""
    st.session_state.description = ""
    st.session_state.options_list = []
    st.session_state.initial_analysis = None
    st.session_state.followup_questions = []
    st.session_state.qna_responses = {}
    st.session_state.hidden_factors = None
    st.session_state.tradeoffs = None
    st.session_state.final_report = None

def load_preset_template(template_data: dict):
    """Load a pre-configured scenario template into state."""
    st.session_state.current_step = STAGE_DEFINE
    st.session_state.decision_title = template_data.get("title", "")
    st.session_state.category = template_data.get("category", "Career & Professional")
    st.session_state.description = template_data.get("description", "")
    st.session_state.options_list = template_data.get("options", [])
    st.session_state.initial_analysis = None
    st.session_state.followup_questions = []
    st.session_state.qna_responses = {}
    st.session_state.hidden_factors = None
    st.session_state.tradeoffs = None
    st.session_state.final_report = None
