"use client";

import { useState } from "react";
import { Message } from "@/types";
import { cn, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useStore } from "@/store/useStore";
import { api } from "@/lib/api";

// ── Severity helpers ─────────────────────────────────────────────────────────
const SEVERITY_CONFIG = {
  CRITICAL: { color: "bg-red-950/60 border-red-500/50 text-red-300", dot: "bg-red-400", label: "CRITICAL" },
  HIGH:     { color: "bg-orange-950/60 border-orange-500/50 text-orange-300", dot: "bg-orange-400", label: "HIGH" },
  MEDIUM:   { color: "bg-amber-950/60 border-amber-500/40 text-amber-300", dot: "bg-amber-400", label: "MEDIUM" },
  LOW:      { color: "bg-emerald-950/60 border-emerald-500/40 text-emerald-300", dot: "bg-emerald-400", label: "LOW" },
} as const;

type SeverityKey = keyof typeof SEVERITY_CONFIG;

export function MessageBubble({ message }: { message: Message }) {
  const isUser   = message.role === "user";
  const isSystem = message.role === "system";

  const [isSaved,      setIsSaved]      = useState(false);
  const [isLoved,      setIsLoved]      = useState(false);
  const [isSaving,     setIsSaving]     = useState(false);
  const [chainOpen,    setChainOpen]    = useState(false);
  const [evidenceOpen, setEvidenceOpen] = useState(true);
  const [actionsOpen,  setActionsOpen]  = useState(true);

  const addNotification = useStore((state) => state.addNotification);

  // Metadata from assistant messages
  const meta          = message.metadata as any;
  const confidence    = meta?.confidence as number | undefined;
  const severity      = (meta?.severity as SeverityKey) ?? null;
  const evidence      = (meta?.evidence as string[]) ?? [];
  const actions       = (meta?.actions  as string[]) ?? [];
  const agentChain    = (meta?.agentChain as any[]) ?? [];
  const keyFinding    = meta?.keyFinding as string | undefined;
  const priority      = meta?.priority  as string | undefined;
  const agentUsed     = meta?.agentUsed as string | undefined;
  const totalMs       = meta?.totalDurationMs as number | undefined;

  const sevCfg = severity && SEVERITY_CONFIG[severity] ? SEVERITY_CONFIG[severity] : null;

  const handleSaveToVault = async () => {
    if (isSaved || isSaving) return;
    setIsSaving(true);
    try {
      const content = `Cognitive Agent Trace\n======================\nTimestamp: ${new Date().toLocaleString()}\nAgent: ${agentUsed ?? "Kernel"}\nConfidence: ${confidence ? (confidence * 100).toFixed(0) + "%" : "N/A"}\nSeverity: ${severity ?? "N/A"}\n\n${message.content}`;
      const blob = new Blob([content], { type: "text/plain" });
      const file = new File([blob], `trace_${message.id.slice(0, 8)}.txt`, { type: "text/plain" });
      const formData = new FormData();
      formData.append("file", file);
      await api.uploadDocument(formData);
      setIsSaved(true);
      addNotification("Trace saved to Memory Vault! 🔒");
    } catch {
      addNotification("Failed to save to vault.");
    } finally {
      setIsSaving(false);
    }
  };

  const attachmentMatch   = message.content.match(/^\[Multimodal Attachment:\s*(.*?)\]\s*([\s\S]*)$/);
  const displayContent    = attachmentMatch ? attachmentMatch[2] : message.content;
  const attachmentFilename = attachmentMatch ? attachmentMatch[1] : null;

  return (
    <div className={cn("flex gap-3 items-start my-4 w-full", isUser ? "flex-row-reverse" : "flex-row")}>

      {/* Avatar */}
      <div className={cn(
        "flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 text-sm font-black transition-all duration-300",
        isUser   ? "bg-primary/20 border-border text-primary-foreground shadow-[0_0_10px_rgba(124,58,237,0.3)]"
        : isSystem ? "bg-destructive/20 border-destructive text-destructive-foreground"
        : "bg-amber-950/20 border-amber-500/30 text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.25)] animate-pulse"
      )}>
        {isUser ? "👤" : isSystem ? "⚠️" : "🧠"}
      </div>

      {/* Bubble */}
      <div className={cn(
        "max-w-[80%] rounded-2xl border transition-all duration-300",
        isUser   ? "bg-primary/10 border-border/60 text-foreground shadow-[0_4px_15px_rgba(124,58,237,0.15)] rounded-tr-none"
        : isSystem ? "bg-destructive/5 border-destructive/30 text-destructive-foreground rounded-tl-none px-4 py-3.5"
        : "bg-card border-border/20 text-foreground shadow-[0_4px_20px_rgba(0,0,0,0.7)] rounded-tl-none"
      )}>

        {/* ── ASSISTANT HEADER ── */}
        {!isUser && !isSystem && (
          <div className="flex flex-wrap items-center gap-2 px-4 pt-3.5 pb-2 border-b border-border/10">
            <span className="text-[10px] font-black tracking-widest uppercase text-amber-300">
              {agentUsed ?? "COGNITIVE KERNEL"}
            </span>

            {/* Confidence */}
            {confidence != null && (
              <div className="flex items-center gap-1.5">
                <div className="w-20 h-1.5 rounded-full bg-border/30 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-violet-500 to-emerald-400 transition-all duration-700"
                    style={{ width: `${(confidence * 100).toFixed(0)}%` }}
                  />
                </div>
                <span className="text-[9px] font-black text-emerald-400 tracking-widest">
                  {(confidence * 100).toFixed(0)}%
                </span>
              </div>
            )}

            {/* Severity badge */}
            {sevCfg && (
              <Badge className={cn("text-[8px] font-black tracking-widest px-2 py-0.5 border flex items-center gap-1", sevCfg.color)}>
                <span className={cn("h-1.5 w-1.5 rounded-full animate-pulse", sevCfg.dot)} />
                {sevCfg.label}
              </Badge>
            )}

            {/* Priority badge */}
            {priority && (
              <Badge className="text-[8px] font-black text-indigo-300 border border-indigo-500/30 bg-indigo-950/40 px-2 py-0.5 tracking-widest">
                ⏱ {priority.replace("_", " ")}
              </Badge>
            )}

            {/* Duration */}
            {totalMs != null && (
              <span className="text-[8px] text-muted-foreground/50 ml-auto font-mono">
                {(totalMs / 1000).toFixed(1)}s
              </span>
            )}
          </div>
        )}

        {/* ── USER HEADER ── */}
        {isUser && (
          <div className="flex items-center gap-2 px-4 pt-3.5 pb-1.5">
            <span className="text-[10px] font-black tracking-widest uppercase text-primary-foreground">USER COGNITION</span>
          </div>
        )}

        {/* ── AGENT CHAIN TRACE ─────────────────────────────────────────── */}
        {!isUser && !isSystem && agentChain.length > 0 && (
          <div className="px-4 py-2">
            <button
              onClick={() => setChainOpen(!chainOpen)}
              className="flex items-center gap-1.5 text-[9px] font-black text-muted-foreground/70 hover:text-primary-foreground tracking-widest uppercase transition-colors"
            >
              <span>{chainOpen ? "▾" : "▸"}</span>
              {agentChain.length}-AGENT CHAIN TRACE
            </button>

            {chainOpen && (
              <div className="mt-2 space-y-1.5">
                {agentChain.map((step: any, i: number) => (
                  <div key={i} className="flex items-start gap-2">
                    {/* Step connector */}
                    <div className="flex flex-col items-center gap-0.5 shrink-0 mt-0.5">
                      <div className={cn(
                        "flex h-6 w-6 items-center justify-center rounded-full border text-xs font-black",
                        step.status === "success"
                          ? "bg-emerald-950/40 border-emerald-500/30 text-emerald-300"
                          : "bg-red-950/40 border-red-500/30 text-red-300"
                      )}>
                        {step.emoji ?? "🤖"}
                      </div>
                      {i < agentChain.length - 1 && (
                        <div className="w-px h-3 bg-border/30" />
                      )}
                    </div>

                    <div className="flex-1 min-w-0 bg-background/30 rounded-lg px-2.5 py-1.5 border border-border/10">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-[9px] font-black text-primary-foreground/90 tracking-wider uppercase">
                          {step.agent_name}
                        </span>
                        <div className="flex items-center gap-1.5 shrink-0">
                          <span className="text-[8px] font-mono text-muted-foreground/50">
                            {step.duration_ms?.toFixed(0)}ms
                          </span>
                          <span className="text-[8px] font-black text-emerald-400">
                            {(step.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                      <p className="text-[10px] text-muted-foreground/70 mt-0.5 leading-relaxed truncate">
                        ↳ {step.output_summary}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ── KEY FINDING BANNER ── */}
        {!isUser && !isSystem && keyFinding && (
          <div className="mx-4 mb-2 px-3 py-2 bg-primary/10 border border-primary/20 rounded-xl">
            <span className="text-[9px] font-black text-primary-foreground/60 tracking-widest uppercase">Key Finding</span>
            <p className="text-xs font-black text-primary-foreground mt-0.5">{keyFinding}</p>
          </div>
        )}

        {/* ── ATTACHMENT BADGE ── */}
        {attachmentFilename && (
          <div className="mx-4 mb-2 flex items-center gap-2 bg-[#020207]/60 border border-border/30 rounded-lg p-2 text-xs font-bold text-amber-300">
            <span>📎</span>
            <Badge className="bg-primary/20 border border-border/40 text-primary-foreground font-mono text-[9px] px-1.5 py-0">
              {attachmentFilename}
            </Badge>
          </div>
        )}

        {/* ── MAIN CONTENT ── */}
        <p className="px-4 pb-2 text-sm leading-relaxed font-medium tracking-wide whitespace-pre-wrap selection:bg-primary/50 selection:text-primary-foreground">
          {displayContent}
        </p>

        {/* ── EVIDENCE ── */}
        {!isUser && !isSystem && evidence.length > 0 && (
          <div className="px-4 pb-2">
            <button
              onClick={() => setEvidenceOpen(!evidenceOpen)}
              className="flex items-center gap-1.5 text-[9px] font-black text-muted-foreground/70 hover:text-amber-300 tracking-widest uppercase transition-colors mb-1.5"
            >
              <span>{evidenceOpen ? "▾" : "▸"}</span>
              📌 EVIDENCE ({evidence.length})
            </button>
            {evidenceOpen && (
              <ul className="space-y-1">
                {evidence.map((e: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-[11px] text-muted-foreground/80 bg-background/30 border border-border/10 rounded-lg px-2.5 py-1.5">
                    <span className="text-amber-400 shrink-0 font-black text-[9px] mt-0.5">#{i + 1}</span>
                    <span className="leading-relaxed">{e}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* ── ACTIONS ── */}
        {!isUser && !isSystem && actions.length > 0 && (
          <div className="px-4 pb-3">
            <button
              onClick={() => setActionsOpen(!actionsOpen)}
              className="flex items-center gap-1.5 text-[9px] font-black text-muted-foreground/70 hover:text-emerald-300 tracking-widest uppercase transition-colors mb-1.5"
            >
              <span>{actionsOpen ? "▾" : "▸"}</span>
              🎯 ACTION ITEMS ({actions.length})
            </button>
            {actionsOpen && (
              <ul className="space-y-1.5">
                {actions.map((a: any, i: number) => {
                  const isObj = typeof a === "object" && a !== null;
                  const title = isObj ? (a.title || a.name || "Action Item") : String(a);
                  const desc = isObj ? a.description : "";

                  return (
                    <li key={i} className="flex flex-col gap-1 text-[11px] text-emerald-300/80 bg-[#061e14]/40 border border-emerald-500/15 rounded-lg px-2.5 py-1.5 shadow-sm">
                      <div className="flex items-center gap-2">
                        <span className="text-emerald-400 shrink-0 font-black text-xs">✓</span>
                        <span className="leading-relaxed font-bold text-emerald-200">{title}</span>
                        {isObj && a.status && (
                          <Badge className="ml-auto text-[7px] font-black tracking-widest uppercase bg-[#05140e] text-emerald-400 border border-emerald-500/30 px-1 py-0 h-4">
                            {a.status}
                          </Badge>
                        )}
                      </div>
                      {desc && (
                        <p className="text-[10px] text-muted-foreground/80 leading-relaxed pl-3.5 border-l border-emerald-500/10 mt-0.5">
                          {desc}
                        </p>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        )}

        {/* ── ACTION BUTTONS ── */}
        {!isUser && !isSystem && (
          <div className="px-4 pb-3 flex items-center gap-2 pt-1 border-t border-border/10">
            <Button variant="outline" size="sm" onClick={handleSaveToVault} disabled={isSaving}
              className={cn(
                "text-[9px] font-black tracking-widest uppercase transition-all duration-300 rounded-lg px-2.5 py-1 border h-7",
                isSaved
                  ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-400"
                  : "bg-background/40 border-border/30 text-primary-foreground hover:bg-primary/20"
              )}>
              {isSaving ? "⏳ SAVING..." : isSaved ? "🔒 SAVED" : "💾 SAVE TO VAULT"}
            </Button>
            <Button variant="outline" size="sm" onClick={() => { setIsLoved(!isLoved); if (!isLoved) addNotification("Saved to highlights! ❤️"); }}
              className={cn(
                "transition-all duration-300 rounded-lg px-2.5 py-1 border h-7 text-xs",
                isLoved ? "bg-rose-950/30 border-rose-500/40 text-rose-400" : "bg-background/40 border-border/30 text-muted-foreground"
              )}>
              {isLoved ? "❤️" : "🤍"}
            </Button>
            <span className="ml-auto text-[9px] text-muted-foreground/40 font-mono">{formatDate(message.timestamp)}</span>
          </div>
        )}

        {/* USER timestamp */}
        {isUser && (
          <div className="px-4 pb-3 text-[9px] text-right text-muted-foreground/40 font-mono">
            {formatDate(message.timestamp)}
          </div>
        )}
      </div>
    </div>
  );
}
