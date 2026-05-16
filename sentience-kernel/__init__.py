from .kernel import SentienceKernel, KernelState, CognitiveEvent
from .arousal_system import ArousalSystem
from .dream_engine import DreamEngine, DreamFragment
from .doubt_generator import DoubtGenerator, DoubtPattern
from .intuition_module import IntuitionModule, IntuitionSignal
from .metacognition import MetacognitionEngine, MetaRecord
from .self_model import SelfModel, CapabilityModel, IdentityState

__version__ = "4.0.0"
__all__ = [
    "SentienceKernel",
    "KernelState",
    "CognitiveEvent",
    "ArousalSystem",
    "DreamEngine",
    "DreamFragment",
    "DoubtGenerator",
    "DoubtPattern",
    "IntuitionModule",
    "IntuitionSignal",
    "MetacognitionEngine",
    "MetaRecord",
    "SelfModel",
    "CapabilityModel",
    "IdentityState",
]