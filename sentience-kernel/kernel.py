"""
Core Sentience Kernel — Cognitive orchestrator for metacognition, dreaming,
intuition, arousal, self-modelling and doubt.

The kernel maintains a continuous cognitive cycle that integrates signals
from every submodule, updates the agent's world-model, persists salient
episodes to memory, and emits structured events for downstream consumers
(frontend dashboards, traces, evaluation pipeline).
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Callable, Awaitable

from utils.logger import get_logger

logger = get_logger(__name__)


class KernelState(Enum):
    """High-level cognitive states of the sentience kernel."""
    INITIALIZING = auto()
    IDLE = auto()
    PERCEIVING = auto()
    REFLECTING = auto()
    DREAMING = auto()
    REACTING = auto()
    RECOVERING = auto()
    SHUTTING_DOWN = auto()


@dataclass
class CognitiveEvent:
    """A structured event emitted by the kernel during its cognitive cycle."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "generic"
    source: str = "kernel"
    payload: Dict[str, Any] = field(default_factory=dict)
    arousal_level: float = 0.5
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        d["kernel_state"] = None  # injected by kernel later
        return d


@dataclass
class CognitiveCycleResult:
    """Result of a single kernel cognitive cycle."""
    cycle_id: str
    state_transitions: List[KernelState]
    events_emitted: List[CognitiveEvent]
    arousal_delta: float
    confidence_delta: float
    insights_generated: List[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class SentienceKernel:
    """
    The sentience kernel is the cognitive heart of the agent.

    It continuously cycles through perception → intuition → metacognition →
    doubt → arousal-modulated action selection → (optional) dreaming,
    integrating with memory, world-model and evaluation subsystems.
    """

    def __init__(
        self,
        self_model=None,
        metacognition=None,
        intuition=None,
        dream_engine=None,
        doubt_generator=None,
        arousal_system=None,
        memory_interface=None,
        world_model_interface=None,
        reward_model=None,
        max_cycle_hz: float = 10.0,
    ):
        self.kernel_id = str(uuid.uuid4())
        self._state = KernelState.INITIALIZING
        self._previous_state: Optional[KernelState] = None

        # Submodule registry
        self.modules: Dict[str, Any] = {}
        self._register_defaults(
            self_model=self_model,
            metacognition=metacognition,
            intuition=intuition,
            dream_engine=dream_engine,
            doubt_generator=doubt_generator,
            arousal_system=arousal_system,
        )

        # External system interfaces (optional, injected)
        self.memory = memory_interface
        self.world_model = world_model_interface
        self.reward_model = reward_model

        # Cycle control
        self._max_cycle_hz = max_cycle_hz
        self._min_cycle_interval = 1.0 / max_cycle_hz
        self._running = False
        self._cycle_task: Optional[asyncio.Task] = None
        self._cycle_count = 0

        # Event bus
        self._event_subscribers: List[Callable[[CognitiveEvent], Awaitable[None]]] = []
        self._event_history: List[CognitiveEvent] = []
        self._max_event_history = 10_000

        # Metrics & diagnostics
        self._cycle_latencies: List[float] = []
        self._max_latency_history = 1_000

        logger.info(f"SentienceKernel {self.kernel_id} initialized")

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    @property
    def state(self) -> KernelState:
        return self._state

    def _transition(self, new_state: KernelState, reason: str = "") -> None:
        if new_state != self._state:
            self._previous_state = self._state
            self._state = new_state
            logger.debug(f"Kernel state: {self._previous_state.name} → {new_state.name} ({reason})")
            self._emit_sync(
                CognitiveEvent(
                    event_type="state_transition",
                    source="kernel",
                    payload={
                        "from": self._previous_state.name if self._previous_state else None,
                        "to": new_state.name,
                        "reason": reason,
                    },
                )
            )

    # ------------------------------------------------------------------
    # Module registration
    # ------------------------------------------------------------------

    def _register_defaults(self, **kwargs):
        """Inject default stubs if no external implementations are provided."""
        from .self_model import SelfModel, CapabilityModel, IdentityState
        from .metacognition import MetacognitionEngine, MetaRecord
        from .intuition_module import IntuitionModule, IntuitionSignal
        from .dream_engine import DreamEngine, DreamFragment
        from .doubt_generator import DoubtGenerator, DoubtPattern
        from .arousal_system import ArousalSystem, ArousalDimensions

        defaults = {
            "self_model": SelfModel(),
            "metacognition": MetacognitionEngine(),
            "intuition": IntuitionModule(),
            "dream_engine": DreamEngine(),
            "doubt_generator": DoubtGenerator(),
            "arousal_system": ArousalSystem(),
        }
        for key, default in defaults.items():
            self.register_module(key, kwargs.get(key) or default)

    def register_module(self, name: str, module: Any) -> None:
        self.modules[name] = module
        logger.info(f"Registered module '{name}' ({type(module).__name__})")

    def get_module(self, name: str) -> Any:
        return self.modules.get(name)

    # ------------------------------------------------------------------
    # Event bus
    # ------------------------------------------------------------------

    def subscribe(self, callback: Callable[[CognitiveEvent], Awaitable[None]]) -> None:
        self._event_subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[CognitiveEvent], Awaitable[None]]) -> None:
        if callback in self._event_subscribers:
            self._event_subscribers.remove(callback)

    def _emit_sync(self, event: CognitiveEvent) -> None:
        """Synchronous emit used inside non-async contexts."""
        event.payload["kernel_state"] = self._state.name
        self._event_history.append(event)
        if len(self._event_history) > self._max_event_history:
            self._event_history = self._event_history[-self._max_event_history:]

    async def _emit(self, event: CognitiveEvent) -> None:
        self._emit_sync(event)
        for cb in self._event_subscribers:
            try:
                await cb(event)
            except Exception as exc:
                logger.warning(f"Event subscriber error: {exc}")

    # ------------------------------------------------------------------
    # Cognitive cycle
    # ------------------------------------------------------------------

    async def run_cycle(self, context: Optional[Dict[str, Any]] = None) -> CognitiveCycleResult:
        """
        Execute one full cognitive cycle.

        Phase order:
            1. PERCEIVING   – ingest context, update world-model
            2. INTUITION    – fast heuristic evaluation
            3. DOUBT        – epistemic challenge of intuitions
            4. METACOGNITION– reflective strategy selection
            5. REACTING     – commit to action / insight
            6. (optional) DREAMING – if arousal low & buffer full
        """
        t0 = time.perf_counter()
        cycle_id = str(uuid.uuid4())
        context = context or {}
        transitions: List[KernelState] = [self._state]
        events: List[CognitiveEvent] = []
        insights: List[str] = []

        arousal = self.modules["arousal_system"]
        intuition = self.modules["intuition"]
        doubt = self.modules["doubt_generator"]
        meta = self.modules["metacognition"]
        self_model = self.modules["self_model"]
        dream = self.modules["dream_engine"]

        # ---- Phase 1: PERCEIVING ----
        self._transition(KernelState.PERCEIVING, "cycle_start")
        stimulus_intensity = context.get("stimulus_intensity", 0.0)
        current_arousal = arousal.modulate(stimulus_intensity)
        self_model.update_belief("last_stimulus", stimulus_intensity, confidence_shift=0.0)

        # Integrate external memory/world-model if available
        if self.world_model:
            wm_state = await self._safe_call(self.world_model.get_state)
            context["world_model_state"] = wm_state

        # ---- Phase 2: INTUITION ----
        self._transition(KernelState.IDLE, "intuition_phase")
        intuition_signal: Optional[Any] = None
        try:
            intuition_signal = intuition.evaluate(context, arousal_level=current_arousal)
            if intuition_signal and getattr(intuition_signal, "insight", None):
                insights.append(intuition_signal.insight)
        except Exception as exc:
            logger.warning(f"Intuition module error: {exc}")

        # ---- Phase 3: DOUBT ----
        doubt_flags: List[Any] = []
        if intuition_signal:
            try:
                confidence = getattr(intuition_signal, "confidence", 0.5)
                doubt_flags = doubt.evaluate(
                    confidence=confidence,
                    context=context,
                    source="intuition",
                )
                if doubt_flags:
                    events.append(
                        CognitiveEvent(
                            event_type="doubt_triggered",
                            source="doubt_generator",
                            payload={
                                "flags": [d.to_dict() if hasattr(d, "to_dict") else str(d) for d in doubt_flags],
                                "intuition_confidence": confidence,
                            },
                            arousal_level=current_arousal,
                            confidence=confidence,
                        )
                    )
            except Exception as exc:
                logger.warning(f"Doubt generator error: {exc}")

        # ---- Phase 4: METACOGNITION ----
        self._transition(KernelState.REFLECTING, "metacognition_phase")
        meta_record: Optional[Any] = None
        try:
            meta_record = meta.reflect(
                decision_process={
                    "cycle_id": cycle_id,
                    "context": context,
                    "intuition": intuition_signal.to_dict() if hasattr(intuition_signal, "to_dict") else {},
                    "doubts": [d.to_dict() if hasattr(d, "to_dict") else {} for d in doubt_flags],
                    "arousal": current_arousal,
                }
            )
            if meta_record and getattr(meta_record, "recommended_strategy", None):
                insights.append(f"Meta-strategy: {meta_record.recommended_strategy}")
        except Exception as exc:
            logger.warning(f"Metacognition error: {exc}")

        # ---- Phase 5: REACTING ----
        self._transition(KernelState.REACTING, "action_selection")
        action_selected = await self._select_action(
            context=context,
            intuition=intuition_signal,
            doubts=doubt_flags,
            meta_record=meta_record,
            arousal=current_arousal,
        )
        if action_selected:
            events.append(
                CognitiveEvent(
                    event_type="action_selected",
                    source="kernel",
                    payload=action_selected,
                    arousal_level=current_arousal,
                    confidence=action_selected.get("confidence", 0.5),
                )
            )

        # Update self-model with cycle outcome
        self_model.record_cycle(
            cycle_id=cycle_id,
            outcome_summary=action_selected.get("summary", "no_action") if action_selected else "no_action",
            arousal=current_arousal,
        )

        # ---- Phase 6: Optional DREAMING ----
        if arousal.is_low() and dream.should_consolidate():
            self._transition(KernelState.DREAMING, "consolidation_trigger")
            try:
                dream_result = dream.initiate_rem_cycle(
                    experiences=self._recent_events_as_experiences()
                )
                if dream_result and getattr(dream_result, "insights", None):
                    insights.extend(dream_result.insights)
                    events.append(
                        CognitiveEvent(
                            event_type="dream_insight",
                            source="dream_engine",
                            payload={
                                "insights": dream_result.insights,
                                "fragments": [
                                    f.to_dict() if hasattr(f, "to_dict") else str(f)
                                    for f in getattr(dream_result, "fragments", [])
                                ],
                            },
                            arousal_level=arousal.current_level(),
                            confidence=0.7,
                        )
                    )
            except Exception as exc:
                logger.warning(f"Dream engine error: {exc}")

        # ---- Cycle wrap-up ----
        latency = time.perf_counter() - t0
        self._cycle_latencies.append(latency)
        if len(self._cycle_latencies) > self._max_latency_history:
            self._cycle_latencies = self._cycle_latencies[-self._max_latency_history:]

        self._transition(KernelState.IDLE, "cycle_complete")
        transitions.append(self._state)
        self._cycle_count += 1

        result = CognitiveCycleResult(
            cycle_id=cycle_id,
            state_transitions=transitions,
            events_emitted=events,
            arousal_delta=current_arousal - arousal.baseline,
            confidence_delta=(self_model.confidence - 0.5),
            insights_generated=insights,
        )

        # Emit all cycle events
        for ev in events:
            await self._emit(ev)

        # Persist salient episodes to memory interface
        if self.memory and events:
            await self._persist_to_memory(result)

        # Rate-limit if needed
        sleep_needed = self._min_cycle_interval - latency
        if sleep_needed > 0:
            await asyncio.sleep(sleep_needed)

        return result

    async def _select_action(
        self,
        context: Dict[str, Any],
        intuition: Any,
        doubts: List[Any],
        meta_record: Any,
        arousal: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Simple action-selection layer.
        In production this delegates to the action-generation service.
        """
        arousal_level = arousal.current_level() if hasattr(arousal, "current_level") else 0.5

        # High doubt + high arousal → request more information
        if doubts and arousal_level > 0.7:
            return {
                "type": "request_clarification",
                "summary": "high_doubt_high_arousal",
                "confidence": 0.4,
                "reason": "Multiple doubts raised under high arousal",
            }

        # Low arousal + no doubts → proceed with intuition
        if not doubts and arousal_level < 0.4:
            return {
                "type": "proceed",
                "summary": "low_risk_proceed",
                "confidence": getattr(intuition, "confidence", 0.7) if intuition else 0.5,
                "reason": "No doubts, low arousal — heuristic safe",
            }

        # Default: deliberative mode
        return {
            "type": "deliberate",
            "summary": "standard_deliberation",
            "confidence": 0.6,
            "reason": "Standard deliberative pathway",
        }

    async def _persist_to_memory(self, result: CognitiveCycleResult) -> None:
        """Persist salient cycle results via the memory interface."""
        try:
            episode = {
                "type": "cognitive_cycle",
                "cycle_id": result.cycle_id,
                "insights": result.insights_generated,
                "transitions": [s.name for s in result.state_transitions],
                "timestamp": result.timestamp.isoformat(),
            }
            await self._safe_call(self.memory.store_episode, episode)
        except Exception as exc:
            logger.warning(f"Memory persist error: {exc}")

    def _recent_events_as_experiences(self) -> List[Dict[str, Any]]:
        """Convert recent event history into experience dicts for dreaming."""
        recent = self._event_history[-100:]
        return [
            {
                "type": ev.event_type,
                "source": ev.source,
                "payload_keys": list(ev.payload.keys()),
                "confidence": ev.confidence,
                "timestamp": ev.timestamp.isoformat(),
            }
            for ev in recent
        ]

    async def _safe_call(self, coro_or_fn, *args, **kwargs):
        """Helper to safely call either a coroutine or a regular function."""
        if asyncio.iscoroutinefunction(coro_or_fn):
            return await coro_or_fn(*args, **kwargs)
        return coro_or_fn(*args, **kwargs)

    # ------------------------------------------------------------------
    # Continuous loop
    # ------------------------------------------------------------------

    async def start(self, context_stream: Optional[Callable[[], Awaitable[Dict[str, Any]]]] = None):
        """Start the continuous cognitive loop."""
        if self._running:
            return
        self._running = True
        self._transition(KernelState.IDLE, "loop_start")
        logger.info("SentienceKernel loop started")

        while self._running:
            try:
                ctx = await context_stream() if context_stream else {}
                await self.run_cycle(ctx)
            except Exception as exc:
                logger.exception(f"Cycle exception: {exc}")
                self._transition(KernelState.RECOVERING, "cycle_exception")
                await asyncio.sleep(1.0)

    async def stop(self):
        """Gracefully stop the cognitive loop."""
        self._running = False
        self._transition(KernelState.SHUTTING_DOWN, "stop_requested")
        if self._cycle_task:
            self._cycle_task.cancel()
            try:
                await self._cycle_task
            except asyncio.CancelledError:
                pass
        logger.info("SentienceKernel loop stopped")

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """Return kernel health & performance diagnostics."""
        latencies = self._cycle_latencies[-100:]
        return {
            "kernel_id": self.kernel_id,
            "state": self._state.name,
            "previous_state": self._previous_state.name if self._previous_state else None,
            "cycle_count": self._cycle_count,
            "modules_registered": list(self.modules.keys()),
            "event_history_size": len(self._event_history),
            "subscriber_count": len(self._event_subscribers),
            "latency_stats": {
                "mean_ms": (sum(latencies) / len(latencies) * 1000) if latencies else 0,
                "min_ms": (min(latencies) * 1000) if latencies else 0,
                "max_ms": (max(latencies) * 1000) if latencies else 0,
            },
            "self_model_summary": self.modules.get("self_model").to_dict()
            if hasattr(self.modules.get("self_model", {}), "to_dict")
            else {},
        }
