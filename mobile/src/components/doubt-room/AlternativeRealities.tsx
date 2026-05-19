"use client";

import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface AlternativeRealitiesProps {
  activeDebate: any;
}

export function AlternativeRealities({ activeDebate }: AlternativeRealitiesProps) {
  const topicText = activeDebate?.topic || "Should we auto-execute high-confidence actions?";
  
  // Custom branches based on the topic
  const isPostgresList = topicText.toLowerCase().includes("postgres") || topicText.toLowerCase().includes("tool");
  
  const realityAlpha = {
    title: "Reality Alpha (Consensus Path)",
    status: "NOMINAL & ACTIVE",
    statusColor: "text-emerald-400 border-emerald-500/20 bg-emerald-950/20",
    metrics: [
      { label: "Latency", value: "22 ms" },
      { label: "Quarantine Risk", value: "0.1%" },
      { label: "ROI Potential", value: "+184.5%" }
    ],
    details: isPostgresList
      ? "Caching postgres queries locally maps Relational MCP indices with zero lookup drift."
      : "Automated scheduler dispatches consensus-approved index updates. Complete sandbox isolation verified."
  };

  const realityBeta = {
    title: "Reality Beta (Critic Risk Path)",
    status: "DISSENT SIMULATED",
    statusColor: "text-rose-400 border-rose-500/20 bg-rose-950/20",
    metrics: [
      { label: "Latency", value: "425 ms" },
      { label: "Quarantine Risk", value: "42.0%" },
      { label: "Economic Cost", value: "-$24.58K" }
    ],
    details: isPostgresList
      ? "Parallel query injections bypass transaction wrappers, resulting in connection thread lockouts."
      : "SQLite sandbox quarantine triggers transaction rollbacks, preventing potential database crashes."
  };

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4">
        <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center justify-between">
          <span>🔮 Swarm Alternative Causal Realities</span>
          <Badge className="bg-violet-950/40 border border-violet-500/30 text-violet-400 font-mono text-[8px] uppercase">
            Causal Prediction
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4 space-y-4">
        <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">
          Simulating divergent futures for active debate topic:
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Reality Alpha */}
          <div className="p-3.5 rounded-xl border border-emerald-500/10 bg-[#020403] space-y-3 relative overflow-hidden group hover:border-emerald-500/30 transition-all duration-300">
            <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl group-hover:bg-emerald-500/10 transition-all duration-300" />
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-black text-emerald-400 tracking-wide">
                {realityAlpha.title}
              </span>
              <Badge className={cn("text-[7px] font-mono font-black border", realityAlpha.statusColor)}>
                {realityAlpha.status}
              </Badge>
            </div>
            
            <p className="text-[10px] text-muted-foreground leading-normal min-h-[40px]">
              {realityAlpha.details}
            </p>
            
            <div className="grid grid-cols-3 gap-2 border-t border-emerald-500/10 pt-2.5">
              {realityAlpha.metrics.map((m, idx) => (
                <div key={idx} className="text-center">
                  <span className="text-[8px] font-black text-muted-foreground/60 uppercase tracking-widest block">
                    {m.label}
                  </span>
                  <span className="text-[10px] font-mono font-black text-emerald-400">
                    {m.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Reality Beta */}
          <div className="p-3.5 rounded-xl border border-rose-500/10 bg-[#050203] space-y-3 relative overflow-hidden group hover:border-rose-500/30 transition-all duration-300">
            <div className="absolute top-0 right-0 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl group-hover:bg-rose-500/10 transition-all duration-300" />
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-black text-rose-400 tracking-wide">
                {realityBeta.title}
              </span>
              <Badge className={cn("text-[7px] font-mono font-black border", realityBeta.statusColor)}>
                {realityBeta.status}
              </Badge>
            </div>
            
            <p className="text-[10px] text-muted-foreground leading-normal min-h-[40px]">
              {realityBeta.details}
            </p>
            
            <div className="grid grid-cols-3 gap-2 border-t border-rose-500/10 pt-2.5">
              {realityBeta.metrics.map((m, idx) => (
                <div key={idx} className="text-center">
                  <span className="text-[8px] font-black text-muted-foreground/60 uppercase tracking-widest block">
                    {m.label}
                  </span>
                  <span className="text-[10px] font-mono font-black text-rose-400">
                    {m.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
