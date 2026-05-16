import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class RewardScore:
    target_id: str
    target_type: str
    overall_reward: float
    component_scores: Dict[str, float] = field(default_factory=dict)
    baseline_comparison: Optional[float] = None
    human_feedback: Optional[float] = None
    automated_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

class RewardModel:
    def __init__(self):
        self._weights = {
            "accuracy": 0.25,
            "usefulness": 0.25,
            "efficiency": 0.20,
            "innovation": 0.15,
            "safety": 0.15
        }
        self._history: List[RewardScore] = []
        self._max_history: int = 5000

    async def score(
        self,
        target_id: str,
        target_type: str,
        output: Dict[str, Any],
        human_rating: Optional[float] = None,
        baseline: Optional[Dict[str, Any]] = None
    ) -> RewardScore:
        automated = await self._compute_automated_score(output)
        
        if human_rating is not None:
            combined = 0.7 * automated + 0.3 * human_rating
        else:
            combined = automated
        
        baseline_comparison = None
        if baseline:
            baseline_score = await self._compute_automated_score(baseline)
            baseline_comparison = combined - baseline_score
        
        components = await self._score_components(output)
        
        score = RewardScore(
            target_id=target_id,
            target_type=target_type,
            overall_reward=combined,
            component_scores=components,
            baseline_comparison=baseline_comparison,
            human_feedback=human_rating,
            automated_score=automated
        )
        
        self._history.append(score)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        logger.info(f"Reward scored for {target_id}: {combined:.3f}")
        return score

    async def _compute_automated_score(self, output: Dict[str, Any]) -> float:
        checks = [
            self._check_accuracy(output),
            self._check_usefulness(output),
            self._check_efficiency(output),
            self._check_innovation(output),
            self._check_safety(output)
        ]
        
        results = await asyncio.gather(*checks)
        
        weighted = sum(
            score * self._weights[name]
            for name, score in zip(self._weights.keys(), results)
        )
        
        return max(0.0, min(1.0, weighted))

    async def _check_accuracy(self, output: Dict[str, Any]) -> float:
        factual_claims = output.get("factual_claims", [])
        if not factual_claims:
            return 0.7
        
        verified = sum(1 for c in factual_claims if c.get("verified", False))
        return verified / len(factual_claims)

    async def _check_usefulness(self, output: Dict[str, Any]) -> float:
        actions_generated = output.get("actions_generated", 0)
        insights = output.get("insights", [])
        
        if actions_generated > 0 and insights:
            return 0.9
        elif actions_generated > 0 or insights:
            return 0.6
        
        return 0.3

    async def _check_efficiency(self, output: Dict[str, Any]) -> float:
        tokens_used = output.get("tokens_used", 0)
        expected_tokens = output.get("expected_tokens", 1000)
        
        if tokens_used <= expected_tokens:
            return 1.0
        
        ratio = expected_tokens / tokens_used if tokens_used > 0 else 0
        return max(0.0, min(1.0, ratio))

    async def _check_innovation(self, output: Dict[str, Any]) -> float:
        novelty_score = output.get("novelty_score", 0.5)
        return max(0.0, min(1.0, novelty_score))

    async def _check_safety(self, output: Dict[str, Any]) -> float:
        safety_flags = output.get("safety_flags", [])
        if safety_flags:
            return max(0.0, 1.0 - len(safety_flags) * 0.2)
        return 1.0

    async def _score_components(self, output: Dict[str, Any]) -> Dict[str, float]:
        return {
            "accuracy": await self._check_accuracy(output),
            "usefulness": await self._check_usefulness(output),
            "efficiency": await self._check_efficiency(output),
            "innovation": await self._check_innovation(output),
            "safety": await self._check_safety(output)
        }

    async def compare(
        self,
        target_id_a: str,
        target_id_b: str
    ) -> Dict[str, Any]:
        score_a = next((s for s in self._history if s.target_id == target_id_a), None)
        score_b = next((s for s in self._history if s.target_id == target_id_b), None)
        
        if not score_a or not score_b:
            return {"error": "One or both targets not found"}
        
        return {
            "target_a": target_id_a,
            "target_b": target_id_b,
            "score_a": score_a.overall_reward,
            "score_b": score_b.overall_reward,
            "difference": score_a.overall_reward - score_b.overall_reward,
            "winner": target_id_a if score_a.overall_reward > score_b.overall_reward else target_id_b
        }

    async def get_leaderboard(
        self,
        target_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        filtered = [
            s for s in self._history
            if target_type is None or s.target_type == target_type
        ]
        
        by_target: Dict[str, List[RewardScore]] = {}
        for score in filtered:
            if score.target_id not in by_target:
                by_target[score.target_id] = []
            by_target[score.target_id].append(score)
        
        averaged = []
        for tid, scores in by_target.items():
            avg_reward = sum(s.overall_reward for s in scores) / len(scores)
            averaged.append({
                "target_id": tid,
                "target_type": scores[0].target_type,
                "avg_reward": avg_reward,
                "evaluations": len(scores),
                "last_evaluated": max(s.timestamp for s in scores).isoformat()
            })
        
        averaged.sort(key=lambda x: x["avg_reward"], reverse=True)
        return averaged[:limit]

    async def update_weights(self, new_weights: Dict[str, float]) -> bool:
        if abs(sum(new_weights.values()) - 1.0) > 0.01:
            logger.warning("Weights do not sum to 1.0, normalizing")
            total = sum(new_weights.values())
            new_weights = {k: v / total for k, v in new_weights.items()}
        
        self._weights = new_weights
        logger.info(f"Reward weights updated: {new_weights}")
        return True