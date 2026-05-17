/** * Hook
for memory graph interaction */
import { useState, useEffect, useCallback } from "react";
import { MemoryNode } from "@/types";
import { api } from "@/lib/api";
export function useMemory() {
  const [nodes, setNodes] = useState<MemoryNode[]>([]);
  const [selectedNode, setSelectedNode] = useState<MemoryNode | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    api.getMemory().then((data: any) => {
      setNodes(data);
      setIsLoading(false);
    });
  }, []);
  const searchMemory = useCallback(async (query: string) => {
    setIsLoading(true);
    try {
      const results = (await api.searchMemory(query)) as any;
      setNodes(results);
    } finally {
      setIsLoading(false);
    }
  }, []);
  const getConnectedNodes = useCallback(
    (nodeId: string) => {
      const node = nodes.find((n) => n.id === nodeId);
      if (!node) return [];
      return nodes.filter((n) => node.connections.includes(n.id));
    },
    [nodes],
  );
  return {
    nodes,
    selectedNode,
    setSelectedNode,
    isLoading,
    searchMemory,
    getConnectedNodes,
  };
}
