"""
Decision Matrix Generator Agent (Agent 4) for IntelliDecision AI
Generates scored multi-attribute decision evaluation matrices comparing all options.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.DecisionMatrixGenerator")


class DecisionMatrixGenerator:
    """
    Agent 4: Decision Matrix Generator.
    Evaluates and scores each candidate option across standardized decision criteria:
    Cost, Risk, Difficulty, Growth, Financial Return, Learning, Long-Term Value, Feasibility, Emotional Impact.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize DecisionMatrixGenerator with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def generate_matrix(self, parsed_decision: Dict[str, Any], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured multi-criteria decision matrix with option scores (0-100).

        :param parsed_decision: Output from DecisionParser.
        :param user_answers: Clarification answers from user.
        :return: Decision matrix dictionary containing criteria weights, option scores, and total rankings.
        """
        if not parsed_decision or not isinstance(parsed_decision, dict):
            return self._get_fallback_matrix()

        options = parsed_decision.get("possible_options", ["Option A", "Option B"])

        system_instruction = (
            "You are an expert Management Scientist and Quantitative Decision Analyst. "
            "Your task is to construct a rigorous Multi-Criteria Decision Matrix scoring "
            "every candidate option on a 0-100 scale across standard decision criteria."
        )

        prompt = f"""
Decision Context:
{json.dumps(parsed_decision, indent=2)}

User Clarifications & Priorities:
{json.dumps(user_answers, indent=2)}

Options to Score: {json.dumps(options)}

Criteria to evaluate (0-100 scale, where 100 is most favorable/highest quality):
1. Financial Impact / ROI
2. Career / Business Growth Potential
3. Learning & Skill Development
4. Long-Term Value & Upside
5. Feasibility & Speed
6. Ease of Execution (100 = very easy, 0 = extremely hard)
7. Low Risk Advantage (100 = minimal risk, 0 = extreme risk)
8. Emotional Satisfaction / Fit

Return ONLY a valid JSON object matching this schema:
{{
  "criteria_list": [
    "Financial Return",
    "Growth Potential",
    "Learning Opportunity",
    "Long-Term Value",
    "Feasibility & Speed",
    "Ease of Execution",
    "Low Risk Advantage",
    "Emotional Fit"
  ],
  "options_scores": [
    {{
      "option_name": "Option 1 Name",
      "scores": {{
        "Financial Return": 85,
        "Growth Potential": 90,
        "Learning Opportunity": 88,
        "Long-Term Value": 92,
        "Feasibility & Speed": 70,
        "Ease of Execution": 65,
        "Low Risk Advantage": 60,
        "Emotional Fit": 80
      }},
      "weighted_total_score": 81,
      "key_advantage": "Highest upside growth and learning",
      "main_bottleneck": "Higher execution complexity"
    }}
  ],
  "matrix_summary": "1-2 sentence quantitative summary comparing the option scores."
}}

Rule:
- Scores MUST be integers between 0 and 100.
- Ensure an object exists in "options_scores" for EVERY option in {json.dumps(options)}.
- Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Utilizing fallback decision matrix.")
                return self._get_fallback_matrix(options)

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                return self._get_fallback_matrix(options)

            parsed = json.loads(response_text)
            return self._sanitize_matrix(parsed, options)

        except Exception as e:
            logger.error(f"Error in DecisionMatrixGenerator: {e}")
            return self._get_fallback_matrix(options)

    def _sanitize_matrix(self, data: Dict[str, Any], options: List[str]) -> Dict[str, Any]:
        """Validates and cleans matrix scores and option names."""
        criteria = [
            "Financial Return", "Growth Potential", "Learning Opportunity",
            "Long-Term Value", "Feasibility & Speed", "Ease of Execution",
            "Low Risk Advantage", "Emotional Fit"
        ]

        raw_opts = data.get("options_scores", [])
        sanitized_opts = []

        if isinstance(raw_opts, list) and len(raw_opts) > 0:
            for item in raw_opts:
                if isinstance(item, dict):
                    opt_name = str(item.get("option_name", "Option")).strip()
                    raw_scores = item.get("scores", {}) if isinstance(item.get("scores"), dict) else {}

                    clean_scores: Dict[str, int] = {}
                    sum_scores = 0
                    for c in criteria:
                        val = raw_scores.get(c, 70)
                        try:
                            score_val = max(0, min(100, int(val)))
                        except (ValueError, TypeError):
                            score_val = 70
                        clean_scores[c] = score_val
                        sum_scores += score_val

                    calc_avg = int(sum_scores / len(criteria))
                    total_val = item.get("weighted_total_score", calc_avg)
                    try:
                        total_score = max(0, min(100, int(total_val)))
                    except (ValueError, TypeError):
                        total_score = calc_avg

                    sanitized_opts.append({
                        "option_name": opt_name,
                        "scores": clean_scores,
                        "weighted_total_score": total_score,
                        "key_advantage": str(item.get("key_advantage", "High strategic alignment")).strip(),
                        "main_bottleneck": str(item.get("main_bottleneck", "Requires deliberate execution")).strip()
                    })

        if not sanitized_opts:
            return self._get_fallback_matrix(options)

        return {
            "criteria_list": criteria,
            "options_scores": sanitized_opts,
            "matrix_summary": str(data.get("matrix_summary", "Comparative analysis shows clear divergence in upside vs execution effort.")).strip()
        }

    def _get_fallback_matrix(self, options: Optional[List[str]] = None) -> Dict[str, Any]:
        """Fallback decision matrix if API is unconfigured or fails."""
        opts = options or ["Primary Option", "Alternative Option"]
        criteria = [
            "Financial Return", "Growth Potential", "Learning Opportunity",
            "Long-Term Value", "Feasibility & Speed", "Ease of Execution",
            "Low Risk Advantage", "Emotional Fit"
        ]

        opts_scores = []
        base_scores = [82, 68, 75]
        for idx, opt in enumerate(opts):
            b = base_scores[idx % len(base_scores)]
            s = {c: min(100, max(40, b + (i % 3) * 5 - (i % 2) * 8)) for i, c in enumerate(criteria)}
            avg_score = int(sum(s.values()) / len(criteria))
            opts_scores.append({
                "option_name": opt,
                "scores": s,
                "weighted_total_score": avg_score,
                "key_advantage": "Strong long-term strategic upside",
                "main_bottleneck": "Requires initial investment of effort"
            })

        return {
            "criteria_list": criteria,
            "options_scores": opts_scores,
            "matrix_summary": "Decision matrix highlights primary option as leading in long-term value and career upside."
        }
