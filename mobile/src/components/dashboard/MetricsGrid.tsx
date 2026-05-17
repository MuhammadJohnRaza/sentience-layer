/** Metrics Grid — Plan Steps Trace Panel + Before vs After Incident Ledger */
"use client";
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { DashboardMetric } from "@/types";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

// ─── Plan Step trace data ────────────────────────────────────────────────────
const PLAN_STEPS = [
  {
    id: 1,
    label: "Ingest Anomaly",
    agent: "CriticAgent",
    detail: "Unindexed checkout transaction columns detected. Latency surged to 425ms.",
    severity: "CRITICAL",
  },
  {
    id: 2,
    label: "Causal Audit",
    agent: "CausalInferenceAgent",
    detail: "Causal coefficient 0.94 links read-saturation to $24,580 daily revenue loss.",
    severity: "HIGH",
  },
  {
    id: 3,
    label: "Doubt Sandbox",
    agent: "DoubtAgent",
    detail: "Anomalous thread pool quarantined inside Doubt Room isolation boundary.",
    severity: "CONTAINED",
  },
  {
    id: 4,
    label: "Dispatch Playbook",
    agent: "ConsensusAgent",
    detail: "Unanimous swarm vote. Postgres caching + CRM incentive campaign dispatched.",
    severity: "RESOLVED",
  },
];

// ─── Decision flow branch alternatives ──────────────────────────────────────
const DECISION_BRANCHES = [
  {
    chosen: true,
    label: "Postgres Caching Index Optimization",
    reason: "Directly resolves root cause — unindexed read scans — with 94% causal confidence. ROI: 245%.",
    tag: "✅ CHOSEN",
    color: "border-emerald-500/40 bg-emerald-950/20 text-emerald-300",
    badge: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  },
  {
    chosen: false,
    label: "Raw Connection Pool Expansion",
    reason: "REJECTED — Does not clear saturated read locks. Thread exhaustion persists under load.",
    tag: "❌ REJECTED",
    color: "border-rose-500/30 bg-rose-950/10 text-rose-400/70",
    badge: "bg-rose-500/10 text-rose-400 border-rose-500/20",
  },
  {
    chosen: false,
    label: "Global Price Discounts",
    reason: "REJECTED — Does not address technical bottleneck. Margin loss risk without resolving checkout failures.",
    tag: "❌ REJECTED",
    color: "border-rose-500/30 bg-rose-950/10 text-rose-400/70",
    badge: "bg-rose-500/10 text-rose-400 border-rose-500/20",
  },
];

// ─── Before / After incident state ──────────────────────────────────────────
const BEFORE_STATE = {
  latency_ms: 425.2,
  pool_utilization: 98.2,
  abandonment_pct: 42.0,
  loss_usd: 24580,
  status: "🔴 ANOMALY DETECTED",
};

const AFTER_STATE = {
  latency_ms: 22.4,
  pool_utilization: 11.2,
  abandonment_pct: 2.8,
  loss_usd: 0,
  status: "🟡 SELF-HEALED",
};

