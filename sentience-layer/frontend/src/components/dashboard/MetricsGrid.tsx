/**
 * Metrics Grid — Black / Purple / Gold Theme
 */

"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

const ICONS = {
  agents: (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
  ),
  insights: (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
  ),
  actions: (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
  ),
  health: (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
  ),
};

export function MetricsGrid() {
  const [metrics, setMetrics] = useState<any[]>([]);

  useEffect(() => {
    api.getAgentStatus().then((data: any[]) => {
      setMetrics([
        { label: "Active Agents", value: data.filter((a) => a.status === "running").length, change: 12, trend: "up", icon: "agents" },
        { label: "Insights Today", value: 24, change: 8, trend: "up", icon: "insights" },
        { label: "Actions Executed", value: 156, change: -3, trend: "down", icon: "actions" },
        { label: "System Health", value: "98.5%", change: 0.2, trend: "up", icon: "health" },
      ]);
    }).catch(() => {
      setMetrics([
        { label: "Active Agents", value: "—", change: 0, trend: "neutral", icon: "agents" },
        { label: "Insights Today", value: "—", change: 0, trend: "neutral", icon: "insights" },
        { label: "Actions Executed", value: "—", change: 0, trend: "neutral", icon: "actions" },
        { label: "System Health", value: "—", change: 0, trend: "neutral", icon: "health" },
      ]);
    });
  }, []);

  if (metrics.length === 0) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 rounded-xl border border-zinc-800 bg-zinc-900/40 animate-pulse" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <div
          key={metric.label}
          className="relative overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 hover:border-[#EAB308]/30 transition-colors group"
        >
          {/* Subtle glow top-right */}
          <div className="absolute -top-6 -right-6 h-20 w-20 rounded-full bg-[#A855F7]/5 group-hover:bg-[#EAB308]/10 transition-colors" />

          <div className="flex items-start justify-between">
            <div className="text-[#A855F7]/60">{ICONS[metric.icon as keyof typeof ICONS]}</div>
            <span className={cn(
              "flex items-center gap-0.5 rounded-full px-2 py-0.5 text-[10px] font-semibold",
              metric.trend === "up"
                ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/40"
                : metric.trend === "down"
                ? "bg-red-950/60 text-red-400 border border-red-800/40"
                : "bg-zinc-800/60 text-zinc-400 border border-zinc-700/40"
            )}>
              {metric.trend === "up" ? "▲" : metric.trend === "down" ? "▼" : "·"}
              {" "}{Math.abs(metric.change)}{typeof metric.change === "number" ? "%" : ""}
            </span>
          </div>

          <div className="mt-4">
            <p className="text-2xl font-bold text-[#EAB308]">{metric.value}</p>
            <p className="text-xs text-zinc-500 mt-1 uppercase tracking-wider">{metric.label}</p>
          </div>
        </div>
      ))}
    </div>
  );
}