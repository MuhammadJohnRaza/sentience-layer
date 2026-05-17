import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict

from .base_agent import BaseAgent, AgentMessage, AgentResult

@dataclass
class CausalHypothesis:
    cause: str
    effect: str
    strength: float
    mechanism: str
    evidence: List[str]
    confidence: float

class CausalInferenceAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "causal_inference",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.hypotheses: List[CausalHypothesis] = []
        self.observations: List[Dict[str, Any]] = []
        self.variable_history: Dict[str, List[float]] = defaultdict(list)
        self.confidence_threshold = config.get("confidence_threshold", 0.7)
        self.min_observations = config.get("min_observations", 10)
        
    async def initialize(self):
        self.register_skill("infer", self._infer_causality)
        self.register_skill("test", self._test_hypothesis)
        self.register_skill("intervene", self._suggest_intervention)
        self.register_skill("explain", self._explain_causation)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "infer")
        
        if skill == "infer":
            return await self._infer_causality(
                message.content,
                message.metadata.get("variables")
            )
        elif skill == "test":
            return await self._test_hypothesis(message.content)
        elif skill == "intervene":
            return await self._suggest_intervention(
                message.content,
                message.metadata.get("goal")
            )
        elif skill == "explain":
            return await self._explain_causation(
                message.content,
                message.metadata.get("outcome")
            )
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _infer_causality(
        self,
        data: List[Dict[str, Any]],
        variables: Optional[List[str]] = None
    ) -> AgentResult:
        self.observations.extend(data)
        
        if variables is None:
            variables = list(data[0].keys()) if data else []
            
        for obs in data:
            for var, value in obs.items():
                if isinstance(value, (int, float)):
                    self.variable_history[var].append(float(value))
                    
        hypotheses = []
        
        for i, cause in enumerate(variables):
            for effect in variables[i+1:]:
                if cause == effect:
                    continue
                    
                correlation = self._calculate_correlation(cause, effect)
                if abs(correlation) < 0.3:
                    continue
                    
                granger = self._granger_causality(cause, effect)
                temporal = self._temporal_precedence(cause, effect)
                
                strength = (abs(correlation) + granger + temporal) / 3
                
                if strength > 0.5:
                    hypothesis = CausalHypothesis(
                        cause=cause,
                        effect=effect,
                        strength=strength,
                        mechanism=self._infer_mechanism(cause, effect),
                        evidence=[f"correlation: {correlation:.3f}"],
                        confidence=min(1.0, strength)
                    )
                    hypotheses.append(hypothesis)
                    
        self.hypotheses.extend(hypotheses)
        
        return AgentResult(
            success=True,
            data={
                "hypotheses_generated": len(hypotheses),
                "strongest": [
                    {
                        "cause": h.cause,
                        "effect": h.effect,
                        "strength": round(h.strength, 4),
                        "mechanism": h.mechanism
                    }
                    for h in sorted(hypotheses, key=lambda x: x.strength, reverse=True)[:5]
                ],
                "total_observations": len(self.observations)
            }
        )
        
    async def _test_hypothesis(
        self,
        hypothesis_spec: Dict[str, Any]
    ) -> AgentResult:
        cause = hypothesis_spec.get("cause")
        effect = hypothesis_spec.get("effect")
        
        matching = [
            h for h in self.hypotheses
            if h.cause == cause and h.effect == effect
        ]
        
        if not matching:
            return AgentResult(
                success=False,
                error="Hypothesis not found",
                confidence=0.0
            )
            
        hypothesis = matching[0]
        
        counterfactual = self._generate_counterfactual(cause, effect)
        confounders = self._identify_confounders(cause, effect)
        natural_experiment = self._find_natural_experiment(cause, effect)
        
        test_strength = (
            (1.0 if counterfactual else 0.0) * 0.3 +
            (1.0 / (1.0 + len(confounders))) * 0.4 +
            (1.0 if natural_experiment else 0.0) * 0.3
        )
        
        return AgentResult(
            success=True,
            data={
                "hypothesis": {
                    "cause": cause,
                    "effect": effect,
                    "original_strength": round(hypothesis.strength, 4)
                },
                "test_results": {
                    "counterfactual_available": counterfactual is not None,
                    "confounders_identified": len(confounders),
                    "natural_experiment_found": natural_experiment is not None
                },
                "adjusted_confidence": round(
                    hypothesis.confidence * test_strength, 4
                ),
                "recommendation": "Strong evidence" if test_strength > 0.7 else "Needs more testing"
            }
        )
        
    async def _suggest_intervention(
        self,
        target_variable: str,
        goal: Optional[str] = None
    ) -> AgentResult:
        relevant = [
            h for h in self.hypotheses
            if h.effect == target_variable and h.strength > 0.5
        ]
        
        if not relevant:
            return AgentResult(
                success=False,
                error=f"No causal paths to {target_variable} found"
            )
            
        interventions = []
        for h in relevant:
            expected_change = h.strength * 0.5
            
            interventions.append({
                "intervene_on": h.cause,
                "target": target_variable,
                "expected_effect": round(expected_change, 4),
                "confidence": round(h.confidence, 4),
                "mechanism": h.mechanism,
                "side_effects": self._estimate_side_effects(h.cause)
            })
            
        interventions.sort(key=lambda x: x["expected_effect"], reverse=True)
        
        return AgentResult(
            success=True,
            data={
                "target": target_variable,
                "recommended_interventions": interventions[:3],
                "optimal_intervention": interventions[0] if interventions else None
            }
        )
        
    async def _explain_causation(
        self,
        event: str,
        outcome: Optional[str]
    ) -> AgentResult:
        paths = self._find_causal_paths(event, outcome)
        
        if not paths:
            return AgentResult(
                success=True,
                data={
                    "event": event,
                    "outcome": outcome,
                    "explanation": "No direct causal path found",
                    "alternative_explanations": self._generate_alternatives(event, outcome)
                }
            )
            
        primary_path = paths[0]
        
        explanation_parts = []
        for i in range(len(primary_path) - 1):
            cause = primary_path[i]
            effect = primary_path[i + 1]
            
            matching = [
                h for h in self.hypotheses
                if h.cause == cause and h.effect == effect
            ]
            
            if matching:
                explanation_parts.append(
                    f"{cause} causes {effect} via {matching[0].mechanism}"
                )
            else:
                explanation_parts.append(f"{cause} leads to {effect}")
                
        return AgentResult(
            success=True,
            data={
                "event": event,
                "outcome": outcome,
                "explanation": " -> ".join(explanation_parts),
                "causal_path": primary_path,
                "alternative_paths": paths[1:3] if len(paths) > 1 else [],
                "confidence": round(
                    sum(h.strength for h in [
                        next((hx for hx in self.hypotheses if hx.cause == primary_path[i] and hx.effect == primary_path[i+1]), None)
                        for i in range(len(primary_path)-1)
                        if next((hx for hx in self.hypotheses if hx.cause == primary_path[i] and hx.effect == primary_path[i+1]), None)
                    ]) / max(len(primary_path)-1, 1), 4
                )
            }
        )
        
    def _calculate_correlation(self, var_a: str, var_b: str) -> float:
        history_a = self.variable_history.get(var_a, [])
        history_b = self.variable_history.get(var_b, [])
        
        min_len = min(len(history_a), len(history_b))
        if min_len < self.min_observations:
            return 0.0
            
        a = np.array(history_a[-min_len:])
        b = np.array(history_b[-min_len:])
        
        if np.std(a) == 0 or np.std(b) == 0:
            return 0.0
            
        return float(np.corrcoef(a, b)[0, 1])
        
    def _granger_causality(self, cause: str, effect: str) -> float:
        cause_history = self.variable_history.get(cause, [])
        effect_history = self.variable_history.get(effect, [])
        
        if len(cause_history) < 5 or len(effect_history) < 5:
            return 0.0
            
        lagged_correlations = []
        for lag in range(1, min(4, len(cause_history))):
            if len(cause_history) > lag and len(effect_history) > lag:
                corr = np.corrcoef(
                    cause_history[:-lag],
                    effect_history[lag:]
                )[0, 1] if len(cause_history[:-lag]) == len(effect_history[lag:]) else 0
                lagged_correlations.append(abs(corr) if not np.isnan(corr) else 0)
                
        return max(lagged_correlations) if lagged_correlations else 0.0
        
    def _temporal_precedence(self, cause: str, effect: str) -> float:
        cause_first = 0
        total = 0
        
        for i in range(len(self.observations) - 1):
            if cause in self.observations[i] and effect in self.observations[i+1]:
                if self.observations[i][cause] != 0 and self.observations[i+1][effect] != 0:
                    cause_first += 1
                total += 1
                
        return cause_first / max(total, 1)
        
    def _infer_mechanism(self, cause: str, effect: str) -> str:
        mechanisms = [
            f"direct_influence_{cause}_on_{effect}",
            "correlational_linkage",
            "mediated_effect"
        ]
        return mechanisms[0]
        
    def _generate_counterfactual(
        self,
        cause: str,
        effect: str
    ) -> Optional[Dict[str, Any]]:
        cause_history = self.variable_history.get(cause, [])
        effect_history = self.variable_history.get(effect, [])
        
        if not cause_history or not effect_history:
            return None
            
        instances_without_cause = [
            i for i, v in enumerate(cause_history)
            if abs(v) < 0.1
        ]
        
        if instances_without_cause:
            return {
                "instances": len(instances_without_cause),
                "avg_effect_without_cause": np.mean([
                    effect_history[i] for i in instances_without_cause
                    if i < len(effect_history)
                ]) if instances_without_cause else 0
            }
        return None
        
    def _identify_confounders(self, cause: str, effect: str) -> List[str]:
        confounders = []
        
        for var in self.variable_history.keys():
            if var == cause or var == effect:
                continue
                
            corr_cause = abs(self._calculate_correlation(var, cause))
            corr_effect = abs(self._calculate_correlation(var, effect))
            
            if corr_cause > 0.5 and corr_effect > 0.5:
                confounders.append(var)
                
        return confounders
        
    def _find_natural_experiment(self, cause: str, effect: str) -> Optional[Dict[str, Any]]:
        cause_history = self.variable_history.get(cause, [])
        
        if not cause_history:
            return None
            
        mean_val = np.mean(cause_history)
        std_val = np.std(cause_history)
        shocks = []
        if std_val > 0:
            shocks = [
                i for i, v in enumerate(cause_history)
                if abs(v - mean_val) > 2 * std_val
            ]
        
        if shocks:
            return {
                "shock_instances": len(shocks),
                "shock_indices": shocks[:5]
            }
        return None
        
    def _find_causal_paths(
        self,
        start: str,
        end: Optional[str]
    ) -> List[List[str]]:
        if not end:
            return [[start]]
            
        paths = []
        visited = set()
        
        def dfs(current: str, path: List[str]):
            if current == end:
                paths.append(path[:])
                return
                
            visited.add(current)
            
            for h in self.hypotheses:
                if h.cause == current and h.effect not in visited:
                    path.append(h.effect)
                    dfs(h.effect, path)
                    path.pop()
                    
            visited.remove(current)
            
        dfs(start, [start])
        return paths
        
    def _estimate_side_effects(self, intervention: str) -> List[str]:
        effects = [
            h.effect for h in self.hypotheses
            if h.cause == intervention
        ]
        return list(set(effects))[:5]
        
    def _generate_alternatives(
        self,
        event: str,
        outcome: Optional[str]
    ) -> List[str]:
        return [
            f"Coincidence: {event} and {outcome} occurred together by chance",
            f"Reverse causation: {outcome} may have caused {event}",
            f"Common cause: Both influenced by an unobserved variable"
        ]