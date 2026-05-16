from fastapi import APIRouter

from . import ingest, insights, actions, simulate, agents, memory, playbook
from . import vault, causal, explain, debate, economic, temporal, dream
from . import premonition, health

api_router = APIRouter()

api_router.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
api_router.include_router(simulate.router, prefix="/simulate", tags=["simulation"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(playbook.router, prefix="/playbooks", tags=["playbooks"])
api_router.include_router(vault.router, prefix="/vault", tags=["vault"])
api_router.include_router(causal.router, prefix="/causal", tags=["causal"])
api_router.include_router(explain.router, prefix="/explain", tags=["explainability"])
api_router.include_router(debate.router, prefix="/debate", tags=["debate"])
api_router.include_router(economic.router, prefix="/economic", tags=["economic"])
api_router.include_router(temporal.router, prefix="/temporal", tags=["temporal"])
api_router.include_router(dream.router, prefix="/dream", tags=["dream"])
api_router.include_router(premonition.router, prefix="/premonition", tags=["premonition"])
api_router.include_router(health.router, prefix="/health", tags=["health"])