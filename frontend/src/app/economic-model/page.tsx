/** * Economic Model Page */
import { ROICalculator } from "@/components/economic-model/ROICalculator";
import { CostBenefitMatrix } from "@/components/economic-model/CostBenefitMatrix";
export default function EconomicModelPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">
          Economic Model
        </h1>{" "}
        <p className="text-foreground0">
          Cost-benefit analysis and resource optimization
        </p>{" "}
      </div>{" "}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {" "}
        <ROICalculator /> <CostBenefitMatrix />{" "}
      </div>{" "}
    </div>
  );
}
