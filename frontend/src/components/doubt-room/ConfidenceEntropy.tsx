/** * Confidence Entropy Visualization */ "use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
export function ConfidenceEntropy() {
  // Simulated entropy data
  const entropyLevels = [
    {
      label: "High Confidence",
      value: 40,
      color: "bg-primary",
    },
    {
      label: "Medium Confidence",
      value: 35,
      color: "bg-amber-500",
    },
    {
      label: "Low Confidence",
      value: 20,
      color: "bg-orange-500",
    },
    {
      label: "Uncertainty",
      value: 5,
      color: "bg-destructive",
    },
  ];
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Confidence Entropy</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="flex h-48 items-end gap-2">
          {" "}
          {entropyLevels.map((level) => (
            <div
              key={level.label}
              className="flex flex-1 flex-col items-center gap-2"
            >
              {" "}
              <div
                className={cn("w-full rounded-t transition-all", level.color)}
                style={{
                  height: `${level.value * 2}%`,
                }}
              />{" "}
              <span className="text-xs text-center font-medium">
                {level.label}
              </span>{" "}
              <span className="text-xs text-foreground0">
                {level.value}%
              </span>{" "}
            </div>
          ))}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
import { cn } from "@/lib/utils";
