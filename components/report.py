"""
Report Component for IntelliDecision AI
Renders a modern, executive SaaS Decision Intelligence Dashboard with KPI metric cards,
Decision Matrix comparison table, Why Recommended Wins vs Weaker alternatives,
Risk Analyst breakdown, SWOT cards per option, Cognitive Biases, 30-60-90 Day Action Plan,
Plotly charts, and PDF/MD/JSON export capabilities.
"""

import json
import pandas as pd
import streamlit as st
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
from services.report_generator import ReportGenerator

# Initialize ReportGenerator instance for downloads
_report_gen = ReportGenerator()


def render_report_component(report: Dict[str, Any], raw_analysis: Optional[Dict[str, Any]] = None) -> None:
    """
    Renders the executive decision report dashboard featuring KPI cards, Plotly charts,
    Decision Matrix table, SWOT cards, Risk breakdown, and export options.

    :param report: Executive decision report dictionary.
    :param raw_analysis: Optional raw analysis dictionary from DecisionAnalyzer.
    """
    if not report:
        st.warning("No report available. Please start a new decision analysis.")
        if st.button("← Back to Decision Entry"):
            st.session_state.step = "HOME"
            st.rerun()
        return

    parsed_decision: Dict[str, Any] = st.session_state.get("parsed_decision", {}) or {}
    risk_analysis: Dict[str, Any] = report.get("risk_analysis", {}) or {}
    decision_matrix: Dict[str, Any] = report.get("decision_matrix", {}) or {}
    swot_analysis: Dict[str, Any] = report.get("swot_analysis", {}) or {}

    # Top Header & Action Row
    col_title, col_actions = st.columns([2.0, 2.0])

    with col_title:
        title = report.get("title", "Executive Decision Intelligence Report")
        st.markdown(f"<h1 style='font-size: 1.85rem; font-weight: 800; color: #f8fafc; margin: 0;'>{title}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #64748b; font-weight: 600; text-transform: uppercase; margin-top: 0.25rem; letter-spacing: 0.05em;'>McKinsey-Grade Multi-Agent Strategy Dashboard</p>", unsafe_allow_html=True)

    with col_actions:
        # Row 1: Export Buttons (Markdown, PDF, JSON)
        bcol1, bcol2, bcol3 = st.columns(3)
        with bcol1:
            md_text = _report_gen.generate_markdown(report)
            st.download_button(
                label="📄 Markdown",
                data=md_text,
                file_name="Executive_Decision_Report.md",
                mime="text/markdown",
                use_container_width=True
            )
        with bcol2:
            try:
                pdf_bytes = _report_gen.generate_pdf(report)
                st.download_button(
                    label="📥 Export PDF",
                    data=pdf_bytes,
                    file_name="Executive_Decision_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                st.button("PDF Export", disabled=True, use_container_width=True)
        with bcol3:
            json_str = _report_gen.generate_json(report)
            st.download_button(
                label="💾 Export JSON",
                data=json_str,
                file_name="Executive_Decision_Report.json",
                mime="application/json",
                use_container_width=True
            )

        # Row 2: Navigation Buttons
        ncol1, ncol2 = st.columns(2)
        with ncol1:
            if st.button("↺ New Decision", type="primary", use_container_width=True):
                st.session_state.step = "HOME"
                st.session_state.decision_input = ""
                st.session_state.parsed_decision = None
                st.session_state.questions = []
                st.session_state.user_answers = {}
                st.session_state.analysis_result = None
                st.session_state.final_report = None
                st.rerun()
        with ncol2:
            history_count = len(st.session_state.get("history", []))
            if st.button(f"📜 Session History ({history_count})", use_container_width=True):
                st.session_state.step = "HISTORY"
                st.rerun()

    st.markdown("<hr style='border-color: #1e293b; margin: 1.25rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # 1. Top Executive KPI Cards Row
    _render_kpi_metrics_row(parsed_decision, report)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Winning Recommendation & Strategic Rationale Section
    _render_winning_recommendation_section(report)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Interactive Multi-Criteria Decision Matrix Table
    _render_decision_matrix_section(decision_matrix)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Multi-Agent Risk Analysis Section (Financial, Career, Legal, Emotional, Health, Business)
    _render_risk_analysis_section(risk_analysis)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Interactive Visualizations (Plots: Confidence Gauge, Decision Scores Bar Chart, Multi-Attribute Radar)
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 1rem;'>📊 Decision Analytics & Radar Visualizations</h3>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        _render_confidence_gauge_chart(report.get("confidence_score", 85))
    with chart_col2:
        _render_option_scores_bar_chart(decision_matrix)

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        _render_risk_dimensions_bar_chart(risk_analysis)
    with chart_col4:
        _render_decision_radar_chart(report, decision_matrix)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. SWOT Analysis Cards per Candidate Option
    _render_swot_section(swot_analysis)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. Cognitive Biases & Hidden Assumptions Section
    _render_cognitive_biases_and_assumptions(report)

    st.markdown("<br>", unsafe_allow_html=True)

    # 8. 30-60-90 Day Action Plan & Contingency Triggers
    _render_action_plan_section(report)


def _render_kpi_metrics_row(parsed_decision: Dict[str, Any], report: Dict[str, Any]) -> None:
    """Renders top SaaS KPI cards row for key metrics."""
    col1, col2, col3, col4 = st.columns(4)

    dec_type = parsed_decision.get("decision_type", "Strategic")
    risk_level = parsed_decision.get("risk_level", "Medium")
    conf_score = report.get("confidence_score", 85)
    winning_opt = report.get("recommended_option", "Primary Choice")

    risk_color = "#34d399" if "low" in risk_level.lower() else ("#f87171" if "high" in risk_level.lower() else "#fbbf24")

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Decision Type</span>
                    <span class="kpi-icon">🎯</span>
                </div>
                <div class="kpi-value" style="font-size: 1.1rem; color: #a5b4fc;">{dec_type}</div>
                <div class="kpi-subtext">Categorized Domain</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Winning Choice</span>
                    <span class="kpi-icon">🏆</span>
                </div>
                <div class="kpi-value" style="font-size: 1.1rem; color: #34d399;">{winning_opt}</div>
                <div class="kpi-subtext">Top Recommended Path</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Risk Severity</span>
                    <span class="kpi-icon">🛡️</span>
                </div>
                <div class="kpi-value" style="color: {risk_color};">{risk_level}</div>
                <div class="kpi-subtext">Evaluated Exposure</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Confidence Index</span>
                    <span class="kpi-icon">⚡</span>
                </div>
                <div class="kpi-value" style="color: #818cf8;">{conf_score}%</div>
                <div class="kpi-subtext">AI Recommendation Certainty</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def _render_winning_recommendation_section(report: Dict[str, Any]) -> None:
    """Renders prominent winning recommendation card explaining why it wins vs why others are weaker."""
    rec_opt = report.get("recommended_option", "Primary Choice")
    summary = report.get("executive_summary", "")
    why_wins = report.get("why_recommended_wins", [])
    why_weaker = report.get("why_others_are_weaker", [])

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.18) 0%, rgba(139, 92, 246, 0.18) 100%); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 16px; padding: 1.5rem; box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; color: #a5b4fc; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em;">
                    <span>🏆 Recommended Winner: <strong style="color: #ffffff; font-size: 1.15rem; text-transform: none;">{rec_opt}</strong></span>
                </div>
                <span class="badge-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);">Confidence: {report.get('confidence_score', 85)}%</span>
            </div>
            <p style="color: #e2e8f0; font-size: 0.98rem; line-height: 1.6; margin-bottom: 1.25rem;">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_wins, col_weaker = st.columns(2)

    with col_wins:
        st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #34d399;'>✅ Why This Option Wins</h4>", unsafe_allow_html=True)
        _render_bullet_card_list(why_wins, border_color="rgba(16, 185, 129, 0.3)", bg_color="rgba(16, 185, 129, 0.05)", icon="✓")

    with col_weaker:
        st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #f87171;'>⚠️ Why Other Options Are Weaker</h4>", unsafe_allow_html=True)
        _render_bullet_card_list(why_weaker, border_color="rgba(239, 68, 68, 0.3)", bg_color="rgba(239, 68, 68, 0.05)", icon="✗")


