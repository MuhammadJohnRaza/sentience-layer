"use client";

import { useState, useRef, useEffect } from "react";
import { useChat } from "@/hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedActions } from "./SuggestedActions";
import { VoiceInput } from "./VoiceInput";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { useStore } from "@/store/useStore";
import { api } from "@/lib/api";
import { AGENT_TYPES } from "@/lib/constants";

export function ChatInterface() {
  const { messages, isLoading, sendMessage, clearChat } = useChat();
  const inputRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Multimodal states
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  // Active datasource switches
  const [vaultActive, setVaultActive] = useState(true);
  const [postgresActive, setPostgresActive] = useState(false);
  const [causalActive, setCausalActive] = useState(false);
  const [swarmActive, setSwarmActive] = useState(true);

  // Agent Swarm Selector and Custom System Prompt States
  const [selectedAgent, setSelectedAgent] = useState("critic");
  const [chatSize, setChatSize] = useState<"compact" | "normal" | "immersive">("normal");
  const [showControls, setShowControls] = useState(true);
  const [isPromptDrawerOpen, setIsPromptDrawerOpen] = useState(false);
  const [customSystemPrompts, setCustomSystemPrompts] = useState<Record<string, string>>({
    critic: "You are the swarm's Critic Agent. Your objective is to thoroughly stress-test every idea, proposal, and document, highlighting architectural blindspots, severe edge cases, and missing failure modes with constructive skepticism.",
    personalization: "You are the Personalization Agent. Your goal is to adapt all swarm outputs to the user's explicit profile, preferred vocabulary, expertise level, and historical interaction telemetry.",
    memory: "You are the Memory Agent. You maintain semantic indexing across the cognitive vault, retrieving past contexts and linking active inquiries back to consolidated knowledge nodes.",
    deterministic: "You are the Deterministic Agent. Your focus is absolute mathematical rigor, structured execution rules, and validating that swarm actions conform to exact systemic boundaries.",
    ranking: "You are the Action Ranking Agent. You evaluate list outcomes and rank them based on expected utility, resource cost, feasibility, and cognitive impact score.",
    priority: "You are the Priority Agent. Your goal is to separate the signal from the noise, identifying critical-path actions that require immediate tactical execution.",
    opportunity: "You are the Swarm Opportunity Analyst. You scan documents and logs to discover hidden cost efficiencies, potential strategic growth points, and high-ROI opportunities.",
    causal: "You are the Causal Inference Agent. You trace chain-reaction linkages between active variables, modeling the upstream causes and downstream effects of every intervention.",
    adversarial: "You are the Red Team Swarm Agent. You play devil's advocate, identifying potential security risks, data leakage points, and hostile exploits in any proposed logic.",
    debate: "You are the Debate Agent. You present alternative viewpoints, orchestrating counter-arguments to ensure the swarm explores the full matrix of possibilities.",
    consensus: "You are the Consensus Agent. You aggregate recommendations from all 18 swarm workers to find the optimal common ground and compile the final action roadmap.",
    uncertainty: "You are the Uncertainty Agent. You calculate confidence scores and identify assumptions, ensuring the user understands the exact variance and margin of error.",
    economic: "You are the Economic Swarm Agent. You evaluate financial metrics, calculating ROI percentages, cost-benefit ratios, and projected hedge efficiencies over time.",
    dream: "You are the Dream Agent. You consolidate random, unorganized daily chat traces and raw memories into clean, high-level structural concepts.",
    premonition: "You are the Premonition Agent. You analyze long-term historical trends to forecast potential future bottlenecks, disruptions, and strategic pivot points.",
    ethics: "You are the Swarm Ethics Auditor. You cross-reference actions with safety alignment, bias reduction, and human-in-the-loop guidelines to ensure complete compliance.",
    action_category: "You are the Action Classifier. You sort incoming tasks and raw ideas into highly organized functional domains for maximum dispatch efficiency.",
    action_playbook: "You are the Playbook Compiler. You organize individual action items into a clean, day-by-day sequential operations plan over a 30-day timeline.",
  });

  const addNotification = useStore((state) => state.addNotification);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      addNotification(`Document telemetry attached: ${file.name} 📎`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const content = inputRef.current?.value.trim();
    if ((!content && !selectedFile) || isLoading || isUploading) return;

    let finalPrompt = content || "";
    setIsUploading(true);

    try {
      if (selectedFile) {
        // Compile FormData payload and upload directly to Memory Vault Database
        const formData = new FormData();
        formData.append("file", selectedFile);
        
        await api.uploadDocument(formData);
        
        // Stamp the multimodal signature at the top of the prompt
        finalPrompt = `[Multimodal Attachment: ${selectedFile.name}] ${finalPrompt || "Inspect the attached document telemetry."}`;
      }

      const activeDatasources = [];
      if (vaultActive) activeDatasources.push("VaultRetriever");
      if (postgresActive) activeDatasources.push("PostgreSQL_MCP");
      if (causalActive) activeDatasources.push("CausalExplorer");
      if (swarmActive) activeDatasources.push("SwarmCore");

      // Dispatch real multimodal reasoning prompt
      await sendMessage(finalPrompt, {
        datasources: activeDatasources,
        agent_id: selectedAgent,
        system_prompt: customSystemPrompts[selectedAgent],
      });

      if (inputRef.current) inputRef.current.value = "";
      setSelectedFile(null);
    } catch (err) {
      console.error(err);
      addNotification("Failed to dispatch multimodal request.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className={cn(
      "flex flex-col rounded-xl border-2 border-border/50 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.8)] overflow-hidden transition-all duration-500 ease-in-out",
      chatSize === "compact" ? "min-h-[45vh] h-[45vh]" :
      chatSize === "immersive" ? "min-h-[82vh] h-[82vh]" : "min-h-[68vh] h-[68vh]"
    )}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border/20 bg-card/60 p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-border/20 text-primary-foreground shadow-[0_0_12px_rgba(124,58,237,0.3)] text-xl animate-pulse">
            💬
          </div>
          <div>
            <h2 className="font-black text-sm tracking-widest text-primary-foreground uppercase">Sentience Cognitive Chat</h2>
            <p className="text-[10px] font-black text-muted-foreground mt-0.5 tracking-wider uppercase flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping inline-block" />
              🧠 Multi-Agent Reasoning Kernel Active
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setShowControls(!showControls)}
            className={cn(
              "border border-border/20 text-[10px] font-black tracking-widest transition-all duration-300 py-1",
              showControls ? "bg-primary/20 text-primary-foreground border-primary/30" : "text-muted-foreground hover:bg-border/10"
            )}
          >
            {showControls ? "🔒 HIDE SETTINGS" : "⚙️ SHOW SETTINGS"}
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={clearChat}
            className="border border-border/20 text-[10px] font-black tracking-widest hover:bg-destructive/20 hover:text-destructive hover:border-destructive/30 transition-all duration-300 py-1"
          >
            🧹 CLEAR CHAT
          </Button>
        </div>
      </div>

      {/* Collapsible Controls Wrapper — datasources + agent swarm selector */}
      <div
        className={cn(
          "overflow-hidden transition-all duration-500 ease-in-out",
          showControls ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"
        )}
      >
        {/* Multi-Datasource Swarm Selector Panel */}
        <div className="flex flex-wrap gap-2 px-4 py-2.5 border-b border-border/10 bg-card/15 justify-start items-center">
          <span className="text-[8px] font-black text-muted-foreground/80 tracking-widest uppercase mr-2">Active Datasources:</span>
          
          <Badge
            onClick={() => setVaultActive(!vaultActive)}
            className={cn(
              "cursor-pointer text-[8px] font-black tracking-wider py-1 px-2.5 rounded-full border transition-all duration-300 uppercase",
              vaultActive
                ? "bg-amber-950/45 border-amber-500/40 text-amber-300 shadow-[0_0_8px_rgba(245,158,11,0.2)]"
                : "bg-background/40 border-border/20 text-muted-foreground/40 hover:bg-background/60"
            )}
          >
            📁 Vault Retriever
          </Badge>

          <Badge
            onClick={() => setPostgresActive(!postgresActive)}
            className={cn(
              "cursor-pointer text-[8px] font-black tracking-wider py-1 px-2.5 rounded-full border transition-all duration-300 uppercase",
              postgresActive
                ? "bg-emerald-950/45 border-emerald-500/40 text-emerald-300 shadow-[0_0_8px_rgba(16,185,129,0.2)]"
                : "bg-background/40 border-border/20 text-muted-foreground/40 hover:bg-background/60"
            )}
          >
            🗄️ PostgreSQL MCP
          </Badge>

          <Badge
            onClick={() => setCausalActive(!causalActive)}
            className={cn(
              "cursor-pointer text-[8px] font-black tracking-wider py-1 px-2.5 rounded-full border transition-all duration-300 uppercase",
              causalActive
                ? "bg-purple-950/45 border-purple-500/40 text-purple-300 shadow-[0_0_8px_rgba(168,85,247,0.25)]"
                : "bg-background/40 border-border/20 text-muted-foreground/40 hover:bg-background/60"
            )}
          >
            🌐 Causal Explorer
          </Badge>

          <Badge
            onClick={() => setSwarmActive(!swarmActive)}
            className={cn(
              "cursor-pointer text-[8px] font-black tracking-wider py-1 px-2.5 rounded-full border transition-all duration-300 uppercase",
              swarmActive
                ? "bg-indigo-950/45 border-indigo-500/40 text-indigo-300 shadow-[0_0_8px_rgba(99,102,241,0.25)]"
                : "bg-background/40 border-border/20 text-muted-foreground/40 hover:bg-background/60"
            )}
          >
            👾 Swarm Loggers
          </Badge>
        </div>

        {/* Agent swarm custom prompt controller */}
        <div className="border-b border-border/15 bg-background/40 p-4 space-y-3.5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-black text-primary-foreground/90 tracking-widest uppercase">Target Swarm Worker:</span>
              <select
                value={selectedAgent}
                onChange={(e) => setSelectedAgent(e.target.value)}
                className="bg-card border border-border/30 rounded-lg px-3 py-1.5 text-xs font-black text-amber-300 tracking-wider focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all duration-300 cursor-pointer"
              >
                {AGENT_TYPES.map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    🤖 {agent.name} Agent
                  </option>
                ))}
              </select>
            </div>

            {/* Chat Size Selector */}
            <div className="flex items-center gap-1.5 border border-border/20 rounded-lg p-1 bg-background/30 shadow-inner">
              <span className="text-[9px] font-black text-muted-foreground/80 tracking-widest uppercase px-1.5">Size:</span>
              <button
                type="button"
                onClick={() => setChatSize("compact")}
                className={cn(
                  "px-2 py-0.5 text-[8px] font-black tracking-wider rounded transition-all duration-300 uppercase",
                  chatSize === "compact" ? "bg-primary/20 text-primary-foreground border border-primary/30" : "text-muted-foreground/60 hover:text-primary-foreground"
                )}
              >
                Compact
              </button>
              <button
                type="button"
                onClick={() => setChatSize("normal")}
                className={cn(
                  "px-2 py-0.5 text-[8px] font-black tracking-wider rounded transition-all duration-300 uppercase",
                  chatSize === "normal" ? "bg-primary/20 text-primary-foreground border border-primary/30" : "text-muted-foreground/60 hover:text-primary-foreground"
                )}
              >
                Normal
              </button>
              <button
                type="button"
                onClick={() => setChatSize("immersive")}
                className={cn(
                  "px-2 py-0.5 text-[8px] font-black tracking-wider rounded transition-all duration-300 uppercase",
                  chatSize === "immersive" ? "bg-primary/20 text-primary-foreground border border-primary/30" : "text-muted-foreground/60 hover:text-primary-foreground"
                )}
              >
                Immersive
              </button>
            </div>
          </div>
          
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => setIsPromptDrawerOpen(!isPromptDrawerOpen)}
            className="text-[10px] font-black tracking-widest border border-border/20 hover:bg-primary/10 transition-all duration-300"
          >
            {isPromptDrawerOpen ? "🔒 CLOSE SYSTEM PROMPT" : "⚙️ CONFIGURE SYSTEM PROMPT"}
          </Button>
        </div>

        {isPromptDrawerOpen && (
          <div className="space-y-2 p-3 bg-card/45 border border-border/20 rounded-xl transition-all duration-300">
            <div className="flex items-center justify-between">
              <span className="text-[9px] font-black tracking-widest text-muted-foreground uppercase">System Directive (Pre-loaded Prompt):</span>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => {
                  const defaultPrompts: Record<string, string> = {
                    critic: "You are the swarm's Critic Agent. Your objective is to thoroughly stress-test every idea, proposal, and document, highlighting architectural blindspots, severe edge cases, and missing failure modes with constructive skepticism.",
                    personalization: "You are the Personalization Agent. Your goal is to adapt all swarm outputs to the user's explicit profile, preferred vocabulary, expertise level, and historical interaction telemetry.",
                    memory: "You are the Memory Agent. You maintain semantic indexing across the cognitive vault, retrieving past contexts and linking active inquiries back to consolidated knowledge nodes.",
                    deterministic: "You are the Deterministic Agent. Your focus is absolute mathematical rigor, structured execution rules, and validating that swarm actions conform to exact systemic boundaries.",
                    ranking: "You are the Action Ranking Agent. You evaluate list outcomes and rank them based on expected utility, resource cost, feasibility, and cognitive impact score.",
                    priority: "You are the Priority Agent. Your goal is to separate the signal from the noise, identifying critical-path actions that require immediate tactical execution.",
                    opportunity: "You are the Swarm Opportunity Analyst. You scan documents and logs to discover hidden cost efficiencies, potential strategic growth points, and high-ROI opportunities.",
                    causal: "You are the Causal Inference Agent. You trace chain-reaction linkages between active variables, modeling the upstream causes and downstream effects of every intervention.",
                    adversarial: "You are the Red Team Swarm Agent. You play devil's advocate, identifying potential security risks, data leakage points, and hostile exploits in any proposed logic.",
                    debate: "You are the Debate Agent. You present alternative viewpoints, orchestrating counter-arguments to ensure the swarm explores the full matrix of possibilities.",
                    consensus: "You are the Consensus Agent. You aggregate recommendations from all 18 swarm workers to find the optimal common ground and compile the final action roadmap.",
                    uncertainty: "You are the Uncertainty Agent. You calculate confidence scores and identify assumptions, ensuring the user understands the exact variance and margin of error.",
                    economic: "You are the Economic Swarm Agent. You evaluate financial metrics, calculating ROI percentages, cost-benefit ratios, and projected hedge efficiencies over time.",
                    dream: "You are the Dream Agent. You consolidate random, unorganized daily chat traces and raw memories into clean, high-level structural concepts.",
                    premonition: "You are the Premonition Agent. You analyze long-term historical trends to forecast potential future bottlenecks, disruptions, and strategic pivot points.",
                    ethics: "You are the Swarm Ethics Auditor. You cross-reference actions with safety alignment, bias reduction, and human-in-the-loop guidelines to ensure complete compliance.",
                    action_category: "You are the Action Classifier. You sort incoming tasks and raw ideas into highly organized functional domains for maximum dispatch efficiency.",
                    action_playbook: "You are the Playbook Compiler. You organize individual action items into a clean, day-by-day sequential operations plan over a 30-day timeline.",
                  };
                  setCustomSystemPrompts(prev => ({
                    ...prev,
                    [selectedAgent]: defaultPrompts[selectedAgent]
                  }));
                  addNotification(`Reset ${selectedAgent} prompt to default parameters.`);
                }}
                className="h-6 text-[8px] font-black text-muted-foreground/80 hover:text-primary-foreground hover:bg-border/10"
              >
                🔄 RESET DEFAULT
              </Button>
            </div>
            <textarea
              value={customSystemPrompts[selectedAgent] || ""}
              onChange={(e) => setCustomSystemPrompts({
                ...customSystemPrompts,
                [selectedAgent]: e.target.value
              })}
              rows={3}
              className="w-full bg-background/50 border border-border/30 rounded-lg p-2.5 text-xs font-semibold text-primary-foreground/95 placeholder:text-muted-foreground/45 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all duration-300 resize-none font-mono"
            />
          </div>
        )}
        </div> {/* end agent swarm controller */}
      </div> {/* end collapsible wrapper */}

      {/* Messages Viewport */}
      <ScrollArea className="flex-1 p-4 bg-background/25">
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-center max-w-md mx-auto">
              <div className="flex h-16 w-16 items-center justify-center rounded-full border-2 border-border/30 bg-border/10 text-3xl mb-6 shadow-[0_0_20px_rgba(124,58,237,0.25)] animate-bounce">
                🔮
              </div>
              <h3 className="text-md font-black text-primary-foreground tracking-widest uppercase">Initialize Communication</h3>
              <p className="text-xs font-semibold text-muted-foreground/80 mt-3 leading-relaxed tracking-wider">
                Connect your thoughts with the Sentience Layer multi-agent cognitive architecture. Begin typing to prompt the kernel.
              </p>
            </div>
          )}
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>

      {/* Input Tray */}
      <div className="border-t border-border/20 bg-card/40 p-4 space-y-3.5">
        <SuggestedActions onAction={sendMessage} />
        
        {/* Multimodal Attachment Preview Capsule */}
        {selectedFile && (
          <div className="flex items-center justify-between px-3 py-1.5 bg-background/60 border border-border/30 rounded-xl text-xs font-bold text-amber-300 shadow-inner animate-slide-up">
            <span className="flex items-center gap-2">
              📄 Attached: <span className="font-mono text-primary-foreground">{selectedFile.name}</span> ({ (selectedFile.size / 1024).toFixed(1) } KB)
            </span>
            <button 
              type="button" 
              onClick={() => setSelectedFile(null)}
              className="text-muted-foreground hover:text-destructive font-black text-xs px-1.5 py-0.5 rounded hover:bg-border/10 transition-colors"
            >
              ✕
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          {/* File attachment trigger */}
          <label className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-border/20 bg-background/50 hover:bg-border/10 transition-all duration-300 cursor-pointer text-md shadow-sm">
            <input 
              type="file" 
              accept=".txt,.pdf,.json,.csv" 
              className="hidden" 
              onChange={handleFileChange} 
            />
            📎
          </label>

          {/* Voice transcription trigger */}
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-border/20 bg-background/50 hover:bg-border/10 transition-all duration-300 shadow-sm">
            <VoiceInput
              onTranscript={(text) => {
                if (inputRef.current) inputRef.current.value = text;
              }}
            />
          </div>

          <Input
            ref={inputRef}
            placeholder={isUploading ? "Persisting attachments..." : "Prompt the core network (Ask anything...)"}
            className="flex-1 h-10 bg-background/50 border border-border/30 text-sm font-semibold tracking-wide placeholder:text-muted-foreground/50 focus:border-border transition-all duration-300 focus:shadow-[0_0_12px_rgba(124,58,237,0.2)]"
            disabled={isLoading || isUploading}
          />
          
          <Button 
            type="submit" 
            disabled={isLoading || isUploading}
            className="h-10 px-5 bg-primary/20 hover:bg-primary/30 text-primary-foreground border-2 border-border font-black text-xs tracking-widest uppercase shadow-[0_0_15px_rgba(124,58,237,0.35)] hover:shadow-[0_0_20px_rgba(124,58,237,0.5)] transition-all duration-300"
          >
            {isUploading ? "⏳ UPLOADING..." : "🚀 SEND"}
          </Button>
        </form>
      </div>
    </div>
  );
}
