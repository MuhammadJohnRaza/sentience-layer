/** * Memory Page */
import { MemoryViewer } from "@/components/memory/MemoryViewer";
import { MemoryGraph } from "@/components/memory/MemoryGraph";
export default function MemoryPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">Memory</h1>{" "}
        <p className="text-foreground0">
          Episodic, semantic, and procedural memory graphs
        </p>{" "}
      </div>{" "}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {" "}
        <div className="lg:col-span-2">
          {" "}
          <MemoryGraph />{" "}
        </div>{" "}
        <MemoryViewer />{" "}
      </div>{" "}
    </div>
  );
}
