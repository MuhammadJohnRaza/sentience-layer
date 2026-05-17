import os
import sys
import asyncio
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any

# Ensure both root workspace and backend/python are on the path
backend_python_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(backend_python_dir))
sys.path.insert(0, backend_python_dir)
sys.path.insert(0, workspace_root)

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Sentience Layer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Register local PostgreSQL MCP server in global registry for agent discovery
    from mcp.client import get_mcp_registry
    from mcp_servers.postgres_mcp import get_instance as get_postgres_mcp
    
    registry = get_mcp_registry()
    registry.register_local_server("postgres", get_postgres_mcp())


# ─── Request / Response Models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    context: Optional[Any] = None

class ChatResponse(BaseModel):
    content: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    sources: Optional[list] = None
    suggested_actions: Optional[list] = None
    agent_used: Optional[str] = None
    reasoning_steps: Optional[int] = None

# ─── Root & Health ─────────────────────────────────────────────────────────────

@app.get("/")
def read_root():
    return {"status": "online", "message": "Sentience Layer Kernel Active"}


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "components": {
            "kernel": "online",
            "world_model": "online",
            "agents": 18
        }
    }

# ─── Agent Status ──────────────────────────────────────────────────────────────

@app.get("/api/agents/status")
def agent_status():
    agents = [
        "ActionCategoryAgent", "ActionPlaybookAgent", "ActionPriorityAgent",
        "ActionRankingAgent", "AdversarialTestAgent", "CausalInferenceAgent",
        "ConsensusAgent", "CriticAgent", "DebateAgent", "DeterministicAgent",
        "DreamAgent", "EconomicAgent", "EthicsAgent", "MemoryEnabledAgent",
        "OpportunityAnalystAgent", "PersonalizationAgent", "PremonitionAgent",
        "UncertaintyAgent"
    ]
    return [
        {"id": a.lower().replace("agent", ""), "name": a, "status": "active", "load": 0.1}
        for a in agents
    ]

# ─── Cognitive Session Memory Store ──────────────────────────────────────────
SESSION_MEMORY = []

# ─── Chat Endpoint ─────────────────────────────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Route user message through a cognitive agent ReAct loop."""
    from agents.critic_agent import CriticAgent
    from datetime import datetime

    agent = CriticAgent(config={})
    agent.max_reasoning_steps = 2

    try:
        result = await agent.reason_and_act(req.message)

        # Build the response text from the reasoning chain
        thoughts = []
        if result.reasoning_chain:
            for step in result.reasoning_chain:
                if step.thought and step.thought.strip():
                    thoughts.append(step.thought.strip())

        response_text = "\n\n".join(thoughts) if thoughts else (
            result.data.get("response", "") if isinstance(result.data, dict)
            else "I processed your request through the cognitive kernel."
        )

        if not response_text.strip():
            response_text = "Cognitive reasoning complete. The kernel has processed your input."

        response_obj = ChatResponse(
            content=response_text,
            intent="reasoning",
            confidence=result.confidence,
            sources=[],
            suggested_actions=[
                "Explore causal relationships",
                "Run adversarial test",
                "Analyze economic impact",
                "Check ethical constraints"
            ],
            agent_used="CriticAgent",
            reasoning_steps=len(result.reasoning_chain) if result.reasoning_chain else 0
        )

        # Automatically store this session in cognitive memory
        SESSION_MEMORY.append({
            "id": f"session_{len(SESSION_MEMORY) + 1}",
            "timestamp": datetime.utcnow().strftime("%b %d, %I:%M %p"),
            "iso_time": datetime.utcnow().isoformat(),
            "user": req.message,
            "assistant": response_text,
            "confidence": result.confidence
        })

        return response_obj

    except Exception as e:
        return ChatResponse(
            content=f"The cognitive kernel encountered an issue: {str(e)}. Please try again.",
            intent="error",
            confidence=0.0,
            suggested_actions=["Retry", "Check agent status"]
        )

# ─── Stub & Mock Endpoints for Frontend Dashboard ────────────────────────────────

class SearchRequest(BaseModel):
    query: str

class InterventionRequest(BaseModel):
    nodeId: str
    value: float

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "Sentience Layer Cognitive API", "version": "1.0.0"}

