/** * Agent Trace Viewer */ "use client";
import { useAgentTraces } from "@/hooks/useAgentTraces";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { TraceTimeline } from "./TraceTimeline";
import { ReasoningChain } from "./ReasoningChain";
import { DecisionTree } from "./DecisionTree";
export function AgentTraceViewer() {
  const { traces, isLoading } = useAgentTraces();
  if (isLoading) {
    return <div className="h-96 animate-pulse bg-border/10 rounded-lg" />;
  }
  return (
    <div className="space-y-4">
      {" "}
      {traces.map((trace) => (
        <Card key={trace.id}>
          {" "}
          <CardHeader>
            {" "}
            <div className="flex items-center justify-between">
              {" "}
              <div>
                {" "}
                <CardTitle className="text-lg">
                  {trace.agentName}
                </CardTitle>{" "}
                <p className="text-xs text-foreground0">
                  {trace.agentType}•{" "}
                  {new Date(trace.startTime).toLocaleString()}
                </p>{" "}
              </div>{" "}
              <Badge
                variant={
                  trace.status === "success"
                    ? "default"
                    : trace.status === "error"
                      ? "destructive"
                      : trace.status === "running"
                        ? "secondary"
                        : "outline"
                }
              >
                {" "}
                {trace.status}
              </Badge>{" "}
            </div>{" "}
          </CardHeader>{" "}
          <CardContent>
            {" "}
            <Tabs defaultValue="timeline">
              {" "}
              <TabsList>
                {" "}
                <TabsTrigger value="timeline">Timeline</TabsTrigger>{" "}
                <TabsTrigger value="reasoning">Reasoning</TabsTrigger>{" "}
                <TabsTrigger value="decision">Decision</TabsTrigger>{" "}
              </TabsList>{" "}
              <TabsContent value="timeline" className="mt-4">
                {" "}
                <TraceTimeline trace={trace} />{" "}
              </TabsContent>{" "}
              <TabsContent value="reasoning" className="mt-4">
                {" "}
                <ReasoningChain reasoning={trace.reasoning} />{" "}
              </TabsContent>{" "}
              <TabsContent value="decision" className="mt-4">
                {" "}
                <DecisionTree decision={trace.decision} />{" "}
              </TabsContent>{" "}
            </Tabs>{" "}
          </CardContent>{" "}
        </Card>
      ))}
    </div>
  );
}
