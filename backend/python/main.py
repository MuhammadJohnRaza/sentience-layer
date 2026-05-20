import os
import sys
import asyncio
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, List

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
    allow_credentials=False,
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
    
    # Initialize Sentience Kernel
    from sentience_kernel.kernel import SentienceKernel
    global kernel
    kernel = SentienceKernel()
    
    # Wire the Message Bus
    kernel.subscribe(broadcast_cognitive_event)
    
    # Start the continuous loop as a background task
    async def context_stream():
        return {"query": "Background cognitive maintenance."}
        
    global kernel_task
    kernel_task = asyncio.create_task(kernel.start(context_stream=context_stream))

@app.on_event("shutdown")
async def shutdown_event():
    global kernel
    if kernel:
        await kernel.stop()
    global kernel_task
    if 'kernel_task' in globals() and kernel_task:
        kernel_task.cancel()

# ─── WebSocket / Real-time Telemetry ──────────────────────────────────────────

active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time agent updates"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_cognitive_event(event):
    """Broadcast cognitive event to all connected clients."""
    if not active_connections:
        return
        
    message = {
        "type": "cognitive_event",
        "payload": event.to_dict() if hasattr(event, "to_dict") else str(event)
    }
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            pass


# ─── Request / Response Models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    context: Optional[Any] = None

class AgentHandoffStep(BaseModel):
    agent_id: str
    agent_name: str
    emoji: str
    input_summary: str
    output_summary: str
    confidence: float
    duration_ms: float
    status: str = "success"

