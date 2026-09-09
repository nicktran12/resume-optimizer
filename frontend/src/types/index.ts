export interface Resume {
  resume_id: string;
  filename: string;
  status: "uploaded" | "processing" | "ready" | "failed";
}

export interface Job {
  job_id: string;
  url?: string;
  raw_description?: string;
  status: "pending" | "processing" | "ready" | "failed";
}

export interface Evidence {
  requirement: string;
  resume_evidence: string;
  match: "strong" | "partial" | "none";
}

export interface Recommendation {
  category: string;
  recommendation: string;
}

export interface ScoreBreakdown {
  education: number;
  required_skills: number;
  preferred_skills: number;
}

export interface AnalysisResult {
  analysis_id: string;
  status: "pending" | "processing" | "complete" | "failed";
  overall_score: number;
  score_breakdown: ScoreBreakdown;
  matched_skills: string[];
  missing_skills: string[];
  recommendations: Recommendation[];
  evidence: Evidence[];
}
