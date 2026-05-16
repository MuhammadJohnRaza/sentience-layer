"use client";

import React from "react";

export default function AgentTrace() {
  const traces = [
    { id: 1, action: "Initialize memory core", status: "success", time: "10:00:01" },
    { id: 2, action: "Connect to database", status: "success", time: "10:00:05" },
    { id: 3, action: "Fetch user context", status: "pending", time: "10:00:12" },
    { id: 4, action: "Analyze causal links", status: "failed", time: "10:00:15" },
  ];

  return (
    <div className="space-y-4 font-mono text-sm">
      <h2 className="text-xl font-semibold mb-4 text-white">Agent Trace Execution</h2>
      {traces.map((trace) => (
        <div key={trace.id} className="flex items-center gap-4 p-3 bg-slate-900 rounded-md border border-slate-800">
          <span className="text-slate-500 w-20">{trace.time}</span>
          <span className="flex-1 text-slate-300">{trace.action}</span>
          <span className={`px-2 py-1 rounded text-xs uppercase tracking-wider font-bold ${
            trace.status === 'success' ? 'bg-emerald-900/50 text-emerald-400' :
            trace.status === 'pending' ? 'bg-amber-900/50 text-amber-400' :
            'bg-red-900/50 text-red-400'
          }`}>
            {trace.status}
          </span>
        </div>
      ))}
    </div>
  );
}
