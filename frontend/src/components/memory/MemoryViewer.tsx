/** * Memory Node Viewer */ "use client";
import { useMemory } from "@/hooks/useMemory";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { formatRelativeTime } from "@/lib/utils";
export function MemoryViewer() {
  const { nodes, selectedNode } = useMemory();
  return (
    <Card className="h-[600px]">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Memory Nodes</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <ScrollArea className="h-[500px]">
          {" "}
          <div className="space-y-2">
            {" "}
            {nodes.map((node) => (
              <div
                key={node.id}
                className={cn(
                  "rounded-lg border p-3 cursor-pointer transition-colors",
                  selectedNode?.id === node.id
                    ? "border-slate-900 bg-background dark:border-slate-50 dark:bg-card"
                    : "hover:bg-background dark:hover:bg-card",
                )}
              >
                {" "}
                <div className="flex items-center justify-between mb-1">
                  {" "}
                  <Badge
                    variant={
                      node.type === "episodic"
                        ? "default"
                        : node.type === "semantic"
                          ? "secondary"
                          : "outline"
                    }
                    className="text-xs"
                  >
                    {" "}
                    {node.type}
                  </Badge>{" "}
                  <span className="text-xs text-muted-foreground">
                    {formatRelativeTime(node.timestamp)}
                  </span>{" "}
                </div>{" "}
                <p className="text-sm">{node.content}</p>{" "}
                <div className="mt-2 flex gap-1">
                  {" "}
                  {node.connections.slice(0, 3).map((c) => (
                    <span
                      key={c}
                      className="text-[10px] bg-border/10 px-1.5 py-0.5 rounded dark:bg-border/30"
                    >
                      {" "}
                      {c.slice(0, 6)}...{" "}
                    </span>
                  ))}
                </div>{" "}
              </div>
            ))}
          </div>{" "}
        </ScrollArea>{" "}
      </CardContent>{" "}
    </Card>
  );
}
import { cn } from "@/lib/utils";
