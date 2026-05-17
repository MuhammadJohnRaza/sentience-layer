/**
 * API Client for Sentience Layer Backend
 * Integrates with Antigravity endpoints
 */

import { API_BASE_URL } from "./constants";

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(response.status, error);
  }

  return response.json();
}

export const api = {
  // Chat
  sendMessage: (message: string, context?: any) =>
    fetchApi("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message, context }),
    }),

  getChatHistory: () => fetchApi<any[]>("/api/chat/history"),

  // Insights
  getInsights: (filters?: any) =>
    fetchApi<any[]>("/api/insights?" + new URLSearchParams(filters)),

  // Actions
  getActions: () => fetchApi<any[]>("/api/actions"),
  executeAction: (actionId: string) =>
    fetchApi(`/api/actions/${actionId}/execute`, { method: "POST" }),
  simulateAction: (actionId: string) =>
    fetchApi(`/api/actions/${actionId}/simulate`, { method: "POST" }),

  // Agents
  getAgentTraces: () => fetchApi<any[]>("/api/agents/traces"),
  getAgentStatus: () => fetchApi<any[]>("/api/agents/status"),

  // Memory
  getMemory: (type?: string) =>
    fetchApi<any[]>("/api/memory?" + (type ? `type=${type}` : "")),
  searchMemory: (query: string) =>
    fetchApi("/api/memory/search", {
      method: "POST",
      body: JSON.stringify({ query }),
    }),

  // Causal
  getCausalGraph: () => fetchApi("/api/causal/graph"),
  simulateIntervention: (intervention: any) =>
    fetchApi("/api/causal/intervene", {
      method: "POST",
      body: JSON.stringify(intervention),
    }),

  // Economic
  analyzeEconomics: (actionId: string) =>
    fetchApi(`/api/economic/${actionId}/analyze`),

  // Dreams
  getDreamReports: () => fetchApi<any[]>("/api/dream/reports"),

  // Premonitions
  getPremonitions: () => fetchApi<any[]>("/api/premonition"),

  // Vault
  getVaultDocuments: () => fetchApi<any[]>("/api/vault/documents"),
  uploadDocument: (formData: FormData) =>
    fetchApi("/api/vault/upload", {
      method: "POST",
      body: formData,
    }),

  // Playbook
  generatePlaybook: () =>
    fetchApi("/api/playbook/generate", {
      method: "POST",
    }),

  // Health
  health: () => fetchApi("/api/health"),
};
