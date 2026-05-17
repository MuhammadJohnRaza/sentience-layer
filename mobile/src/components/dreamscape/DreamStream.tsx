"use client";

import React, { useEffect, useRef, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface DreamNode {
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
}

const MEMORY_TRACES = [
  { title: "Postgres Schema Alignment", category: "MCP", schema: "ALTER TABLE trace ADD COLUMN alignment_vector DOUBLE PRECISION[]", impact: 94 },
  { title: "Vector Index Consolidation", category: "Memory", schema: "CREATE INDEX ON memory USING ivfflat (vector cosine_ops)", impact: 91 },
  { title: "Consensus Node Synchronization", category: "Swarm", schema: "UPDATE nodes SET consensus_status = 'aligned' WHERE latency < 20", impact: 88 },
  { title: "Adversarial Stress Verification", category: "Quarantine", schema: "SELECT verify_containment_vault('agent_doubt_trace_4')", impact: 97 },
  { title: "Economic Cost Hedging", category: "Tokenomics", schema: "SELECT compute_roi_bounds(245.0, 0.95)", impact: 85 }
];

export function DreamStream() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [selectedNode, setSelectedNode] = useState<DreamNode | null>(null);
  const [consolidatedCount, setConsolidatedCount] = useState(148);
  const [isConsolidating, setIsConsolidating] = useState(false);
  const nodesRef = useRef<DreamNode[]>([]);

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

    // Initialize interactive neural particles
    const initNodes = () => {
      const newNodes: DreamNode[] = [];
      for (let i = 0; i < 15; i++) {
        const trace = MEMORY_TRACES[i % MEMORY_TRACES.length];
        newNodes.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.8,
          vy: (Math.random() - 0.5) * 0.8,
          radius: Math.random() * 8 + 4,
          alpha: Math.random() * 0.5 + 0.4,
          title: trace.title,
          category: trace.category,
          schema: trace.schema,
          impact: trace.impact
        });
      }
      nodesRef.current = newNodes;
    };

    initNodes();

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Create a gorgeous glowing cosmic background gradient
      const bgGrad = ctx.createRadialGradient(width / 2, height / 2, 10, width / 2, height / 2, width);
      bgGrad.addColorStop(0, "#080612");
      bgGrad.addColorStop(1, "#030206");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Draw connection links (neural net effect)
      ctx.strokeStyle = "rgba(139, 92, 246, 0.08)";
      ctx.lineWidth = 1;
      const nodes = nodesRef.current;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
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

      // Draw and update particles
      nodes.forEach((node) => {
        // Move particle
        node.x += node.vx;
        node.y += node.vy;

        // Bounce on borders
        if (node.x < 0 || node.x > width) node.vx *= -1;
        if (node.y < 0 || node.y > height) node.vy *= -1;

        // Draw glowing particle
        ctx.shadowBlur = 12;
        ctx.shadowColor = "rgba(167, 139, 250, 0.4)";
        ctx.beginPath();
        
        const grad = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, node.radius);
        grad.addColorStop(0, "rgba(255, 255, 255, 0.9)");
        grad.addColorStop(0.4, "rgba(167, 139, 250, 0.8)");
        grad.addColorStop(1, "rgba(139, 92, 246, 0)");
        
        ctx.fillStyle = grad;
        ctx.arc(node.x, node.y, node.radius * 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0; // reset
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

  const triggerConsolidation = () => {
    if (!selectedNode) return;
    setIsConsolidating(true);
    setTimeout(() => {
      setConsolidatedCount((prev) => prev + 1);
      setIsConsolidating(false);
      setSelectedNode(null);
    }, 1500);
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
                <h4 className="text-xs font-black text-primary-foreground tracking-wide">
                  {selectedNode.title}
                </h4>
                <div className="space-y-1">
                  <span className="text-[9px] font-black text-muted-foreground/50 uppercase tracking-widest block">Proposed Mutation</span>
                  <pre className="text-[9px] font-mono text-primary-foreground bg-[#0a0711] p-2.5 rounded-lg border border-border/10 overflow-x-auto leading-relaxed max-h-[110px]">
                    {selectedNode.schema}
                  </pre>
                </div>
              </div>
              <Button
                size="sm"
                onClick={triggerConsolidation}
                disabled={isConsolidating}
                className="w-full text-[9px] font-black tracking-widest uppercase rounded-lg h-8 bg-violet-600 hover:bg-violet-700 text-white shadow-[0_0_15px_rgba(124,58,237,0.4)]"
              >
                {isConsolidating ? "⚡ INTEGRATING TO VAULT..." : "✓ CONSOLIDATE MEMORY"}
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
