/** * Action Page */
import { ActionPanel } from "@/components/actions/ActionPanel";
export default function ActionPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">Actions</h1>{" "}
        <p className="text-foreground0">
          Manage and execute agent actions
        </p>{" "}
      </div>{" "}
      <ActionPanel />{" "}
    </div>
  );
}
