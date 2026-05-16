import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

from .base_agent import BaseAgent, AgentMessage, AgentResult

@dataclass
class ActionCandidate:
    action_id: str
    description: str
    expected_value: float
    risk_score: float
    effort_cost: float
    time_horizon: float
    prerequisites: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class ActionRankingAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "action_ranker",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.candidates: Dict[str, ActionCandidate] = {}
        self.criteria_weights = config.get("criteria_weights", {
            "value": 0.35,
            "risk": 0.25,
            "effort": 0.20,
            "time": 0.20
        })
        self.risk_tolerance = config.get("risk_tolerance", 0.5)
        
    async def initialize(self):
        self.register_skill("rank", self._rank_actions)
        self.register_skill("evaluate", self._evaluate_candidate)
        self.register_skill("filter", self._filter_actions)
        self.register_skill("optimize", self._optimize_sequence)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "rank")
        
        if skill == "rank":
            return await self._rank_actions(
                message.content,
                message.metadata.get("context", {})
            )
        elif skill == "evaluate":
            return await self._evaluate_candidate(message.content)
        elif skill == "filter":
            return await self._filter_actions(
                message.content,
                message.metadata.get("constraints", {})
            )
        elif skill == "optimize":
            return await self._optimize_sequence(message.content)
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _rank_actions(
        self,
        actions: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> AgentResult:
        scored_actions = []
        
        for action_data in actions:
            candidate = ActionCandidate(
                action_id=action_data.get("id", ""),
                description=action_data.get("description", ""),
                expected_value=action_data.get("expected_value", 0.0),
                risk_score=action_data.get("risk", 0.5),
                effort_cost=action_data.get("effort", 1.0),
                time_horizon=action_data.get("time_horizon", 1.0),
                prerequisites=action_data.get("prerequisites", []),
                dependencies=action_data.get("dependencies", [])
            )
            
            score = self._calculate_score(candidate, context)
            
            scored_actions.append({
                "candidate": candidate,
                "score": score,
                "breakdown": self._score_breakdown(candidate, context)
            })
            
        scored_actions.sort(key=lambda x: x["score"], reverse=True)
        
        return AgentResult(
            success=True,
            data={
                "ranked_actions": [
                    {
                        "id": a["candidate"].action_id,
                        "description": a["candidate"].description,
                        "score": round(a["score"], 4),
                        "breakdown": a["breakdown"]
                    }
                    for a in scored_actions
                ],
                "top_choice": scored_actions[0]["candidate"].action_id if scored_actions else None,
                "recommendation": self._generate_recommendation(scored_actions)
            },
            confidence=scored_actions[0]["score"] if scored_actions else 0.0
        )
        
    async def _evaluate_candidate(
        self,
        candidate_data: Dict[str, Any]
    ) -> AgentResult:
        candidate = ActionCandidate(
            action_id=candidate_data.get("id", ""),
            description=candidate_data.get("description", ""),
            expected_value=candidate_data.get("expected_value", 0.0),
            risk_score=candidate_data.get("risk", 0.5),
            effort_cost=candidate_data.get("effort", 1.0),
            time_horizon=candidate_data.get("time_horizon", 1.0)
        )
        
        score = self._calculate_score(candidate, {})
        
        feasibility = self._check_feasibility(candidate)
        
        return AgentResult(
            success=True,
            data={
                "action_id": candidate.action_id,
                "overall_score": round(score, 4),
                "feasible": feasibility["feasible"],
                "blockers": feasibility["blockers"],
                "risk_assessment": self._assess_risk(candidate),
                "value_assessment": self._assess_value(candidate)
            },
            confidence=score
        )
        
    async def _filter_actions(
        self,
        actions: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> AgentResult:
        max_risk = constraints.get("max_risk", 1.0)
        max_effort = constraints.get("max_effort", float('inf'))
        max_time = constraints.get("max_time", float('inf'))
        required_prereqs = set(constraints.get("available_prerequisites", []))
        
        filtered = []
        
        for action_data in actions:
            candidate = ActionCandidate(
                action_id=action_data.get("id", ""),
                description=action_data.get("description", ""),
                expected_value=action_data.get("expected_value", 0.0),
                risk_score=action_data.get("risk", 0.5),
                effort_cost=action_data.get("effort", 1.0),
                time_horizon=action_data.get("time_horizon", 1.0),
                prerequisites=action_data.get("prerequisites", [])
            )
            
            passes = True
            reasons = []
            
            if candidate.risk_score > max_risk:
                passes = False
                reasons.append(f"Risk {candidate.risk_score:.2f} exceeds max {max_risk}")
                
            if candidate.effort_cost > max_effort:
                passes = False
                reasons.append(f"Effort {candidate.effort_cost:.1f} exceeds max {max_effort}")
                
            if candidate.time_horizon > max_time:
                passes = False
                reasons.append(f"Time {candidate.time_horizon:.1f} exceeds max {max_time}")
                
            missing_prereqs = set(candidate.prerequisites) - required_prereqs
            if missing_prereqs:
                passes = False
                reasons.append(f"Missing prerequisites: {missing_prereqs}")
                
            if passes:
                filtered.append({
                    "id": candidate.action_id,
                    "description": candidate.description,
                    "value": candidate.expected_value
                })
            else:
                filtered.append({
                    "id": candidate.action_id,
                    "filtered_out": True,
                    "reasons": reasons
                })
                
        viable = [a for a in filtered if not a.get("filtered_out")]
        
        return AgentResult(
            success=True,
            data={
                "viable_actions": viable,
                "filtered_count": len(actions) - len(viable),
                "all_results": filtered
            },
            confidence=len(viable) / max(len(actions), 1)
        )
        
    async def _optimize_sequence(
        self,
        action_ids: List[str]
    ) -> AgentResult:
        candidates = [
            self.candidates.get(aid) for aid in action_ids
            if aid in self.candidates
        ]
        
        if not candidates:
            return AgentResult(
                success=False,
                error="No valid candidates found",
                confidence=0.0
            )
            
        sequences = self._generate_sequences(candidates)
        
        best_sequence = None
        best_score = -float('inf')
        
        for sequence in sequences:
            score = self._evaluate_sequence(sequence)
            if score > best_score:
                best_score = score
                best_sequence = sequence
                
        return AgentResult(
            success=True,
            data={
                "optimal_sequence": [
                    {
                        "id": a.action_id,
                        "description": a.description
                    }
                    for a in (best_sequence or [])
                ],
                "expected_total_value": best_score if best_sequence else 0.0,
                "sequence_length": len(best_sequence) if best_sequence else 0
            },
            confidence=min(1.0, best_score) if best_sequence else 0.0
        )
        
    def _calculate_score(
        self,
        candidate: ActionCandidate,
        context: Dict[str, Any]
    ) -> float:
        w = self.criteria_weights
        
        value_norm = min(1.0, candidate.expected_value / 100.0)
        risk_norm = 1.0 - candidate.risk_score
        effort_norm = 1.0 / (1.0 + candidate.effort_cost)
        time_norm = 1.0 / (1.0 + candidate.time_horizon)
        
        context_boost = context.get("priority_multiplier", 1.0)
        
        score = (
            value_norm * w["value"] +
            risk_norm * w["risk"] +
            effort_norm * w["effort"] +
            time_norm * w["time"]
        ) * context_boost
        
        return min(1.0, max(0.0, score))
        
    def _score_breakdown(
        self,
        candidate: ActionCandidate,
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        w = self.criteria_weights
        
        return {
            "value_component": min(1.0, candidate.expected_value / 100.0) * w["value"],
            "risk_component": (1.0 - candidate.risk_score) * w["risk"],
            "effort_component": (1.0 / (1.0 + candidate.effort_cost)) * w["effort"],
            "time_component": (1.0 / (1.0 + candidate.time_horizon)) * w["time"]
        }
        
    def _check_feasibility(
        self,
        candidate: ActionCandidate
    ) -> Dict[str, Any]:
        blockers = []
        
        if candidate.risk_score > self.risk_tolerance * 1.5:
            blockers.append("Risk exceeds tolerance threshold")
            
        if candidate.effort_cost > 10.0:
            blockers.append("Effort cost prohibitively high")
            
        return {
            "feasible": len(blockers) == 0,
            "blockers": blockers
        }
        
    def _assess_risk(self, candidate: ActionCandidate) -> Dict[str, Any]:
        if candidate.risk_score < 0.2:
            level = "low"
        elif candidate.risk_score < 0.5:
            level = "moderate"
        elif candidate.risk_score < 0.8:
            level = "high"
        else:
            level = "critical"
            
        return {
            "level": level,
            "score": candidate.risk_score,
            "acceptable": candidate.risk_score <= self.risk_tolerance
        }
        
    def _assess_value(self, candidate: ActionCandidate) -> Dict[str, Any]:
        return {
            "raw_value": candidate.expected_value,
            "value_per_effort": candidate.expected_value / max(candidate.effort_cost, 0.1),
            "value_per_time": candidate.expected_value / max(candidate.time_horizon, 0.1)
        }
        
    def _generate_sequences(
        self,
        candidates: List[ActionCandidate]
    ) -> List[List[ActionCandidate]]:
        if len(candidates) <= 1:
            return [candidates]
            
        from itertools import permutations
        return [list(p) for p in permutations(candidates)]
        
    def _evaluate_sequence(self, sequence: List[ActionCandidate]) -> float:
        if not sequence:
            return 0.0
            
        total_value = 0.0
        cumulative_risk = 1.0
        
        for i, candidate in enumerate(sequence):
            time_decay = 0.9 ** i
            cumulative_risk *= (1 - candidate.risk_score * 0.1)
            
            total_value += (
                candidate.expected_value *
                time_decay *
                cumulative_risk /
                (1 + candidate.effort_cost * 0.1)
            )
            
        return total_value
        
    def _generate_recommendation(
        self,
        scored_actions: List[Dict[str, Any]]
    ) -> str:
        if not scored_actions:
            return "No viable actions identified"
            
        top = scored_actions[0]
        score = top["score"]
        
        if score > 0.8:
            return f"Strongly recommend: {top['candidate'].action_id}"
        elif score > 0.6:
            return f"Recommend with confidence: {top['candidate'].action_id}"
        elif score > 0.4:
            return f"Consider: {top['candidate'].action_id} with risk mitigation"
        else:
            return "No clearly superior option; review constraints"