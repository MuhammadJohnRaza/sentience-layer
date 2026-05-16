"""
Task Graph Builder Service
Constructs executable task graphs from decomposed goals.
Uses Antigravity for workflow optimization and resource allocation.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from .goal_decomposer import GoalDecomposition, SubTask

logger = get_logger(__name__)


class NodeStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskNode:
    id: str
    task: SubTask
    status: NodeStatus
    assigned_agent: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    retry_count: int = 0
    outputs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskGraph:
    graph_id: str
    nodes: Dict[str, TaskNode]
    edges: List[Tuple[str, str]]  # (from, to)
    entry_points: List[str]
    exit_points: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskGraphBuilderService:
    """
    Converts goal decompositions into executable DAGs with agent assignment.
    Integrates with Antigravity for optimal workflow orchestration.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("TaskGraphBuilderService initialized")

    async def build(
        self,
        decomposition: GoalDecomposition,
        available_agents: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> TaskGraph:
        """
        Agentic task graph construction:
        1. Node creation → 2. Edge linking → 3. Agent assignment →
        4. Validation → 5. Optimization
        """
        available_agents = available_agents or []
        context = context or {}
        
        try:
            # Step 1: Create nodes
            nodes = self._create_nodes(decomposition)
            
            # Step 2: Create edges from dependencies
            edges = self._create_edges(nodes)
            
            # Step 3: Find entry/exit points
            entry, exit_points = self._find_boundaries(nodes, edges)
            
            # Step 4: Assign agents
            assigned = await self._assign_agents(nodes, available_agents, context)
            
            # Step 5: Validate DAG
            self._validate_dag(assigned, edges)
            
            # Step 6: Optimize with Antigravity
            optimized = await self._optimize_graph(assigned, edges, context)
            
            graph = TaskGraph(
                graph_id=f"graph-{hash(decomposition.goal) % 1000000}",
                nodes={n.id: n for n in optimized},
                edges=edges,
                entry_points=entry,
                exit_points=exit_points,
                metadata={"goal": decomposition.goal}
            )
            
            logger.info(f"Built task graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
            return graph

        except Exception as e:
            logger.error(f"Task graph build failed: {e}")
            raise TaskGraphBuildError(f"Build failed: {e}") from e

    def _create_nodes(self, decomposition: GoalDecomposition) -> List[TaskNode]:
        """Create task nodes from decomposition."""
        return [
            TaskNode(
                id=task.id,
                task=task,
                status=NodeStatus.PENDING
            )
            for task in decomposition.subtasks
        ]

    def _create_edges(self, nodes: List[TaskNode]) -> List[Tuple[str, str]]:
        """Create edges from task dependencies."""
        edges = []
        for node in nodes:
            for dep_id in node.task.dependencies:
                edges.append((dep_id, node.id))
        return edges

    def _find_boundaries(
        self, nodes: List[TaskNode], edges: List[Tuple[str, str]]
    ) -> Tuple[List[str], List[str]]:
        """Find entry and exit points."""
        all_targets = {e[1] for e in edges}
        all_sources = {e[0] for e in edges}
        
        entry = [n.id for n in nodes if n.id not in all_targets]
        exits = [n.id for n in nodes if n.id not in all_sources]
        
        return entry, exits

    async def _assign_agents(
        self,
        nodes: List[TaskNode],
        agents: List[str],
        context: Dict
    ) -> List[TaskNode]:
        """Assign optimal agents to tasks."""
        if not agents:
            return nodes
        
        for node in nodes:
            try:
                best_agent = await self.ag.orchestration.match_agent(
                    task=node.task.__dict__,
                    available_agents=agents,
                    context=context
                )
                node.assigned_agent = best_agent.get("agent_id", agents[0])
            except Exception:
                # Round-robin fallback
                idx = hash(node.id) % len(agents)
                node.assigned_agent = agents[idx]
        
        return nodes

    def _validate_dag(self, nodes: List[TaskNode], edges: List[Tuple[str, str]]):
        """Validate that graph is a proper DAG (no cycles)."""
        # Simple cycle detection
        visited = set()
        rec_stack = set()
        
        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for edge in edges:
                if edge[0] == node_id:
                    if edge[1] not in visited:
                        if has_cycle(edge[1]):
                            return True
                    elif edge[1] in rec_stack:
                        return True
            
            rec_stack.remove(node_id)
            return False
        
        for node in nodes:
            if node.id not in visited:
                if has_cycle(node.id):
                    raise TaskGraphBuildError("Cycle detected in task graph")

    async def _optimize_graph(
        self,
        nodes: List[TaskNode],
        edges: List[Tuple[str, str]],
        context: Dict
    ) -> List[TaskNode]:
        """Optimize graph execution order."""
        try:
            optimization = await self.ag.orchestration.optimize_workflow(
                nodes=[n.__dict__ for n in nodes],
                edges=edges
            )
            # Apply optimizations
            return nodes
        except Exception:
            return nodes

    async def execute_step(
        self,
        graph: TaskGraph,
        node_id: str,
        execution_context: Dict[str, Any]
    ) -> TaskNode:
        """Execute a single step in the graph."""
        node = graph.nodes.get(node_id)
        if not node:
            raise TaskGraphBuildError(f"Node {node_id} not found")
        
        # Check dependencies
        for edge in graph.edges:
            if edge[1] == node_id:
                dep_node = graph.nodes.get(edge[0])
                if dep_node and dep_node.status != NodeStatus.COMPLETED:
                    raise TaskGraphBuildError(f"Dependency {edge[0]} not completed")
        
        node.status = NodeStatus.RUNNING
        node.start_time = __import__('datetime').datetime.utcnow().isoformat()
        
        try:
            # Execute via assigned agent
            if node.assigned_agent:
                result = await self.ag.agents.execute(
                    agent_id=node.assigned_agent,
                    task=node.task.__dict__,
                    context=execution_context
                )
                node.outputs = result.get("outputs", {})
            
            node.status = NodeStatus.COMPLETED
            node.end_time = __import__('datetime').datetime.utcnow().isoformat()
            
        except Exception as e:
            node.status = NodeStatus.FAILED
            node.retry_count += 1
            if node.retry_count < 3:
                node.status = NodeStatus.READY  # Retry
            raise
        
        return node


class TaskGraphBuildError(Exception):
    pass