/**
 * Agent Trace Page
 */

import { AgentTraceViewer } from "@/components/trace/AgentTraceViewer";

export default function TracePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Agent Traces</h1>
        <p className="text-slate-500">Inspect agent reasoning chains and decisions</p>
      </div>
      <AgentTraceViewer />
    </div>
  );
}