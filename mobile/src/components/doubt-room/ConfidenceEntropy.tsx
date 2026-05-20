"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ConfidenceEntropyProps {
  refreshTrigger?: number;
  activeDebate?: any;
}

export function ConfidenceEntropy({ refreshTrigger, activeDebate }: ConfidenceEntropyProps) {
  const [stats, setStats] = useState<{
    entropy: number;
    totalAudits: number;
    confidenceLevels: {
      high: number;
      medium: number;
      low: number;
      uncertainty: number;
    };
  }>({
    entropy: 0.35,
    totalAudits: 28,
    confidenceLevels: {
      high: 55,
      medium: 25,
      low: 15,
      uncertainty: 5
    }
  });

  const fetchStats = async () => {
    try {
      const data = await api.getDoubtStats();
      if (data && !Array.isArray(data)) {
        setStats(data as {
          entropy: number;
          totalAudits: number;
          confidenceLevels: { high: number; medium: number; low: number; uncertainty: number };
        });
      }
    } catch (err) {
      console.error("Failed to load doubt stats:", err);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [refreshTrigger, activeDebate]);

  const entropyLevels = [
    {
      label: "High Confidence",
      value: stats.confidenceLevels.high,
      color: "bg-gradient-to-t from-emerald-600 to-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.3)]",
    },
    {
      label: "Medium Confidence",
      value: stats.confidenceLevels.medium,
      color: "bg-gradient-to-t from-indigo-600 to-indigo-400 shadow-[0_0_12px_rgba(129,140,248,0.3)]",
    },
    {
      label: "Low Confidence",
      value: stats.confidenceLevels.low,
      color: "bg-gradient-to-t from-amber-600 to-amber-400 shadow-[0_0_12px_rgba(251,191,36,0.3)]",
    },
    {
      label: "Uncertainty",
      value: stats.confidenceLevels.uncertainty,
      color: "bg-gradient-to-t from-rose-600 to-rose-400 shadow-[0_0_12px_rgba(248,113,113,0.3)]",
    },
  ];

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            📊 Swarm Confidence Entropy
          </CardTitle>
          <p className="text-[10px] text-muted-foreground/80 uppercase tracking-wider mt-1">
            Statistical measurement of agent uncertainty levels across {stats.totalAudits} total audits
          </p>
        </div>
        <Badge className="bg-destructive/20 border border-destructive/30 text-rose-400 font-mono text-[9px] px-2.5 py-0.5">
          ENTROPY: {stats.entropy.toFixed(3)} H
        </Badge>
      </CardHeader>
      <CardContent className="p-6">
        <div className="flex h-[200px] items-end gap-3 pt-4 border-b border-border/10 pb-2">
          {entropyLevels.map((level) => (
            <div
              key={level.label}
              className="flex flex-1 flex-col items-center gap-2 h-full justify-end"
            >
              <span className="text-[10px] font-mono font-black text-primary-foreground/90">
                {level.value}%
              </span>
              <div
                className={cn("w-full rounded-t-lg transition-all duration-700 ease-out", level.color)}
                style={{
                  height: `${Math.max(8, level.value * 1.5)}%`,
                }}
              />
              <span className="text-[9px] font-black text-muted-foreground uppercase text-center mt-1 leading-normal tracking-wide line-clamp-1 w-full">
                {level.label}
              </span>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-center justify-between text-[9px] text-muted-foreground font-mono uppercase">
          <span>⚙️ SYSTEM METRIC: SHANNON_ENTROPY_INDEX</span>
          <span>STATUS: AUDIT_STABLE</span>
        </div>
      </CardContent>
    </Card>
  );
}