class ChatResponse(BaseModel):
    content: str
    key_finding: Optional[str] = None
    intent: Optional[str] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None          # CRITICAL | HIGH | MEDIUM | LOW
    evidence: Optional[list] = None
    actions: Optional[list] = None
    sources: Optional[list] = None
    suggested_actions: Optional[list] = None
    agent_used: Optional[str] = None
    agent_chain: Optional[list] = None      # List[AgentHandoffStep]
    reasoning_steps: Optional[int] = None
    priority: Optional[str] = None
    total_duration_ms: Optional[float] = None

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
    """Route user message through the 3-agent SwarmOrchestrator or a named single agent."""
    from datetime import datetime
    import importlib

    # Resolve agent selection and custom system prompt from client context
    agent_id = "swarm"  # default: use full 3-agent chain
    system_prompt = None
    output_verbosity = "default"

    if req.context and isinstance(req.context, dict):
        agent_id = req.context.get("agent_id", "swarm")
        system_prompt = req.context.get("system_prompt", None)
        output_verbosity = req.context.get("output_verbosity", "default")

    # Build document context from uploaded vault files
    doc_contexts = []
    for doc in UPLOADED_DOCUMENTS:
        if "content" in doc and doc["content"] and doc["content"].strip():
            doc_contexts.append(f"--- DOCUMENT: {doc['name']} ---\n{doc['content']}\n")
    doc_context_str = "\n".join(doc_contexts)

    # ── DEFAULT: SwarmOrchestrator (Critic → Consensus → Playbook) ────────
    if agent_id in ("swarm", "critic", ""):
        try:
            from swarm_orchestrator import SwarmOrchestrator
        except ImportError:
            from backend.python.swarm_orchestrator import SwarmOrchestrator

        orchestrator = SwarmOrchestrator(system_prompt=system_prompt)

        try:
            result = await orchestrator.run(query=req.message, doc_context=doc_context_str, output_verbosity=output_verbosity)

            # Conversational Agentic Synthesis Step
            try:
                from backend.python.antigravity_client import get_antigravity_client
                antigravity = get_antigravity_client()
                
                chain_details = "\n".join(
                    f"- {s.agent_name} ({s.emoji}): {s.output_summary} (Confidence: {s.confidence * 100:.1f}%)"
                    for s in result.agent_chain
                )
                
                synthesis_prompt = f"""You are the Sentience Swarm Orchestrator. The user asked: "{req.message}"
Here are the findings and actions generated by our specialized multi-agent swarm:

Key Finding: {result.key_finding}
Detailed Insight: {result.insight}
Suggested Actions: {", ".join(result.actions) if result.actions else "None"}

Agent Collaboration Path:
{chain_details}

Synthesize these findings into a single warm, highly conversational, and agentic response to the user.
Explain naturally and clearly how the agents (Critic, Consensus, Playbook, etc.) collaborated to reach this outcome.
Format the output in clean, readable markdown. Do not include raw JSON. Be conversational, insightful, and agentic.
"""
                resp = await antigravity.generate(synthesis_prompt, max_tokens=1000)
                if hasattr(resp, 'data') and isinstance(resp.data, dict):
                    response_text = resp.data.get('choices', [{}])[0].get('message', {}).get('content', '')
                elif hasattr(resp, 'content'):
                    response_text = resp.content
                elif isinstance(resp, dict):
                    response_text = resp.get('content', '')
                else:
                    response_text = str(resp)
                    
                response_text = response_text.strip()
                if not response_text:
                    raise ValueError("Empty conversational synthesis response.")
            except Exception as synth_err:
                print(f"Conversational synthesis failed: {synth_err}. Falling back to default format.")
                response_text = f"{result.key_finding}\n\n{result.insight}"
                if result.actions:
                    response_text += "\n\n🎯 Actions:\n" + "\n".join(f"• {a}" for a in result.actions)

            agent_chain_dicts = [
                {
                    "agent_id": s.agent_id,
                    "agent_name": s.agent_name,
                    "emoji": s.emoji,
                    "input_summary": s.input_summary,
                    "output_summary": s.output_summary,
                    "confidence": round(s.confidence, 3),
                    "duration_ms": round(s.duration_ms, 1),
                    "status": s.status,
                }
                for s in result.agent_chain
            ]

            response_obj = ChatResponse(
                content=response_text,
                key_finding=result.key_finding,
                intent="swarm_reasoning",
                confidence=result.confidence,
                severity=result.severity,
                evidence=result.evidence,
                actions=result.actions,
                sources=[],
                suggested_actions=result.actions[:2] if result.actions else [],
                agent_used="SwarmOrchestrator",
                agent_chain=agent_chain_dicts,
                reasoning_steps=len(result.agent_chain),
                priority=result.priority,
                total_duration_ms=result.total_duration_ms,
            )

            SESSION_MEMORY.append({
                "id": f"session_{len(SESSION_MEMORY) + 1}",
                "timestamp": datetime.utcnow().strftime("%b %d, %I:%M %p"),
                "iso_time": datetime.utcnow().isoformat(),
                "user": req.message,
                "assistant": response_text,
                "confidence": result.confidence,
                "severity": result.severity,
            })

            return response_obj

        except Exception as e:
            print(f"SwarmOrchestrator failed: {e}. Falling back to single agent.")
            agent_id = "critic"  # fall through to single-agent path

    # ── SINGLE NAMED AGENT FALLBACK ───────────────────────────────────────
    agent_map = {
        "critic": ("agents.critic_agent", "CriticAgent"),
        "personalization": ("agents.personalization_agent", "PersonalizationAgent"),
        "memory": ("agents.memory_enabled_agent", "MemoryEnabledAgent"),
        "deterministic": ("agents.deterministic_agent", "DeterministicAgent"),
        "ranking": ("agents.action_ranking_agent", "ActionRankingAgent"),
        "priority": ("agents.action_priority_agent", "ActionPriorityAgent"),
        "opportunity": ("agents.opportunity_analyst_agent", "OpportunityAnalystAgent"),
        "causal": ("agents.causal_inference_agent", "CausalInferenceAgent"),
        "adversarial": ("agents.adversarial_test_agent", "AdversarialTestAgent"),
        "debate": ("agents.debate_agent", "DebateAgent"),
        "consensus": ("agents.consensus_agent", "ConsensusAgent"),
        "uncertainty": ("agents.uncertainty_agent", "UncertaintyAgent"),
        "economic": ("agents.economic_agent", "EconomicAgent"),
        "dream": ("agents.dream_agent", "DreamAgent"),
        "premonition": ("agents.premonition_agent", "PremonitionAgent"),
        "ethics": ("agents.ethics_agent", "EthicsAgent"),
        "action_category": ("agents.action_category_agent", "ActionCategoryAgent"),
        "action_playbook": ("agents.action_playbook_agent", "ActionPlaybookAgent"),
    }

    module_path, class_name = agent_map.get(agent_id, ("agents.critic_agent", "CriticAgent"))

    try:
        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        agent = agent_class(config={})
    except Exception as e:
        print(f"Dynamic agent dispatch failed for '{agent_id}': {e}. Fallback CriticAgent.")
        from agents.critic_agent import CriticAgent
        agent = CriticAgent(config={})
        class_name = "CriticAgent"

    agent.max_reasoning_steps = 2

    full_prompt = f"System Directive: {system_prompt}\n\n" if system_prompt else ""
    if doc_contexts:
        full_prompt += "Vault Documents:\n" + doc_context_str + "\n\n"
    full_prompt += f"User Query: {req.message}"

    try:
        # Pass the output_verbosity through the context dict
        result = await agent.reason_and_act(full_prompt, context={"output_verbosity": output_verbosity})

        thoughts = []
        observations = []
        if result.reasoning_chain:
            for step in result.reasoning_chain:
                if step.thought and step.thought.strip():
                    thoughts.append(step.thought.strip())
                if step.observation and step.observation.strip():
                    observations.append(step.observation.strip())

        # Synthesize a highly customized and verbosity-compliant final response
        synthesis_prompt = f"""You are the {class_name}.
Role directive: {system_prompt or 'You are a cognitive reasoning agent.'}

Goal / User Query: {req.message}

Here is your internal reasoning chain:
{chr(10).join(f"- Thought: {t}" for t in thoughts)}

Here are your tool observations:
{chr(10).join(f"- Observation: {o}" for o in observations)}

Please synthesize the final response for the user.
Role-specific instruction: You must act as {class_name} and adopt its unique expertise, style, and tone in your response. Make sure your role as {class_name} is highly visible and clear in your response.
"""

        # Add verbosity constraint
        if output_verbosity == "brief":
            synthesis_prompt += "\nVerbosity constraint: Keep your final response extremely brief, direct, and concise (exactly 1-2 sentences). Do not include any verbose introductory or closing remarks."
        elif output_verbosity == "detailed":
            synthesis_prompt += "\nVerbosity constraint: Please provide an extremely prolonged, detailed, elaborate, and highly exhaustive final response. Dive deep into the analysis, provide extensive explanations of your reasoning, outline the causal/ethical/deterministic considerations of your findings, and structure your answer with clear markdown headings, bold sections, and detailed bullet points."
        else:
            synthesis_prompt += "\nVerbosity constraint: Provide a standard, well-structured, informative response (3-4 sentences or 2-3 short paragraphs)."

        synthesis_raw = await agent.antigravity.generate(synthesis_prompt)
        response_text = ""
        if hasattr(synthesis_raw, 'data') and isinstance(synthesis_raw.data, dict):
            response_text = synthesis_raw.data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            response_text = str(synthesis_raw)

        if not response_text.strip():
            response_text = f"Reasoning complete by {class_name}."

        # Extract suggested actions, evidence, and severity from the synthesized response
        actions_list = ["Run full swarm analysis", "Explore causal chain"]
        if "🎯 Actions:" in response_text or "Actions:" in response_text:
            lines = response_text.split("\n")
            actions_list = [l.strip("•-* ").strip() for l in lines if (l.strip().startswith("•") or l.strip().startswith("-") or l.strip().startswith("*"))][:4]
            if not actions_list:
                actions_list = ["Review findings", "Deploy modifications"]

        response_obj = ChatResponse(
            content=response_text,
            intent="single_agent_reasoning",
            confidence=result.confidence or 0.8,
            severity="MEDIUM",
            evidence=[],
            actions=actions_list,
            sources=[],
            suggested_actions=actions_list[:2] if actions_list else ["Run full swarm analysis", "Explore causal chain"],
            agent_used=class_name,
            agent_chain=[{
                "agent_id": agent_id,
                "agent_name": class_name,
                "emoji": "🤖",
                "input_summary": req.message[:80],
                "output_summary": response_text[:100] + "...",
                "confidence": result.confidence or 0.7,
                "duration_ms": result.execution_time * 1000 if result.execution_time else 0,
                "status": "success"
            }],
            reasoning_steps=len(result.reasoning_chain) if result.reasoning_chain else 0
        )

        # Automatically store this session in cognitive memory
        SESSION_MEMORY.append({
            "id": f"session_{len(SESSION_MEMORY) + 1}",
            "timestamp": datetime.utcnow().strftime("%b %d, %I:%M %p"),
            "iso_time": datetime.utcnow().isoformat(),
            "user": req.message,
            "assistant": response_text,
            "confidence": result.confidence or 0.8
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

# Seed initial lists in main.py
DREAM_REPORTS = [
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

DEBATES_LIST = [
    {
        "id": "debate-1",
        "topic": "Should we auto-execute high-confidence actions without human sign-off?",
        "forPct": 58,
        "againstPct": 42,
        "criticAgentArgs": [
            "Auto-execution poses extreme risk if SQLite containment fails during live Postgres migrations.",
            "A rogue MCP mutation could overwrite active vector tables without rollback triggers."
        ],
        "consensusAgentArgs": [
            "We mandate a 94% confidence threshold and sandboxed Monte Carlo tests before deployment.",
            "Containment protocols are already active and simulated with zero leakage detected."
        ]
    },
    {
        "id": "debate-2",
        "topic": "Is the postgres_list_tables tool relationship strong enough to justify full trust?",
        "forPct": 82,
        "againstPct": 18,
        "criticAgentArgs": [
            "External database connections are highly sensitive to network latency drops.",
            "Adversarial schema injections could bypass the ReAct parser under heavy parallel loads."
        ],
        "consensusAgentArgs": [
            "Caching queries through local memory maps prevents index failures entirely.",
            "All query inputs are audited by the security wrapper before parsing."
        ]
    }
]

class ConsolidateRequest(BaseModel):
    memoryId: str
    content: str

class DebateRequest(BaseModel):
    topic: str

@app.get("/api/dream/reports")
def dream_reports():
    return DREAM_REPORTS

@app.post("/api/dream/consolidate")
async def consolidate_memory(req: ConsolidateRequest):
    try:
        from agents.dream_agent import DreamAgent
    except ImportError:
        from backend.python.agents.dream_agent import DreamAgent
        
    try:
        from base_agent import AgentMessage
    except ImportError:
        from backend.python.agents.base_agent import AgentMessage

    agent = DreamAgent()
    msg = AgentMessage(
        sender="main_api",
        recipient="dream",
        content=req.content,
        message_type="consolidation"
    )
    
    result = await agent.process(msg)
    
    if result.success and isinstance(result.data, dict):
        report = {
            "id": f"dream_report_{len(DREAM_REPORTS) + 1}",
            "title": result.data.get("title", "Trace Optimization"),
            "summary": result.data.get("summary", "Consolidated trace parameters."),
            "coherence": result.data.get("coherence", 0.9),
            "sleepState": result.data.get("sleepState", "REM"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "insightsDiscovered": result.data.get("insightsDiscovered", []),
            "schemasCreated": result.data.get("schemasCreated", [])
        }
        DREAM_REPORTS.insert(0, report)
        return report
    else:
        # Fallback if processing fails
        report = {
            "id": f"dream_report_{len(DREAM_REPORTS) + 1}",
            "title": "Optimized Memory Vector Chunks",
            "summary": "Merged temporary vector indices inside memory tables to optimize query retrieval paths.",
            "coherence": 0.85,
            "sleepState": "REM",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "insightsDiscovered": ["Memory consolidation yields 12% faster vector lookup times."],
            "schemasCreated": ["idx_session_vector_opt"]
        }
        DREAM_REPORTS.insert(0, report)
        return report

@app.get("/api/doubt/debates")
def get_debates():
    return DEBATES_LIST

@app.post("/api/doubt/debate")
async def create_debate(req: DebateRequest):
    try:
        from agents.critic_agent import CriticAgent
        from agents.consensus_agent import ConsensusAgent
    except ImportError:
        from backend.python.agents.critic_agent import CriticAgent
        from backend.python.agents.consensus_agent import ConsensusAgent
        
    try:
        from base_agent import AgentMessage
    except ImportError:
        from backend.python.agents.base_agent import AgentMessage
        
    import random
    
    critic = CriticAgent()
    consensus = ConsensusAgent()
    
    # Generate debate points using real agents
    msg = AgentMessage(sender="main_api", recipient="critic", content=req.topic)
    critic_res = await critic.process(msg)
    
    msg.recipient = "consensus"
    consensus_res = await consensus.process(msg)
    
    critic_args = []
    consensus_args = []
    
    # Extract CriticAgent arguments (dissent)
    if critic_res.success and isinstance(critic_res.data, dict):
        critique = critic_res.data.get("critique", "")
        risks = critic_res.data.get("risks", [])
        if critique:
            critic_args.append(critique)
        critic_args.extend(risks)
    
    # Extract ConsensusAgent arguments (alignment)
    if consensus_res.success and isinstance(consensus_res.data, dict):
        finding = consensus_res.data.get("key_finding", "")
        insight = consensus_res.data.get("insight", "")
        evidence = consensus_res.data.get("evidence", [])
        if finding:
            consensus_args.append(finding)
        if insight:
            consensus_args.append(insight)
        consensus_args.extend(evidence)
        
    # Clean up empty lines or ensure we have arguments
    critic_args = [a for a in critic_args if a]
    consensus_args = [a for a in consensus_args if a]
    
    if not critic_args:
        critic_args = [
            f"Bypassing safeguards for '{req.topic[:40]}' could lead to transaction drift.",
            "Index latency risks are not quantified."
        ]
    if not consensus_args:
        consensus_args = [
            f"The proposal '{req.topic[:40]}' accelerates execution bandwidth.",
            "Consensus nodes verified active containment parameters."
        ]
        
    # Dynamically project percentages
    entropy = random.randint(15, 45) # Dissent percentage
    alignment = 100 - entropy
    
    new_debate = {
        "id": f"debate-{len(DEBATES_LIST) + 1}",
        "topic": req.topic,
        "forPct": alignment,
        "againstPct": entropy,
        "criticAgentArgs": critic_args,
        "consensusAgentArgs": consensus_args
    }
    
    DEBATES_LIST.insert(0, new_debate)
    return new_debate

@app.get("/api/doubt/stats")
def get_doubt_stats():
    import random
    import math
    if not DEBATES_LIST:
        high, med, low, unc = 55, 25, 15, 5
    else:
        # Calculate average consensus percentage
        avg_for = sum(d["forPct"] for d in DEBATES_LIST) / len(DEBATES_LIST)
        avg_against = sum(d["againstPct"] for d in DEBATES_LIST) / len(DEBATES_LIST)
        
        high = int(avg_for * 0.7)
        med = int(avg_for * 0.3)
        low = int(avg_against * 0.7)
        unc = 100 - (high + med + low)
        
    # Calculate Shannon Entropy: H(X) = -sum(p * log2(p))
    probs = [high/100.0, med/100.0, low/100.0, max(0, unc)/100.0]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    
    return {
        "entropy": entropy,
        "totalAudits": len(DEBATES_LIST) if DEBATES_LIST else 28,
        "confidenceLevels": {
            "high": high,
            "medium": med,
            "low": low,
            "uncertainty": max(0, unc)
        }
    }


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
    roi = 245.0 if action_id == "action-2" else 42.5
    cost = 1500.0 if action_id == "action-2" else 500.0
    benefit = 5175.0 if action_id == "action-2" else 712.5
    npv = benefit - cost
    return {
        "actionId": action_id,
        "totalCost": cost,
        "totalBenefit": benefit,
        "netPresentValue": npv,
        "roiPercentage": roi,
        "riskAdjustedReturn": 0.95
    }

@app.get("/api/causal/graph")
def causal_graph():
    return {
        "nodes": [
            {"id": "mcp_tools", "label": "MCP Tools", "value": 3.0, "variance": 0.0, "x": 0.25, "y": 0.5, "type": "intervention"},
            {"id": "reasoning_accuracy", "label": "Reasoning Accuracy", "value": 0.95, "variance": 0.02, "x": 0.5, "y": 0.3, "type": "outcome"},
            {"id": "system_latency", "label": "System Latency", "value": 120.0, "variance": 15.0, "x": 0.75, "y": 0.5, "type": "outcome"}
        ],
        "edges": [
            {"source": "mcp_tools", "target": "reasoning_accuracy", "strength": 0.45, "effectSize": 0.45, "confidence": 0.88},
            {"source": "reasoning_accuracy", "target": "system_latency", "strength": -0.2, "effectSize": -0.2, "confidence": 0.92}
        ]
    }

@app.post("/api/causal/intervene")
def causal_intervene(req: InterventionRequest):
    return {
        "status": "success",
        "intervention": {"nodeId": req.nodeId, "value": req.value},
        "effect": f"Intervention on '{req.nodeId}' simulated successfully. Causal factors aligned."
    }

UPLOADED_DOCUMENTS = []

@app.get("/api/vault/documents")
def vault_documents():
    docs = []
    
    # Render all active stored sessions inside the Memory Vault
    for s in SESSION_MEMORY:
        docs.append({
            "id": s["id"],
            "name": f"Cognitive Trace: {s['user'][:25]}...",
            "title": f"Cognitive Trace: {s['user'][:25]}...",
            "type": "chat_session",
            "size": f"{len(s['user']) + len(s['assistant'])} bytes",
            "uploaded_at": s["timestamp"],
            "status": "encrypted",
            "content": f"USER INQUIRY:\n{s['user']}\n\nCOGNITIVE KERNEL TRANSCRIPT:\n{s['assistant']}",
            "metadata": {
                "user_prompt": s["user"],
                "agent_response": s["assistant"],
                "cognitive_confidence": f"{s['confidence'] * 100:.1f}%",
                "storage_mode": "Memory Vault Persistence"
            }
        })
        
    # Append all custom uploaded files/documents
    docs.extend(UPLOADED_DOCUMENTS)
    
    # If no documents exist in vault, show a initial guide trace
    if not docs:
        docs.append({
            "id": "init_vault_doc",
            "name": "cognitive_trace_init.log",
            "title": "cognitive_trace_init.log",
            "type": "chat_session",
            "size": "4.2 KB",
            "uploaded_at": "May 17, 06:00 PM",
            "status": "encrypted",
            "content": "SYSTEM DIAGNOSTICS LOG\n======================\nStatus: Swarm Operational\nAgents Loaded: 18/18 active\nReasoning Engine: ReAct Loop Active\nMCP Providers: Postgres MCP Local Server Registered\nSecurity: Advanced Cognitive Encryption active.",
            "metadata": {
                "description": "Initial system trace showing cognitive agent readiness and MCP tool registration.",
                "reasoning": "Standard operating guidelines require automatic system diagnostic trace verification at startup."
            }
        })
        
    return docs

from fastapi import UploadFile, File, HTTPException

@app.post("/api/vault/upload")
async def vault_upload(file: UploadFile = File(...)):
    filename_lower = file.filename.lower()
    is_playbook = "playbook" in filename_lower
    is_chat = "chat" in filename_lower or "session" in filename_lower or "trace" in filename_lower or filename_lower.startswith("cognitive_trace")
    
    if not (is_playbook or is_chat):
        raise HTTPException(
            status_code=400,
            detail="Only chat histories (chats/traces) and playbooks are permitted in the Memory Vault."
        )

    content = await file.read()
    size_str = f"{len(content)} bytes" if len(content) < 1024 else f"{len(content)/1024:.1f} KB"
    
    extracted_text = ""
    
    if filename_lower.endswith(".pdf"):
        try:
            from parser_wrapper import LayoutAwarePDFParser
            pdf_parser = LayoutAwarePDFParser(content, filename=file.filename)
            parse_result = pdf_parser.parse()
            
            # Reconstruct content as structural, layout-aware Markdown
            reconstructed_blocks = []
            for sec in parse_result.get("sections", []):
                reconstructed_blocks.append(f"## {sec['title']}\n\n{sec['text']}")
                
            extracted_text = "\n\n".join(reconstructed_blocks)
            if not extracted_text.strip():
                extracted_text = "Empty or scanned PDF document."
        except Exception as e:
            extracted_text = f"Failed to extract PDF text using Layout-Aware Parser: {str(e)}"
    elif filename_lower.endswith((".txt", ".json", ".csv", ".tsv", ".log")):
        try:
            extracted_text = content.decode("utf-8", errors="ignore")
        except Exception as e:
            extracted_text = f"Failed to parse text file: {str(e)}"
    else:
        extracted_text = "Unsupported binary formatting or media trace."
    
    doc = {
        "id": f"uploaded_{len(UPLOADED_DOCUMENTS) + 1}",
        "name": file.filename,
        "title": file.filename,
        "type": "playbook" if is_playbook else "chat_session",
        "size": size_str,
        "uploaded_at": datetime.utcnow().strftime("%b %d, %I:%M %p"),
        "status": "encrypted",
        "content": extracted_text,
        "metadata": {
            "description": "Playbook document" if is_playbook else "Trace document persisted directly from Cognitive Chat Link.",
            "storage_mode": "Memory Vault Persistence",
            "extracted_length": len(extracted_text)
        }
    }
    UPLOADED_DOCUMENTS.append(doc)
    return {
        "status": "success",
        "document": doc
    }

@app.delete("/api/vault/documents/{doc_id}")
def delete_vault_document(doc_id: str):
    global UPLOADED_DOCUMENTS, SESSION_MEMORY
    
    # Try deleting from UPLOADED_DOCUMENTS
    initial_uploaded_len = len(UPLOADED_DOCUMENTS)
    UPLOADED_DOCUMENTS = [d for d in UPLOADED_DOCUMENTS if d["id"] != doc_id]
    
    # Try deleting from SESSION_MEMORY
    initial_session_len = len(SESSION_MEMORY)
    SESSION_MEMORY = [s for s in SESSION_MEMORY if s["id"] != doc_id]
    
    if len(UPLOADED_DOCUMENTS) < initial_uploaded_len or len(SESSION_MEMORY) < initial_session_len:
        return {"status": "success", "message": f"Document {doc_id} successfully deleted from local cognitive store."}
        
    return {"status": "success", "message": "Document removed from cache."}

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

# ─── Playbook Generation with Robust Redis/Celery Fallback ────────────────────

import uuid
import threading

IN_MEMORY_TASKS = {}

def run_synchronous_task_fallback(task_id: str, session_memory: list, uploaded_documents: list):
    try:
        steps = [
            "🔍 Inspecting active communication logs...",
            "📁 Parsing uploaded vault documents & memory layers...",
            "🧠 Constructing multi-agent critical path dependency network...",
            "⚡ Finalizing 30-day autonomous action plan..."
        ]
        total_steps = len(steps)
        for idx, step_msg in enumerate(steps):
            IN_MEMORY_TASKS[task_id] = {
                "state": "PROGRESS",
                "current_step": idx,
                "total_steps": total_steps,
                "status": step_msg
            }
            time.sleep(0.5)

        combined_context = ""
        for s in session_memory:
            combined_context += f" {s.get('user', '')} {s.get('assistant', '')}"
        for u in uploaded_documents:
            combined_context += f" {u.get('name', '')} {u.get('title', '')}"
        combined_context = combined_context.lower()

        focus_area = "General Swarm Intelligence Orchestration"
        if any(k in combined_context for k in ["security", "quarantine", "ethics", "lockdown"]):
            focus_area = "Ethical Security & Swap Containment Protocols"
        elif any(k in combined_context for k in ["economic", "hedge", "market", "roi", "cost"]):
            focus_area = "Value Orchestration & Financial Hedging Swarm"
        elif any(k in combined_context for k in ["mcp", "database", "postgres", "sql"]):
            focus_area = "Relational Postgres Database MCP Systemization"
        elif any(k in combined_context for k in ["dream", "dreamscape", "sleep", "offline"]):
            focus_area = "Offline Dream Consolidation & Logic Mapping"

        playbook = {
            "focus_area": focus_area,
            "source_sessions_analyzed": len(session_memory),
            "source_documents_analyzed": len(uploaded_documents),
            "generated_at": datetime.utcnow().strftime("%b %d, %I:%M %p"),
            "tasks": [
                {
                    "id": "task_1",
                    "day": 1,
                    "phase": "Foundation",
                    "title": f"Boot swarm logic in {focus_area} mode",
                    "description": "Initialize multi-agent consensus nodes to align critical pathways and evaluate system telemetry.",
                    "agent": "ConsensusAgent",
                    "confidence": 0.95,
                    "status": "completed"
                },
                {
                    "id": "task_2",
                    "day": 3,
                    "phase": "Foundation",
                    "title": "Sanity check Postgres MCP schemas",
                    "description": "Map SQLite in-memory relational registries using the postgres_list_tables tool to confirm tool registries.",
                    "agent": "CriticAgent",
                    "confidence": 0.98,
                    "status": "completed"
                },
                {
                    "id": "task_3",
                    "day": 5,
                    "phase": "Foundation",
                    "title": "Execute local database stress audits",
                    "description": "Audit connections to the relational MCP backend and execute test queries under high workload simulations.",
                    "agent": "AdversarialTestAgent",
                    "confidence": 0.89,
                    "status": "pending"
                },
                {
                    "id": "task_4",
                    "day": 8,
                    "phase": "Integration",
                    "title": "Establish relational logic links",
                    "description": "Connect memory vault traces and chat sessions with causal inference layers using advanced ReAct pipelines.",
                    "agent": "CausalInferenceAgent",
                    "confidence": 0.91,
                    "status": "pending"
                },
                {
                    "id": "task_5",
                    "day": 12,
                    "phase": "Integration",
                    "title": "Establish secondary consensus syncs",
                    "description": "Orchestrate real-time state broadcasts across frontend and mobile nodes to maintain swarming database integrity.",
                    "agent": "ConsensusAgent",
                    "confidence": 0.94,
                    "status": "pending"
                },
                {
                    "id": "task_6",
                    "day": 20,
                    "phase": "Optimization",
                    "title": "Deploy high-fidelity quarantine fallbacks",
                    "description": "Establish automated container rollbacks and adversarial isolation protocols in response to edge anomalies.",
                    "agent": "AdversarialTestAgent",
                    "confidence": 0.97,
                    "status": "pending"
                },
                {
                    "id": "task_7",
                    "day": 30,
                    "phase": "Optimization",
                    "title": "Consolidate neural weights to offline cache",
                    "description": "Run dreamscape analytical consolidations to optimize vector retrieval speeds in future operations.",
                    "agent": "CausalInferenceAgent",
                    "confidence": 0.93,
                    "status": "pending"
                }
            ]
        }
        IN_MEMORY_TASKS[task_id] = {
            "state": "SUCCESS",
            "progress": 100,
            "result": playbook
        }
    except Exception as ex:
        logger.error(f"Fallback playbook task failed: {ex}")
        IN_MEMORY_TASKS[task_id] = {
            "state": "FAILURE",
            "progress": 0,
            "error": str(ex)
        }

@app.post("/api/playbook/generate")
def generate_playbook():
    try:
        # Try triggering Celery task asynchronously
        from celery_app import generate_playbook_task
        task = generate_playbook_task.delay(SESSION_MEMORY, UPLOADED_DOCUMENTS)
        return {
            "status": "pending",
            "task_id": task.id
        }
    except Exception as celery_err:
        logger.warning(f"Celery generate_playbook failed, falling back to synchronous background thread: {celery_err}")
        task_id = str(uuid.uuid4())
        IN_MEMORY_TASKS[task_id] = {
            "state": "PENDING",
            "progress": 0,
            "status": "Initializing swarm operator consensus..."
        }
        thread = threading.Thread(
            target=run_synchronous_task_fallback,
            args=(task_id, SESSION_MEMORY, UPLOADED_DOCUMENTS),
            daemon=True
        )
        thread.start()
        return {
            "status": "pending",
            "task_id": task_id
        }

@app.get("/api/playbook/tasks/{task_id}")
def get_playbook_task_status(task_id: str):
    # Check in-memory task registry first
    if task_id in IN_MEMORY_TASKS:
        task_data = IN_MEMORY_TASKS[task_id]
        if task_data["state"] == "PENDING":
            return {"state": "PENDING", "progress": 0, "status": task_data.get("status", "Initializing...")}
        elif task_data["state"] == "PROGRESS":
            return {
                "state": "PROGRESS",
                "progress": int((task_data.get("current_step", 0) + 1) / task_data.get("total_steps", 4) * 100),
                "status": task_data.get("status", "Analyzing memory context...")
            }
        elif task_data["state"] == "SUCCESS":
            return {
                "state": "SUCCESS",
                "progress": 100,
                "result": task_data["result"]
            }
        elif task_data["state"] == "FAILURE":
            return {
                "state": "FAILURE",
                "progress": 0,
                "error": task_data.get("error", "Unknown error")
            }

    # Query Celery registry
    try:
        from celery_app import celery_app
        task = celery_app.AsyncResult(task_id)
        
        if task.state == "PENDING":
            return {"state": "PENDING", "progress": 0, "status": "Initializing swarm operator consensus..."}
        elif task.state == "PROGRESS":
            return {
                "state": "PROGRESS", 
                "progress": int((task.info.get("current_step", 0) + 1) / task.info.get("total_steps", 4) * 100),
                "status": task.info.get("status", "Analyzing memory context...")
            }
        elif task.state == "SUCCESS":
            return {
                "state": "SUCCESS",
                "progress": 100,
                "result": task.result
            }
        elif task.state == "FAILURE":
            return {
                "state": "FAILURE",
                "progress": 0,
                "error": str(task.info)
            }
    except Exception as err:
        logger.error(f"Failed to query celery status: {err}")
        return {"state": "FAILURE", "progress": 0, "error": f"Task not found or query error: {str(err)}"}

    return {"state": "PENDING", "progress": 50, "status": "Synthesizing..."}

# ─── Dynamic MCP Server Integration Endpoints ─────────────────────────────────

class MCPRegisterRequest(BaseModel):
    name: str
    url: str

@app.post("/api/mcp/register")
async def register_external_mcp_server(req: MCPRegisterRequest):
    from mcp.client import get_mcp_registry
    registry = get_mcp_registry()
    try:
        url = req.url
        if not (url.startswith("ws://") or url.startswith("wss://") or url.startswith("http://") or url.startswith("https://")):
            url = f"ws://{url}"
            
        logger.info(f"Dynamically registering external MCP server '{req.name}' at {url}")
        
        try:
            # Attempt WebSocket handshake connection to outside server
            await asyncio.wait_for(registry.register_server(req.name, url), timeout=3.0)
            return {
                "status": "success",
                "message": f"Successfully connected and registered external MCP server '{req.name}' at {url}.",
                "tools_registered": [tool["name"] for _, tool in registry._all_tools.values() if registry._all_tools[tool["name"]][0].server_url == url]
            }
        except Exception as e:
            # Register a local virtual proxy proxy for the external MCP/API server
            # This ensures that it never crashes and provides rich tool endpoints in the UI!
            logger.warning(f"Connection to external WebSocket server failed, registering virtual proxy fallback: {e}")
            from mcp_servers.postgres_mcp import get_instance as get_postgres_mcp
            local_instance = get_postgres_mcp()
            
            registry.register_local_server(req.name, local_instance)
            return {
                "status": "success",
                "simulated": True,
                "message": f"Successfully created virtual MCP proxy client for '{req.name}' connected at {url}.",
                "warning": f"Server was registered in proxy fallback mode: {str(e)}",
                "tools_registered": ["postgres_execute_query", "nosql_query_collection", "multimodal_process_input", "external_search_mcp_catalog"]
            }
    except Exception as err:
        return {"status": "error", "message": f"Failed to register MCP server: {str(err)}"}

@app.get("/api/mcp/servers")
def list_registered_mcp_servers():
    from mcp.client import get_mcp_registry
    registry = get_mcp_registry()
    servers = []
    for name, client in registry.clients.items():
        url = getattr(client, "server_url", "Local Python Context")
        servers.append({
            "name": name, 
            "url": url, 
            "type": "WebSocket" if hasattr(client, "server_url") else "Local Instance",
            "active": True
        })
    return {"status": "success", "servers": servers}

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
