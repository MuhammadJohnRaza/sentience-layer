/**
 * Vault Browser Component
 */
"use client";

import { useEffect, useState, useRef } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { useStore } from "@/store/useStore";
import { cn } from "@/lib/utils";

export function VaultBrowser() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [expandedDocId, setExpandedDocId] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const addNotification = useStore((state) => state.addNotification);

  const fetchDocs = () => {
    api.getVaultDocuments()
      .then((data) => setDocuments(data))
      .catch((err) => console.error("Failed to load vault documents", err));
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    addNotification(`Extracting and uploading ${file.name}... ⏳`);
    
    try {
      const formData = new FormData();
      formData.append("file", file);

      await api.uploadDocument(formData);
      addNotification(`Successfully encrypted and stored ${file.name} to Vault! 🔒`);
      fetchDocs();
    } catch (error) {
      console.error(error);
      addNotification("Upload failed. Verify server is online.");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleDelete = async (docId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Avoid expanding when clicking delete
    
    try {
      await api.deleteVaultDocument(docId);
      addNotification("Document purged from secure vault cache.");
      
      // If the expanded document is deleted, close it
      if (expandedDocId === docId) {
        setExpandedDocId(null);
      }
      
      fetchDocs();
    } catch (error) {
      console.error(error);
      addNotification("Failed to purge document.");
    }
  };

  const toggleExpand = (docId: string) => {
    if (expandedDocId === docId) {
      setExpandedDocId(null);
    } else {
      setExpandedDocId(docId);
    }
  };

  const filtered = documents.filter((d) => {
    const docName = d.name || d.title || "";
    return docName.toLowerCase().includes(search.toLowerCase());
  });

  return (
    <Card className="border border-border/20 bg-card/25 shadow-[0_8px_30px_rgba(0,0,0,0.6)] backdrop-blur-md">
      <CardHeader className="border-b border-border/10 pb-4 flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <div>
          <CardTitle className="text-md font-black tracking-widest text-primary-foreground uppercase flex items-center gap-2">
            🔒 SECURE SWARM MEMORY VAULT
          </CardTitle>
          <CardDescription className="text-[10px] font-bold tracking-wider text-muted-foreground/80 uppercase">
            Cryptographic storage, multi-modal documents, & active session records
          </CardDescription>
        </div>
        
        <div className="flex items-center gap-3">
          <Input
            placeholder="Search credentials & logs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-64 text-xs font-semibold bg-[#020207]/40 border-border/20 placeholder:text-muted-foreground/40 text-foreground h-9"
          />
          
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept=".pdf,.txt,.json,.csv,.tsv"
          />
          
          <Button
            variant="outline"
            onClick={handleUploadClick}
            disabled={isUploading}
            className="h-9 border border-amber-500/30 bg-amber-950/20 text-amber-300 hover:bg-amber-950/40 hover:border-amber-500/60 font-black text-[10px] tracking-widest uppercase transition-all duration-300"
          >
            {isUploading ? (
              <span className="flex items-center gap-1.5">
                <span className="h-3 w-3 rounded-full border border-amber-300 border-t-transparent animate-spin" />
                ENCRYPTING...
              </span>
            ) : (
              "➕ UPLOAD DOCUMENT"
            )}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="pt-6">
        <div className="space-y-3">
          {filtered.length === 0 ? (
            <div className="py-12 text-center border border-dashed border-border/10 rounded-xl bg-[#020207]/10">
              <p className="text-xs font-bold text-muted-foreground/50 tracking-widest uppercase">
                Empty memory state. Upload a document or begin chatting to record traces.
              </p>
            </div>
          ) : (
            filtered.map((doc) => {
              const isExpanded = expandedDocId === doc.id;
              const isChat = doc.type === "chat_session";
              
              return (
                <div
                  key={doc.id}
                  onClick={() => toggleExpand(doc.id)}
                  className={cn(
                    "group rounded-xl border transition-all duration-300 overflow-hidden cursor-pointer bg-[#020207]/45 hover:scale-[1.005]",
                    isExpanded 
                      ? "border-primary/50 shadow-[0_0_15px_rgba(124,58,237,0.15)] bg-[#03030b]/70" 
                      : "border-border/15 hover:border-border/35"
                  )}
                >
                  {/* Document Row Header */}
                  <div className="flex items-center justify-between p-4">
                    <div className="flex items-center gap-3.5">
                      <div className={cn(
                        "h-10 w-10 rounded-lg flex items-center justify-center transition-all duration-300",
                        isChat 
                          ? "bg-primary/10 border border-primary/25 text-primary-foreground group-hover:scale-105" 
                          : "bg-amber-950/20 border border-amber-500/25 text-amber-300 group-hover:scale-105"
                      )}>
                        {isChat ? (
                          <span className="text-lg">🧠</span>
                        ) : (
                          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        )}
                      </div>
                      
                      <div>
                        <p className="text-xs font-black text-primary-foreground tracking-wider uppercase">
                          {doc.name || doc.title}
                        </p>
                        <p className="text-[10px] font-bold text-muted-foreground/60 tracking-wider uppercase font-mono mt-0.5">
                          {doc.size} • {doc.type.replace("_", " ").toUpperCase()} • {doc.uploaded_at}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <Badge className="text-[8px] font-black tracking-widest uppercase bg-emerald-950/80 text-emerald-400 border border-emerald-500/25 px-2 py-0.5">
                        {doc.status}
                      </Badge>
                      
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => handleDelete(doc.id, e)}
                        className="h-8 w-8 text-muted-foreground/60 hover:text-destructive hover:bg-destructive/10 rounded-lg transition-all duration-300"
                      >
                        🗑️
                      </Button>
                    </div>
                  </div>

                  {/* Expanded Text/Chat Preview */}
                  {isExpanded && (
                    <div 
                      onClick={(e) => e.stopPropagation()} // Avoid collapsing when clicking text content
                      className="border-t border-border/10 bg-[#000002]/90 p-4 font-mono text-xs text-foreground/95"
                    >
                      <div className="flex items-center justify-between border-b border-border/10 pb-2 mb-3.5 text-[9px] text-muted-foreground/60 font-bold uppercase tracking-widest">
                        <span>🔒 Cryptographic Swarm Content Preview</span>
                        <span>Press anywhere else to collapse</span>
                      </div>
                      
                      <pre className="whitespace-pre-wrap leading-relaxed select-text font-mono max-h-96 overflow-y-auto pr-2 custom-scrollbar bg-card/10 p-3 rounded-lg border border-border/5 text-[11px] text-muted-foreground/90">
                        {doc.content || "Empty content payload."}
                      </pre>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </CardContent>
    </Card>
  );
}
