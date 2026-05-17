"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface DebateTopic {
  id: string;
  topic: string;
  forPct: number;
  againstPct: number;
  criticAgentArgs: string[];
  consensusAgentArgs: string[];
}

const DEBATES: DebateTopic[] = [
  {
    id: "debate-1",
    topic: "Should we auto-execute high-confidence actions without human sign-off?",
    forPct: 58,
    againstPct: 42,
    criticAgentArgs: [
      "Auto-execution poses extreme risk if SQLite containment fails during live Postgres migrations.",
      "A rogue MCP mutation could overwrite active vector tables without rollback triggers."
    ],
    consensusAgentArgs: [
      "We mandate a 94% confidence threshold and sandboxed Monte Carlo tests before deployment.",
      "Containment protocols are already active and simulated with zero leakage detected."
    ]
  },
  {
    id: "debate-2",
    topic: "Is the postgres_list_tables tool relationship strong enough to justify full trust?",
    forPct: 82,
    againstPct: 18,
    criticAgentArgs: [
      "External database connections are highly sensitive to network latency drops.",
      "Adversarial schema injections could bypass the ReAct parser under heavy parallel loads."
    ],
    consensusAgentArgs: [
      "Caching queries through local memory maps prevents index failures entirely.",
      "All query inputs are audited by the security wrapper before parsing."
    ]
  }
];

export function DoubtTheater() {
  const [activeDebates, setActiveDebates] = useState<DebateTopic[]>(DEBATES);
  const [argumentLog, setArgumentLog] = useState<{ agent: string; msg: string; type: "pro" | "con" }[]>([]);
  const [selectedDebateId, setSelectedDebateId] = useState<string>("debate-1");

  // Stream debates updates and add random argument exchanges
  useEffect(() => {
    // Seed initial argument logs
    const active = DEBATES.find(d => d.id === selectedDebateId) || DEBATES[0];
    setArgumentLog([
      { agent: "CriticAgent", msg: active.criticAgentArgs[0], type: "con" },
      { agent: "ConsensusAgent", msg: active.consensusAgentArgs[0], type: "pro" }
    ]);

    const interval = setInterval(() => {
      // Randomly fluctuation percentages
      setActiveDebates(prev => prev.map(d => {
        const delta = Math.floor(Math.random() * 5) - 2;
        const newFor = Math.max(10, Math.min(90, d.forPct + delta));
        return {
          ...d,
          forPct: newFor,
          againstPct: 100 - newFor
        };
      }));

      // Add a random argument exchange sometimes
      if (Math.random() > 0.4) {
        const currentDebate = DEBATES.find(d => d.id === selectedDebateId) || DEBATES[0];
        const isPro = Math.random() > 0.5;
        const pool = isPro ? currentDebate.consensusAgentArgs : currentDebate.criticAgentArgs;
        const randArg = pool[Math.floor(Math.random() * pool.length)];
        
        setArgumentLog(prev => {
          const next = [...prev, {
            agent: isPro ? "ConsensusAgent" : "CriticAgent",
            msg: randArg,
            type: isPro ? ("pro" as const) : ("con" as const)
          }];
          return next.slice(-4); // keep latest 4 arguments
        });
      }

    }, 3000);

    return () => clearInterval(interval);
  }, [selectedDebateId]);

  const activeDebate = activeDebates.find(d => d.id === selectedDebateId) || activeDebates[0];

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4">
        <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center justify-between">
          <span>⚖️ Live Swarm Audit & Doubt Theater</span>
          <Badge className="bg-destructive/20 border border-destructive/30 text-rose-400 font-mono text-[8px] animate-pulse">
            ● CONTROVERSY HIGH
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4 space-y-4">
        {/* Debate selector */}
        <div className="grid grid-cols-2 gap-2">
          {activeDebates.map(d => (
            <button
              key={d.id}
              onClick={() => setSelectedDebateId(d.id)}
              className={cn(
                "p-2.5 rounded-xl border text-left transition-all duration-300",
                selectedDebateId === d.id
                  ? "bg-primary/10 border-primary/40 text-primary-foreground"
                  : "bg-[#050408]/30 border-border/5 text-muted-foreground hover:border-border/20"
              )}
            >
              <h5 className="text-[10px] font-black uppercase tracking-wider text-muted-foreground mb-1">Debate Topic</h5>
              <p className="text-[11px] font-bold line-clamp-1 leading-relaxed">{d.topic}</p>
            </button>
          ))}
        </div>

        {/* Selected Debate Card */}
        <div className="p-4 bg-[#030206] rounded-xl border border-border/10 space-y-4 shadow-inner">
          <h4 className="text-xs font-black text-primary-foreground tracking-wide leading-relaxed">
            {activeDebate.topic}
          </h4>

          {/* Voting Bars */}
          <div className="space-y-3 pt-2">
            {/* For (Consensus) */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[10px] font-black uppercase">
                <span className="text-emerald-400">✓ CONSENSUS ALIGNMENT</span>
                <span className="text-emerald-400">{activeDebate.forPct}%</span>
              </div>
              <div className="h-2.5 bg-emerald-950/20 border border-emerald-500/20 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500 shadow-[0_0_12px_rgba(16,185,129,0.5)]" 
                  style={{ width: `${activeDebate.forPct}%` }}
                />
              </div>
            </div>

            {/* Against (Critic / Doubt) */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[10px] font-black uppercase">
                <span className="text-rose-400">⚠ CRITICAL DISSENT (DOUBT)</span>
                <span className="text-rose-400">{activeDebate.againstPct}%</span>
              </div>
              <div className="h-2.5 bg-rose-950/20 border border-rose-500/20 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-rose-500 to-red-400 transition-all duration-500 shadow-[0_0_12px_rgba(244,63,94,0.5)]" 
                  style={{ width: `${activeDebate.againstPct}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Live debate stream */}
        <div className="space-y-2">
          <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-widest block">Live Swarm Argument Stream</span>
          <div className="space-y-2 max-h-[160px] overflow-y-auto bg-[#020204] p-3 rounded-xl border border-border/5">
            {argumentLog.map((log, index) => (
              <div 
                key={index} 
                className={cn(
                  "p-2 rounded-lg border text-[10px] leading-relaxed transition-all duration-300",
                  log.type === "pro" 
                    ? "bg-emerald-950/10 border-emerald-500/10 text-emerald-300/90 pl-3" 
                    : "bg-rose-950/10 border-rose-500/10 text-rose-300/90 pl-3"
                )}
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span className={cn("h-1.5 w-1.5 rounded-full", log.type === "pro" ? "bg-emerald-400" : "bg-rose-400")} />
                  <span className="font-black uppercase tracking-wider text-[9px]">
                    {log.agent}
                  </span>
                </div>
                <p className="font-semibold">{log.msg}</p>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
