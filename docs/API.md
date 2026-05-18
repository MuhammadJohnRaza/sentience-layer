# 📡 Sentience Layer - REST & WebSocket API Reference

Welcome to the official API specification for the **Sentience Layer Cognitive Engine**. All core services run natively on **FastAPI (Python)** at `http://localhost:8000`.

---

## 🔒 Session & Security Protocol
All cognitive operations and document vault modifications are fully validated. The backend supports stateful conversation logging via `SESSION_MEMORY` and utilizes Pydantic validation models to verify message schemas.

---

## 💬 Chat & Reasoning Endpoints

### 1. Route Agentic Chat Handoff
Sends a user prompt to be routed through either the complete 3-agent cognitive chain or a single specialized reasoning agent.

- **URL**: `/api/chat`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
- **Request Body (`ChatRequest`)**:
```json
{
  "message": "Why did customer retention decline in Q1?",
  "context": {
    "agent_id": "swarm",
    "system_prompt": "You are a senior business intelligence auditor.",
    "output_verbosity": "detailed"
  }
}
```
*Note: Valid `agent_id` selections are `swarm` (Critic → Consensus → Playbook), `critic`, `personalization`, `memory`, `deterministic`, `ranking`, `priority`, `opportunity`, `causal`, `adversarial`, `debate`, `consensus`, `uncertainty`, `economic`, `dream`, `premonition`, `ethics`, `action_category`, or `action_playbook`.*

- **Response (`ChatResponse`)**:
```json
{
  "content": "Synthesized insight detailing Q1 retention drops...",
  "key_finding": "Onboarding friction accounts for 68% of early-stage churn.",
  "intent": "swarm_reasoning",
  "confidence": 0.895,
  "severity": "HIGH",
  "evidence": [
    "Average onboarding time increased from 15 mins to 42 mins in Q1",
    "Drop-off rate at the SMS-verification step spiked by 24%"
  ],
  "actions": [
    "Fix SMS verification pipeline — Platform Lead — 24h",
    "Draft simplified onboarding walkthrough — Product Designer — 48h"
  ],
  "sources": [],
  "suggested_actions": [
    "Fix SMS verification pipeline — Platform Lead — 24h",
    "Draft simplified onboarding walkthrough — Product Designer — 48h"
  ],
  "agent_used": "SwarmOrchestrator",
  "agent_chain": [
    {
      "agent_id": "critic",
      "agent_name": "Critic Agent",
      "emoji": "🔍",
      "input_summary": "Why did customer retention decline in Q1?",
      "output_summary": "Identified onboarding friction at validation stages...",
      "confidence": 0.85,
      "duration_ms": 320.5,
      "status": "success"
    },
    {
      "agent_id": "consensus",
      "agent_name": "Consensus Agent",
      "emoji": "🤝",
      "input_summary": "Critic: Identified onboarding friction at validation...",
      "output_summary": "Onboarding friction accounts for 68% of early-stage...",
      "confidence": 0.92,
      "duration_ms": 450.2,
      "status": "success"
    },
    {
      "agent_id": "action_playbook",
      "agent_name": "Action Playbook",
      "emoji": "📋",
      "input_summary": "Onboarding friction accounts for 68% of early-stage...",
      "output_summary": "2 actions — THIS_WEEK",
      "confidence": 0.92,
      "duration_ms": 380.1,
      "status": "success"
    }
  ],
  "reasoning_steps": 3,
  "priority": "THIS_WEEK",
  "total_duration_ms": 1150.8
}
```

---

## ⚡ Real-Time Telemetry Stream

### 1. Cognitive Event Broadcast
Allows real-time telemetry streaming of active agent reasoning steps, thoughts, tool executions, and event logs.

- **URL**: `/ws`
- **Protocol**: `WebSocket`
- **Establishment**:
```javascript
const socket = new WebSocket('ws://localhost:8000/ws');

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === "cognitive_event") {
     console.log("Telemetry Frame:", message.payload);
  }
};
```

---

## 📊 Telemetry & System Status

### 1. Health Status
Check backend operational logs and connected infrastructure models.
- **URL**: `/api/health`
- **Method**: `GET`
- **Response**:
```json
{
  "status": "healthy",
  "components": {
    "kernel": "online",
    "world_model": "online",
    "agents": 18
  }
}
```

