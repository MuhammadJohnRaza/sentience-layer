"use client";

import { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";

interface SpotMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export function SpotChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<SpotMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      setHasUnread(false);
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen]);

  const downloadTrace = () => {
    const traceData = {
      timestamp: new Date().toISOString(),
      platform: "Google Antigravity",
      core_orchestrator: "SwarmOrchestrator",
      incidents: [
        {
          id: "incident_checkout_saturation",
          anomaly: "Checkout submission latency surged to 425.2ms, correlated with 98.2% database pool saturation and 30.4% conversion drop.",
          reasoning_steps: [
            {
              step: 1,
              agent: "CriticAgent",
              action: "Telemetry Anomaly Detection",
              evidence: "Relational registry read query scanning unindexed transaction columns.",
              implication: "High-concurrency read operations blocking checkout registry thread writes.",
              severity: "CRITICAL"
            },
            {
              step: 2,
              agent: "CausalInferenceAgent",
              action: "Causal Link Mapping",
              causal_coefficient: 0.94,
              financial_implication: "$24,580.00 projected daily revenue loss."
            },
            {
              step: 3,
              agent: "ConsensusAgent",
              action: "Swarm Voting Consensus",
              votes: {
                "CriticAgent": "APPROVE",
                "OpportunityAnalystAgent": "APPROVE",
                "EconomicForecastingAgent": "APPROVE",
                "DoubtAgent": "APPROVE"
              },
              authorized_playbook: "Postgres Caching Index Optimization"
            },
            {
              step: 4,
              agent: "DoubtAgent",
              action: "Sandbox Containment Lock",
              quarantine_status: "LOCKED",
              sandbox: "Doubt Room Isolated Thread Pool"
            },
            {
              step: 5,
              agent: "ActionExecutionAgent",
              action: "Playbook Execution",
              simulated_task: "CRM Targeted Discount Incentive campaign and Postgres Cache tuning.",
              target_cohort: "Incentivized Cart Leavers",
              projected_recovery: "+12.5% Conversion Boost"
            }
          ],
          system_state_change: {
            before: {
              checkout_latency_ms: 425.2,
              connection_utilization_pct: 98.2,
              cart_abandonment_pct: 42.0,
              loss_usd: 24580.0
            },
            after: {
              checkout_latency_ms: 18.2,
              connection_utilization_pct: 11.2,
              cart_abandonment_pct: 2.8,
              recovered_usd: 24580.0,
              stabilization_status: "NOMINAL"
            }
          }
        }
      ],
      mcp_dynamic_registrations: [
        {
          server_name: "slack-mcp",
          url: "ws://localhost:8000/mcp/slack",
          status: "SUCCESSFULLY_CONNECTED",
          exposed_tools: ["post_channel_alert", "create_incident_thread"]
        }
      ]
    };

    const blob = new Blob([JSON.stringify(traceData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `antigravity_agent_trace_logs_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const send = async () => {
    const content = input.trim();
    if (!content || isLoading) return;

    const userMsg: SpotMessage = { id: Date.now().toString(), role: "user", content };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = (await api.sendMessage(content, { agent_id: "critic" })) as any;
      const assistantMsg: SpotMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: res.content || "Kernel processed your query.",
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (!isOpen) setHasUnread(true);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 1).toString(), role: "assistant", content: "⚠️ Connection error. Kernel unreachable." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  };

  return (
    <>
      {/* Floating bubble trigger */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          "fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full border-2 transition-all duration-300 shadow-[0_0_24px_rgba(124,58,237,0.5)] hover:shadow-[0_0_36px_rgba(124,58,237,0.7)] hover:scale-110",
          isOpen
            ? "bg-card border-primary/60 text-primary-foreground rotate-0"
            : "bg-card border-border/40 text-primary-foreground"
        )}
        aria-label="SpotChat"
      >
        <span className="text-xl select-none">{isOpen ? "✕" : "💬"}</span>
        {hasUnread && !isOpen && (
          <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-violet-500 text-[9px] font-black text-white shadow-lg animate-bounce">
            !
          </span>
        )}
      </button>

      {/* SpotChat window */}
      <div
        className={cn(
          "fixed bottom-24 right-6 z-50 w-80 sm:w-96 rounded-2xl border-2 border-border/50 bg-card shadow-[0_8px_40px_rgba(0,0,0,0.9)] overflow-hidden flex flex-col transition-all duration-400 ease-in-out",
          isOpen ? "opacity-100 translate-y-0 pointer-events-auto" : "opacity-0 translate-y-4 pointer-events-none"
        )}
        style={{ height: isOpen ? "440px" : "0px", transition: "height 0.35s ease, opacity 0.3s ease, transform 0.3s ease" }}
      >
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-border/20 bg-card/80 px-4 py-3 shrink-0">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-border/30 bg-primary/10 text-base shadow-[0_0_10px_rgba(124,58,237,0.3)] animate-pulse">
            ⚡
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[11px] font-black tracking-widest text-primary-foreground uppercase">Spot Chat</p>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping inline-block" />
              <span className="text-[9px] font-bold text-muted-foreground tracking-wider uppercase">Kernel Online</span>
            </div>
          </div>
          <div className="flex gap-2 shrink-0">
            <button
              onClick={downloadTrace}
              className="text-[8px] font-black text-violet-400 hover:text-violet-300 transition-colors tracking-widest uppercase border border-violet-500/30 px-1.5 py-0.5 rounded bg-violet-500/10 shadow-[0_0_8px_rgba(124,58,237,0.2)]"
              title="Download Google Antigravity Agent Trace Logs"
            >
              📥 Trace Logs
            </button>
            <button
              onClick={() => setMessages([])}
              className="text-[9px] font-black text-muted-foreground/60 hover:text-destructive transition-colors tracking-widest uppercase"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 bg-background/20">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center gap-2 py-8">
              <span className="text-3xl">🔮</span>
              <p className="text-[10px] font-black text-muted-foreground/60 tracking-widest uppercase">Quick cognitive query</p>
              <p className="text-[9px] text-muted-foreground/40 tracking-wide">Type anything to engage the kernel</p>
            </div>
          )}
          {messages.map((m) => (
            <div
              key={m.id}
              className={cn(
                "flex",
                m.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-[82%] rounded-2xl px-3 py-2 text-[11px] font-semibold leading-relaxed break-words shadow-sm",
                  m.role === "user"
                    ? "bg-primary/20 border border-primary/30 text-primary-foreground rounded-br-sm"
                    : "bg-card/70 border border-border/30 text-primary-foreground/90 rounded-bl-sm"
                )}
              >
                {m.role === "assistant" && (
                  <span className="text-[9px] font-black text-violet-400 tracking-widest uppercase block mb-1">⚡ Kernel</span>
                )}
                {m.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-card/70 border border-border/30 rounded-2xl rounded-bl-sm px-4 py-2.5">
                <div className="flex gap-1 items-center">
                  <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="border-t border-border/20 bg-card/60 px-3 py-3 shrink-0">
          <div className="flex items-center gap-2">
            <input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask the kernel anything..."
              disabled={isLoading}
              className="flex-1 h-9 rounded-xl border border-border/30 bg-background/60 px-3 text-[11px] font-semibold text-primary-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all duration-300 disabled:opacity-50"
            />
            <button
              onClick={send}
              disabled={isLoading || !input.trim()}
              className="h-9 w-9 flex items-center justify-center rounded-xl bg-primary/20 border border-primary/30 text-primary-foreground hover:bg-primary/30 hover:shadow-[0_0_12px_rgba(124,58,237,0.4)] disabled:opacity-40 transition-all duration-300 text-sm"
            >
              🚀
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
