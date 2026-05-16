"use client";

import React from "react";

export default function WorkflowVisualizer() {
  const nodes = ["Input", "Context Extraction", "Planning", "Execution", "Feedback"];

  return (
    <div>
      <h2 className="text-xl font-semibold mb-6 text-white">System Workflow</h2>
      <div className="flex items-center justify-between mt-12 px-8">
        {nodes.map((node, i) => (
          <React.Fragment key={node}>
            <div className="flex flex-col items-center gap-2 relative">
              <div className={`w-16 h-16 rounded-full border-4 flex items-center justify-center bg-slate-900 z-10 ${
                i < 3 ? "border-indigo-500 text-indigo-400" : "border-slate-700 text-slate-500"
              }`}>
                {i + 1}
              </div>
              <span className="text-xs font-medium text-slate-400 absolute -bottom-8 whitespace-nowrap">{node}</span>
            </div>
            {i < nodes.length - 1 && (
              <div className={`flex-1 h-1 -mx-2 ${
                i < 2 ? "bg-indigo-500" : "bg-slate-700"
              }`} />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
