import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import deque

@dataclass
class MetaRecord:
    timestamp: float
    operation: str
    confidence: float
    accuracy: Optional[float] = None
    feedback: Optional[str] = None

class MetacognitionEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.history: deque = deque(maxlen=config.get("history_size", 1000))
        self.calibration_window = config.get("calibration_window", 100)
        self.learning_rate = config.get("learning_rate", 0.01)
        
        self._confidence_bias = 0.0
        self._accuracy_trend = []
        
    async def score(self, item: Any) -> float:
        content = getattr(item, 'content', str(item))
        length_score = min(len(content) / 500, 1.0)
        complexity_score = self._assess_complexity(content)
        
        base_confidence = 0.5 + (length_score * 0.2) + (complexity_score * 0.3)
        calibrated = base_confidence + self._confidence_bias
        
        record = MetaRecord(
            timestamp=time.time(),
            operation="score",
            confidence=min(1.0, max(0.0, calibrated))
        )
        self.history.append(record)
        
        return record.confidence
        
    async def analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        operation = params.get("operation", "unknown")
        recent = list(self.history)[-self.calibration_window:]
        
        avg_confidence = sum(r.confidence for r in recent) / max(len(recent), 1)
        calibrated_accuracy = self._estimate_accuracy(recent)
        
        return {
            "self_awareness_score": avg_confidence,
            "calibration_gap": abs(avg_confidence - calibrated_accuracy),
            "bias_estimate": self._confidence_bias,
            "recommendation": self._generate_recommendation(
                avg_confidence, calibrated_accuracy
            ),
            "trend": "improving" if self._is_improving() else "stable"
        }
        
    async def reflect_on_batch(self, items: List[Any]) -> Dict[str, Any]:
        if not items:
            return {"reflection": "No items to reflect on"}
            
        scores = []
        for item in items:
            score = await self.score(item)
            scores.append(score)
            
        avg_score = sum(scores) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        
        patterns = self._identify_patterns(items)
        
        reflection = {
            "batch_size": len(items),
            "average_confidence": avg_score,
            "confidence_variance": variance,
            "patterns": patterns,
            "suggested_adjustments": self._suggest_adjustments(avg_score, variance)
        }
        
        record = MetaRecord(
            timestamp=time.time(),
            operation="reflect",
            confidence=avg_score
        )
        self.history.append(record)
        
        return reflection
        
    def _assess_complexity(self, content: str) -> float:
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        unique_words = len(set(content.lower().split()))
        
        if words == 0:
            return 0.0
            
        diversity = unique_words / words
        density = min(sentences / 10, 1.0)
        
        return (diversity * 0.5) + (density * 0.5)
        
    def _estimate_accuracy(self, records: List[MetaRecord]) -> float:
        if not records:
            return 0.5
            
        accurate = sum(
            1 for r in records 
            if r.accuracy is not None and r.accuracy > 0.7
        )
        return accurate / len(records) if records else 0.5
        
    def _generate_recommendation(self, confidence: float, accuracy: float) -> str:
        gap = confidence - accuracy
        
        if gap > 0.2:
            return "Overconfident - increase skepticism"
        elif gap < -0.2:
            return "Underconfident - trust capabilities more"
        elif confidence < 0.5:
            return "Low confidence - gather more information"
        else:
            return "Well calibrated - maintain current approach"
            
    def _is_improving(self) -> bool:
        if len(self._accuracy_trend) < 2:
            return False
        return self._accuracy_trend[-1] > self._accuracy_trend[0]
        
    def _identify_patterns(self, items: List[Any]) -> List[str]:
        patterns = []
        contents = [str(getattr(i, 'content', i)) for i in items]
        
        avg_length = sum(len(c) for c in contents) / max(len(contents), 1)
        if avg_length > 500:
            patterns.append("long_form_content")
        else:
            patterns.append("short_form_content")
            
        return patterns
        
    def _suggest_adjustments(self, avg_score: float, variance: float) -> List[str]:
        adjustments = []
        
        if avg_score < 0.5:
            adjustments.append("Increase context gathering")
        if variance > 0.1:
            adjustments.append("Improve consistency")
        if avg_score > 0.9:
            adjustments.append("Verify against overconfidence")
            
        return adjustments