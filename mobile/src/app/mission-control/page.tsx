/** * Mission Control Page - System Overview */ "use client";
import { SystemMap } from "@/components/mission-control/SystemMap";
import { AgentNetwork } from "@/components/mission-control/AgentNetwork";
import { WorkflowHeatmap } from "@/components/mission-control/WorkflowHeatmap";
import { ResourceMonitor } from "@/components/mission-control/ResourceMonitor";
import { EconomicDashboard } from "@/components/mission-control/EconomicDashboard";
import { AutonomousHUD } from "@/components/mission-control/AutonomousHUD";

export default function MissionControlPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Mission Control
        </h1>
        <p className="text-foreground">
          System-wide orchestration and monitoring
        </p>
      </div>

      <AutonomousHUD />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SystemMap /> <AgentNetwork />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <WorkflowHeatmap />
        </div>
        <ResourceMonitor />
      </div>
      
      <EconomicDashboard />
    </div>
  );
}
