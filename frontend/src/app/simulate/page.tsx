/** * Simulation Page */
import { SimulationDashboard } from "@/components/simulation/SimulationDashboard";
import { ActionLogger } from "@/components/ActionLogger";

export default function SimulatePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Simulation</h1>
        <p className="text-foreground">
          Test actions before execution with Monte Carlo modeling
        </p>
      </div>
      
      <SimulationDashboard />
      
      <ActionLogger />
    </div>
  );
}
