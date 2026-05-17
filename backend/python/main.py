import os
import sys
import asyncio
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

# ─── Stub endpoints for other frontend calls ───────────────────────────────────

@app.get("/api/agents/traces")
def agent_traces():
    return []

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
    return memories

@app.get("/api/dream/reports")
def dream_reports():
    return []

@app.get("/api/premonition")
def premonitions():
    return []

@app.get("/api/actions")
def get_actions():
    return []

@app.get("/api/causal/graph")
def causal_graph():
    return {"nodes": [], "edges": []}

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

@app.get("/api/insights")
def insights():
    return []

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
