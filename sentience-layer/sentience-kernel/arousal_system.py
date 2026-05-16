import time
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import deque
import asyncio

@dataclass
class StimulusRecord:
    source: str
    intensity: float
    timestamp: float = field(default_factory=time.time)
    decayed: bool = False

class ArousalSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_level = config.get("base_level", 0.3)
        self.decay_rate = config.get("decay_rate", 0.05)
        self.threshold_high = config.get("threshold_high", 0.8)
        self.threshold_reflect = config.get("threshold_reflect", 0.5)
        self.window_size = config.get("window_size", 100)
        
        self.stimuli: deque = deque(maxlen=self.window_size)
        self._current_level = self.base_level
        self._last_update = time.time()
        self._lock = asyncio.Lock()
        
    async def calibrate(self):
        self.stimuli.clear()
        self._current_level = self.base_level
        self._last_update = time.time()
        
    async def register_stimulus(self, source: str, intensity: float):
        async with self._lock:
            self._update_level()
            record = StimulusRecord(source=source, intensity=min(1.0, max(0.0, intensity)))
            self.stimuli.append(record)
            self._current_level = min(1.0, self._current_level + intensity * 0.3)
            
    def _update_level(self):
        now = time.time()
        elapsed = now - self._last_update
        self._last_update = now
        
        decay = self.decay_rate * elapsed
        self._current_level = max(self.base_level, self._current_level - decay)
        
        for record in self.stimuli:
            if not record.decayed:
                age = now - record.timestamp
                if age > 60:
                    record.decayed = True
                    
    @property
    def current_level(self) -> float:
        self._update_level()
        return self._current_level
        
    def is_alert(self) -> bool:
        return self.current_level > self.threshold_high
        
    def should_reflect(self) -> bool:
        return self.current_level < self.threshold_reflect and len(self.stimuli) > 10
        
    def get_stimulus_distribution(self) -> Dict[str, float]:
        distribution = {}
        total = len(self.stimuli)
        if total == 0:
            return distribution
            
        for record in self.stimuli:
            if not record.decayed:
                distribution[record.source] = distribution.get(record.source, 0) + 1
                
        for source in distribution:
            distribution[source] /= total
            
        return distribution
        
    def get_arousal_history(self, n: int = 20) -> List[float]:
        history = []
        step = max(1, len(self.stimuli) // n) if self.stimuli else 1
        for i in range(0, len(self.stimuli), step):
            if i < len(self.stimuli):
                history.append(self.stimuli[i].intensity)
        return history[-n:]