"use client";

import { Message } from "@/types";
import { cn, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  return (
    <div className={cn("flex gap-3 items-start my-4 w-full", isUser ? "flex-row-reverse" : "flex-row")}>
      {/* Avatar column */}
      <div 
        className={cn(
          "flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 text-sm font-black transition-all duration-300",
          isUser
            ? "bg-primary/20 border-border text-primary-foreground shadow-[0_0_10px_rgba(124,58,237,0.3)]"
            : isSystem
              ? "bg-destructive/20 border-destructive text-destructive-foreground shadow-[0_0_10px_rgba(239,68,68,0.3)]"
              : "bg-amber-950/20 border-amber-500/30 text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.25)] animate-pulse"
        )}
      >
        {isUser ? "👤" : isSystem ? "⚠️" : "🧠"}
      </div>

      {/* Message bubble content */}
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-3.5 border transition-all duration-300",
          isUser
            ? "bg-primary/10 border-border/60 text-foreground shadow-[0_4px_15px_rgba(124,58,237,0.15)] rounded-tr-none hover:border-border"
            : isSystem
              ? "bg-destructive/5 border-destructive/30 text-destructive-foreground rounded-tl-none"
              : "bg-card border-border/20 text-foreground shadow-[0_4px_15px_rgba(0,0,0,0.6)] rounded-tl-none hover:border-border/50"
        )}
      >
        {/* Header (Display Role / Agent name) */}
        <div className="flex items-center gap-2 mb-1.5">
          <span className={cn(
            "text-[10px] font-black tracking-widest uppercase",
            isUser ? "text-primary-foreground" : isSystem ? "text-destructive" : "text-amber-300"
          )}>
            {isUser ? "USER COGNITION" : isSystem ? "SYSTEM ALIGNMENT" : "COGNITIVE KERNEL"}
          </span>
          {message.metadata?.confidence && (
            <Badge className="bg-emerald-950/80 text-emerald-400 border border-emerald-500/25 text-[9px] font-extrabold px-1.5 py-0">
              {(message.metadata.confidence * 100).toFixed(0)}% CONFIDENCE
            </Badge>
          )}
        </div>

        {/* Content text */}
        <p className="text-sm leading-relaxed font-medium tracking-wide whitespace-pre-wrap selection:bg-primary/50 selection:text-primary-foreground">
          {message.content}
        </p>

        {/* Action badges */}
        {message.metadata?.actions && message.metadata.actions.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2 pt-2 border-t border-border/10">
            {message.metadata.actions.map((action: any) => (
              <Badge
                key={action.id}
                variant="outline"
                className="text-xs cursor-pointer bg-background/50 border-border/30 text-primary-foreground hover:bg-primary/25 hover:border-border font-bold tracking-wide transition-all duration-300 py-1"
              >
                ⚙️ {action.title}
              </Badge>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <div className="mt-2 flex items-center justify-end text-[9px] font-bold tracking-widest text-muted-foreground/60">
          {formatDate(message.timestamp)}
        </div>
      </div>
    </div>
  );
}
