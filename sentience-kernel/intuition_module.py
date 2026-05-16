"""
Intuition module — fast, heuristic-based pattern recognition and
gestalt evaluation.

The intuition module provides *System 1* style cognition: rapid,
automatic, affect-laden judgments that guide the kernel before
deliberative reasoning kicks in. Over time it learns from feedback
which heuristics are reliable in which contexts.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class IntuitionSignal:
    """Structured output of an intuitive evaluation."""
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    score: float = 0.5               # Overall heuristic score (0–1)
    confidence: float = 0.5          # Model certainty in this score
    insight: Optional[str] = None    # Human-readable flash insight
    activated_heuristics: List[str] = field(default_factory=list)
    pattern_matches: List[str] = field(default_factory=list)
    gestalt_tags: List[str] = field(default_factory=list)
    latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


class Heuristic:
    """A single heuristic rule with adaptive weight."""

    def __init__(
        self,
        name: str,
        matcher: Callable[[Dict[str, Any]], bool],
        base_score: float = 0.0,
        context_tags: Optional[List[str]] = None,
    ):
        self.name = name
        self.matcher = matcher
        self.base_score = base_score
        self.weight = 1.0
        self.success_history: List[bool] = []
        self.context_tags = set(context_tags or [])

    @property
    def reliability(self) -> float:
        if not self.success_history:
            return 0.5
        return sum(self.success_history) / len(self.success_history)

    def evaluate(self, context: Dict[str, Any]) -> float:
        if self.matcher(context):
            return self.base_score * self.weight * self.reliability
        return 0.0

    def feedback(self, was_correct: bool) -> None:
        self.success_history.append(was_correct)
        if len(self.success_history) > 200:
            self.success_history = self.success_history[-200:]
        # Adjust weight slowly
        if was_correct:
            self.weight = min(2.0, self.weight + 0.02)
        else:
            self.weight = max(0.1, self.weight - 0.05)


class IntuitionModule:
    """
    Fast heuristic evaluator with adaptive learning.

    Maintains a library of heuristics, pattern recognisers, and
    gestalt classifiers. Can be pre-seeded with domain-specific rules
    or learn entirely from feedback.
    """

    def __init__(self):
        self.module_id = str(uuid.uuid4())
        self.heuristics: Dict[str, Heuristic] = {}
        self._gestalt_patterns: Dict[str, Callable[[Dict[str, Any]], float]] = {}
        self._pattern_library: Dict[str, Dict[str, Any]] = {}

        # Seed with universal heuristics
        self._seed_universal_heuristics()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(
        self,
        context: Dict[str, Any],
        arousal_level: float = 0.5,
    ) -> IntuitionSignal:
        """
        Run all applicable heuristics and pattern matchers against
        the current context, returning a composite IntuitionSignal.
        """
        t0 = datetime.utcnow()

        activated: List[str] = []
        matches: List[str] = []
        raw_scores: List[float] = []

        # --- Heuristic layer ---
        for name, h in self.heuristics.items():
            score = h.evaluate(context)
            if score != 0.0:
                activated.append(name)
                raw_scores.append(score)

        # --- Pattern layer ---
        for pattern_name, matcher in self._gestalt_patterns.items():
            match_strength = matcher(context)
            if match_strength > 0.3:
                matches.append(pattern_name)
                raw_scores.append(match_strength)

        # --- Combine scores ---
        if raw_scores:
            # Arousal modulates integration:
            # High arousal → more weight on strong signals (risk-sensitive)
            # Low arousal  → average more evenly (exploratory)
            if arousal_level > 0.7:
                composite = max(raw_scores)
            else:
                composite = sum(raw_scores) / len(raw_scores)
        else:
            composite = 0.5

        composite = max(0.0, min(1.0, composite))

        # Confidence is inversely related to number of conflicting signals
        if len(raw_scores) > 1:
            variance = sum((s - composite) ** 2 for s in raw_scores) / len(raw_scores)
            confidence = max(0.0, 1.0 - variance ** 0.5)
        else:
            confidence = 0.5

        # Generate flash insight if strong pattern match
        insight: Optional[str] = None
        if matches and composite > 0.8:
            insight = f"Strong gestalt match on {matches[0]} (score={composite:.2f})"
        elif activated and composite < 0.2:
            insight = f"Conflicting heuristics activated: {activated} — caution advised."

        latency = (datetime.utcnow() - t0).total_seconds() * 1000

        return IntuitionSignal(
            score=composite,
            confidence=confidence,
            insight=insight,
            activated_heuristics=activated,
            pattern_matches=matches,
            latency_ms=latency,
        )

    def add_heuristic(
        self,
        name: str,
        matcher: Callable[[Dict[str, Any]], bool],
        base_score: float = 0.0,
        context_tags: Optional[List[str]] = None,
    ) -> Heuristic:
        h = Heuristic(name, matcher, base_score, context_tags)
        self.heuristics[name] = h
        return h

    def remove_heuristic(self, name: str) -> None:
        self.heuristics.pop(name, None)

    def provide_feedback(self, heuristic_name: str, was_correct: bool) -> None:
        """Update a heuristic based on outcome feedback."""
        h = self.heuristics.get(heuristic_name)
        if h:
            h.feedback(was_correct)
            logger.debug(f"Heuristic '{heuristic_name}' feedback: correct={was_correct}, weight={h.weight:.2f}")

    def register_gestalt_pattern(
        self,
        name: str,
        matcher: Callable[[Dict[str, Any]], float],
    ) -> None:
        """
        Register a gestalt pattern matcher that returns a float 0–1
        indicating match strength.
        """
        self._gestalt_patterns[name] = matcher

    # ------------------------------------------------------------------
    # Seeded heuristics
    # ------------------------------------------------------------------

    def _seed_universal_heuristics(self) -> None:
        """Pre-populate with domain-agnostic heuristics."""

        # High confidence + high stakes → elevate score
        self.add_heuristic(
            name="high_confidence_high_stakes",
            matcher=lambda ctx: (
                ctx.get("confidence", 0) > 0.8 and ctx.get("stakes", 0) > 0.7
            ),
            base_score=0.25,
            context_tags=["risk", "confidence"],
        )

        # Recent failure streak → lower score (loss aversion)
        self.add_heuristic(
            name="recent_failure_streak",
            matcher=lambda ctx: (
                isinstance(ctx.get("recent_outcomes"), list)
                and len([o for o in ctx["recent_outcomes"] if not o]) >= 3
            ),
            base_score=-0.2,
            context_tags=["history", "risk"],
        )

        # Familiar pattern → moderate positive
        self.add_heuristic(
            name="familiar_pattern",
            matcher=lambda ctx: ctx.get("pattern_recognition", False) is True,
            base_score=0.1,
            context_tags=["pattern"],
        )

        # Novel context with no history → uncertainty penalty
        self.add_heuristic(
            name="novel_uncertainty",
            matcher=lambda ctx: (
                ctx.get("novelty_score", 0) > 0.8
                and ctx.get("historical_success_rate") is None
            ),
            base_score=-0.15,
            context_tags=["novelty", "uncertainty"],
        )

        # Human in the loop → elevate (trust augmentation)
        self.add_heuristic(
            name="human_in_loop",
            matcher=lambda ctx: ctx.get("human_approved", False) is True,
            base_score=0.15,
            context_tags=["trust", "human"],
        )

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "heuristic_count": len(self.heuristics),
            "gestalt_pattern_count": len(self._gestalt_patterns),
            "heuristic_details": [
                {
                    "name": h.name,
                    "weight": h.weight,
                    "reliability": h.reliability,
                    "history_size": len(h.success_history),
                }
                for h in self.heuristics.values()
            ],
        }
