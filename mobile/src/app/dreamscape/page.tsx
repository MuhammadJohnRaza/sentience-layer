"use client";

import { useState } from "react";
import { DreamStream } from "@/components/dreamscape/DreamStream";
import { InsightEmergence } from "@/components/dreamscape/InsightEmergence";

export default function DreamscapePage() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleConsolidated = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
          Dreamscape
        </h1>
        <p className="text-muted-foreground text-sm">
          Offline learning, vector consolidation, and creative agent synthesis
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DreamStream onConsolidated={handleConsolidated} />
        <InsightEmergence refreshTrigger={refreshKey} />
      </div>
    </div>
  );
}

