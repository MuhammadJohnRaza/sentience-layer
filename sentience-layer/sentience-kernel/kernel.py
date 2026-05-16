import asyncio
import time
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

from .arousal_system import ArousalSystem
from .dream_engine import DreamEngine
from .doubt_generator import DoubtGenerator
from .intuition_module import IntuitionModule
from .metacognition import MetacognitionEngine
from .self_model import SelfModel

logger = logging.getLogger(__name__)

class KernelState(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    REFLECTING = "reflecting"
    DREAMING = "dreaming"
    ALERT = "alert"

@dataclass
class CognitiveEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    content: Any = None
    priority: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

class SentienceKernel:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.state = KernelState.IDLE
        self.event_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.memory_buffer: List[CognitiveEvent] = []
        self.max_buffer_size = self.config.get("max_buffer_size", 1000)
        
        self.arousal = ArousalSystem(self.config.get("arousal", {}))
        self.dream = DreamEngine(self.config.get("dream", {}))
        self.doubt = DoubtGenerator(self.config.get("doubt", {}))
        self.intuition = IntuitionModule(self.config.get("intuition", {}))
        self.metacognition = MetacognitionEngine(self.config.get("metacognition", {}))
        self.self_model = SelfModel(self.config.get("self_model", {}))
        
        self._running = False
        self._handlers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()
        
    async def boot(self):
        logger.info("Sentience Kernel booting...")
        await self.self_model.initialize()
        await self.arousal.calibrate()
        self._running = True
        asyncio.create_task(self._main_loop())
        logger.info("Sentience Kernel active")
        
    async def shutdown(self):
        self._running = False
        await self._flush_buffer()
        logger.info("Sentience Kernel shutdown complete")
        
    async def ingest(self, event: CognitiveEvent) -> str:
        event_id = event.id
        priority = 1.0 - event.priority
        await self.event_queue.put((priority, time.time(), event))
        self.arousal.register_stimulus(event.source, event.priority)
        return event_id
        
    async def query(self, query_type: str, params: Dict[str, Any]) -> Any:
        async with self._lock:
            self.state = KernelState.PROCESSING
            
            if query_type == "intuition":
                result = await self.intuition.generate(params)
            elif query_type == "doubt":
                result = await self.doubt.evaluate(params)
            elif query_type == "self":
                result = await self.self_model.reflect(params)
            elif query_type == "meta":
                result = await self.metacognition.analyze(params)
            else:
                result = {"error": f"Unknown query type: {query_type}"}
                
            self.state = KernelState.IDLE
            return result
            
    async def _main_loop(self):
        while self._running:
            try:
                _, _, event = await asyncio.wait_for(
                    self.event_queue.get(), timeout=1.0
                )
                await self._process_event(event)
            except asyncio.TimeoutError:
                if self.arousal.should_reflect():
                    await self._reflect()
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                
    async def _process_event(self, event: CognitiveEvent):
        self.state = KernelState.PROCESSING
        
        processed = {
            "event": event,
            "intuition": await self.intuition.generate({"content": event.content}),
            "confidence": await self.metacognition.score(event),
            "doubt": await self.doubt.evaluate({"content": event.content})
        }
        
        self.memory_buffer.append(processed)
        if len(self.memory_buffer) > self.max_buffer_size:
            self.memory_buffer.pop(0)
            
        await self._emit("event_processed", processed)
        self.state = KernelState.IDLE
        
    async def _reflect(self):
        self.state = KernelState.REFLECTING
        recent = self.memory_buffer[-50:]
        reflection = await self.metacognition.reflect_on_batch(recent)
        await self.self_model.update(reflection)
        self.state = KernelState.IDLE
        
    async def _flush_buffer(self):
        if self.memory_buffer:
            await self.self_model.consolidate(self.memory_buffer)
            self.memory_buffer.clear()
            
    def on(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        
    async def _emit(self, event_type: str, data: Any):
        for handler in self._handlers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Handler error: {e}")