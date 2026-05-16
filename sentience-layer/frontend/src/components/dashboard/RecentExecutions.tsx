/**
 * Recent Executions — Black / Purple / Gold Theme
 */

"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

function timeAgo(iso: string) {
  try {
    const diff = Date.now() - new Date(iso).getTime();
    const m = Math.floor(diff / 60000);
    if (m < 1) return "just now";
    if (m < 60) return `${m}m ago`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
  } catch { return "—"; }
}

const STATUS_STYLE: Record<string, string> = {
  completed: "bg-emerald-950/50 text-emerald-400 border-emerald-800/40",
  running:   "bg-purple-950/50 text-[#A855F7] border-purple-800/40",
  pending:   "bg-yellow-950/50 text-[#EAB308] border-yellow-800/40",
  failed:    "bg-red-950/50 text-red-400 border-red-800/40",
};

export function RecentExecutions() {
  const [actions, setActions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.getActions()
      .then((data) => { setActions(data.slice(0, 6)); setIsLoading(false); })
      .catch(() => setIsLoading(false));
  }, []);

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
        <h3 className="text-sm font-bold text-[#EAB308] uppercase tracking-wider">Recent Executions</h3>
        <span className="text-[10px] text-zinc-600">{actions.length} items</span>
      </div>

      {/* Table */}
      <div className="divide-y divide-zinc-800/60">
        {isLoading ? (
          [1, 2, 3].map((i) => (
            <div key={i} className="px-5 py-3 flex items-center gap-4">
              <div className="h-4 w-48 bg-zinc-800/60 rounded animate-pulse" />
              <div className="h-4 w-20 bg-zinc-800/40 rounded animate-pulse ml-auto" />
            </div>
          ))
        ) : actions.length === 0 ? (
          <p className="text-xs text-zinc-600 text-center py-10">No recent executions</p>
        ) : (
          actions.map((action) => (
            <div
              key={action.id}
              className="flex items-center justify-between px-5 py-3.5 hover:bg-zinc-800/20 transition-colors group"
            >
              <div className="flex-1 min-w-0 pr-4">
                <p className="text-sm font-medium text-slate-200 truncate group-hover:text-[#EAB308] transition-colors">
                  {action.title}
                </p>
                <p className="text-[11px] text-zinc-600 truncate mt-0.5">{action.description}</p>
              </div>

              <div className="flex items-center gap-3 flex-shrink-0">
                {/* Confidence bar */}
                {action.confidence && (
                  <div className="hidden sm:flex items-center gap-1.5">
                    <div className="w-16 h-1 rounded-full bg-zinc-800 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-[#A855F7] to-[#EAB308]"
                        style={{ width: `${Math.round(action.confidence * 100)}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-zinc-600">{Math.round(action.confidence * 100)}%</span>
                  </div>
                )}

                {/* Status badge */}
                <span className={cn(
                  "text-[10px] font-medium px-2 py-0.5 rounded-full border capitalize",
                  STATUS_STYLE[action.status] ?? "bg-zinc-800/50 text-zinc-500 border-zinc-700/40"
                )}>
                  {action.status}
                </span>

                {/* Time */}
                <span className="text-[10px] text-zinc-700 w-12 text-right">
                  {timeAgo(action.createdAt)}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}