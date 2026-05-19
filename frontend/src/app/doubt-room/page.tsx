/** * Doubt Room Page */
"use client";

import { useState } from "react";
import { DoubtTheater } from "@/components/doubt-room/DoubtTheater";
import { ConfidenceEntropy } from "@/components/doubt-room/ConfidenceEntropy";
import { AlternativeRealities } from "@/components/doubt-room/AlternativeRealities";

export default function DoubtRoomPage() {
  const [activeDebate, setActiveDebate] = useState<any>(null);
  const [refreshStatsKey, setRefreshStatsKey] = useState<number>(0);

  const handleDebateChanged = (debate: any) => {
    setActiveDebate(debate);
  };

  const triggerStatsRefresh = () => {
    setRefreshStatsKey(prev => prev + 1);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-rose-400 to-violet-400 bg-clip-text text-transparent">
          Doubt Room
        </h1>
        <p className="text-muted-foreground text-sm">
          Uncertainty quantification, dynamic dissent simulations, and causal divergent realities
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        <DoubtTheater onDebateChanged={handleDebateChanged} refreshStatsTrigger={triggerStatsRefresh} />
        <div className="space-y-6">
          <ConfidenceEntropy refreshTrigger={refreshStatsKey} />
          <AlternativeRealities activeDebate={activeDebate} />
        </div>
      </div>
    </div>
  );
}
