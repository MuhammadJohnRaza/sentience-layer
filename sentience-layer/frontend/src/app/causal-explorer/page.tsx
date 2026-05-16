/**
 * Causal Explorer Page
 */

import { CausalGraph } from "@/components/causal-explorer/CausalGraph";
import { InterventionSimulator } from "@/components/causal-explorer/InterventionSimulator";

export default function CausalExplorerPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Causal Explorer</h1>
        <p className="text-slate-500">Discover and test causal relationships</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <CausalGraph />
        </div>
        <InterventionSimulator />
      </div>
    </div>
  );
}