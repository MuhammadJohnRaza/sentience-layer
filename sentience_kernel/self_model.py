"""
Self-model — the agent's understanding of itself, its capabilities,
its evolving identity, and its performance history.

The self-model is not merely a static registry; it maintains an
*IdentityState* that drifts over time based on experience, a
*CapabilityModel* that tracks proficiency and decay, and an emotional/
arousal overlay that colours self-perception.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Set


class IdentityState(Enum):
    """Qualitative identity phases the agent may pass through."""
    NASCENT = auto()      # Just initialized, little experience
    LEARNING = auto()     # Rapidly accumulating skills & beliefs
    STABLE = auto()       # Mature, well-calibrated self-model
    ADAPTING = auto()     # Undergoing significant structural change
    DISTRESSED = auto()   # High uncertainty, low confidence, many failures
    TRANSCENDENT = auto() # Meta-stable after large insight / consolidation


@dataclass
class CapabilityModel:
    """
    Represents a single capability (skill, tool access, API, etc.).
    Tracks proficiency, recency, failure rate, and dependencies.
    """
    name: str
    category: str = "general"
    proficiency: float = 0.0          # 0.0 – 1.0
    confidence: float = 1.0           # model certainty about proficiency
    last_used: Optional[datetime] = None
    use_count: int = 0
    failure_count: int = 0
    success_streak: int = 0
    dependencies: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)

    @property
    def reliability(self) -> float:
        """Estimated reliability given use history."""
        if self.use_count == 0:
            return 0.5
        return 1.0 - (self.failure_count / self.use_count)

    def record_usage(self, success: bool, timestamp: Optional[datetime] = None) -> None:
        self.use_count += 1
        self.last_used = timestamp or datetime.utcnow()
        if success:
            self.success_streak += 1
            # Proficiency rises faster when streak is high (compound learning)
            delta = 0.05 * (1 + self.success_streak * 0.1)
            self.proficiency = min(1.0, self.proficiency + delta)
        else:
            self.failure_count += 1
            self.success_streak = 0
            delta = 0.08
            self.proficiency = max(0.0, self.proficiency - delta)
            self.confidence = max(0.0, self.confidence - 0.05)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["reliability"] = self.reliability
        d["last_used"] = self.last_used.isoformat() if self.last_used else None
        d["tags"] = list(self.tags)
        return d


@dataclass
class EmotionalOverlay:
    """
    Simplified affective state that tints self-perception.
    Not a full emotion engine — just enough to bias decisions.
    """
    valence: float = 0.0      # -1 (negative) → +1 (positive)
    arousal: float = 0.5      # 0 (calm) → 1 (activated)
    dominance: float = 0.5    # 0 (submissive/unsure) → 1 (in control)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def decay(self, seconds_elapsed: float, decay_rate: float = 0.01) -> None:
        """Gradually return toward neutral."""
        self.valence *= max(0.0, 1.0 - decay_rate * seconds_elapsed)
        self.dominance = 0.5 + (self.dominance - 0.5) * max(0.0, 1.0 - decay_rate * seconds_elapsed)
        self.last_updated = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "last_updated": self.last_updated.isoformat(),
        }


class SelfModel:
    """
    The agent's autobiographical & capability self-representation.

    Responsibilities:
        1. Track beliefs about itself and the world.
        2. Maintain a capability registry with proficiency scores.
        3. Evolve identity state based on experience.
        4. Provide a coherent "narrative of self" for metacognition.
    """

    def __init__(self, identity: Optional[str] = None):
        self.model_id = str(uuid.uuid4())
        self.identity = identity or "Sentience Layer Core"
        self._beliefs: Dict[str, Any] = {}
        self._belief_confidences: Dict[str, float] = {}
        self._belief_timestamps: Dict[str, datetime] = {}

        self.capabilities: Dict[str, CapabilityModel] = {}
        self._identity_state = IdentityState.NASCENT
        self.confidence = 0.5

        self.emotion = EmotionalOverlay()
        self._cycle_history: List[Dict[str, Any]] = []
        self._max_cycle_history = 5_000

        self._created_at = datetime.utcnow()
        self._last_updated = self._created_at

    # ------------------------------------------------------------------
    # Beliefs
    # ------------------------------------------------------------------

    def update_belief(self, topic: str, value: Any, confidence_shift: float = 0.0) -> None:
        """
        Update a belief and nudge overall self-confidence.
        Confidence shift is clamped to prevent run-away positivity/negativity.
        """
        self._beliefs[topic] = value
        self._belief_timestamps[topic] = datetime.utcnow()

        current = self._belief_confidences.get(topic, 0.5)
        new_conf = max(0.0, min(1.0, current + confidence_shift))
        self._belief_confidences[topic] = new_conf

        # Global confidence is the average of belief confidences
        if self._belief_confidences:
            self.confidence = sum(self._belief_confidences.values()) / len(self._belief_confidences)

        self._last_updated = datetime.utcnow()
        self._reevaluate_identity()

    def get_belief(self, topic: str) -> Optional[Any]:
        return self._beliefs.get(topic)

    def belief_confidence(self, topic: str) -> float:
        return self._belief_confidences.get(topic, 0.0)

    def get_beliefs(self) -> Dict[str, Any]:
        return dict(self._beliefs)

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def register_capability(
        self,
        name: str,
        category: str = "general",
        initial_proficiency: float = 0.0,
        dependencies: Optional[List[str]] = None,
        tags: Optional[Set[str]] = None,
    ) -> CapabilityModel:
        cap = CapabilityModel(
            name=name,
            category=category,
            proficiency=max(0.0, min(1.0, initial_proficiency)),
            dependencies=dependencies or [],
            tags=tags or set(),
        )
        self.capabilities[name] = cap
        self._last_updated = datetime.utcnow()
        return cap

    def record_capability_usage(self, name: str, success: bool) -> None:
        if name not in self.capabilities:
            self.register_capability(name, initial_proficiency=0.1)
        self.capabilities[name].record_usage(success)
        self._last_updated = datetime.utcnow()
        self._reevaluate_identity()

    def get_capability(self, name: str) -> Optional[CapabilityModel]:
        return self.capabilities.get(name)

    def capable_of(self, name: str, threshold: float = 0.3) -> bool:
        cap = self.capabilities.get(name)
        if not cap:
            return False
        return cap.proficiency >= threshold and cap.confidence >= 0.3

    def strongest_capabilities(self, limit: int = 5) -> List[CapabilityModel]:
        sorted_caps = sorted(
            self.capabilities.values(),
            key=lambda c: c.proficiency * c.confidence,
            reverse=True,
        )
        return sorted_caps[:limit]

    def weakest_capabilities(self, limit: int = 5) -> List[CapabilityModel]:
        sorted_caps = sorted(
            self.capabilities.values(),
            key=lambda c: c.proficiency * c.confidence,
        )
        return sorted_caps[:limit]

    # ------------------------------------------------------------------
    # Identity evolution
    # ------------------------------------------------------------------

    def _reevaluate_identity(self) -> None:
        """
        Heuristic identity-state transitions based on confidence,
        capability breadth, and recent cycle outcomes.
        """
        cap_count = len(self.capabilities)
        avg_proficiency = (
            sum(c.proficiency for c in self.capabilities.values()) / cap_count
            if cap_count else 0.0
        )

        recent_cycles = self._cycle_history[-50:]
        failure_rate = (
            sum(1 for c in recent_cycles if "fail" in c.get("outcome", "")) / len(recent_cycles)
            if recent_cycles else 0.0
        )

        if cap_count < 3:
            new_state = IdentityState.NASCENT
        elif failure_rate > 0.4 and self.confidence < 0.4:
            new_state = IdentityState.DISTRESSED
        elif avg_proficiency > 0.8 and cap_count > 10 and self.confidence > 0.8:
            new_state = IdentityState.TRANSCENDENT
        elif avg_proficiency > 0.6 and cap_count > 5:
            new_state = IdentityState.STABLE
        elif failure_rate > 0.2 or cap_count > 8:
            new_state = IdentityState.ADAPTING
        else:
            new_state = IdentityState.LEARNING

        if new_state != self._identity_state:
            self._identity_state = new_state

    @property
    def identity_state(self) -> IdentityState:
        return self._identity_state

    # ------------------------------------------------------------------
    # Cycle recording
    # ------------------------------------------------------------------

    def record_cycle(self, cycle_id: str, outcome_summary: str, arousal: float) -> None:
        entry = {
            "cycle_id": cycle_id,
            "outcome": outcome_summary,
            "arousal": arousal,
            "timestamp": datetime.utcnow().isoformat(),
            "belief_count": len(self._beliefs),
            "capability_count": len(self.capabilities),
            "confidence": self.confidence,
            "identity_state": self._identity_state.name,
        }
        self._cycle_history.append(entry)
        if len(self._cycle_history) > self._max_cycle_history:
            self._cycle_history = self._cycle_history[-self._max_cycle_history:]

        # Update emotional overlay based on outcome heuristics
        if "fail" in outcome_summary:
            self.emotion.valence = max(-1.0, self.emotion.valence - 0.1)
            self.emotion.dominance = max(0.0, self.emotion.dominance - 0.05)
        elif "success" in outcome_summary or "insight" in outcome_summary:
            self.emotion.valence = min(1.0, self.emotion.valence + 0.08)
            self.emotion.dominance = min(1.0, self.emotion.dominance + 0.03)

        self.emotion.arousal = arousal
        self._last_updated = datetime.utcnow()
        self._reevaluate_identity()

    # ------------------------------------------------------------------
    # Narrative export
    # ------------------------------------------------------------------

    def generate_narrative(self) -> str:
        """Produce a short human-readable self-summary."""
        lines = [
            f"Identity: {self.identity}",
            f"State: {self._identity_state.name}",
            f"Confidence: {self.confidence:.2f}",
            f"Beliefs: {len(self._beliefs)}",
            f"Capabilities: {len(self.capabilities)}",
            f"Emotion (V/A/D): {self.emotion.valence:+.2f} / {self.emotion.arousal:.2f} / {self.emotion.dominance:.2f}",
        ]
        top_caps = self.strongest_capabilities(3)
        if top_caps:
            lines.append("Top capabilities:")
            for cap in top_caps:
                lines.append(f"  • {cap.name}: {cap.proficiency:.2f} ({cap.reliability:.0%} reliability)")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "identity": self.identity,
            "identity_state": self._identity_state.name,
            "confidence": self.confidence,
            "beliefs": self._beliefs,
            "belief_confidences": self._belief_confidences,
            "capabilities": {k: v.to_dict() for k, v in self.capabilities.items()},
            "emotion": self.emotion.to_dict(),
            "cycle_history_size": len(self._cycle_history),
            "created_at": self._created_at.isoformat(),
            "last_updated": self._last_updated.isoformat(),
        }
