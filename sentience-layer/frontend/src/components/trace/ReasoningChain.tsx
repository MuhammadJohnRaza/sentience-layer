/**
 * Reasoning Chain Display
 */

import { ReasoningStep } from "@/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getConfidenceColor } from "@/lib/utils";

export function ReasoningChain({ reasoning }: { reasoning: ReasoningStep[] }) {
  return (
    <div className="space-y-3">
      {reasoning.map((step, i) => (
        <Card key={i} className="p-4">
          <div className="flex items-start justify-between mb-2">
            <Badge variant="outline">Step {step.step}</Badge>
            <span className={cn("text-xs px-2 py-0.5 rounded-full", getConfidenceColor(step.confidence))}>
              {(step.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="space-y-2 text-sm">
            <p><span className="font-medium text-slate-500">Thought:</span> {step.thought}</p>
            <p><span className="font-medium text-slate-500">Action:</span> {step.action}</p>
            <p><span className="font-medium text-slate-500">Observation:</span> {step.observation}</p>
          </div>
        </Card>
      ))}
    </div>
  );
}

import { cn } from "@/lib/utils";