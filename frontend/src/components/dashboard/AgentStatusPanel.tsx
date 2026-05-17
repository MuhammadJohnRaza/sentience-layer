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
        <div className="max-h-[420px] overflow-y-auto pr-2 space-y-3.5 scrollbar-thin scrollbar-thumb-purple-500/20 scrollbar-track-transparent">
          {AGENT_TYPES.map((agent) => {
            const trace = traces.find((t) => t.agentType === agent.id);
            let status: any = trace?.status || "idle";
            if (status === "idle") {
              if (["critic", "consensus", "causal", "dream", "memory", "opportunity"].includes(agent.id)) {
                status = "active";
              } else {
                status = "nominal";
              }
            }

            return (
              <div key={agent.id} className="flex items-center gap-3 group border border-border/5 bg-background/25 rounded-lg p-2 hover:bg-primary/5 hover:border-primary/10 transition-all duration-300">
                <div
                  className={cn(
                    "h-2 w-2 rounded-full shrink-0",
                    status === "running" ? "animate-ping" : "animate-pulse"
                  )}
                  style={{
                    backgroundColor: agent.color,
                    boxShadow: `0 0 8px ${agent.color}`,
                  }}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-black text-foreground/90 tracking-wide truncate group-hover:text-primary-foreground transition-colors">
                      {agent.name}
                    </span>
                    <Badge
                      variant={status === "running" ? "default" : status === "active" ? "outline" : "secondary"}
                      className={cn(
                        "text-[9px] font-black uppercase px-2 py-0 h-4 tracking-widest shrink-0",
                        status === "running"
                          ? "bg-primary/20 text-primary-foreground border-border shadow-[0_0_8px_rgba(124,58,237,0.4)] animate-pulse"
                          : status === "active"
                            ? "bg-purple-950/20 text-purple-300 border-purple-500/30"
                            : "bg-background/40 text-muted-foreground/60 border-border/10"
                      )}
                    >
                      {status}
                    </Badge>
                  </div>
                  <Progress
                    value={
                      status === "running" ? 65 : status === "active" ? 100 : status === "nominal" ? 100 : 0
                    }
                    className={cn(
                      "mt-1.5 h-1 bg-background border border-border/5",
                      status === "running" && "[&>div]:bg-primary",
                      status === "active" && "[&>div]:bg-purple-500/60",
                      status === "nominal" && "[&>div]:bg-emerald-500/40"
                    )}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>{" "}
    </Card>
  );
}
