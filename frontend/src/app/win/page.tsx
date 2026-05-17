"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface WinItem {
  id: string;
  title: string;
  category: "Economic" | "Performance" | "Containment" | "Consolidation";
  metric: string;
  agent: string;
  timestamp: string;
  description: string;
  confidence: number;
}

const WINS_LEDGER: WinItem[] = [
  {
    id: "win_1",
    title: "Postgres Connection Pool Saturation Avoidance",
    category: "Containment",
    metric: "100% Contained",
    agent: "CriticAgent",
    timestamp: "May 17, 09:34 PM",
    description: "Successfully detected a transaction sequence loop anomaly inside checkout query queues. Quarantined active thread in Doubt Room sandbox, preventing general database lockout.",
    confidence: 0.98,
  },
  {
    id: "win_2",
    title: "Checkout Query Latency Index Optimization",
    category: "Performance",
    metric: "-325ms Latency",
    agent: "ConsensusAgent",
    timestamp: "May 17, 09:30 PM",
    description: "Analyzed query path coefficients. Automatically injected optimized checkout index wrappers, bringing baseline SQL query latencies down from 425ms to 100ms.",
    confidence: 0.96,
  },
  {
    id: "win_3",
    title: "Active Sales Conversion Anomaly Intervention",
    category: "Economic",
    metric: "+$24,580 Yield",
    agent: "SwarmOrchestrator",
    timestamp: "May 17, 09:25 PM",
    description: "Triggered dynamic Cart Recovery Retargeting discount protocols based on Causal Inference opportunity scans, recovering a 30% pipeline abandonment drift.",
    confidence: 0.94,
  },
  {
    id: "win_4",
    title: "Memory Vault Thread Consolidation",
    category: "Consolidation",
    metric: "4 Traces Merged",
    agent: "DreamAgent",
    timestamp: "May 17, 09:15 PM",
    description: "Consolidated temporary transaction files and vector caches into the primary SQLite database nodes, reducing table fragmentations by 18.5%.",
    confidence: 0.95,
  },
];

