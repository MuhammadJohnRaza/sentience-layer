"""
Dream Orchestrator Service
Manages offline learning, memory consolidation, and creative synthesis.
Uses Antigravity's generative sandbox for safe dream environments.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import random
import asyncio

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class DreamScenario:
    id: str
    dream_type: str  # consolidation, counterfactual, creative, adversarial
    seed_data: Dict[str, Any]
    generated_scenarios: List[Dict[str, Any]]
    insights_discovered: List[str]
    confidence: float
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DreamReport:
    dream_id: str
    scenarios_run: int
    insights_novel: List[str]
    insights_validated: List[str]
    memory_consolidation_count: int
    schemas_created: List[str]
    creative_synthesis: List[str]


class DreamOrchestratorService:
    """
    Orchestrates agent 'dreams' for continuous learning and insight generation.
    Integrates with Antigravity for safe generative simulation.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._dream_history: List[DreamReport] = []
        logger.info("DreamOrchestratorService initialized")

    async def dream(
        self,
        memory_fragments: List[Dict[str, Any]],
        dream_type: str = "consolidation",
        num_scenarios: int = 100,
        context: Optional[Dict[str, Any]] = None,
    ) -> DreamReport:
        """
        Agentic dreaming pipeline:
        1. Memory preparation → 2. Scenario generation → 3. Simulation →
        4. Insight extraction → 5. Validation → 6. Consolidation
        """
        context = context or {}
        
        try:
            # Step 1: Prepare memory seeds
            seeds = await self._prepare_seeds(memory_fragments, dream_type)
            
            # Step 2: Generate scenarios in Antigravity sandbox
            scenarios = await self._generate_scenarios(seeds, dream_type, num_scenarios)
            
            # Step 3: Run simulations
            results = await asyncio.gather(*[
                self._simulate_scenario(s, context) for s in scenarios
            ])
            
            # Step 4: Extract insights
            insights = self._extract_insights(results)
            
            # Step 5: Validate insights
            validated = await self._validate_insights(insights)
            
            # Step 6: Consolidate memories
            consolidated = await self._consolidate_memories(memory_fragments, validated)
            
            report = DreamReport(
                dream_id=f"dream-{datetime.utcnow().timestamp()}",
                scenarios_run=num_scenarios,
                insights_novel=[i for i in insights if i not in validated],
                insights_validated=validated,
                memory_consolidation_count=consolidated,
                schemas_created=[f"schema-{i}" for i in validated[:5]],
                creative_synthesis=[r.get("synthesis") for r in results if r.get("synthesis")]
            )
            
            self._dream_history.append(report)
            logger.info(f"Dream complete: {len(validated)} validated insights")
            return report

        except Exception as e:
            logger.error(f"Dream failed: {e}")
            raise DreamOrchestratorError(f"Dream failed: {e}") from e

    async def _prepare_seeds(
        self, fragments: List[Dict], dream_type: str
    ) -> List[Dict]:
        """Prepare memory seeds for dreaming."""
        if dream_type == "consolidation":
            # Group related fragments
            return fragments
        elif dream_type == "counterfactual":
            # Add counterfactual markers
            return [{**f, "counterfactual": True} for f in fragments]
        elif dream_type == "creative":
            # Mix unrelated fragments
            random.shuffle(fragments)
            return fragments
        elif dream_type == "adversarial":
            # Add stress markers
            return [{**f, "adversarial": True} for f in fragments]
        return fragments

    async def _generate_scenarios(
        self,
        seeds: List[Dict],
        dream_type: str,
        num: int
    ) -> List[DreamScenario]:
        """Generate synthetic scenarios."""
        scenarios = []
        for i in range(num):
            try:
                generated = await self.ag.sandbox.generate_scenario(
                    seeds=seeds,
                    dream_type=dream_type,
                    constraints={"safe_mode": True}
                )
                scenarios.append(DreamScenario(
                    id=f"scenario-{i}",
                    dream_type=dream_type,
                    seed_data=seeds[0] if seeds else {},
                    generated_scenarios=generated.get("scenarios", []),
                    insights_discovered=[],
                    confidence=generated.get("confidence", 0.7)
                ))
            except Exception:
                # Fallback: simple variation
                scenarios.append(DreamScenario(
                    id=f"scenario-{i}",
                    dream_type=dream_type,
                    seed_data=seeds[0] if seeds else {},
                    generated_scenarios=[{"variant": i}],
                    insights_discovered=[],
                    confidence=0.5
                ))
        return scenarios

    async def _simulate_scenario(
        self, scenario: DreamScenario, context: Dict
    ) -> Dict[str, Any]:
        """Simulate single dream scenario."""
        try:
            result = await self.ag.sandbox.simulate(
                scenario.generated_scenarios[0] if scenario.generated_scenarios else {},
                context
            )
            return result
        except Exception:
            return {"synthesis": None, "outcome": "unknown"}

    def _extract_insights(self, results: List[Dict]) -> List[str]:
        """Extract insights from simulation results."""
        insights = []
        for r in results:
            if r.get("novel_pattern"):
                insights.append(r["novel_pattern"])
            if r.get("synthesis"):
                insights.append(r["synthesis"])
        return list(set(insights))

    async def _validate_insights(self, insights: List[str]) -> List[str]:
        """Validate insights against real world."""
        validated = []
        for insight in insights:
            try:
                validation = await self.ag.validation.validate_insight(insight)
                if validation.get("valid", False):
                    validated.append(insight)
            except Exception:
                pass
        return validated

    async def _consolidate_memories(
        self, fragments: List[Dict], insights: List[str]
    ) -> int:
        """Consolidate memory fragments into schemas."""
        try:
            consolidation = await self.ag.memory.consolidate(
                fragments=fragments,
                insights=insights
            )
            return consolidation.get("schemas_created", 0)
        except Exception:
            return 0


class DreamOrchestratorError(Exception):
    pass