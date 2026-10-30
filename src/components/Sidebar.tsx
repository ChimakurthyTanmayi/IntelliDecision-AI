import React from 'react';
import { Brain, Sparkles, History, FileText, CheckCircle2, ShieldAlert, Cpu } from 'lucide-react';

interface SidebarProps {
  currentStep: string;
  setStep: (step: string) => void;
  geminiConfigured: boolean;
  historyCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentStep,
  setStep,
  geminiConfigured,
  historyCount,
}) => {
  return (
    <aside className="w-64 bg-[#0b0f1a] border-r border-slate-800 flex flex-col justify-between p-4 min-h-screen text-slate-200 shrink-0">
      <div className="space-y-6">
        {/* Brand */}
        <div className="flex items-center gap-3 px-2 pt-2">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 shadow-lg shadow-indigo-500/20 text-white">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-extrabold text-base text-slate-100 tracking-tight leading-none">IntelliDecision AI</h1>
            <p className="text-[11px] font-semibold text-indigo-400 mt-1 uppercase tracking-wider">Multi-Agent Strategy</p>
          </div>
        </div>

        {/* API Status Badge */}
        <div className={`p-3 rounded-xl border ${geminiConfigured ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-400' : 'bg-amber-950/30 border-amber-500/30 text-amber-300'} text-xs font-medium flex items-center justify-between`}>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${geminiConfigured ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
            <span>{geminiConfigured ? 'Gemini 2.5 Active' : 'Demo Mode Active'}</span>
          </div>
          <Sparkles className="w-3.5 h-3.5 opacity-75" />
        </div>

        {/* Navigation */}
        <nav className="space-y-1 text-sm font-medium">
          <button
            onClick={() => setStep('HOME')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all ${
              currentStep === 'HOME' || currentStep === 'QUESTIONS'
                ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-semibold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>New Decision</span>
          </button>

          <button
            onClick={() => setStep('REPORT')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all ${
              currentStep === 'REPORT'
                ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-semibold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Active Report</span>
          </button>

          <button
            onClick={() => setStep('HISTORY')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition-all ${
              currentStep === 'HISTORY'
                ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-semibold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <div className="flex items-center gap-3">
              <History className="w-4 h-4" />
              <span>Session History</span>
            </div>
            {historyCount > 0 && (
              <span className="px-2 py-0.5 text-xs font-bold bg-indigo-900/60 text-indigo-300 rounded-full border border-indigo-500/30">
                {historyCount}
              </span>
            )}
          </button>
        </nav>

        {/* Core Pillars */}
        <div className="pt-4 border-t border-slate-800/80 space-y-2">
          <p className="px-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">Multi-Agent Simulation</p>
          <div className="space-y-1.5 text-xs text-slate-400">
            <div className="flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-slate-800/30">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>Strategic Advisor</span>
            </div>
            <div className="flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-slate-800/30">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              <span>Risk & Downside Analyst</span>
            </div>
            <div className="flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-slate-800/30">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span>Decision Matrix Engine</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer info */}
      <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-500 text-center">
        IntelliDecision v2.5 • Gemini Powered
      </div>
    </aside>
  );
};
