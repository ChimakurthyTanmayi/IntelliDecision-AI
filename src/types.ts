export interface ParsedDecision {
  title: string;
  decision_type: string;
  risk_level: string;
  primary_goal: string;
  candidate_options: string[];
  core_concerns: string[];
}

export interface Question {
  id: string;
  question: string;
  category: string;
  suggested_options: string[];
}

export interface DecisionMatrixScore {
  option_name: string;
  weighted_total_score: number;
  key_advantage: string;
  scores: Record<string, number>;
}

export interface DecisionMatrix {
  matrix_summary: string;
  criteria_list: string[];
  options_scores: DecisionMatrixScore[];
}

export interface RiskDimension {
  score: number;
  level: string;
  description: string;
  mitigation: string;
}

export interface RiskAnalysis {
  risk_summary: string;
  risk_dimensions: Record<string, RiskDimension>;
}

export interface OptionSWOT {
  option_name: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

export interface SWOTAnalysis {
  swot_by_option: OptionSWOT[];
}

export interface DecisionReport {
  title: string;
  recommended_option: string;
  confidence_score: number;
  executive_summary: string;
  why_recommended_wins: string[];
  why_others_are_weaker: string[];
  decision_matrix: DecisionMatrix;
  risk_analysis: RiskAnalysis;
  swot_analysis: SWOTAnalysis;
  hidden_assumptions: string[];
  cognitive_biases: string[];
  action_plan_30_60_90: string[];
  contingency_triggers: string[];
}

export interface HistoryItem {
  id: string;
  timestamp: string;
  decisionInput: string;
  report: DecisionReport;
}

export interface ScenarioTemplate {
  title: string;
  category: string;
  description: string;
  options: string[];
}
