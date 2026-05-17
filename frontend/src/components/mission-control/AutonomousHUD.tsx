"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface HUDLog {
  timestamp: string;
  agent: string;
  action: string;
  status: "success" | "warning" | "error" | "info";
  message: string;
}

export function AutonomousHUD() {
  const [isAutoPilot, setIsAutoPilot] = useState(true);
  const [systemState, setSystemState] = useState<"optimal" | "quarantining" | "healing" | "syncing">("optimal");
  const [logs, setLogs] = useState<HUDLog[]>([]);
  const [telemetry, setTelemetry] = useState({
    alignment: 98.4,
    nodeLatency: "14ms",
    economicROI: "+245.0%",
    threatLevel: "0.0%"
  });

  // Populate initial logs
  useEffect(() => {
    setLogs([
      {
        timestamp: new Date(Date.now() - 5000).toLocaleTimeString(),
        agent: "CriticAgent",
        action: "TELEMETRY_AUDIT",
        status: "success",
        message: "No anomalies detected in postgres_list_tables tool register. System nominal."
      },
      {
        timestamp: new Date(Date.now() - 2000).toLocaleTimeString(),
        agent: "ConsensusAgent",
        action: "SWARM_SYNCHRONIZATION",
        status: "success",
        message: "Synchronized state boundaries across all 18 cognitive agents successfully."
      }
    ]);
  }, []);

  // Run autonomous loop if auto-pilot is active
  useEffect(() => {
    if (!isAutoPilot) return;

    const interval = setInterval(() => {
      // Small metric fluctuations
      setTelemetry(prev => {
        if (systemState !== "optimal") return prev;
        const alignDelta = (Math.random() - 0.5) * 0.4;
        const latency = Math.floor(Math.random() * 4) + 12;
        return {
          ...prev,
          alignment: Math.max(90, Math.min(100, Number((prev.alignment + alignDelta).toFixed(2)))),
          nodeLatency: `${latency}ms`
        };
      });

      // Periodic audit logs
      if (Math.random() > 0.7 && systemState === "optimal") {
        const events = [
          { agent: "OpportunityAnalystAgent", action: "ROI_AUDIT", msg: "Discovered optimized index cache path. Gained 12ms latency improvement.", status: "success" as const },
          { agent: "CriticAgent", action: "CONSTRAINT_CHECK", msg: "Stress-tested memory query latency boundaries. 100% compliant.", status: "success" as const },
          { agent: "ConsensusAgent", action: "ALIGNMENT_BROADCAST", msg: "State vectors successfully broadcast to offline dream consolidator.", status: "info" as const }
        ];
        const event = events[Math.floor(Math.random() * events.length)];
        
        setLogs(prev => [
          {
            timestamp: new Date().toLocaleTimeString(),
            agent: event.agent,
            action: event.action,
            status: event.status,
            message: event.msg
          },
          ...prev.slice(0, 4)
        ]);
      }

    }, 3500);

    return () => clearInterval(interval);
  }, [isAutoPilot, systemState]);

  const handleInjectAnomaly = () => {
    if (systemState !== "optimal") return;

    setSystemState("quarantining");
    setTelemetry(prev => ({ ...prev, alignment: 74.2, threatLevel: "92.6%" }));
    
    // Inject emergency logs
    setLogs(prev => [
      {
        timestamp: new Date().toLocaleTimeString(),
        agent: "AdversarialTestAgent",
        action: "ANOMALY_DETECTION",
        status: "error",
        message: "CRITICAL DRIFT: SQLite memory boundary violation detected inside Vault container!"
      },
      ...prev
    ]);

    // Transition to self-healing after 3 seconds
    setTimeout(() => {
      setSystemState("healing");
      setLogs(prev => [
        {
          timestamp: new Date().toLocaleTimeString(),
          agent: "CriticAgent",
          action: "EMERGENCY_QUARANTINE",
          status: "warning",
          message: "Doubt Room isolation activated. Isolating container trace 'vault_sqlite_corrupt'..."
        },
        {
          timestamp: new Date().toLocaleTimeString(),
          agent: "ConsensusAgent",
          action: "AUTONOMOUS_HEAL",
          status: "info",
          message: "Consensus node approved automated database state rollbacks. Initiating snapshot restoration..."
        },
        ...prev
      ]);
    }, 2800);

    // Back to optimal after 6 seconds
    setTimeout(() => {
      setSystemState("optimal");
      setTelemetry(prev => ({ ...prev, alignment: 99.1, threatLevel: "0.0%" }));
      setLogs(prev => [
        {
          timestamp: new Date().toLocaleTimeString(),
          agent: "ConsensusAgent",
          action: "RESTORATION_COMPLETE",
          status: "success",
          message: "System self-healed successfully in 34ms. Snapshot restored. SQLite containment active."
        },
        ...prev
      ]);
    }, 6000);
  };

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            🛸 Autonomous Auto-Pilot Central Command
          </CardTitle>
          <p className="text-[10px] text-muted-foreground/80 uppercase tracking-wider mt-1">
            Bleeding-edge autonomous cognitive orchestration, threat monitoring, and self-healing telemetry
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Button
            size="sm"
            onClick={() => setIsAutoPilot(!isAutoPilot)}
            className={cn(
              "text-[9px] font-black tracking-widest uppercase rounded-lg px-3 py-1.5 h-8 border transition-all duration-300",
              isAutoPilot
                ? "bg-emerald-950/20 text-emerald-400 border-emerald-500/30 hover:bg-emerald-950/30"
                : "bg-transparent text-muted-foreground border-border hover:border-primary/20"
            )}
          >
            {isAutoPilot ? "● AUTO-PILOT ON" : "○ MANUAL MODE"}
          </Button>
          <Button
            size="sm"
            onClick={handleInjectAnomaly}
            disabled={systemState !== "optimal" || !isAutoPilot}
            className="text-[9px] font-black tracking-widest uppercase rounded-lg px-3.5 py-1.5 h-8 bg-rose-600 hover:bg-rose-700 text-white shadow-[0_0_15px_rgba(244,63,94,0.4)] disabled:opacity-45"
          >
            ⚡ INJECT ANOMALY
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-4 grid grid-cols-1 xl:grid-cols-4 gap-6">
        
        {/* Dynamic Circular Gauges & Gauges */}
        <div className="xl:col-span-1 grid grid-cols-2 gap-4">
          
          {/* Alignment */}
          <div className="p-3 bg-[#030206] rounded-xl border border-border/10 flex flex-col justify-between shadow-inner">
            <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-wider">SWARM ALIGNMENT</span>
            <div className="my-2 flex items-baseline gap-1">
              <span className={cn(
                "text-2xl font-black transition-colors duration-300",
                systemState === "quarantining" ? "text-rose-400" : "text-primary-foreground"
              )}>
                {telemetry.alignment}%
              </span>
            </div>
            <div className="h-1 bg-border/20 rounded-full overflow-hidden">
              <div 
                className={cn(
                  "h-full transition-all duration-500",
                  systemState === "quarantining" ? "bg-rose-500" : "bg-violet-500"
                )} 
                style={{ width: `${telemetry.alignment}%` }}
              />
            </div>
          </div>

          {/* Node Latency */}
          <div className="p-3 bg-[#030206] rounded-xl border border-border/10 flex flex-col justify-between shadow-inner">
            <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-wider">NODE LATENCY</span>
            <div className="my-2 flex items-baseline gap-1">
              <span className="text-2xl font-black text-amber-300">
                {telemetry.nodeLatency}
              </span>
            </div>
            <span className="text-[8px] font-mono text-muted-foreground/45 uppercase tracking-wider">Nominal limits &lt; 20ms</span>
          </div>

          {/* Economic ROI */}
          <div className="p-3 bg-[#030206] rounded-xl border border-border/10 flex flex-col justify-between shadow-inner">
            <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-wider">ECONOMIC ROI BOUNDS</span>
            <div className="my-2 flex items-baseline gap-1">
              <span className="text-2xl font-black text-emerald-400">
                {telemetry.economicROI}
              </span>
            </div>
            <span className="text-[8px] font-mono text-muted-foreground/45 uppercase tracking-wider">Value Hedging Active</span>
          </div>

          {/* Threat containment */}
          <div className="p-3 bg-[#030206] rounded-xl border border-border/10 flex flex-col justify-between shadow-inner">
            <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-wider">THREAT LEVEL</span>
            <div className="my-2 flex items-baseline gap-1">
              <span className={cn(
                "text-2xl font-black transition-colors duration-300",
                systemState === "optimal" ? "text-muted-foreground/40" : "text-rose-500 animate-pulse"
              )}>
                {telemetry.threatLevel}
              </span>
            </div>
            <Badge className={cn(
              "text-[7px] font-black tracking-widest uppercase h-4 px-1 justify-center border",
              systemState === "optimal" 
                ? "bg-emerald-950/20 border-emerald-500/20 text-emerald-400" 
                : systemState === "quarantining"
                  ? "bg-rose-950/40 border-rose-500/30 text-rose-400"
                  : "bg-amber-950/40 border-amber-500/30 text-amber-400"
            )}>
              {systemState.toUpperCase()}
            </Badge>
          </div>

        </div>

        {/* Live Swarm Console Stream */}
        <div className="xl:col-span-3 border border-border/10 rounded-xl bg-[#020204] overflow-hidden flex flex-col shadow-inner">
          <div className="flex gap-1.5 px-3 py-2 border-b border-border/5 bg-card/20 justify-between items-center">
            <div className="flex gap-1.5">
              <div className="w-2 h-2 rounded-full bg-rose-500/40" />
              <div className="w-2 h-2 rounded-full bg-amber-500/40" />
              <div className="w-2 h-2 rounded-full bg-emerald-500/40" />
            </div>
            <Badge className="bg-[#0b0c16] border border-border/20 text-[8px] font-mono text-muted-foreground/60">
              ● COGNITIVE SHELL ONLINE
            </Badge>
          </div>
          <div className="p-3 font-mono text-[10px] space-y-2 max-h-[140px] overflow-y-auto">
            {logs.map((log, index) => (
              <div 
                key={index} 
                className={cn(
                  "p-2 rounded-lg border leading-relaxed flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 transition-all duration-300",
                  log.status === "error"
                    ? "bg-rose-950/20 border-rose-500/25 text-rose-300"
                    : log.status === "warning"
                      ? "bg-amber-950/20 border-amber-500/25 text-amber-300"
                      : log.status === "info"
                        ? "bg-indigo-950/20 border-indigo-500/25 text-indigo-300"
                        : "bg-background/40 border-border/5 text-primary-foreground/90"
                )}
              >
                <div>
                  <span className="text-muted-foreground/50 mr-2">[{log.timestamp}]</span>
                  <span className="font-black text-violet-400 mr-2">{log.agent}</span>
                  <span className="font-semibold">{log.message}</span>
                </div>
                <Badge className={cn(
                  "text-[7px] font-black tracking-widest uppercase h-4.5 py-0 px-1 border shrink-0 w-fit self-end sm:self-auto",
                  log.status === "error"
                    ? "bg-rose-950 border-rose-500 text-rose-400"
                    : log.status === "warning"
                      ? "bg-amber-950 border-amber-500 text-amber-400"
                      : log.status === "info"
                        ? "bg-indigo-950 border-indigo-500 text-indigo-400"
                        : "bg-emerald-950 border-emerald-500 text-emerald-400"
                )}>
                  {log.action}
                </Badge>
              </div>
            ))}
          </div>
        </div>

      </CardContent>
    </Card>
  );
}
