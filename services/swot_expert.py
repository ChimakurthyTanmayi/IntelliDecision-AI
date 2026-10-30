"""
SWOT Expert Agent (Agent 5) for IntelliDecision AI
Generates comprehensive SWOT analyses (Strengths, Weaknesses, Opportunities, Threats) for each candidate option.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.SWOTExpert")


class SWOTExpert:
    """
    Agent 5: SWOT Expert.
    Performs rigorous SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
    for every candidate option in the decision scenario.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize SWOTExpert with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def generate_swot(self, parsed_decision: Dict[str, Any], user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates SWOT analysis objects for each candidate option.

        :param parsed_decision: Output from DecisionParser.
        :param user_answers: User clarifications.
        :return: Dictionary mapping option names to SWOT structures.
        """
        if not parsed_decision or not isinstance(parsed_decision, dict):
            return self._get_fallback_swot()

        options = parsed_decision.get("possible_options", ["Option A", "Option B"])

        system_instruction = (
            "You are a C-suite Strategic Management Consultant. Your objective is to perform a thorough "
            "SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats) for every candidate option "
            "being evaluated in this decision."
        )

        prompt = f"""
Decision Context:
{json.dumps(parsed_decision, indent=2)}

User Clarifications:
{json.dumps(user_answers, indent=2)}

Options to Analyze: {json.dumps(options)}

Generate a SWOT breakdown for each option.
Return ONLY a valid JSON object matching this schema:
{{
  "swot_by_option": [
    {{
      "option_name": "Option 1 Name",
      "strengths": [
        "Internal competitive advantage 1",
        "Key structural asset 2"
      ],
      "weaknesses": [
        "Internal operational gap or deficit 1",
        "Resource constraint 2"
      ],
      "opportunities": [
        "External growth catalyst or trend 1",
        "Future option value unlocked"
      ],
      "threats": [
        "External market, competition, or macro risk 1",
        "Downside hazard 2"
      ]
    }}
  ]
}}

Rules:
- Generate an entry in "swot_by_option" for EVERY option in {json.dumps(options)}.
- Every array field MUST contain at least 2 specific, actionable bullet points.
- Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Using fallback SWOT analysis.")
                return self._get_fallback_swot(options)

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                return self._get_fallback_swot(options)

            parsed = json.loads(response_text)
            return self._sanitize_swot(parsed, options)

        except Exception as e:
            logger.error(f"Error in SWOTExpert: {e}")
            return self._get_fallback_swot(options)

    def _sanitize_swot(self, data: Dict[str, Any], options: List[str]) -> Dict[str, Any]:
        """Ensures SWOT structure has valid bullet lists per option."""
        swot_list = data.get("swot_by_option", [])
        sanitized: List[Dict[str, Any]] = []

        if isinstance(swot_list, list) and len(swot_list) > 0:
            for item in swot_list:
                if isinstance(item, dict):
                    opt_name = str(item.get("option_name", "Option")).strip()
                    sanitized.append({
                        "option_name": opt_name,
                        "strengths": self._ensure_list(item.get("strengths"), ["Strong strategic alignment", "Clear value proposition"]),
                        "weaknesses": self._ensure_list(item.get("weaknesses"), ["Requires capital or time investment", "Short-term learning curve"]),
                        "opportunities": self._ensure_list(item.get("opportunities"), ["Accelerates future option value", "Expands network & capability"]),
                        "threats": self._ensure_list(item.get("threats"), ["Execution delay risk", "External market volatility"])
                    })

        if not sanitized:
            return self._get_fallback_swot(options)

        return {"swot_by_option": sanitized}

    def _ensure_list(self, val: Any, default_bullets: List[str]) -> List[str]:
        """Ensures non-empty list of non-empty strings."""
        if isinstance(val, list) and len(val) > 0:
            cleaned = [str(x).strip() for x in val if str(x).strip()]
            if cleaned:
                return cleaned
        return default_default if (default_default := default_bullets) else ["Validated assumption."]

    def _get_fallback_swot(self, options: Optional[List[str]] = None) -> Dict[str, Any]:
        """Fallback SWOT analysis."""
        opts = options or ["Primary Option", "Alternative Option"]
        swot_list = []
        for opt in opts:
            swot_list.append({
                "option_name": opt,
                "strengths": ["High strategic fit with stated primary goals", "Leverages existing core competencies"],
                "weaknesses": ["Demands disciplined execution focus", "Temporary resource commitment"],
                "opportunities": ["Positions for non-linear growth", "Unlocks new industry/market capabilities"],
                "threats": ["Unexpected external market/timeline shifts", "Potential opportunity cost"]
            })
        return {"swot_by_option": swot_list}
