/**
 * Economic Overview Dashboard
 */
"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { EconomicAnalysis } from "@/types";
import { cn } from "@/lib/utils";

export function EconomicDashboard() {
  const [analyses, setAnalyses] = useState<EconomicAnalysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch economic analyses for recent actions
    Promise.all([
      api.analyzeEconomics("action-1").catch(() => null),
      api.analyzeEconomics("action-2").catch(() => null),
    ])
      .then((results) => {
        setAnalyses(results.filter((r): r is EconomicAnalysis => r !== null));
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  return (
    <Card className="border border-border/20 bg-card/25 shadow-[0_8px_30px_rgba(0,0,0,0.6)] backdrop-blur-md">
      <CardHeader className="border-b border-border/10 pb-4">
        <div>
          <CardTitle className="text-md font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            📊 ECONOMIC IMPACT METRICS
          </CardTitle>
          <CardDescription className="text-[10px] font-bold tracking-wider text-muted-foreground/80 uppercase">
            Cost-Benefit swarm analytics & net present valuations
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="pt-6">
        {isLoading ? (
          <div className="h-32 w-full flex items-center justify-center">
            <span className="h-6 w-6 rounded-full border-2 border-primary border-t-transparent animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
            {analyses.map((analysis) => {
              const roi = analysis?.roiPercentage ?? 0;
              const cost = analysis?.totalCost ?? 0;
              const benefit = analysis?.totalBenefit ?? 0;
              const npv = analysis?.netPresentValue ?? 0;
              const riskAdjusted = analysis?.riskAdjustedReturn ?? 0.0;

              return (
                <div 
                  key={analysis.actionId} 
                  className={cn(
                    "rounded-xl border p-4.5 bg-[#020207]/45 transition-all duration-300 hover:scale-[1.01] flex flex-col justify-between space-y-4",
                    roi > 100 
                      ? "border-emerald-500/20 hover:border-emerald-500/40" 
                      : "border-border/25 hover:border-border/55"
                  )}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-black text-primary-foreground tracking-wider uppercase font-mono">
                      ⚙️ ACTION {analysis.actionId.toUpperCase()}
                    </span>
                    <Badge
                      className={cn(
                        "text-[9px] font-extrabold tracking-widest uppercase px-2 py-0.5",
                        roi > 100 
                          ? "bg-emerald-950/60 border border-emerald-500/30 text-emerald-400" 
                          : "bg-amber-950/60 border border-amber-500/30 text-amber-400"
                      )}
                    >
                      ROI {roi.toFixed(1)}%
                    </Badge>
                  </div>

                  <div className="space-y-2.5 text-xs font-medium text-muted-foreground">
                    <div className="flex justify-between items-center py-0.5 border-b border-border/5">
                      <span>Compute & Ops Cost</span>
                      <span className="font-extrabold text-foreground font-mono">${cost.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                    </div>
                    
                    <div className="flex justify-between items-center py-0.5 border-b border-border/5">
                      <span>Projected Benefit Gain</span>
                      <span className="font-extrabold text-emerald-400 font-mono">${benefit.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                    </div>

                    <div className="flex justify-between items-center py-0.5 border-b border-border/5">
                      <span>Net Present Value (NPV)</span>
                      <span
                        className={cn(
                          "font-black font-mono",
                          npv > 0 ? "text-emerald-400" : "text-destructive"
                        )}
                      >
                        ${npv.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </span>
                    </div>

                    <div className="flex justify-between items-center py-0.5">
                      <span>Risk-Adjusted Confidence</span>
                      <span className="font-black text-amber-300 font-mono">{(riskAdjusted * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
