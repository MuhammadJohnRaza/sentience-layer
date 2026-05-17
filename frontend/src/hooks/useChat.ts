/** * Chat Hook with streaming support */
import { useState, useCallback, useRef } from "react";
import { Message } from "@/types";
import { api } from "@/lib/api";
import { generateId } from "@/lib/utils";
import { useStore } from "@/store/useStore";
export function useChat() {
  const messages = useStore((state) => state.chatMessages);
  const isLoading = useStore((state) => state.isChatLoading);
  const setMessages = useStore((state) => state.setChatMessages);
  const setIsLoading = useStore((state) => state.setChatLoading);
  const abortRef = useRef<AbortController | null>(null);
  const sendMessage = useCallback(
    async (content: string, customContext?: any) => {
      const userMsg: Message = {
        id: generateId(),
        role: "user",
        content,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);
      try {
        abortRef.current = new AbortController();
        const response = (await api.sendMessage(content, {
          history: messages.slice(-10),
          ...customContext,
        })) as any;
        const assistantMsg: Message = {
          id: generateId(),
          role: "assistant",
          content: response.content || "I processed your request.",
          timestamp: new Date().toISOString(),
          metadata: {
            intent: response.intent,
            confidence: response.confidence,
            severity: response.severity,
            evidence: response.evidence,
            actions: response.actions,
            agentChain: response.agent_chain,
            keyFinding: response.key_finding,
            priority: response.priority,
            totalDurationMs: response.total_duration_ms,
            agentUsed: response.agent_used,
            sources: response.sources,
          } as any,
        };
        setMessages((prev) => [...prev, assistantMsg]);
        return assistantMsg;
      } catch (error) {
        const errorMsg: Message = {
          id: generateId(),
          role: "system",
          content: "Sorry, I encountered an error processing your message.",
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMsg]);
        throw error;
      } finally {
        setIsLoading(false);
        abortRef.current = null;
      }
    },
    [messages],
  );
  const clearChat = useCallback(() => {
    abortRef.current?.abort();
    setMessages([]);
  }, []);
  return {
    messages,
    isLoading,
    sendMessage,
    clearChat,
  };
}
