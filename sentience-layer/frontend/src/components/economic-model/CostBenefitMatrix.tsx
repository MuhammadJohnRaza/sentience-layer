/**
 * Cost-Benefit Matrix
 */

"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const MATRIX_ITEMS = [
  { name: "Auto-execution", cost: "Low", benefit: "High", effort: "Low", risk: "Medium" },
  { name: "Manual Review", cost: "Medium", benefit: "Medium", effort: "High", risk: "Low" },
  { name: "Simulation First", cost: "High", benefit: "High", effort: "Medium", risk: "Low" },
  { name: "Direct Deploy", cost: "Low", benefit: "High", effort: "Low", risk: "High" },
];

export function CostBenefitMatrix() {
  const getColor = (value: string) => {
    switch (value) {
      case "High": return "bg-emerald-100 text-emerald-800";
      case "Medium": return "bg-amber-100 text-amber-800";
      case "Low": return "bg-blue-100 text-blue-800";
      default: return "bg-slate-100 text-slate-800";
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cost-Benefit Matrix</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {MATRIX_ITEMS.map((item) => (
            <div key={item.name} className="rounded-lg border p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">{item.name}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge className={getColor(item.cost)}>Cost: {item.cost}</Badge>
                <Badge className={getColor(item.benefit)}>Benefit: {item.benefit}</Badge>
                <Badge className={getColor(item.effort)}>Effort: {item.effort}</Badge>
                <Badge className={getColor(item.risk)}>Risk: {item.risk}</Badge>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}