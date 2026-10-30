"""
Home Component for IntelliDecision AI
Handles Step 1 (Decision Context Input) and Step 2 (Clarification Q&A)
with modern SaaS UI components and loading indicators.
"""

import streamlit as st
from typing import Dict, Any, List
from services.gemini_service import GeminiService
from services.decision_parser import DecisionParser
from services.question_generator import QuestionGenerator
from services.decision_analyzer import DecisionAnalyzer
from services.report_generator import ReportGenerator

# UI Constants
STEP_HOME: str = "HOME"
STEP_QUESTIONS: str = "QUESTIONS"
STEP_REPORT: str = "REPORT"


def render_home_component(
    gemini_service: GeminiService,
    decision_parser: DecisionParser,
    question_generator: QuestionGenerator,
    decision_analyzer: DecisionAnalyzer,
    report_generator: ReportGenerator
) -> None:
    """
    Main home view controller managing decision entry and dynamic follow-up Q&A flow.

    :param gemini_service: GeminiService instance.
    :param decision_parser: DecisionParser service.
    :param question_generator: QuestionGenerator service.
    :param decision_analyzer: DecisionAnalyzer service.
    :param report_generator: ReportGenerator service.
    """
    step: str = st.session_state.get("step", STEP_HOME)

    # Step progress indicator banner
    _render_step_bar(step)

    if step == STEP_HOME:
        _render_step_1_input(decision_parser, question_generator)
    elif step == STEP_QUESTIONS:
        _render_step_2_questions(decision_analyzer, report_generator)


