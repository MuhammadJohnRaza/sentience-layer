/**
 * Agent Status Panel — Black / Purple / Gold Theme
 */

"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

export function AgentStatusPanel() {
  const [agents, setAgents] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.getAgentStatus()
      .then((data) => { setAgents(data); setIsLoading(false); })
      .catch(() => setIsLoading(false));
  }, []);

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
        <h3 className="text-sm font-bold text-[#EAB308] uppercase tracking-wider">Agent Network</h3>
        <span className="flex items-center gap-1.5 text-[10px] text-emerald-400">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Live
        </span>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
        {isLoading ? (
          [1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-10 rounded-lg bg-zinc-800/50 animate-pulse" />
          ))
        ) : agents.length === 0 ? (
          <p className="text-xs text-zinc-600 text-center py-6">No agent data available</p>
        ) : (
          agents.map((agent) => {
            const isRunning = agent.status === "running";
            return (
              <div key={agent.id} className="flex items-center gap-3 rounded-lg px-3 py-2.5 border border-zinc-800/60 bg-black/30 hover:border-zinc-700 transition-colors">
                {/* Status dot */}
                <div className={cn(
                  "flex-shrink-0 h-2 w-2 rounded-full",
                  isRunning ? "bg-emerald-400 animate-pulse" : "bg-zinc-600"
                )} />

                {/* Name */}
                <span className="flex-1 text-sm text-slate-300 truncate">{agent.name}</span>

                {/* Status badge */}
                <span className={cn(
                  "text-[10px] font-medium px-2 py-0.5 rounded-full border",
                  isRunning
                    ? "bg-emerald-950/50 text-emerald-400 border-emerald-800/40"
                    : "bg-zinc-800/50 text-zinc-500 border-zinc-700/40"
                )}>
                  {agent.status}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}