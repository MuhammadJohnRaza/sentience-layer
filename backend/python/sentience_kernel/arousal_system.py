"""
Arousal system — multi-dimensional attention and processing-depth modulator.

Arousal is not a single scalar in biological cognition; it spans alertness,
curiosity, anxiety, and cognitive effort. The ArousalSystem maintains these
dimensions, modulates them based on stimulus characteristics, and exposes
current levels to guide the kernel's decision between fast heuristic and
deep deliberative processing.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ArousalDimensions:
    """
    Multi-dimensional arousal state.

    Dimensions:
        alertness     – readiness to respond to external stimuli
        curiosity     – drive to explore / seek information
        anxiety       – threat-detection activation (can be useful)
        effort        – willingness to expend cognitive resources
        valence       – positive (approach) vs negative (avoid) tone
    """
    alertness: float = 0.5
    curiosity: float = 0.5
    anxiety: float = 0.0
    effort: float = 0.5
    valence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    @property
    def mean(self) -> float:
        return (self.alertness + self.curiosity + self.anxiety + self.effort) / 4.0


class StimulusProfile:
    """Typed descriptor for an incoming stimulus."""

    def __init__(
        self,
        intensity: float = 0.0,
        novelty: float = 0.5,
        threat_potential: float = 0.0,
        reward_potential: float = 0.0,
        urgency: float = 0.0,
        source: str = "unknown",
    ):
        self.intensity = max(0.0, min(1.0, intensity))
        self.novelty = max(0.0, min(1.0, novelty))
        self.threat_potential = max(0.0, min(1.0, threat_potential))
        self.reward_potential = max(0.0, min(1.0, reward_potential))
        self.urgency = max(0.0, min(1.0, urgency))
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intensity": self.intensity,
            "novelty": self.novelty,
            "threat_potential": self.threat_potential,
            "reward_potential": self.reward_potential,
            "urgency": self.urgency,
            "source": self.source,
        }


class ArousalSystem:
    """
    Modulates the agent's cognitive posture along multiple arousal dimensions.

    Responsibilities:
        1. Translate raw stimuli into dimensional arousal changes.
        2. Decay arousal naturally toward baseline over time.
        3. Provide unified indices (level, is_low, is_high) for kernel use.
        4. Log stimulus-response pairs for later analysis.
    """

    def __init__(
        self,
        baseline: float = 0.3,
        decay_rate_per_second: float = 0.05,
    ):
        self.system_id = str(uuid.uuid4())
        self.baseline = baseline
        self._decay_rate = decay_rate_per_second

        self.dimensions = ArousalDimensions()
        self._last_update = time.monotonic()

        self._stimulus_log: List[Dict[str, Any]] = []
        self._max_log_size = 1_000

    # ------------------------------------------------------------------
    # Core modulation
    # ------------------------------------------------------------------

    def modulate(self, stimulus_intensity: float) -> float:
        """
        Legacy scalar API — maps intensity onto a uniform arousal bump
        distributed across dimensions heuristically.
        """
        profile = StimulusProfile(
            intensity=stimulus_intensity,
            novelty=stimulus_intensity * 0.5,
            urgency=stimulus_intensity * 0.3,
        )
        return self.modulate_from_profile(profile)

    def modulate_from_profile(self, profile: StimulusProfile) -> float:
        """
        Dimensional modulation based on a full stimulus profile.
        Returns the unified arousal level.
        """
        self._apply_decay()

        # Alertness: driven by intensity + urgency
        self.dimensions.alertness = self._bump(
            self.dimensions.alertness,
            profile.intensity * 0.4 + profile.urgency * 0.4,
        )

        # Curiosity: driven by novelty + reward potential
        self.dimensions.curiosity = self._bump(
            self.dimensions.curiosity,
            profile.novelty * 0.35 + profile.reward_potential * 0.25,
        )

        # Anxiety: driven by threat potential + uncertainty
        self.dimensions.anxiety = self._bump(
            self.dimensions.anxiety,
            profile.threat_potential * 0.5 + profile.novelty * 0.15,
        )

        # Effort: driven by urgency + reward potential
        self.dimensions.effort = self._bump(
            self.dimensions.effort,
            profile.urgency * 0.3 + profile.reward_potential * 0.2,
        )

        # Valence: net approach/avoid signal
        valence_delta = profile.reward_potential * 0.3 - profile.threat_potential * 0.3
        self.dimensions.valence = max(-1.0, min(1.0, self.dimensions.valence + valence_delta))

        self.dimensions.timestamp = datetime.utcnow()
        self._log_stimulus(profile)

        logger.debug(f"Arousal modulated: mean={self.current_level():.2f}, profile={profile.to_dict()}")
        return self.current_level()

    def _bump(self, current: float, delta: float, max_val: float = 1.0) -> float:
        """Additive modulation with ceiling."""
        return min(max_val, current + delta * 0.1)

    def _apply_decay(self) -> None:
        """Exponential decay toward baseline since last update."""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._last_update = now

        if elapsed <= 0:
            return

        decay_factor = max(0.0, 1.0 - self._decay_rate * elapsed)
        for dim in ("alertness", "curiosity", "anxiety", "effort"):
            current = getattr(self.dimensions, dim)
            baseline = self.baseline if dim != "anxiety" else 0.0
            new_val = baseline + (current - baseline) * decay_factor
            setattr(self.dimensions, dim, new_val)

        # Valence decays toward 0
        self.dimensions.valence *= decay_factor

    # ------------------------------------------------------------------
    # Unified indices
    # ------------------------------------------------------------------

    def current_level(self) -> float:
        """Unified scalar arousal for backward compatibility."""
        return self.dimensions.mean

    def is_low(self, threshold: float = 0.25) -> bool:
        """True when arousal is low enough to permit dreaming/consolidation."""
        return self.current_level() < threshold

    def is_high(self, threshold: float = 0.75) -> bool:
        """True when arousal demands fast, shallow processing."""
        return self.current_level() > threshold

    def recommended_processing_depth(self) -> str:
        """Suggest cognitive depth based on current arousal."""
        level = self.current_level()
        if level < 0.25:
            return "deep"
        elif level < 0.6:
            return "balanced"
        else:
            return "shallow"

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _log_stimulus(self, profile: StimulusProfile) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "profile": profile.to_dict(),
            "dimensions_after": self.dimensions.to_dict(),
        }
        self._stimulus_log.append(entry)
        if len(self._stimulus_log) > self._max_log_size:
            self._stimulus_log = self._stimulus_log[-self._max_log_size:]

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "system_id": self.system_id,
            "baseline": self.baseline,
            "decay_rate": self._decay_rate,
            "current_dimensions": self.dimensions.to_dict(),
            "unified_level": self.current_level(),
            "recommended_depth": self.recommended_processing_depth(),
            "stimulus_log_size": len(self._stimulus_log),
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.diagnostics()