def _render_decision_matrix_section(decision_matrix: Dict[str, Any]) -> None:
    """Renders interactive multi-criteria decision evaluation table."""
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;'>📐 Multi-Criteria Decision Evaluation Matrix</h3>", unsafe_allow_html=True)

    summary = decision_matrix.get("matrix_summary", "Comparative multi-attribute scoring across candidates.")
    st.markdown(f"<p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;'>{summary}</p>", unsafe_allow_html=True)

    criteria = decision_matrix.get("criteria_list", [])
    opts_scores = decision_matrix.get("options_scores", [])

    if not opts_scores or not criteria:
        st.info("Decision matrix data being compiled.")
        return

    # Build Pandas DataFrame for clean Streamlit table
    data_rows = []
    for opt in opts_scores:
        row = {"Option": opt.get("option_name", "Option")}
        scores = opt.get("scores", {})
        for c in criteria:
            row[c] = scores.get(c, 70)
        row["Overall Score"] = opt.get("weighted_total_score", 75)
        row["Key Advantage"] = opt.get("key_advantage", "")
        data_rows.append(row)

    df = pd.DataFrame(data_rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Option": st.column_config.TextColumn("Option", help="Candidate choice", width="medium"),
            "Overall Score": st.column_config.ProgressColumn("Overall Score", help="0-100 weighted total", min_value=0, max_value=100, format="%d"),
            "Key Advantage": st.column_config.TextColumn("Key Advantage", width="large")
        }
    )


