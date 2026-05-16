/**
 * Insight Emergence Panel
 */

"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

export function InsightEmergence() {
  const [insights, setInsights] = useState<string[]>([]);

  useEffect(() => {
    api.getDreamReports().then((data) => {
      const allInsights = data.flatMap((r: any) => r.insightsDiscovered || []);
      setInsights(allInsights);
    });
  }, []);

  return (
    <Card className="h-96">
      <CardHeader>
        <CardTitle>Insight Emergence</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {insights.map((insight, i) => (
            <div
              key={i}
              className="flex items-center gap-3 rounded-lg border p-3 animate-in fade-in slide-in-from-left-4 duration-500"
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className="h-2 w-2 rounded-full bg-purple-500" />
              <span className="text-sm">{insight}</span>
              <Badge variant="outline" className="ml-auto text-xs">Dream</Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}