"use client";

import { useRef, useEffect } from "react";
import { useChat } from "@/hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedActions } from "./SuggestedActions";
import { VoiceInput } from "./VoiceInput";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

export function ChatInterface() {
  const { messages, isLoading, sendMessage, clearChat } = useChat();
  const inputRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const content = inputRef.current?.value.trim();
    if (!content || isLoading) return;
    sendMessage(content);
    inputRef.current!.value = "";
  };

  return (
    <div className="flex h-full min-h-[75vh] flex-col rounded-xl border-2 border-border/50 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.8)] overflow-hidden">
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
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={clearChat}
          className="border border-border/20 text-[10px] font-black tracking-widest hover:bg-destructive/20 hover:text-destructive hover:border-destructive/30 transition-all duration-300 py-1"
        >
          🧹 CLEAR CHAT
        </Button>
      </div>

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
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-border/20 bg-background/50 hover:bg-border/10 transition-all duration-300">
            <VoiceInput
              onTranscript={(text) => {
                if (inputRef.current) inputRef.current.value = text;
              }}
            />
          </div>
          <Input
            ref={inputRef}
            placeholder="Prompt the core network (Ask anything...)"
            className="flex-1 h-10 bg-background/50 border border-border/30 text-sm font-semibold tracking-wide placeholder:text-muted-foreground/50 focus:border-border transition-all duration-300 focus:shadow-[0_0_12px_rgba(124,58,237,0.2)]"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            disabled={isLoading}
            className="h-10 px-5 bg-primary/20 hover:bg-primary/30 text-primary-foreground border-2 border-border font-black text-xs tracking-widest uppercase shadow-[0_0_15px_rgba(124,58,237,0.35)] hover:shadow-[0_0_20px_rgba(124,58,237,0.5)] transition-all duration-300"
          >
            🚀 SEND
          </Button>
        </form>
      </div>
    </div>
  );
}
