/** * Landing / Home Page */
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-8">
      {" "}
      <div className="text-center space-y-4">
        {" "}
        <h1 className="text-5xl font-bold tracking-tight bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent dark:from-slate-100 dark:to-slate-400">
          {" "}
          Sentience Layer{" "}
        </h1>{" "}
        <p className="text-xl text-slate-600 dark:text-muted-foreground max-w-2xl">
          {" "}
          A Cognitive Operating System powered by Google Antigravity — where AI
          agents reason, simulate, and act with human-aligned intelligence.{" "}
        </p>{" "}
      </div>{" "}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full">
        {" "}
        <Card>
          {" "}
          <CardHeader>
            {" "}
            <CardTitle>Agentic Reasoning</CardTitle>{" "}
          </CardHeader>{" "}
          <CardContent>
            {" "}
            <p className="text-sm text-slate-600">
              Multi-step reasoning with 18 specialized agents working in
              concert.
            </p>{" "}
          </CardContent>{" "}
        </Card>{" "}
        <Card>
          {" "}
          <CardHeader>
            {" "}
            <CardTitle>Action Simulation</CardTitle>{" "}
          </CardHeader>{" "}
          <CardContent>
            {" "}
            <p className="text-sm text-slate-600">
              Monte Carlo simulation of outcomes before execution.
            </p>{" "}
          </CardContent>{" "}
        </Card>{" "}
        <Card>
          {" "}
          <CardHeader>
            {" "}
            <CardTitle>Antigravity Core</CardTitle>{" "}
          </CardHeader>{" "}
          <CardContent>
            {" "}
            <p className="text-sm text-slate-600">
              Deeply integrated with Google Antigravity for enterprise
              intelligence.
            </p>{" "}
          </CardContent>{" "}
        </Card>{" "}
      </div>{" "}
      <Link href="/dashboard">
        {" "}
        <Button size="lg" className="px-8">
          {" "}
          Enter Mission Control{" "}
        </Button>{" "}
      </Link>{" "}
    </div>
  );
}
