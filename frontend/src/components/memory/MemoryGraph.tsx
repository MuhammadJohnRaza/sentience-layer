/** * Memory Graph Visualization */ "use client";
import { useMemory } from "@/hooks/useMemory";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
export function MemoryGraph() {
  const { nodes, selectedNode, setSelectedNode, searchMemory, isLoading } =
    useMemory();
  return (
    <Card className="h-[600px]">
      {" "}
      <CardHeader>
        {" "}
        <div className="flex items-center justify-between">
          {" "}
          <CardTitle>Memory Graph</CardTitle>{" "}
          <div className="flex gap-2">
            {" "}
            <Input
              placeholder="Search memory..."
              className="w-48"
              onChange={(e) => searchMemory(e.target.value)}
            />{" "}
          </div>{" "}
        </div>{" "}
      </CardHeader>{" "}
      <CardContent className="relative h-full">
        {" "}
        {isLoading ? (
          <div className="h-full animate-pulse bg-border/10 rounded" />
        ) : (
          <div className="relative h-full overflow-hidden">
            {" "}
            {/* Simplified force-directed visualization */}
            {nodes.map((node, i) => {
              const angle = (i / Math.max(nodes.length, 1)) * 2 * Math.PI;
              const radius = 200;
              const x = 50 + Math.cos(angle) * 40;
              const y = 50 + Math.sin(angle) * 40;
              return (
                <div
                  key={node.id}
                  className="absolute cursor-pointer transition-all hover:scale-110"
                  style={{
                    left: `${x}%`,
                    top: `${y}%`,
                    transform: "translate(-50%, -50%)",
                  }}
                  onClick={() => setSelectedNode(node)}
                >
                  {" "}
                  <div
                    className={cn(
                      "h-16 w-16 rounded-full flex items-center justify-center text-xs font-medium text-white shadow-lg",
                      node.type === "episodic"
                        ? "bg-purple-500"
                        : node.type === "semantic"
                          ? "bg-primary"
                          : "bg-primary",
                    )}
                  >
                    {" "}
                    {node.content.slice(0, 10)}...{" "}
                  </div>{" "}
                </div>
              );
            })}
            {/* Selected node info */}
            {selectedNode && (
              <div className="absolute bottom-4 left-4 right-4 rounded-lg border bg-white/90 p-4 backdrop-blur dark:bg-background/90">
                {" "}
                <p className="font-medium">{selectedNode.content}</p>{" "}
                <p className="text-xs text-foreground0 mt-1">
                  {" "}
                  Type: {selectedNode.type}• Strength:{" "}
                  {(selectedNode.strength * 100).toFixed(0)}% • Connections:{" "}
                  {selectedNode.connections.length}
                </p>{" "}
              </div>
            )}
          </div>
        )}
      </CardContent>{" "}
    </Card>
  );
}
import { cn } from "@/lib/utils";
