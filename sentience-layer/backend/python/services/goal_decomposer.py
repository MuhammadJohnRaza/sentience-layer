"""
Goal Decomposer Service
Breaks high-level goals into actionable sub-tasks.
Uses Antigravity for hierarchical task planning and dependency mapping.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import hashlib

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class SubTask:
    id: str
    description: str
    parent_id: Optional[str]
    dependencies: List[str]
    estimated_effort_hours: float
    required_skills: List[str]
    success_criteria: List[str]
    is_leaf: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GoalDecomposition:
    goal: str
    subtasks: List[SubTask]
    critical_path: List[str]
    parallel_groups: List[List[str]]
    total_estimated_hours: float
    risk_points: List[str]


class GoalDecomposerService:
    """
    Hierarchical goal decomposition with critical path analysis.
    Integrates with Antigravity for enterprise goal alignment.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("GoalDecomposerService initialized")

    async def decompose(
        self,
        goal: str,
        constraints: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> GoalDecomposition:
        """
        Agentic goal decomposition:
        1. Goal understanding → 2. Hierarchical breakdown → 3. Dependency mapping →
        4. Effort estimation → 5. Critical path identification → 6. Risk analysis
        """
        constraints = constraints or {}
        context = context or {}
        
        try:
            # Step 1: Understand goal via Antigravity
            goal_analysis = await self.ag.planning.analyze_goal(goal, context)
            
            # Step 2: Hierarchical decomposition
            hierarchy = await self._hierarchical_breakdown(goal, goal_analysis, constraints)
            
            # Step 3: Map dependencies
            with_deps = self._map_dependencies(hierarchy)
            
            # Step 4: Estimate effort
            with_effort = await self._estimate_effort(with_deps, context)
            
            # Step 5: Find critical path
            critical_path = self._find_critical_path(with_effort)
            
            # Step 6: Identify parallel groups
            parallel = self._find_parallel_groups(with_effort, critical_path)
            
            # Step 7: Risk analysis
            risks = self._identify_risks(with_effort)
            
            total_hours = sum(t.estimated_effort_hours for t in with_effort)
            
            return GoalDecomposition(
                goal=goal,
                subtasks=with_effort,
                critical_path=critical_path,
                parallel_groups=parallel,
                total_estimated_hours=total_hours,
                risk_points=risks
            )

        except Exception as e:
            logger.error(f"Goal decomposition failed: {e}")
            raise GoalDecompositionError(f"Decomposition failed: {e}") from e

    async def _hierarchical_breakdown(
        self, goal: str, analysis: Dict, constraints: Dict
    ) -> List[SubTask]:
        """Break goal into hierarchical subtasks."""
        subtasks = []
        
        # Get decomposition from Antigravity
        try:
            ag_tasks = await self.ag.planning.decompose(goal, constraints)
            for task in ag_tasks:
                subtasks.append(SubTask(
                    id=task.get("id", f"task-{hashlib.md5(task['description'].encode()).hexdigest()[:8]}"),
                    description=task["description"],
                    parent_id=task.get("parent_id"),
                    dependencies=task.get("dependencies", []),
                    estimated_effort_hours=task.get("effort", 1.0),
                    required_skills=task.get("skills", []),
                    success_criteria=task.get("success_criteria", ["Completed"]),
                    is_leaf=task.get("is_leaf", True),
                    metadata=task.get("metadata", {})
                ))
        except Exception:
            # Fallback: simple binary split
            subtasks = [
                SubTask(
                    id=f"{hashlib.md5(goal.encode()).hexdigest()[:8]}-1",
                    description=f"Research and plan: {goal}",
                    parent_id=None,
                    dependencies=[],
                    estimated_effort_hours=2.0,
                    required_skills=["research"],
                    success_criteria=["Plan documented"]
                ),
                SubTask(
                    id=f"{hashlib.md5(goal.encode()).hexdigest()[:8]}-2",
                    description=f"Execute: {goal}",
                    parent_id=None,
                    dependencies=[f"{hashlib.md5(goal.encode()).hexdigest()[:8]}-1"],
                    estimated_effort_hours=4.0,
                    required_skills=["execution"],
                    success_criteria=["Goal achieved"]
                )
            ]
        
        return subtasks

    def _map_dependencies(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Ensure dependency graph is valid."""
        task_ids = {t.id for t in subtasks}
        for task in subtasks:
            # Remove invalid dependencies
            task.dependencies = [d for d in task.dependencies if d in task_ids]
        return subtasks

    async def _estimate_effort(
        self, subtasks: List[SubTask], context: Dict
    ) -> List[SubTask]:
        """Estimate effort using historical data."""
        for task in subtasks:
            try:
                historical = await self.ag.planning.get_historical_effort(
                    task.description,
                    context.get("team_id")
                )
                if historical:
                    task.estimated_effort_hours = historical.get("median", task.estimated_effort_hours)
            except Exception:
                pass
        return subtasks

    def _find_critical_path(self, subtasks: List[SubTask]) -> List[str]:
        """Find critical path using longest path algorithm."""
        # Simplified: sort by dependencies
        completed = set()
        path = []
        
        while len(path) < len(subtasks):
            for task in subtasks:
                if task.id not in completed and all(d in completed for d in task.dependencies):
                    path.append(task.id)
                    completed.add(task.id)
                    break
            else:
                break  # Circular dependency detected
        
        return path

    def _find_parallel_groups(
        self, subtasks: List[SubTask], critical_path: List[str]
    ) -> List[List[str]]:
        """Find tasks that can execute in parallel."""
        groups = []
        current_group = []
        
        for task_id in critical_path:
            task = next((t for t in subtasks if t.id == task_id), None)
            if task:
                # Tasks with same dependencies can be parallel
                parallel_candidates = [
                    t.id for t in subtasks
                    if t.id != task_id and t.dependencies == task.dependencies
                ]
                if parallel_candidates:
                    current_group.extend([task_id] + parallel_candidates)
                else:
                    if current_group:
                        groups.append(list(set(current_group)))
                        current_group = []
                    groups.append([task_id])
        
        if current_group:
            groups.append(list(set(current_group)))
        
        return groups

    def _identify_risks(self, subtasks: List[SubTask]) -> List[str]:
        """Identify risk points in decomposition."""
        risks = []
        
        # Long tasks are risky
        long_tasks = [t for t in subtasks if t.estimated_effort_hours > 8]
        if long_tasks:
            risks.append(f"Long tasks detected: {len(long_tasks)} tasks > 8 hours")
        
        # Many dependencies are risky
        complex_tasks = [t for t in subtasks if len(t.dependencies) > 3]
        if complex_tasks:
            risks.append(f"Complex dependencies: {len(complex_tasks)} tasks with >3 dependencies")
        
        # Missing skills
        all_skills = set()
        for t in subtasks:
            all_skills.update(t.required_skills)
        if all_skills:
            risks.append(f"Required skills: {', '.join(all_skills)}")
        
        return risks


class GoalDecompositionError(Exception):
    pass