def _render_step_bar(current_step: str) -> None:
    """
    Displays sticky step navigation bar indicating user progression.

    :param current_step: Current active application step ("HOME", "QUESTIONS", or "REPORT").
    """
    step1_active = "active" if current_step == STEP_HOME else "completed"
    step2_active = "active" if current_step == STEP_QUESTIONS else ("completed" if current_step == STEP_REPORT else "")
    step3_active = "active" if current_step == STEP_REPORT else ""

    st.markdown(
        f"""
        <div class="step-bar-container">
            <div class="step-item {step1_active}">
                <div class="step-number">1</div>
                <span>Decision Context</span>
            </div>
            <div style="color: #334155;">→</div>
            <div class="step-item {step2_active}">
                <div class="step-number">2</div>
                <span>Clarification Q&A</span>
            </div>
            <div style="color: #334155;">→</div>
            <div class="step-item {step3_active}">
                <div class="step-number">3</div>
                <span>Executive Analysis</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _render_step_1_input(decision_parser: DecisionParser, question_generator: QuestionGenerator) -> None:
    """
    Renders Step 1: Decision Context Input Form.

    :param decision_parser: DecisionParser service.
    :param question_generator: QuestionGenerator service.
    """
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.75rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">
                What decision are you trying to make?
            </h2>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin: 0;">
                Describe your strategic dilemma, career choice, investment option, or operational decision in plain language.
                Our Gemini AI engine will parse the core dilemma and synthesize probing clarification questions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Main text area input
    default_text = st.session_state.get("decision_input", "")
    user_text = st.text_area(
        "Describe your decision in detail:",
        value=default_text,
        height=180,
        placeholder="e.g. Should I accept a Senior AI Architect role at a Series B AI startup ($180k salary + 0.5% equity) or stay as a Principal Engineer at a stable enterprise software company ($220k total comp)? I value career growth and ownership, but I have a family and 6 months of liquid savings...",
        key="main_decision_text_input"
    )

    # Save to session state
    st.session_state.decision_input = user_text

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("Analyze Decision →", type="primary", use_container_width=True):
            if not user_text.strip():
                st.error("Please enter a decision description or select a preset scenario from the sidebar.")
                return

            status_box = st.empty()
            status_box.markdown(
                """
                <div class="loading-pulse-container">
                    <div class="loading-spinner-ring"></div>
                    <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Gemini AI is analyzing decision structure...</div>
                    <div style="font-size: 0.85rem; color: #818cf8; margin-top: 0.3rem;">Deconstructing constraints, risks, and option pathways</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            try:
                # Parse raw decision text
                parsed = decision_parser.parse_decision(user_text)
                st.session_state.parsed_decision = parsed

                status_box.markdown(
                    """
                    <div class="loading-pulse-container">
                        <div class="loading-spinner-ring"></div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Generating personalized follow-up questions...</div>
                        <div style="font-size: 0.85rem; color: #a855f7; margin-top: 0.3rem;">Synthesizing financial, lifestyle, and risk probing factors</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Generate probing follow-up questions
                questions = question_generator.generate_questions(parsed)
                st.session_state.questions = questions

                # Advance step to QUESTIONS
                st.session_state.step = STEP_QUESTIONS
                st.rerun()

            except Exception as e:
                status_box.empty()
                st.error(f"Error parsing decision context: {str(e)}")

    with col2:
        if st.button("Clear Input", use_container_width=True):
            st.session_state.decision_input = ""
            st.rerun()

    # Feature info cards
    st.markdown("<br>", unsafe_allow_html=True)
    _render_info_cards()


def _render_step_2_questions(decision_analyzer: DecisionAnalyzer, report_generator: ReportGenerator) -> None:
    """
    Renders Step 2: Dynamic Follow-up Clarification Q&A Form.

    :param decision_analyzer: DecisionAnalyzer service.
    :param report_generator: ReportGenerator service.
    """
    parsed: Dict[str, Any] = st.session_state.get("parsed_decision", {})
    questions: List[Dict[str, Any]] = st.session_state.get("questions", [])

    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">
                Clarification & Constraint Discovery
            </h2>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                To generate a highly tailored recommendation, answer these probing follow-up questions derived from your context.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show Parsed Context Overview
    if parsed:
        with st.expander("🔍 View Extracted Decision Context", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Category:** {parsed.get('decision_type', 'General')}")
                st.markdown(f"**Risk Level:** {parsed.get('risk_level', 'Medium')}")
            with c2:
                st.markdown(f"**Timeline:** {parsed.get('timeline', 'Immediate')}")
                st.markdown(f"**Primary Goal:** {parsed.get('primary_goal', 'Optimized decision')}")
            with c3:
                options = parsed.get("possible_options", [])
                st.markdown(f"**Options:** {', '.join(options) if options else 'Multiple paths'}")
                st.markdown(f"**Stakeholders:** {', '.join(parsed.get('stakeholders', ['Self']))}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Q&A Form
    with st.form("followup_questions_form"):
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1rem;'>Follow-Up Questions</h3>", unsafe_allow_html=True)

        for q in questions:
            q_id = q.get("id", 1)
            q_text = q.get("question", "")
            q_cat = q.get("category", "General")
            q_type = str(q.get("type", "text")).lower()
            q_importance = q.get("importance", "Medium")

            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 1.25rem; margin-bottom: 0.4rem;">
                    <span style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Q{q_id}. {q_text}</span>
                    <span class="badge-pill">{q_cat} • {q_importance} Priority</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            input_key = f"q_input_{q_id}"
            if q_type in ["slider", "scale"]:
                st.slider(
                    f"Rating for Q{q_id}",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key=input_key,
                    label_visibility="collapsed"
                )
            elif q_type == "number":
                st.number_input(
                    f"Number for Q{q_id}",
                    value=0,
                    step=1,
                    key=input_key,
                    label_visibility="collapsed"
                )
            elif q_type in ["select", "selectbox"]:
                st.selectbox(
                    f"Select for Q{q_id}",
                    options=["High Priority / Critical", "Moderate / Secondary", "Low Priority / Optional", "Not Applicable"],
                    key=input_key,
                    label_visibility="collapsed"
                )
            elif q_type in ["choice", "radio"]:
                st.radio(
                    f"Choice for Q{q_id}",
                    options=["Strongly Agree / Critical", "Somewhat Agree", "Neutral / Undecided", "Somewhat Disagree", "Strongly Disagree"],
                    key=input_key,
                    label_visibility="collapsed"
                )
            else:  # default text input
                st.text_input(
                    f"Response for Q{q_id}",
                    placeholder="Type your response here...",
                    key=input_key,
                    label_visibility="collapsed"
                )

            st.markdown("<hr style='border-color: #1e293b; margin: 1rem 0;'>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_submit, col_back = st.columns([2, 1])

        with col_submit:
            submitted = st.form_submit_button("Synthesize Executive Analysis →", type="primary", use_container_width=True)

        with col_back:
            back_clicked = st.form_submit_button("← Back to Decision Text", use_container_width=True)

    if back_clicked:
        st.session_state.step = STEP_HOME
        st.rerun()

    if submitted:
        # Collect answers cleanly from session_state keys
        answers: Dict[str, Any] = {}
        for q in questions:
            q_id = q.get("id", 1)
            q_text = q.get("question", "")
            q_cat = q.get("category", "General")
            input_key = f"q_input_{q_id}"
            user_ans = st.session_state.get(input_key, "")

            answers[f"Q{q_id}_{q_cat}"] = {
                "question": q_text,
                "answer": user_ans,
                "category": q_cat
            }

        st.session_state.user_answers = answers

        status_box = st.empty()
        status_box.markdown(
            """
            <div class="loading-pulse-container">
                <div class="loading-spinner-ring"></div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Gemini AI is performing multi-attribute decision synthesis...</div>
                <div style="font-size: 0.85rem; color: #38bdf8; margin-top: 0.3rem;">Evaluating trade-offs, risks, and second-order consequences</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        try:
            # Perform Decision Analysis
            analysis_res = decision_analyzer.analyze(parsed, answers)
            st.session_state.analysis_result = analysis_res

            status_box.markdown(
                """
                <div class="loading-pulse-container">
                    <div class="loading-spinner-ring"></div>
                    <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Formatting Executive Decision Report...</div>
                    <div style="font-size: 0.85rem; color: #34d399; margin-top: 0.3rem;">Building dashboard metrics and PDF exports</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Generate Executive Report
            title_summary = parsed.get("summary", "Executive Decision Report")
            report = report_generator.generate_report(analysis_res, decision_title=title_summary)
            st.session_state.final_report = report

            # Save Decision to Session History
            import datetime
            history = st.session_state.get("history", [])
            history_entry = {
                "id": f"dec_{len(history) + 1}_{int(datetime.datetime.now().timestamp())}",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "title": report.get("title", title_summary),
                "decision_type": parsed.get("decision_type", "General"),
                "risk_level": parsed.get("risk_level", "Medium"),
                "confidence_score": report.get("confidence_score", 85),
                "executive_summary": report.get("executive_summary", ""),
                "report": report,
                "parsed_decision": parsed,
                "analysis_result": analysis_res,
                "user_answers": answers,
                "decision_input": st.session_state.get("decision_input", "")
            }
            history.insert(0, history_entry)
            st.session_state.history = history

            # Advance to step 3 (REPORT)
            st.session_state.step = STEP_REPORT
            st.rerun()

        except Exception as e:
            status_box.empty()
            st.error(f"Error during decision synthesis: {str(e)}")


def _render_info_cards() -> None:
    """Renders informative cards explaining the Decision Intelligence framework."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card-panel">
                <div class="card-title">🎯 De-Bias & Frame</div>
                <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                    Uncovers hidden assumptions, loss aversion, and cognitive biases before evaluating choices.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card-panel">
                <div class="card-title">⚖️ Trade-off Matrix</div>
                <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                    Weighs immediate upside against long-term risk and second-order consequences.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card-panel">
                <div class="card-title">📋 Executive Report</div>
                <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                    Generates clean, actionable executive recommendations with structured next steps.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