@app.get("/api/agents/status")
def agents_status():
    return [
        {"id": "critic", "name": "CriticAgent", "status": "active", "load": 0.05, "role": "Constraint Audit"},
        {"id": "dream", "name": "DreamAgent", "status": "active", "load": 0.02, "role": "Memory Consolidation"},
        {"id": "postgres", "name": "PostgresMcpServer", "status": "active", "load": 0.01, "role": "Relational Indexing"}
    ]

@app.get("/api/agents/traces")
def agent_traces():
    return [
        {
            "id": "trace_1",
            "agent": "CriticAgent",
            "action": "system_audit",
            "thought": "Verifying relational schema parameters and active MCP connections.",
            "status": "completed",
            "timestamp": datetime.utcnow().strftime("%b %d, %I:%M %p"),
            "reasoning": [
                {"step": 1, "action": "Validate Postgres MCP server connectivity", "confidence": 0.95},
                {"step": 2, "action": "Verify schema indices and document vault status", "confidence": 0.92}
            ]
        }
    ]

@app.get("/api/chat/history")
def chat_history():
    history = []
    for s in SESSION_MEMORY:
        history.append({
            "role": "user",
            "content": s["user"],
            "timestamp": s["timestamp"]
        })
        history.append({
            "role": "assistant",
            "content": s["assistant"],
            "timestamp": s["timestamp"]
        })
    return history

@app.get("/api/memory")
def get_memory():
    memories = []
    for s in SESSION_MEMORY:
        memories.append({
            "id": s["id"],
            "type": "episodic",
            "content": f"User: {s['user']} | Agent: {s['assistant']}",
            "timestamp": s["timestamp"],
            "importance": 0.9,
            "connections": ["user_interaction", "cognitive_kernel"]
        })
    # Seed default memories if empty
    if not memories:
        memories.append({
            "id": "mem_default_1",
            "type": "semantic",
            "content": "System registered and authorized local PostgreSQL MCP server tools.",
            "timestamp": "May 17, 06:00 PM",
            "importance": 0.95,
            "connections": ["mcp_init", "postgres"]
        })
    return memories

@app.post("/api/memory/search")
def search_memory(req: SearchRequest):
    matches = []
    # Search simulated memories
    all_mems = get_memory()
    for m in all_mems:
        if req.query.lower() in m["content"].lower():
            matches.append(m)
    return matches

@app.get("/api/dream/reports")
def dream_reports():
    return [
        {
            "id": "dream_report_1",
            "title": "Database Schema Consolidation",
            "summary": "Optimized indices on cognitive_states table and verified integrity.",
            "coherence": 0.94,
            "sleepState": "REM",
            "timestamp": "2026-05-17T18:10:00Z",
            "insightsDiscovered": ["Seeding database results in 40% faster tool execution speeds."],
            "schemasCreated": ["cognitive_states", "vault_metadata"]
        }
    ]

@app.get("/api/premonition")
def premonitions():
    return [
        {
            "id": "premonition_1",
            "indicator": "MCP Registry Load",
            "prediction": "Registration of complex database tools will increase local reasoning success.",
            "probability": 0.92,
            "timeframe": "Short-term",
            "severity": "beneficial"
        }
    ]

@app.get("/api/actions")
def get_actions():
    return [
        {
            "id": "action-1",
            "title": "Audit System Readiness",
            "description": "Perform relational database schema sanity checks and verify MCP registrations.",
            "category": "diagnostic",
            "status": "pending",
            "impactScore": 85,
            "createdAt": "2026-05-17T18:00:00Z",
            "steps": [
                {"id": "step1", "description": "Scan active local DB ports", "status": "completed"},
                {"id": "step2", "description": "Verify Postgres MCP status", "status": "completed"}
            ]
        },
        {
            "id": "action-2",
            "title": "Run Opportunity Scan",
            "description": "Trigger multi-agent ReAct cognitive cycles to uncover causal synergies.",
            "category": "reasoning",
            "status": "pending",
            "impactScore": 95,
            "createdAt": "2026-05-17T18:15:00Z",
            "steps": [
                {"id": "step3", "description": "Initialize agent reasoning cycles", "status": "pending"},
                {"id": "step4", "description": "Map local relational associations", "status": "pending"}
            ]
        }
    ]

