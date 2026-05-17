"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useStore } from "@/store/useStore";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function PlaybookPage() {
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [playbook, setPlaybook] = useState<any>(null);
  const [activeSessions, setActiveSessions] = useState(0);
  const [vaultDocs, setVaultDocs] = useState(0);
  const [isExported, setIsExported] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [expandedTask, setExpandedTask] = useState<string | null>(null);

  const addNotification = useStore((state) => state.addNotification);

  // Load telemetry metrics
  useEffect(() => {
    api.getChatHistory().then((history) => setActiveSessions(history.length));
    api.getVaultDocuments().then((docs) => {
      // Exclude the placeholder diagnostic trace doc
      const customDocs = docs.filter(d => d.id !== "init_vault_doc");
      setVaultDocs(customDocs.length);
    });
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    setLoadingStep(0);
    setIsExported(false);

    // Dynamic reasoning milestones
    const steps = [
      "🔍 Inspecting active communication logs...",
      "📁 Parsing uploaded vault documents & memory layers...",
      "🧠 Constructing multi-agent critical path dependency network...",
      "⚡ Finalizing 30-day autonomous action plan...",
    ];

    for (let i = 0; i < steps.length; i++) {
      setLoadingStep(i);
      await new Promise((resolve) => setTimeout(resolve, 900));
    }

    try {
      const response = await api.generatePlaybook();
      setPlaybook(response);
      addNotification("30-Day Swarm Playbook generated successfully! 🔮");
    } catch (error) {
      addNotification("Playbook generation failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleExportToVault = async () => {
    if (!playbook || isExported || isExporting) return;
    setIsExporting(true);

    try {
      const content = `30-Day Swarm Intelligence Playbook
=========================================
Generated At: ${playbook.generated_at}
Focus Swarm Focus: ${playbook.focus_area}
Chats Analyzed: ${playbook.source_sessions_analyzed}
Vault Documents Analyzed: ${playbook.source_documents_analyzed}

Chronological Day-by-Day Action Plan:
-----------------------------------------
${playbook.tasks.map((t: any) => `
[DAY ${t.day}] [${t.phase.toUpperCase()}] ${t.title}
Assigned Swarm Operator: ${t.agent} (Confidence: ${(t.confidence * 100).toFixed(0)}%)
Description: ${t.description}
Status: ${t.status.toUpperCase()}
`).join("\n")}
`;

      const blob = new Blob([content], { type: "text/plain" });
      const file = new File([blob], `swarm_playbook_${new Date().toISOString().slice(0,10)}.txt`, {
        type: "text/plain",
      });

      const formData = new FormData();
      formData.append("file", file);

      await api.uploadDocument(formData);
      setIsExported(true);
      addNotification("Swarm Playbook exported directly to Vault! 🔒");
    } catch (e) {
      addNotification("Failed to export playbook.");
    } finally {
      setIsExporting(false);
    }
  };

  const stepsList = [
    "🔍 Inspecting active communication logs...",
    "📁 Parsing uploaded vault documents & memory layers...",
    "🧠 Constructing multi-agent critical path dependency network...",
    "⚡ Finalizing 30-day autonomous action plan...",
  ];

  return (
    <div className="flex h-full min-h-screen flex-col bg-[#05050f] p-6 text-foreground space-y-6">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-border/10 pb-6 gap-4">
        <div>
          <h1 className="text-3xl font-black tracking-widest text-primary-foreground flex items-center gap-3 uppercase">
            🔮 Cognitive Playbook Generator
          </h1>
          <p className="text-xs text-muted-foreground/80 font-bold mt-1 tracking-wider uppercase flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-primary animate-ping" />
            Active Memory Swarm Synthesizer
          </p>
        </div>

        {/* Input Sources Summary */}
        <div className="flex items-center gap-4 bg-card/45 border border-border/20 rounded-xl p-3 shadow-inner">
          <div className="text-center px-3 border-r border-border/10">
            <p className="text-[10px] text-muted-foreground font-black tracking-widest uppercase">Memory Vault</p>
            <p className="text-md font-black text-amber-300 mt-0.5">{vaultDocs} Stored</p>
          </div>
          <div className="text-center px-3">
            <p className="text-[10px] text-muted-foreground font-black tracking-widest uppercase">Chat History</p>
            <p className="text-md font-black text-primary-foreground mt-0.5">{activeSessions} Logs</p>
          </div>
        </div>
      </div>

      {/* Main Generator Section */}
      {!playbook && !loading && (
        <Card className="border-2 border-border/30 bg-card/20 shadow-[0_10px_35px_rgba(0,0,0,0.7)] backdrop-blur-md max-w-xl mx-auto py-12 px-8 text-center my-12">
          <div className="h-16 w-16 bg-primary/20 border border-primary/30 rounded-full flex items-center justify-center text-3xl mx-auto mb-6 animate-pulse">
            ⚡
          </div>
          <h2 className="text-lg font-black tracking-widest text-primary-foreground uppercase">Compile 30-Day Swarm Roadmap</h2>
          <p className="text-xs text-muted-foreground/80 mt-4 leading-relaxed font-semibold tracking-wider max-w-md mx-auto">
            Process all stored system memories, session logs, and vault archives through the 18-agent ReAct kernel to construct a critical-path 30-day operations playbook.
          </p>
          <Button
            onClick={handleGenerate}
            className="mt-8 px-8 py-5 bg-primary/20 hover:bg-primary/35 border-2 border-border/50 hover:border-border text-primary-foreground font-black tracking-widest uppercase rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(124,58,237,0.3)]"
          >
            🚀 Run Synthesis Cycle
          </Button>
        </Card>
      )}

      {/* Loading Reasoning Steps */}
      {loading && (
        <Card className="border-2 border-border/30 bg-card/25 shadow-[0_10px_35px_rgba(0,0,0,0.8)] max-w-md mx-auto p-8 my-16">
          <div className="flex items-center justify-between mb-4">
            <p className="text-[10px] font-black tracking-widest text-primary-foreground uppercase">Cognitive Kernel Thinking</p>
            <p className="text-xs font-black text-amber-300">{( (loadingStep + 1) / 4 * 100).toFixed(0)}%</p>
          </div>
          <Progress value={((loadingStep + 1) / 4) * 100} className="h-2 bg-background/50 border border-border/20 rounded-full mb-6" />
          <div className="space-y-3">
            {stepsList.map((step, idx) => (
              <div
                key={idx}
                className={cn(
                  "flex items-center gap-3 text-xs font-semibold py-2 px-3 rounded-lg border transition-all duration-300",
                  idx === loadingStep
                    ? "bg-primary/20 border-primary text-primary-foreground shadow-[0_0_8px_rgba(124,58,237,0.2)] animate-pulse"
                    : idx < loadingStep
                      ? "bg-emerald-950/20 border-emerald-500/35 text-emerald-400"
                      : "bg-transparent border-transparent text-muted-foreground/40"
                )}
              >
                <span>{idx < loadingStep ? "✅" : idx === loadingStep ? "⏳" : "🔒"}</span>
                <span>{step}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Playbook Display Output */}
      {playbook && !loading && (
        <div className="space-y-6 animate-fade-in">
          {/* Output Header */}
          <Card className="border border-border/20 bg-card/30 backdrop-blur-md p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-2">
                <Badge className="bg-primary/30 border border-primary/50 text-primary-foreground font-black text-[9px] px-2 py-0.5 tracking-wider uppercase">
                  Swarm Focus Area
                </Badge>
                <h2 className="text-xl font-black text-amber-300 tracking-wider uppercase">{playbook.focus_area}</h2>
                <div className="flex items-center gap-4 text-xs font-bold text-muted-foreground/80 mt-2 uppercase tracking-wide">
                  <span>📊 Chats Analyzed: <span className="text-primary-foreground">{playbook.source_sessions_analyzed}</span></span>
                  <span>🔒 Vault Documents: <span className="text-primary-foreground">{playbook.source_documents_analyzed}</span></span>
                  <span>📅 Compiled: <span className="text-primary-foreground">{playbook.generated_at}</span></span>
                </div>
              </div>

              <div className="flex flex-wrap gap-2.5">
                <Button
                  onClick={handleExportToVault}
                  disabled={isExported || isExporting}
                  className={cn(
                    "font-black text-xs tracking-widest uppercase transition-all duration-300 rounded-xl px-5 py-4 border-2 h-10",
                    isExported
                      ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-400 hover:bg-emerald-950/40 shadow-[0_0_10px_rgba(16,185,129,0.2)]"
                      : "bg-primary/10 border-border/40 text-primary-foreground hover:bg-primary/20 hover:border-border hover:shadow-[0_0_15px_rgba(124,58,237,0.3)]"
                  )}
                >
                  {isExporting ? "⏳ EXPORTING..." : isExported ? "🔒 EXPORTED TO VAULT" : "📁 EXPORT PLAYBOOK TO VAULT"}
                </Button>
                
                <Button
                  variant="outline"
                  onClick={handleGenerate}
                  className="border border-border/20 text-xs font-black tracking-widest text-muted-foreground uppercase hover:bg-destructive/10 hover:text-destructive hover:border-destructive/30 rounded-xl py-4 h-10"
                >
                  🔄 RE-RUN SYNTHESIS
                </Button>
              </div>
            </div>
          </Card>

          {/* Timeline Grid */}
          <h3 className="text-md font-black tracking-widest text-primary-foreground uppercase mt-4">30-Day Swarm Roadmap</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {playbook.tasks.map((task: any) => {
              const isCompleted = task.status === "completed";
              const isExpanded = expandedTask === task.id;

              return (
                <Card
                  key={task.id}
                  onClick={() => setExpandedTask(isExpanded ? null : task.id)}
                  className={cn(
                    "border transition-all duration-300 hover:scale-[1.01] cursor-pointer bg-card/25 backdrop-blur-md relative overflow-hidden flex flex-col justify-between",
                    isCompleted
                      ? "border-emerald-500/25 hover:border-emerald-500/45 shadow-[0_4px_15px_rgba(16,185,129,0.08)]"
                      : "border-border/20 hover:border-border/55 hover:shadow-[0_4px_20px_rgba(124,58,237,0.12)]"
                  )}
                >
                  {/* Phase Status Banner */}
                  <div className={cn(
                    "absolute left-0 top-0 bottom-0 w-1",
                    task.phase === "Foundation"
                      ? "bg-amber-500"
                      : task.phase === "Integration"
                        ? "bg-primary"
                        : task.phase === "Optimization"
                          ? "bg-sky-500"
                          : "bg-emerald-500"
                  )} />

                  <CardContent className="p-4 pl-5 space-y-3.5">
                    {/* Header bar */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-black text-primary-foreground tracking-widest uppercase">DAY {task.day}</span>
                        <Badge className={cn(
                          "text-[9px] font-black tracking-widest uppercase py-0.5",
                          task.phase === "Foundation"
                            ? "bg-amber-950/65 text-amber-400 border border-amber-500/30"
                            : task.phase === "Integration"
                              ? "bg-indigo-950/65 text-indigo-400 border border-indigo-500/30"
                              : task.phase === "Optimization"
                                ? "bg-sky-950/65 text-sky-400 border border-sky-500/30"
                                : "bg-emerald-950/65 text-emerald-400 border border-emerald-500/30"
                        )}>
                          {task.phase}
                        </Badge>
                      </div>
                      <span className="text-xs">{isCompleted ? "✅" : "⏳"}</span>
                    </div>

                    {/* Task Title */}
                    <p className="font-extrabold text-sm text-foreground tracking-wide line-clamp-2 uppercase">
                      {task.title}
                    </p>

                    {/* Collapsible Info Panel */}
                    {isExpanded && (
                      <div className="text-xs font-medium text-muted-foreground/80 leading-relaxed pt-2 border-t border-border/10 animate-slide-down">
                        {task.description}
                      </div>
                    )}

                    {/* Footer operator badges */}
                    <div className="flex items-center justify-between pt-2 border-t border-border/10">
                      <Badge className="bg-background border border-border/20 text-[9px] font-extrabold text-amber-300">
                        👾 {task.agent}
                      </Badge>
                      <span className="text-[9px] font-extrabold text-muted-foreground">
                        {(task.confidence * 100).toFixed(0)}% CONFIDENCE
                      </span>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
