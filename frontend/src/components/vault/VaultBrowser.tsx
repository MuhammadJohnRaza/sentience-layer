/** * Vault Browser Component */ "use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
export function VaultBrowser() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  useEffect(() => {
    api.getVaultDocuments().then((data) => setDocuments(data));
  }, []);
  const filtered = documents.filter((d) => {
    const docName = d.name || d.title || "";
    return docName.toLowerCase().includes(search.toLowerCase());
  });
  return (
    <Card>
      {" "}
      <CardHeader>
        {" "}
        <div className="flex items-center justify-between">
          {" "}
          <CardTitle>Documents</CardTitle>{" "}
          <div className="flex gap-2">
            {" "}
            <Input
              placeholder="Search documents..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64"
            />{" "}
            <Button variant="outline">Upload</Button>{" "}
          </div>{" "}
        </div>{" "}
      </CardHeader>{" "}
      <CardContent>
        {" "}
        <div className="space-y-2">
          {" "}
          {filtered.map((doc) => (
            <div
              key={doc.id}
              className="flex items-center justify-between rounded-lg border p-3 hover:bg-background dark:hover:bg-card transition-colors"
            >
              {" "}
              <div className="flex items-center gap-3">
                {" "}
                <div className="h-10 w-10 rounded-lg bg-border/10 flex items-center justify-center dark:bg-border/30">
                  {" "}
                  <svg
                    className="h-5 w-5 text-foreground0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    {" "}
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />{" "}
                  </svg>{" "}
                </div>{" "}
                <div>
                  {" "}
                  <p className="font-medium">{doc.name || doc.title}</p>{" "}
                  <p className="text-xs text-foreground0">
                    {doc.size}• {doc.type}
                  </p>{" "}
                </div>{" "}
              </div>{" "}
              <Badge variant="outline">{doc.status}</Badge>{" "}
            </div>
          ))}
        </div>{" "}
      </CardContent>{" "}
    </Card>
  );
}
