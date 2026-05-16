/** * Real-time Activity Chart */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useWebSocket } from "@/hooks/useWebSocket";
export function RealtimeChart() {
  const [data, setData] = useState<number[]>([
    30, 45, 35, 50, 40, 60, 55, 70, 65, 80,
  ]);
  const { subscribe } = useWebSocket();
  useEffect(() => {
    return subscribe("agent_update", () => {
      setData((prev) => [
        ...prev.slice(1),
        Math.floor(Math.random() * 40) + 40,
      ]);
    });
  }, [subscribe]);
  const max = Math.max(...data);
  const min = Math.min(...data);
  return (
    <Card className="h-full">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Real-time Activity</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="flex items-end gap-1 h-48">
          {" "}
          {data.map((value, i) => (
            <div
              key={i}
              className="flex-1 rounded-t bg-card dark:bg-background transition-all duration-500"
              style={{
                height: `${((value - min) / (max - min || 1)) * 100}%`,
                opacity: 0.3 + (i / data.length) * 0.7,
              }}
            />
          ))}
        </div>{" "}
        <div className="flex justify-between mt-2 text-xs text-foreground0">
          {" "}
          <span>-10m</span> <span>Now</span>{" "}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
