"""
Decision Parser Module (Agent 1) for IntelliDecision AI
Parses unstructured decision inputs into structured JSON using Google Gemini AI.
Extracts: Decision Goal, Options, Constraints, Unknown Information, Stakeholders, Priorities.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.DecisionParser")


class DecisionParser:
    """
    Agent 1: Decision Parser.
    Parses unstructured decision problem descriptions into structured JSON dictionaries.
    Uncovers decision goal, options, constraints, missing/unknown information, stakeholders, priorities, and risk factors.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize DecisionParser with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """
        Analyzes raw decision text and returns a structured dictionary representing the decision context.

        :param decision_text: Unstructured user description of the decision problem.
        :return: Structured dictionary containing categorized decision attributes.
        """
        if not decision_text or not decision_text.strip():
            logger.warning("Empty decision_text passed to parse_decision.")
            return self._get_fallback_dict("", "Decision text cannot be empty.")

        system_instruction = (
            "You are an expert C-suite Decision Intelligence Analyst. Your task is to analyze raw "
            "decision scenarios and extract key structural attributes into a clean, valid JSON object."
        )

        prompt = f"""
Analyze the following user-submitted decision scenario:

Decision Scenario:
"{decision_text.strip()}"

Extract and structure the information into a valid JSON object matching this exact schema:
{{
  "decision_type": "Category (e.g. Career, Strategic Business, Education & Higher Studies, Investment & Finance, Tech Product, Personal)",
  "summary": "Crisp 1-2 sentence summary of the core dilemma",
  "primary_goal": "The main goal or objective the user wants to achieve",
  "possible_options": ["Option 1", "Option 2"],
  "constraints": ["Financial/Budget limits", "Resource/Time/Visa limits"],
  "unknown_information": ["Key missing details or unstated variables needed to make an informed choice"],
  "stakeholders": ["Who is impacted or involved"],
  "priorities": ["Top user priorities like ROI, growth, work-life balance, brand reputation"],
  "timeline": "Stated or implied deadline or timeframe",
  "risk_level": "High / Medium / Low"
}}

Rules:
1. "possible_options" MUST contain distinct choice paths inferred from the text (e.g., ["MS in US", "Stay in Current Job"] or ["Buy Laptop A", "Buy Laptop B"]).
2. Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Utilizing structured fallback for decision parsing.")
                return self._get_fallback_dict(decision_text, "Gemini API key not configured.")

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                logger.error("Gemini model returned empty response for decision parsing.")
                return self._get_fallback_dict(decision_text, "Model returned empty output.")

            parsed_json = json.loads(response_text)
            return self._validate_and_sanitize(parsed_json, decision_text)

        except json.JSONDecodeError as jde:
            logger.error(f"Failed to parse JSON response from Gemini: {jde}")
            return self._get_fallback_dict(decision_text, f"JSON parsing error: {str(jde)}")
        except Exception as e:
            logger.error(f"Unexpected error in parse_decision: {e}")
            return self._get_fallback_dict(decision_text, f"Processing error: {str(e)}")

    def _validate_and_sanitize(self, data: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
        """Ensures all required schema fields exist with sensible defaults."""
        summary_default = raw_text[:150] + "..." if len(raw_text) > 150 else raw_text

        required_schema: Dict[str, Any] = {
            "decision_type": "General",
            "summary": summary_default if summary_default.strip() else "Decision dilemma analysis",
            "primary_goal": "Make an informed and balanced strategic choice.",
            "possible_options": ["Option 1 (Primary Path)", "Option 2 (Alternative Path)"],
            "constraints": ["Time and resource limitations"],
            "unknown_information": ["Specific financial ROI details", "Long-term market conditions"],
            "stakeholders": ["Self / Primary Decision Maker"],
            "priorities": ["Risk mitigation", "Growth & long-term value"],
            "timeline": "Immediate / Not specified",
            "risk_level": "Medium"
        }

        sanitized: Dict[str, Any] = {}
        for key, default_val in required_schema.items():
            val = data.get(key)
            if val is None or (isinstance(val, list) and not val and isinstance(default_val, list) and default_val):
                sanitized[key] = default_val
            elif isinstance(val, list):
                sanitized[key] = [str(item).strip() for item in val if str(item).strip()]
            else:
                sanitized[key] = str(val).strip() if isinstance(val, str) else val

        # Ensure missing_information key also maps to unknown_information for backward compatibility
        sanitized["missing_information"] = sanitized.get("unknown_information", [])

        return sanitized

    def _get_fallback_dict(self, raw_text: str, error_msg: str = "") -> Dict[str, Any]:
        """Generates a safe fallback dictionary if AI parsing fails."""
        summary_text = raw_text.strip() if raw_text.strip() else "No context provided."
        return {
            "decision_type": "Uncategorized",
            "summary": summary_text[:200] if len(summary_text) > 200 else summary_text,
            "primary_goal": "Resolve decision dilemma effectively.",
            "possible_options": ["Primary Choice", "Alternative Path"],
            "constraints": ["Resource limitations", "Evaluation uncertainty"],
            "unknown_information": [f"Analysis note: {error_msg}"] if error_msg else ["Exact financial breakdown"],
            "missing_information": [f"Analysis note: {error_msg}"] if error_msg else ["Exact financial breakdown"],
            "stakeholders": ["Self / Primary Decision Maker"],
            "priorities": ["Capital preservation", "Career progression"],
            "timeline": "Immediate / Unknown",
            "risk_level": "Medium"
        }
