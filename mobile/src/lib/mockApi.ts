/**
 * Mock API for Frontend Screens
 * Used when backend is unavailable or for deterministic UI testing
 */

export const mockApi = {
  // Dashboard
  getMetrics: async () => ({
    activeAgents: 18,
    systemLoad: "42%",
    decisionsToday: 1420,
    confidenceAvg: 0.94,
  }),

  // Chat
  getChatHistory: async () => [
    {
      id: "1",
      role: "assistant",
      content: "Welcome back, Administrator. All 18 agents are nominal.",
      timestamp: new Date().toISOString(),
    },
  ],

  sendMessage: async (msg: string) => {
    return {
      id: Math.random().toString(),
      role: "assistant",
      content: `Simulated response to: "${msg}"`,
      timestamp: new Date().toISOString(),
    };
  },

  // Trace
  getAgentTraces: async () => [
    {
      id: "trace_1",
      agentName: "Causal Inference Alpha",
      agentType: "Reasoning",
      status: "success",
      startTime: new Date().toISOString(),
      reasoning: [
        {
          step: 1,
          thought: "Analyzing initial causal vectors",
          action: "compute",
          observation: "Vectors nominal",
          confidence: 0.99,
        },
      ],
      decision: {
        chosen: "Execute branch B",
        confidence: 0.95,
        framework: "ReAct",
        alternatives: ["Branch A", "Wait"],
      },
    },
  ],

  // Vault
  getVaultDocuments: async () => [
    {
      id: "doc_1",
      name: "System Architecture v4.pdf",
      size: "2.4 MB",
      type: "PDF",
      status: "Indexed",
    },
    {
      id: "doc_2",
      name: "Q2 Threat Matrix.csv",
      size: "145 KB",
      type: "Dataset",
      status: "Processing",
    },
  ],

  // Playbook
  getPlaybooks: async () => [
    {
      id: "pb_1",
      name: "Emergency Lockdown",
      status: "Ready",
      lastRun: "2 days ago",
    },
    {
      id: "pb_2",
      name: "Daily Data Sync",
      status: "Active",
      lastRun: "3 hours ago",
    },
  ],

  // Memory
  getMemories: async () => [
    {
      id: "mem_1",
      content: "User prefers conservative execution.",
      weight: 0.88,
      type: "Belief",
    },
  ],

  // Actions
  getActions: async () => [
    {
      id: "act_1",
      title: "Deploy Security Patch",
      status: "Pending Approval",
      confidence: 0.92,
      priority: "High",
    },
  ],
};
