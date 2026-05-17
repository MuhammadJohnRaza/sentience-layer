/**
 * Neo4j-Style Cognitive Memory Graph Visualization
 */
"use client";

import { useState, useMemo } from "react";
import { useMemory } from "@/hooks/useMemory";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function MemoryGraph() {
  const { nodes, selectedNode, setSelectedNode, searchMemory, isLoading } = useMemory();
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  // Map nodes to deterministic multi-layered coordinates (Concentric orbits like Neo4j Bloom)
  const nodePositions = useMemo(() => {
    return nodes.map((node, i) => {
      const angle = (i / Math.max(nodes.length, 1)) * 2 * Math.PI;
      // Vary distance based on index to create multiple concentric orbital rings
      const orbitRing = (i % 3); 
      const distance = 24 + orbitRing * 11; // 24%, 35%, 46% radius
      const x = 50 + Math.cos(angle) * distance;
      const y = 50 + Math.sin(angle) * distance;
      
      return {
        ...node,
        x,
        y,
      };
    });
  }, [nodes]);

  // Extract all active connecting lines (edges) in the graph
  const edges = useMemo(() => {
    const edgeList: Array<{ id: string; x1: number; y1: number; x2: number; y2: number; isActive: boolean; isDimmed: boolean }> = [];
    const positionMap = new Map(nodePositions.map(n => [n.id, n]));

    nodePositions.forEach(source => {
      if (source.connections && Array.isArray(source.connections)) {
        source.connections.forEach(targetId => {
          const target = positionMap.get(targetId);
          if (target) {
            // Determine active highlight state
            const isRelatedToHover = hoveredNodeId === source.id || hoveredNodeId === targetId;
            const isAnyHovered = hoveredNodeId !== null;

            edgeList.push({
              id: `${source.id}-${targetId}`,
              x1: source.x,
              y1: source.y,
              x2: target.x,
              y2: target.y,
              isActive: isRelatedToHover,
              isDimmed: isAnyHovered && !isRelatedToHover,
            });
          }
        });
      }
    });

    return edgeList;
  }, [nodePositions, hoveredNodeId]);

  // Filter or highlight matching search nodes
  const matchingNodeIds = useMemo(() => {
    if (!search) return new Set();
    const query = search.toLowerCase();
    return new Set(
      nodes
        .filter(n => n.content?.toLowerCase().includes(query) || n.type?.toLowerCase().includes(query))
        .map(n => n.id)
    );
  }, [nodes, search]);

  return (
    <Card className="h-[650px] border border-border/20 bg-card/25 shadow-[0_10px_35px_rgba(0,0,0,0.6)] backdrop-blur-md relative overflow-hidden flex flex-col justify-between">
      <CardHeader className="border-b border-border/10 pb-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <CardTitle className="text-lg font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
              🟢 NEO4J COGNITIVE INDEX
            </CardTitle>
            <CardDescription className="text-[10px] font-bold tracking-wider text-muted-foreground/80 uppercase">
              Relational Swarm Memory Network Explorer
            </CardDescription>
          </div>
          
          <div className="flex gap-2">
            <Input
              placeholder="Query memory tags..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-48 h-9 bg-background/50 border border-border/30 text-xs font-semibold placeholder:text-muted-foreground/50 focus:border-border transition-all duration-300 focus:shadow-[0_0_10px_rgba(16,185,129,0.2)]"
            />
            <Button 
              variant="outline"
              size="sm"
              onClick={() => { setSearch(""); searchMemory(""); }}
              className="h-9 border border-border/20 hover:bg-border/10 text-[10px] font-black tracking-widest uppercase rounded-lg px-3"
            >
              RESET
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="relative flex-1 bg-[#020207]/45 overflow-hidden p-0">
        {isLoading ? (
          <div className="h-full w-full flex items-center justify-center bg-card/10">
            <div className="flex flex-col items-center gap-3">
              <span className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
              <p className="text-[10px] font-black tracking-widest text-muted-foreground uppercase">Traversing database graph...</p>
            </div>
          </div>
        ) : (
          <div className="relative h-full w-full select-none">
            {/* SVG Connecting Edges Canvas */}
            <svg className="absolute inset-0 h-full w-full pointer-events-none z-0">
              <defs>
                <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.4" />
                </linearGradient>
              </defs>
              {edges.map((edge) => (
                <line
                  key={edge.id}
                  x1={`${edge.x1}%`}
                  y1={`${edge.y1}%`}
                  x2={`${edge.x2}%`}
                  y2={`${edge.y2}%`}
                  className={cn(
                    "transition-all duration-500",
                    edge.isActive
                      ? "stroke-amber-400 stroke-[2px] opacity-100 shadow-[0_0_8px_rgba(245,158,11,0.5)]"
                      : edge.isDimmed
                        ? "stroke-border/5 stroke-[0.5px] opacity-10"
                        : "stroke-primary/20 stroke-[1px] opacity-40"
                  )}
                  style={edge.isActive ? {} : { stroke: "url(#edgeGrad)" }}
                />
              ))}
            </svg>

            {/* Glowing Interactive Nodes */}
            {nodePositions.map((node) => {
              const isHovered = hoveredNodeId === node.id;
              const isAnyHovered = hoveredNodeId !== null;
              const isSelected = selectedNode?.id === node.id;
              const isSearchMatch = matchingNodeIds.has(node.id);
              const isDimmed = isAnyHovered && !isHovered && !(node.connections?.includes(hoveredNodeId || "") || nodePositions.find(n => n.id === hoveredNodeId)?.connections?.includes(node.id));

              return (
                <div
                  key={node.id}
                  className="absolute cursor-pointer z-10 transition-all duration-300"
                  style={{
                    left: `${node.x}%`,
                    top: `${node.y}%`,
                    transform: "translate(-50%, -50%)",
                  }}
                  onMouseEnter={() => setHoveredNodeId(node.id)}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  onClick={() => setSelectedNode(node)}
                >
                  <div
                    className={cn(
                      "h-14 w-14 rounded-full border-2 flex flex-col items-center justify-center text-[8px] font-black transition-all duration-300 relative shadow-2xl uppercase tracking-widest",
                      isSelected
                        ? "scale-110 border-amber-400 bg-amber-950/60 text-amber-200 ring-4 ring-amber-500/25 shadow-[0_0_20px_rgba(245,158,11,0.5)]"
                        : isHovered
                          ? "scale-115 border-primary bg-primary/20 text-primary-foreground shadow-[0_0_18px_rgba(124,58,237,0.45)]"
                          : isSearchMatch
                            ? "border-emerald-400 bg-emerald-950/40 text-emerald-300 ring-2 ring-emerald-400/20 shadow-[0_0_15px_rgba(52,211,153,0.4)] animate-pulse"
                            : isDimmed
                              ? "opacity-25 border-border/10 bg-card/5 text-muted-foreground/30 scale-95"
                              : node.type === "episodic"
                                ? "border-purple-500/40 bg-purple-950/20 text-purple-200 hover:border-purple-400"
                                : "border-indigo-500/40 bg-indigo-950/20 text-indigo-200 hover:border-indigo-400"
                    )}
                  >
                    {/* Node Mini Icon */}
                    <span className="text-xs mb-0.5">
                      {node.type === "episodic" ? "🔮" : "🧠"}
                    </span>
                    <span className="max-w-[42px] truncate px-1 text-center font-extrabold font-mono">
                      {node.content.slice(0, 5)}
                    </span>

                    {/* Active Connection Count Badge */}
                    {node.connections && node.connections.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-background border border-border/30 text-[7px] font-black text-amber-400 h-4 w-4 rounded-full flex items-center justify-center shadow-md">
                        {node.connections.length}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}

            {/* Floating Neo4j Node Inspector Card */}
            {selectedNode && (
              <Card className="absolute bottom-4 left-4 right-4 md:right-auto md:w-96 border border-border/30 bg-card/90 backdrop-blur-md p-4 shadow-[0_10px_35px_rgba(0,0,0,0.8)] z-20 animate-slide-up">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Badge className={cn(
                      "text-[8px] font-black tracking-widest uppercase px-2 py-0.5",
                      selectedNode.type === "episodic"
                        ? "bg-purple-950/50 border border-purple-500/30 text-purple-300"
                        : "bg-indigo-950/50 border border-indigo-500/30 text-indigo-300"
                    )}>
                      {selectedNode.type} Node
                    </Badge>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedNode(null)}
                      className="h-5 w-5 p-0 text-[10px] text-muted-foreground hover:text-foreground font-black hover:bg-border/10 rounded-full"
                    >
                      ✕
                    </Button>
                  </div>

                  <div className="space-y-1">
                    <p className="text-[8px] font-black tracking-widest text-muted-foreground uppercase font-mono">Node Content Payload</p>
                    <p className="text-xs font-semibold text-foreground tracking-wide leading-relaxed">
                      {selectedNode.content}
                    </p>
                  </div>

                  {/* Association strength progress bar */}
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-[8px] font-black tracking-widest text-muted-foreground uppercase font-mono">
                      <span>Weight Strength</span>
                      <span className="text-amber-400">{(selectedNode.strength * 100).toFixed(0)}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-background border border-border/20 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-primary to-amber-400 transition-all duration-500" 
                        style={{ width: `${selectedNode.strength * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-border/10 text-[8px] font-black tracking-widest text-muted-foreground uppercase font-mono">
                    <span>UUID: <span className="font-semibold font-mono text-primary-foreground">{selectedNode.id.slice(0, 8)}</span></span>
                    <span>Connections: <span className="font-semibold text-amber-400">{selectedNode.connections?.length || 0}</span></span>
                  </div>
                </div>
              </Card>
            )}

            {/* Orbit / Scale Legend */}
            <div className="absolute top-4 left-4 bg-background/60 border border-border/20 backdrop-blur rounded-lg p-2.5 space-y-1.5 z-20">
              <p className="text-[7px] font-black tracking-widest text-muted-foreground uppercase">Topology Legend</p>
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-1.5 text-[8px] font-bold text-purple-300">
                  <span className="h-2 w-2 rounded-full bg-purple-500/50 border border-purple-500" />
                  EPISODIC EVENTS
                </div>
                <div className="flex items-center gap-1.5 text-[8px] font-bold text-indigo-300">
                  <span className="h-2 w-2 rounded-full bg-indigo-500/50 border border-indigo-500" />
                  SEMANTIC ASSOCIATIONS
                </div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
