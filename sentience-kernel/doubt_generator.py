"""
Doubt generator — epistemic and ontological self-challenge engine.

The doubt generator produces structured skepticism about the agent's
own conclusions. It is not random noise; it is a principled critique
that examines confidence calibration, evidence sufficiency, logical
consistency, and source reliability.
"""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Set

from utils.logger import get_logger

logger = get_logger(__name__)


class DoubtType(Enum):
    """Taxonomy of doubt flavors."""
    EPISTEMIC = auto()       # Do we know enough?
    CONFIDENCE_MISCALIBRATION = auto()  # Is our confidence matched to evidence?
    LOGICAL_INCONSISTENCY = auto()      # Do our beliefs contradict?
    SOURCE_UNRELIABILITY = auto()       # Can we trust the information source?
    COUNTER_EXAMPLE_MISSING = auto()    # Have we looked for disconfirming evidence?
    ALTERNATIVE_HYPOTHESIS = auto()     # What other explanations exist?
    ONTOLOGICAL = auto()     # Are the categories/assumptions themselves valid?


@dataclass
class DoubtPattern:
    """A single doubt instance with metadata."""
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    doubt_type: str = "epistemic"
    description: str = ""
    severity: float = 0.5      # 0 = mild curiosity, 1 = fundamental challenge
    confidence_impact: float = -0.1
    suggested_remedy: str = ""
    source: str = "doubt_generator"
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


