import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { HomeView } from './components/HomeView';
import { QuestionsView } from './components/QuestionsView';
import { ReportView } from './components/ReportView';
import { HistoryView } from './components/HistoryView';
import { ParsedDecision, Question, DecisionReport, HistoryItem } from './types';

export default function App() {
  const [step, setStep] = useState<string>('HOME'); // HOME | QUESTIONS | REPORT | HISTORY
  const [geminiConfigured, setGeminiConfigured] = useState<boolean>(false);

  const [decisionInput, setDecisionInput] = useState<string>('');
  const [parsedDecision, setParsedDecision] = useState<ParsedDecision | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [finalReport, setFinalReport] = useState<DecisionReport | null>(null);

  // Load history from localStorage
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const saved = localStorage.getItem('intellidecision_history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Check health on mount
  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => {
        setGeminiConfigured(Boolean(data.geminiConfigured));
      })
      .catch(() => {
        setGeminiConfigured(false);
      });
  }, []);

  // Sync history to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('intellidecision_history', JSON.stringify(history));
    } catch (e) {
      console.error("Failed to save history to localStorage", e);
    }
  }, [history]);

  // Parse decision text
  const handleParseDecision = async (text: string): Promise<ParsedDecision | null> => {
    const res = await fetch('/api/parse-decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ decisionInput: text }),
    });

    if (!res.ok) {
      throw new Error("Failed to parse decision");
    }

    const data = await res.json();
    setParsedDecision(data.parsed);
    return data.parsed;
  };

  // Generate clarifying questions
  const handleProceedToQuestions = async () => {
    setStep('QUESTIONS');
    try {
      const res = await fetch('/api/generate-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parsedDecision, decisionInput }),
      });

      if (res.ok) {
        const data = await res.json();
        setQuestions(data.questions || []);
      }
    } catch (err) {
      console.error("Failed to load clarifying questions:", err);
    }
  };

  // Analyze decision & synthesize final report
  const handleAnalyze = async () => {
    const res = await fetch('/api/analyze-decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        decisionInput,
        parsedDecision,
        answers: userAnswers,
      }),
    });

    if (!res.ok) {
      throw new Error("Failed to synthesize report");
    }

    const data = await res.json();
    const report: DecisionReport = data.report;
    setFinalReport(report);

    // Save to history
    const newItem: HistoryItem = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }),
      decisionInput,
      report,
    };

    setHistory((prev) => [newItem, ...prev]);
    setStep('REPORT');
  };

  const handleNewDecision = () => {
    setDecisionInput('');
    setParsedDecision(null);
    setQuestions([]);
    setUserAnswers({});
    setFinalReport(null);
    setStep('HOME');
  };

  const handleSelectHistoryItem = (item: HistoryItem) => {
    setDecisionInput(item.decisionInput);
    setFinalReport(item.report);
    setStep('REPORT');
  };

  const handleDeleteHistoryItem = (id: string) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="flex min-h-screen bg-[#070a12] text-slate-100 font-sans antialiased selection:bg-indigo-500 selection:text-white">
      {/* Sidebar */}
      <Sidebar
        currentStep={step}
        setStep={setStep}
        geminiConfigured={geminiConfigured}
        historyCount={history.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 p-4 sm:p-8 lg:p-10 overflow-y-auto max-h-screen">
        {step === 'HOME' && (
          <HomeView
            decisionInput={decisionInput}
            setDecisionInput={setDecisionInput}
            onParseDecision={handleParseDecision}
            parsedDecision={parsedDecision}
            onProceedToQuestions={handleProceedToQuestions}
          />
        )}

        {step === 'QUESTIONS' && (
          <QuestionsView
            questions={questions}
            parsedDecision={parsedDecision}
            userAnswers={userAnswers}
            setUserAnswers={setUserAnswers}
            onAnalyze={handleAnalyze}
            onBack={() => setStep('HOME')}
          />
        )}

        {step === 'REPORT' && (
          <ReportView
            report={finalReport}
            parsedDecision={parsedDecision}
            onNewDecision={handleNewDecision}
            onGoHistory={() => setStep('HISTORY')}
            historyCount={history.length}
          />
        )}

        {step === 'HISTORY' && (
          <HistoryView
            history={history}
            onSelectReport={handleSelectHistoryItem}
            onDeleteReport={handleDeleteHistoryItem}
            onClearHistory={handleClearHistory}
            onNewDecision={handleNewDecision}
          />
        )}
      </main>
    </div>
  );
}
