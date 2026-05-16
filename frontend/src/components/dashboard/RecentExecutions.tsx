/** * Recent Action Executions */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { formatRelativeTime } from "@/lib/utils";
import { Action } from "@/types";
export function RecentExecutions() {
  const [actions, setActions] = useState<Action[]>([]);
  useEffect(() => {
    api.getActions().then((data) => setActions(data.slice(0, 5)));
  }, []);
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Recent Executions</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="space-y-3">
          {" "}
          {actions.map((action) => (
            <div
              key={action.id}
              className="flex items-center justify-between rounded-lg border p-3"
            >
              {" "}
              <div>
                {" "}
                <p className="font-medium">{action.title}</p>{" "}
                <p className="text-xs text-foreground0">
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
                >
                  {" "}
                  {action.status}
                </Badge>{" "}
                <span className="text-xs text-muted-foreground">
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
