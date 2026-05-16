import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .base_agent import BaseAgent, AgentMessage, AgentResult

class Stance(Enum):
    PRO = "pro"
    CON = "con"
    NEUTRAL = "neutral"

@dataclass
class Argument:
    argument_id: str
    claim: str
    evidence: List[str]
    stance: Stance
    strength: float
    rebuttals: List[str] = field(default_factory=list)

@dataclass
class DebateRound:
    round_number: int
    pro_arguments: List[Argument]
    con_arguments: List[Argument]
    synthesis: Optional[str] = None

class DebateAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "debater",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.arguments: Dict[str, Argument] = {}
        self.rounds: List[DebateRound] = []
        self.topic: Optional[str] = None
        self.max_rounds = config.get("max_rounds", 5)
        self.consensus_threshold = config.get("consensus_threshold", 0.7)
        
    async def initialize(self):
        self.register_skill("debate", self._conduct_debate)
        self.register_skill("argue", self._generate_argument)
        self.register_skill("rebut", self._generate_rebuttal)
        self.register_skill("synthesize", self._synthesize_debate)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "debate")
        
        if skill == "debate":
            return await self._conduct_debate(
                message.content,
                message.metadata.get("rounds", self.max_rounds)
            )
        elif skill == "argue":
            return await self._generate_argument(
                message.content,
                message.metadata.get("stance", "pro")
            )
        elif skill == "rebut":
            return await self._generate_rebuttal(
                message.content,
                message.metadata.get("target_argument")
            )
        elif skill == "synthesize":
            return await self._synthesize_debate()
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _conduct_debate(
        self,
        topic: str,
        rounds: int
    ) -> AgentResult:
        self.topic = topic
        self.arguments.clear()
        self.rounds.clear()
        
        for round_num in range(1, rounds + 1):
            pro_args = await self._generate_stance_arguments(topic, Stance.PRO, round_num)
            con_args = await self._generate_stance_arguments(topic, Stance.CON, round_num)
            
            for arg in pro_args:
                self.arguments[arg.argument_id] = arg
            for arg in con_args:
                self.arguments[arg.argument_id] = arg
                
            if round_num > 1:
                await self._generate_rebuttals_for_round(pro_args, con_args)
                
            debate_round = DebateRound(
                round_number=round_num,
                pro_arguments=pro_args,
                con_arguments=con_args
            )
            self.rounds.append(debate_round)
            
        synthesis = await self._synthesize_debate()
        
        pro_strength = sum(a.strength for a in self.arguments.values() if a.stance == Stance.PRO)
        con_strength = sum(a.strength for a in self.arguments.values() if a.stance == Stance.CON)
        
        winner = "pro" if pro_strength > con_strength * 1.2 else "con" if con_strength > pro_strength * 1.2 else "tie"
        
        return AgentResult(
            success=True,
            data={
                "topic": topic,
                "rounds_conducted": len(self.rounds),
                "total_arguments": len(self.arguments),
                "pro_strength": round(pro_strength, 4),
                "con_strength": round(con_strength, 4),
                "winner": winner,
                "synthesis": synthesis,
                "key_arguments": {
                    "pro": [
                        {
                            "claim": a.claim,
                            "strength": round(a.strength, 4)
                        }
                        for a in sorted(
                            [arg for arg in self.arguments.values() if arg.stance == Stance.PRO],
                            key=lambda x: x.strength,
                            reverse=True
                        )[:3]
                    ],
                    "con": [
                        {
                            "claim": a.claim,
                            "strength": round(a.strength, 4)
                        }
                        for a in sorted(
                            [arg for arg in self.arguments.values() if arg.stance == Stance.CON],
                            key=lambda x: x.strength,
                            reverse=True
                        )[:3]
                    ]
                }
            }
        )
        
    async def _generate_argument(
        self,
        claim: str,
        stance_str: str
    ) -> AgentResult:
        stance = Stance(stance_str)
        
        argument = Argument(
            argument_id=f"arg_{len(self.arguments)}",
            claim=claim,
            evidence=self._generate_evidence(claim, stance),
            stance=stance,
            strength=self._assess_argument_strength(claim, stance)
        )
        
        self.arguments[argument.argument_id] = argument
        
        return AgentResult(
            success=True,
            data={
                "argument_id": argument.argument_id,
                "claim": claim,
                "stance": stance.value,
                "strength": round(argument.strength, 4),
                "evidence_count": len(argument.evidence)
            }
        )
        
    async def _generate_rebuttal(
        self,
        argument_id: str,
        target_id: Optional[str]
    ) -> AgentResult:
        if target_id not in self.arguments:
            return AgentResult(
                success=False,
                error=f"Target argument {target_id} not found"
            )
            
        target = self.arguments[target_id]
        rebuttal_stance = Stance.PRO if target.stance == Stance.CON else Stance.CON
        
        rebuttal_claim = f"Counter to: {target.claim}"
        rebuttal = Argument(
            argument_id=f"reb_{len(self.arguments)}",
            claim=rebuttal_claim,
   Here are the next 10 coding files with full implementations:

---

## 1. `backend/python/agents/action_priority_agent.py`

```python
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