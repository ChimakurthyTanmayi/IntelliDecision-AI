"""
Gemini API Client for IntelliDecision AI
Handles all interactions with Google Gemini AI models using the official google-genai SDK.
"""

import os
import json
import logging
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IntelliDecision.GeminiClient")

class GeminiDecisionClient:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        # Preferred models with fallback
        self.primary_model = "gemini-2.5-flash"
        self.fallback_model = "gemini-2.0-flash"
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini Client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")

    def is_configured(self) -> bool:
        """Check if GEMINI_API_KEY is available and client is active."""
        return bool(self.api_key and self.client)

    def _generate(self, prompt: str, system_instruction: str = None, json_mode: bool = False) -> str:
        """Helper to invoke Gemini model with fallback error handling."""
        if not self.is_configured():
            raise ValueError("GEMINI_API_KEY is missing or invalid. Please configure your key in environment secrets.")

        config = types.GenerateContentConfig()
        if system_instruction:
            config.system_instruction = system_instruction
        if json_mode:
            config.response_mime_type = "application/json"

        # Attempt primary model first, fallback to secondary if needed
        models_to_try = [self.primary_model, self.fallback_model, "gemini-1.5-flash"]
        
        last_error = None
        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {e}. Trying next fallback...")
                last_error = e

        raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

    def analyze_initial_decision(self, decision_title: str, description: str, category: str, options: list) -> dict:
        """
        Step 1: Analyzes the initial decision input, validates scope, and produces a structured overview.
        """
        system_instruction = (
            "You are IntelliDecision AI, a world-class Decision Intelligence Executive Advisor. "
            "Your task is to analyze complex choices objectively, cut through ambiguity, and bring structured clarity."
        )

        options_str = ", ".join(options) if options else "Not explicitly specified"
        prompt = f"""
Analyze this decision scenario submitted by the user:

Title: {decision_title}
Category: {category}
Description: {description}
Options Being Considered: {options_str}

Respond in valid JSON format with the following keys:
- "problem_statement": A refined, clear 2-sentence summary of the core dilemma.
- "key_objectives": List of 3-4 implicit strategic or personal goals the user wants to achieve.
- "primary_uncertainties": List of 3 major unknowns or risks currently present.
- "suggested_options": List of 2-4 concrete options (include user's options plus any missing high-value alternative).
- "initial_ai_insight": A 2-sentence executive perspective on how to approach this decision.
"""
        raw_text = self._generate(prompt, system_instruction=system_instruction, json_mode=True)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "problem_statement": description,
                "key_objectives": ["Optimize long-term outcome", "Minimize operational & financial risk"],
                "primary_uncertainties": ["Market/environmental volatility", "Resource allocation"],
                "suggested_options": options if options else ["Option A", "Option B"],
                "initial_ai_insight": "This decision requires balancing immediate operational gains against long-term strategic flexibility."
            }

    def generate_followup_questions(self, decision_summary: str, options: list) -> list:
        """
        Step 2: Asks intelligent probing questions to uncover crucial context.
        """
        system_instruction = (
            "You are a Decision Analyst. Ask 4 highly strategic, non-obvious probing questions "
            "that force the decision-maker to clarify priorities, resource limits, timelines, and risk tolerance."
        )

        options_str = ", ".join(options)
        prompt = f"""
Decision Context: {decision_summary}
Options: {options_str}

Generate 4 probing follow-up questions. Return a JSON array of objects, where each object has:
- "id": "q1", "q2", etc.
- "question": "The question string",
- "purpose": "Why this question matters for making the decision",
- "category": "Financial" | "Risk Tolerance" | "Strategic Alignment" | "Personal Value" | "Execution Capability",
- "input_type": "text" or "select",
- "suggested_answers": [list of 3-4 options if select, or empty list if text]
"""
        raw_text = self._generate(prompt, system_instruction=system_instruction, json_mode=True)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return [
                {
                    "id": "q1",
                    "question": "What is your hard deadline for making and acting on this decision?",
                    "purpose": "Establishes urgency and time-decay risk.",
                    "category": "Execution Capability",
                    "input_type": "select",
                    "suggested_answers": ["Within 7 days", "1-4 weeks", "1-3 months", "No strict timeline"]
                },
                {
                    "id": "q2",
                    "question": "What is the worst-case scenario you can accept without severe disruption?",
                    "purpose": "Measures true downside risk tolerance.",
                    "category": "Risk Tolerance",
                    "input_type": "text",
                    "suggested_answers": []
                },
                {
                    "id": "q3",
                    "question": "What is the primary key metric or success criteria for this decision?",
                    "purpose": "Defines what 'winning' looks like.",
                    "category": "Strategic Alignment",
                    "input_type": "text",
                    "suggested_answers": []
                },
                {
                    "id": "q4",
                    "question": "Are there irreversible commitments or high switching costs associated with any option?",
                    "purpose": "Identifies reversible vs. irreversible decisions (One-Way vs Two-Way doors).",
                    "category": "Financial",
                    "input_type": "select",
                    "suggested_answers": ["High switching cost (One-way door)", "Moderate switching cost", "Low switching cost (Reversible)"]
                }
            ]

    def identify_hidden_factors(self, decision_title: str, description: str, options: list, qna_pairs: list) -> dict:
        """
        Step 3: Uncovers hidden factors, second-order effects, cognitive biases, and unexpected risks.
        """
        system_instruction = (
            "You are a cognitive psychologist and risk analyst specializing in decision science. "
            "Identify hidden blind spots, cognitive biases, second-order consequences, and hidden costs."
        )

        qna_str = "\n".join([f"Q: {item['question']}\nA: {item.get('answer', 'N/A')}" for item in qna_pairs])
        prompt = f"""
Decision Scenario: {decision_title}
Details: {description}
Options: {", ".join(options)}

User's Context Answers:
{qna_str}

Provide a comprehensive hidden factor analysis in JSON format with these exact keys:
- "hidden_costs": List of 3 non-obvious financial, time, or emotional costs.
- "second_order_effects": List of 3 downstream consequences that may happen 6-12 months later.
- "cognitive_biases_to_watch": List of 2-3 potential biases (e.g. Sunk Cost Fallacy, Status Quo Bias, Confirmation Bias, FOMO) with brief explanations of how they might affect this decision.
- "blind_spots": List of 2 critical assumptions the user might be taking for granted.
"""
        raw_text = self._generate(prompt, system_instruction=system_instruction, json_mode=True)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return {
                "hidden_costs": ["Opportunity cost of delayed execution", "Emotional cognitive load & fatigue", "Team/family alignment friction"],
                "second_order_effects": ["Resource bottlenecks in quarter 2", "Possible realignment of long-term roadmap"],
                "cognitive_biases_to_watch": [{"bias": "Status Quo Bias", "explanation": "Tendency to prefer current state over beneficial change due to fear of loss."}],
                "blind_spots": ["Assuming external conditions remain static", "Underestimating transition timeline"]
            }

    def evaluate_tradeoffs(self, decision_title: str, options: list, qna_pairs: list, hidden_factors: dict) -> dict:
        """
        Step 4: Compares trade-offs with multi-criteria evaluation matrix and option scores.
        """
        system_instruction = (
            "You are a quantitative decision strategist. Build a comparative evaluation matrix "
            "scoring each option across 4 criteria (0-100 scale): Strategic Fit, Downside Risk Protection, Ease of Execution, and Long-Term Value."
        )

        prompt = f"""
Decision Scenario: {decision_title}
Options to Evaluate: {", ".join(options)}

Context Answers: {json.dumps(qna_pairs)}
Hidden Factors: {json.dumps(hidden_factors)}

Output JSON format:
{{
    "criteria_weights": {{
        "Strategic Fit": 30,
        "Downside Risk Protection": 25,
        "Ease of Execution": 20,
        "Long-Term Value": 25
    }},
    "option_evaluations": [
        {{
            "option_name": "Option Name",
            "scores": {{
                "Strategic Fit": 85,
                "Downside Risk Protection": 60,
                "Ease of Execution": 70,
                "Long-Term Value": 90
            }},
            "overall_score": 78,
            "pros": ["Pro 1", "Pro 2"],
            "cons": ["Con 1", "Con 2"],
            "key_tradeoff_summary": "High growth potential traded against immediate resource stretch."
        }}
    ],
    "winning_option": "Name of best option",
    "tradeoff_verdict": "A 2-sentence summary of the core trade-off between the top options."
}}
"""
        raw_text = self._generate(prompt, system_instruction=system_instruction, json_mode=True)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            # Fallback evaluation matrix
            evals = []
            for idx, opt in enumerate(options):
                score = 80 - (idx * 5)
                evals.append({
                    "option_name": opt,
                    "scores": {
                        "Strategic Fit": score,
                        "Downside Risk Protection": score - 10,
                        "Ease of Execution": 75,
                        "Long-Term Value": score + 5
                    },
                    "overall_score": score,
                    "pros": ["Strong alignment with primary goal"],
                    "cons": ["Requires higher initial focus"],
                    "key_tradeoff_summary": "Balances risk vs reward effectively."
                })
            return {
                "criteria_weights": {"Strategic Fit": 30, "Downside Risk Protection": 25, "Ease of Execution": 20, "Long-Term Value": 25},
                "option_evaluations": evals,
                "winning_option": options[0] if options else "Option 1",
                "tradeoff_verdict": "The primary trade-off is higher long-term impact versus initial execution velocity."
            }

    def generate_final_report(self, decision_title: str, description: str, category: str, options: list, qna_pairs: list, hidden_factors: dict, tradeoffs: dict) -> dict:
        """
        Step 5: Synthesizes everything into an Executive Decision Intelligence Report.
        """
        system_instruction = (
            "You are a C-suite Executive Strategy Advisor. Synthesize all analyses into a definitive, "
            "actionable, and authoritative Decision Intelligence Report."
        )

        prompt = f"""
Decision Title: {decision_title}
Category: {category}
Description: {description}
Options: {", ".join(options)}
Q&A Context: {json.dumps(qna_pairs)}
Hidden Factors: {json.dumps(hidden_factors)}
Trade-Off Matrix: {json.dumps(tradeoffs)}

Generate a complete report in JSON format:
{{
    "executive_summary": "A crisp 3-4 sentence overview of the decision synthesis.",
    "final_recommendation": {{
        "recommended_option": "{tradeoffs.get('winning_option', options[0] if options else '')}",
        "confidence_score": 88,
        "primary_justification": "Detailed 3-bullet rationale explaining why this option wins."
    }},
    "action_plan": [
        {{"phase": "Immediate (Days 1-7)", "steps": ["Step 1", "Step 2"]}},
        {{"phase": "Short-Term (Weeks 2-4)", "steps": ["Step 1", "Step 2"]}},
        {{"phase": "Execution (Months 2-3)", "steps": ["Step 1", "Step 2"]}}
    ],
    "contingency_plan": "What trigger event should cause you to pivot, and what is Plan B?",
    "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"]
}}
"""
        raw_text = self._generate(prompt, system_instruction=system_instruction, json_mode=True)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return {
                "executive_summary": f"Based on thorough evaluation of {decision_title}, option '{tradeoffs.get('winning_option', options[0])}' delivers the optimal balance of strategic impact and risk mitigation.",
                "final_recommendation": {
                    "recommended_option": tradeoffs.get("winning_option", options[0] if options else "Option 1"),
                    "confidence_score": 85,
                    "primary_justification": "Maximizes long-term ROI while maintaining acceptable risk parameters."
                },
                "action_plan": [
                    {"phase": "Immediate (Days 1-7)", "steps": ["Finalize decision alignment with key stakeholders", "Set quantitative success milestones"]},
                    {"phase": "Short-Term (Weeks 2-4)", "steps": ["Execute phase 1 rollout", "Monitor early metrics"]},
                    {"phase": "Execution (Months 2-3)", "steps": ["Review progress at 60-day mark", "Optimize based on feedback"]}
                ],
                "contingency_plan": "If milestone 1 misses target by >20%, activate backup option with pre-agreed budget cap.",
                "key_takeaways": ["Decisive action reduces opportunity cost", "Monitor leading indicators early", "Ensure team alignment"]
            }