def _render_risk_analysis_section(risk_analysis: Dict[str, Any]) -> None:
    """Renders Multi-Dimension Risk Analysis Grid (Financial, Career, Legal, Emotional, Health, Business)."""
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;'>🛡️ Multi-Dimensional Risk Analysis</h3>", unsafe_allow_html=True)

    summary = risk_analysis.get("risk_summary", "Multi-factor evaluation of risk dimensions.")
    st.markdown(f"<p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;'>{summary}</p>", unsafe_allow_html=True)

    dimensions = risk_analysis.get("risk_dimensions", {})
    cols = st.columns(3)

    dim_keys = list(dimensions.keys())
    for idx, dim in enumerate(dim_keys):
        d = dimensions.get(dim, {})
        score = d.get("score", 5)
        level = d.get("level", "Medium")
        desc = d.get("description", "")
        mitigation = d.get("mitigation", "")

        card_col = cols[idx % 3]

        level_color = "#34d399" if score <= 3 else ("#f87171" if score >= 7 else "#fbbf24")

        with card_col:
            st.markdown(
                f"""
                <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: #f8fafc; font-weight: 700; font-size: 0.95rem;">{dim} Risk</span>
                        <span style="background: rgba(255, 255, 255, 0.05); color: {level_color}; padding: 0.2rem 0.5rem; border-radius: 6px; font-weight: 800; font-size: 0.8rem; border: 1px solid {level_color}40;">
                            {score}/10 ({level})
                        </span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4; margin-bottom: 0.5rem;">{desc}</p>
                    <div style="background: rgba(99, 102, 241, 0.08); border-radius: 6px; padding: 0.5rem; color: #a5b4fc; font-size: 0.8rem;">
                        <strong>Mitigation:</strong> {mitigation}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def _render_swot_section(swot_analysis: Dict[str, Any]) -> None:
    """Renders SWOT Analysis Cards per option."""
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 1rem;'>🧩 SWOT Analysis per Option</h3>", unsafe_allow_html=True)

    swot_list = swot_analysis.get("swot_by_option", [])
    if not swot_list:
        st.info("SWOT analysis compiled.")
        return

    tabs = st.tabs([opt.get("option_name", f"Option {i+1}") for i, opt in enumerate(swot_list)])

    for idx, tab in enumerate(tabs):
        opt_swot = swot_list[idx]
        with tab:
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #34d399;'>💪 Strengths (Internal)</h4>", unsafe_allow_html=True)
                _render_bullet_card_list(opt_swot.get("strengths", []), border_color="rgba(16, 185, 129, 0.3)", bg_color="rgba(16, 185, 129, 0.05)", icon="•")

                st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #38bdf8; margin-top: 1rem;'>🚀 Opportunities (External)</h4>", unsafe_allow_html=True)
                _render_bullet_card_list(opt_swot.get("opportunities", []), border_color="rgba(56, 189, 248, 0.3)", bg_color="rgba(56, 189, 248, 0.05)", icon="•")

            with s_col2:
                st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #f87171;'>⚠️ Weaknesses (Internal)</h4>", unsafe_allow_html=True)
                _render_bullet_card_list(opt_swot.get("weaknesses", []), border_color="rgba(239, 68, 68, 0.3)", bg_color="rgba(239, 68, 68, 0.05)", icon="•")

                st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #fbbf24; margin-top: 1rem;'>⚡ Threats (External)</h4>", unsafe_allow_html=True)
                _render_bullet_card_list(opt_swot.get("threats", []), border_color="rgba(245, 158, 11, 0.3)", bg_color="rgba(245, 158, 11, 0.05)", icon="•")


def _render_cognitive_biases_and_assumptions(report: Dict[str, Any]) -> None:
    """Renders Hidden Assumptions & Cognitive Biases section."""
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 1rem;'>🧠 Cognitive Biases & Hidden Assumptions</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='font-size: 1rem; font-weight: 700; color: #fbbf24;'>🔍 Unexamined Hidden Assumptions</h4>", unsafe_allow_html=True)
        assumptions = report.get("hidden_assumptions", [])
        _render_bullet_card_list(assumptions, border_color="rgba(245, 158, 11, 0.3)", bg_color="rgba(245, 158, 11, 0.05)", icon="❓")

    with col2:
        st.markdown("<h4 style='font-size: 1rem; font-weight: 700; color: #c084fc;'>🧩 Identified Cognitive Biases</h4>", unsafe_allow_html=True)
        biases = report.get("cognitive_biases", [])
        _render_bullet_card_list(biases, border_color="rgba(192, 132, 252, 0.3)", bg_color="rgba(192, 132, 252, 0.05)", icon="🧠")


def _render_action_plan_section(report: Dict[str, Any]) -> None:
    """Renders 30-60-90 Day Action Plan & Contingency Triggers."""
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 1rem;'>📅 30-60-90 Day Execution Roadmap</h3>", unsafe_allow_html=True)

    plan = report.get("action_plan_30_60_90", [])
    contingencies = report.get("contingency_triggers", [])

    st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
    for idx, item in enumerate(plan, start=1):
        st.markdown(f"**Phase {idx}:** {item}")
    st.markdown("</div>", unsafe_allow_html=True)

    if contingencies:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size: 1rem; font-weight: 700; color: #f87171;'>🚨 Downside Contingency Triggers</h4>", unsafe_allow_html=True)
        _render_bullet_card_list(contingencies, border_color="rgba(239, 68, 68, 0.3)", bg_color="rgba(239, 68, 68, 0.05)", icon="🚨")


def _render_confidence_gauge_chart(conf_score: int) -> None:
    """Renders Plotly Confidence Gauge Chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=conf_score,
        title={'text': "Recommendation Confidence Index", 'font': {'size': 14, 'color': '#f8fafc', 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#64748b"},
            'bar': {'color': "#6366f1", 'thickness': 0.3},
            'bgcolor': "#0b0f1a",
            'borderwidth': 1,
            'bordercolor': "#1e293b",
            'steps': [
                {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.15)"},
                {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.15)"},
                {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.15)"}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor='#0b0f1a',
        plot_bgcolor='#0b0f1a',
        font=dict(color='#cbd5e1', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=30, r=30, t=40, b=20),
        height=260
    )

    with st.container():
        st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_option_scores_bar_chart(decision_matrix: Dict[str, Any]) -> None:
    """Renders Plotly Option Overall Weighted Scores Bar Chart."""
    opts_scores = decision_matrix.get("options_scores", [])
    if not opts_scores:
        opts = ["Primary Option", "Alternative Option"]
        scores = [85, 70]
    else:
        opts = [o.get("option_name", "Option") for o in opts_scores]
        scores = [o.get("weighted_total_score", 75) for o in opts_scores]

    colors = ['#6366f1', '#38bdf8', '#c084fc', '#34d399', '#fbbf24']

    fig = go.Figure(data=[
        go.Bar(
            x=opts,
            y=scores,
            marker_color=colors[:len(opts)],
            borderRadius=6,
            text=[f"{s}/100" for s in scores],
            textposition='auto',
            textfont=dict(color='#ffffff', size=13, family='Plus Jakarta Sans')
        )
    ])

    fig.update_layout(
        title={'text': "Option Decision Matrix Total Scores", 'font': {'size': 14, 'color': '#f8fafc', 'family': 'Plus Jakarta Sans'}},
        paper_bgcolor='#0b0f1a',
        plot_bgcolor='#0b0f1a',
        yaxis=dict(showgrid=True, gridcolor='#1e293b', range=[0, 100], tickfont=dict(color='#94a3b8')),
        xaxis=dict(tickfont=dict(color='#cbd5e1', size=12, family='Plus Jakarta Sans')),
        font=dict(color='#cbd5e1', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=30, r=30, t=40, b=20),
        height=260
    )

    with st.container():
        st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_risk_dimensions_bar_chart(risk_analysis: Dict[str, Any]) -> None:
    """Renders Bar Chart of Risk Dimensions."""
    dims = risk_analysis.get("risk_dimensions", {})
    if not dims:
        categories = ["Financial", "Career", "Legal", "Emotional", "Health", "Business"]
        scores = [5, 4, 2, 6, 3, 5]
    else:
        categories = list(dims.keys())
        scores = [dims[k].get("score", 5) for k in categories]

    colors = ['#ef4444' if s >= 7 else ('#f59e0b' if s >= 4 else '#10b981') for s in scores]

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=scores,
            marker_color=colors,
            borderRadius=6,
            text=[f"{s}/10" for s in scores],
            textposition='auto',
            textfont=dict(color='#ffffff', size=11, family='Plus Jakarta Sans')
        )
    ])

    fig.update_layout(
        title={'text': "Risk Severity per Dimension (1-10)", 'font': {'size': 14, 'color': '#f8fafc', 'family': 'Plus Jakarta Sans'}},
        paper_bgcolor='#0b0f1a',
        plot_bgcolor='#0b0f1a',
        yaxis=dict(showgrid=True, gridcolor='#1e293b', range=[0, 10], tickfont=dict(color='#94a3b8')),
        xaxis=dict(tickfont=dict(color='#cbd5e1', size=11, family='Plus Jakarta Sans')),
        font=dict(color='#cbd5e1', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=30, r=30, t=40, b=20),
        height=260
    )

    with st.container():
        st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_decision_radar_chart(report: Dict[str, Any], decision_matrix: Dict[str, Any]) -> None:
    """Renders Plotly Radar overlay comparing top options across criteria."""
    opts_scores = decision_matrix.get("options_scores", [])
    criteria = decision_matrix.get("criteria_list", ["Financial Return", "Growth Potential", "Learning Opportunity", "Long-Term Value", "Feasibility & Speed", "Low Risk Advantage"])

    fig = go.Figure()

    colors = ['#6366f1', '#38bdf8', '#c084fc']

    if opts_scores:
        for idx, opt in enumerate(opts_scores[:3]):
            scores_dict = opt.get("scores", {})
            r_vals = [scores_dict.get(c, 70) for c in criteria[:6]]
            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=criteria[:6],
                fill='toself',
                name=opt.get("option_name", f"Option {idx+1}"),
                line=dict(color=colors[idx % len(colors)], width=2),
                fillcolor=f"rgba{tuple(list(int(colors[idx % len(colors)].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}"
            ))
    else:
        fig.add_trace(go.Scatterpolar(
            r=[85, 90, 80, 88, 75, 65],
            theta=criteria[:6],
            fill='toself',
            name='Recommended Path',
            line=dict(color='#6366f1', width=2),
            fillcolor='rgba(99, 102, 241, 0.25)'
        ))

    fig.update_layout(
        title={'text': "Multi-Criteria Radar Comparison", 'font': {'size': 14, 'color': '#f8fafc', 'family': 'Plus Jakarta Sans'}},
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='#64748b', showticklabels=False),
            bgcolor='#0b0f1a'
        ),
        paper_bgcolor='#0b0f1a',
        plot_bgcolor='#0b0f1a',
        font=dict(color='#cbd5e1', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=30, r=30, t=40, b=20),
        height=260,
        showlegend=True,
        legend=dict(font=dict(size=10, color='#cbd5e1'), orientation="h", y=-0.1)
    )

    with st.container():
        st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_bullet_card_list(items: List[str], border_color: str, bg_color: str, icon: str) -> None:
    """Helper to render bulleted list cards with custom styling."""
    if not items:
        items = ["None specified."]

    items_html = ""
    for idx, item in enumerate(items, start=1):
        display_icon = f"{idx}." if icon == "1." else icon
        items_html += f"""
        <div style="display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.65rem 0; border-bottom: 1px solid #1e293b;">
            <span style="color: #818cf8; font-weight: 800; font-size: 0.9rem;">{display_icon}</span>
            <span style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">{item}</span>
        </div>
        """

    st.markdown(
        f"""
        <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 12px; padding: 1rem 1.25rem; margin-top: 0.5rem;">
            {items_html}
        </div>
        """,
        unsafe_allow_html=True
    )
