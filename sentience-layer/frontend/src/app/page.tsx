/**
 * Landing / Home Page
 */

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-6xl font-extrabold tracking-tighter bg-gradient-to-r from-[#A855F7] via-[#EAB308] to-[#A855F7] bg-clip-text text-transparent animate-gradient-x">
          Sentience Layer
        </h1>
        <p className="text-xl text-[#A855F7]/80 max-w-2xl font-light">
          A Cognitive Operating System powered by Google Antigravity — 
          where AI agents reason, simulate, and act with human-aligned intelligence.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full">
        <Card className="bg-zinc-900/50 border-zinc-800 hover:border-[#EAB308]/50 transition-colors">
          <CardHeader>
            <CardTitle className="text-[#EAB308]">Agentic Reasoning</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[#A855F7]/70">Multi-step reasoning with 18 specialized agents working in concert.</p>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900/50 border-zinc-800 hover:border-[#EAB308]/50 transition-colors">
          <CardHeader>
            <CardTitle className="text-[#EAB308]">Action Simulation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[#A855F7]/70">Monte Carlo simulation of outcomes before execution.</p>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900/50 border-zinc-800 hover:border-[#EAB308]/50 transition-colors">
          <CardHeader>
            <CardTitle className="text-[#EAB308]">Antigravity Core</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[#A855F7]/70">Deeply integrated with Google Antigravity for enterprise intelligence.</p>
          </CardContent>
        </Card>
      </div>

      <Link href="/dashboard">
        <Button size="lg" className="px-10 bg-[#EAB308] text-black hover:bg-[#EAB308]/90 font-bold rounded-full shadow-[0_0_20px_rgba(234,179,8,0.3)]">
          Enter Mission Control
        </Button>
      </Link>
    </div>
  );
}