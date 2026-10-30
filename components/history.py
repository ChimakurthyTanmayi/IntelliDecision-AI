"""
History Component for IntelliDecision AI
Displays session decision history stored in Streamlit session_state,
allowing users to review, filter, and reopen previous decision reports.
"""

import streamlit as st
from typing import Dict, Any, List


def render_history_component() -> None:
    """
    Renders the Previous Decisions page displaying all decisions made during
    the current Streamlit session.
    """
    history: List[Dict[str, Any]] = st.session_state.get("history", [])

    # Header and Top Actions
    col_title, col_actions = st.columns([2.5, 1.5])

    with col_title:
        st.markdown(
            """
            <h1 style='font-size: 1.85rem; font-weight: 800; color: #f8fafc; margin: 0;'>
                📜 Previous Decisions
            </h1>
            <p style='font-size: 0.85rem; color: #64748b; font-weight: 600; text-transform: uppercase; margin-top: 0.25rem; letter-spacing: 0.05em;'>
                Session Memory • Review and Reopen Past Decision Syntheses
            </p>
            """,
            unsafe_allow_html=True
        )

    with col_actions:
        bcol1, bcol2 = st.columns(2)
        with bcol1:
            if st.button("+ New Decision", type="primary", use_container_width=True):
                st.session_state.step = "HOME"
                st.session_state.decision_input = ""
                st.session_state.parsed_decision = None
                st.session_state.questions = []
                st.session_state.user_answers = {}
                st.session_state.analysis_result = None
                st.session_state.final_report = None
                st.rerun()
        with bcol2:
            if history:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.history = []
                    st.rerun()

    st.markdown("<hr style='border-color: #1e293b; margin: 1.25rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    if not history:
        st.markdown(
            """
            <div class="card-panel" style="text-align: center; padding: 3rem 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                <h3 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">No Decisions Recorded Yet</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; max-width: 500px; margin: 0 auto 1.5rem auto;">
                    Decisions you analyze during this browser session will automatically be stored here for review and reopening.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚀 Start Your First Decision Analysis", type="primary"):
            st.session_state.step = "HOME"
            st.rerun()
        return

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="color: #94a3b8; font-size: 0.9rem; font-weight: 600;">
                Showing <span style="color: #818cf8; font-weight: 700;">{len(history)}</span> saved decisions in session memory
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render list of historical decisions
    for idx, item in enumerate(history):
        title = item.get("title", "Untitled Decision")
        timestamp = item.get("timestamp", "Recent")
        dec_type = item.get("decision_type", "General")
        risk_level = item.get("risk_level", "Medium")
        conf_score = item.get("confidence_score", 85)
        exec_summary = item.get("executive_summary", "No summary available.")

        # Risk level color badge
        risk_color = "#34d399" if "low" in risk_level.lower() else ("#f87171" if "high" in risk_level.lower() else "#fbbf24")

        with st.container():
            st.markdown(
                f"""
                <div class="card-panel" style="border-left: 4px solid #6366f1; margin-bottom: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; flex-wrap: wrap;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.3rem;">
                                <span class="badge-pill">{dec_type}</span>
                                <span style="font-size: 0.75rem; color: #64748b; font-weight: 600;">🕒 {timestamp}</span>
                            </div>
                            <h3 style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 0 0 0.5rem 0;">
                                {title}
                            </h3>
                        </div>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(255, 255, 255, 0.05); color: {risk_color}; border: 1px solid {risk_color}40; font-weight: 700;">
                                Risk: {risk_level}
                            </span>
                            <span style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); font-weight: 700;">
                                Confidence: {conf_score}%
                            </span>
                        </div>
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin-top: 0.75rem; border-top: 1px solid #1e293b; padding-top: 0.75rem;">
                        {exec_summary[:280]}...
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_btn1, col_btn2, _ = st.columns([1.5, 1, 3])

            with col_btn1:
                if st.button(f"📂 Reopen Report", key=f"open_hist_{idx}", type="primary", use_container_width=True):
                    # Load item back into current active session state
                    st.session_state.final_report = item.get("report", {})
                    st.session_state.parsed_decision = item.get("parsed_decision", {})
                    st.session_state.analysis_result = item.get("analysis_result", {})
                    st.session_state.user_answers = item.get("user_answers", {})
                    st.session_state.decision_input = item.get("decision_input", "")
                    st.session_state.step = "REPORT"
                    st.rerun()

            with col_btn2:
                if st.button(f"🗑️ Delete", key=f"del_hist_{idx}", use_container_width=True):
                    st.session_state.history.pop(idx)
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
