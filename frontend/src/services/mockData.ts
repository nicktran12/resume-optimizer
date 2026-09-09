import type { AnalysisResult } from "../types";

export const mockAnalysis: AnalysisResult = {
  analysis_id: "mock-analysis-1",
  status: "complete",
  overall_score: 87,
  score_breakdown: {
    required_skills: 92,
    technical_experience: 88,
    responsibilities: 84,
    education: 100,
    preferred_skills: 60,
  },
  matched_skills: ["Python", "FastAPI", "PostgreSQL", "React"],
  missing_skills: ["Kubernetes", "AWS Lambda"],
  recommendations: [
    {
      category: "Experience",
      recommendation: "Emphasize backend API development in the first bullet of your most recent role.",
    },
    {
      category: "Skills",
      recommendation: "Move PostgreSQL and AWS higher in your technical skills section.",
    },
    {
      category: "Projects",
      recommendation: "Highlight any distributed-systems work — it aligns closely with this job's infrastructure requirements.",
    },
  ],
  evidence: [
    {
      requirement: "Build scalable backend services",
      resume_evidence: "Built an API service using FastAPI and PostgreSQL, handling 10k+ requests/day.",
      match: "strong",
    },
    {
      requirement: "Experience with container orchestration (Kubernetes)",
      resume_evidence: "No direct mention of Kubernetes or container orchestration found in resume.",
      match: "none",
    },
  ],
};