import React, { useState } from 'react';
import { HelpCircle, ArrowRight, ArrowLeft, FastForward, CheckCircle2, Loader2, Sparkles } from 'lucide-react';
import { Question, ParsedDecision } from '../types';

interface QuestionsViewProps {
  questions: Question[];
  parsedDecision: ParsedDecision | null;
  userAnswers: Record<string, string>;
  setUserAnswers: React.Dispatch<React.SetStateAction<Record<string, string>>>;
  onAnalyze: () => Promise<void>;
  onBack: () => void;
}

export const QuestionsView: React.FC<QuestionsViewProps> = ({
  questions,
  parsedDecision,
  userAnswers,
  setUserAnswers,
  onAnalyze,
  onBack,
}) => {
  const [analyzing, setAnalyzing] = useState(false);

  const handleOptionSelect = (qId: string, optionText: string) => {
    setUserAnswers((prev) => ({
      ...prev,
      [qId]: optionText,
    }));
  };

  const handleTextChange = (qId: string, value: string) => {
    setUserAnswers((prev) => ({
      ...prev,
      [qId]: value,
    }));
  };

  const handleAutoFillAndSubmit = async () => {
    // Auto-fill unanswered questions with suggested option 1
    const filled: Record<string, string> = { ...userAnswers };
    questions.forEach((q) => {
      if (!filled[q.id] && q.suggested_options && q.suggested_options.length > 0) {
        filled[q.id] = q.suggested_options[0];
      }
    });
    setUserAnswers(filled);
    setAnalyzing(true);
    try {
      await onAnalyze();
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSubmit = async () => {
    setAnalyzing(true);
    try {
      await onAnalyze();
    } finally {
      setAnalyzing(false);
    }
  };

  const answeredCount = Object.keys(userAnswers).filter((k) => userAnswers[k]?.trim()).length;
  const progressPercent = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          disabled={analyzing}
          className="flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Context</span>
        </button>

        <button
          onClick={handleAutoFillAndSubmit}
          disabled={analyzing}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition-all"
        >
          <FastForward className="w-3.5 h-3.5 text-indigo-400" />
          <span>Skip & Auto-Fill All</span>
        </button>
      </div>

      {/* Decision Context Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 block">
            Target Decision Context
          </span>
          <h2 className="text-base font-bold text-slate-200">
            {parsedDecision?.title || "Decision Analysis"}
          </h2>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <span>Clarification Progress:</span>
          <span className="font-bold text-indigo-400">{answeredCount}/{questions.length} ({progressPercent}%)</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
        <div
          className="bg-indigo-500 h-full transition-all duration-300"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        {questions.map((q, idx) => {
          const currentAnswer = userAnswers[q.id] || "";
          return (
            <div
              key={q.id}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-lg hover:border-slate-700 transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800/40 text-xs font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    {q.category}
                  </span>
                </div>
                {currentAnswer && (
                  <span className="text-emerald-400 text-xs font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Answered
                  </span>
                )}
              </div>

              <h3 className="text-base font-semibold text-slate-100 leading-snug">
                {q.question}
              </h3>

              {/* Quick Choice Buttons */}
              {q.suggested_options && q.suggested_options.length > 0 && (
                <div className="space-y-1.5">
                  <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block">
                    Quick Choices:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {q.suggested_options.map((opt, oIdx) => {
                      const isSelected = currentAnswer === opt;
                      return (
                        <button
                          key={oIdx}
                          type="button"
                          onClick={() => handleOptionSelect(q.id, opt)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all text-left ${
                            isSelected
                              ? 'bg-indigo-600 text-white border border-indigo-400 font-semibold shadow-md shadow-indigo-600/30'
                              : 'bg-slate-950 text-slate-300 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-800/60'
                          }`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Custom Input */}
              <input
                type="text"
                value={currentAnswer}
                onChange={(e) => handleTextChange(q.id, e.target.value)}
                placeholder="Or type a custom specific answer..."
                className="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-slate-200 placeholder-slate-600 outline-none transition-all"
              />
            </div>
          );
        })}
      </div>

      {/* Action Submit Row */}
      <div className="pt-4 flex items-center justify-between border-t border-slate-800">
        <span className="text-xs text-slate-500">
          Ready to synthesize multi-agent findings?
        </span>

        <button
          onClick={handleSubmit}
          disabled={analyzing}
          className="px-8 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 flex items-center gap-2 transition-all cursor-pointer"
        >
          {analyzing ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Synthesizing Strategy Report...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Generate Executive Report</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};
