import { useState, useRef } from "react";

type JobInputMode = "url" | "paste";

export interface UploadPanelProps {
  disabled: boolean;
  onSubmit: (data: { resumeFile: File; jobUrl?: string; jobDescription?: string }) => void;
}

function UploadPanel({ disabled, onSubmit }: UploadPanelProps) {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobMode, setJobMode] = useState<JobInputMode>("url");
  const [jobUrl, setJobUrl] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please upload a PDF file");
      return;
    } 

    if (file.size > 10 * 1024 * 1024) {
      setError("File is too large (max 10MB)");
      return;
    }

    setError(null);
    setResumeFile(file);
  }

  function handleRemoveFile() {
    setResumeFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function handleSubmit() {
    if (disabled) return;

    if (!resumeFile) {
      setError("Please upload your resume first.");
      return;
    }

    if (jobMode === "url" && !jobUrl.trim()) {
      setError("Please enter a job posting URL.");
      return;
    }

    if (jobMode === "paste" && !jobDescription.trim()) {
      setError("Please paste the job description.");
      return;
    }

    setError(null);
    onSubmit({
      resumeFile,
      jobUrl: jobMode === "url" ? jobUrl: undefined,
      jobDescription: jobMode === "paste" ? jobDescription: undefined,
    });
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
      <h1 className="text-2xl font-semibold text-slate-900">Resume Optimizer</h1>
      <p className="mt-2 text-slate-500">
        Upload your resume and a job posting to get a match score and tailored recommendations.
      </p>

      <div className="mt-6">
        <label className="block text-sm font-medium text-slate-700 mb-2">Resume (PDF)</label>
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-lg py-8 cursor-pointer hover:border-slate-400 transition-colors">
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          {resumeFile ? (
            <span className="text-slate-700 font-medium">{resumeFile.name}</span>
          ) : (
            <span className="text-slate-400">Click to upload or drag a PDF here</span>
          )}
        </label>
        {resumeFile && (
          <button onClick={handleRemoveFile} className="mt-2 text-sm text-slate-400 hover:text-slate-600 cursor-pointer">
            Remove file
          </button>
        )}
      </div>

      <div className="mt-6">
        <div className="flex gap-2">
          <button
            onClick={() => setJobMode("url")}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer ${
              jobMode === "url" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-500"
            }`}
          >
            Job URL
          </button>
          <button
            onClick={() => setJobMode("paste")}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer ${
              jobMode === "paste" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-500"
            }`}
          >
            Paste Description
          </button>
        </div>

        {jobMode === "url" ? (
          <input
            type="url"
            placeholder="https://company.com/jobs/software-engineer"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            className="mt-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
          />
        ) : (
          <textarea
            placeholder="Paste the full job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={5}
            className="mt-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
          />
        )}
      </div>

      {error && <p className="mt-4 text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={disabled}
        className="mt-6 w-full bg-slate-900 text-white rounded-lg py-3 font-medium hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      >
        {disabled ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}

export default UploadPanel;