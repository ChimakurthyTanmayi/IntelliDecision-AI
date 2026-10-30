"""
Sidebar Component for IntelliDecision AI
Provides sidebar navigation, system status indicators, scenario templates, and reset controls.
"""

import streamlit as st
from typing import Optional
from services.gemini_service import GeminiService
from modules.mock_data import DECISION_TEMPLATES


def render_sidebar(gemini_service: Optional[GeminiService]) -> None:
    """
    Renders the sidebar navigation, system status, scenario templates, and controls.

    :param gemini_service: Optional GeminiService instance for checking configuration status.
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 38px; height: 38px; background: #4f46e5; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);">ID</div>
                <div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; tracking-tight: -0.02em;">IntelliDecision AI</div>
                    <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Decision Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Gemini Status Badge
        if gemini_service and gemini_service.is_configured():
            st.markdown(
                """
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.75rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 6px; color: #34d399; font-size: 0.75rem; font-weight: 700; margin-bottom: 1.25rem;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                    Gemini 2.5 Active
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.75rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 6px; color: #f87171; font-size: 0.75rem; font-weight: 700; margin-bottom: 1.25rem;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></span>
                    API Key Missing
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<hr style='border-color: #1e293b; margin: 0.5rem 0 1.25rem 0;'>", unsafe_allow_html=True)

        # Navigation Controls
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.step = "HOME"
                st.rerun()
        with col_nav2:
            history_len = len(st.session_state.get("history", []))
            if st.button(f"📜 History ({history_len})", use_container_width=True):
                st.session_state.step = "HISTORY"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Start New Decision / Reset Button
        if st.button("+ New Analysis", use_container_width=True, type="primary"):
            _reset_session_state()
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Preset Templates Section
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>Preset Scenarios</div>", unsafe_allow_html=True)

        template_choice = st.selectbox(
            "Select Scenario Template",
            options=["-- Choose Template --"] + list(DECISION_TEMPLATES.keys()),
            label_visibility="collapsed"
        )

        if template_choice != "-- Choose Template --":
            if st.button("Load Scenario", use_container_width=True):
                tmpl = DECISION_TEMPLATES[template_choice]
                opts_text = "\n".join([f"- {opt}" for opt in tmpl['options']])
                st.session_state.decision_input = f"Title: {tmpl['title']}\n\nCategory: {tmpl['category']}\n\nContext:\n{tmpl['description']}\n\nOptions Being Considered:\n{opts_text}"
                _reset_session_state(keep_input=True)
                st.rerun()

        st.markdown("<hr style='border-color: #1e293b; margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="font-size: 0.75rem; color: #475569; line-height: 1.5;">
                <strong style="color: #64748b;">System Architecture:</strong><br>
                • Google Gemini 2.5 Flash SDK<br>
                • Decision Parsing Engine<br>
                • Probing Question Synthesizer<br>
                • Multi-Criteria Trade-Off Engine
            </div>
            """,
            unsafe_allow_html=True
        )


def _reset_session_state(keep_input: bool = False) -> None:
    """
    Clears decision pipeline state to begin a fresh analysis.

    :param keep_input: If True, preserves decision_input value.
    """
    st.session_state.step = "HOME"
    if not keep_input:
        st.session_state.decision_input = ""
    st.session_state.parsed_decision = None
    st.session_state.questions = []
    st.session_state.user_answers = {}
    st.session_state.analysis_result = None
    st.session_state.final_report = None
