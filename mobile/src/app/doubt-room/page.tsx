/** * Doubt Room Page */
import { DoubtTheater } from "@/components/doubt-room/DoubtTheater";
import { ConfidenceEntropy } from "@/components/doubt-room/ConfidenceEntropy";
export default function DoubtRoomPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">Doubt Room</h1>{" "}
        <p className="text-foreground0">
          Uncertainty quantification and alternative realities
        </p>{" "}
      </div>{" "}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {" "}
        <DoubtTheater /> <ConfidenceEntropy />{" "}
      </div>{" "}
    </div>
  );
}
