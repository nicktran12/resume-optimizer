import { useState, useEffect } from "react";
import { api } from "./services/api";

type ConnectionState = "checking" | "connected" | "error";

function App() {
  const [status, setStatus] = useState<ConnectionState>("checking");
  const [detail, setDetail] = useState<string>("");

  useEffect(() => {
    api
      .health()
      .then((res) => {
        setStatus("connected");
        setDetail(res.environment);
      })
      .catch((err) => {
        setStatus("error");
        setDetail(err.message);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="max-w-lg w-full bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h1 className="text-2xl font-semibold text-slate-900">Resume Optimizer</h1>
        <p className="mt-2 text-slate-500">
          Milestone 1: basic React + FastAPI connectivity check.
        </p>
        <div className="mt-6">
          {status === "checking" && (
            <span className="text-slate-500">Checking backend...</span>
          )}
          {status === "connected" && (
            <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 text-emerald-700 px-3 py-1 text-sm font-medium">
              Connected ({detail})
            </span>
          )}
          {status === "error" && (
            <span className="inline-flex items-center gap-2 rounded-full bg-red-50 text-red-700 px-3 py-1 text-sm font-medium">
              Error {detail}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default App;
