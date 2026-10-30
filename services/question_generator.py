"""
Question Generator Module (Agent 2) for IntelliDecision AI
Generates personalized, probing follow-up questions tailored specifically to the user's decision type,
options, and missing information. Never uses generic fixed lists.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger("IntelliDecision.QuestionGenerator")

VALID_CATEGORIES = {
    "Financial", "Career", "Risk", "Personal Preferences", "Time",
    "Family", "Health", "Strategy", "Execution", "Education", "Market", "General"
}
VALID_TYPES = {"text", "scale", "choice", "slider", "number", "select", "selectbox", "radio"}
VALID_IMPORTANCES = {"High", "Medium", "Low"}


class QuestionGenerator:
    """
    Agent 2: Question Generator.
    Generates dynamic, non-repetitive follow-up questions tailored directly to the specific decision domain.
    Probes missing variables, constraints, risk tolerances, and trade-off priorities.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None) -> None:
        """
        Initialize QuestionGenerator with a GeminiService instance.

        :param gemini_service: Optional pre-configured GeminiService instance.
        """
        self.gemini_service: GeminiService = gemini_service if gemini_service is not None else GeminiService()

    def generate_questions(self, parsed_decision: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates 5 probing, domain-specific follow-up questions based on the parsed decision context.

        :param parsed_decision: Output dictionary from DecisionParser.parse_decision()
        :return: List of question dictionaries with schema:
                 [{"id": 1, "question": str, "category": str, "importance": str, "type": str}]
        """
        if not parsed_decision or not isinstance(parsed_decision, dict):
            logger.warning("Invalid or empty parsed_decision provided to QuestionGenerator.")
            return self._get_fallback_questions("General")

        dec_type = parsed_decision.get("decision_type", "General")
        missing_info = parsed_decision.get("unknown_information", parsed_decision.get("missing_information", []))
        options = parsed_decision.get("possible_options", [])

        system_instruction = (
            "You are an expert Decision Analyst and Management Consultant. Your job is to ask sharp, "
            "domain-specific, highly probing follow-up questions tailored directly to the decision category. "
            "NEVER ask generic or canned questions. Every question must directly probe unstated variables, "
            "financial limits, risk tolerances, or trade-offs."
        )

        decision_context = json.dumps(parsed_decision, indent=2)

        prompt = f"""
Decision Category: {dec_type}
Options Evaluated: {json.dumps(options)}
Identified Unknown Information: {json.dumps(missing_info)}

Structured Decision Context:
{decision_context}

Generate 5 dynamic, highly relevant follow-up questions specific to this exact decision domain ({dec_type}).

Domain Specificity Guidelines:
- If Career Decision (job switch, promo): Probe salary differential, equity structure, learning velocity, manager quality, work-life balance, commute/relocation.
- If Business/Startup Decision: Probe customer acquisition cost (CAC), runway, unit economics, competition, execution capability.
- If Education/Higher Studies (e.g. MS in US): Probe tuition debt, scholarship options, visa/job market risk, post-graduation salary expectations, ROI timeline.
- If Financial/Investment: Probe liquid savings buffer, investment horizon, tax implications, loss tolerance percentage.
- If Tech/Laptop Purchase: Probe primary use cases (gaming, coding, video editing), portability vs power, budget cap, expected lifespan.

Return ONLY a valid JSON array of objects matching this exact schema:
[
  {{
    "id": 1,
    "question": "Domain-specific question probing missing constraints or choices",
    "category": "Financial",
    "importance": "High",
    "type": "text"
  }},
  {{
    "id": 2,
    "question": "On a scale of 1-10, how risk-averse are you regarding this specific transition?",
    "category": "Risk",
    "importance": "High",
    "type": "scale"
  }}
]

Supported "type" values: "text", "scale", "choice", "select", "number".
Return ONLY valid JSON.
"""

        try:
            if not self.gemini_service.is_configured():
                logger.warning("Gemini API key not configured. Returning domain fallback questions.")
                return self._get_fallback_questions(dec_type)

            response_text = self.gemini_service.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )

            if not response_text or not response_text.strip():
                logger.error("Gemini returned empty response for question generation.")
                return self._get_fallback_questions(dec_type)

            parsed_questions = json.loads(response_text)

            if isinstance(parsed_questions, list):
                return self._validate_and_sanitize_questions(parsed_questions, dec_type)
            else:
                logger.warning("Response was valid JSON but not a list. Returning domain fallback questions.")
                return self._get_fallback_questions(dec_type)

        except json.JSONDecodeError as jde:
            logger.error(f"Failed to parse JSON response from Gemini: {jde}")
            return self._get_fallback_questions(dec_type)
        except Exception as e:
            logger.error(f"Unexpected error in generate_questions: {e}")
            return self._get_fallback_questions(dec_type)

    def _validate_and_sanitize_questions(self, questions: List[Dict[str, Any]], dec_type: str) -> List[Dict[str, Any]]:
        """Validates structure and assigns clean IDs and defaults."""
        sanitized: List[Dict[str, Any]] = []

        for idx, q in enumerate(questions, start=1):
            if not isinstance(q, dict) or "question" not in q or not str(q["question"]).strip():
                continue

            category = str(q.get("category", "General")).strip()
            if category not in VALID_CATEGORIES:
                category = "General"

            importance = str(q.get("importance", "Medium")).strip()
            if importance not in VALID_IMPORTANCES:
                importance = "Medium"

            q_type = str(q.get("type", "text")).strip().lower()
            if q_type not in VALID_TYPES:
                q_type = "text"

            sanitized.append({
                "id": idx,
                "question": str(q["question"]).strip(),
                "category": category,
                "importance": importance,
                "type": q_type
            })

        return sanitized if len(sanitized) >= 3 else self._get_fallback_questions(dec_type)

    def _get_fallback_questions(self, dec_type: str) -> List[Dict[str, Any]]:
        """Provides domain-tailored fallback questions if API is unconfigured."""
        dec_type_lower = dec_type.lower()

        if "career" in dec_type_lower or "job" in dec_type_lower:
            return [
                {"id": 1, "question": "What is the exact compensation gap (salary + bonus + equity) between your current role and the prospective role?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 2, "question": "On a scale of 1-10, how confident are you in the new company's leadership and financial stability?", "category": "Risk", "importance": "High", "type": "scale"},
                {"id": 3, "question": "How significantly will this move accelerate your growth towards your 3-year career milestone?", "category": "Career", "importance": "High", "type": "choice"},
                {"id": 4, "question": "What impact will this change have on your daily commute, working hours, and family flexibility?", "category": "Personal Preferences", "importance": "Medium", "type": "text"},
                {"id": 5, "question": "What is your emergency liquid runway (months of living expenses) if the transition takes time to stabilize?", "category": "Financial", "importance": "High", "type": "number"}
            ]
        elif "business" in dec_type_lower or "startup" in dec_type_lower:
            return [
                {"id": 1, "question": "What is your current monthly capital burn rate and total capital runway?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 2, "question": "On a scale of 1-10, how validated is customer demand for this offering?", "category": "Market", "importance": "High", "type": "scale"},
                {"id": 3, "question": "What is the single biggest operational or competitive barrier to achieving profitability?", "category": "Strategy", "importance": "High", "type": "text"},
                {"id": 4, "question": "How easily can this business model pivot if initial unit economics fail?", "category": "Execution", "importance": "Medium", "type": "choice"},
                {"id": 5, "question": "What is your target payback period (in months) on customer acquisition?", "category": "Financial", "importance": "High", "type": "number"}
            ]
        elif "education" in dec_type_lower or "study" in dec_type_lower or "ms" in dec_type_lower:
            return [
                {"id": 1, "question": "What is the total estimated tuition + living expense debt you will incur, net of scholarships?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 2, "question": "On a scale of 1-10, how strong is the post-graduation employment market for your target field?", "category": "Career", "importance": "High", "type": "scale"},
                {"id": 3, "question": "What is your target expected starting salary upon completing the program?", "category": "Financial", "importance": "High", "type": "number"},
                {"id": 4, "question": "What is your contingency plan if visa or work permit regulations become restrictive?", "category": "Risk", "importance": "High", "type": "text"},
                {"id": 5, "question": "How important is university brand equity vs practical industry networking in your decision?", "category": "Personal Preferences", "importance": "Medium", "type": "choice"}
            ]
        elif "invest" in dec_type_lower or "financial" in dec_type_lower or "stock" in dec_type_lower:
            return [
                {"id": 1, "question": "What percentage of your net liquid net worth does this investment represent?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 2, "question": "On a scale of 1-10, what is your emotional comfort level if this asset drops 25% in value temporarily?", "category": "Risk", "importance": "High", "type": "scale"},
                {"id": 3, "question": "What is your target investment time horizon before you need liquidity?", "category": "Time", "importance": "High", "type": "choice"},
                {"id": 4, "question": "What is the expected annual yield or growth rate driving this investment thesis?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 5, "question": "Have you accounted for capital gains tax and management fee drag?", "category": "Financial", "importance": "Medium", "type": "choice"}
            ]
        else:
            return [
                {"id": 1, "question": "What is your firm hard deadline for locking in this decision?", "category": "Time", "importance": "High", "type": "text"},
                {"id": 2, "question": "What is the maximum financial loss or budget strain you can absorb comfortably?", "category": "Financial", "importance": "High", "type": "text"},
                {"id": 3, "question": "On a scale of 1-10, how risk-averse are you regarding this choice?", "category": "Risk", "importance": "High", "type": "scale"},
                {"id": 4, "question": "Who are the key stakeholders who must be aligned before proceeding?", "category": "Family", "importance": "Medium", "type": "text"},
                {"id": 5, "question": "What primary success metric will prove this was the right choice 12 months from now?", "category": "Career", "importance": "High", "type": "text"}
            ]
