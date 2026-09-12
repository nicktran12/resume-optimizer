import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import { api } from "./services/api";
import type { AnalysisResult } from "./types";

const STAGES = [
  "Uploading resume...",
  "Reading job description...",
  "Finding relevant experience...",
  "Generating recommendations...",
];

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [stageIndex, setStageIndex] = useState(0);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(data: { resumeFile: File; jobUrl?: string; jobDescription?: string }) {
    setIsAnalyzing(true);
    setError(null);
    setStageIndex(0);

    try {
      setStageIndex(0);
      const resume = await api.uploadResume(data.resumeFile);

      setStageIndex(1);
      const job = await api.submitJob({ url: data.jobUrl, description: data.jobDescription });

      setStageIndex(2);
      setStageIndex(3);
      const result = await api.runAnalysis(resume.resume_id, job.job_id);

      setAnalysis(result)
    } catch (err) {
      setError("Analysis failed. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
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
          ) : error ? (
            <div className="bg-white rounded-xl shadow-sm border border-red-200 p-8 flex flex-col items-center justify-center text-center h-64">
              <div className="h-12 w-12 rounded-full bg-red-50 flex items-center justify-center text-2xl">⚠️</div>
              <p className="mt-4 text-slate-900 font-medium">Analysis failed</p>
              <p className="mt-1 text-sm text-slate-500">{error}</p>
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
