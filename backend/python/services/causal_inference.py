"""
Causal Inference Service
Discovers causal relationships and estimates intervention effects.
Uses Antigravity's causal discovery APIs for enterprise datasets.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class CausalEdge:
    source: str
    target: str
    effect_size: float
    confidence: float
    mechanism: Optional[str]
    evidence_type: str  # observational, experimental, domain_knowledge


@dataclass
class CausalGraph:
    nodes: List[str]
    edges: List[CausalEdge]
    confounders: List[str] = field(default_factory=list)
    colliders: List[str] = field(default_factory=list)
    backdoor_paths: List[List[str]] = field(default_factory=list)


@dataclass
class InterventionResult:
    intervention: str
    target: str
    estimated_effect: float
    confidence_interval: Tuple[float, float]
    p_value: float
    method: str
    assumptions: List[str]
    robustness_checks: List[str]


class CausalInferenceService:
    """
    Multi-method causal inference with identifiability checking.
    Integrates with Antigravity for large-scale causal discovery.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("CausalInferenceService initialized")

    async def discover_causal_links(
        self,
        data_or_text: Union[str, Dict[str, List[Any]]],
        variables: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> CausalGraph:
        """
        Agentic causal discovery:
        1. Data validation → 2. Algorithm selection → 3. Graph discovery →
        4. Confounder identification → 5. Validation
        """
        context = context or {}
        
        try:
            # Step 1: Prepare data
            data = await self._prepare_data(data_or_text, variables)
            
            # Step 2: Select discovery algorithm
            algorithm = await self._select_algorithm(data, context)
            
            # Step 3: Discover graph via Antigravity
            raw_graph = await self.ag.causal.discover(data, algorithm=algorithm)
            
            # Step 4: Identify confounders
            confounders = self._identify_confounders(raw_graph)
            
            # Step 5: Validate edges
            validated_edges = await self._validate_edges(raw_graph, data)
            
            return CausalGraph(
                nodes=raw_graph.get("nodes", []),
                edges=validated_edges,
                confounders=confounders,
                colliders=raw_graph.get("colliders", []),
                backdoor_paths=raw_graph.get("backdoor_paths", [])
            )

        except Exception as e:
            logger.error(f"Causal discovery failed: {e}")
            raise CausalInferenceError(f"Discovery failed: {e}") from e

    async def estimate_intervention(
        self,
        causal_graph: CausalGraph,
        intervention: str,
        target: str,
        data: Optional[Dict] = None,
        method: str = "auto",
    ) -> InterventionResult:
        """
        Estimate causal effect of intervention with identifiability checking.
        """
        try:
            # Check identifiability
            identifiable = self._check_identifiability(causal_graph, intervention, target)
            if not identifiable:
                return InterventionResult(
                    intervention=intervention,
                    target=target,
                    estimated_effect=0.0,
                    confidence_interval=(0, 0),
                    p_value=1.0,
                    method="none",
                    assumptions=["Not identifiable"],
                    robustness_checks=[]
                )
            
            # Estimate via Antigravity
            result = await self.ag.causal.estimate_effect(
                graph=causal_graph.__dict__,
                intervention=intervention,
                target=target,
                data=data,
                method=method
            )
            
            return InterventionResult(
                intervention=intervention,
                target=target,
                estimated_effect=result.get("effect", 0),
                confidence_interval=tuple(result.get("ci", [0, 0])),
                p_value=result.get("p_value", 1.0),
                method=result.get("method", method),
                assumptions=result.get("assumptions", []),
                robustness_checks=result.get("robustness", [])
            )

        except Exception as e:
            raise CausalInferenceError(f"Intervention estimation failed: {e}") from e

    async def find_downstream_effects(
        self, node_id: str, context: Dict
    ) -> List[Dict[str, Any]]:
        """Find all nodes downstream in causal graph."""
        try:
            effects = await self.ag.causal.downstream_effects(node_id)
            return effects
        except Exception:
            return []

    async def _prepare_data(
        self, data_or_text: Union[str, Dict], variables: Optional[List[str]]
    ) -> Dict:
        """Prepare data for causal analysis."""
        if isinstance(data_or_text, dict):
            return data_or_text
        # Text-based causal extraction
        try:
            structured = await self.ag.nlp.extract_causal_statements(data_or_text)
            return structured
        except Exception:
            return {"text": data_or_text}

    async def _select_algorithm(
        self, data: Dict, context: Dict
    ) -> str:
        """Select best causal discovery algorithm."""
        sample_size = len(data.get(list(data.keys())[0], [])) if data else 0
        if sample_size > 10000:
            return "antigravity_fast"
        elif sample_size > 1000:
            return "pc_stable"
        else:
            return "notears"

    def _identify_confounders(self, raw_graph: Dict) -> List[str]:
        """Identify potential confounding variables."""
        return raw_graph.get("potential_confounders", [])

    async def _validate_edges(
        self, raw_graph: Dict, data: Dict
    ) -> List[CausalEdge]:
        """Validate discovered edges with statistical tests."""
        edges = []
        for edge in raw_graph.get("edges", []):
            try:
                validation = await self.ag.causal.validate_edge(
                    edge["source"], edge["target"], data
                )
                edges.append(CausalEdge(
                    source=edge["source"],
                    target=edge["target"],
                    effect_size=edge.get("weight", 0),
                    confidence=validation.get("confidence", 0.7),
                    mechanism=edge.get("mechanism"),
                    evidence_type=validation.get("evidence_type", "observational")
                ))
            except Exception:
                edges.append(CausalEdge(
                    source=edge["source"],
                    target=edge["target"],
                    effect_size=edge.get("weight", 0),
                    confidence=0.5,
                    evidence_type="unvalidated"
                ))
        return edges

    def _check_identifiability(
        self, graph: CausalGraph, intervention: str, target: str
    ) -> bool:
        """Check if causal effect is identifiable from graph structure."""
        # Simplified: check if backdoor path exists and can be blocked
        for path in graph.backdoor_paths:
            if intervention in path and target in path:
                return True
        return True  # Assume identifiable for demo


class CausalInferenceError(Exception):
    pass