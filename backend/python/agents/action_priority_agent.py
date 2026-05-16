import heapq
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .base_agent import BaseAgent, AgentMessage, AgentResult

class PriorityLevel(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    DEFERRED = 5

@dataclass
class PriorityTask:
    task_id: str
    description: str
    priority: PriorityLevel
    urgency: float
    importance: float
    effort: float
    deadline: Optional[float] = None
    blocked_by: Set[str] = field(default_factory=set)
    blocking: Set[str] = field(default_factory=set)
    tags: List[str] = field(default_factory=list)

class ActionPriorityAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "action_priority",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.tasks: Dict[str, PriorityTask] = {}
        self.queue: List[Tuple[float, str]] = []
        self.completed: Set[str] = set()
        self.urgency_decay = config.get("urgency_decay", 0.95)
        self.importance_weight = config.get("importance_weight", 0.4)
        self.urgency_weight = config.get("urgency_weight", 0.35)
        self.effort_weight = config.get("effort_weight", 0.25)
        
    async def initialize(self):
        self.register_skill("prioritize", self._prioritize_tasks)
        self.register_skill("schedule", self._schedule_next)
        self.register_skill("block", self._block_task)
        self.register_skill("unblock", self._unblock_task)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "prioritize")
        
        if skill == "prioritize":
            return await self._prioritize_tasks(message.content)
        elif skill == "schedule":
            return await self._schedule_next(
                message.metadata.get("count", 1)
            )
        elif skill == "block":
            return await self._block_task(
                message.content,
                message.metadata.get("blocker")
            )
        elif skill == "unblock":
            return await self._unblock_task(message.content)
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _prioritize_tasks(
        self,
        tasks_data: List[Dict[str, Any]]
    ) -> AgentResult:
        for task_data in tasks_data:
            task = PriorityTask(
                task_id=task_data.get("id", ""),
                description=task_data.get("description", ""),
                priority=PriorityLevel[task_data.get("priority", "MEDIUM")],
                urgency=task_data.get("urgency", 0.5),
                importance=task_data.get("importance", 0.5),
                effort=task_data.get("effort", 1.0),
                deadline=task_data.get("deadline"),
                blocked_by=set(task_data.get("blocked_by", [])),
                tags=task_data.get("tags", [])
            )
            
            self.tasks[task.id] = task
            
        self._rebuild_queue()
        
        return AgentResult(
            success=True,
            data={
                "tasks_prioritized": len(tasks_data),
                "queue_size": len(self.queue),
                "ready_count": len(self._get_ready_tasks())
            },
            confidence=0.9
        )
        
    async def _schedule_next(self, count: int = 1) -> AgentResult:
        ready = self._get_ready_tasks()
        
        if not ready:
            blocked = self._get_blocked_analysis()
            return AgentResult(
                success=True,
                data={
                    "scheduled": [],
                    "message": "No ready tasks available",
                    "blocked_analysis": blocked
                },
                confidence=0.5
            )
            
        scheduled = []
        for _ in range(min(count, len(ready))):
            if not self.queue:
                break
                
            _, task_id = heapq.heappop(self.queue)
            
            if task_id in self.tasks and task_id not in self.completed:
                task = self.tasks[task_id]
                if not task.blocked_by:
                    scheduled.append({
                        "task_id": task_id,
                        "description": task.description,
                        "priority": task.priority.value,
                        "score": self._calculate_score(task)
                    })
                    
        return AgentResult(
            success=True,
            data={
                "scheduled": scheduled,
                "remaining_ready": len(self._get_ready_tasks())
            },
            confidence=0.9
        )
        
    async def _block_task(
        self,
        task_id: str,
        blocker_id: Optional[str]
    ) -> AgentResult:
        if task_id not in self.tasks:
            return AgentResult(
                success=False,
                error=f"Task {task_id} not found"
            )
            
        if blocker_id:
            self.tasks[task_id].blocked_by.add(blocker_id)
            
            if blocker_id in self.tasks:
                self.tasks[blocker_id].blocking.add(task_id)
                
        self._rebuild_queue()
        
        return AgentResult(
            success=True,
            data={
                "task_id": task_id,
                "blocked_by": list(self.tasks[task_id].blocked_by),
                "is_ready": len(self.tasks[task_id].blocked_by) == 0
            }
        )
        
    async def _unblock_task(self, task_id: str) -> AgentResult:
        if task_id not in self.tasks:
            return AgentResult(
                success=False,
                error=f"Task {task_id} not found"
            )
            
        task = self.tasks[task_id]
        
        unblocked_tasks = []
        for blocked_id in list(task.blocking):
            if blocked_id in self.tasks:
                self.tasks[blocked_id].blocked_by.discard(task_id)
                if not self.tasks[blocked_id].blocked_by:
                    unblocked_tasks.append(blocked_id)
                    
        task.blocking.clear()
        self.completed.add(task_id)
        
        self._rebuild_queue()
        
        return AgentResult(
            success=True,
            data={
                "completed": task_id,
                "newly_unblocked": unblocked_tasks,
                "remaining_tasks": len(self.tasks) - len(self.completed)
            }
        )
        
    def _calculate_score(self, task: PriorityTask) -> float:
        priority_score = 1.0 / task.priority.value
        
        urgency_score = task.urgency
        if task.deadline:
            import time
            time_remaining = task.deadline - time.time()
            if time_remaining < 0:
                urgency_score = 1.0
            elif time_remaining < 3600:
                urgency_score = 0.9
            elif time_remaining < 86400:
                urgency_score = 0.7
                
        effort_penalty = 1.0 / (1.0 + task.effort)
        
        return (
            priority_score * 0.3 +
            urgency_score * self.urgency_weight +
            task.importance * self.importance_weight +
            effort_penalty * self.effort_weight
        )
        
    def _get_ready_tasks(self) -> List[PriorityTask]:
        return [
            task for task in self.tasks.values()
            if not task.blocked_by and task.task_id not in self.completed
        ]
        
    def _get_blocked_analysis(self) -> List[Dict[str, Any]]:
        blocked = []
        
        for task_id, task in self.tasks.items():
            if task.blocked_by and task_id not in self.completed:
                blockers = [
                    {
                        "blocker_id": b,
                        "status": "completed" if b in self.completed else "pending"
                    }
                    for b in task.blocked_by
                ]
                
                blocked.append({
                    "task_id": task_id,
                    "description": task.description,
                    "blockers": blockers,
                    "can_progress": all(b["status"] == "completed" for b in blockers)
                })
                
        return blocked
        
    def _rebuild_queue(self):
        self.queue = []
        
        for task_id, task in self.tasks.items():
            if task_id not in self.completed:
                score = -self._calculate_score(task)
                heapq.heappush(self.queue, (score, task_id))
                
    def get_dashboard(self) -> Dict[str, Any]:
        return {
            "total": len(self.tasks),
            "completed": len(self.completed),
            "ready": len(self._get_ready_tasks()),
            "blocked": len(self.tasks) - len(self.completed) - len(self._get_ready_tasks()),
            "top_priority": self.queue[0][1] if self.queue else None
        }