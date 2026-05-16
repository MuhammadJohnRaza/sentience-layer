/** * Trace Timeline Visualization */
import { AgentTrace } from "@/types";
import { cn } from "@/lib/utils";
export function TraceTimeline({ trace }: { trace: AgentTrace }) {
  const steps = trace.reasoning.map((r, i) => ({
    step: i + 1,
    label: r.action,
    status:
      r.confidence > 0.7 ? "success" : r.confidence > 0.4 ? "warning" : "error",
    time: `${r.step * 2}s`,
  }));
  return (
    <div className="relative">
      {" "}
      <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-slate-200 dark:bg-border/30" />{" "}
      <div className="space-y-4">
        {" "}
        {steps.map((step) => (
          <div
            key={step.step}
            className="relative flex items-center gap-4 pl-10"
          >
            {" "}
            <div
              className={cn(
                "absolute left-2 h-4 w-4 rounded-full border-2",
                step.status === "success"
                  ? "bg-primary border-emerald-500"
                  : step.status === "warning"
                    ? "bg-amber-500 border-amber-500"
                    : "bg-destructive border-red-500",
              )}
            />{" "}
            <div className="flex-1 rounded-lg border p-3">
              {" "}
              <div className="flex items-center justify-between">
                {" "}
                <span className="font-medium text-sm">
                  Step {step.step}: {step.label}
                </span>{" "}
                <span className="text-xs text-muted-foreground">
                  {step.time}
                </span>{" "}
              </div>{" "}
            </div>{" "}
          </div>
        ))}
      </div>{" "}
    </div>
  );
}
