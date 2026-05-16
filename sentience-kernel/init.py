"""
Initialization module for the sentience kernel.

Provides factory functions, dependency injection wiring, and lifecycle
hooks for bootstrapping the kernel in different environments
(development, testing, production).
"""

from __future__ import annotations

import asyncio
import os
from typing import Dict, Any, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


def initialize_kernel(
    config: Optional[Dict[str, Any]] = None,
    memory_interface=None,
    world_model_interface=None,
    reward_model=None,
) -> "SentienceKernel":
    """
    Bootstrap a fully configured SentienceKernel.

    Args:
        config: Optional dict with keys such as:
            - max_cycle_hz (float)
            - identity (str)
            - consolidation_threshold (int)
            - epistemic_aggressiveness (float)
            - base_doubt_threshold (float)
            - seed_heuristics (bool)
        memory_interface: Object implementing store_episode().
        world_model_interface: Object implementing get_state().
        reward_model: Evaluation reward model for scoring outcomes.

    Returns:
        A configured SentienceKernel instance ready to start.
    """
    from .kernel import SentienceKernel
    from .self_model import SelfModel
    from .metacognition import MetacognitionEngine
    from .intuition_module import IntuitionModule
    from .dream_engine import DreamEngine
    from .doubt_generator import DoubtGenerator
    from .arousal_system import ArousalSystem

    config = config or {}

    # --- Instantiate submodules with config overrides ---
    self_model = SelfModel(identity=config.get("identity"))

    metacognition = MetacognitionEngine()

    intuition = IntuitionModule()
    if config.get("seed_heuristics", True):
        # Already seeded in constructor, but allow future custom seeding here
        pass

    dream_engine = DreamEngine(
        consolidation_threshold=config.get("consolidation_threshold", 50),
        max_fragments_per_cycle=config.get("max_fragments_per_cycle", 5),
    )

    doubt_generator = DoubtGenerator(
        base_doubt_threshold=config.get("base_doubt_threshold", 0.7),
        epistemic_aggressiveness=config.get("epistemic_aggressiveness", 0.5),
    )

    arousal_system = ArousalSystem(
        baseline=config.get("arousal_baseline", 0.3),
        decay_rate_per_second=config.get("arousal_decay_rate", 0.05),
    )

    # --- Assemble kernel ---
    kernel = SentienceKernel(
        self_model=self_model,
        metacognition=metacognition,
        intuition=intuition,
        dream_engine=dream_engine,
        doubt_generator=doubt_generator,
        arousal_system=arousal_system,
        memory_interface=memory_interface,
        world_model_interface=world_model_interface,
        reward_model=reward_model,
        max_cycle_hz=config.get("max_cycle_hz", 10.0),
    )

    logger.info("SentienceKernel initialized via factory")
    return kernel


async def run_diagnostics(kernel: "SentienceKernel") -> Dict[str, Any]:
    """Run a quick diagnostic cycle and return health report."""
    report = {
        "kernel": kernel.diagnostics(),
        "modules": {},
    }
    for name, mod in kernel.modules.items():
        if hasattr(mod, "diagnostics"):
            report["modules"][name] = mod.diagnostics()
        elif hasattr(mod, "to_dict"):
            report["modules"][name] = mod.to_dict()
        else:
            report["modules"][name] = {"type": type(mod).__name__}

    # Run one silent cycle to verify execution
    try:
        result = await kernel.run_cycle({"stimulus_intensity": 0.1})
        report["test_cycle"] = {
            "cycle_id": result.cycle_id,
            "transitions": [s.name for s in result.state_transitions],
            "events_count": len(result.events_emitted),
            "insights_count": len(result.insights_generated),
            "success": True,
        }
    except Exception as exc:
        report["test_cycle"] = {"success": False, "error": str(exc)}

    return report


def initialize_kernel_sync(
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> "SentienceKernel":
    """Synchronous wrapper for initialize_kernel."""
    return initialize_kernel(config=config, **kwargs)
