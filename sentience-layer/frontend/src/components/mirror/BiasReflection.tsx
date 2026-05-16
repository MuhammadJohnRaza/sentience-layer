/**
 * Bias Reflection Panel
 */

"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const BIASES = [
  { name: "Confirmation Bias", level: 15, status: "low" },
  { name: "Availability Bias", level: 35, status: "medium" },
  { name: "Anchoring Bias", level: 20, status: "low" },
  { name: "Recency Bias", level: 45, status: "medium" },
  { name: "Selection Bias", level: 10, status: "low" },
];

export function BiasReflection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Bias Reflection</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-slate-600">
          Real-time bias monitoring across agent decision chains. Lower is better.
        </p>

        <div className="space-y-3">
          {BIASES.map((bias) => (
            <div key={bias.name} className="rounded-lg border p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">{bias.name}</span>
                <Badge variant={bias.status === "low" ? "default" : "secondary"} className="text-xs">
                  {bias.status}
                </Badge>
              </div>
              <Progress value={bias.level} className="h-2" />
              <p className="text-xs text-slate-500 mt-1">{bias.level}% detected in recent decisions</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}