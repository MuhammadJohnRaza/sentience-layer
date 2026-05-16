/**
 * Mirror Page - Self-Reflection
 */

import { SelfModel } from "@/components/mirror/SelfModel";
import { BiasReflection } from "@/components/mirror/BiasReflection";

export default function MirrorPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Mirror</h1>
        <p className="text-slate-500">Self-model and bias reflection</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SelfModel />
        <BiasReflection />
      </div>
    </div>
  );
}