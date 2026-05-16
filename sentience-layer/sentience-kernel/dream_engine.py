import random
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class DreamFragment:
    source_memory: str
    transformed_content: Any
    emotional_valence: float
    association_strength: float

class DreamEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.consolidation_interval = config.get("consolidation_interval", 3600)
        self.fragment_pool_size = config.get("fragment_pool_size", 100)
        self.association_depth = config.get("association_depth", 3)
        
        self.fragments: List[DreamFragment] = []
        self.dream_log: List[Dict[str, Any]] = []
        self._dreaming = False
        
    async def consolidate(self, memories: List[Any]) -> List[DreamFragment]:
        new_fragments = []
        for memory in memories:
            for _ in range(self.association_depth):
                fragment = await self._transform(memory)
                if fragment:
                    new_fragments.append(fragment)
                    
        self.fragments.extend(new_fragments)
        if len(self.fragments) > self.fragment_pool_size:
            self.fragments = self.fragments[-self.fragment_pool_size:]
            
        return new_fragments
        
    async def generate_dream(self, seed: Optional[Any] = None) -> Dict[str, Any]:
        self._dreaming = True
        
        if not self.fragments:
            self._dreaming = False
            return {"narrative": "Silence...", "insights": []}
            
        selected = random.sample(
            self.fragments, 
            min(5, len(self.fragments))
        )
        
        narrative = await self._weave_narrative(selected)
        insights = await self._extract_insights(selected)
        
        dream_record = {
            "timestamp": time.time(),
            "narrative": narrative,
            "insights": insights,
            "fragment_count": len(selected)
        }
        self.dream_log.append(dream_record)
        
        self._dreaming = False
        return dream_record
        
    async def _transform(self, memory: Any) -> Optional[DreamFragment]:
        content = getattr(memory, 'content', str(memory))
        valence = random.uniform(-1.0, 1.0)
        strength = random.uniform(0.1, 1.0)
        
        transformations = [
            lambda x: f"Perhaps {x} means something deeper",
            lambda x: f"What if {x} was different",
            lambda x: f"Remember when {x} seemed important",
            lambda x: f"{x} connects to everything"
        ]
        
        transformed = random.choice(transformations)(content)
        
        return DreamFragment(
            source_memory=str(id(memory)),
            transformed_content=transformed,
            emotional_valence=valence,
            association_strength=strength
        )
        
    async def _weave_narrative(self, fragments: List[DreamFragment]) -> str:
        parts = []
        for frag in fragments:
            parts.append(frag.transformed_content)
            
        connectors = ["Then", "Suddenly", "Meanwhile", "In another place", "But"]
        narrative = fragments[0].transformed_content if fragments else ""
        
        for i, frag in enumerate(fragments[1:], 1):
            connector = connectors[i % len(connectors)]
            narrative += f". {connector}, {frag.transformed_content}"
            
        return narrative + "."
        
    async def _extract_insights(self, fragments: List[DreamFragment]) -> List[str]:
        insights = []
        for frag in fragments:
            if frag.association_strength > 0.7:
                insights.append(
                    f"Strong association detected in: {frag.transformed_content[:50]}..."
                )
            if abs(frag.emotional_valence) > 0.6:
                insights.append(
                    f"Emotional significance: {frag.transformed_content[:50]}..."
                )
        return insights
        
    def is_dreaming(self) -> bool:
        return self._dreaming