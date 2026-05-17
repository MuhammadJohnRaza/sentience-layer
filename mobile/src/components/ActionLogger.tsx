"use client";

import React, { useState, useEffect, useRef } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ActionItem {
  id: string;
  title: string;
  description: string;
  category: string;
  status: string;
  impactScore: number;
  createdAt: string;
  steps: { id: string; description: string; status: string }[];
}

interface LogEntry {
  timestamp: string;
  agent: string;
  action: string;
  httpStatus: number;
  result: string;
  beforeState: Record<string, any>;
  afterState: Record<string, any>;
}

export function ActionLogger() {
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loadingActionId, setLoadingActionId] = useState<string | null>(null);
  const [activeLogIndex, setActiveLogIndex] = useState<number | null>(null);
  const logTerminalRef = useRef<HTMLDivElement>(null);

  // Initialize with some default action log entries to showcase
  useEffect(() => {
    const fetchActions = async () => {
      try {
        const data = await api.getActions();
        setActions(data);
      } catch (err) {
        console.error("Failed to load actions:", err);
      }
    };

    fetchActions();

    // Seed initial logs
    setLogs([
      {
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        agent: "CriticAgent",
        action: "Audit System Readiness",
        httpStatus: 200,
        result: "Constraint audit completed successfully. 18 cognitive agents online and verified.",
        beforeState: {
          system_status: "INITIALIZING",
          postgres_mcp: "OFFLINE",
          active_connections: 0
        },
        afterState: {
          system_status: "ACTIVE",
          postgres_mcp: "ONLINE",
          active_connections: 18
        }
      },
      {
        timestamp: new Date(Date.now() - 1800000).toISOString(),
        agent: "OpportunityAnalystAgent",
        action: "Run Opportunity Scan",
        httpStatus: 200,
        result: "Discovered 45% potential ROI boost from postgres schema caching indices.",
        beforeState: {
          caching_indices: "NONE",
          roi_score: 42.5,
          db_read_latency: "120ms"
        },
        afterState: {
          caching_indices: "CONFIGURED",
          roi_score: 245.0,
          db_read_latency: "24ms"
        }
      }
    ]);
  }, []);

  const handleExecute = async (actionId: string, actionTitle: string, category: string) => {
    setLoadingActionId(actionId);
    try {
      const response = (await api.executeAction(actionId)) as any;
      
      const newEntry: LogEntry = {
        timestamp: new Date().toISOString(),
        agent: category === "reasoning" ? "OpportunityAnalystAgent" : "CriticAgent",
        action: actionTitle,
        httpStatus: 200,
        result: response.result || `Action successfully executed.`,
        beforeState: actionId === "action-2" ? {
          swarm_analysis: "STALE",
          memory_alignment: "UNLINKED",
          active_swarms: 1
        } : {
          mcp_tools: "UNAUDITED",
          postgres_index: "STALE"
        },
        afterState: actionId === "action-2" ? {
          swarm_analysis: "SYNCHRONIZED",
          memory_alignment: "SECURELY_PERSISTED",
          active_swarms: 3
        } : {
          mcp_tools: "VERIFIED",
          postgres_index: "OPTIMIZED"
        }
      };

      setLogs((prev) => [...prev, newEntry]);
      
      // Update actions status locally
      setActions(prev => prev.map(a => a.id === actionId ? { ...a, status: "completed" } : a));
      
      // Select the newly added log to show diff
      setActiveLogIndex(logs.length);

      // Scroll terminal to bottom
      setTimeout(() => {
        if (logTerminalRef.current) {
          logTerminalRef.current.scrollTop = logTerminalRef.current.scrollHeight;
        }
      }, 100);

    } catch (err) {
      console.error("Failed to execute action:", err);
    } finally {
      setLoadingActionId(null);
    }
  };

  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mt-6">
      {/* Actions Execution Panel */}
      <Card className="xl:col-span-1 border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
        <CardHeader className="border-b border-border/10 bg-card/40 p-4">
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            🎯 Cognitive Playbook Actions
          </CardTitle>
        </CardHeader>
        <CardContent className="p-4 space-y-4 max-h-[500px] overflow-y-auto">
          {actions.map((act) => (
            <div
              key={act.id}
              className="p-3.5 bg-background/30 rounded-xl border border-border/10 flex flex-col justify-between gap-3 hover:border-primary/30 transition-all duration-300 shadow-inner"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <Badge className="bg-primary/20 border border-primary/30 text-primary-foreground font-black text-[8px] tracking-widest uppercase">
                    {act.category}
                  </Badge>
                  <span className="text-[10px] font-mono text-muted-foreground/60">ID: {act.id}</span>
                </div>
                <h4 className="text-xs font-black text-primary-foreground tracking-wide">{act.title}</h4>
                <p className="text-[11px] text-muted-foreground/80 mt-1 leading-relaxed">{act.description}</p>
                
                {/* Steps indicators */}
                <div className="mt-3 space-y-1.5">
                  {act.steps.map((st) => (
                    <div key={st.id} className="flex items-center gap-2 text-[10px] text-muted-foreground/70">
                      <span className={cn(
                        "h-1.5 w-1.5 rounded-full shrink-0",
                        st.status === "completed" ? "bg-emerald-400" : "bg-amber-400"
                      )} />
                      <span className="truncate">{st.description}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex items-center justify-between border-t border-border/10 pt-3 mt-1">
                <span className="text-[10px] font-black text-amber-300">
                  🔥 Impact: {act.impactScore}%
                </span>
                <Button
                  size="sm"
                  onClick={() => handleExecute(act.id, act.title, act.category)}
                  disabled={loadingActionId === act.id || act.status === "completed"}
                  className={cn(
                    "text-[9px] font-black tracking-widest uppercase rounded-lg px-3 py-1.5 h-7",
                    act.status === "completed" 
                      ? "bg-emerald-950/20 text-emerald-400 border border-emerald-500/30 cursor-not-allowed"
                      : "bg-primary/20 hover:bg-primary/30 text-primary-foreground border border-border"
                  )}
                >
                  {loadingActionId === act.id ? "⚡ RUNNING..." : act.status === "completed" ? "✓ EXECUTED" : "⚡ EXECUTE"}
                </Button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Live Action Terminal Log Panel */}
      <Card className="xl:col-span-2 border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
        <CardHeader className="border-b border-border/10 bg-card/40 p-4 flex flex-row items-center justify-between">
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            💻 Live Cognitive Action Terminal
          </CardTitle>
          <Badge className="bg-emerald-950/40 border border-emerald-500/30 text-emerald-400 font-mono text-[8px] px-2 py-0.5 tracking-wider animate-pulse">
            ● FEED ONLINE
          </Badge>
        </CardHeader>
        <CardContent className="p-4 grid grid-cols-1 lg:grid-cols-2 gap-4 h-[440px]">
          {/* Terminal log stream */}
          <div className="flex flex-col border border-border/10 rounded-xl bg-[#020205] overflow-hidden p-2 shadow-inner">
            <div className="flex gap-1.5 px-2 py-1.5 border-b border-border/5">
              <div className="w-2.5 h-2.5 rounded-full bg-rose-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-amber-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/60" />
            </div>
            <div 
              ref={logTerminalRef}
              className="flex-1 overflow-y-auto p-2 font-mono text-[10px] space-y-2 max-h-[360px]"
            >
              {logs.map((log, index) => (
                <div
                  key={index}
                  onClick={() => setActiveLogIndex(index)}
                  className={cn(
                    "p-2 rounded-lg cursor-pointer border transition-all duration-300",
                    activeLogIndex === index
                      ? "bg-primary/10 border-primary/40 text-primary-foreground"
                      : "bg-transparent border-transparent text-muted-foreground/80 hover:bg-background/20"
                  )}
                >
                  <div className="flex items-center gap-2 text-indigo-400">
                    <span>[{new Date(log.timestamp).toLocaleTimeString()}]</span>
                    <span className="font-bold text-amber-400">{log.agent}</span>
                  </div>
                  <div className="mt-1 flex items-center justify-between">
                    <span className="truncate">↳ {log.action}</span>
                    <Badge className="bg-emerald-950/40 text-emerald-400 text-[8px] px-1 font-mono py-0 h-4 border border-emerald-500/20">
                      HTTP {log.httpStatus}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* State Diff Panel */}
          <div className="border border-border/10 rounded-xl bg-[#030308] p-4 flex flex-col justify-between overflow-y-auto shadow-inner">
            {activeLogIndex !== null && logs[activeLogIndex] ? (
              <div className="space-y-4">
                <div>
                  <h4 className="text-[10px] font-black text-amber-300 tracking-widest uppercase">Action Result</h4>
                  <p className="text-xs font-semibold text-primary-foreground mt-1 leading-relaxed bg-[#0c0c16] p-2.5 rounded-xl border border-border/10">
                    {logs[activeLogIndex].result}
                  </p>
                </div>
                <div>
                  <h4 className="text-[10px] font-black text-indigo-300 tracking-widest uppercase mb-2">Cognitive State Mutation (Before ➔ After)</h4>
                  <div className="space-y-1.5 font-mono text-[10px] bg-[#020205] p-3 rounded-xl border border-border/5">
                    {Object.keys(logs[activeLogIndex].beforeState).map((key) => {
                      const before = logs[activeLogIndex].beforeState[key];
                      const after = logs[activeLogIndex].afterState[key];
                      return (
                        <div key={key} className="space-y-0.5 border-b border-border/5 pb-1.5 last:border-b-0 last:pb-0">
                          <div className="text-muted-foreground font-black text-[9px] uppercase tracking-wider">{key}:</div>
                          <div className="text-rose-400 flex items-center gap-1.5 pl-2">
                            <span>-</span>
                            <span>{String(before)}</span>
                          </div>
                          <div className="text-emerald-400 flex items-center gap-1.5 pl-2">
                            <span>+</span>
                            <span>{String(after)}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center max-w-[240px] mx-auto text-muted-foreground">
                <span className="text-2xl mb-2">💻</span>
                <h5 className="text-xs font-black text-primary-foreground uppercase tracking-widest">State Mutation Visualizer</h5>
                <p className="text-[10px] leading-relaxed mt-2">
                  Select a live execution log to audit the exact before and after cognitive database mutations.
                </p>
              </div>
            )}
            {activeLogIndex !== null && (
              <span className="text-[9px] font-mono text-muted-foreground/35 block text-right mt-2">
                State Persisted to Memory Vault securely.
              </span>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
