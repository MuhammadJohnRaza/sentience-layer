/** * System Architecture Map */ "use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { AGENT_TYPES } from "@/lib/constants";
export function SystemMap() {
  return (
    <Card className="h-96">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>System Architecture</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="relative h-full">
        {" "}
        <div className="absolute inset-0 flex items-center justify-center">
          {" "}
          <div className="relative">
            {" "}
            {/* Central Antigravity Hub */}
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-20 w-20 rounded-full bg-card dark:bg-background flex items-center justify-center z-10">
              {" "}
              <span className="text-xs font-bold text-white dark:text-foreground text-center">
                Anti
                <br />
                gravity
              </span>{" "}
            </div>{" "}
            {/* Orbiting Agents */}
            {AGENT_TYPES.slice(0, 8).map((agent, i) => {
              const angle = (i / 8) * 2 * Math.PI;
              const radius = 140;
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              return (
                <div
                  key={agent.id}
                  className="absolute h-12 w-12 rounded-full flex items-center justify-center text-[10px] font-medium text-white shadow-lg"
                  style={{
                    backgroundColor: agent.color,
                    left: `calc(50% + ${x}px - 24px)`,
                    top: `calc(50% + ${y}px - 24px)`,
                  }}
                >
                  {" "}
                  {agent.name.slice(0, 3)}
                </div>
              );
            })}
            {/* Connection lines (simplified) */}
            <svg className="absolute inset-0 h-full w-full pointer-events-none opacity-20">
              {" "}
              <circle
                cx="50%"
                cy="50%"
                r="140"
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
                strokeDasharray="4 4"
              />{" "}
            </svg>{" "}
          </div>{" "}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
