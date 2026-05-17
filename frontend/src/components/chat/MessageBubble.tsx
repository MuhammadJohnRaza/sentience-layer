"use client";

import { useState } from "react";
import { Message } from "@/types";
import { cn, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useStore } from "@/store/useStore";
import { api } from "@/lib/api";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  const [isSaved, setIsSaved] = useState(false);
  const [isLoved, setIsLoved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const addNotification = useStore((state) => state.addNotification);

  const handleSaveToVault = async () => {
    if (isSaved || isSaving) return;
    setIsSaving(true);
    try {
      const fileContent = `Cognitive Agent Trace Document
==============================
Timestamp: ${new Date().toLocaleString()}
Message ID: ${message.id}

Cognitive Content:
--------------------
${message.content}
`;
      const blob = new Blob([fileContent], { type: "text/plain" });
      const file = new File([blob], `cognitive_trace_${message.id.slice(0, 8)}.txt`, {
        type: "text/plain",
      });

      const formData = new FormData();
      formData.append("file", file);

      await api.uploadDocument(formData);
      setIsSaved(true);
      addNotification("Trace saved to Memory Vault successfully! 🔒");
    } catch (e) {
      console.error(e);
      addNotification("Failed to save to vault.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleToggleLove = () => {
    setIsLoved(!isLoved);
    if (!isLoved) {
      addNotification("Saved to system highlights! ❤️");
    }
  };

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

        {/* Action Buttons */}
        {!isUser && !isSystem && (
          <div className="mt-3 flex items-center gap-2 pt-2 border-t border-border/10">
            <Button
              variant="outline"
              size="sm"
              onClick={handleSaveToVault}
              disabled={isSaving}
              className={cn(
                "text-[9px] font-black tracking-widest uppercase transition-all duration-300 rounded-lg px-2.5 py-1 border h-7",
                isSaved
                  ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-400 hover:bg-emerald-950/40 shadow-[0_0_8px_rgba(16,185,129,0.2)]"
                  : "bg-background/40 border-border/30 text-primary-foreground hover:bg-primary/20 hover:border-border"
              )}
            >
              {isSaving ? "⏳ SAVING..." : isSaved ? "🔒 SAVED TO VAULT" : "💾 SAVE TO VAULT"}
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={handleToggleLove}
              className={cn(
                "transition-all duration-300 rounded-lg px-2.5 py-1 border h-7 text-xs flex items-center justify-center gap-1",
                isLoved
                  ? "bg-rose-950/30 border-rose-500/40 text-rose-400 hover:bg-rose-950/40 shadow-[0_0_8px_rgba(244,63,94,0.2)]"
                  : "bg-background/40 border-border/30 text-muted-foreground hover:bg-rose-950/20 hover:border-rose-500/30"
              )}
            >
              {isLoved ? "❤️" : "🤍"}
            </Button>
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
