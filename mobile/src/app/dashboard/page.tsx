/** * Dashboard Page */ "use client";
import { MetricsGrid } from "@/components/dashboard/MetricsGrid";
import { RealtimeChart } from "@/components/dashboard/RealtimeChart";
import { AgentStatusPanel } from "@/components/dashboard/AgentStatusPanel";
import { RecentExecutions } from "@/components/dashboard/RecentExecutions";
export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>{" "}
        <p className="text-foreground0">
          Real-time system overview and key metrics
        </p>{" "}
      </div>{" "}
      <MetricsGrid />{" "}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {" "}
        <div className="lg:col-span-2">
          {" "}
          <RealtimeChart />{" "}
        </div>{" "}
        <div>
          {" "}
          <AgentStatusPanel />{" "}
        </div>{" "}
      </div>{" "}
      <RecentExecutions />{" "}
    </div>
  );
}
