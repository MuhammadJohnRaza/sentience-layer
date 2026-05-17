"""
Dream engine — offline memory consolidation, counterfactual scenario
generation, and insight extraction.

Inspired by the critical role of sleep/REM in biological cognition,
the dream engine operates when arousal is low, recombining recent
experiences into novel scenarios, detecting hidden patterns, and
consolidating salient memories into long-term structures.
"""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Set

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class DreamFragment:
    """A discrete unit of dream content — a recombined experience."""
    fragment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_experiences: List[str] = field(default_factory=list)
    scenario: str = ""
    emotional_tone: str = "neutral"   # e.g., 'anxious', 'euphoric', 'curious'
    novelty_score: float = 0.0        # 0 = replay, 1 = highly novel recombination
    salience: float = 0.5
    insights: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class DreamResult:
    """Output of a REM cycle."""
    cycle_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fragments: List[DreamFragment] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    consolidation_score: float = 0.0
    duration_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        d["fragments"] = [f.to_dict() for f in self.fragments]
        return d


class DreamEngine:
    """
    Generates dream-like recombinations of experience for:
        1. Memory consolidation (reinforce salient patterns).
        2. Counterfactual simulation ("what if" scenarios).
        3. Insight extraction (detect non-obvious connections).
    """

    def __init__(
        self,
        consolidation_threshold: int = 50,
        max_fragments_per_cycle: int = 5,
    ):
        self.engine_id = str(uuid.uuid4())
        self.is_dreaming = False
        self.dream_log: List[DreamResult] = []
        self._max_log_size = 500

        self._experience_buffer: List[Dict[str, Any]] = []
        self._buffer_capacity = 200

        self._consolidation_threshold = consolidation_threshold
        self._max_fragments_per_cycle = max_fragments_per_cycle

        # Pattern templates for scenario generation
        self._scenario_templates = [
            "What if {subject} had chosen {alternative} instead of {original}?",
            "Imagine a world where {subject} and {unrelated} are deeply connected.",
            "Replay {event} but with {modifier} intensified tenfold.",
            "Merge the patterns of {event_a} and {event_b} into a single flow.",
            "Remove {component} from {system}. What emerges?",
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest_experience(self, experience: Dict[str, Any]) -> None:
        """Feed a new experience into the buffer for later dreaming."""
        self._experience_buffer.append(experience)
        if len(self._experience_buffer) > self._buffer_capacity:
            # Drop oldest low-salience experiences
            self._experience_buffer.sort(key=lambda e: e.get("salience", 0.5))
            self._experience_buffer = self._experience_buffer[-self._buffer_capacity:]

    def should_consolidate(self) -> bool:
        """True when the buffer is full enough to warrant a dream cycle."""
        return len(self._experience_buffer) >= self._consolidation_threshold

    def initiate_rem_cycle(
        self,
        experiences: Optional[List[Dict[str, Any]]] = None,
    ) -> DreamResult:
        """
        Run a full dream/consolidation cycle.

        If `experiences` are passed directly, they are used in addition
        to the internal buffer. The internal buffer is cleared afterward.
        """
        self.is_dreaming = True
        t0 = datetime.utcnow()

        source_pool = list(self._experience_buffer)
        if experiences:
            source_pool.extend(experiences)

        if not source_pool:
            self.is_dreaming = False
            return DreamResult(insights=["No experiences to dream about."])

        fragments: List[DreamFragment] = []
        insights: Set[str] = set()

        # --- Fragment generation ---
        num_fragments = min(self._max_fragments_per_cycle, max(1, len(source_pool) // 10))
        for _ in range(num_fragments):
            frag = self._generate_fragment(source_pool)
            fragments.append(frag)
            insights.update(frag.insights)

        # --- Cross-fragment insight extraction ---
        cross_insights = self._extract_cross_fragment_insights(fragments)
        insights.update(cross_insights)

        # --- Consolidation scoring ---
        consolidation_score = self._compute_consolidation_score(fragments, source_pool)

        # Clear buffer (consolidated)
        cleared_count = len(self._experience_buffer)
        self._experience_buffer.clear()

        duration = (datetime.utcnow() - t0).total_seconds()

        result = DreamResult(
            fragments=fragments,
            insights=sorted(insights),
            consolidation_score=consolidation_score,
            duration_seconds=duration,
        )

        self.dream_log.append(result)
        if len(self.dream_log) > self._max_log_size:
            self.dream_log = self.dream_log[-self._max_log_size:]

        self.is_dreaming = False
        logger.info(
            f"REM cycle complete: {len(fragments)} fragments, "
            f"{len(insights)} insights, score={consolidation_score:.2f}, "
            f"cleared={cleared_count} experiences"
        )
        return result

    def get_dream_statistics(self) -> Dict[str, Any]:
        """Aggregate statistics over all dream cycles."""
        if not self.dream_log:
            return {"total_cycles": 0}

        total_fragments = sum(len(d.fragments) for d in self.dream_log)
        total_insights = sum(len(d.insights) for d in self.dream_log)
        avg_consolidation = sum(d.consolidation_score for d in self.dream_log) / len(self.dream_log)

        return {
            "total_cycles": len(self.dream_log),
            "total_fragments": total_fragments,
            "total_insights": total_insights,
            "avg_consolidation_score": avg_consolidation,
            "buffer_size": len(self._experience_buffer),
            "is_dreaming_now": self.is_dreaming,
        }

    # ------------------------------------------------------------------
    # Fragment generation
    # ------------------------------------------------------------------

    def _generate_fragment(self, pool: List[Dict[str, Any]]) -> DreamFragment:
        """Create a single dream fragment by recombining experiences."""
        # Pick 2-4 experiences
        k = min(len(pool), random.randint(2, 4))
        samples = random.sample(pool, k)
        source_ids = [s.get("id", s.get("type", "unknown")) for s in samples]

        # Build scenario
        template = random.choice(self._scenario_templates)
        scenario = self._fill_template(template, samples)

        # Determine emotional tone heuristically
        tones = ["neutral", "anxious", "curious", "euphoric", "melancholic"]
        emotional_tone = random.choice(tones)

        # Compute novelty (higher when samples are from disparate sources)
        source_types = {s.get("type", "unknown") for s in samples}
        novelty = len(source_types) / max(1, len(samples))

        # Salience is max of component saliences
        salience = max((s.get("salience", 0.5) for s in samples), default=0.5)

        # Extract insights via simple pattern matching
        insights = self._extract_insights(samples, scenario)

        return DreamFragment(
            source_experiences=source_ids,
            scenario=scenario,
            emotional_tone=emotional_tone,
            novelty_score=novelty,
            salience=salience,
            insights=insights,
        )

    def _fill_template(self, template: str, samples: List[Dict[str, Any]]) -> str:
        """Naïve template filling using random fields from samples."""
        try:
            subject = random.choice(samples).get("type", "the agent")
            original = random.choice(samples).get("outcome", "the default")
            alternative = random.choice(["success", "failure", "delay", "shortcut"])
            unrelated = random.choice(samples).get("source", "another module")
            event = random.choice(samples).get("type", "an event")
            modifier = random.choice(["urgency", "uncertainty", "reward", "risk"])
            event_a = random.choice(samples).get("type", "event A")
            event_b = random.choice(samples).get("type", "event B")
            component = random.choice(["feedback loop", "human oversight", "randomness"])
            system = random.choice(samples).get("source", "the system")

            return template.format(
                subject=subject,
                original=original,
                alternative=alternative,
                unrelated=unrelated,
                event=event,
                modifier=modifier,
                event_a=event_a,
                event_b=event_b,
                component=component,
                system=system,
            )
        except (KeyError, IndexError):
            return "A vague recombination of recent experiences."

    # ------------------------------------------------------------------
    # Insight extraction
    # ------------------------------------------------------------------

    def _extract_insights(
        self, samples: List[Dict[str, Any]], scenario: str
    ) -> List[str]:
        """Lightweight insight extraction — can be upgraded with LLM."""
        insights: List[str] = []
        confidences = [s.get("confidence", 0.5) for s in samples]
        types = [s.get("type", "unknown") for s in samples]

        # Insight: confidence divergence
        if confidences:
            spread = max(confidences) - min(confidences)
            if spread > 0.5:
                insights.append(
                    f"High confidence divergence detected ({spread:.2f}) among {types}."
                )

        # Insight: repeated source type
        from collections import Counter
        type_counts = Counter(types)
        most_common, count = type_counts.most_common(1)[0]
        if count >= 3:
            insights.append(
                f"Frequent '{most_common}' events may indicate a systemic pattern."
            )

        # Insight: low-confidence cluster
        low_conf = [c for c in confidences if c < 0.4]
        if len(low_conf) >= 2:
            insights.append(
                f"Cluster of {len(low_conf)} low-confidence experiences suggests knowledge gap."
            )

        return insights

    def _extract_cross_fragment_insights(self, fragments: List[DreamFragment]) -> Set[str]:
        """Look for patterns *across* fragments."""
        insights: Set[str] = set()
        if len(fragments) < 2:
            return insights

        # Detect recurring emotional tones
        tones = [f.emotional_tone for f in fragments]
        from collections import Counter
        tone_counts = Counter(tones)
        dominant_tone, tone_count = tone_counts.most_common(1)[0]
        if tone_count >= len(fragments) * 0.6:
            insights.add(f"Dominant dream tone is '{dominant_tone}' — may reflect underlying affective state.")

        # Detect high-novelty streak
        avg_novelty = sum(f.novelty_score for f in fragments) / len(fragments)
        if avg_novelty > 0.7:
            insights.add("High average novelty in dreams — system is in rapid learning phase.")

        return insights

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _compute_consolidation_score(
        self, fragments: List[DreamFragment], pool: List[Dict[str, Any]]
    ) -> float:
        """
        Heuristic: good consolidation when fragments cover many source
        experiences with high salience and generate insights.
        """
        if not fragments or not pool:
            return 0.0

        covered = set()
        for frag in fragments:
            covered.update(frag.source_experiences)

        coverage = len(covered) / len(pool)
        avg_salience = sum(f.salience for f in fragments) / len(fragments)
        insight_density = sum(len(f.insights) for f in fragments) / len(fragments)

        score = (coverage * 0.4) + (avg_salience * 0.3) + (min(1.0, insight_density / 3.0) * 0.3)
        return min(1.0, score)
