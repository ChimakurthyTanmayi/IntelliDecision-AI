import React, { useState } from 'react';
import {
  Trophy,
  ShieldAlert,
  Zap,
  Target,
  FileText,
  Download,
  RotateCcw,
  History,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Brain,
  Calendar,
  Layers,
  Sparkles
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend
} from 'recharts';
import { jsPDF } from 'jspdf';
import { DecisionReport, ParsedDecision } from '../types';

interface ReportViewProps {
  report: DecisionReport | null;
  parsedDecision: ParsedDecision | null;
  onNewDecision: () => void;
  onGoHistory: () => void;
  historyCount: number;
}

export const ReportView: React.FC<ReportViewProps> = ({
  report,
  parsedDecision,
  onNewDecision,
  onGoHistory,
  historyCount,
}) => {
  const [activeSwotTab, setActiveSwotTab] = useState(0);

  if (!report) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-slate-900 border border-slate-800 rounded-2xl text-center space-y-4">
        <Brain className="w-12 h-12 text-indigo-400 mx-auto" />
        <h2 className="text-xl font-bold text-slate-100">No Active Decision Report</h2>
        <p className="text-sm text-slate-400">Please enter a decision prompt on the home screen to synthesize a strategic report.</p>
        <button
          onClick={onNewDecision}
          className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition-all"
        >
          ← Return to Decision Entry
        </button>
      </div>
    );
  }

  // Export handlers
  const handleExportMarkdown = () => {
    const mdContent = `# ${report.title}
*Executive Decision Intelligence Report*

## Executive Summary
**Recommended Choice:** ${report.recommended_option} (Confidence: ${report.confidence_score}%)

${report.executive_summary}

### Why Recommended Option Wins
${report.why_recommended_wins.map((item) => `- ✅ ${item}`).join('\n')}

### Why Alternatives Are Weaker
${report.why_others_are_weaker.map((item) => `- ⚠️ ${item}`).join('\n')}

## Multi-Criteria Decision Matrix
${report.decision_matrix.matrix_summary}

${report.decision_matrix.options_scores
  .map((opt) => `### ${opt.option_name} (Score: ${opt.weighted_total_score}/100)\n- **Key Advantage:** ${opt.key_advantage}`)
  .join('\n\n')}

