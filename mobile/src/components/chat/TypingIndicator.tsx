"use client";

import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";

const REASONING_STAGES = [
  {
    emoji: "🕵️",
    label: "CRITIC_AUDIT",
    description: "CriticAgent is auditing query constraints & transaction boundaries..."
  },
  {
    emoji: "🤝",
    label: "CONSENSUS_NEGOTIATION",
    description: "ConsensusAgent is negotiating alignment across 18 specialized nodes..."
  },
  {
    emoji: "📋",
    label: "PLAYBOOK_SYNTHESIS",
    description: "ActionPlaybookAgent is compiling execution timelines and risk parameters..."
  },
  {
    emoji: "⚡",
    label: "RESPONSE_FINALIZATION",
    description: "Swarm orchestrator is finalizing response synthesis..."
  }
];

export function TypingIndicator() {
  const [stageIndex, setStageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStageIndex((prev) => (prev + 1) % REASONING_STAGES.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const currentStage = REASONING_STAGES[stageIndex];

  return (
    <div className="flex gap-3 items-start my-4 w-full flex-row animate-in fade-in duration-300">
      {/* Avatar column */}
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 border-amber-500/30 bg-amber-950/20 text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.25)] animate-pulse text-sm">
        {currentStage.emoji}
      </div>

      {/* Message bubble content */}
      <div className="rounded-2xl px-4 py-3.5 border bg-card border-border/20 shadow-[0_4px_15px_rgba(0,0,0,0.6)] rounded-tl-none flex items-center gap-3 max-w-[85%] transition-all duration-300">
        <div className="flex items-center gap-1.5 shrink-0">
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)] [animation-delay:-0.3s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)] [animation-delay:-0.15s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)]" />
        </div>
        <div className="flex flex-col gap-0.5">
          <span className="text-[9px] font-black text-amber-500 tracking-wider uppercase">
            {currentStage.label}
          </span>
          <span className="text-xs text-muted-foreground leading-normal animate-pulse">
            {currentStage.description}
          </span>
        </div>
      </div>
    </div>
  );
}

