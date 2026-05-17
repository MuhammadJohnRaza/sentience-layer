"use client";

import { cn } from "@/lib/utils";

export function TypingIndicator() {
  return (
    <div className="flex gap-3 items-start my-4 w-full flex-row">
      {/* Avatar column */}
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 border-amber-500/30 bg-amber-950/20 text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.25)] animate-pulse text-sm">
        🧠
      </div>

      {/* Message bubble content */}
      <div className="rounded-2xl px-4 py-3.5 border bg-card border-border/20 shadow-[0_4px_15px_rgba(0,0,0,0.6)] rounded-tl-none flex items-center gap-2">
        <div className="flex items-center gap-1.5 mr-1">
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)] [animation-delay:-0.3s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)] [animation-delay:-0.15s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary shadow-[0_0_6px_rgba(124,58,237,0.8)]" />
        </div>
        <span className="text-[10px] font-black text-amber-300 tracking-widest uppercase animate-pulse">
          Agents are reasoning...
        </span>
      </div>
    </div>
  );
}
