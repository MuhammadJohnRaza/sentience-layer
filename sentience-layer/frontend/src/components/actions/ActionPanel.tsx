/**
 * Action Panel
 */

"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api";
import { Action } from "@/types";
import { formatRelativeTime } from "@/lib/utils";

export function ActionPanel() {
  const [actions, setActions] = useState<Action[]>([]);
  const [executing, setExecuting] = useState<string | null>(null);

  useEffect(() => {
    api.getActions().then((data) => setActions(data));
  }, []);

  const execute = async (actionId: string) => {
    setExecuting(actionId);
    try {
      await api.executeAction(actionId);
      // Refresh
      const updated = await api.getActions();
      setActions(updated);
    } finally {
      setExecuting(null);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {actions.map((action) => (
        <Card key={action.id}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">{action.title}</CardTitle>
              <Badge variant={
                action.status === "completed" ? "default" :
                action.status === "failed" ? "destructive" :
                action.status === "running" ? "secondary" : "outline"
              }>
                {action.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-slate-600">{action.description}</p>
            
            <div className="space-y-2">
              {action.steps.map((step) => (
                <div key={step.id} className="flex items-center gap-2">
                  <div className={cn(
                    "h-2 w-2 rounded-full",
                    step.status === "completed" ? "bg-emerald-500" :
                    step.status === "running" ? "bg-blue-500 animate-pulse" :
                    step.status === "failed" ? "bg-red-500" : "bg-slate-300"
                  )} />
                  <span className="text-xs">{step.description}</span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500">Impact: {action.impactScore}/100</span>
                <span className="text-xs text-slate-500">•</span>
                <span className="text-xs text-slate-500">{formatRelativeTime(action.createdAt)}</span>
              </div>
              {action.status === "pending" && (
                <Button 
                  size="sm" 
                  onClick={() => execute(action.id)}
                  isLoading={executing === action.id}
                >
                  Execute
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

import { cn } from "@/lib/utils";