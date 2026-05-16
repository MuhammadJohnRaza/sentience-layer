/**
 * Resource Monitor Panel
 */

"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export function ResourceMonitor() {
  const resources = [
    { label: "CPU", value: 45, color: "bg-blue-500" },
    { label: "Memory", value: 62, color: "bg-purple-500" },
    { label: "GPU", value: 78, color: "bg-pink-500" },
    { label: "Network", value: 23, color: "bg-emerald-500" },
    { label: "Storage", value: 89, color: "bg-amber-500" },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resources</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {resources.map((res) => (
          <div key={res.label}>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium">{res.label}</span>
              <span className="text-sm text-slate-500">{res.value}%</span>
            </div>
            <Progress value={res.value} className="h-2" />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}