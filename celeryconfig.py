"""
Celery Configuration
"""
import os

broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

task_track_started = True
task_time_limit = 3600
worker_prefetch_multiplier = 1
worker_concurrency = 4

task_routes = {
    "tasks.agent_tasks.*": {"queue": "agents"},
    "tasks.simulation_tasks.*": {"queue": "simulation"},
    "tasks.rag_tasks.*": {"queue": "rag"},
}

task_default_queue = "default"