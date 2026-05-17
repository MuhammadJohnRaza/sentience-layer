/** * Agent Network Visualization */ "use client";
import { useAgentTraces } from "@/hooks/useAgentTraces";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AGENT_TYPES } from "@/lib/constants";
export function AgentNetwork() {
  const { traces } = useAgentTraces();
  return (
    <Card className="h-96">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Agent Network</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="space-y-3">
          {" "}
          {AGENT_TYPES.map((agent) => {
            const trace = traces.find((t) => t.agentType === agent.id);
            const isActive = trace?.status === "running";
            return (
              <div
                key={agent.id}
                className="flex items-center justify-between rounded-lg border p-2"
              >
                {" "}
                <div className="flex items-center gap-3">
                  {" "}
                  <div
                    className="h-3 w-3 rounded-full"
                    style={{
                      backgroundColor: agent.color,
                    }}
                  />{" "}
                  <span className="text-sm font-medium">{agent.name}</span>{" "}
                </div>{" "}
                <div className="flex items-center gap-2">
                  {" "}
                  {isActive && (
                    <span className="relative flex h-2 w-2">
                      {" "}
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />{" "}
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />{" "}
                    </span>
                  )}
                  <Badge variant="secondary" className="text-xs">
                    {" "}
                    {trace?.status || "idle"}
                  </Badge>{" "}
                </div>{" "}
              </div>
            );
          })}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
