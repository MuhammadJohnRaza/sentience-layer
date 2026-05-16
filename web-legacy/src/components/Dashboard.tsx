"use client";

import React, { useState } from "react";
import AgentTrace from "./AgentTrace";
import WorkflowVisualizer from "./WorkflowVisualizer";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("trace");

  return (
    <div className="flex flex-col gap-6">
      <div className="flex gap-4 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab("trace")}
          className={`px-4 py-2 rounded-t-lg transition-colors ${
            activeTab === "trace" ? "bg-slate-800 text-indigo-400 font-medium" : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
          }`}
        >
          Agent Trace
        </button>
        <button
          onClick={() => setActiveTab("workflow")}
          className={`px-4 py-2 rounded-t-lg transition-colors ${
            activeTab === "workflow" ? "bg-slate-800 text-indigo-400 font-medium" : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
          }`}
        >
          Workflow Visualizer
        </button>
      </div>

      <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 min-h-[500px]">
        {activeTab === "trace" && <AgentTrace />}
        {activeTab === "workflow" && <WorkflowVisualizer />}
      </div>
    </div>
  );
}
