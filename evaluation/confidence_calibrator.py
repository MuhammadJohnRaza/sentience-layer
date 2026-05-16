import asyncio
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean, stdev

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class CalibrationResult:
    model_id: str
    original_confidence: float
    calibrated_confidence: float
    calibration_error: float
    reliability_diagram: List[Dict[str, Any]] = field(default_factory=list)
    is_well_calibrated: bool = False
    sample_count: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

class ConfidenceCalibrator:
    def __init__(self):
        self._bins: int = 10
        self._history: List[Dict[str, Any]] = []
        self._max_history: int = 10000

    async def calibrate(
        self,
        model_id: str,
        predictions: List[Dict[str, Any]]
    ) -> CalibrationResult:
        if not predictions:
            return CalibrationResult(
                model_id=model_id,
                original_confidence=0.5,
                calibrated_confidence=0.5,
                calibration_error=0.0,
                sample_count=0
            )
        
        bin_stats = self._compute_bin_statistics(predictions)
        reliability = self._build_reliability_diagram(bin_stats)
        
        original_confidences = [p["confidence"] for p in predictions]
        avg_original = mean(original_confidences) if original_confidences else 0.5
        
        accuracies = [1.0 if p.get("correct", False) else 0.0 for p in predictions]
        avg_accuracy = mean(accuracies) if accuracies else 0.5
        
        calibration_error = sum(
            abs(r["confidence"] - r["accuracy"]) * r["count"]
            for r in reliability
        ) / len(predictions) if predictions else 0.0
        
        calibrated = self._apply_temperature_scaling(original_confidences, avg_accuracy)
        
        is_well_calibrated = calibration_error < 0.1
        
        result = CalibrationResult(
            model_id=model_id,
            original_confidence=avg_original,
            calibrated_confidence=calibrated,
            calibration_error=calibration_error,
            reliability_diagram=reliability,
            is_well_calibrated=is_well_calibrated,
            sample_count=len(predictions)
        )
        
        self._history.append({
            "model_id": model_id,
            "result": result,
            "timestamp": datetime.utcnow()
        })
        
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        return result

    def _compute_bin_statistics(
        self,
        predictions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        bins: List[List[Dict[str, Any]]] = [[] for _ in range(self._bins)]
        
        for pred in predictions:
            confidence = pred.get("confidence", 0.5)
            bin_idx = min(int(confidence * self._bins), self._bins - 1)
            bins[bin_idx].append(pred)
        
        stats = []
        for i, bin_preds in enumerate(bins):
            if not bin_preds:
                continue
            
            confidences = [p["confidence"] for p in bin_preds]
            accuracies = [1.0 if p.get("correct", False) else 0.0 for p in bin_preds]
            
            stats.append({
                "bin": i,
                "range": (i / self._bins, (i + 1) / self._bins),
                "count": len(bin_preds),
                "avg_confidence": mean(confidences),
                "accuracy": mean(accuracies),
                "predictions": bin_preds
            })
        
        return stats

    def _build_reliability_diagram(
        self,
        bin_stats: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return [
            {
                "confidence": s["avg_confidence"],
                "accuracy": s["accuracy"],
                "count": s["count"],
                "gap": abs(s["avg_confidence"] - s["accuracy"])
            }
            for s in bin_stats
        ]

    def _apply_temperature_scaling(
        self,
        confidences: List[float],
        target_accuracy: float
    ) -> float:
        if not confidences:
            return 0.5
        
        avg_conf = mean(confidences)
        
        if avg_conf == 0:
            return 0.0
        
        temperature = avg_conf / target_accuracy if target_accuracy > 0 else 1.0
        temperature = max(0.1, min(10.0, temperature))
        
        scaled = [c / temperature for c in confidences]
        return mean(scaled) if scaled else 0.5

    async def get_calibration_history(
        self,
        model_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        filtered = [
            h for h in self._history
            if model_id is None or h["model_id"] == model_id
        ]
        
        return [
            {
                "model_id": h["model_id"],
                "calibration_error": h["result"].calibration_error,
                "is_well_calibrated": h["result"].is_well_calibrated,
                "timestamp": h["timestamp"].isoformat()
            }
            for h in filtered[-limit:]
        ]

    async def suggest_adjustment(self, model_id: str) -> Dict[str, Any]:
        history = [h for h in self._history if h["model_id"] == model_id]
        
        if not history:
            return {"suggestion": "insufficient_data"}
        
        recent = history[-10:]
        avg_error = mean(h["result"].calibration_error for h in recent)
        
        if avg_error > 0.2:
            return {
                "suggestion": "recalibrate",
                "urgency": "high",
                "recommended_temperature": 1.5,
                "reason": f"High calibration error: {avg_error:.3f}"
            }
        elif avg_error > 0.1:
            return {
                "suggestion": "monitor",
                "urgency": "medium",
                "reason": f"Moderate calibration drift: {avg_error:.3f}"
            }
        
        return {
            "suggestion": "maintain",
            "urgency": "low",
            "reason": f"Well calibrated: {avg_error:.3f}"
        }