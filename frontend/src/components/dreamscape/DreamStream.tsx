"use client";

import React, { useEffect, useRef, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

interface DreamNode {
  id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  alpha: number;
  title: string;
  category: string;
  schema: string;
  impact: number;
  isCollapsing?: boolean;
}

export function DreamStream({ onConsolidated }: { onConsolidated?: () => void }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [selectedNode, setSelectedNode] = useState<DreamNode | null>(null);
  const [consolidatedCount, setConsolidatedCount] = useState(148);
  const [isConsolidating, setIsConsolidating] = useState(false);
  const nodesRef = useRef<DreamNode[]>([]);

  // Function to fetch live memory nodes and initialize canvas particles
  const loadMemories = async (width: number, height: number) => {
    try {
      let data = await api.getMemory();
      if (!data || data.length === 0) {
        // Seeding some fallback traces if none exist
        data = [
          {
            id: "mem_chat_1",
            content: "Checkout conversion query analysis: Correlation identified between Postgres connection pools and active cart drop-off thresholds.",
            tags: ["postgres", "checkout"]
          },
          {
            id: "mem_action_1",
            content: "Optimized Postgres checkout index wrappers and scaled connection pool limits from 14% to 92% impact.",
            tags: ["action", "optimization"]
          },
          {
            id: "mem_doubt_1",
            content: "SQLite quarantine check: Transaction drift loop anomaly successfully detected and contained in Doubt Room sandbox.",
            tags: ["security", "sandbox"]
          },
          {
            id: "mem_vault_1",
            content: "Uploaded diagnostic trace: trace_a7b8e.txt containing multi-agent critical path trace data.",
            tags: ["vault", "telemetry"]
          }
        ];
      }

      const newNodes: DreamNode[] = data.map((m: any) => {
        const title = m.content.includes(":") ? m.content.split(":")[0] : m.content.slice(0, 32);
        const category = m.tags && m.tags[0] ? m.tags[0].toUpperCase() : "TRACE";
        return {
          id: m.id,
          x: Math.random() * (width - 40) + 20,
          y: Math.random() * (height - 40) + 20,
          vx: (Math.random() - 0.5) * 0.6,
          vy: (Math.random() - 0.5) * 0.6,
          radius: Math.random() * 5 + 6,
          alpha: Math.random() * 0.4 + 0.5,
          title: title,
          category: category,
          schema: m.content,
          impact: Math.floor(Math.random() * 15) + 83
        };
      });
      nodesRef.current = newNodes;
    } catch (err) {
      console.error("Failed to load memory nodes for DreamStream:", err);
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || 500);
    let height = (canvas.height = 300);

    const handleResize = () => {
      if (canvas) {
        width = canvas.width = canvas.parentElement?.clientWidth || 500;
        height = canvas.height = 300;
      }
    };
    window.addEventListener("resize", handleResize);

    loadMemories(width, height);

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Cosmic dark gradient background
      const bgGrad = ctx.createRadialGradient(width / 2, height / 2, 10, width / 2, height / 2, width);
      bgGrad.addColorStop(0, "#090615");
      bgGrad.addColorStop(1, "#030206");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Draw connection lines
      ctx.strokeStyle = "rgba(139, 92, 246, 0.08)";
      ctx.lineWidth = 1;
      const nodes = nodesRef.current;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          if (nodes[i].isCollapsing || nodes[j].isCollapsing) continue;
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
          }
        }
      }

      // Update and draw nodes
      nodesRef.current = nodes.filter((node) => {
        if (node.isCollapsing) {
          // Implosion physics: pull particle towards canvas center
          const dx = width / 2 - node.x;
          const dy = height / 2 - node.y;
          node.x += dx * 0.08;
          node.y += dy * 0.08;
          node.radius -= 0.35;
          if (node.radius <= 0.5) {
            return false; // remove node from drawing loop
          }
        } else {
          node.x += node.vx;
          node.y += node.vy;

          if (node.x < 10 || node.x > width - 10) node.vx *= -1;
          if (node.y < 10 || node.y > height - 10) node.vy *= -1;
        }

        ctx.shadowBlur = node.isCollapsing ? 24 : 12;
        ctx.shadowColor = node.isCollapsing ? "rgba(236, 72, 153, 0.6)" : "rgba(167, 139, 250, 0.4)";
        ctx.beginPath();

        const grad = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, node.radius);
        if (node.isCollapsing) {
          grad.addColorStop(0, "rgba(255, 255, 255, 1)");
          grad.addColorStop(0.5, "rgba(236, 72, 153, 0.9)");
          grad.addColorStop(1, "rgba(219, 39, 119, 0)");
        } else {
          grad.addColorStop(0, "rgba(255, 255, 255, 0.9)");
          grad.addColorStop(0.4, "rgba(167, 139, 250, 0.8)");
          grad.addColorStop(1, "rgba(139, 92, 246, 0)");
        }

        ctx.fillStyle = grad;
        ctx.arc(node.x, node.y, node.radius * 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
        return true;
      });

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    const handleCanvasClick = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      let found: DreamNode | null = null;
      nodesRef.current.forEach((node) => {
        if (node.isCollapsing) return;
        const dx = node.x - clickX;
        const dy = node.y - clickY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 25) {
          found = node;
        }
      });

      if (found) {
        setSelectedNode(found);
      }
    };

    canvas.addEventListener("click", handleCanvasClick);

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
      if (canvas) {
        canvas.removeEventListener("click", handleCanvasClick);
      }
    };
  }, []);

  const triggerConsolidation = async () => {
    if (!selectedNode || isConsolidating) return;
    setIsConsolidating(true);

    try {
      // Trigger API consolidation route
      await api.consolidateMemory(selectedNode.id, selectedNode.schema);

      // Trigger collapsing flag for canvas simulation
      const currentNodes = nodesRef.current;
      const nodeIndex = currentNodes.findIndex((n) => n.id === selectedNode.id);
      if (nodeIndex !== -1) {
        currentNodes[nodeIndex].isCollapsing = true;
      }

      setTimeout(() => {
        setConsolidatedCount((prev) => prev + 1);
        setIsConsolidating(false);
        setSelectedNode(null);
        if (onConsolidated) {
          onConsolidated();
        }
      }, 1200);
    } catch (err) {
      console.error("Memory consolidation failed:", err);
      setIsConsolidating(false);
    }
  };

  return (
    <Card className="border-2 border-border/40 bg-card shadow-[0_4px_30px_rgba(0,0,0,0.65)] overflow-hidden">
      <CardHeader className="border-b border-border/10 bg-card/40 p-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-sm font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            🔮 Cognitive Dream Stream
          </CardTitle>
          <p className="text-[10px] text-muted-foreground/80 uppercase tracking-wider mt-1">
            Visualizing background neural consolidation and offline trace alignment
          </p>
        </div>
        <Badge className="bg-primary/20 border border-primary/30 text-primary font-mono text-[9px] px-2.5 py-0.5">
          {consolidatedCount} CONSOLIDATED
        </Badge>
      </CardHeader>
      <CardContent className="p-0 relative grid grid-cols-1 md:grid-cols-3">
        {/* Canvas Visualizer */}
        <div className="md:col-span-2 border-r border-border/10 relative h-[300px]">
          <canvas ref={canvasRef} className="block w-full h-full cursor-pointer" />
          <div className="absolute bottom-3 left-3 bg-[#030206]/80 px-2.5 py-1 rounded-md border border-border/10 pointer-events-none">
            <span className="text-[9px] font-mono text-muted-foreground/60 uppercase">
              🖱️ Click glowing nodes to inspect cognitive schemas
            </span>
          </div>
        </div>

        {/* Selected Dream Trace Panel */}
        <div className="p-4 bg-[#030207] flex flex-col justify-between h-[300px]">
          {selectedNode ? (
            <div className="space-y-3 flex-1 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge className="bg-violet-950/40 border border-violet-500/30 text-violet-400 font-black text-[8px] tracking-widest uppercase">
                    {selectedNode.category} TRACE
                  </Badge>
                  <span className="text-[10px] font-black text-amber-300">
                    🔥 Impact: {selectedNode.impact}%
                  </span>
                </div>
                <h4 className="text-xs font-black text-primary-foreground tracking-wide line-clamp-2">
                  {selectedNode.title}
                </h4>
                <div className="space-y-1">
                  <span className="text-[9px] font-black text-muted-foreground/50 uppercase tracking-widest block">Proposed Mutation</span>
                  <div className="text-[9px] font-mono text-primary-foreground bg-[#0a0711] p-2.5 rounded-lg border border-border/10 overflow-y-auto max-h-[100px] whitespace-pre-wrap break-all leading-normal">
                    {selectedNode.schema}
                  </div>
                </div>
              </div>
              <Button
                size="sm"
                onClick={triggerConsolidation}
                disabled={isConsolidating || selectedNode.isCollapsing}
                className="w-full text-[9px] font-black tracking-widest uppercase rounded-lg h-8 bg-violet-600 hover:bg-violet-700 text-white shadow-[0_0_15px_rgba(124,58,237,0.4)]"
              >
                {isConsolidating ? "⚡ VAULT INTEGRATION..." : "✓ CONSOLIDATE MEMORY"}
              </Button>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center max-w-[200px] mx-auto text-muted-foreground">
              <span className="text-3xl mb-2 animate-bounce">🔮</span>
              <h5 className="text-[11px] font-black text-primary-foreground uppercase tracking-widest">Trace Analyzer</h5>
              <p className="text-[9px] leading-relaxed mt-2">
                Click any floating memory particle inside the cosmic dream canvas to analyze it.
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
