import asyncio
import math
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

class DecayStrategy(Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    STEP = "step"
    NONE = "none"

@dataclass
class DecayConfig:
    strategy: DecayStrategy = DecayStrategy.EXPONENTIAL
    half_life_hours: float = 168.0
    min_retention: float = 0.1
    boost_on_access: float = 0.2
    emotional_boost: float = 0.3

class MemoryDecayEngine:
    def __init__(self):
        self._config = DecayConfig()
        self._retention_scores: Dict[str, float] = {}
        self._last_accessed: Dict[str, datetime] = {}

    async def apply_decay(
        self,
        memory_ids: Optional[List[str]] = None,
        rate: Optional[float] = None
    ) -> int:
        if rate is not None:
            self._config.half_life_hours = max(1.0, 168.0 / rate)
        
        now = datetime.utcnow()
        ids_to_process = memory_ids or list(self._retention_scores.keys())
        decayed_count = 0
        
        for mid in ids_to_process:
            if mid not in self._retention_scores:
                self._retention_scores[mid] = 1.0
                self._last_accessed[mid] = now
                continue
            
            last_access = self._last_accessed.get(mid, now)
            hours_elapsed = (now - last_access).total_seconds() / 3600
            
            current = self._retention_scores[mid]
            decayed = self._compute_decay(current, hours_elapsed)
            
            if decayed != current:
                self._retention_scores[mid] = decayed
                decayed_count += 1
        
        logger.info(f"Decay applied to {decayed_count} memories")
        return decayed_count

    def _compute_decay(
        self,
        current_retention: float,
        hours_elapsed: float
    ) -> float:
        if self._config.strategy == DecayStrategy.NONE:
            return current_retention
        
        if self._config.strategy == DecayStrategy.EXPONENTIAL:
            decayed = current_retention * math.exp(
                -0.693 * hours_elapsed / self._config.half_life_hours
            )
        elif self._config.strategy == DecayStrategy.LINEAR:
            decay_rate = (1.0 - self._config.min_retention) / self._config.half_life_hours
            decayed = current_retention - decay_rate * hours_elapsed
        elif self._config.strategy == DecayStrategy.STEP:
            periods = hours_elapsed / self._config.half_life_hours
            decayed = current_retention * (0.5 ** int(periods))
        else:
            return current_retention
        
        return max(self._config.min_retention, min(1.0, decayed))

    async def boost(
        self,
        memory_id: str,
        boost_amount: Optional[float] = None
    ) -> float:
        if memory_id not in self._retention_scores:
            self._retention_scores[memory_id] = 1.0
        
        boost = boost_amount or self._config.boost_on_access
        current = self._retention_scores[memory_id]
        boosted = min(1.0, current + boost)
        
        self._retention_scores[memory_id] = boosted
        self._last_accessed[memory_id] = datetime.utcnow()
        
        return boosted

    async def get_retention(self, memory_id: str) -> float:
        return self._retention_scores.get(memory_id, 1.0)

    async def should_forget(self, memory_id: str, threshold: float = 0.15) -> bool:
        retention = await self.get_retention(memory_id)
        return retention < threshold

    async def configure(self, config: DecayConfig) -> None:
        self._config = config
        logger.info(f"Decay configuration updated: {config.strategy.value}")

    async def get_stats(self) -> Dict[str, Any]:
        scores = list(self._retention_scores.values())
        
        if not scores:
            return {"total_memories": 0}
        
        return {
            "total_memories": len(scores),
            "avg_retention": sum(scores) / len(scores),
            "min_retention": min(scores),
            "max_retention": max(scores),
            "strategy": self._config.strategy.value,
            "half_life_hours": self._config.half_life_hours
        }