/** * Agent Status Panel */ "use client";
import { useAgentTraces } from "@/hooks/useAgentTraces";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import { AGENT_TYPES } from "@/lib/constants";
export function AgentStatusPanel() {
  const { traces, isLoading } = useAgentTraces();
  if (isLoading) {
    return (
      <Card>
        {" "}
        <CardHeader>
          {" "}
          <CardTitle>Agent Status</CardTitle>{" "}
        </CardHeader>{" "}
        <CardContent>
          {" "}
          <div className="space-y-2">
            {" "}
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-8 bg-border/10 animate-pulse rounded" />
            ))}
          </div>{" "}
        </CardContent>{" "}
      </Card>
    );
  }
  return (
    <Card className="h-full">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Agent Status</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="space-y-4">
        {" "}
        {AGENT_TYPES.slice(0, 6).map((agent) => {
          const trace = traces.find((t) => t.agentType === agent.id);
          const status = trace?.status || "idle";
          return (
            <div key={agent.id} className="flex items-center gap-3">
              {" "}
              <div
                className="h-2 w-2 rounded-full"
                style={{
                  backgroundColor: agent.color,
                }}
              />{" "}
              <div className="flex-1">
                {" "}
                <div className="flex items-center justify-between">
                  {" "}
                  <span className="text-sm font-medium">{agent.name}</span>{" "}
                  <Badge
                    variant={status === "running" ? "default" : "secondary"}
                    className="text-xs"
                  >
                    {" "}
                    {status}
                  </Badge>{" "}
                </div>{" "}
                <Progress
                  value={
                    status === "running" ? 65 : status === "success" ? 100 : 0
                  }
                  className="mt-1 h-1"
                />{" "}
              </div>{" "}
            </div>
          );
        })}
      </CardContent>{" "}
    </Card>
  );
}
