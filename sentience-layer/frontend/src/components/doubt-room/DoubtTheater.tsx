/**
 * Doubt Theater - Debate Visualization
 */

"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const DEBATE_TOPICS = [
  { topic: "Should we auto-execute high-confidence actions?", for: 65, against: 35 },
  { topic: "Is the causal link strong enough?", for: 45, against: 55 },
  { topic: "Does the economic model justify the cost?", for: 78, against: 22 },
];

export function DoubtTheater() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Doubt Theater</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {DEBATE_TOPICS.map((debate, i) => (
          <div key={i} className="rounded-lg border p-4">
            <p className="font-medium mb-3">{debate.topic}</p>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge className="bg-emerald-500 w-12 justify-center">For</Badge>
                <Progress value={debate.for} className="flex-1 h-2" />
                <span className="text-sm w-10 text-right">{debate.for}%</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge className="bg-red-500 w-12 justify-center">Against</Badge>
                <Progress value={debate.against} className="flex-1 h-2" />
                <span className="text-sm w-10 text-right">{debate.against}%</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}