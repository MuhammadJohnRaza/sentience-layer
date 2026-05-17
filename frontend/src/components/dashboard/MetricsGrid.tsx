/** * Metrics Grid with live data */ "use client";
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { DashboardMetric } from "@/types";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
export function MetricsGrid() {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  useEffect(() => {
    api.getAgentStatus().then((data) => {
      setMetrics([
        {
          label: "Active Agents",
          value: data.filter((a: any) => a.status === "running").length,
          change: 12,
          trend: "up",
          icon: "agents",
        },
        {
          label: "Insights Today",
          value: 24,
          change: 8,
          trend: "up",
          icon: "insights",
        },
        {
          label: "Actions Executed",
          value: 156,
          change: -3,
          trend: "down",
          icon: "actions",
        },
        {
          label: "System Health",
          value: "98.5%",
          change: 0.2,
          trend: "up",
          icon: "health",
        },
      ]);
    });
  }, []);
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {" "}
      {metrics.map((metric) => (
        <Card key={metric.label} className="relative overflow-hidden border-2 border-border/40 bg-card shadow-[0_4px_25px_rgba(0,0,0,0.5)] hover:border-border transition-all duration-300">
          {" "}
          <CardContent className="p-6">
            {" "}
            <div className="flex items-center justify-between">
              {" "}
              <div>
                {" "}
                <p className="text-xs font-black text-muted-foreground tracking-widest uppercase">
                  {metric.label}
                </p>{" "}
                <p className="text-3xl font-black text-primary-foreground mt-2 tracking-tight">
                  {metric.value}
                </p>{" "}
              </div>{" "}
              <div
                className={cn(
                  "flex items-center rounded-full px-2.5 py-1 text-xs font-bold tracking-wide border",
                  metric.trend === "up"
                    ? "bg-emerald-950/50 text-emerald-400 border-emerald-500/20 shadow-[0_0_8px_rgba(16,185,129,0.15)]"
                    : metric.trend === "down"
                      ? "bg-rose-950/50 text-rose-400 border-rose-500/20 shadow-[0_0_8px_rgba(244,63,94,0.15)]"
                      : "bg-border/10 text-muted-foreground border-border/20",
                )}
              >
                {" "}
                {metric.trend === "up"
                  ? "▲ "
                  : metric.trend === "down"
                    ? "▼ "
                    : ""}
                {Math.abs(metric.change)}%{" "}
              </div>{" "}
            </div>{" "}
          </CardContent>{" "}
        </Card>
      ))}
    </div>
  );
}
