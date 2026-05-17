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
    <Card className="h-full border-2 border-border/50 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.6)]">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle className="text-primary-foreground font-black tracking-wider">Real-Time Cognitive Activity</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="flex items-end gap-1.5 h-48 px-2 border-b border-border/20 pb-1">
          {" "}
          {data.map((value, i) => (
            <div
              key={i}
              className="flex-1 rounded-t bg-gradient-to-t from-primary/10 via-primary/60 to-primary shadow-[0_0_15px_rgba(124,58,237,0.3)] transition-all duration-500 border-x border-t border-primary/40"
              style={{
                height: `${((value - min) / (max - min || 1)) * 100}%`,
                opacity: 0.4 + (i / data.length) * 0.6,
              }}
            />
          ))}
        </div>{" "}
        <div className="flex justify-between mt-3 text-xs font-bold tracking-widest text-primary-foreground/60">
          {" "}
          <span>-10M</span> <span>NOW</span>{" "}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
