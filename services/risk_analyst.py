"""
Risk Analyst Agent (Agent 3) for IntelliDecision AI
Analyzes multi-dimensional risks across options: Financial, Career, Legal, Emotional, Health, and Business risks.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.RiskAnalyst")


class RiskAnalyst:
    """
    Agent 3: Risk Analyst.
    Evaluates multi-dimensional risk profiles (Financial, Career, Legal, Emotional, Health, Business)
    and identifies downside scenarios and risk severity for each decision option.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize RiskAnalyst with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def analyze_risks(self, parsed_decision: Dict[str, Any], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates risk dimensions for the decision scenario.

        :param parsed_decision: Output from DecisionParser.
        :param user_answers: Clarification answers provided by the user.
        :return: Risk analysis dictionary containing scores and detailed breakdowns.
        """
        if not parsed_decision or not isinstance(parsed_decision, dict):
            return self._get_fallback_risks()

        system_instruction = (
            "You are a C-suite Risk Analyst and Actuary. Your sole objective is to rigorously "
            "evaluate risk dimensions across options: Financial, Career, Legal, Emotional, Health, and Business risks. "
            "Quantify risk severity (1-10) and provide concrete downside explanations and mitigations."
        )

        options = parsed_decision.get("possible_options", ["Option A", "Option B"])

        prompt = f"""
Decision Scenario:
{json.dumps(parsed_decision, indent=2)}

User Clarifications & Constraints:
{json.dumps(user_answers, indent=2)}

Options to Evaluate: {json.dumps(options)}

Analyze the risk landscape and return ONLY a valid JSON object matching this schema:
{{
  "overall_risk_level": "High / Medium / Low",
  "risk_summary": "1-2 sentence overview of the primary risk drivers.",
  "risk_dimensions": {{
    "Financial": {{"score": 6, "level": "Medium", "description": "Risk of capital loss or cash flow strain", "mitigation": "Maintain 6-month buffer"}},
    "Career": {{"score": 4, "level": "Low", "description": "Impact on long-term professional trajectory", "mitigation": "Upskill continuously"}},
    "Legal": {{"score": 2, "level": "Low", "description": "Compliance or contractual liability", "mitigation": "Review covenants"}},
    "Emotional": {{"score": 7, "level": "High", "description": "Stress, uncertainty, and burnout risk", "mitigation": "Set clear boundaries"}},
    "Health": {{"score": 3, "level": "Low", "description": "Physical well-being impact", "mitigation": "Prioritize sleep"}},
    "Business": {{"score": 5, "level": "Medium", "description": "Market, execution, or operational risk", "mitigation": "Run a 30-day pilot"}}
  }},
  "option_risks": [
    {{
      "option_name": "Option 1 Name",
      "primary_risk": "Main downside risk",
      "risk_score": 6,
      "worst_case_scenario": "What happens if things go wrong",
      "mitigation_strategy": "Concrete action to prevent or reduce harm"
    }}
  ]
}}

Rule:
- "score" fields MUST be integers between 1 (minimal risk) and 10 (extreme risk).
- Provide a risk entry in "option_risks" for each option in {json.dumps(options)}.
- Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Using fallback risk analysis.")
                return self._get_fallback_risks(options)

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                return self._get_fallback_risks(options)

            parsed = json.loads(response_text)
            return self._sanitize_risks(parsed, options)

        except Exception as e:
            logger.error(f"Error in RiskAnalyst: {e}")
            return self._get_fallback_risks(options)

    def _sanitize_risks(self, data: Dict[str, Any], options: List[str]) -> Dict[str, Any]:
        """Ensures risk structure has clean values and defaults."""
        dimensions = data.get("risk_dimensions", {})
        standard_dims = ["Financial", "Career", "Legal", "Emotional", "Health", "Business"]
        sanitized_dims: Dict[str, Any] = {}

        for dim in standard_dims:
            d = dimensions.get(dim, {}) if isinstance(dimensions, dict) else {}
            try:
                score = int(d.get("score", 5))
                score = max(1, min(10, score))
            except (ValueError, TypeError):
                score = 5

            level = "Low" if score <= 3 else ("High" if score >= 7 else "Medium")
            sanitized_dims[dim] = {
                "score": score,
                "level": str(d.get("level", level)).strip(),
                "description": str(d.get("description", f"{dim} exposure in this scenario.")).strip(),
                "mitigation": str(d.get("mitigation", "Establish clear operational boundaries.")).strip()
            }

        option_risks = data.get("option_risks", [])
        sanitized_opt_risks = []
        if isinstance(option_risks, list) and len(option_risks) > 0:
            for item in option_risks:
                if isinstance(item, dict):
                    sanitized_opt_risks.append({
                        "option_name": str(item.get("option_name", "Option")).strip(),
                        "primary_risk": str(item.get("primary_risk", "Uncertain outcome")).strip(),
                        "risk_score": max(1, min(10, int(item.get("risk_score", 5)))),
                        "worst_case_scenario": str(item.get("worst_case_scenario", "Execution delay")).strip(),
                        "mitigation_strategy": str(item.get("mitigation_strategy", "Phased implementation")).strip()
                    })

        if not sanitized_opt_risks:
            for opt in options:
                sanitized_opt_risks.append({
                    "option_name": opt,
                    "primary_risk": "Uncertain execution timeline or resource strain",
                    "risk_score": 5,
                    "worst_case_scenario": "Delayed ROI or temporary cash/time strain",
                    "mitigation_strategy": "Phased rollout with 30-day review milestones"
                })

        return {
            "overall_risk_level": str(data.get("overall_risk_level", "Medium")).strip(),
            "risk_summary": str(data.get("risk_summary", "Balanced risk exposure requiring structured execution.")).strip(),
            "risk_dimensions": sanitized_dims,
            "option_risks": sanitized_opt_risks
        }

    def _get_fallback_risks(self, options: Optional[List[str]] = None) -> Dict[str, Any]:
        """Fallback risk analysis if API call fails."""
        opts = options or ["Primary Option", "Alternative Option"]
        return {
            "overall_risk_level": "Medium",
            "risk_summary": "Moderate overall risk exposure. Primary risk drivers center on execution time and opportunity cost.",
            "risk_dimensions": {
                "Financial": {"score": 5, "level": "Medium", "description": "Moderate capital commitment.", "mitigation": "Set strict spending limits."},
                "Career": {"score": 4, "level": "Low", "description": "Stable career trajectory impact.", "mitigation": "Focus on transferable skills."},
                "Legal": {"score": 2, "level": "Low", "description": "Minimal legal exposure.", "mitigation": "Standard contract review."},
                "Emotional": {"score": 6, "level": "Medium", "description": "Transition fatigue or decision stress.", "mitigation": "Pace milestones evenly."},
                "Health": {"score": 3, "level": "Low", "description": "Manageable stress level.", "mitigation": "Maintain work-life balance."},
                "Business": {"score": 5, "level": "Medium", "description": "Execution uncertainty.", "mitigation": "Conduct a 2-week pilot trial."}
            },
            "option_risks": [
                {
                    "option_name": opt,
                    "primary_risk": "Execution delay or unexpected resource strain",
                    "risk_score": 5,
                    "worst_case_scenario": "Sub-optimal timeline completion",
                    "mitigation_strategy": "Establish 30-day checkpoint reviews"
                } for opt in opts
            ]
        }
