/**
 * Simulation Dashboard
 */

"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";
import { SimulationResult } from "@/types";

export function SimulationDashboard() {
  const [actionId, setActionId] = useState("");
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const runSimulation = async () => {
    if (!actionId) return;
    setIsSimulating(true);
    try {
      const data = await api.simulateAction(actionId);
      setResult(data);
    } catch (error) {
      console.error("Simulation failed:", error);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Run Simulation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Enter Action ID"
              value={actionId}
              onChange={(e) => setActionId(e.target.value)}
            />
            <Button onClick={runSimulation} disabled={isSimulating} isLoading={isSimulating}>
              Simulate
            </Button>
          </div>
        </CardContent>
      </Card>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Outcome Probability</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Success Probability</span>
                <span className="text-2xl font-bold">{(result.successProbability * 100).toFixed(1)}%</span>
              </div>
              <Progress value={result.successProbability * 100} className="h-3" />
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Expected Value</span>
                <span className="text-lg font-semibold">${result.expectedValue.toFixed(2)}</span>
              </div>

              <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-900">
                <p className="text-xs font-medium text-slate-500 mb-1">Best Case</p>
                <p className="text-sm">{result.bestCase}</p>
              </div>
              <div className="rounded-lg bg-red-50 p-3 dark:bg-red-950/20">
                <p className="text-xs font-medium text-red-500 mb-1">Worst Case</p>
                <p className="text-sm text-red-700">{result.worstCase}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Downstream Effects</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {result.downstreamEffects.map((effect, i) => (
                  <div key={i} className="flex items-center justify-between rounded-lg border p-3">
                    <div>
                      <Badge variant="outline" className="mb-1">Hop {effect.hop}</Badge>
                      <p className="text-sm">{effect.description}</p>
                    </div>
                    <span className="text-sm font-medium">{(effect.probability * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}