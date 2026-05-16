import os
import json
import time
import hashlib
import hmac
from typing import Any, Dict, List, Optional, Callable
from urllib.parse import urljoin, urlencode
from dataclasses import dataclass, asdict
from enum import Enum


class AgentCapability(Enum):
    REASONING = "reasoning"
    PLANNING = "planning"
    EXECUTION = "execution"
    MEMORY = "memory"
    PERCEPTION = "perception"
    COMMUNICATION = "communication"
    LEARNING = "learning"


@dataclass
class AgentDefinition:
    name: str
    version: str
    capabilities: List[AgentCapability]
    model: str
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: Optional[str] = None
    tools: Optional[List[str]] = None
    memory_enabled: bool = False
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TaskRequest:
    task_id: str
    agent_name: str
    input_data: Dict[str, Any]
    priority: int = 5
    timeout_seconds: int = 300
    dependencies: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class TaskResult:
    task_id: str
    status: str
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
    tokens_used: Optional[int] = None
    confidence: Optional[float] = None


class AntigravityTool:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.antigravity.ai",
        org_id: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("ANTIGRAVITY_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.org_id = org_id or os.getenv("ANTIGRAVITY_ORG_ID")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Organization-ID": self.org_id or "",
        }
        self._agent_registry: Dict[str, AgentDefinition] = {}
        self._task_callbacks: Dict[str, Callable] = {}
        self._webhook_secret = os.getenv("ANTIGRAVITY_WEBHOOK_SECRET")

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        import requests

        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params,
            timeout=120,
            stream=stream,
        )
        response.raise_for_status()

        if stream:
            return {"stream": response.iter_lines()}

        return response.json()

    def register_agent(self, agent_def: AgentDefinition) -> Dict[str, Any]:
        payload = {
            "name": agent_def.name,
            "version": agent_def.version,
            "capabilities": [c.value for c in agent_def.capabilities],
            "model": agent_def.model,
            "temperature": agent_def.temperature,
            "max_tokens": agent_def.max_tokens,
            "system_prompt": agent_def.system_prompt,
            "tools": agent_def.tools,
            "memory_enabled": agent_def.memory_enabled,
            "metadata": agent_def.metadata,
        }
        result = self._request("POST", "/v1/agents/register", payload)
        self._agent_registry[agent_def.name] = agent_def
        return result

    def get_agent(self, agent_name: str) -> Optional[AgentDefinition]:
        return self._agent_registry.get(agent_name)

    def list_agents(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/v1/agents")

    def unregister_agent(self, agent_name: str) -> Dict[str, Any]:
        if agent_name in self._agent_registry:
            del self._agent_registry[agent_name]
        return self._request("DELETE", f"/v1/agents/{agent_name}")

    def deploy_agent(
        self,
        agent_name: str,
        environment: str = "production",
        replicas: int = 1,
        resources: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "agent_name": agent_name,
            "environment": environment,
            "replicas": replicas,
        }
        if resources:
            payload["resources"] = resources
        return self._request("POST", "/v1/agents/deploy", payload)

    def undeploy_agent(self, agent_name: str, environment: str = "production") -> Dict[str, Any]:
        return self._request(
            "POST",
            f"/v1/agents/{agent_name}/undeploy",
            {"environment": environment},
        )

    def submit_task(self, task: TaskRequest, callback: Optional[Callable] = None) -> TaskResult:
        payload = {
            "task_id": task.task_id,
            "agent_name": task.agent_name,
            "input_data": task.input_data,
            "priority": task.priority,
            "timeout_seconds": task.timeout_seconds,
            "dependencies": task.dependencies or [],
            "context": task.context,
        }

        if callback:
            self._task_callbacks[task.task_id] = callback
            payload["webhook_url"] = f"{self.base_url}/webhooks/tasks/{task.task_id}"

        result = self._request("POST", "/v1/tasks", payload)
        return TaskResult(
            task_id=result.get("task_id", task.task_id),
            status=result.get("status", "pending"),
            output=result.get("output"),
            error=result.get("error"),
            execution_time_ms=result.get("execution_time_ms"),
            tokens_used=result.get("tokens_used"),
            confidence=result.get("confidence"),
        )

    def get_task_status(self, task_id: str) -> TaskResult:
        result = self._request("GET", f"/v1/tasks/{task_id}")
        return TaskResult(
            task_id=result.get("task_id", task_id),
            status=result.get("status", "unknown"),
            output=result.get("output"),
            error=result.get("error"),
            execution_time_ms=result.get("execution_time_ms"),
            tokens_used=result.get("tokens_used"),
            confidence=result.get("confidence"),
        )

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        return self._request("POST", f"/v1/tasks/{task_id}/cancel")

    def list_tasks(
        self,
        agent_name: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if agent_name:
            params["agent_name"] = agent_name
        if status:
            params["status"] = status
        return self._request("GET", "/v1/tasks", params=params)

    def stream_task(self, task_id: str):
        return self._request("GET", f"/v1/tasks/{task_id}/stream", stream=True)

    def create_workflow(
        self,
        name: str,
        steps: List[Dict[str, Any]],
        triggers: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "steps": steps,
        }
        if triggers:
            payload["triggers"] = triggers
        if metadata:
            payload["metadata"] = metadata
        return self._request("POST", "/v1/workflows", payload)

    def execute_workflow(
        self,
        workflow_id: str,
        inputs: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {}
        if inputs:
            payload["inputs"] = inputs
        return self._request("POST", f"/v1/workflows/{workflow_id}/execute", payload)

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/v1/workflows/{workflow_id}")

    def list_workflows(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._request("GET", "/v1/workflows", params={"limit": limit})

    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/v1/workflows/{workflow_id}")

    def get_knowledge_base(self, kb_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/v1/knowledge/{kb_id}")

    def query_knowledge_base(
        self,
        kb_id: str,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "query": query,
            "top_k": top_k,
        }
        if filter_metadata:
            payload["filter"] = filter_metadata
        return self._request("POST", f"/v1/knowledge/{kb_id}/query", payload)

    def add_to_knowledge_base(
        self,
        kb_id: str,
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        payload = {"documents": documents}
        return self._request("POST", f"/v1/knowledge/{kb_id}/documents", payload)

    def create_knowledge_base(
        self,
        name: str,
        embedding_model: str = "text-embedding-3-large",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "embedding_model": embedding_model,
        }
        if metadata:
            payload["metadata"] = metadata
        return self._request("POST", "/v1/knowledge", payload)

    def get_metrics(
        self,
        agent_name: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {}
        if agent_name:
            params["agent_name"] = agent_name
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return self._request("GET", "/v1/metrics", params=params)

    def get_billing_usage(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", "/v1/billing/usage", params=params)

    def validate_webhook(self, payload: bytes, signature: str) -> bool:
        if not self._webhook_secret:
            return False
        expected = hmac.new(
            self._webhook_secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def handle_webhook(self, payload: bytes, signature: str) -> Optional[TaskResult]:
        if not self.validate_webhook(payload, signature):
            return None

        data = json.loads(payload)
        task_id = data.get("task_id")
        if task_id and task_id in self._task_callbacks:
            result = TaskResult(
                task_id=task_id,
                status=data.get("status"),
                output=data.get("output"),
                error=data.get("error"),
                execution_time_ms=data.get("execution_time_ms"),
                tokens_used=data.get("tokens_used"),
                confidence=data.get("confidence"),
            )
            self._task_callbacks[task_id](result)
            del self._task_callbacks[task_id]
            return result
        return None

    def get_organization(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/org")

    def update_organization(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PATCH", "/v1/org", settings)

    def list_api_keys(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/v1/api-keys")

    def create_api_key(
        self,
        name: str,
        permissions: List[str],
        expires_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "permissions": permissions,
        }
        if expires_at:
            payload["expires_at"] = expires_at
        return self._request("POST", "/v1/api-keys", payload)

    def revoke_api_key(self, key_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/v1/api-keys/{key_id}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_url": self.base_url,
            "authenticated": self.api_key is not None,
            "org_id": self.org_id,
            "registered_agents": list(self._agent_registry.keys()),
        }