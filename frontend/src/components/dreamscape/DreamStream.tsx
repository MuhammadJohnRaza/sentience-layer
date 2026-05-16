/** * Dream Stream Visualization */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { DreamReport } from "@/types";
export function DreamStream() {
  const [reports, setReports] = useState<DreamReport[]>([]);
  useEffect(() => {
    api.getDreamReports().then((data) => setReports(data));
  }, []);
  return (
    <Card className="h-96">
      {" "}
      <CardHeader>
        {" "}
        <CardTitle>Dream Stream</CardTitle>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="relative h-full overflow-hidden">
          {" "}
          {/* Animated dream particles */}
          <div className="absolute inset-0">
            {" "}
            {reports.map((report, i) => (
              <div
                key={report.id}
                className="absolute animate-float rounded-lg border bg-white/80 p-3 shadow-sm backdrop-blur dark:bg-card/80"
                style={{
                  left: `${(i % 3) * 30 + 10}%`,
                  top: `${Math.floor(i / 3) * 25 + 10}%`,
                  animationDelay: `${i * 0.5}s`,
                }}
              >
                {" "}
                <Badge variant="secondary" className="mb-1 text-xs">
                  {" "}
                  {new Date(report.timestamp).toLocaleDateString()}
                </Badge>{" "}
                <p className="text-xs">
                  {report.insightsDiscovered.length}
                  insights
                </p>{" "}
                <p className="text-xs text-foreground0">
                  {report.schemasCreated.length}
                  schemas
                </p>{" "}
              </div>
            ))}
          </div>{" "}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
