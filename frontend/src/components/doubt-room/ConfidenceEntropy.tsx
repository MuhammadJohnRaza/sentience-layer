"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ConfidenceEntropyProps {
  refreshTrigger?: number;
}

export function ConfidenceEntropy({ refreshTrigger }: ConfidenceEntropyProps) {
  const [entropy, setEntropy] = useState<number>(0.42);
  const [totalAudits, setTotalAudits] = useState<number>(28);
  const [levels, setLevels] = useState([
    { label: "High Confidence", value: 55, color: "bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]" },
    { label: "Medium Confidence", value: 25, color: "bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]" },
    { label: "Low Confidence", value: 15, color: "bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)]" },
    { label: "Uncertainty", value: 5, color: "bg-destructive shadow-[0_0_10px_rgba(239,68,68,0.3)]" }
  ]);

  const loadStats = async () => {
    try {
      const stats = await api.getDoubtStats();
      if (stats && typeof stats === "object") {
        if (!Array.isArray(stats)) {
          // Dynamic signature return structure
          setEntropy(stats.entropy ?? 0.42);
          setTotalAudits(stats.totalAudits ?? 28);
          if (stats.confidenceLevels) {
            const cl = stats.confidenceLevels;
            setLevels([
              { label: "High Confidence", value: cl.high ?? 55, color: "bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]" },
              { label: "Medium Confidence", value: cl.medium ?? 25, color: "bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]" },
              { label: "Low Confidence", value: cl.low ?? 15, color: "bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)]" },
              { label: "Uncertainty", value: cl.uncertainty ?? 5, color: "bg-destructive shadow-[0_0_10px_rgba(239,68,68,0.3)]" }
            ]);
          }
        } else {
          // Old array return list format fallback
          const highVal = stats.find((s: any) => s.label.toLowerCase().includes("high"))?.value ?? 55;
          const medVal = stats.find((s: any) => s.label.toLowerCase().includes("medium"))?.value ?? 25;
          const lowVal = stats.find((s: any) => s.label.toLowerCase().includes("low"))?.value ?? 15;
          const uncVal = stats.find((s: any) => s.label.toLowerCase().includes("uncertainty"))?.value ?? 5;
          
          setLevels([
            { label: "High Confidence", value: highVal, color: "bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]" },
            { label: "Medium Confidence", value: medVal, color: "bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]" },
            { label: "Low Confidence", value: lowVal, color: "bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)]" },
            { label: "Uncertainty", value: uncVal, color: "bg-destructive shadow-[0_0_10px_rgba(239,68,68,0.3)]" }
          ]);
        }
      }
    } catch (err) {
      console.error("Failed to load doubt stats:", err);
    }
  };

  useEffect(() => {
    loadStats();
  }, [refreshTrigger]);

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase">
            📊 Swarm Confidence Entropy
          </CardTitle>
          <p className="text-[9px] text-muted-foreground/80 uppercase tracking-wider mt-0.5">
            Total Live Audits: {totalAudits} | Shannon Index: H(X) = {entropy.toFixed(3)}
          </p>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <div className="flex h-36 items-end gap-3 justify-center">
          {levels.map((level) => (
            <div key={level.label} className="flex flex-1 flex-col items-center gap-2 group cursor-help">
              <div className="w-full relative h-28 flex items-end">
                <div
                  className={cn("w-full rounded-xl transition-all duration-700", level.color)}
                  style={{
                    height: `${Math.max(4, level.value)}%`,
                  }}
                />
                <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] font-black text-primary-foreground bg-[#0a0711] px-1.5 py-0.5 rounded border border-border/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  {level.value}%
                </span>
              </div>
              <span className="text-[9px] text-center font-black uppercase text-muted-foreground/80 tracking-wider">
                {level.label.split(" ")[0]}
              </span>
              <span className="text-[10px] font-mono font-bold text-primary-foreground">
                {level.value}%
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