### 2. Loaded Agents & Servers
Returns list of all registered cognitive agents, active servers, and current computing loads.
- **URL**: `/api/agents/status`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "critic",
    "name": "CriticAgent",
    "status": "active",
    "load": 0.05,
    "role": "Constraint Audit"
  },
  {
    "id": "dream",
    "name": "DreamAgent",
    "status": "active",
    "load": 0.02,
    "role": "Memory Consolidation"
  },
  {
    "id": "postgres",
    "name": "PostgresMcpServer",
    "status": "active",
    "load": 0.01,
    "role": "Relational Indexing"
  }
]
```

### 3. Active Reasoning Traces
Exposes real-time tracing steps executed by system agents for audit verification.
- **URL**: `/api/agents/traces`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "trace_1",
    "agent": "CriticAgent",
    "action": "system_audit",
    "thought": "Verifying relational schema parameters and active MCP connections.",
    "status": "completed",
    "timestamp": "May 18, 02:40 PM",
    "reasoning": [
      {
        "step": 1,
        "action": "Validate Postgres MCP server connectivity",
        "confidence": 0.95
      },
      {
        "step": 2,
        "action": "Verify schema indices and document vault status",
        "confidence": 0.92
      }
    ]
  }
]
```

---

## 🧠 Cognitive Memory Store

### 1. Chat History
Exposes stateful chronological records of active sessions.
- **URL**: `/api/chat/history`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "role": "user",
    "content": "Why did customer retention decline in Q1?",
    "timestamp": "May 18, 02:40 PM"
  },
  {
    "role": "assistant",
    "content": "Synthesized insight detailing Q1 retention drops...",
    "timestamp": "May 18, 02:40 PM"
  }
]
```

### 2. Retrieve Cognitive Memory
Loads all stored episodic and semantic memory objects compiled by agents.
- **URL**: `/api/memory`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "mem_default_1",
    "type": "semantic",
    "content": "System registered and authorized local PostgreSQL MCP server tools.",
    "timestamp": "May 18, 12:00 PM",
    "importance": 0.95,
    "connections": [
      "mcp_init",
      "postgres"
    ]
  }
]
```

### 3. Vector-Search Memories
Uses keyword similarity to search memory vault stores for matching vectors.
- **URL**: `/api/memory/search`
- **Method**: `POST`
- **Request Body**:
```json
{
  "query": "Postgres"
}
```
- **Response**:
```json
[
  {
    "id": "mem_default_1",
    "type": "semantic",
    "content": "System registered and authorized local PostgreSQL MCP server tools.",
    "timestamp": "May 18, 12:00 PM",
    "importance": 0.95,
    "connections": ["mcp_init", "postgres"]
  }
]
```

---

## 🌙 Dreamscape & Foresight

### 1. Dream Mode Consolidation Reports
Loads reports compiled by the cognitive dream kernel consolidations.
- **URL**: `/api/dream/reports`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "dream_report_1",
    "title": "Database Schema Consolidation",
    "summary": "Optimized indices on cognitive_states table and verified integrity.",
    "coherence": 0.94,
    "sleepState": "REM",
    "timestamp": "2026-05-18T03:10:00Z",
    "insightsDiscovered": ["Seeding database results in 40% faster tool execution speeds."],
    "schemasCreated": ["cognitive_states", "vault_metadata"]
  }
]
```

### 2. Premonition Indicators
Loads forecasting and risk trends projected by the premonition engine.
- **URL**: `/api/premonition`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "premonition_1",
    "indicator": "MCP Registry Load",
    "prediction": "Registration of complex database tools will increase local reasoning success.",
    "probability": 0.92,
    "timeframe": "Short-term",
    "severity": "beneficial"
  }
]
```

---

## 🎯 Action & Investment Recommendations

