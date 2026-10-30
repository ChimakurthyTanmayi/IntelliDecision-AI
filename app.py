"""
IntelliDecision AI - Main Application Entry Point
Connects GeminiService, DecisionParser, QuestionGenerator, DecisionAnalyzer, and ReportGenerator
into an executive-grade Streamlit Decision Intelligence Platform.
"""

import streamlit as st
import logging
from typing import Tuple, Optional

from modules.ui_components import inject_chatgpt_css
from services.gemini_service import GeminiService
from services.decision_parser import DecisionParser
from services.question_generator import QuestionGenerator
from services.decision_analyzer import DecisionAnalyzer
from services.report_generator import ReportGenerator

from components.sidebar import render_sidebar
from components.home import render_home_component
from components.report import render_report_component
from components.history import render_history_component

logger = logging.getLogger("IntelliDecision.App")

# Page Configuration
st.set_page_config(
    page_title="IntelliDecision AI - Strategic Decision Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Custom Elegant Dark Theme Styling
inject_chatgpt_css()


@st.cache_resource
def init_services() -> Tuple[
    Optional[GeminiService],
    DecisionParser,
    QuestionGenerator,
    DecisionAnalyzer,
    ReportGenerator
]:
    """
    Initializes and caches core AI services using Streamlit resource caching.

    :return: Tuple containing service instances (gemini_service, decision_parser, question_generator, decision_analyzer, report_generator).
    """
    try:
        gemini_service = GeminiService()
    except Exception as e:
        logger.warning(f"GeminiService initialization warning: {e}")
        gemini_service = None

    decision_parser = DecisionParser(gemini_service)
    question_generator = QuestionGenerator(gemini_service)
    decision_analyzer = DecisionAnalyzer(gemini_service)
    report_generator = ReportGenerator()

    return gemini_service, decision_parser, question_generator, decision_analyzer, report_generator


# Initialize Cached Services
gemini_service, decision_parser, question_generator, decision_analyzer, report_generator = init_services()

# Session State Initialization
if "step" not in st.session_state:
    st.session_state.step = "HOME"  # HOME | QUESTIONS | REPORT
if "decision_input" not in st.session_state:
    st.session_state.decision_input = ""
if "parsed_decision" not in st.session_state:
    st.session_state.parsed_decision = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "history" not in st.session_state:
    st.session_state.history = []

# Render Sidebar Navigation & Status
render_sidebar(gemini_service)

# Header Banner
st.markdown(
    """
    <div class="app-header">
        <div>
            <h1 class="app-title">🧠 IntelliDecision AI</h1>
            <div class="app-subtitle">Executive Decision Intelligence Platform • Google Gemini 2.5 AI</div>
        </div>
        <div style="font-size: 0.8rem; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); padding: 0.4rem 0.8rem; border-radius: 8px; color: #a5b4fc; font-weight: 700;">
            PROTOTYPE v2.5
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# API Key Missing Warning Banner
if not gemini_service or not gemini_service.is_configured():
    st.warning(
        "⚠️ **GEMINI_API_KEY environment variable is not configured.**\n\n"
        "Please add your `GEMINI_API_KEY` to the `.env` file or environment secrets to enable full Gemini AI decision synthesis."
    )

# Main Application Router
current_step = st.session_state.get("step", "HOME")

if current_step in ["HOME", "QUESTIONS"]:
    render_home_component(
        gemini_service=gemini_service,
        decision_parser=decision_parser,
        question_generator=question_generator,
        decision_analyzer=decision_analyzer,
        report_generator=report_generator
    )
elif current_step == "REPORT":
    render_report_component(
        report=st.session_state.get("final_report", {}),
        raw_analysis=st.session_state.get("analysis_result", {})
    )
elif current_step == "HISTORY":
    render_history_component()
