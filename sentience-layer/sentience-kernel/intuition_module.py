import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class IntuitionSignal:
    content: str
    confidence: float
    source_pattern: str
    urgency: float

class IntuitionModule:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pattern_library: Dict[str, List[str]] = {
            "anomaly": [
                "Something doesn't fit the pattern",
                "This breaks the usual flow",
                "Unexpected deviation detected"
            ],
            "opportunity": [
                "There's a window opening here",
                "This could be leveraged",
                "A favorable alignment exists"
            ],
            "threat": [
                "This path feels risky",
                "Caution advised here",
                "Potential downside ahead"
            ],
            "insight": [
                "These pieces connect differently",
                "A deeper pattern emerges",
                "The underlying structure reveals itself"
            ],
            "familiarity": [
                "I've seen this pattern before",
                "This resonates with past experience",
                "Historical parallel detected"
            ]
        }
        self.confidence_threshold = config.get("confidence_threshold", 0.6)
        self.signal_history: List[IntuitionSignal] = []
        
    async def generate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        content = params.get("content", "")
        context = params.get("context", {})
        
        signals = []
        for pattern_type, templates in self.pattern_library.items():
            signal = await self._generate_signal(
                content, context, pattern_type, templates
            )
            if signal.confidence > self.confidence_threshold:
                signals.append(signal)
                
        signals.sort(key=lambda x: x.confidence * x.urgency, reverse=True)
        
        return {
            "signals": [
                {
                    "content": s.content,
                    "confidence": s.confidence,
                    "pattern": s.source_pattern,
                    "urgency": s.urgency
                }
                for s in signals[:3]
            ],
            "dominant_pattern": signals[0].source_pattern if signals else "neutral",
            "aggregate_confidence": sum(s.confidence for s in signals) / max(len(signals), 1)
        }
        
    async def _generate_signal(
        self,
        content: str,
        context: Dict[str, Any],
        pattern_type: str,
        templates: List[str]
    ) -> IntuitionSignal:
        base_confidence = random.uniform(0.3, 0.95)
        
        context_boost = 0.1 if context else 0.0
        length_factor = min(len(content) / 1000, 0.1)
        
        confidence = min(1.0, base_confidence + context_boost + length_factor)
        
        template = random.choice(templates)
        
        urgency_map = {
            "threat": 0.9,
            "anomaly": 0.7,
            "opportunity": 0.6,
            "insight": 0.5,
            "familiarity": 0.4
        }
        
        return IntuitionSignal(
            content=template,
            confidence=confidence,
            source_pattern=pattern_type,
            urgency=urgency_map.get(pattern_type, 0.5)
        )
        
    def add_pattern(self, pattern_type: str, templates: List[str]):
        if pattern_type not in self.pattern_library:
            self.pattern_library[pattern_type] = []
        self.pattern_library[pattern_type].extend(templates)
        
    def get_pattern_stats(self) -> Dict[str, int]:
        return {
            pattern: len(templates) 
            for pattern, templates in self.pattern_library.items()
        }