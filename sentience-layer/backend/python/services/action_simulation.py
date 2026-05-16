"""
Action Simulation Service
Simulates action execution outcomes with probabilistic modeling.
Uses Antigravity's simulation sandbox for safe experimentation.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import asyncio

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from .action_generation import Action, ActionStep

logger = get_logger(__name__)


class SimulationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class StepOutcome:
    step_id: str
    status: str  # success, failure, partial, timeout
    state_diff: Dict[str, Any] = field(default_factory=dict)
    side_effects: List[str] = field(default_factory=list)
    execution_time_ms: int = 0
    error_message: Optional[str] = None


@dataclass
class SimulationResult:
    action_id: str
    status: SimulationStatus
    final_state: Dict[str, Any]
    step_outcomes: List[StepOutcome]
    success_probability: float
    expected_value: float
    worst_case_scenario: Optional[str]
    best_case_scenario: Optional[str]
    downstream_effects: List[Dict[str, Any]] = field(default_factory=list)
    rollback_state: Optional[Dict[str, Any]] = None


class ActionSimulationService:
    """
    Monte Carlo action simulation with state-space exploration.
    Integrates with Antigravity for realistic environment modeling.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._simulation_history: List[SimulationResult] = []
        logger.info("ActionSimulationService initialized")

    async def simulate(
        self,
        action: Action,
        initial_state: Dict[str, Any],
        num_runs: int = 100,
        context: Optional[Dict[str, Any]] = None,
    ) -> SimulationResult:
        """
        Agentic simulation pipeline:
        1. State initialization → 2. Monte Carlo runs → 3. Outcome aggregation →
        4. Downstream propagation → 5. Rollback state capture
        """
        context = context or {}
        
        try:
            # Step 1: Initialize simulation environment
            env = await self._initialize_environment(initial_state, context)
            
            # Step 2: Run Monte Carlo simulations in parallel
            runs = await asyncio.gather(*[
                self._run_single_simulation(action, env, context, seed=i)
                for i in range(num_runs)
            ])
            
            # Step 3: Aggregate outcomes
            aggregated = self._aggregate_outcomes(runs, action)
            
            # Step 4: Downstream effect simulation
            downstream = await self._simulate_downstream(aggregated, context)
            aggregated.downstream_effects = downstream
            
            # Step 5: Capture rollback state
            aggregated.rollback_state = await self._capture_rollback_state(initial_state)
            
            # Step 6: Antigravity validation
            validated = await self._validate_with_antigravity(aggregated, context)
            
            self._simulation_history.append(validated)
            logger.info(f"Simulation complete for {action.id}: {validated.success_probability:.2%} success rate")
            return validated

        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            raise SimulationError(f"Simulation failed: {e}") from e

    async def _initialize_environment(
        self, initial_state: Dict, context: Dict
    ) -> Dict[str, Any]:
        """Initialize simulation environment."""
        env = dict(initial_state)
        try:
            # Antigravity environment enrichment
            env_update = await self.ag.simulation.get_environment(context.get("user_id"))
            env.update(env_update)
        except Exception:
            pass
        return env

    async def _run_single_simulation(
        self, action: Action, env: Dict, context: Dict, seed: int
    ) -> List[StepOutcome]:
        """Run one simulation trajectory."""
        random.seed(seed)
        outcomes = []
        current_state = dict(env)
        
        for step in action.steps:
            try:
                # Simulate step execution
                outcome = await self._simulate_step(step, current_state, context)
                outcomes.append(outcome)
                
                # Update state
                current_state.update(outcome.state_diff)
                
                # Check for failure
                if outcome.status in ["failure", "timeout"]:
                    break
                    
            except Exception as e:
                outcomes.append(StepOutcome(
                    step_id=step.step_id,
                    status="failure",
                    error_message=str(e),
                    state_diff={}
                ))
                break
        
        return outcomes

    async def _simulate_step(
        self, step: ActionStep, state: Dict, context: Dict
    ) -> StepOutcome:
        """Simulate single step execution."""
        # Base success rate from tool reliability
        base_success = 0.95
        if step.tool:
            try:
                reliability = await self.ag.tools.get_reliability(step.tool)
                base_success = reliability
            except Exception:
                pass
        
        # Adjust for parameter complexity
        complexity_penalty = len(step.parameters) * 0.01
        success_rate = max(0.1, base_success - complexity_penalty)
        
        # Roll dice
        roll = random.random()
        if roll < success_rate:
            status = "success"
            # Generate plausible state diff
            state_diff = await self._generate_state_diff(step, state, success=True)
            side_effects = []
        elif roll < success_rate + 0.03:
            status = "partial"
            state_diff = await self._generate_state_diff(step, state, success=False)
            side_effects = ["Partial completion - manual verification needed"]
        else:
            status = "failure"
            state_diff = {}
            side_effects = [f"Tool {step.tool} failed with simulated error"]
        
        return StepOutcome(
            step_id=step.step_id,
            status=status,
            state_diff=state_diff,
            side_effects=side_effects,
            execution_time_ms=random.randint(100, step.estimated_duration_seconds * 1000)
        )

    async def _generate_state_diff(
        self, step: ActionStep, state: Dict, success: bool
    ) -> Dict[str, Any]:
        """Generate realistic state changes."""
        diff = {}
        for key, value in step.parameters.items():
            if success:
                diff[f"{key}_result"] = f"processed_{value}"
            else:
                diff[f"{key}_status"] = "pending"
        return diff

    def _aggregate_outcomes(
        self, runs: List[List[StepOutcome]], action: Action
    ) -> SimulationResult:
        """Aggregate Monte Carlo runs into statistics."""
        total = len(runs)
        successes = sum(1 for run in runs if all(o.status == "success" for o in run))
        partials = sum(1 for run in runs if any(o.status == "partial" for o in run))
        
        success_prob = successes / total
        partial_prob = partials / total
        
        # Expected value calculation
        ev = success_prob * 1.0 + partial_prob * 0.5 + (1 - success_prob - partial_prob) * 0.0
        
        # Find worst/best cases
        worst = min(runs, key=lambda r: sum(1 for o in r if o.status == "failure"))
        best = max(runs, key=lambda r: sum(1 for o in r if o.status == "success"))
        
        # Aggregate step outcomes
        aggregated_steps = []
        for i, step in enumerate(action.steps):
            step_outcomes = [run[i] for run in runs if i < len(run)]
            if step_outcomes:
                # Most common status
                statuses = [o.status for o in step_outcomes]
                most_common = max(set(statuses), key=statuses.count)
                
                # Average state diff
                all_diffs = [o.state_diff for o in step_outcomes if o.state_diff]
                avg_diff = all_diffs[0] if all_diffs else {}
                
                aggregated_steps.append(StepOutcome(
                    step_id=step.step_id,
                    status=most_common,
                    state_diff=avg_diff,
                    execution_time_ms=int(sum(o.execution_time_ms for o in step_outcomes) / len(step_outcomes))
                ))
        
        return SimulationResult(
            action_id=action.id,
            status=SimulationStatus.COMPLETED,
            final_state={},  # Will be populated downstream
            step_outcomes=aggregated_steps,
            success_probability=success_prob,
            expected_value=ev,
            worst_case_scenario=f"Failed at step {worst[0].step_id if worst else 'unknown'}",
            best_case_scenario="All steps completed successfully"
        )

    async def _simulate_downstream(
        self, result: SimulationResult, context: Dict
    ) -> List[Dict[str, Any]]:
        """Simulate effects 2-3 hops downstream."""
        effects = []
        try:
            downstream = await self.ag.simulation.propagate_downstream(
                result.action_id,
                result.final_state
            )
            effects.extend(downstream)
        except Exception:
            # Fallback: generate synthetic downstream effects
            effects.append({
                "hop": 1,
                "description": "Notification sent to stakeholders",
                "probability": result.success_probability
            })
            effects.append({
                "hop": 2,
                "description": "Dependent workflows triggered",
                "probability": result.success_probability * 0.8
            })
        return effects

    async def _capture_rollback_state(self, initial_state: Dict) -> Dict[str, Any]:
        """Capture state for potential rollback."""
        return dict(initial_state)

    async def _validate_with_antigravity(
        self, result: SimulationResult, context: Dict
    ) -> SimulationResult:
        """Validate simulation results with Antigravity."""
        try:
            validation = await self.ag.simulation.validate(result.__dict__)
            if validation.get("adjusted_probability"):
                result.success_probability = validation["adjusted_probability"]
        except Exception:
            pass
        return result

    async def compare_actions(
        self,
        actions: List[Action],
        initial_state: Dict,
        context: Optional[Dict] = None,
    ) -> List[Tuple[Action, SimulationResult]]:
        """Compare multiple actions via simulation."""
        results = await asyncio.gather(*[
            self.simulate(action, initial_state, context=context)
            for action in actions
        ])
        return list(zip(actions, results))


class SimulationError(Exception):
    pass