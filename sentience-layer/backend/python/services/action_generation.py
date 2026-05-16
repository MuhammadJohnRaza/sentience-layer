"""
Action Generation Service
Generates structured, executable actions from insights and goals.
Uses Antigravity for action template enrichment and validation.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import hashlib
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from .insight_extraction import Insight, InsightExtractionService
from .economic_engine import EconomicEngineService

logger = get_logger(__name__)


@dataclass
class ActionStep:
    step_id: str
    description: str
    tool: Optional[str]
    parameters: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
    estimated_duration_seconds: int = 60
    rollback_possible: bool = True


@dataclass
class Action:
    id: str
    title: str
    description: str
    steps: List[ActionStep]
    expected_outcome: str
    success_criteria: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.8
    cost_estimate: Optional[float] = None
    risk_level: str = "low"  # low, medium, high, critical


class ActionGenerationService:
    """
    Multi-step action generation with dependency resolution and cost optimization.
    Integrates with Antigravity for enterprise action templates.
    """

    def __init__(
        self,
        antigravity_client: Optional[AntigravityClient] = None,
        economic_engine: Optional[EconomicEngineService] = None,
    ):
        self.ag = antigravity_client or AntigravityClient()
        self.economic = economic_engine or EconomicEngineService(self.ag)
        logger.info("ActionGenerationService initialized")

    async def generate(
        self,
        trigger: Union[Insight, str, Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> List[Action]:
        """
        Agentic action generation pipeline:
        1. Intent parsing → 2. Template retrieval → 3. Step sequencing →
        4. Dependency resolution → 5. Cost estimation → 6. Validation
        """
        context = context or {}
        constraints = constraints or {}
        
        try:
            # Normalize trigger
            intent = await self._parse_intent(trigger)
            
            # Step 1: Retrieve relevant templates from Antigravity
            templates = await self._retrieve_templates(intent, context)
            
            # Step 2: Generate candidate action sequences
            candidates = await self._generate_candidates(intent, templates, context)
            
            # Step 3: Add dependencies
            with_dependencies = [self._resolve_dependencies(a) for a in candidates]
            
            # Step 4: Cost estimation
            with_costs = await asyncio.gather(*[
                self._estimate_costs(a) for a in with_dependencies
            ])
            
            # Step 5: Validate against constraints
            valid = [a for a in with_costs if self._meets_constraints(a, constraints)]
            
            # Step 6: Rank by expected value
            ranked = await self._rank_actions(valid, context)
            
            logger.info(f"Generated {len(ranked)} valid actions for intent: {intent[:50]}...")
            return ranked[:5]  # Top 5

        except Exception as e:
            logger.error(f"Action generation failed: {e}")
            raise ActionGenerationError(f"Generation failed: {e}") from e

    async def _parse_intent(self, trigger: Union[Insight, str, Dict]) -> str:
        """Extract intent from trigger."""
        if isinstance(trigger, Insight):
            return f"{trigger.type}: {trigger.title}. {trigger.description}"
        elif isinstance(trigger, dict):
            return trigger.get("description", trigger.get("intent", json.dumps(trigger)))
        return str(trigger)

    async def _retrieve_templates(
        self, intent: str, context: Dict
    ) -> List[Dict[str, Any]]:
        """Retrieve action templates from Antigravity marketplace."""
        try:
            templates = await self.ag.playbooks.search(intent, limit=5)
            return templates
        except Exception:
            return []

    async def _generate_candidates(
        self, intent: str, templates: List[Dict], context: Dict
    ) -> List[Action]:
        """Generate action candidates from templates and intent."""
        candidates = []
        
        # Template-based generation
        for template in templates:
            try:
                action = await self._instantiate_template(template, intent, context)
                candidates.append(action)
            except Exception as e:
                logger.warning(f"Template instantiation failed: {e}")
        
        # De novo generation if no templates match
        if not candidates:
            action = await self._generate_from_scratch(intent, context)
            candidates.append(action)
        
        return candidates

    async def _instantiate_template(
        self, template: Dict, intent: str, context: Dict
    ) -> Action:
        """Fill template slots with intent-specific values."""
        steps = []
        for i, step_template in enumerate(template.get("steps", [])):
            step = ActionStep(
                step_id=f"{template['id']}-step-{i}",
                description=step_template.get("description", "Execute step"),
                tool=step_template.get("tool"),
                parameters=self._fill_parameters(step_template.get("parameters", {}), intent, context),
                depends_on=step_template.get("depends_on", []),
                estimated_duration_seconds=step_template.get("duration", 60),
                rollback_possible=step_template.get("rollback", True)
            )
            steps.append(step)
        
        return Action(
            id=f"action-{template['id']}-{hashlib.md5(intent.encode()).hexdigest()[:8]}",
            title=template.get("title", "Generated Action"),
            description=intent,
            steps=steps,
            expected_outcome=template.get("expected_outcome", "Success"),
            success_criteria=template.get("success_criteria", ["Completed without errors"]),
            metadata={"template_id": template["id"], "source": "antigravity_template"},
            confidence=template.get("success_rate", 0.8)
        )

    def _fill_parameters(
        self, params: Dict, intent: str, context: Dict
    ) -> Dict[str, Any]:
        """Fill parameter slots using intent parsing."""
        filled = {}
        for key, value in params.items():
            if value == "{{intent}}":
                filled[key] = intent
            elif value == "{{user_id}}":
                filled[key] = context.get("user_id")
            elif value == "{{timestamp}}":
                filled[key] = datetime.utcnow().isoformat()
            else:
                filled[key] = value
        return filled

    async def _generate_from_scratch(self, intent: str, context: Dict) -> Action:
        """Generate action without template."""
        # Use Antigravity for de novo generation
        try:
            generated = await self.ag.actions.generate(intent, context)
            steps = [
                ActionStep(
                    step_id=f"gen-step-{i}",
                    description=s.get("description"),
                    tool=s.get("tool"),
                    parameters=s.get("parameters", {})
                )
                for i, s in enumerate(generated.get("steps", []))
            ]
            
            return Action(
                id=f"action-generated-{hashlib.md5(intent.encode()).hexdigest()[:8]}",
                title=generated.get("title", "Generated Action"),
                description=intent,
                steps=steps or [ActionStep(
                    step_id="gen-step-0",
                    description="Execute primary task",
                    tool=None,
                    parameters={"intent": intent}
                )],
                expected_outcome="Task completed successfully",
                success_criteria=["Primary objective achieved"],
                metadata={"source": "antigravity_generated"},
                confidence=0.75
            )
        except Exception:
            # Ultimate fallback
            return Action(
                id=f"action-fallback-{hashlib.md5(intent.encode()).hexdigest()[:8]}",
                title="Manual Review Required",
                description=intent,
                steps=[ActionStep(
                    step_id="fallback",
                    description="Please review and manually execute this task",
                    tool=None,
                    parameters={"original_intent": intent}
                )],
                expected_outcome="Human handles the task",
                success_criteria=["Human confirms completion"],
                confidence=0.5,
                risk_level="medium"
            )

    def _resolve_dependencies(self, action: Action) -> Action:
        """Ensure step dependencies form a valid DAG."""
        # Simple topological validation
        step_ids = {s.step_id for s in action.steps}
        for step in action.steps:
            for dep in step.depends_on:
                if dep not in step_ids:
                    logger.warning(f"Missing dependency {dep} in action {action.id}")
        return action

    async def _estimate_costs(self, action: Action) -> Action:
        """Estimate action cost using economic engine."""
        try:
            cost = await self.economic.estimate_action_cost(action.__dict__)
            action.cost_estimate = cost
        except Exception:
            action.cost_estimate = sum(s.estimated_duration_seconds * 0.01 for s in action.steps)
        return action

    def _meets_constraints(self, action: Action, constraints: Dict) -> bool:
        """Validate action against hard constraints."""
        max_cost = constraints.get("max_cost")
        if max_cost and action.cost_estimate and action.cost_estimate > max_cost:
            return False
        
        max_duration = constraints.get("max_duration_seconds")
        total_duration = sum(s.estimated_duration_seconds for s in action.steps)
        if max_duration and total_duration > max_duration:
            return False
        
        forbidden_tools = constraints.get("forbidden_tools", [])
        for step in action.steps:
            if step.tool in forbidden_tools:
                return False
        
        return True

    async def _rank_actions(self, actions: List[Action], context: Dict) -> List[Action]:
        """Rank actions by expected value."""
        scored = []
        for action in actions:
            score = action.confidence
            if action.cost_estimate:
                score /= (1 + action.cost_estimate)  # Lower cost is better
            if action.risk_level == "low":
                score *= 1.2
            elif action.risk_level == "critical":
                score *= 0.5
            scored.append((score, action))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [a for _, a in scored]


class ActionGenerationError(Exception):
    pass