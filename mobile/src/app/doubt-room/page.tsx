"use client";

import { useState } from "react";
import { DoubtTheater } from "@/components/doubt-room/DoubtTheater";
import { ConfidenceEntropy } from "@/components/doubt-room/ConfidenceEntropy";
import { AlternativeRealities } from "@/components/doubt-room/AlternativeRealities";

export default function DoubtRoomPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [activeDebate, setActiveDebate] = useState<any>(null);

  const handleDebateChanged = (selectedDebate: any) => {
    setActiveDebate(selectedDebate);
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-rose-400 to-amber-400 bg-clip-text text-transparent">
          Doubt Room
        </h1>
        <p className="text-muted-foreground text-sm">
          Uncertainty quantification, swarm audits, and alternative reality branches
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {/* Left Column: Debate Simulation Control & Logs */}
        <div className="w-full">
          <DoubtTheater onDebateChanged={handleDebateChanged} />
        </div>

        {/* Right Column: Statistics & Divergent Timeline Pathways */}
        <div className="w-full space-y-6">
          <ConfidenceEntropy refreshTrigger={refreshKey} activeDebate={activeDebate} />
          <AlternativeRealities activeDebate={activeDebate} />
        </div>
      </div>
    </div>
  );
}

