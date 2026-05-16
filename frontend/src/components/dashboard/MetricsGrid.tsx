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
        <Card key={metric.label} className="relative overflow-hidden">
          {" "}
          <CardContent className="p-6">
            {" "}
            <div className="flex items-center justify-between">
              {" "}
              <div>
                {" "}
                <p className="text-sm font-medium text-foreground0">
                  {metric.label}
                </p>{" "}
                <p className="text-2xl font-bold mt-1">{metric.value}</p>{" "}
              </div>{" "}
              <div
                className={cn(
                  "flex items-center rounded-full px-2 py-1 text-xs font-medium",
                  metric.trend === "up"
                    ? "bg-emerald-100 text-emerald-700"
                    : metric.trend === "down"
                      ? "bg-red-100 text-red-700"
                      : "bg-border/10 text-slate-700",
                )}
              >
                {" "}
                {metric.trend === "up"
                  ? "+"
                  : metric.trend === "down"
                    ? "-"
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
