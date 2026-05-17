"""
Metacognition — thinking about thinking.

The MetacognitionEngine reflects on decision processes, detects cognitive
biases, selects strategies, and modulates the learning rate of the agent
based on recent performance volatility.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Set


class ReflectionStrategy(Enum):
    """Strategies the metacognitive engine can recommend."""
    DEEP_ANALYSIS = auto()
    FAST_HEURISTIC = auto()
    SEEK_EXTERNAL_VALIDATION = auto()
    SIMULATE_COUNTERFACTUALS = auto()
    DEFER_DECISION = auto()
    ESCALATE_TO_HUMAN = auto()
    EXPLORE_MORE = auto()
    EXPLOIT_CURRENT = auto()


class CognitiveBias(Enum):
    """Known biases the engine can flag."""
    CONFIRMATION = "confirmation_bias"
    OVERCONFIDENCE = "overconfidence"
    AVAILABILITY = "availability_heuristic"
    ANCHORING = "anchoring"
    SUNK_COST = "sunk_cost_fallacy"
    RECENCY = "recency_bias"
    STATUS_QUO = "status_quo_bias"


@dataclass
class MetaRecord:
    """Output of a single metacognitive reflection."""
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reflection_type: str = "generic"
    recommended_strategy: Optional[str] = None
    biases_detected: List[str] = field(default_factory=list)
    confidence_in_decision: float = 0.5
    confidence_in_self_model: float = 0.5
    learning_rate_delta: float = 0.0
    notes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


class MetacognitionEngine:
    """
    Reflects on decision processes and suggests cognitive strategies.

    Key functions:
        1. Bias detection via lightweight heuristics.
        2. Strategy selection based on arousal, confidence, and context.
        3. Learning-rate modulation to prevent overfitting or stagnation.
        4. Self-model calibration recommendations.
    """

    def __init__(self):
        self.engine_id = str(uuid.uuid4())
        self.reflection_history: List[MetaRecord] = []
        self._max_history = 2_000

        # Running stats for volatility tracking
        self._recent_confidences: List[float] = []
        self._confidence_window = 20

        # Strategy preference weights (adapted over time)
        self._strategy_weights: Dict[ReflectionStrategy, float] = {
            ReflectionStrategy.DEEP_ANALYSIS: 0.2,
            ReflectionStrategy.FAST_HEURISTIC: 0.2,
            ReflectionStrategy.SEEK_EXTERNAL_VALIDATION: 0.1,
            ReflectionStrategy.SIMULATE_COUNTERFACTUALS: 0.15,
            ReflectionStrategy.DEFER_DECISION: 0.1,
            ReflectionStrategy.ESCALATE_TO_HUMAN: 0.05,
            ReflectionStrategy.EXPLORE_MORE: 0.1,
            ReflectionStrategy.EXPLOIT_CURRENT: 0.1,
        }

        self._learning_rate = 0.1
        self._min_learning_rate = 0.001
        self._max_learning_rate = 0.5

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reflect(self, decision_process: Dict[str, Any]) -> MetaRecord:
        """
        Analyze a decision process and return a MetaRecord with
        recommendations, bias flags, and learning-rate adjustments.
        """
        context = decision_process.get("context", {})
        intuition = decision_process.get("intuition", {})
        doubts = decision_process.get("doubts", [])
        arousal = decision_process.get("arousal", 0.5)
        cycle_id = decision_process.get("cycle_id", "unknown")

        # --- Bias detection ---
        biases = self._detect_biases(decision_process)

        # --- Confidence tracking ---
        intuition_conf = intuition.get("confidence", 0.5)
        self._recent_confidences.append(intuition_conf)
        if len(self._recent_confidences) > self._confidence_window:
            self._recent_confidences = self._recent_confidences[-self._confidence_window:]

        confidence_volatility = self._compute_volatility(self._recent_confidences)
        confidence_trend = self._compute_trend(self._recent_confidences)

        # --- Strategy selection ---
        strategy = self._select_strategy(
            arousal=arousal,
            confidence=intuition_conf,
            volatility=confidence_volatility,
            bias_count=len(biases),
            doubt_count=len(doubts),
        )

        # --- Learning rate modulation ---
        lr_delta = self._adjust_learning_rate(
            volatility=confidence_volatility,
            trend=confidence_trend,
            bias_count=len(biases),
        )

        record = MetaRecord(
            reflection_type="full_reflection",
            recommended_strategy=strategy.name,
            biases_detected=[b.value for b in biases],
            confidence_in_decision=intuition_conf,
            confidence_in_self_model=1.0 - confidence_volatility,
            learning_rate_delta=lr_delta,
            notes=[
                f"Cycle {cycle_id}: arousal={arousal:.2f}",
                f"Confidence volatility: {confidence_volatility:.3f}",
                f"Confidence trend: {confidence_trend:+.3f}",
                f"Biases detected: {len(biases)}",
                f"Doubts raised: {len(doubts)}",
            ],
        )

        self.reflection_history.append(record)
        if len(self.reflection_history) > self._max_history:
            self.reflection_history = self.reflection_history[-self._max_history:]

        return record

    def get_reflection_summary(self, n: int = 10) -> Dict[str, Any]:
        """Summary statistics over recent reflections."""
        recent = self.reflection_history[-n:]
        if not recent:
            return {"count": 0}

        bias_counter: Dict[str, int] = {}
        strategy_counter: Dict[str, int] = {}
        avg_conf = sum(r.confidence_in_decision for r in recent) / len(recent)

        for r in recent:
            for b in r.biases_detected:
                bias_counter[b] = bias_counter.get(b, 0) + 1
            if r.recommended_strategy:
                strategy_counter[r.recommended_strategy] = strategy_counter.get(r.recommended_strategy, 0) + 1

        return {
            "count": len(recent),
            "avg_confidence_in_decision": avg_conf,
            "top_biases": sorted(bias_counter.items(), key=lambda x: x[1], reverse=True)[:5],
            "top_strategies": sorted(strategy_counter.items(), key=lambda x: x[1], reverse=True)[:5],
            "current_learning_rate": self._learning_rate,
        }

    # ------------------------------------------------------------------
    # Bias detection heuristics
    # ------------------------------------------------------------------

    def _detect_biases(self, decision_process: Dict[str, Any]) -> Set[CognitiveBias]:
        biases: Set[CognitiveBias] = set()
        context = decision_process.get("context", {})
        intuition = decision_process.get("intuition", {})
        doubts = decision_process.get("doubts", [])

        # Confirmation: high confidence but no contradictory evidence examined
        if intuition.get("confidence", 0.0) > 0.85 and not doubts:
            biases.add(CognitiveBias.OVERCONFIDENCE)
            # Also likely confirmation if only supporting evidence present
            evidence = context.get("evidence", [])
            if evidence and not any(e.get("contradicts_hypothesis") for e in evidence):
                biases.add(CognitiveBias.CONFIRMATION)

        # Availability: decision based on very few recent examples
        recent_examples = context.get("recent_examples", [])
        if len(recent_examples) < 3 and intuition.get("confidence", 0.0) > 0.6:
            biases.add(CognitiveBias.AVAILABILITY)

        # Anchoring: first piece of evidence has disproportionate weight
        evidence = context.get("evidence", [])
        if evidence:
            weights = [e.get("weight", 1.0) for e in evidence]
            if weights and weights[0] / sum(weights) > 0.5:
                biases.add(CognitiveBias.ANCHORING)

        # Recency: only looked at last N items
        if context.get("lookback_window", 100) < 5:
            biases.add(CognitiveBias.RECENCY)

        # Status quo: action is "maintain" with no justification
        proposed_action = context.get("proposed_action", {})
        if proposed_action.get("type") == "maintain" and not proposed_action.get("justification"):
            biases.add(CognitiveBias.STATUS_QUO)

        return biases

    # ------------------------------------------------------------------
    # Strategy selection
    # ------------------------------------------------------------------

    def _select_strategy(
        self,
        arousal: float,
        confidence: float,
        volatility: float,
        bias_count: int,
        doubt_count: int,
    ) -> ReflectionStrategy:
        """
        Score each strategy based on current cognitive context and pick
        the highest-scoring one.
        """
        scores: Dict[ReflectionStrategy, float] = {}

        # Deep analysis: good when confidence is moderate and we have time (low arousal)
        scores[ReflectionStrategy.DEEP_ANALYSIS] = (
            self._strategy_weights[ReflectionStrategy.DEEP_ANALYSIS]
            * (0.5 - abs(confidence - 0.5))  # peaks at mid-confidence
            * (1.0 - arousal)
        )

        # Fast heuristic: good when arousal is high and we need speed
        scores[ReflectionStrategy.FAST_HEURISTIC] = (
            self._strategy_weights[ReflectionStrategy.FAST_HEURISTIC]
            * arousal
            * (1.0 - volatility)
        )

        # External validation: good when many biases detected or confidence low
        scores[ReflectionStrategy.SEEK_EXTERNAL_VALIDATION] = (
            self._strategy_weights[ReflectionStrategy.SEEK_EXTERNAL_VALIDATION]
            * (bias_count / 3.0)
            * (1.0 - confidence)
        )

        # Counterfactuals: good when we have time and want to test assumptions
        scores[ReflectionStrategy.SIMULATE_COUNTERFACTUALS] = (
            self._strategy_weights[ReflectionStrategy.SIMULATE_COUNTERFACTUALS]
            * (1.0 - arousal)
            * confidence
        )

        # Defer: good when volatility is high or many doubts
        scores[ReflectionStrategy.DEFER_DECISION] = (
            self._strategy_weights[ReflectionStrategy.DEFER_DECISION]
            * volatility
            * (doubt_count / 3.0)
        )

        # Escalate: rare, only when everything looks bad
        scores[ReflectionStrategy.ESCALATE_TO_HUMAN] = (
            self._strategy_weights[ReflectionStrategy.ESCALATE_TO_HUMAN]
            * (1.0 if (bias_count >= 3 and confidence < 0.3) else 0.0)
        )

        # Explore more: good when confidence is low and not many biases
        scores[ReflectionStrategy.EXPLORE_MORE] = (
            self._strategy_weights[ReflectionStrategy.EXPLORE_MORE]
            * (1.0 - confidence)
            * (1.0 if bias_count < 2 else 0.3)
        )

        # Exploit current: good when confidence is high and stable
        scores[ReflectionStrategy.EXPLOIT_CURRENT] = (
            self._strategy_weights[ReflectionStrategy.EXPLOIT_CURRENT]
            * confidence
            * (1.0 - volatility)
        )

        best = max(scores, key=lambda k: scores[k])
        return best

    # ------------------------------------------------------------------
    # Learning-rate modulation
    # ------------------------------------------------------------------

    def _adjust_learning_rate(self, volatility: float, trend: float, bias_count: int) -> float:
        """
        High volatility → decrease LR (we're unstable).
        Strong positive trend + low bias → increase LR (we're learning well).
        """
        if volatility > 0.3:
            delta = -0.02
        elif trend > 0.05 and bias_count < 2:
            delta = +0.01
        else:
            delta = 0.0

        self._learning_rate = max(
            self._min_learning_rate,
            min(self._max_learning_rate, self._learning_rate + delta),
        )
        return delta

    # ------------------------------------------------------------------
    # Statistics helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_volatility(series: List[float]) -> float:
        if len(series) < 2:
            return 0.0
        mean = sum(series) / len(series)
        variance = sum((x - mean) ** 2 for x in series) / len(series)
        return variance ** 0.5

    @staticmethod
    def _compute_trend(series: List[float]) -> float:
        if len(series) < 2:
            return 0.0
        # Simple linear slope over the window
        n = len(series)
        x_mean = (n - 1) / 2
        y_mean = sum(series) / n
        numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(series))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        return numerator / denominator if denominator else 0.0
