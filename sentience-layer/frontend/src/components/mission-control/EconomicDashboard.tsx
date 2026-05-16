/**
 * Economic Overview Dashboard
 */

"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { EconomicAnalysis } from "@/types";

export function EconomicDashboard() {
  const [analyses, setAnalyses] = useState<EconomicAnalysis[]>([]);

  useEffect(() => {
    // Fetch economic analyses for recent actions
    Promise.all([
      api.analyzeEconomics("action-1"),
      api.analyzeEconomics("action-2"),
    ]).then((results) => setAnalyses(results.filter(Boolean)));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Economic Impact</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {analyses.map((analysis) => (
            <div key={analysis.actionId} className="rounded-lg border p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Action {analysis.actionId}</span>
                <Badge variant={analysis.roiPercentage > 0 ? "default" : "destructive"}>
                  ROI {analysis.roiPercentage.toFixed(1)}%
                </Badge>
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-500">Cost</span>
                  <span>${analysis.totalCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Benefit</span>
                  <span>${analysis.totalBenefit.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">NPV</span>
                  <span className={analysis.netPresentValue > 0 ? "text-emerald-600" : "text-red-600"}>
                    ${analysis.netPresentValue.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}