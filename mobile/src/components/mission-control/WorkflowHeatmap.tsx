/** * Workflow Execution Heatmap */ "use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
const HOURS = Array.from(
  {
    length: 24,
  },
  (_, i) => i,
);
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
export function WorkflowHeatmap() {
  // Generate fake heatmap data
  const data = DAYS.map(() => HOURS.map(() => Math.floor(Math.random() * 10)));
  const maxValue = Math.max(...data.flat());
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Workflow Heatmap</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="space-y-1">
          {" "}
          <div className="flex">
            {" "}
            <div className="w-8" />{" "}
            {HOURS.filter((_, i) => i % 3 === 0).map((h) => (
              <div
                key={h}
                className="flex-1 text-[10px] text-muted-foreground text-center"
              >
                {h}:00
              </div>
            ))}
          </div>{" "}
          {DAYS.map((day, dayIdx) => (
            <div key={day} className="flex items-center gap-1">
              {" "}
              <span className="w-8 text-xs text-foreground0">{day}</span>{" "}
              <div className="flex flex-1 gap-0.5">
                {" "}
                {HOURS.map((_, hourIdx) => {
                  const value = data[dayIdx][hourIdx];
                  const intensity = value / maxValue;
                  return (
                    <div
                      key={hourIdx}
                      className="h-4 flex-1 rounded-sm"
                      style={{
                        backgroundColor:
                          intensity > 0.7
                            ? "#0f172a"
                            : intensity > 0.4
                              ? "#475569"
                              : intensity > 0.1
                                ? "#94a3b8"
                                : "#e2e8f0",
                      }}
                      title={`${day}
${hourIdx}:00 - ${value}
executions`}
                    />
                  );
                })}
              </div>{" "}
            </div>
          ))}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
