/**
 * Chat Hook with streaming support
 */

import { useState, useCallback, useRef } from "react";
import { Message } from "@/types";
import { api } from "@/lib/api";
import { generateId } from "@/lib/utils";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (content: string) => {
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
      
      const response = await api.sendMessage(content, {
        history: messages.slice(-10),
      });

      const assistantMsg: Message = {
        id: generateId(),
        role: "assistant",
        content: response.content || "I processed your request.",
        timestamp: new Date().toISOString(),
        metadata: {
          intent: response.intent,
          confidence: response.confidence,
          sources: response.sources,
          actions: response.suggested_actions,
        },
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
  }, [messages]);

  const clearChat = useCallback(() => {
    abortRef.current?.abort();
    setMessages([]);
  }, []);

  return { messages, isLoading, sendMessage, clearChat };
}