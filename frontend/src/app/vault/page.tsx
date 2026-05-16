/** * Vault Page - Document Management */
import { VaultBrowser } from "@/components/vault/VaultBrowser";
export default function VaultPage() {
  return (
    <div className="space-y-6">
      {" "}
      <div>
        {" "}
        <h1 className="text-3xl font-bold tracking-tight">Vault</h1>{" "}
        <p className="text-foreground0">
          Secure document storage and retrieval
        </p>{" "}
      </div>{" "}
      <VaultBrowser />{" "}
    </div>
  );
}