### 1. Recommended Decisions
Retrieve pending operations and diagnostics ranked by urgency and impact.
- **URL**: `/api/actions`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "action-1",
    "title": "Audit System Readiness",
    "description": "Perform relational database schema sanity checks and verify MCP registrations.",
    "category": "diagnostic",
    "status": "pending",
    "impactScore": 85,
    "createdAt": "2026-05-18T02:00:00Z",
    "steps": [
      {
        "id": "step1",
        "description": "Scan active local DB ports",
        "status": "completed"
      },
      {
        "id": "step2",
        "description": "Verify Postgres MCP status",
        "status": "completed"
      }
    ]
  }
]
```

### 2. Execute Action
Dispatches the Action Priority agent to process a chosen operational step.
- **URL**: `/api/actions/{action_id}/execute`
- **Method**: `POST`
- **Response**:
```json
{
  "action_id": "action-1",
  "status": "success",
  "result": "Action 'action-1' successfully executed by CriticAgent."
}
```

### 3. Simulate Action Outcomes
Triggers Monte Carlo scenarios to predict the probability of success.
- **URL**: `/api/actions/{action_id}/simulate`
- **Method**: `POST`
- **Response**:
```json
{
  "action_id": "action-1",
  "status": "success",
  "simulation": {
    "success_probability": 0.95,
    "estimated_impact": "high",
    "unintended_consequences": ["Minor compute usage increase"]
  }
}
```

### 4. Quantitative Economic Analysis
Evaluates the Net Present Value (NPV), financial viability, and return probability.
- **URL**: `/api/economic/{action_id}/analyze`
- **Method**: `GET`
- **Response**:
```json
{
  "actionId": "action-1",
  "totalCost": 1500.0,
  "totalBenefit": 5175.0,
  "netPresentValue": 3675.0,
  "roiPercentage": 245.0,
  "riskAdjustedReturn": 0.95
}
```

---

## 🕸️ Causal Inference Engine

### 1. Causal Graph
Extracts the temporal knowledge graph showing causal strengths.
- **URL**: `/api/causal/graph`
- **Method**: `GET`
- **Response**:
```json
{
  "nodes": [
    {"id": "mcp_tools", "label": "MCP Tools Registered", "value": 3.0, "variance": 0.0},
    {"id": "reasoning_accuracy", "label": "Reasoning Accuracy", "value": 0.95, "variance": 0.02}
  ],
  "edges": [
    {"source": "mcp_tools", "target": "reasoning_accuracy", "strength": 0.45}
  ]
}
```

### 2. Causal Intervention Simulation
Calculates what happens if you manually modify or adjust one causal parameter.
- **URL**: `/api/causal/intervene`
- **Method**: `POST`
- **Request Body**:
```json
{
  "nodeId": "mcp_tools",
  "value": 5.0
}
```
- **Response**:
```json
{
  "status": "success",
  "intervention": {"nodeId": "mcp_tools", "value": 5.0},
  "effect": "Intervention on 'mcp_tools' simulated successfully. Causal factors aligned."
}
```

---

## 🔒 Memory Vault Operations

### 1. Vault Documents
Retrieves all files, text, and chat sessions encrypted in the vault.
- **URL**: `/api/vault/documents`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "init_vault_doc",
    "name": "Sentience Layer System Diagnostics",
    "title": "Sentience Layer System Diagnostics",
    "type": "system_report",
    "size": "4.2 KB",
    "uploaded_at": "May 18, 02:00 PM",
    "status": "encrypted",
    "content": "SYSTEM DIAGNOSTICS LOG...",
    "metadata": {
      "description": "Initial system trace showing cognitive agent readiness...",
      "reasoning": "Standard operating guidelines require diagnostic trace verification..."
    }
  }
]
```

### 2. Upload Document to Vault
Uploads a `.pdf`, `.txt`, `.json`, `.csv`, or `.tsv` file to the encrypted vault.
- **URL**: `/api/vault/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Request Body**: `file` (Binary payload)
- **Response**:
```json
{
  "status": "success",
  "document": {
    "id": "uploaded_1",
    "name": "q1_reports.txt",
    "title": "q1_reports.txt",
    "type": "uploaded_file",
    "size": "15.4 KB",
    "uploaded_at": "May 18, 02:45 PM",
    "status": "encrypted",
    "content": "Document text extracted here...",
    "metadata": {
      "description": "Trace document persisted directly from Cognitive Chat Link.",
      "storage_mode": "Memory Vault Persistence",
      "extracted_length": 15400
    }
  }
}
```

### 3. Delete Document from Vault
Removes an uploaded file or session memory from the local memory store.
- **URL**: `/api/vault/documents/{doc_id}`
- **Method**: `DELETE`
- **Response**:
```json
{
  "status": "success",
  "message": "Document uploaded_1 successfully deleted from local cognitive store."
}
```
