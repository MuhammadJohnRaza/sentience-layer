"""
Impact Analysis Service
Analyzes downstream effects of actions using causal graphs and simulation.
Integrates with Antigravity for enterprise-scale impact modeling.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from .causal_inference import CausalInferenceService

logger = get_logger(__name__)


class ImpactType(Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    CASCADING = "cascading"
    REVERSIBLE = "reversible"
    IRREVERSIBLE = "irreversible"


class ImpactDirection(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    NEUTRAL = "neutral"


@dataclass
class ImpactNode:
    node_id: str
    description: str
    impact_type: ImpactType
    direction: ImpactDirection
    magnitude: float  # 0-1
    confidence: float
    time_horizon: str  # immediate, short, medium, long
    affected_stakeholders: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class ImpactReport:
    action_id: str
    summary: str
    total_impact_score: float
    nodes: List[ImpactNode]
    risk_adjusted_score: float
    irreversible_nodes: List[ImpactNode] = field(default_factory=list)
    mitigation_suggestions: List[str] = field(default_factory=list)


class ImpactAnalysisService:
    """
    Multi-hop impact analysis with causal propagation.
    Uses Antigravity for cross-system impact modeling.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self.causal = CausalInferenceService(self.ag)
        logger.info("ImpactAnalysisService initialized")

    async def analyze(
        self,
        action: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        depth: int = 3,
    ) -> ImpactReport:
        """
        Agentic impact analysis:
        1. Direct effects → 2. Causal propagation → 3. Stakeholder mapping →
        4. Risk adjustment → 5. Mitigation planning
        """
        context = context or {}
        action_id = action.get("id", "unknown")
        
        try:
            # Step 1: Direct impact identification
            direct_nodes = await self._identify_direct_impact(action, context)
            
            # Step 2: Causal propagation (multi-hop)
            all_nodes = await self._propagate_causally(direct_nodes, depth, context)
            
            # Step 3: Stakeholder mapping
            nodes_with_stakeholders = await self._map_stakeholders(all_nodes)
            
            # Step 4: Risk adjustment
            risk_adjusted = self._calculate_risk_adjusted_score(nodes_with_stakeholders)
            
            # Step 5: Mitigation planning
            mitigations = await self._suggest_mitigations(nodes_with_stakeholders)
            
            # Step 6: Antigravity cross-system impact
            cross_system = await self._check_cross_system_impact(action, context)
            nodes_with_stakeholders.extend(cross_system)
            
            irreversible = [n for n in nodes_with_stakeholders if n.impact_type == ImpactType.IRREVERSIBLE]
            
            report = ImpactReport(
                action_id=action_id,
                summary=self._generate_summary(nodes_with_stakeholders),
                total_impact_score=sum(n.magnitude for n in nodes_with_stakeholders) / max(len(nodes_with_stakeholders), 1),
                nodes=nodes_with_stakeholders,
                risk_adjusted_score=risk_adjusted,
                irreversible_nodes=irreversible,
                mitigation_suggestions=mitigations
            )
            
            logger.info(f"Impact analysis complete for {action_id}: {len(report.nodes)} nodes")
            return report

        except Exception as e:
            logger.error(f"Impact analysis failed: {e}")
            raise ImpactAnalysisError(f"Analysis failed: {e}") from e

    async def _identify_direct_impact(
        self, action: Dict[str, Any], context: Dict
    ) -> List[ImpactNode]:
        """Identify immediate effects of action."""
        nodes = []
        
        # Resource impact
        if "cost" in action or "compute" in action:
            nodes.append(ImpactNode(
                node_id=f"{action['id']}-resource",
                description=f"Resource consumption: {action.get('cost', 'unknown cost')}",
                impact_type=ImpactType.DIRECT,
                direction=ImpactDirection.NEGATIVE,
                magnitude=0.3,
                confidence=0.95,
                time_horizon="immediate",
                metrics={"cost": action.get("cost", 0)}
            ))
        
        # State change impact
        if "state_change" in action:
            nodes.append(ImpactNode(
                node_id=f"{action['id']}-state",
                description=f"State mutation: {action['state_change']}",
                impact_type=ImpactType.DIRECT,
                direction=ImpactDirection.MIXED,
                magnitude=0.5,
                confidence=0.9,
                time_horizon="immediate"
            ))
        
        # User impact
        if "affected_users" in action:
            user_count = len(action["affected_users"])
            nodes.append(ImpactNode(
                node_id=f"{action['id']}-users",
                description=f"Affects {user_count} users",
                impact_type=ImpactType.DIRECT,
                direction=ImpactDirection.MIXED,
                magnitude=min(user_count / 100, 1.0),
                confidence=0.85,
                time_horizon="short",
                affected_stakeholders=action["affected_users"]
            ))
        
        return nodes

    async def _propagate_causally(
        self, seed_nodes: List[ImpactNode], depth: int, context: Dict
    ) -> List[ImpactNode]:
        """Propagate impact through causal graph."""
        all_nodes = list(seed_nodes)
        current_layer = list(seed_nodes)
        
        for hop in range(depth):
            next_layer = []
            for node in current_layer:
                try:
                    # Query causal graph for children
                    children = await self.causal.find_downstream_effects(node.node_id, context)
                    for child in children:
                        impact_node = ImpactNode(
                            node_id=f"{node.node_id}-hop{hop}-{child['id']}",
                            description=child.get("description", "Causal downstream effect"),
                            impact_type=ImpactType.CASCADING,
                            direction=ImpactDirection(child.get("direction", "mixed")),
                            magnitude=node.magnitude * 0.7,  # Decay
                            confidence=node.confidence * 0.9,
                            time_horizon=["short", "medium", "long"][min(hop, 2)],
                            affected_stakeholders=child.get("stakeholders", [])
                        )
                        next_layer.append(impact_node)
                except Exception as e:
                    logger.warning(f"Causal propagation failed at hop {hop}: {e}")
            
            all_nodes.extend(next_layer)
            current_layer = next_layer
            if not current_layer:
                break
        
        return all_nodes

    async def _map_stakeholders(self, nodes: List[ImpactNode]) -> List[ImpactNode]:
        """Map affected stakeholders using Antigravity org graph."""
        for node in nodes:
            if not node.affected_stakeholders:
                try:
                    stakeholders = await self.ag.org_graph.find_affected(node.description)
                    node.affected_stakeholders = stakeholders
                except Exception:
                    pass
        return nodes

    def _calculate_risk_adjusted_score(self, nodes: List[ImpactNode]) -> float:
        """Apply risk adjustment to total impact."""
        total = 0.0
        for node in nodes:
            weight = 1.0
            if node.impact_type == ImpactType.IRREVERSIBLE:
                weight = 2.0
            if node.direction == ImpactDirection.NEGATIVE:
                weight *= 1.5
            total += node.magnitude * node.confidence * weight
        
        return total / max(len(nodes), 1)

    async def _suggest_mitigations(self, nodes: List[ImpactNode]) -> List[str]:
        """Generate mitigation strategies."""
        mitigations = []
        
        irreversible = [n for n in nodes if n.impact_type == ImpactType.IRREVERSIBLE]
        if irreversible:
            mitigations.append("Create backup/rollback plan before executing irreversible steps")
        
        high_negative = [n for n in nodes if n.direction == ImpactDirection.NEGATIVE and n.magnitude > 0.5]
        if high_negative:
            mitigations.append("Implement staged rollout to limit blast radius")
        
        many_stakeholders = [n for n in nodes if len(n.affected_stakeholders) > 10]
        if many_stakeholders:
            mitigations.append("Schedule stakeholder communication before execution")
        
        # Antigravity mitigation suggestions
        try:
            ag_mitigations = await self.ag.impact.suggest_mitigations([n.__dict__ for n in nodes])
            mitigations.extend(ag_mitigations)
        except Exception:
            pass
        
        return list(set(mitigations))

    async def _check_cross_system_impact(
        self, action: Dict, context: Dict
    ) -> List[ImpactNode]:
        """Check impact on external systems via Antigravity."""
        nodes = []
        try:
            cross_impacts = await self.ag.systems.check_impact(action.get("system_targets", []))
            for impact in cross_impacts:
                nodes.append(ImpactNode(
                    node_id=f"cross-sys-{impact['system']}",
                    description=f"Cross-system impact on {impact['system']}: {impact['description']}",
                    impact_type=ImpactType.INDIRECT,
                    direction=ImpactDirection(impact.get("direction", "mixed")),
                    magnitude=impact.get("severity", 0.5),
                    confidence=0.8,
                    time_horizon="medium"
                ))
        except Exception:
            pass
        return nodes

    def _generate_summary(self, nodes: List[ImpactNode]) -> str:
        """Generate human-readable impact summary."""
        total_nodes = len(nodes)
        irreversible_count = len([n for n in nodes if n.impact_type == ImpactType.IRREVERSIBLE])
        negative_count = len([n for n in nodes if n.direction == ImpactDirection.NEGATIVE])
        
        return (
            f"Analysis identified {total_nodes} impact nodes "
            f"({irreversible_count} irreversible, {negative_count} negative). "
            f"Stakeholders affected: {sum(len(n.affected_stakeholders) for n in nodes)}"
        )


class ImpactAnalysisError(Exception):
    pass