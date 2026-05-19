"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface DebateTopic {
  id: string;
  topic: string;
  forPct: number;
  againstPct: number;
  criticAgentArgs: string[];
  consensusAgentArgs: string[];
}

interface DoubtTheaterProps {
  onDebateChanged?: (debate: DebateTopic) => void;
}

export function DoubtTheater({ onDebateChanged }: DoubtTheaterProps) {
  const [activeDebates, setActiveDebates] = useState<DebateTopic[]>([]);
  const [selectedDebateId, setSelectedDebateId] = useState<string>("");
  const [argumentLog, setArgumentLog] = useState<{ agent: string; msg: string; type: "pro" | "con" }[]>([]);
  
  // Custom doubt submission
  const [newTopic, setNewTopic] = useState("");
  const [isSimulating, setIsSimulating] = useState(false);

  // Load debates from API on mount
  const loadDebates = async (selectFirst = true) => {
    try {
      const data = await api.getDebates();
      setActiveDebates(data);
      if (data.length > 0 && selectFirst) {
        setSelectedDebateId(data[0].id);
        updateArgumentLog(data[0]);
        if (onDebateChanged) {
          onDebateChanged(data[0]);
        }
      }
    } catch (err) {
      console.error("Failed to load debates list:", err);
    }
  };

  useEffect(() => {
    loadDebates(true);
  }, []);

  const updateArgumentLog = (debate: DebateTopic) => {
    const log: { agent: string; msg: string; type: "pro" | "con" }[] = [];
    if (debate.criticAgentArgs && debate.criticAgentArgs[0]) {
      log.push({ agent: "CriticAgent", msg: debate.criticAgentArgs[0], type: "con" });
    }
    if (debate.consensusAgentArgs && debate.consensusAgentArgs[0]) {
      log.push({ agent: "ConsensusAgent", msg: debate.consensusAgentArgs[0], type: "pro" });
    }
    setArgumentLog(log);
  };

  // Fluctuating percentage simulation & occasional argument exchange
  useEffect(() => {
    if (!selectedDebateId || activeDebates.length === 0) return;

    const interval = setInterval(() => {
      // Small fluctuation to show active reasoning
      setActiveDebates((prev) =>
        prev.map((d) => {
          if (d.id !== selectedDebateId) return d;
          const delta = Math.floor(Math.random() * 3) - 1;
          const newFor = Math.max(15, Math.min(85, d.forPct + delta));
          return {
            ...d,
            forPct: newFor,
            againstPct: 100 - newFor,
          };
        })
      );

      // Add a random argument sometimes
      if (Math.random() > 0.45) {
        const currentDebate = activeDebates.find((d) => d.id === selectedDebateId);
        if (!currentDebate) return;

        const isPro = Math.random() > 0.5;
        const pool = isPro ? currentDebate.consensusAgentArgs : currentDebate.criticAgentArgs;
        if (!pool || pool.length === 0) return;

        const randArg = pool[Math.floor(Math.random() * pool.length)];

        setArgumentLog((prev) => {
          // Avoid duplicate consecutive arguments
          if (prev.some((p) => p.msg === randArg)) return prev;
          const next = [
            ...prev,
            {
              agent: isPro ? "ConsensusAgent" : "CriticAgent",
              msg: randArg,
              type: isPro ? ("pro" as const) : ("con" as const),
            },
          ];
          return next.slice(-4); // keep latest 4
        });
      }
    }, 4000);

    return () => clearInterval(interval);
  }, [selectedDebateId, activeDebates]);

  const handleSelectDebate = (debateId: string) => {
    setSelectedDebateId(debateId);
    const debate = activeDebates.find((d) => d.id === debateId);
    if (debate) {
      updateArgumentLog(debate);
      if (onDebateChanged) {
        onDebateChanged(debate);
      }
    }
  };

  const handleSimulateDoubt = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTopic.trim() || isSimulating) return;

    setIsSimulating(true);
    try {
      const newDebate = await api.createDebate(newTopic);
      setActiveDebates((prev) => [newDebate, ...prev]);
      setSelectedDebateId(newDebate.id);
      updateArgumentLog(newDebate);
      setNewTopic("");
      if (onDebateChanged) {
        onDebateChanged(newDebate);
      }
    } catch (err) {
      console.error("Failed to simulate custom doubt:", err);
    } finally {
      setIsSimulating(false);
    }
  };

  const activeDebate = activeDebates.find((d) => d.id === selectedDebateId) || activeDebates[0];

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
        
        {/* Custom doubt submission form */}
        <form onSubmit={handleSimulateDoubt} className="flex gap-2">
          <Input
            value={newTopic}
            onChange={(e) => setNewTopic(e.target.value)}
            placeholder="Enter custom architectural or execution doubt topic..."
            disabled={isSimulating}
            className="text-xs h-9 bg-black/40 border-border/20 text-primary-foreground placeholder:text-muted-foreground/60 rounded-xl"
          />
          <Button
            type="submit"
            disabled={isSimulating || !newTopic.trim()}
            className="text-[9px] font-black tracking-widest uppercase shrink-0 h-9 rounded-xl px-4 bg-rose-950/40 hover:bg-rose-900/60 border border-rose-500/30 text-rose-300"
          >
            {isSimulating ? "SIMULATING..." : "SIMULATE DEBATE"}
          </Button>
        </form>

        {/* Debate selector sidebar-like list */}
        <div className="grid grid-cols-2 gap-2 max-h-[140px] overflow-y-auto pr-1">
          {activeDebates.map((d) => (
            <button
              key={d.id}
              onClick={() => handleSelectDebate(d.id)}
              className={cn(
                "p-2.5 rounded-xl border text-left transition-all duration-300",
                selectedDebateId === d.id
                  ? "bg-primary/10 border-primary/40 text-primary-foreground"
                  : "bg-[#050408]/30 border-border/5 text-muted-foreground hover:border-border/20"
              )}
            >
              <h5 className="text-[9px] font-black uppercase tracking-wider text-muted-foreground/60 mb-0.5">Debate Topic</h5>
              <p className="text-[10px] font-bold line-clamp-1 leading-relaxed">{d.topic}</p>
            </button>
          ))}
        </div>

        {/* Selected Debate Card */}
        {activeDebate ? (
          <div className="p-4 bg-[#030206] rounded-xl border border-border/10 space-y-4 shadow-inner">
            <h4 className="text-xs font-black text-primary-foreground tracking-wide leading-relaxed">
              {activeDebate.topic}
            </h4>

            {/* Voting Bars */}
            <div className="space-y-3 pt-2">
              {/* For (Consensus) */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-[9px] font-black uppercase">
                  <span className="text-emerald-400">✓ CONSENSUS ALIGNMENT</span>
                  <span className="text-emerald-400">{activeDebate.forPct}%</span>
                </div>
                <div className="h-2 bg-emerald-950/20 border border-emerald-500/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500 shadow-[0_0_12px_rgba(16,185,129,0.5)]"
                    style={{ width: `${activeDebate.forPct}%` }}
                  />
                </div>
              </div>

              {/* Against (Critic / Doubt) */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-[9px] font-black uppercase">
                  <span className="text-rose-400">⚠ CRITICAL DISSENT (DOUBT)</span>
                  <span className="text-rose-400">{activeDebate.againstPct}%</span>
                </div>
                <div className="h-2 bg-rose-950/20 border border-rose-500/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-rose-500 to-red-400 transition-all duration-500 shadow-[0_0_12px_rgba(244,63,94,0.5)]"
                    style={{ width: `${activeDebate.againstPct}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-[90px] border border-dashed border-border/10 flex items-center justify-center rounded-xl">
            <span className="text-[10px] text-muted-foreground uppercase tracking-widest font-black">No active debates</span>
          </div>
        )}

        {/* Live debate stream */}
        <div className="space-y-2">
          <span className="text-[9px] font-black text-muted-foreground/60 uppercase tracking-widest block font-bold">
            Live Swarm Argument Stream
          </span>
          <div className="space-y-2 max-h-[140px] overflow-y-auto bg-[#020204] p-3 rounded-xl border border-border/5">
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
                  <span className="font-black uppercase tracking-wider text-[8px] opacity-75">
                    {log.agent}
                  </span>
                </div>
                <p className="font-semibold text-muted-foreground/90">{log.msg}</p>
              </div>
            ))}
            {argumentLog.length === 0 && (
              <div className="text-center py-4">
                <span className="text-[9px] font-mono text-muted-foreground/40 uppercase">Awaiting arguments...</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

