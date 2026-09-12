import type { AnalysisResult } from "../types";

interface ResultsPanelProps {
  analysis: AnalysisResult | null;
}

function formatCategoryLabel(category: string): string {
  return category.split("_").map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-slate-600">{label}</span>
        <span className="font-medium text-slate-900">{value}%</span>
      </div>
      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div className="h-full bg-slate-900 rounded-full" style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function ResultsPanel({ analysis }: ResultsPanelProps) {
  if (!analysis) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 flex flex-col items-center justify-center text-center h-64">
        <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center text-2xl">
          📄
        </div>
        <p className="mt-4 text-slate-900 font-medium">No analysis yet</p>
        <p className="mt-1 text-sm text-slate-400">
          Upload a resume and job posting on the left to see your match score here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center">
        <p className="text-sm text-slate-500">Overall Match</p>
        <p className="text-5xl font-semibold text-slate-900 mt-2">{analysis.overall_score}%</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 space-y-4">
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Score Breakdown</h2>
        <ScoreBar label="Education" value={analysis.score_breakdown.education} />
        <ScoreBar label="Required Skills" value={analysis.score_breakdown.required_skills} />
        <ScoreBar label="Preferred Skills" value={analysis.score_breakdown.preferred_skills} />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Skills</h2>
        <div className="space-y-3">
          <div>
            <p className="text-sm font-medium text-slate-500 mb-2">Strong Matches</p>
            <div className="flex flex-wrap gap-2">
              {analysis.matched_skills.map((skill) => (
                <span key={skill} className="text-sm bg-emerald-50 text-emerald-700 rounded-full px-3 py-1">
                  ✓ {skill}
                </span>
              ))}
            </div>
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 mb-2">Potential Gaps</p>
            <div className="flex flex-wrap gap-2">
              {analysis.missing_skills.map((skill) => (
                <span key={skill} className="text-sm bg-amber-50 text-amber-700 rounded-full px-3 py-1">
                  ! {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Recommendations</h2>
        <div className="space-y-4">
          {analysis.recommendations.map((rec, i) => (
            <div key={i}>
              <p className="text-sm font-medium text-slate-900">{formatCategoryLabel(rec.category)}</p>
              <p className="text-sm text-slate-600 mt-1">{rec.recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Evidence</h2>
        <div className="space-y-4">
          {analysis.evidence.map((ev, i) => (
            <div key={i}>
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium text-slate-900">{ev.requirement}</p>
                <span
                  className={`text-xs font-medium rounded-full px-2 py-0.5 shrink-0 ${
                    ev.match === "strong"
                      ? "bg-emerald-50 text-emerald-700"
                      : ev.match === "partial"
                      ? "bg-amber-50 text-amber-700"
                      : "bg-red-50 text-red-700"
                  }`}
                >
                  {ev.match}
                </span>
              </div>
              <p className="text-sm text-slate-600 mt-1">{ev.resume_evidence}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ResultsPanel;