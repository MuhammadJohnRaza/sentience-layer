/**
 * Hook for real-time agent trace monitoring
 */

import { useState, useEffect, useCallback } from "react";
import { AgentTrace } from "@/types";
import { api } from "@/lib/api";
import { wsClient } from "@/lib/websocket";

export function useAgentTraces() {
  const [traces, setTraces] = useState<AgentTrace[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Initial load
    api.getAgentTraces().then((data) => {
      setTraces(data);
      setIsLoading(false);
    });

    // Real-time updates
    const unsubscribe = wsClient.on("agent_update", (payload) => {
      setTraces((prev) => {
        const existing = prev.findIndex((t) => t.id === payload.id);
        if (existing >= 0) {
          const updated = [...prev];
          updated[existing] = { ...updated[existing], ...payload };
          return updated;
        }
        return [payload, ...prev].slice(0, 50);
      });
    });

    return unsubscribe;
  }, []);

  const getTraceById = useCallback(
    (id: string) => {
      return traces.find((t) => t.id === id);
    },
    [traces],
  );

  return { traces, isLoading, getTraceById };
}
