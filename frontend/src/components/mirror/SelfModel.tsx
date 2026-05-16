/** * Self Model Visualization */ "use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
const CAPABILITIES = [
  {
    name: "Reasoning",
    value: 92,
  },
  {
    name: "Memory",
    value: 88,
  },
  {
    name: "Creativity",
    value: 75,
  },
  {
    name: "Empathy",
    value: 85,
  },
  {
    name: "Speed",
    value: 95,
  },
  {
    name: "Accuracy",
    value: 90,
  },
];
export function SelfModel() {
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Self Model</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent className="space-y-4">
        {" "}
        <div className="flex items-center justify-center py-6">
          {" "}
          <div className="relative h-32 w-32">
            {" "}
            <div className="absolute inset-0 rounded-full border-4 border-border dark:border-border" />{" "}
            <div className="absolute inset-2 rounded-full border-4 border-slate-300 dark:border-border" />{" "}
            <div className="absolute inset-4 rounded-full bg-card dark:bg-background flex items-center justify-center">
              {" "}
              <span className="text-2xl font-bold text-white dark:text-foreground">
                SL
              </span>{" "}
            </div>{" "}
          </div>{" "}
        </div>{" "}
        <div className="space-y-3">
          {" "}
          {CAPABILITIES.map((cap) => (
            <div key={cap.name}>
              {" "}
              <div className="flex justify-between mb-1">
                {" "}
                <span className="text-sm font-medium">{cap.name}</span>{" "}
                <span className="text-sm text-foreground0">
                  {cap.value}%
                </span>{" "}
              </div>{" "}
              <Progress value={cap.value} className="h-2" />{" "}
            </div>
          ))}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
