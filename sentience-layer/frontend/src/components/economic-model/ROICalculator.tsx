/**
 * ROI Calculator
 */

"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function ROICalculator() {
  const [cost, setCost] = useState(1000);
  const [benefit, setBenefit] = useState(2000);
  const [period, setPeriod] = useState(12);

  const roi = ((benefit - cost) / cost) * 100;
  const monthlyReturn = (benefit - cost) / period;

  return (
    <Card>
      <CardHeader>
        <CardTitle>ROI Calculator</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Total Cost ($)</label>
            <Input type="number" value={cost} onChange={(e) => setCost(Number(e.target.value))} />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Total Benefit ($)</label>
            <Input type="number" value={benefit} onChange={(e) => setBenefit(Number(e.target.value))} />
          </div>
        </div>
        
        <div className="space-y-2">
          <label className="text-sm font-medium">Period (months)</label>
          <Input type="number" value={period} onChange={(e) => setPeriod(Number(e.target.value))} />
        </div>

        <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-900 space-y-3">
          <div className="flex items-center justify-between">
            <span className="font-medium">ROI</span>
            <Badge variant={roi > 0 ? "default" : "destructive"} className="text-lg">
              {roi.toFixed(1)}%
            </Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-500">Monthly Return</span>
            <span className="font-medium">${monthlyReturn.toFixed(2)}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-500">Payback Period</span>
            <span className="font-medium">
              {monthlyReturn > 0 ? (cost / monthlyReturn).toFixed(1) : "∞"} months
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}