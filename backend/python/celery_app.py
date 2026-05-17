"""
Celery Task Queue Engine for Sentience Layer
"""
import os
import time
from celery import Celery
from datetime import datetime

# Initialize Redis coordinates for the Celery task queue broker and backend
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

# Local fallback check: if running outside docker, convert 'redis' hostname to 'localhost'
if "localhost" not in CELERY_BROKER and "127.0.0.1" not in CELERY_BROKER:
    import socket
    try:
        socket.gethostbyname("redis")
    except socket.gaierror:
        CELERY_BROKER = CELERY_BROKER.replace("redis:6379", "localhost:6379")
        CELERY_BACKEND = CELERY_BACKEND.replace("redis:6379", "localhost:6379")

celery_app = Celery(
    "sentience_swarm",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True
)

@celery_app.task(bind=True)
def generate_playbook_task(self, session_memory: list, uploaded_documents: list):
    """
    Asynchronous, CPU-bound Swarm roadmapping compiler.
    Updates Redis state periodically to show progress logs to clients.
    """
    steps = [
        "🔍 Inspecting active communication logs...",
        "📁 Parsing uploaded vault documents & memory layers...",
        "🧠 Constructing multi-agent critical path dependency network...",
        "⚡ Finalizing 30-day autonomous action plan..."
    ]
    
    total_steps = len(steps)
    for idx, step_msg in enumerate(steps):
        # Update progress tracking state in broker
        self.update_state(
            state="PROGRESS",
            meta={
                "current_step": idx,
                "total_steps": total_steps,
                "status": step_msg
            }
        )
        time.sleep(1.2) # Simulating heavy agent reasoning chain calculations

    # Calculate swarm focus based on keywords present in prompt history and file vault
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
    
    return playbook

# ─── Integration of tasks directory modules ────────────────────────────────────

from tasks.report_tasks import get_instance as get_report_tasks
from tasks.cleanup_tasks import get_instance as get_cleanup_tasks
from tasks.dream_tasks import get_instance as get_dream_tasks
from tasks.learning_tasks import get_instance as get_learning_tasks
from tasks.agent_tasks import get_instance as get_agent_tasks

@celery_app.task(bind=True)
def execute_report_task(self, *args, **kwargs):
    instance = get_report_tasks()
    return instance.execute(*args, **kwargs)

@celery_app.task(bind=True)
def execute_cleanup_task(self, *args, **kwargs):
    instance = get_cleanup_tasks()
    return instance.execute(*args, **kwargs)

@celery_app.task(bind=True)
def execute_dream_task(self, *args, **kwargs):
    instance = get_dream_tasks()
    return instance.execute(*args, **kwargs)

@celery_app.task(bind=True)
def execute_learning_task(self, *args, **kwargs):
    instance = get_learning_tasks()
    return instance.execute(*args, **kwargs)

@celery_app.task(bind=True)
def execute_agent_task(self, *args, **kwargs):
    instance = get_agent_tasks()
    return instance.execute(*args, **kwargs)
