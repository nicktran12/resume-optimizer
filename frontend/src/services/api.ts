import type { AnalysisResult } from "../types";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface HealthResponse {
  status: string;
  environment: string;
}

export interface ResumeUploadResponse {
  resume_id: string;
  filename: string;
  status: string;
  chunk_count: number;
}

export interface JobSubmitResponse {
  job_id: string;
  status: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, init);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const message = body?.detail || `Request to ${path} failed (${res.status})`;
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>("/health"),

  uploadResume: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<ResumeUploadResponse>("/api/resumes", { method: "POST", body: formData });
  },

  submitJob: (payload: { url?: string; description?: string }) =>
    request<JobSubmitResponse>("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),

  runAnalysis: (resumeId: string, jobId: string) =>
    request<AnalysisResult & { analysis_id: string; status: string }>("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_id: resumeId, job_id: jobId }),
    }),
};