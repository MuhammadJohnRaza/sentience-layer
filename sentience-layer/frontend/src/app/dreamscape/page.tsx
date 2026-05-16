/**
 * Dreamscape Page
 */

import { DreamStream } from "@/components/dreamscape/DreamStream";
import { InsightEmergence } from "@/components/dreamscape/InsightEmergence";

export default function DreamscapePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dreamscape</h1>
        <p className="text-slate-500">Offline learning and creative synthesis</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DreamStream />
        <InsightEmergence />
      </div>
    </div>
  );
}