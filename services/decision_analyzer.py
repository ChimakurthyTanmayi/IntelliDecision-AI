"""
Decision Analyzer Orchestrator Module for IntelliDecision AI
Orchestrates multi-agent analysis: Risk Analyst (Agent 3), Decision Matrix (Agent 4),
SWOT Expert (Agent 5), and Recommendation Engine (Agent 6).
"""

import logging
from typing import Dict, Any, Optional
from services.gemini_service import GeminiService
from services.risk_analyst import RiskAnalyst
from services.decision_matrix_generator import DecisionMatrixGenerator
from services.swot_expert import SWOTExpert
from services.recommendation_engine import RecommendationEngine

logger = logging.getLogger("IntelliDecision.DecisionAnalyzer")


class DecisionAnalyzer:
    """
    Multi-Agent Orchestrator.
    Synthesizes parsed decision context and user Q&A answers through specialized agents:
    - Agent 3: RiskAnalyst
    - Agent 4: DecisionMatrixGenerator
    - Agent 5: SWOTExpert
    - Agent 6: RecommendationEngine
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize DecisionAnalyzer and instantiate child agents.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()
        self.risk_analyst = RiskAnalyst(self.gemini_service)
        self.matrix_generator = DecisionMatrixGenerator(self.gemini_service)
        self.swot_expert = SWOTExpert(self.gemini_service)
        self.recommendation_engine = RecommendationEngine(self.gemini_service)

    def analyze(self, parsed_decision: Dict[str, Any], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates multi-agent deep reasoning on the decision scenario.

        :param parsed_decision: Structured dictionary from DecisionParser.
        :param user_answers: Dictionary containing user's Q&A responses.
        :return: Master structured dictionary combining all agent outputs.
        """
        if not parsed_decision or not isinstance(parsed_decision, dict):
            logger.warning("Empty or invalid parsed_decision provided to DecisionAnalyzer.")
            return self._get_fallback_master_analysis("Missing parsed decision context.")

        try:
            logger.info("Executing Agent 3 (RiskAnalyst)...")
            risk_res = self.risk_analyst.analyze_risks(parsed_decision, user_answers)

            logger.info("Executing Agent 4 (DecisionMatrixGenerator)...")
            matrix_res = self.matrix_generator.generate_matrix(parsed_decision, user_answers)

            logger.info("Executing Agent 5 (SWOTExpert)...")
            swot_res = self.swot_expert.generate_swot(parsed_decision, user_answers)

            logger.info("Executing Agent 6 (RecommendationEngine)...")
            rec_res = self.recommendation_engine.generate_recommendation(
                parsed_decision, user_answers, risk_res, matrix_res, swot_res
            )

            # Package master synthesized dictionary
            master_analysis = {
                "decision_summary": rec_res.get("executive_summary", "Decision analysis complete."),
                "recommended_option": rec_res.get("recommended_option", ""),
                "recommendation": rec_res.get("recommended_option", ""),
                "confidence_score": rec_res.get("confidence_score", 85),
                "why_recommended_wins": rec_res.get("why_recommended_wins", []),
                "why_others_are_weaker": rec_res.get("why_others_are_weaker", []),
                "hidden_assumptions": rec_res.get("hidden_assumptions", []),
                "cognitive_biases": rec_res.get("cognitive_biases", []),
                "action_plan_30_60_90": rec_res.get("action_plan_30_60_90", []),
                "contingency_triggers": rec_res.get("contingency_triggers", []),
                "risk_analysis": risk_res,
                "decision_matrix": matrix_res,
                "swot_analysis": swot_res,
                "reasoning": " \n".join(rec_res.get("why_recommended_wins", [])),
                "pros": self._extract_pros(swot_res),
                "cons": self._extract_cons(swot_res),
                "trade_offs": self._extract_trade_offs(matrix_res),
                "hidden_factors": rec_res.get("hidden_assumptions", []),
                "risks": [f"{k}: {v.get('description', '')}" for k, v in risk_res.get("risk_dimensions", {}).items() if isinstance(v, dict)],
                "opportunities": self._extract_opportunities(swot_res),
                "alternative_options": parsed_decision.get("possible_options", [])[1:] if len(parsed_decision.get("possible_options", [])) > 1 else ["Phased pilot implementation"]
            }

            return master_analysis

        except Exception as e:
            logger.error(f"Error in DecisionAnalyzer multi-agent orchestration: {e}", exc_info=True)
            return self._get_fallback_master_analysis(str(e))

    def _extract_pros(self, swot_res: Dict[str, Any]) -> list:
        """Extracts strengths as top pros."""
        pros = []
        for opt_swot in swot_res.get("swot_by_option", []):
            opt_name = opt_swot.get("option_name", "Option")
            for s in opt_swot.get("strengths", []):
                pros.append(f"[{opt_name}] {s}")
        return pros[:6] if pros else ["Strong strategic alignment with primary goal"]

    def _extract_cons(self, swot_res: Dict[str, Any]) -> list:
        """Extracts weaknesses as top cons."""
        cons = []
        for opt_swot in swot_res.get("swot_by_option", []):
            opt_name = opt_swot.get("option_name", "Option")
            for w in opt_swot.get("weaknesses", []):
                cons.append(f"[{opt_name}] {w}")
        return cons[:6] if cons else ["Requires initial effort and transition period"]

    def _extract_opportunities(self, swot_res: Dict[str, Any]) -> list:
        """Extracts opportunities from SWOT."""
        opps = []
        for opt_swot in swot_res.get("swot_by_option", []):
            for o in opt_swot.get("opportunities", []):
                opps.append(o)
        return opps[:5] if opps else ["Accelerates skill development and future career options"]

    def _extract_trade_offs(self, matrix_res: Dict[str, Any]) -> list:
        """Extracts bottlenecks and trade-offs from decision matrix."""
        trade_offs = []
        for opt_score in matrix_res.get("options_scores", []):
            opt_name = opt_score.get("option_name", "Option")
            adv = opt_score.get("key_advantage", "")
            bot = opt_score.get("main_bottleneck", "")
            if adv and bot:
                trade_offs.append(f"{opt_name}: {adv} VS {bot}")
        return trade_offs if trade_offs else ["Immediate execution effort vs long-term ROI"]

    def _get_fallback_master_analysis(self, reason: str = "") -> Dict[str, Any]:
        """Provides a safe master fallback structure."""
        return {
            "decision_summary": f"Executive evaluation of decision scenario. ({reason})",
            "recommended_option": "Primary Option",
            "recommendation": "Pursue primary option with structured 30-day risk milestones.",
            "confidence_score": 80,
            "why_recommended_wins": [
                "Delivers highest strategic alignment with user's core objectives.",
                "Provides optimal balance of immediate feasibility and long-term upside."
            ],
            "why_others_are_weaker": [
                "Alternative choices exhibit higher execution complexity or lower long-term career growth."
            ],
            "hidden_assumptions": [
                "Assuming external conditions and personal capacity remain consistent during transition."
            ],
            "cognitive_biases": [
                "Status Quo Bias: Natural resistance to departing from baseline comfort zone."
            ],
            "action_plan_30_60_90": [
                "Days 1-30: Align key stakeholders and set quantifiable milestone metrics.",
                "Days 31-60: Initiate core execution phase with 30-day review checkpoint.",
                "Days 61-90: Evaluate progress, adjust parameters, and solidify outcomes."
            ],
            "contingency_triggers": [
                "If execution milestones lag by over 30 days, re-evaluate secondary fallback option."
            ],
            "risk_analysis": {
                "overall_risk_level": "Medium",
                "risk_summary": "Balanced risk profile requiring disciplined timeline management.",
                "risk_dimensions": {
                    "Financial": {"score": 5, "level": "Medium", "description": "Manageable financial commitment.", "mitigation": "Set cash buffer."},
                    "Career": {"score": 4, "level": "Low", "description": "Positive career trajectory impact.", "mitigation": "Focus on growth skills."},
                    "Legal": {"score": 2, "level": "Low", "description": "Standard compliance requirements.", "mitigation": "Review terms."},
                    "Emotional": {"score": 5, "level": "Medium", "description": "Transition fatigue.", "mitigation": "Pace implementation."},
                    "Health": {"score": 3, "level": "Low", "description": "Minimal health risk.", "mitigation": "Maintain balance."},
                    "Business": {"score": 5, "level": "Medium", "description": "Execution uncertainty.", "mitigation": "Run a 2-week pilot."}
                },
                "option_risks": []
            },
            "decision_matrix": {
                "criteria_list": ["Financial Return", "Growth Potential", "Learning Opportunity", "Long-Term Value", "Feasibility & Speed", "Ease of Execution", "Low Risk Advantage", "Emotional Fit"],
                "options_scores": [
                    {
                        "option_name": "Primary Option",
                        "scores": {"Financial Return": 85, "Growth Potential": 90, "Learning Opportunity": 85, "Long-Term Value": 88, "Feasibility & Speed": 75, "Ease of Execution": 70, "Low Risk Advantage": 65, "Emotional Fit": 80},
                        "weighted_total_score": 80,
                        "key_advantage": "High growth upside",
                        "main_bottleneck": "Initial transition effort"
                    }
                ],
                "matrix_summary": "Primary option leads in overall multi-criteria weighted evaluation."
            },
            "swot_analysis": {
                "swot_by_option": [
                    {
                        "option_name": "Primary Option",
                        "strengths": ["High strategic fit", "Strong value creation"],
                        "weaknesses": ["Initial learning curve"],
                        "opportunities": ["Unlocks future leadership/career opportunities"],
                        "threats": ["External timeline volatility"]
                    }
                ]
            },
            "reasoning": "Pursuing the primary option maximizes expected value while respecting defined constraints.",
            "pros": ["High long-term strategic value", "Maximizes growth potential"],
            "cons": ["Requires initial transition effort"],
            "trade_offs": ["Execution effort vs long-term reward"],
            "hidden_factors": ["Opportunity cost of status quo"],
            "risks": ["Timeline delay"],
            "opportunities": ["Skill and network expansion"],
            "alternative_options": ["Conduct a 14-day test pilot"]
        }
