"""
UI Components and Custom CSS Styling for IntelliDecision AI
Provides modern Elegant Dark SaaS UI styling, responsive progress bars, message bubbles, KPI cards, badges, and cards.
"""

import streamlit as st
from typing import List, Dict, Any


def inject_chatgpt_css() -> None:
    """Injects custom CSS styling for the dark SaaS theme into Streamlit."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container background & spacing - Elegant Dark #0F172A */
    .stApp {
        background-color: #0f172a !important;
        color: #e2e8f0;
    }

    /* Sidebar custom styling - Deep Slate #020617 */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e293b !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    /* Custom Header Banner */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: #0b0f1a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    .app-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .app-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-weight: 600;
    }

    /* Step Navigation Bar - Sticky Header */
    .step-bar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        background: #020617;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }

    .step-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    .step-item.active {
        color: #818cf8;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .step-item.completed {
        color: #34d399;
    }

    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 6px;
        background: #1e293b;
        font-size: 0.75rem;
    }

    .step-item.active .step-number {
        background: #4f46e5;
        color: #ffffff;
    }

    .step-item.completed .step-number {
        background: #10b981;
        color: #ffffff;
    }

    /* KPI Cards Styling */
    .kpi-card {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.15rem 1.25rem;
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        border-color: #334155;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }

    .kpi-icon {
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .kpi-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 0.2rem;
        letter-spacing: -0.01em;
    }

    .kpi-subtext {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Cards & Panels - Slate #0B0F1A */
    .card-panel {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: rgba(99, 102, 241, 0.12);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.25);
    }

    /* Input fields styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #0b0f1a !important;
        border: 1px solid #1e293b !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* Streamlit Expander Dark Theme Styling */
    .stExpander {
        background-color: #0b0f1a !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
    }

    .stExpander [data-testid="stExpanderToggleIcon"] {
        color: #818cf8 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }

    /* Primary Indigo Button Override */
    .stButton > button[kind="primary"] {
        background: #4f46e5 !important;
        border: 1px solid #6366f1 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #4338ca !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    }

    /* Loading Animation Container */
    .loading-pulse-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2.5rem;
        background: #0b0f1a;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.15);
    }

    .loading-spinner-ring {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-top: 4px solid #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_app_header() -> None:
    """Renders the top branding header banner."""
    header_html = """
    <div class="app-header">
        <div>
            <h1 class="app-title">🧠 IntelliDecision AI</h1>
            <div class="app-subtitle">Autonomous Decision Intelligence Engine • Google Gemini 2.5 AI</div>
        </div>
        <div>
            <span class="badge-pill">Powered by Gemini 2.5</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_step_progress(current_step: int) -> None:
    """
    Renders step progress bar across the core decision intelligence stages.

    :param current_step: Current active stage index (1-5).
    """
    steps = [
        {"num": 1, "name": "1. Define Choice"},
        {"num": 2, "name": "2. Probing Q&A"},
        {"num": 3, "name": "3. Hidden Factors"},
        {"num": 4, "name": "4. Trade-Off Matrix"},
        {"num": 5, "name": "5. Decision Report"},
    ]

    items_html = ""
    for s in steps:
        step_class = "step-item"
        if s["num"] == current_step:
            step_class += " active"
        elif s["num"] < current_step:
            step_class += " completed"

        icon = "✓" if s["num"] < current_step else str(s["num"])
        items_html += f"""
        <div class="{step_class}">
            <span class="step-number">{icon}</span>
            <span>{s['name']}</span>
        </div>
        """

    progress_html = f"""
    <div class="step-bar-container">
        {items_html}
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)


def render_ai_message(content: str, title: str = "IntelliDecision AI") -> None:
    """
    Renders an AI message bubble formatted cleanly.

    :param content: Message text content.
    :param title: Sender header title.
    """
    html = f"""
    <div class="chat-bubble-ai">
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
            <div style="width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #6366f1, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 14px;">🧠</div>
            <strong style="font-size: 0.95rem; color: #f1f5f9;">{title}</strong>
        </div>
        <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
            {content}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_user_message(content: str, title: str = "Decision Maker") -> None:
    """
    Renders a user message bubble formatted cleanly.

    :param content: Message text content.
    :param title: Sender header title.
    """
    html = f"""
    <div class="chat-bubble-user">
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
            <div style="width: 28px; height: 28px; border-radius: 8px; background: #475569; display: flex; align-items: center; justify-content: center; font-size: 14px;">👤</div>
            <strong style="font-size: 0.95rem; color: #f8fafc;">{title}</strong>
        </div>
        <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.5;">
            {content}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
