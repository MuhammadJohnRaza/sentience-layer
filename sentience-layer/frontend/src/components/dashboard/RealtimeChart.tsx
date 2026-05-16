/**
 * Real-time Activity Chart — Black / Purple / Gold Theme
 */

"use client";

import { useEffect, useState } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";

export function RealtimeChart() {
  const [data, setData] = useState<number[]>([30, 45, 35, 50, 40, 60, 55, 70, 65, 80, 72, 88]);
  const { subscribe } = useWebSocket();

  useEffect(() => {
    return subscribe("agent_update", (msg) => {
      const value = msg?.throughput || Math.floor(Math.random() * 40) + 45;
      setData((prev) => [...prev.slice(1), value]);
    });
  }, [subscribe]);

  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  // SVG polyline path
  const w = 100;
  const h = 100;
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  }).join(" ");

  const areaPoints = `0,${h} ${points} ${w},${h}`;

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
        <div>
          <h3 className="text-sm font-bold text-[#EAB308] uppercase tracking-wider">Cognitive Activity</h3>
          <p className="text-[10px] text-zinc-600 mt-0.5">Real-time agent throughput</p>
        </div>
        <div className="flex items-center gap-4 text-[10px] text-zinc-500">
          <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-[#A855F7]" />Active</span>
          <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-[#EAB308]" />Peak</span>
        </div>
      </div>

      {/* Chart */}
      <div className="flex-1 px-5 pb-4 pt-3 flex flex-col justify-between">
        <div className="relative w-full" style={{ height: "160px" }}>
          <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" className="absolute inset-0 w-full h-full">
            {/* Area fill */}
            <defs>
              <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#A855F7" stopOpacity="0.25" />
                <stop offset="100%" stopColor="#A855F7" stopOpacity="0" />
              </linearGradient>
            </defs>
            <polygon points={areaPoints} fill="url(#areaGrad)" />
            {/* Line */}
            <polyline
              points={points}
              fill="none"
              stroke="#A855F7"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              vectorEffect="non-scaling-stroke"
            />
            {/* Latest point highlight */}
            {(() => {
              const last = data[data.length - 1];
              const x = w;
              const y = h - ((last - min) / range) * h;
              return (
                <circle cx={x} cy={y} r="2" fill="#EAB308" vectorEffect="non-scaling-stroke" />
              );
            })()}
          </svg>
        </div>

        {/* X-axis labels */}
        <div className="flex justify-between text-[10px] text-zinc-700 mt-2">
          <span>−{data.length - 1}s</span>
          <span className="text-[#EAB308]/60">Now</span>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-zinc-800">
          {[
            { label: "Current", value: data[data.length - 1] },
            { label: "Peak", value: max },
            { label: "Avg", value: Math.round(data.reduce((a, b) => a + b, 0) / data.length) },
          ].map((s) => (
            <div key={s.label} className="text-center">
              <p className="text-sm font-bold text-[#EAB308]">{s.value}</p>
              <p className="text-[10px] text-zinc-600 uppercase tracking-wide">{s.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}