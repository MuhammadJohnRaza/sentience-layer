import os

frontend_pages = {
    "frontend/src/app/doubt-room/page.tsx": """\"use client\";
import React, { useState } from "react";
import { AlertTriangle, ShieldAlert, Cpu, EyeOff, Lock } from "lucide-react";
import { cn } from "@/lib/utils";

export default function DoubtRoomPage() {
  const [activeDoubt, setActiveDoubt] = useState(0);

  const doubts = [
    { title: "Ethical alignment drift detected", severity: "High", certainty: "60%" },
    { title: "Causal inversion in user data", severity: "Medium", certainty: "85%" },
    { title: "Resource exhaustion predicted", severity: "Low", certainty: "40%" }
  ];

  return (
    <div className="min-h-screen bg-black text-amber-50 font-mono p-8 selection:bg-amber-500/30">
      <div className="max-w-6xl mx-auto">
        <header className="flex items-center gap-4 mb-12 border-b border-amber-900/30 pb-6">
          <ShieldAlert className="w-10 h-10 text-amber-500 animate-pulse" />
          <div>
            <h1 className="text-3xl font-bold tracking-widest text-amber-500 uppercase">The Doubt Room</h1>
            <p className="text-amber-700/80 mt-1 text-sm">Systemic Vulnerability & Uncertainty Analysis</p>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-4">
            <h2 className="text-amber-600 font-bold tracking-widest mb-6">ACTIVE DOUBTS</h2>
            {doubts.map((d, i) => (
              <div 
                key={i} 
                onClick={() => setActiveDoubt(i)}
                className={cn(
                  "p-4 border cursor-pointer transition-all",
                  activeDoubt === i ? "bg-amber-500/10 border-amber-500" : "bg-zinc-950 border-zinc-900 hover:border-amber-900"
                )}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-sm text-amber-200">{d.title}</h3>
                </div>
                <div className="flex gap-4 text-xs text-amber-700">
                  <span>SEVERITY: {d.severity}</span>
                  <span>CERTAINTY: {d.certainty}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="md:col-span-2 border border-amber-900/50 bg-zinc-950 p-6 relative overflow-hidden flex flex-col justify-center items-center min-h-[400px]">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(245,158,11,0.05)_0%,transparent_70%)]" />
            <EyeOff className="w-24 h-24 text-amber-900 mb-6" />
            <h2 className="text-xl font-bold text-amber-600 mb-2">Analyzing: {doubts[activeDoubt].title}</h2>
            <p className="text-amber-800 text-center max-w-md">The Doubt Generator agent is currently running counter-factuals to stress test this hypothesis. Adversarial parameters are engaged.</p>
            
            <div className="mt-8 flex gap-4 w-full max-w-sm">
              <button className="flex-1 py-2 border border-amber-500 text-amber-500 font-bold hover:bg-amber-500 hover:text-black transition-colors">
                CHALLENGE
              </button>
              <button className="flex-1 py-2 border border-zinc-700 text-zinc-500 font-bold hover:bg-zinc-800 transition-colors">
                DISMISS
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/app/simulate/page.tsx": """\"use client\";
import React, { useState } from "react";
import { Play, FastForward, Settings, BarChart2 } from "lucide-react";

export default function SimulatePage() {
  const [running, setRunning] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">Simulation Engine</h1>
            <p className="text-slate-500 mt-1">Run complex scenario forecasts based on world-model temporal states</p>
          </div>
          <div className="flex gap-3">
            <button className="p-3 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200"><Settings className="w-5 h-5" /></button>
            <button 
              onClick={() => setRunning(!running)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-white transition-all ${running ? 'bg-red-500 hover:bg-red-600 shadow-red-200' : 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-200'} shadow-lg`}
            >
              {running ? "Stop Simulation" : <><Play className="w-4 h-4 fill-current" /> Run Simulation</>}
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 space-y-6">
            <h3 className="font-semibold text-slate-700 uppercase tracking-wide text-sm">Parameters</h3>
            <div className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-500 uppercase">Time Horizon</label>
                <input type="range" className="w-full mt-2 accent-indigo-600" />
                <div className="flex justify-between text-xs text-slate-400 font-mono mt-1"><span>1w</span><span>5y</span></div>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-500 uppercase">Agent Entropy</label>
                <input type="range" className="w-full mt-2 accent-indigo-600" />
              </div>
            </div>
          </div>

          <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 min-h-[400px] flex flex-col items-center justify-center">
            {running ? (
              <div className="flex flex-col items-center">
                <FastForward className="w-16 h-16 text-indigo-500 animate-pulse mb-4" />
                <h3 className="text-xl font-bold text-slate-700">Simulating Future States...</h3>
                <p className="text-slate-500 mt-2">Computing temporal branches via Causal Graph</p>
              </div>
            ) : (
              <div className="flex flex-col items-center opacity-50">
                <BarChart2 className="w-16 h-16 text-slate-400 mb-4" />
                <h3 className="text-xl font-bold text-slate-600">No Active Simulation</h3>
                <p className="text-slate-500 mt-2">Configure parameters and press run</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
"""
}

backend_main = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentience Layer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Sentience Layer Kernel Active"}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "components": {
            "kernel": "online",
            "world_model": "online",
            "agents": 18
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

for filepath, content in frontend_pages.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

backend_path = "backend/python/main.py"
os.makedirs(os.path.dirname(backend_path), exist_ok=True)
with open(backend_path, "w", encoding="utf-8") as f:
    f.write(backend_main)

print("Final files implemented successfully.")
