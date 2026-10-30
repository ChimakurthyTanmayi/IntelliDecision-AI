import React from 'react';
import { History, Trophy, ArrowRight, Trash2, Calendar, FileText, Brain } from 'lucide-react';
import { HistoryItem } from '../types';

interface HistoryViewProps {
  history: HistoryItem[];
  onSelectReport: (item: HistoryItem) => void;
  onDeleteReport: (id: string) => void;
  onClearHistory: () => void;
  onNewDecision: () => void;
}

export const HistoryView: React.FC<HistoryViewProps> = ({
  history,
  onSelectReport,
  onDeleteReport,
  onClearHistory,
  onNewDecision,
}) => {
  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 flex items-center gap-2">
            <History className="w-6 h-6 text-indigo-400" />
            Decision History
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Revisit past analyzed decisions and strategic reports.
          </p>
        </div>

        {history.length > 0 && (
          <button
            onClick={onClearHistory}
            className="px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/50 text-rose-300 text-xs font-semibold border border-rose-800/40 flex items-center gap-1.5 transition-all self-start sm:self-auto"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear History</span>
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <Brain className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-lg font-bold text-slate-200">No History Records Found</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            You haven't run any decision analyses yet. Start a new decision to save its report automatically.
          </p>
          <button
            onClick={onNewDecision}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition-all inline-flex items-center gap-2"
          >
            <span>Start New Decision</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-slate-900 border border-slate-800 hover:border-indigo-500/40 rounded-2xl p-5 space-y-3 transition-all group"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                  <span>{item.timestamp}</span>
                </div>

                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-300 text-[11px] font-bold border border-emerald-500/30 flex items-center gap-1">
                    <Trophy className="w-3 h-3" />
                    Win: {item.report.recommended_option}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-purple-950/80 text-purple-300 text-[11px] font-bold border border-purple-500/30">
                    {item.report.confidence_score}% Conf.
                  </span>
                </div>
              </div>

              <h3 className="text-base font-bold text-slate-100 group-hover:text-indigo-300 transition-colors">
                {item.report.title}
              </h3>

              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                {item.report.executive_summary}
              </p>

              <div className="flex items-center justify-between pt-2">
                <button
                  onClick={() => onDeleteReport(item.id)}
                  className="text-slate-500 hover:text-rose-400 text-xs font-semibold flex items-center gap-1 transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Delete</span>
                </button>

                <button
                  onClick={() => onSelectReport(item)}
                  className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-1.5 transition-all"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Open Full Report</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