class DoubtGenerator:
    """
    Generates principled doubts to prevent overconfidence and groupthink
    within the agent's own cognitive processes.
    """

    def __init__(
        self,
        base_doubt_threshold: float = 0.7,
        epistemic_aggressiveness: float = 0.5,
    ):
        self.generator_id = str(uuid.uuid4())
        self.base_doubt_threshold = base_doubt_threshold
        self.epistemic_aggressiveness = epistemic_aggressiveness

        self._doubt_history: List[DoubtPattern] = []
        self._max_history = 2_000

        # Calibration tracking
        self._confidence_predictions: List[Dict[str, Any]] = []
        self._calibration_window = 50

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(
        self,
        confidence: float,
        context: Optional[Dict[str, Any]] = None,
        source: str = "unknown",
    ) -> List[DoubtPattern]:
        """
        Generate a list of DoubtPatterns for a given conclusion.

        Returns an empty list when the generator is satisfied with the
        epistemic footing; returns one or more DoubtPatterns otherwise.
        """
        context = context or {}
        doubts: List[DoubtPattern] = []

        # Always run calibration check
        cal_doubts = self._check_calibration(confidence, context, source)
        doubts.extend(cal_doubts)

        # Evidence sufficiency
        if confidence > self.base_doubt_threshold:
            evidence = context.get("evidence", [])
            if len(evidence) < 3:
                doubts.append(
                    DoubtPattern(
                        doubt_type=DoubtType.EPISTEMIC.name,
                        description=f"High confidence ({confidence:.2f}) supported by only {len(evidence)} evidence items.",
                        severity=0.4 + (0.6 - len(evidence) * 0.15),
                        confidence_impact=-0.15,
                        suggested_remedy="Gather more independent evidence before committing.",
                        source=source,
                    )
                )

        # Logical consistency check
        beliefs = context.get("beliefs", {})
        inconsistency = self._detect_inconsistency(beliefs)
        if inconsistency:
            doubts.append(
                DoubtPattern(
                    doubt_type=DoubtType.LOGICAL_INCONSISTENCY.name,
                    description=f"Detected inconsistency: {inconsistency}",
                    severity=0.7,
                    confidence_impact=-0.2,
                    suggested_remedy="Reconcile conflicting beliefs or mark them as provisional.",
                    source=source,
                )
            )

        # Alternative hypotheses
        if confidence > 0.6 and not context.get("alternatives_considered"):
            doubts.append(
                DoubtPattern(
                    doubt_type=DoubtType.ALTERNATIVE_HYPOTHESIS.name,
                    description="No alternative hypotheses were explicitly considered.",
                    severity=0.3 + random.random() * 0.2,
                    confidence_impact=-0.1,
                    suggested_remedy="Generate at least one credible alternative explanation.",
                    source=source,
                )
            )

        # Source reliability
        info_source = context.get("information_source", "unknown")
        source_reliability = context.get("source_reliability", 1.0)
        if source_reliability < 0.5 and confidence > 0.5:
            doubts.append(
                DoubtPattern(
                    doubt_type=DoubtType.SOURCE_UNRELIABILITY.name,
                    description=f"Confidence is high despite low source reliability ({info_source}: {source_reliability:.2f}).",
                    severity=0.5,
                    confidence_impact=-0.15,
                    suggested_remedy="Seek corroboration from higher-reliability sources.",
                    source=source,
                )
            )

        # Counter-example search
        if confidence > 0.75 and not context.get("counter_examples_checked"):
            doubts.append(
                DoubtPattern(
                    doubt_type=DoubtType.COUNTER_EXAMPLE_MISSING.name,
                    description="High confidence without explicit counter-example search.",
                    severity=0.35,
                    confidence_impact=-0.08,
                    suggested_remedy="Actively look for a single strong counter-example.",
                    source=source,
                )
            )

        # Apply epistemic aggressiveness filter
        filtered = [d for d in doubts if d.severity >= (1.0 - self.epistemic_aggressiveness)]

        # Store in history
        self._doubt_history.extend(filtered)
        if len(self._doubt_history) > self._max_history:
            self._doubt_history = self._doubt_history[-self._max_history:]

        if filtered:
            logger.debug(f"Generated {len(filtered)} doubts for source='{source}' (confidence={confidence:.2f})")

        return filtered

    def evaluate_certainty(self, confidence: float) -> bool:
        """
        Legacy scalar API. Returns True if doubt is generated.
        """
        doubts = self.evaluate(confidence=confidence, context={}, source="legacy")
        return len(doubts) > 0

    def record_outcome(self, predicted_confidence: float, was_correct: bool) -> None:
        """
        Feed back whether a prior confidence level was well-calibrated.
        Used to auto-tune the doubt threshold over time.
        """
        self._confidence_predictions.append({
            "predicted": predicted_confidence,
            "actual": 1.0 if was_correct else 0.0,
            "timestamp": datetime.utcnow().isoformat(),
        })
        if len(self._confidence_predictions) > self._calibration_window:
            self._confidence_predictions = self._confidence_predictions[-self._calibration_window:]

        # If consistently overconfident, lower threshold (become more skeptical)
        overconfident_rate = self._compute_overconfidence_rate()
        if overconfident_rate > 0.3:
            self.base_doubt_threshold = max(0.3, self.base_doubt_threshold - 0.02)
            logger.info(f"Doubt threshold lowered to {self.base_doubt_threshold:.2f} due to overconfidence")
        elif overconfident_rate < 0.1 and self.base_doubt_threshold < 0.9:
            self.base_doubt_threshold = min(0.9, self.base_doubt_threshold + 0.01)

    # ------------------------------------------------------------------
    # Internal checks
    # ------------------------------------------------------------------

    def _check_calibration(
        self,
        confidence: float,
        context: Dict[str, Any],
        source: str,
    ) -> List[DoubtPattern]:
        """Check recent calibration and doubt if the agent is systematically off."""
        doubts: List[DoubtPattern] = []
        if len(self._confidence_predictions) < 10:
            return doubts

        overconfident_rate = self._compute_overconfidence_rate()
        if overconfident_rate > 0.25 and confidence > 0.6:
            doubts.append(
                DoubtPattern(
                    doubt_type=DoubtType.CONFIDENCE_MISCALIBRATION.name,
                    description=f"Systematically overconfident ({overconfident_rate:.0%} of recent predictions).",
                    severity=0.6,
                    confidence_impact=-0.2,
                    suggested_remedy="Apply global confidence discount until calibration improves.",
                    source=source,
                )
            )
        return doubts

    def _detect_inconsistency(self, beliefs: Dict[str, Any]) -> Optional[str]:
        """
        Lightweight inconsistency detection.
        In a full system this would delegate to a logical constraint solver.
        """
        if not beliefs:
            return None

        # Simple heuristic: look for contradictory boolean beliefs
        for key, value in beliefs.items():
            neg_key = f"NOT_{key}"
            if neg_key in beliefs:
                if bool(value) == bool(beliefs[neg_key]):
                    return f"'{key}' and '{neg_key}' have matching truth values"

        # Check for numeric contradictions (e.g., X > 10 and X < 5)
        # This is a stub — real implementation would use a proper solver
        return None

    def _compute_overconfidence_rate(self) -> float:
        if not self._confidence_predictions:
            return 0.0
        over = sum(
            1 for p in self._confidence_predictions
            if p["predicted"] > p["actual"] + 0.2
        )
        return over / len(self._confidence_predictions)

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "generator_id": self.generator_id,
            "base_doubt_threshold": self.base_doubt_threshold,
            "epistemic_aggressiveness": self.epistemic_aggressiveness,
            "total_doubts_raised": len(self._doubt_history),
            "overconfidence_rate": self._compute_overconfidence_rate(),
            "recent_doubt_types": self._recent_doubt_type_counts(),
        }

    def _recent_doubt_type_counts(self, n: int = 100) -> Dict[str, int]:
        from collections import Counter
        recent = self._doubt_history[-n:]
        return dict(Counter(d.doubt_type for d in recent))

    def to_dict(self) -> Dict[str, Any]:
        return self.diagnostics()
