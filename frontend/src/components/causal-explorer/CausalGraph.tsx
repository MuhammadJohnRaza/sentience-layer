/** * Causal Graph Visualization */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { api } from "@/lib/api";
import { CausalNode, CausalEdge } from "@/types";
export function CausalGraph() {
  const [nodes, setNodes] = useState<CausalNode[]>([]);
  const [edges, setEdges] = useState<CausalEdge[]>([]);
  useEffect(() => {
    api.getCausalGraph().then((data: any) => {
      setNodes(data.nodes || []);
      setEdges(data.edges || []);
    });
  }, []);
  return (
    <Card className="h-[600px]">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Causal Graph</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="relative h-full">
        {" "}
        <svg className="absolute inset-0 h-full w-full">
          {" "}
          {/* Edges */}
          {edges.map((edge, i) => {
            const source = nodes.find((n) => n.id === edge.source);
            const target = nodes.find((n) => n.id === edge.target);
            if (!source || !target) return null;
            return (
              <line
                key={i}
                x1={`${(source.x || 0) * 100}%`}
                y1={`${(source.y || 0) * 100}%`}
                x2={`${(target.x || 0) * 100}%`}
                y2={`${(target.y || 0) * 100}%`}
                stroke={edge.confidence > 0.7 ? "#0f172a" : "#94a3b8"}
                strokeWidth={Math.abs(edge.effectSize) * 3}
                markerEnd="url(#arrowhead)"
              />
            );
          })}
          {/* Nodes */}
          {nodes.map((node) => (
            <g key={node.id}>
              {" "}
              <circle
                cx={`${(node.x || 0.5) * 100}%`}
                cy={`${(node.y || 0.5) * 100}%`}
                r="20"
                fill={node.type === "intervention" ? "#ef4444" : "#3b82f6"}
                stroke="white"
                strokeWidth="2"
              />{" "}
              <text
                x={`${(node.x || 0.5) * 100}%`}
                y={`${(node.y || 0.5) * 100 + 5}%`}
                textAnchor="middle"
                className="text-xs font-medium fill-slate-900 dark:fill-slate-50"
              >
                {" "}
                {node.label}
              </text>{" "}
            </g>
          ))}
          <defs>
            {" "}
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              {" "}
              <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />{" "}
            </marker>{" "}
          </defs>{" "}
        </svg>{" "}
      </CardContent>{" "}
    </Card>
  );
}
