/**
 * Decision Tree Visualization
 */

import { Decision } from "@/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

export function DecisionTree({ decision }: { decision: Decision }) {
  return (
    <div className="space-y-4">
      <Card className="p-4 border-2 border-slate-900 dark:border-slate-50">
        <div className="flex items-center justify-between mb-2">
          <Badge>Chosen</Badge>
          <span className="text-sm font-bold">{(decision.confidence * 100).toFixed(0)}% confidence</span>
        </div>
        <p className="font-medium">{decision.chosen}</p>
        <p className="text-xs text-slate-500 mt-1">Framework: {decision.framework}</p>
      </Card>

      <div className="space-y-2">
        <p className="text-sm font-medium text-slate-500">Alternatives Considered:</p>
        {decision.alternatives.map((alt, i) => (
          <Card key={i} className="p-3 opacity-60">
            <div className="flex items-center justify-between">
              <span className="text-sm">{alt}</span>
              <Progress value={30} className="w-24 h-1" />
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}