export default function WinPage() {
  const [totalSaved, setTotalSaved] = useState(0);

  useEffect(() => {
    // Elegant micro-animation counting up
    const target = 24580;
    const duration = 1500;
    const start = Date.now();
    
    const timer = setInterval(() => {
      const elapsed = Date.now() - start;
      if (elapsed >= duration) {
        setTotalSaved(target);
        clearInterval(timer);
      } else {
        setTotalSaved(Math.floor((elapsed / duration) * target));
      }
    }, 16);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-purple-400 via-amber-300 to-emerald-400 bg-clip-text text-transparent">
            Agentic Wins Ledger
          </h1>
          <p className="text-sm text-muted-foreground/80 mt-1">
            Visualizing realized economic profits, query optimizations, and self-healing containment records consolidated by the cognitive swarm.
          </p>
        </div>
        <Badge className="w-fit text-[10px] font-black tracking-widest bg-emerald-950/40 text-emerald-400 border border-emerald-500/30 px-3 py-1 uppercase shrink-0">
          🟢 Telemetry Sync: Nominal
        </Badge>
      </div>

      {/* METRICS ROW */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* STAT 1: ROI */}
        <Card className="relative overflow-hidden bg-gradient-to-b from-[#0e0c1b] to-[#04020a] border-border/20 shadow-[0_4px_20px_rgba(0,0,0,0.6)]">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-500/5 via-transparent to-transparent pointer-events-none" />
          <CardHeader className="pb-2">
            <span className="text-[10px] font-black text-purple-400 tracking-widest uppercase">Realized Swarm ROI</span>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-200 to-purple-400">
              ${totalSaved.toLocaleString()}
            </div>
            <p className="text-[10px] text-muted-foreground mt-1">
              Economic pipeline savings recovered this week
            </p>
          </CardContent>
        </Card>

        {/* STAT 2: LATENCY */}
        <Card className="relative overflow-hidden bg-gradient-to-b from-[#0c1214] to-[#010305] border-border/20 shadow-[0_4px_20px_rgba(0,0,0,0.6)]">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-500/5 via-transparent to-transparent pointer-events-none" />
          <CardHeader className="pb-2">
            <span className="text-[10px] font-black text-emerald-400 tracking-widest uppercase">Total Latency Saved</span>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 to-emerald-400">
              -325 ms
            </div>
            <p className="text-[10px] text-muted-foreground mt-1">
              Checkout query load metrics compressed
            </p>
          </CardContent>
        </Card>

        {/* STAT 3: THREATS */}
        <Card className="relative overflow-hidden bg-gradient-to-b from-[#140b0e] to-[#040103] border-border/20 shadow-[0_4px_20px_rgba(0,0,0,0.6)]">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-500/5 via-transparent to-transparent pointer-events-none" />
          <CardHeader className="pb-2">
            <span className="text-[10px] font-black text-amber-400 tracking-widest uppercase">Threat Containment</span>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-200 to-amber-400">
              100%
            </div>
            <p className="text-[10px] text-muted-foreground mt-1">
              Anomalous transactions quarantined safely
            </p>
          </CardContent>
        </Card>

        {/* STAT 4: NODES */}
        <Card className="relative overflow-hidden bg-gradient-to-b from-[#0a0a0f] to-[#010103] border-border/20 shadow-[0_4px_20px_rgba(0,0,0,0.6)]">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-500/5 via-transparent to-transparent pointer-events-none" />
          <CardHeader className="pb-2">
            <span className="text-[10px] font-black text-indigo-400 tracking-widest uppercase">Consolidated Traces</span>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-200 to-indigo-400">
              284 Nodes
            </div>
            <p className="text-[10px] text-muted-foreground mt-1">
              SQLite transaction vector consolidation yield
            </p>
          </CardContent>
        </Card>
      </div>

      {/* LEDGER COMPONENT */}
      <Card className="relative overflow-hidden bg-gradient-to-b from-[#080810] via-background to-background border-border/20 shadow-[0_4px_30px_rgba(0,0,0,0.8)]">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-500/5 via-transparent to-transparent pointer-events-none" />
        <CardHeader className="border-b border-border/10 pb-4">
          <CardTitle className="text-lg font-black tracking-wider uppercase text-purple-200">
            Realized System Wins Log
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-6 space-y-4">
          {WINS_LEDGER.map((win) => {
            const isEconomic = win.category === "Economic";
            const isPerformance = win.category === "Performance";
            const isContainment = win.category === "Containment";

            const badgeColor = isEconomic 
              ? "bg-purple-950/40 border-purple-500/30 text-purple-300"
              : isPerformance
                ? "bg-emerald-950/40 border-emerald-500/30 text-emerald-300"
                : isContainment
                  ? "bg-amber-950/40 border-amber-500/30 text-amber-300"
                  : "bg-indigo-950/40 border-indigo-500/30 text-indigo-300";

            return (
              <div 
                key={win.id}
                className="group flex flex-col md:flex-row md:items-start gap-4 p-4 rounded-xl border border-border/10 bg-[#04040a]/40 hover:bg-[#070712]/60 hover:border-border/30 hover:shadow-[0_0_15px_rgba(124,58,237,0.15)] transition-all duration-300"
              >
                {/* Category Badge & Metric */}
                <div className="md:w-44 shrink-0 flex flex-row md:flex-col items-center md:items-start justify-between md:justify-start gap-2">
                  <Badge className={`text-[8px] font-black tracking-widest px-2 py-0.5 border uppercase ${badgeColor}`}>
                    {win.category}
                  </Badge>
                  <div className={`text-sm font-black md:mt-1 ${
                    isEconomic ? "text-purple-400" : isPerformance ? "text-emerald-400" : isContainment ? "text-amber-400" : "text-indigo-400"
                  }`}>
                    {win.metric}
                  </div>
                  <span className="text-[8px] font-mono text-muted-foreground/50 md:mt-2">
                    {win.timestamp}
                  </span>
                </div>

                {/* Main Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <h3 className="text-sm font-black text-primary-foreground group-hover:text-amber-300 transition-colors">
                      {win.title}
                    </h3>
                    <div className="flex items-center gap-2">
                      <span className="text-[9px] font-mono text-muted-foreground/60 uppercase">
                        Agent: {win.agent}
                      </span>
                      <span className="text-[9px] font-black text-emerald-400">
                        {(win.confidence * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-muted-foreground/75 leading-relaxed mt-2 pl-3 border-l border-purple-500/20">
                    {win.description}
                  </p>
                </div>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
}
