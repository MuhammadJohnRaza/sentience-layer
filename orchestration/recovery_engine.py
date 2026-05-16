import asyncio
import uuid
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

class RecoveryStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"

@dataclass
class RecoveryStep:
    id: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    delay_seconds: int = 0
    retry_on_fail: bool = True
    max_retries: int = 3
    timeout_seconds: int = 60

@dataclass
class RecoveryPlan:
    plan_id: str
    failure_id: str
    failure_type: str
    steps: List[RecoveryStep] = field(default_factory=list)
    estimated_duration: int = 0
    success_probability: float = 0.0
    status: RecoveryStatus = RecoveryStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    executed_steps: List[Dict[str, Any]] = field(default_factory=list)

class RecoveryEngine:
    def __init__(self):
        self._plans: Dict[str, RecoveryPlan] = {}
        self._strategies: Dict[str, Callable] = {}
        self._lock = asyncio.Lock()
        self._register_default_strategies()

    def _register_default_strategies(self):
        self._strategies = {
            "timeout": self._timeout_recovery,
            "connection_error": self._connection_recovery,
            "resource_exhausted": self._resource_recovery,
            "service_unavailable": self._service_recovery,
            "data_corruption": self._data_recovery,
            "state_inconsistency": self._state_recovery
        }

    async def generate_plan(
        self,
        failure_id: str,
        failure_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RecoveryPlan:
        strategy = self._strategies.get(failure_type, self._generic_recovery)
        steps = await strategy(context or {})
        
        plan = RecoveryPlan(
            plan_id=f"rec_{uuid.uuid4().hex[:8]}",
            failure_id=failure_id,
            failure_type=failure_type,
            steps=steps,
            estimated_duration=sum(s.delay_seconds + s.timeout_seconds for s in steps),
            success_probability=self._estimate_success(steps)
        )
        
        async with self._lock:
            self._plans[plan.plan_id] = plan
        
        logger.info(f"Recovery plan generated: {plan.plan_id} for {failure_type}")
        return plan

    async def execute_plan(self, plan_id: str) -> RecoveryPlan:
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Recovery plan not found: {plan_id}")
        
        plan.status = RecoveryStatus.IN_PROGRESS
        
        for step in plan.steps:
            result = await self._execute_step(step)
            plan.executed_steps.append(result)
            
            if not result["success"] and not step.retry_on_fail:
                plan.status = RecoveryStatus.FAILED
                plan.completed_at = datetime.utcnow()
                return plan
        
        success_count = sum(1 for s in plan.executed_steps if s["success"])
        
        if success_count == len(plan.steps):
            plan.status = RecoveryStatus.SUCCESS
        elif success_count > 0:
            plan.status = RecoveryStatus.PARTIAL
        else:
            plan.status = RecoveryStatus.FAILED
        
        plan.completed_at = datetime.utcnow()
        logger.info(f"Recovery plan completed: {plan_id} - {plan.status.value}")
        
        return plan

    async def _execute_step(self, step: RecoveryStep) -> Dict[str, Any]:
        if step.delay_seconds > 0:
            await asyncio.sleep(step.delay_seconds)
        
        for attempt in range(step.max_retries):
            try:
                result = await asyncio.wait_for(
                    self._run_action(step.action, step.parameters),
                    timeout=step.timeout_seconds
                )
                return {"step_id": step.id, "success": True, "result": result, "attempt": attempt + 1}
            except asyncio.TimeoutError:
                logger.warning(f"Step timeout: {step.id}, attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"Step failed: {step.id}, attempt {attempt + 1}: {str(e)}")
                if attempt < step.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return {"step_id": step.id, "success": False, "attempt": step.max_retries}

    async def _run_action(self, action: str, parameters: Dict[str, Any]) -> Any:
        # Placeholder for actual action execution
        await asyncio.sleep(0.1)
        return {"action": action, "status": "completed"}

    async def _timeout_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="timeout_1",
                action="increase_timeout",
                parameters={"multiplier": 2},
                delay_seconds=0
            ),
            RecoveryStep(
                id="timeout_2",
                action="retry_request",
                parameters={"max_attempts": 3},
                delay_seconds=1
            )
        ]

    async def _connection_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="conn_1",
                action="check_health",
                parameters={"endpoints": context.get("endpoints", [])},
                delay_seconds=0
            ),
            RecoveryStep(
                id="conn_2",
                action="reconnect",
                parameters={"fallback_endpoints": context.get("fallbacks", [])},
                delay_seconds=2
            ),
            RecoveryStep(
                id="conn_3",
                action="verify_connection",
                parameters={},
                delay_seconds=1
            )
        ]

    async def _resource_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="res_1",
                action="scale_up",
                parameters={"resource_type": context.get("resource_type", "cpu")},
                delay_seconds=0
            ),
            RecoveryStep(
                id="res_2",
                action="clear_cache",
                parameters={},
                delay_seconds=1
            ),
            RecoveryStep(
                id="res_3",
                action="optimize_memory",
                parameters={"target_usage": 0.7},
                delay_seconds=2
            )
        ]

    async def _service_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="svc_1",
                action="restart_service",
                parameters={"service_name": context.get("service_name", "unknown")},
                delay_seconds=0
            ),
            RecoveryStep(
                id="svc_2",
                action="health_check",
                parameters={"timeout": 30},
                delay_seconds=5
            ),
            RecoveryStep(
                id="svc_3",
                action="restore_traffic",
                parameters={"gradual": True},
                delay_seconds=2
            )
        ]

    async def _data_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="data_1",
                action="backup_corrupted",
                parameters={"location": context.get("backup_location", "/tmp")},
                delay_seconds=0
            ),
            RecoveryStep(
                id="data_2",
                action="restore_from_backup",
                parameters={"backup_id": context.get("last_backup_id")},
                delay_seconds=1
            ),
            RecoveryStep(
                id="data_3",
                action="verify_integrity",
                parameters={"checksum": context.get("expected_checksum")},
                delay_seconds=2
            )
        ]

    async def _state_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="state_1",
                action="snapshot_current",
                parameters={},
                delay_seconds=0
            ),
            RecoveryStep(
                id="state_2",
                action="rollback_state",
                parameters={"target_version": context.get("last_known_good")},
                delay_seconds=1
            ),
            RecoveryStep(
                id="state_3",
                action="reconcile_state",
                parameters={"sources": context.get("state_sources", [])},
                delay_seconds=2
            )
        ]

    async def _generic_recovery(self, context: Dict[str, Any]) -> List[RecoveryStep]:
        return [
            RecoveryStep(
                id="generic_1",
                action="log_failure",
                parameters={"severity": "high"},
                delay_seconds=0
            ),
            RecoveryStep(
                id="generic_2",
                action="notify_operators",
                parameters={"channels": ["email", "slack"]},
                delay_seconds=1
            ),
            RecoveryStep(
                id="generic_3",
                action="attempt_restart",
                parameters={"graceful": True},
                delay_seconds=5
            )
        ]

    def _estimate_success(self, steps: List[RecoveryStep]) -> float:
        if not steps:
            return 0.0
        
        base_prob = 0.9
        for step in steps:
            if step.retry_on_fail:
                base_prob *= 0.95
            else:
                base_prob *= 0.85
        
        return round(base_prob, 2)

    async def get_plan_status(self, plan_id: str) -> Optional[Dict[str, Any]]:
        plan = self._plans.get(plan_id)
        if not plan:
            return None
        
        return {
            "plan_id": plan.plan_id,
            "status": plan.status.value,
            "progress": len(plan.executed_steps) / len(plan.steps) if plan.steps else 0,
            "steps_total": len(plan.steps),
            "steps_completed": len(plan.executed_steps),
            "success_probability": plan.success_probability,
            "created_at": plan.created_at.isoformat(),
            "completed_at": plan.completed_at.isoformat() if plan.completed_at else None
        }

    async def rollback(self, target_id: str, target_state: str) -> Dict[str, Any]:
        plan = await self.generate_plan(
            failure_id=target_id,
            failure_type="state_inconsistency",
            context={"last_known_good": target_state}
        )
        
        return await self.execute_plan(plan.plan_id)