## 30-60-90 Day Execution Roadmap
${report.action_plan_30_60_90.map((step, idx) => `${idx + 1}. ${step}`).join('\n')}
`;

    const blob = new Blob([mdContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.title.replace(/[^a-z0-9]/gi, '_')}_Report.md`;
    a.click();
  };

  const handleExportJSON = () => {
    const jsonStr = JSON.stringify(report, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.title.replace(/[^a-z0-9]/gi, '_')}_Report.json`;
    a.click();
  };

  const handleExportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text(report.title, 14, 20);
    doc.setFontSize(12);
    doc.text(`Winning Recommendation: ${report.recommended_option}`, 14, 30);
    doc.text(`Confidence Score: ${report.confidence_score}%`, 14, 38);

    doc.setFontSize(10);
    const lines = doc.splitTextToSize(report.executive_summary, 180);
    doc.text(lines, 14, 48);

    let yPos = 48 + lines.length * 6 + 10;
    doc.setFontSize(14);
    doc.text('Key Advantages:', 14, yPos);
    yPos += 8;

    doc.setFontSize(10);
    report.why_recommended_wins.forEach((w) => {
      const wLines = doc.splitTextToSize(`- ${w}`, 180);
      doc.text(wLines, 14, yPos);
      yPos += wLines.length * 5 + 2;
    });

    doc.save(`${report.title.replace(/[^a-z0-9]/gi, '_')}_Report.pdf`);
  };

  // Recharts Data Prep
  const optionScoresData = report.decision_matrix.options_scores.map((opt) => ({
    name: opt.option_name,
    Score: opt.weighted_total_score,
  }));

  const riskDimsData = Object.entries(report.risk_analysis.risk_dimensions).map(([key, val]) => ({
    category: key,
    Severity: val.score,
  }));

  const criteriaList = report.decision_matrix.criteria_list || [
    'Financial Return',
    'Growth Potential',
    'Learning Opportunity',
    'Long-Term Value',
    'Feasibility & Speed',
    'Low Risk Advantage',
  ];

  const radarData = criteriaList.map((crit) => {
    const row: Record<string, any> = { criterion: crit };
    report.decision_matrix.options_scores.forEach((opt) => {
      row[opt.option_name] = opt.scores?.[crit] || 70;
    });
    return row;
  });

  const swotList = report.swot_analysis.swot_by_option || [];
  const currentSwot = swotList[activeSwotTab] || swotList[0];

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16">
      {/* Top Header & Actions */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            Executive Strategy Synthesis
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
            {report.title}
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={handleExportMarkdown}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-800 flex items-center gap-1.5 transition-all"
          >
            <FileText className="w-3.5 h-3.5 text-indigo-400" />
            <span>Markdown</span>
          </button>

          <button
            onClick={handleExportPDF}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-800 flex items-center gap-1.5 transition-all"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>PDF Export</span>
          </button>

          <button
            onClick={handleExportJSON}
            className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-800 flex items-center gap-1.5 transition-all"
          >
            <FileText className="w-3.5 h-3.5 text-amber-400" />
            <span>JSON</span>
          </button>

          <button
            onClick={onNewDecision}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-indigo-600/20 transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>New Decision</span>
          </button>

          <button
            onClick={onGoHistory}
            className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 flex items-center gap-1.5 transition-all"
          >
            <History className="w-3.5 h-3.5" />
            <span>History ({historyCount})</span>
          </button>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 space-y-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Decision Domain</span>
            <Target className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-base font-bold text-indigo-300 truncate">
            {parsedDecision?.decision_type || 'Strategic Choice'}
          </div>
          <div className="text-[11px] text-slate-500">Categorized Scope</div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 space-y-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Winning Choice</span>
            <Trophy className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-base font-bold text-emerald-400 truncate">
            {report.recommended_option}
          </div>
          <div className="text-[11px] text-slate-500">Top Recommended Path</div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 space-y-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Risk Severity</span>
            <ShieldAlert className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-base font-bold text-amber-400">
            {parsedDecision?.risk_level || 'Medium Risk'}
          </div>
          <div className="text-[11px] text-slate-500">Evaluated Downside</div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 space-y-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>Confidence Index</span>
            <Zap className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-base font-bold text-purple-400">
            {report.confidence_score}%
          </div>
          <div className="text-[11px] text-slate-500">AI Recommendation Certainty</div>
        </div>
      </div>

      {/* Winning Recommendation Card */}
      <div className="bg-gradient-to-br from-indigo-950/60 via-slate-900 to-slate-950 border border-indigo-500/30 rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-indigo-500/20 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
                Recommended Strategic Choice
              </span>
              <h2 className="text-xl sm:text-2xl font-extrabold text-slate-100">
                {report.recommended_option}
              </h2>
            </div>
          </div>

          <span className="self-start sm:self-auto px-3 py-1 rounded-full bg-emerald-950/80 text-emerald-300 text-xs font-bold border border-emerald-500/30">
            Confidence Index: {report.confidence_score}%
          </span>
        </div>

        <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
          {report.executive_summary}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          {/* Why Wins */}
          <div className="bg-slate-950/80 border border-emerald-500/20 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              Why This Option Wins
            </h3>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              {report.why_recommended_wins.map((win, idx) => (
                <li key={idx} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-emerald-400 font-bold shrink-0">✓</span>
                  <span>{win}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Why Others Are Weaker */}
          <div className="bg-slate-950/80 border border-rose-500/20 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-rose-400 flex items-center gap-2">
              <XCircle className="w-4 h-4" />
              Why Other Options Are Weaker
            </h3>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              {report.why_others_are_weaker.map((weak, idx) => (
                <li key={idx} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-rose-400 font-bold shrink-0">✗</span>
                  <span>{weak}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Multi-Criteria Decision Evaluation Matrix */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            Multi-Criteria Decision Evaluation Matrix
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {report.decision_matrix.matrix_summary}
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs sm:text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[11px] font-bold tracking-wider">
              <tr>
                <th className="p-3 rounded-l-xl">Candidate Option</th>
                <th className="p-3 text-center">Weighted Score</th>
                <th className="p-3">Key Strategic Advantage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {report.decision_matrix.options_scores.map((opt, idx) => (
                <tr key={idx} className="hover:bg-slate-850/50 transition-colors">
                  <td className="p-3 font-semibold text-slate-200">
                    {opt.option_name}
                  </td>
                  <td className="p-3">
                    <div className="flex items-center gap-2 justify-center">
                      <div className="w-24 bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="bg-indigo-500 h-full rounded-full"
                          style={{ width: `${opt.weighted_total_score}%` }}
                        />
                      </div>
                      <span className="font-bold text-indigo-300">{opt.weighted_total_score}/100</span>
                    </div>
                  </td>
                  <td className="p-3 text-slate-400">{opt.key_advantage}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Interactive Recharts Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Option Total Scores Bar Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <h4 className="text-sm font-bold text-slate-200">
            Option Total Scores Comparison
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={optionScoresData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} interval={0} />
                <YAxis domain={[0, 100]} stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#f8fafc' }}
                />
                <Bar dataKey="Score" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Dimensions Bar Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <h4 className="text-sm font-bold text-slate-200">
            Risk Severity per Dimension (1-10)
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDimsData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="category" stroke="#64748b" fontSize={11} />
                <YAxis domain={[0, 10]} stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#f8fafc' }}
                />
                <Bar dataKey="Severity" fill="#f43f5e" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Multi-Criteria Radar Overlay Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3 lg:col-span-2">
          <h4 className="text-sm font-bold text-slate-200">
            Multi-Criteria Radar Comparison
          </h4>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="criterion" stroke="#94a3b8" fontSize={11} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" fontSize={10} />
                {report.decision_matrix.options_scores.map((opt, i) => {
                  const colors = ['#6366f1', '#38bdf8', '#c084fc', '#34d399'];
                  const color = colors[i % colors.length];
                  return (
                    <Radar
                      key={opt.option_name}
                      name={opt.option_name}
                      dataKey={opt.option_name}
                      stroke={color}
                      fill={color}
                      fillOpacity={0.25}
                    />
                  );
                })}
                <Legend wrapperStyle={{ fontSize: '11px', color: '#cbd5e1' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#f8fafc' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Multi-Dimensional Risk Analysis Grid */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            Multi-Dimensional Risk Analysis
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {report.risk_analysis.risk_summary}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(report.risk_analysis.risk_dimensions).map(([dimKey, dim]) => {
            const levelColor =
              dim.score <= 3
                ? 'text-emerald-400 border-emerald-500/30 bg-emerald-950/30'
                : dim.score >= 7
                ? 'text-rose-400 border-rose-500/30 bg-rose-950/30'
                : 'text-amber-400 border-amber-500/30 bg-amber-950/30';

            return (
              <div
                key={dimKey}
                className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-200 text-sm">{dimKey} Risk</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-bold border ${levelColor}`}>
                      {dim.score}/10 ({dim.level})
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                    {dim.description}
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-850 text-xs text-indigo-300 bg-indigo-950/20 p-2 rounded-lg">
                  <span className="font-bold block text-[10px] text-indigo-400 uppercase">Mitigation:</span>
                  {dim.mitigation}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* SWOT Analysis Cards per Option */}
      {swotList.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            SWOT Analysis per Candidate Option
          </h3>

          {/* Option Tabs */}
          <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
            {swotList.map((optSwot, idx) => (
              <button
                key={idx}
                onClick={() => setActiveSwotTab(idx)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeSwotTab === idx
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                {optSwot.option_name}
              </button>
            ))}
          </div>

          {currentSwot && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-emerald-950/20 border border-emerald-500/20 p-4 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                  💪 Strengths (Internal)
                </h4>
                <ul className="space-y-1 text-xs text-slate-300">
                  {currentSwot.strengths?.map((s, i) => (
                    <li key={i}>• {s}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-rose-950/20 border border-rose-500/20 p-4 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider">
                  ⚠️ Weaknesses (Internal)
                </h4>
                <ul className="space-y-1 text-xs text-slate-300">
                  {currentSwot.weaknesses?.map((w, i) => (
                    <li key={i}>• {w}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-sky-950/20 border border-sky-500/20 p-4 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider">
                  🚀 Opportunities (External)
                </h4>
                <ul className="space-y-1 text-xs text-slate-300">
                  {currentSwot.opportunities?.map((o, i) => (
                    <li key={i}>• {o}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-amber-950/20 border border-amber-500/20 p-4 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider">
                  ⚡ Threats (External)
                </h4>
                <ul className="space-y-1 text-xs text-slate-300">
                  {currentSwot.threats?.map((t, i) => (
                    <li key={i}>• {t}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Cognitive Biases & Hidden Assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <h3 className="text-base font-bold text-amber-400 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Unexamined Hidden Assumptions
          </h3>
          <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
            {report.hidden_assumptions.map((item, idx) => (
              <li key={idx} className="bg-slate-950 p-3 rounded-xl border border-slate-800 leading-relaxed">
                ❓ {item}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <h3 className="text-base font-bold text-purple-400 flex items-center gap-2">
            <Brain className="w-5 h-5" />
            Identified Cognitive Biases
          </h3>
          <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
            {report.cognitive_biases.map((item, idx) => (
              <li key={idx} className="bg-slate-950 p-3 rounded-xl border border-slate-800 leading-relaxed">
                🧠 {item}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 30-60-90 Day Execution Roadmap & Contingency Triggers */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-indigo-400" />
            30-60-90 Day Execution Roadmap & Downside Triggers
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Structured execution plan to lock in gains and establish emergency contingency gates.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {report.action_plan_30_60_90.map((phaseText, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-2">
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
                Phase {idx + 1} Roadmap
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {phaseText}
              </p>
            </div>
          ))}
        </div>

        {report.contingency_triggers?.length > 0 && (
          <div className="bg-rose-950/20 border border-rose-500/30 rounded-xl p-4 space-y-2">
            <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" />
              Downside Contingency Triggers
            </h4>
            <ul className="space-y-1 text-xs text-rose-200">
              {report.contingency_triggers.map((trig, idx) => (
                <li key={idx}>🚨 {trig}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
