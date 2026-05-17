/** Real-time Latency Chart — spikes red at anomaly, recovers to gold after playbook */
"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// Simulated latency timeline:
// Values above 200 = anomaly zone (red), below 50 = nominal zone (gold/green)
const ANOMALY_SEQUENCE = [
  22, 28, 19, 35, 24, 45, 68, 112, 198, 285, 360, 425,   // spike
  425, 398, 410, 425, 415,                                 // peak plateau
  380, 295, 210, 140, 85, 55, 38, 22, 18, 22, 20, 22,    // recovery after playbook
];

function latencyColor(val: number) {
  if (val >= 300) return "from-rose-700/20 via-rose-500/80 to-rose-400 border-rose-400/60 shadow-[0_0_14px_rgba(244,63,94,0.5)]";
  if (val >= 150) return "from-amber-700/20 via-amber-500/70 to-amber-400 border-amber-400/50 shadow-[0_0_10px_rgba(245,158,11,0.4)]";
  if (val >= 60)  return "from-yellow-700/10 via-yellow-500/50 to-yellow-300 border-yellow-400/40";
  return "from-violet-900/20 via-violet-500/50 to-amber-400 border-amber-400/50 shadow-[0_0_10px_rgba(245,158,11,0.3)]";
}

function latencyLabel(val: number) {
  if (val >= 300) return { text: "CRITICAL", cls: "text-rose-400" };
  if (val >= 150) return { text: "WARNING", cls: "text-amber-400" };
  if (val >= 60)  return { text: "ELEVATED", cls: "text-yellow-400" };
  return { text: "NOMINAL", cls: "text-amber-400" };
}

export function RealtimeChart() {
  const WINDOW = 16; // bars visible
  const [cursor, setCursor] = useState(0);
  const [phase, setPhase] = useState<"anomaly" | "healed">("anomaly");

  useEffect(() => {
    const id = setInterval(() => {
      setCursor((prev) => {
        const next = prev + 1;
        if (next >= ANOMALY_SEQUENCE.length) return 0;
        return next;
      });
    }, 420);
    return () => clearInterval(id);
  }, []);

  // Mark phase based on cursor position
  useEffect(() => {
    const current = ANOMALY_SEQUENCE[cursor];
    setPhase(current < 60 && cursor > 18 ? "healed" : "anomaly");
  }, [cursor]);

  const window = ANOMALY_SEQUENCE.slice(
    Math.max(0, cursor - WINDOW + 1),
    cursor + 1
  );

  const current = ANOMALY_SEQUENCE[cursor];
  const label = latencyLabel(current);
  const max = 425;

  return (
    <Card className={cn(
      "h-full border-2 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.6)] transition-all duration-700",
      phase === "healed"
        ? "border-amber-500/35 shadow-[0_0_30px_rgba(245,158,11,0.15)]"
        : current >= 300
          ? "border-rose-500/35 shadow-[0_0_30px_rgba(244,63,94,0.15)]"
          : "border-border/50"
    )}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-primary-foreground font-black tracking-wider text-sm">
            Real-Time Checkout Latency Monitor
          </CardTitle>
          <div className="flex items-center gap-2">
            <span className={cn(
              "text-[9px] font-black tracking-widest border rounded-full px-2 py-0.5 uppercase animate-pulse",
              phase === "healed"
                ? "bg-amber-500/15 border-amber-500/40 text-amber-400"
                : current >= 300
                  ? "bg-rose-500/15 border-rose-500/40 text-rose-400"
                  : current >= 150
                    ? "bg-amber-500/15 border-amber-500/40 text-amber-400"
                    : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
            )}>
              {phase === "healed" ? "🟡 SELF-HEALED" : label.text}
            </span>
            <span className={cn("text-xl font-black", label.cls)}>
              {current}ms
            </span>
          </div>
        </div>
        <p className="text-[9px] text-muted-foreground/50 font-bold tracking-widest uppercase">
          Nominal threshold: 50ms · Anomaly threshold: 300ms
        </p>
      </CardHeader>

      <CardContent>
        {/* Latency Bar Chart */}
        <div className="relative">
          {/* Threshold lines */}
          <div className="absolute inset-x-0 bottom-0 h-48 pointer-events-none">
            {/* 300ms critical line */}
            <div className="absolute w-full border-t border-dashed border-rose-500/30"
              style={{ bottom: `${(300 / max) * 100}%` }}>
              <span className="absolute right-0 -top-3.5 text-[8px] text-rose-400/60 font-black">300ms CRITICAL</span>
            </div>
            {/* 50ms nominal line */}
            <div className="absolute w-full border-t border-dashed border-emerald-500/20"
              style={{ bottom: `${(50 / max) * 100}%` }}>
              <span className="absolute right-0 -top-3.5 text-[8px] text-emerald-400/50 font-black">50ms NOMINAL</span>
            </div>
          </div>

          {/* Bars */}
          <div className="flex items-end gap-1 h-48 px-1 border-b border-border/20 pb-1 relative z-10">
            {window.map((val, i) => (
              <div
                key={i}
                className={cn(
                  "flex-1 rounded-t bg-gradient-to-t border-x border-t transition-all duration-400",
                  latencyColor(val)
                )}
                style={{ height: `${(val / max) * 100}%` }}
              />
            ))}
          </div>
        </div>

        {/* Timeline labels */}
        <div className="flex justify-between mt-2 text-[9px] font-bold tracking-widest text-primary-foreground/40 uppercase">
          <span>-{WINDOW * 0.42}s</span>
          <span className={cn("font-black", label.cls)}>
            {phase === "healed" ? "🟡 PLAYBOOK EXECUTED · RECOVERED" : current >= 300 ? "🔴 ANOMALY PEAK" : "NOW"}
          </span>
          <span>NOW</span>
        </div>

        {/* Metrics row */}
        <div className="mt-3 grid grid-cols-3 gap-2">
          {[
            {
              label: "Current",
              value: `${current}ms`,
              cls: phase === "healed" ? "text-amber-400" : current >= 300 ? "text-rose-400" : "text-emerald-400"
            },
            {
              label: "Peak",
              value: "425ms",
              cls: "text-rose-400"
            },
            {
              label: "Loss",
              value: phase === "healed" ? "$0" : "$24,580",
              cls: phase === "healed" ? "text-emerald-400" : "text-rose-400"
            },
          ].map((stat) => (
            <div key={stat.label} className="flex flex-col items-center rounded-lg border border-border/15 bg-background/20 py-1.5 px-2">
              <span className="text-[8px] font-black tracking-widest text-muted-foreground/50 uppercase">{stat.label}</span>
              <span className={cn("text-sm font-black", stat.cls)}>{stat.value}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
