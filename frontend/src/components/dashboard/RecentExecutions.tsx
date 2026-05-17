/** * Recent Action Executions */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { formatRelativeTime, cn } from "@/lib/utils";
import { Action } from "@/types";
export function RecentExecutions() {
  const [actions, setActions] = useState<Action[]>([]);
  useEffect(() => {
    api.getActions().then((data) => setActions(data.slice(0, 5)));
  }, []);
  return (
    <Card className="border-2 border-border/50 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.6)]">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle className="text-primary-foreground font-black tracking-wider">Recent Executions Log</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="space-y-3">
          {" "}
          {actions.map((action) => (
            <div
              key={action.id}
              className="flex items-center justify-between rounded-lg border border-border/25 bg-background/30 p-4 hover:border-border transition-all duration-300 hover:shadow-[0_0_15px_rgba(124,58,237,0.15)]"
            >
              {" "}
              <div>
                {" "}
                <p className="font-bold text-sm text-foreground tracking-wide">{action.title}</p>{" "}
                <p className="text-xs text-muted-foreground/80 mt-1">
                  {action.description}
                </p>{" "}
              </div>{" "}
              <div className="flex items-center gap-3">
                {" "}
                <Badge
                  variant={
                    action.status === "completed"
                      ? "default"
                      : action.status === "failed"
                        ? "destructive"
                        : action.status === "running"
                          ? "secondary"
                          : "outline"
                  }
                  className={cn(
                    "text-xs font-bold tracking-wide uppercase px-2.5 py-0.5 border",
                    action.status === "completed"
                      ? "bg-emerald-950/50 text-emerald-400 border-emerald-500/25"
                      : action.status === "failed"
                        ? "bg-rose-950/50 text-rose-400 border-rose-500/25 shadow-[0_0_10px_rgba(244,63,94,0.1)]"
                        : action.status === "running"
                          ? "bg-primary/25 text-primary-foreground border-border shadow-[0_0_10px_rgba(124,58,237,0.3)] animate-pulse"
                          : "bg-background border-border/20 text-muted-foreground"
                  )}
                >
                  {" "}
                  {action.status}
                </Badge>{" "}
                <span className="text-xs font-semibold text-muted-foreground/60 tracking-wider">
                  {formatRelativeTime(action.createdAt)}
                </span>{" "}
              </div>{" "}
            </div>
          ))}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
