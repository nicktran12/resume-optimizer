import { useState, useEffect, useRef } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import { mockAnalysis } from "./services/mockData";
import type { AnalysisResult } from "./types";

const STAGES = [
  "Uploading resume...",
  "Processing resume...",
  "Reading job description...",
  "Finding relevant experience...",
  "Generating recommendations...",
];
const STAGE_DURATION_MS = 700;

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [stageIndex, setStageIndex] = useState(0);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);

  const timeoutsRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  useEffect(() => {
    return () => {
      timeoutsRef.current.forEach(clearTimeout);
    };
  }, []);

  function handleSubmit(data: { resumeFile: File; jobUrl?: string; jobDescription?: string }) {
    timeoutsRef.current.forEach(clearTimeout);
    timeoutsRef.current = []

    setIsAnalyzing(true);
    setStageIndex(0);

    STAGES.forEach((_, i) => {
      const t = setTimeout(() => setStageIndex(i), i * STAGE_DURATION_MS);
      timeoutsRef.current.push(t)
    });

    const finalTimeout = setTimeout(() => {
      setAnalysis(mockAnalysis)
      setIsAnalyzing(false);
    }, STAGES.length * STAGE_DURATION_MS);
    timeoutsRef.current.push(finalTimeout);
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-5xl mx-auto flex gap-6 items-start">
        <div className="w-full max-w-sm shrink-0">
          <UploadPanel disabled={isAnalyzing} onSubmit={handleSubmit} />
        </div>

        <div className="flex-1 min-w-0">
          {isAnalyzing ? (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 flex flex-col items-center justify-center text-center h-64">
              <div className="h-8 w-8 border-4 border-slate-200 border-t-slate-900 rounded-full animate-spin" />
              <p className="mt-4 text-slate-900 font-medium">{STAGES[stageIndex]}</p>
            </div>
          ) : (
            <ResultsPanel analysis={analysis} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
