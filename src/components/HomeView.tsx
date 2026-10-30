import React, { useState } from 'react';
import { Brain, ArrowRight, Sparkles, Layers, Shield, HelpCircle, Check, Loader2 } from 'lucide-react';
import { DECISION_TEMPLATES } from '../data/templates';
import { ParsedDecision } from '../types';

interface HomeViewProps {
  decisionInput: string;
  setDecisionInput: (val: string) => void;
  onParseDecision: (text: string) => Promise<ParsedDecision | null>;
  parsedDecision: ParsedDecision | null;
  onProceedToQuestions: () => void;
}

export const HomeView: React.FC<HomeViewProps> = ({
  decisionInput,
  setDecisionInput,
  onParseDecision,
  parsedDecision,
  onProceedToQuestions,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTemplateClick = (key: string) => {
    const tmpl = DECISION_TEMPLATES[key];
    if (tmpl) {
      setDecisionInput(`${tmpl.title}\n\nContext:\n${tmpl.description}\n\nOptions under consideration:\n${tmpl.options.map((o, idx) => `${idx + 1}. ${o}`).join('\n')}`);
    }
  };

  const handleParse = async () => {
    if (!decisionInput.trim()) {
      setError("Please describe your decision context or select a scenario template.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const parsed = await onParseDecision(decisionInput);
      if (parsed) {
        // Automatically proceed to clarifying questions
        onProceedToQuestions();
      }
    } catch (err: any) {
      setError(err.message || "Failed to analyze decision input.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-12">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-950/80 via-slate-900 to-slate-950 border border-indigo-500/20 p-8 shadow-2xl">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold tracking-wide">
            <Sparkles className="w-3.5 h-3.5" />
            Executive Decision Intelligence Engine
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-100 tracking-tight leading-tight">
            Structure Complex Decisions with Multi-Agent AI
          </h1>
          <p className="text-slate-400 text-sm sm:text-base max-w-2xl leading-relaxed">
            Input any high-stakes career, financial, business, or purchasing decision. IntelliDecision AI parses trade-offs, generates clarifying questions, evaluates a multi-criteria decision matrix, and delivers a McKinsey-grade decision report.
          </p>
        </div>
      </div>

      {/* Quick Scenario Templates */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Quick Scenario Templates
          </h2>
          <span className="text-xs text-slate-500">Click to pre-fill context</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {Object.entries(DECISION_TEMPLATES).map(([key, tmpl]) => (
            <button
              key={key}
              onClick={() => handleTemplateClick(key)}
              className="text-left p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-850/80 transition-all group space-y-2"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800/40">
                  {tmpl.category}
                </span>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
              </div>
              <p className="font-semibold text-slate-200 text-xs sm:text-sm line-clamp-2 leading-snug">
                {tmpl.title}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Input Textarea */}
      <div className="space-y-4 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between">
          <label className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-400" />
            Describe Your Decision Context
          </label>
          {decisionInput && (
            <button
              onClick={() => setDecisionInput('')}
              className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
            >
              Clear Text
            </button>
          )}
        </div>

        <textarea
          value={decisionInput}
          onChange={(e) => setDecisionInput(e.target.value)}
          placeholder="e.g. Should I accept an engineering lead offer at a Series A AI startup ($160k + equity) or take a senior engineering manager role at Big Tech ($220k total comp)? Primary goals are rapid career growth and long-term financial upside..."
          rows={6}
          className="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500/80 focus:ring-1 focus:ring-indigo-500/80 rounded-xl p-4 text-slate-200 text-sm sm:text-base placeholder-slate-600 outline-none transition-all resize-y leading-relaxed"
        />

        {error && (
          <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs font-medium">
            {error}
          </div>
        )}

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pt-2">
          <div className="flex items-center gap-4 text-xs text-slate-400">
            <span className="flex items-center gap-1.5">
              <Shield className="w-4 h-4 text-emerald-400" />
              Multi-Agent Evaluation
            </span>
            <span className="flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-indigo-400" />
              Adaptive Clarifying Q&A
            </span>
          </div>

          <button
            onClick={handleParse}
            disabled={loading || !decisionInput.trim()}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Parsing Decision Context...
              </>
            ) : (
              <>
                <span>Start AI Analysis</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Parsed Decision Card if available */}
      {parsedDecision && (
        <div className="bg-slate-900 border border-indigo-500/30 rounded-2xl p-6 space-y-4 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
              <Check className="w-4 h-4 text-emerald-400" />
              Decision Context Parsed
            </div>
            <span className="px-2.5 py-1 rounded-full bg-indigo-950 text-indigo-300 text-xs font-semibold border border-indigo-800/40">
              {parsedDecision.decision_type} • {parsedDecision.risk_level}
            </span>
          </div>

          <h3 className="text-xl font-bold text-slate-100">{parsedDecision.title}</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1">
              <span className="text-slate-500 font-semibold block uppercase text-[10px]">Candidate Options:</span>
              <ul className="list-disc list-inside space-y-0.5 text-slate-200">
                {parsedDecision.candidate_options.map((opt, i) => (
                  <li key={i}>{opt}</li>
                ))}
              </ul>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1">
              <span className="text-slate-500 font-semibold block uppercase text-[10px]">Core Goal / Concern:</span>
              <p className="text-slate-200 leading-relaxed">{parsedDecision.primary_goal}</p>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={onProceedToQuestions}
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-2 transition-all"
            >
              <span>Proceed to Clarifying Questions</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