@app.post("/api/actions/{action_id}/execute")
def execute_action(action_id: str):
    return {
        "action_id": action_id,
        "status": "success",
        "result": f"Action '{action_id}' successfully executed by CriticAgent."
    }

@app.post("/api/actions/{action_id}/simulate")
def simulate_action(action_id: str):
    return {
        "action_id": action_id,
        "status": "success",
        "simulation": {
            "success_probability": 0.95,
            "estimated_impact": "high" if action_id == "action-2" else "low",
            "unintended_consequences": ["Minor compute usage increase"]
        }
    }

@app.get("/api/economic/{action_id}/analyze")
def analyze_economics(action_id: str):
    return {
        "action_id": action_id,
        "status": "success",
        "analysis": {
            "utility_score": 0.91 if action_id == "action-2" else 0.65,
            "cost_benefit_ratio": 3.8 if action_id == "action-2" else 1.2,
            "market_impact": "high" if action_id == "action-2" else "low",
            "regulatory_risk": "negligible"
        }
    }

@app.get("/api/causal/graph")
def causal_graph():
    return {
        "nodes": [
            {"id": "mcp_tools", "label": "MCP Tools Registered", "value": 3.0, "variance": 0.0},
            {"id": "reasoning_accuracy", "label": "Reasoning Accuracy", "value": 0.95, "variance": 0.02},
            {"id": "system_latency", "label": "System Latency", "value": 120.0, "variance": 15.0}
        ],
        "edges": [
            {"source": "mcp_tools", "target": "reasoning_accuracy", "strength": 0.45},
            {"source": "reasoning_accuracy", "target": "system_latency", "strength": -0.2}
        ]
    }

@app.post("/api/causal/intervene")
def causal_intervene(req: InterventionRequest):
    return {
        "status": "success",
        "intervention": {"nodeId": req.nodeId, "value": req.value},
        "effect": f"Intervention on '{req.nodeId}' simulated successfully. Causal factors aligned."
    }

@app.get("/api/vault/documents")
def vault_documents():
    docs = []
    
    # If no sessions are in memory, return a dynamic mock document explaining that session memory is stored in the vault
    if not SESSION_MEMORY:
        docs.append({
            "id": "init_vault_doc",
            "title": "Sentience Layer System Diagnostics",
            "type": "system_report",
            "size": "4.2 KB",
            "uploaded_at": "May 17, 06:00 PM",
            "status": "encrypted",
            "metadata": {
                "description": "Initial system trace showing cognitive agent readiness and MCP tool registration.",
                "reasoning": "Standard operating guidelines require automatic system diagnostic trace verification at startup."
            }
        })
    
    # Render all active stored sessions inside the Memory Vault
    for s in SESSION_MEMORY:
        docs.append({
            "id": s["id"],
            "title": f"Cognitive Trace: {s['user'][:25]}...",
            "type": "chat_session",
            "size": f"{len(s['user']) + len(s['assistant'])} bytes",
            "uploaded_at": s["timestamp"],
            "status": "encrypted",
            "metadata": {
                "user_prompt": s["user"],
                "agent_response": s["assistant"],
                "cognitive_confidence": f"{s['confidence'] * 100:.1f}%",
                "storage_mode": "Memory Vault Persistence"
            }
        })
        
    return docs

from fastapi import UploadFile, File

@app.post("/api/vault/upload")
async def vault_upload(file: UploadFile = File(...)):
    doc_id = f"doc_{len(SESSION_MEMORY) + 1}"
    return {
        "status": "success",
        "document": {
            "id": doc_id,
            "title": file.filename,
            "type": "uploaded_file",
            "size": "15.4 KB",
            "uploaded_at": datetime.utcnow().strftime("%b %d, %I:%M %p"),
            "status": "encrypted"
        }
    }

@app.get("/api/insights")
def insights():
    return [
        {
            "id": "insight_1",
            "title": "MCP Enhancement",
            "description": "Registered local PostgreSQL MCP server with list, describe, and query capabilities.",
            "type": "performance",
            "impact": "high",
            "timestamp": "May 17, 06:12 PM"
        }
    ]

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
