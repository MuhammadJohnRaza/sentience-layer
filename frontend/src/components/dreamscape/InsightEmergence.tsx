/** * Insight Emergence Panel */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
export function InsightEmergence({ refreshTrigger }: { refreshTrigger?: number }) {
  const [insights, setInsights] = useState<string[]>([]);
  useEffect(() => {
    api.getDreamReports().then((data) => {
      const allInsights = data.flatMap((r: any) => r.insightsDiscovered || []);
      setInsights(allInsights);
    });
  }, [refreshTrigger]);
  return (
    <Card className="h-96 border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      {" "}
      <CardHeader className="border-b border-border/10 bg-card/40 p-4">
        {" "}
        <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
          🧠 Consolidated Insights
        </CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="p-4 overflow-y-auto h-[300px]">
        {" "}
        <div className="space-y-2">
          {" "}
          {insights.map((insight, i) => (
            <div
              key={i}
              className="flex items-center gap-3 rounded-lg border border-border/10 p-3 bg-black/40 animate-in fade-in slide-in-from-left-4 duration-500"
              style={{
                animationDelay: `${i * 100}ms`,
              }}
            >
              {" "}
              <div className="h-2 w-2 rounded-full bg-violet-500 animate-pulse" />{" "}
              <span className="text-xs text-primary-foreground leading-normal font-mono">{insight}</span>{" "}
              <Badge variant="outline" className="ml-auto text-[8px] tracking-widest font-black uppercase text-violet-400 bg-violet-950/20 border-violet-500/20">
                Dream
              </Badge>{" "}
            </div>
          ))}
          {insights.length === 0 && (
            <div className="text-center text-muted-foreground/60 text-xs py-12">
              No consolidated insights found. Trigger memory consolidation to emerge insights.
            </div>
          )}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
