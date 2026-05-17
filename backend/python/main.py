import os
import sys
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any

# Ensure backend/python is on the path
sys.path.insert(0, os.path.dirname(__file__))

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

# ─── Chat Endpoint ─────────────────────────────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Route user message through a cognitive agent ReAct loop."""
    from agents.critic_agent import CriticAgent

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

        return ChatResponse(
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
    return []

@app.get("/api/memory")
def get_memory():
    return []

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
    return []

@app.get("/api/insights")
def insights():
    return []

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