// ─── Component ───────────────────────────────────────────────────────────────
export function MetricsGrid() {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [activeStep, setActiveStep] = useState(0);
  const [healed, setHealed] = useState(false);

  // Cycle through plan steps automatically for demo animation
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => {
        const next = (prev + 1) % PLAN_STEPS.length;
        if (next === PLAN_STEPS.length - 1) setHealed(true);
        return next;
      });
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    api.getAgentStatus().then((data) => {
      setMetrics([
        {
          label: "Active Agents",
          value: data.filter((a: any) => a.status === "running").length || 18,
          change: 12,
          trend: "up",
          icon: "agents",
        },
        {
          label: "Insights Today",
          value: 24,
          change: 8,
          trend: "up",
          icon: "insights",
        },
        {
          label: "Actions Executed",
          value: 156,
          change: -3,
          trend: "down",
          icon: "actions",
        },
        {
          label: "System Health",
          value: "98.5%",
          change: 0.2,
          trend: "up",
          icon: "health",
        },
      ]);
    });
  }, []);

  return (
    <div className="space-y-6">

      {/* ── Standard KPI Cards ─────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric) => (
          <Card
            key={metric.label}
            className="relative overflow-hidden border-2 border-border/40 bg-card shadow-[0_4px_25px_rgba(0,0,0,0.5)] hover:border-border transition-all duration-300"
          >
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-black text-muted-foreground tracking-widest uppercase">
                    {metric.label}
                  </p>
                  <p className="text-3xl font-black text-primary-foreground mt-2 tracking-tight">
                    {metric.value}
                  </p>
                </div>
                <div
                  className={cn(
                    "flex items-center rounded-full px-2.5 py-1 text-xs font-bold tracking-wide border",
                    metric.trend === "up"
                      ? "bg-emerald-950/50 text-emerald-400 border-emerald-500/20 shadow-[0_0_8px_rgba(16,185,129,0.15)]"
                      : metric.trend === "down"
                        ? "bg-rose-950/50 text-rose-400 border-rose-500/20 shadow-[0_0_8px_rgba(244,63,94,0.15)]"
                        : "bg-border/10 text-muted-foreground border-border/20",
                  )}
                >
                  {metric.trend === "up" ? "▲ " : metric.trend === "down" ? "▼ " : ""}
                  {Math.abs(metric.change)}%
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* ── Plan Steps Trace Panel ─────────────────────────────────────────── */}
      <Card className="border-2 border-violet-500/25 bg-card/30 shadow-[0_4px_30px_rgba(124,58,237,0.12)] backdrop-blur-md">
        <CardContent className="p-5 space-y-4">
          <div className="flex items-center gap-3 border-b border-border/15 pb-3">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-violet-500/15 border border-violet-500/30 text-sm">🧠</span>
            <div>
              <p className="text-[10px] font-black tracking-widest text-violet-400 uppercase">Google Antigravity · Agentic Reasoning Chain</p>
              <p className="text-[9px] text-muted-foreground/60 tracking-wider">Plan Step 1: Ingest Anomaly → Step 2: Causal Audit → Step 3: Doubt Sandbox → Step 4: Dispatch Playbook</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {PLAN_STEPS.map((step, idx) => {
              const isActive = idx === activeStep;
              const isDone = idx < activeStep || (healed && idx === PLAN_STEPS.length - 1);
              return (
                <div
                  key={step.id}
                  className={cn(
                    "rounded-xl border p-3.5 transition-all duration-500 relative overflow-hidden",
                    isDone
                      ? "border-emerald-500/35 bg-emerald-950/15"
                      : isActive
                        ? "border-violet-500/50 bg-violet-950/20 shadow-[0_0_16px_rgba(124,58,237,0.2)] animate-pulse"
                        : "border-border/15 bg-background/10 opacity-40",
                  )}
                >
                  {/* Step number */}
                  <div className="flex items-center gap-2 mb-2">
                    <span
                      className={cn(
                        "flex h-5 w-5 items-center justify-center rounded-full text-[9px] font-black border",
                        isDone
                          ? "bg-emerald-500/20 border-emerald-500/40 text-emerald-400"
                          : isActive
                            ? "bg-violet-500/30 border-violet-500/60 text-violet-300"
                            : "bg-border/10 border-border/20 text-muted-foreground/40",
                      )}
                    >
                      {isDone ? "✓" : step.id}
                    </span>
                    <span className={cn("text-[9px] font-black tracking-widest uppercase",
                      isDone ? "text-emerald-400" : isActive ? "text-violet-300" : "text-muted-foreground/40"
                    )}>
                      Step {step.id}
                    </span>
                  </div>

                  <p className={cn("text-[11px] font-black tracking-wide mb-1",
                    isDone ? "text-emerald-300" : isActive ? "text-primary-foreground" : "text-muted-foreground/40"
                  )}>
                    {step.label}
                  </p>
                  <p className={cn("text-[9px] font-semibold leading-relaxed",
                    isDone ? "text-emerald-400/70" : isActive ? "text-muted-foreground/80" : "text-muted-foreground/25"
                  )}>
                    {step.detail}
                  </p>

                  <div className="mt-2 flex items-center justify-between">
                    <span className={cn("text-[8px] font-black tracking-widest border rounded px-1.5 py-0.5",
                      isDone
                        ? "bg-emerald-950/40 border-emerald-500/25 text-emerald-400"
                        : isActive
                          ? "bg-violet-950/40 border-violet-500/30 text-violet-300"
                          : "bg-transparent border-border/10 text-muted-foreground/25"
                    )}>
                      {step.agent}
                    </span>
                    <span className={cn("text-[8px] font-black",
                      step.severity === "CRITICAL" ? "text-rose-400"
                        : step.severity === "HIGH" ? "text-amber-400"
                          : step.severity === "CONTAINED" ? "text-sky-400"
                            : "text-emerald-400"
                    )}>
                      {step.severity}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* ── Decision Flow Branch Log ───────────────────────────────────────── */}
      <Card className="border-2 border-amber-500/20 bg-card/30 shadow-[0_4px_25px_rgba(0,0,0,0.5)] backdrop-blur-md">
        <CardContent className="p-5 space-y-3">
          <div className="flex items-center gap-3 border-b border-border/15 pb-3">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-500/15 border border-amber-500/30 text-sm">⚖️</span>
            <div>
              <p className="text-[10px] font-black tracking-widest text-amber-400 uppercase">Decision Flow · Intervention Branch Evaluation</p>
              <p className="text-[9px] text-muted-foreground/60 tracking-wider">Explicit branch reasoning explaining why Postgres Caching was chosen over alternatives</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {DECISION_BRANCHES.map((branch, idx) => (
              <div key={idx} className={cn("rounded-xl border p-3.5 transition-all duration-300", branch.color)}>
                <div className="flex items-center justify-between mb-2">
                  <span className={cn("text-[8px] font-black tracking-widest border rounded px-1.5 py-0.5", branch.badge)}>
                    {branch.tag}
                  </span>
                </div>
                <p className="text-[11px] font-black tracking-wide mb-1.5">{branch.label}</p>
                <p className="text-[9px] font-semibold leading-relaxed opacity-80">{branch.reason}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* ── Before vs After Split-Screen Incident Ledger ─────────────────── */}
      <Card className="border-2 border-border/40 bg-card/30 shadow-[0_4px_30px_rgba(0,0,0,0.6)] backdrop-blur-md overflow-hidden">
        <CardContent className="p-0">
          {/* Header */}
          <div className="flex items-center gap-3 px-5 py-3.5 border-b border-border/20 bg-card/50">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/15 border border-primary/30 text-sm">📊</span>
            <div>
              <p className="text-[10px] font-black tracking-widest text-primary-foreground uppercase">System State Transition · Outcome Visualization</p>
              <p className="text-[9px] text-muted-foreground/60 tracking-wider">Before (Incident Peak) vs After (Post-Playbook Simulation)</p>
            </div>
            <div className="ml-auto flex items-center gap-2">
              <span className={cn(
                "text-[8px] font-black tracking-widest px-2 py-1 rounded-full border animate-pulse",
                healed
                  ? "bg-amber-500/20 border-amber-500/40 text-amber-400 shadow-[0_0_12px_rgba(245,158,11,0.3)]"
                  : "bg-rose-500/20 border-rose-500/40 text-rose-400 shadow-[0_0_12px_rgba(244,63,94,0.3)]"
              )}>
                {healed ? "🟡 SELF-HEALED" : "🔴 ANOMALY ACTIVE"}
              </span>
            </div>
          </div>

          {/* Split columns */}
          <div className="grid grid-cols-1 sm:grid-cols-2 divide-y sm:divide-y-0 sm:divide-x divide-border/20">

            {/* BEFORE column */}
            <div className="p-5 space-y-3 bg-rose-950/10 border-r-0 sm:border-r-0">
              <div className="flex items-center gap-2 mb-3">
                <span className="h-2.5 w-2.5 rounded-full bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.6)] animate-pulse" />
                <p className="text-[10px] font-black tracking-widest text-rose-400 uppercase">Before · Incident Peak</p>
              </div>

              {[
                { label: "Checkout Latency", value: `${BEFORE_STATE.latency_ms} ms`, bad: true },
                { label: "Pool Utilization", value: `${BEFORE_STATE.pool_utilization}%`, bad: true },
                { label: "Cart Abandonment", value: `${BEFORE_STATE.abandonment_pct}%`, bad: true },
                { label: "Est. Revenue Loss", value: `$${BEFORE_STATE.loss_usd.toLocaleString()}`, bad: true },
              ].map((row) => (
                <div key={row.label} className="flex items-center justify-between rounded-lg border border-rose-500/20 bg-rose-950/20 px-3 py-2">
                  <span className="text-[9px] font-black tracking-widest text-rose-300/70 uppercase">{row.label}</span>
                  <span className="text-[13px] font-black text-rose-400 shadow-[0_0_8px_rgba(244,63,94,0.3)]">{row.value}</span>
                </div>
              ))}

              <div className="mt-3 flex items-center justify-center rounded-xl border-2 border-rose-500/40 bg-rose-950/30 py-2.5 shadow-[0_0_20px_rgba(244,63,94,0.2)]">
                <p className="text-[10px] font-black text-rose-400 tracking-widest uppercase">{BEFORE_STATE.status}</p>
              </div>
            </div>

            {/* AFTER column */}
            <div className="p-5 space-y-3 bg-amber-950/5">
              <div className="flex items-center gap-2 mb-3">
                <span className={cn(
                  "h-2.5 w-2.5 rounded-full bg-amber-400",
                  healed ? "shadow-[0_0_10px_rgba(245,158,11,0.6)]" : "opacity-30"
                )} />
                <p className={cn("text-[10px] font-black tracking-widest uppercase", healed ? "text-amber-400" : "text-muted-foreground/30")}>After · Post-Playbook Simulation</p>
              </div>

              {[
                { label: "Checkout Latency", value: `${AFTER_STATE.latency_ms} ms` },
                { label: "Pool Utilization", value: `${AFTER_STATE.pool_utilization}%` },
                { label: "Cart Abandonment", value: `${AFTER_STATE.abandonment_pct}%` },
                { label: "Revenue Recovered", value: `$${BEFORE_STATE.loss_usd.toLocaleString()}` },
              ].map((row) => (
                <div key={row.label} className={cn(
                  "flex items-center justify-between rounded-lg border px-3 py-2 transition-all duration-700",
                  healed
                    ? "border-amber-500/25 bg-amber-950/20"
                    : "border-border/10 bg-background/5 opacity-30"
                )}>
                  <span className={cn("text-[9px] font-black tracking-widest uppercase", healed ? "text-amber-300/70" : "text-muted-foreground/30")}>{row.label}</span>
                  <span className={cn("text-[13px] font-black transition-all duration-700", healed ? "text-amber-400 shadow-[0_0_8px_rgba(245,158,11,0.3)]" : "text-muted-foreground/20")}>{row.value}</span>
                </div>
              ))}

              <div className={cn(
                "mt-3 flex items-center justify-center rounded-xl border-2 py-2.5 transition-all duration-700",
                healed
                  ? "border-amber-500/50 bg-amber-950/25 shadow-[0_0_25px_rgba(245,158,11,0.25)]"
                  : "border-border/10 bg-background/5 opacity-20"
              )}>
                <p className={cn("text-[10px] font-black tracking-widest uppercase", healed ? "text-amber-400" : "text-muted-foreground/20")}>
                  {healed ? AFTER_STATE.status + " · RECOVERY 100%" : "⏳ AWAITING PLAYBOOK EXECUTION"}
                </p>
              </div>
            </div>

          </div>
        </CardContent>
      </Card>

    </div>
  );
}
