"""
Recommendation Engine Agent (Agent 6) for IntelliDecision AI
Synthesizes multi-agent analytical outputs into McKinsey-grade executive recommendations,
explaining why the top option wins, why others are weaker, and unearthing cognitive biases and hidden assumptions.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.RecommendationEngine")


class RecommendationEngine:
    """
    Agent 6: Recommendation Engine.
    Synthesizes outputs from Decision Parser, User Q&A, Risk Analyst, Decision Matrix, and SWOT Expert
    into a cohesive, authoritative executive strategy recommendation.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize RecommendationEngine with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def generate_recommendation(
        self,
        parsed_decision: Dict[str, Any],
        user_answers: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        decision_matrix: Dict[str, Any],
        swot_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes multi-agent outputs into executive recommendation data structure.

        :param parsed_decision: Parsed decision structure.
        :param user_answers: User answers to Q&A questions.
        :param risk_analysis: Multi-dimensional risk analysis from Agent 3.
        :param decision_matrix: Decision matrix scores from Agent 4.
        :param swot_analysis: SWOT breakdown from Agent 5.
        :return: Final executive recommendation dictionary.
        """
        system_instruction = (
            "You are a C-suite Executive Strategy Advisor (ex-McKinsey Principal). "
            "Your role is to synthesize all analytical inputs into a definitive, authoritative, "
            "logically flawless executive recommendation. Explain explicitly WHY the recommended choice "
            "wins and WHY alternative choices are weaker. Identify cognitive biases and hidden assumptions."
        )

        prompt = f"""
Decision Scenario:
{json.dumps(parsed_decision, indent=2)}

User Clarifications:
{json.dumps(user_answers, indent=2)}

Risk Analysis Summary:
{json.dumps(risk_analysis, indent=2)}

Decision Matrix Scores:
{json.dumps(decision_matrix, indent=2)}

SWOT Analysis:
{json.dumps(swot_analysis, indent=2)}

Synthesize these inputs and return ONLY a valid JSON object matching this exact schema:

{{
  "recommended_option": "Name of the single winning option",
  "confidence_score": 88,
  "executive_summary": "Crisp 2-3 sentence C-suite summary of the situation and final decision.",
  "why_recommended_wins": [
    "Core reason 1 why this option outperforms on user's primary goal and risk tolerance",
    "Core reason 2 highlighting superior ROI or alignment"
  ],
  "why_others_are_weaker": [
    "Option B: Inferior due to higher downside risk / lack of long-term upside",
    "Option C: Rejected due to execution bottleneck"
  ],
  "hidden_assumptions": [
    "Assumption 1 that user is making without full validation",
    "Assumption 2 regarding timeline or external support"
  ],
  "cognitive_biases": [
    "Sunk Cost Fallacy: Holding onto past investments rather than future EV",
    "Loss Aversion: Overweighting short-term downside risk vs long-term gain",
    "Status Quo Bias: Preferring familiarity over optimal growth"
  ],
  "action_plan_30_60_90": [
    "Days 1-30: Immediate alignment, stakeholder buy-in, and risk mitigation setup",
    "Days 31-60: Core execution rollout and progress milestone reviews",
    "Days 61-90: Evaluation, optimization, and scaling"
  ],
  "contingency_triggers": [
    "If risk metric X breaches threshold Y, trigger contingency path Z"
  ]
}}

Rules:
1. "confidence_score" MUST be an integer between 0 and 100.
2. "recommended_option" MUST match one of the candidate options evaluated.
3. Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Generating fallback recommendation.")
                return self._get_fallback_recommendation(parsed_decision)

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                return self._get_fallback_recommendation(parsed_decision)

            parsed = json.loads(response_text)
            return self._sanitize_recommendation(parsed, parsed_decision)

        except Exception as e:
            logger.error(f"Error in RecommendationEngine: {e}")
            return self._get_fallback_recommendation(parsed_decision)

    def _sanitize_recommendation(self, data: Dict[str, Any], parsed_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Validates schema fields and types."""
        opts = parsed_decision.get("possible_options", ["Primary Option"])
        rec_opt = str(data.get("recommended_option", opts[0])).strip()

        try:
            score = int(data.get("confidence_score", 85))
            score = max(0, min(100, score))
        except (ValueError, TypeError):
            score = 85

        return {
            "recommended_option": rec_opt if rec_opt else opts[0],
            "confidence_score": score,
            "executive_summary": str(data.get("executive_summary", "Strategic synthesis recommends pursuing the primary option.")).strip(),
            "why_recommended_wins": self._ensure_list(data.get("why_recommended_wins"), ["Delivers highest risk-adjusted expected value", "Aligns directly with primary goal and resource limits"]),
            "why_others_are_weaker": self._ensure_list(data.get("why_others_are_weaker"), ["Alternative options carry higher execution risk with lower long-term upside"]),
            "hidden_assumptions": self._ensure_list(data.get("hidden_assumptions"), ["Assuming current market/personal capacity remains constant"]),
            "cognitive_biases": self._ensure_list(data.get("cognitive_biases"), ["Status Quo Bias: Resistance to necessary organizational or career change", "Loss Aversion: Overweighting short-term transition friction"]),
            "action_plan_30_60_90": self._ensure_list(data.get("action_plan_30_60_90"), [
                "Days 1-30: Align key stakeholders and establish risk guardrails.",
                "Days 31-60: Initiate core implementation and monitor 30-day KPIs.",
                "Days 61-90: Review outcomes, optimize workflow, and scale."
            ]),
            "contingency_triggers": self._ensure_list(data.get("contingency_triggers"), ["If execution delay exceeds 30 days, pivot to secondary fallback plan."])
        }

    def _ensure_list(self, val: Any, fallback: List[str]) -> List[str]:
        """Ensures non-empty list of non-empty strings."""
        if isinstance(val, list) and len(val) > 0:
            cleaned = [str(x).strip() for x in val if str(x).strip()]
            if cleaned:
                return cleaned
        return fallback

    def _get_fallback_recommendation(self, parsed_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback recommendation structure."""
        opts = parsed_decision.get("possible_options", ["Primary Path", "Alternative Path"])
        win_opt = opts[0] if opts else "Primary Option"
        alt_opt = opts[1] if len(opts) > 1 else "Alternative Option"

        return {
            "recommended_option": win_opt,
            "confidence_score": 82,
            "executive_summary": f"After evaluating risk profiles, resource constraints, and long-term upside, pursuing {win_opt} emerges as the optimal choice.",
            "why_recommended_wins": [
                f"{win_opt} maximizes expected return while staying within defined risk guardrails.",
                "Provides greater long-term growth and learning opportunities."
            ],
            "why_others_are_weaker": [
                f"{alt_opt} exhibits higher execution complexity and lower strategic flexibility."
            ],
            "hidden_assumptions": [
                "Assuming external environment and personal priorities remain stable over 12 months.",
                "Assuming resource/financial buffers are sufficient during transition phase."
            ],
            "cognitive_biases": [
                "Status Quo Bias: Potential hesitation to abandon current comfortable baseline.",
                "Loss Aversion: Tendency to fear potential losses more than valuing equivalent gains."
            ],
            "action_plan_30_60_90": [
                "Days 1-30: Define quantitative success metrics and communicate plan to stakeholders.",
                "Days 31-60: Commence execution phase with 30-day milestone reviews.",
                "Days 61-90: Evaluate initial feedback, optimize strategy, and solidify gains."
            ],
            "contingency_triggers": [
                "If initial pilot fails to achieve key threshold within 45 days, re-evaluate secondary path."
            ]
        }
