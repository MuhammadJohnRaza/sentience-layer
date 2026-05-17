/** * Intervention Simulator Panel */ "use client";
import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
export function InterventionSimulator() {
  const [intervention, setIntervention] = useState("");
  const [target, setTarget] = useState("");
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const simulate = async () => {
    setIsLoading(true);
    try {
      const data = await api.simulateIntervention({
        intervention,
        target,
      });
      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Intervention Simulator</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="space-y-4">
        {" "}
        <div className="space-y-2">
          {" "}
          <label className="text-sm font-medium">
            Intervention (do X)
          </label>{" "}
          <Input
            placeholder="e.g., increase_budget"
            value={intervention}
            onChange={(e) => setIntervention(e.target.value)}
          />{" "}
        </div>{" "}
        <div className="space-y-2">
          {" "}
          <label className="text-sm font-medium">Target Variable</label>{" "}
          <Input
            placeholder="e.g., revenue"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />{" "}
        </div>{" "}
        <Button onClick={simulate} disabled={isLoading} className="w-full">
          {isLoading ? "Simulating..." : "Simulate Intervention"}
        </Button>{" "}
        {result && (
          <div className="rounded-lg bg-background p-4 dark:bg-card space-y-2">
            {" "}
            <div className="flex items-center justify-between">
              {" "}
              <span className="text-sm font-medium">Estimated Effect</span>{" "}
              <Badge
                variant={
                  result.estimated_effect > 0 ? "default" : "destructive"
                }
              >
                {" "}
                {result.estimated_effect > 0 ? "+" : ""}
                {result.estimated_effect.toFixed(2)}
              </Badge>{" "}
            </div>{" "}
            <div className="flex items-center justify-between">
              {" "}
              <span className="text-sm font-medium">Confidence</span>{" "}
              <span className="text-sm">
                {(result.confidence * 100).toFixed(0)}%
              </span>{" "}
            </div>{" "}
            <div className="flex items-center justify-between">
              {" "}
              <span className="text-sm font-medium">P-Value</span>{" "}
              <span className="text-sm">
                {result.p_value?.toFixed(3) || "N/A"}
              </span>{" "}
            </div>{" "}
          </div>
        )}
      </CardContent>{" "}
    </Card>
  );
}
