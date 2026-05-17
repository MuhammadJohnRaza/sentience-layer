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
    <Card className="h-full border-2 border-border/50 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.6)]">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle className="text-primary-foreground font-black tracking-wider">Agent Status Modules</CardTitle>{" "}
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
                className="h-2.5 w-2.5 rounded-full animate-ping"
                style={{
                  backgroundColor: agent.color,
                  boxShadow: `0 0 10px ${agent.color}`,
                }}
              />{" "}
              <div className="flex-1">
                {" "}
                <div className="flex items-center justify-between">
                  {" "}
                  <span className="text-sm font-black text-foreground/90 tracking-wide">{agent.name}</span>{" "}
                  <Badge
                    variant={status === "running" ? "default" : "secondary"}
                    className={cn(
                      "text-xs font-bold uppercase px-2 py-0.5 border tracking-wider",
                      status === "running"
                        ? "bg-primary/20 text-primary-foreground border-border shadow-[0_0_8px_rgba(124,58,237,0.4)] animate-pulse"
                        : "bg-background text-muted-foreground border-border/20"
                    )}
                  >
                    {" "}
                    {status}
                  </Badge>{" "}
                </div>{" "}
                <Progress
                  value={
                    status === "running" ? 65 : status === "success" ? 100 : 0
                  }
                  className="mt-2 h-1.5 bg-background border border-border/10"
                />{" "}
              </div>{" "}
            </div>
          );
        })}
      </CardContent>{" "}
    </Card>
  );
}
