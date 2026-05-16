/**
 * Main Chat Interface — Black / Purple / Gold Theme
 */

"use client";

import { useRef, useEffect, useState, KeyboardEvent } from "react";
import { useChat } from "@/hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedActions } from "./SuggestedActions";

export function ChatInterface() {
  const { messages, isLoading, sendMessage, clearChat } = useChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Auto-grow textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [input]);

  const handleSubmit = () => {
    const content = input.trim();
    if (!content || isLoading) return;
    sendMessage(content);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex h-full flex-col bg-black" style={{ minHeight: "calc(100vh - 4rem)" }}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-4 bg-black/90 backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-3">
          {/* AI brain icon */}
          <div className="relative h-9 w-9 rounded-full bg-purple-900/40 border border-[#EAB308]/60 flex items-center justify-center">
            <div className="h-2.5 w-2.5 rounded-full bg-[#EAB308] animate-pulse" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-[#EAB308] tracking-wide uppercase">Sentience Chat</h2>
            <p className="text-[11px] text-[#A855F7]/70">Multi-agent cognitive reasoning engine</p>
          </div>
        </div>
        <button
          onClick={clearChat}
          className="text-xs text-zinc-500 hover:text-[#EAB308] transition-colors px-3 py-1.5 rounded-lg border border-zinc-800 hover:border-[#EAB308]/40"
        >
          Clear Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 space-y-6 scrollbar-thin scrollbar-track-black scrollbar-thumb-zinc-800">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full py-24 text-center space-y-6">
            {/* Pulsing orb */}
            <div className="relative">
              <div className="h-20 w-20 rounded-full bg-purple-900/20 border border-[#EAB308]/20 flex items-center justify-center">
                <div className="h-10 w-10 rounded-full bg-purple-900/40 border border-[#EAB308]/40 flex items-center justify-center">
                  <div className="h-4 w-4 rounded-full bg-[#EAB308] animate-pulse" />
                </div>
              </div>
              <div className="absolute inset-0 rounded-full bg-[#EAB308]/5 animate-ping" />
            </div>
            <div>
              <p className="text-[#EAB308] font-semibold text-lg">Sentience is ready</p>
              <p className="text-[#A855F7]/60 text-sm mt-1 max-w-xs">
                Ask anything — I'll reason through it using 18 specialized cognitive agents.
              </p>
            </div>
            <SuggestedActions onAction={(text) => { setInput(text); textareaRef.current?.focus(); }} />
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-zinc-800 px-4 md:px-8 py-4 bg-black/90 backdrop-blur-md">
        {messages.length > 0 && (
          <div className="mb-3">
            <SuggestedActions onAction={(text) => { setInput(text); textareaRef.current?.focus(); }} />
          </div>
        )}

        <div className="relative flex items-end gap-3 bg-zinc-900/60 border border-zinc-800 rounded-2xl px-4 py-3 focus-within:border-[#A855F7]/60 transition-colors">
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask the Sentience Layer anything... (Enter to send, Shift+Enter for newline)"
            disabled={isLoading}
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-slate-100 placeholder:text-zinc-600 focus:outline-none disabled:opacity-50 py-1"
            style={{ minHeight: "24px", maxHeight: "160px" }}
          />

          {/* Send button */}
          <button
            onClick={handleSubmit}
            disabled={isLoading || !input.trim()}
            className="flex-shrink-0 h-9 w-9 rounded-xl bg-[#EAB308] text-black flex items-center justify-center hover:bg-[#EAB308]/90 disabled:opacity-30 disabled:cursor-not-allowed transition-all shadow-[0_0_12px_rgba(234,179,8,0.3)] hover:shadow-[0_0_20px_rgba(234,179,8,0.5)]"
          >
            {isLoading ? (
              <span className="h-3.5 w-3.5 rounded-full border-2 border-black border-t-transparent animate-spin" />
            ) : (
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
              </svg>
            )}
          </button>
        </div>

        <p className="text-[10px] text-zinc-700 mt-2 text-center">
          Powered by Sentience v4.0 · Multi-step agentic reasoning · Enter to send
        </p>
      </div>
    </div>
  );
}