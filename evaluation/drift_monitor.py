import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from statistics import mean, stdev
import math

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class DriftReport:
    monitor_id: str
    drift_detected: bool
    drift_type: str
    severity: str
    metric_name: str
    baseline_value: float
    current_value: float
    deviation: float
    p_value: Optional[float] = None
    affected_features: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

class DriftMonitor:
    def __init__(self):
        self._baselines: Dict[str, Dict[str, Any]] = {}
        self._history: Dict[str, List[Dict[str, Any]]] = {}
        self._thresholds = {
            "data_drift": 0.1,
            "concept_drift": 0.15,
            "performance_drift": 0.2,
            "prediction_drift": 0.1
        }
        self._window_size: int = 100

    async def establish_baseline(
        self,
        metric_name: str,
        values: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not values:
            raise ValueError("Cannot establish baseline with empty values")
        
        baseline = {
            "mean": mean(values),
            "std": stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
            "count": len(values),
            "metadata": metadata or {},
            "established_at": datetime.utcnow()
        }
        
        self._baselines[metric_name] = baseline
        self._history[metric_name] = []
        
        logger.info(f"Baseline established for {metric_name}: mean={baseline['mean']:.4f}")
        return baseline

    async def check_drift(
        self,
        metric_name: str,
        current_values: List[float],
        drift_type: str = "data_drift"
    ) -> DriftReport:
        baseline = self._baselines.get(metric_name)
        if not baseline:
            raise ValueError(f"No baseline established for {metric_name}")
        
        if not current_values:
            return DriftReport(
                monitor_id=f"drift_{metric_name}",
                drift_detected=False,
                drift_type=drift_type,
                severity="unknown",
                metric_name=metric_name,
                baseline_value=baseline["mean"],
                current_value=0.0,
                deviation=0.0
            )
        
        current_mean = mean(current_values)
        current_std = stdev(current_values) if len(current_values) > 1 else 0.0
        
        baseline_mean = baseline["mean"]
        baseline_std = baseline["std"] if baseline["std"] > 0 else 1.0
        
        deviation = abs(current_mean - baseline_mean) / baseline_std if baseline_std > 0 else 0.0
        
        threshold = self._thresholds.get(drift_type, 0.1)
        drift_detected = deviation > threshold
        
        severity = self._classify_severity(deviation, threshold)
        
        p_value = self._compute_p_value(
            baseline_mean,
            baseline_std,
            baseline["count"],
            current_mean,
            current_std,
            len(current_values)
        )
        
        affected = []
        if drift_detected and drift_type == "data_drift":
            affected = await self._identify_affected_features(current_values, baseline)
        
        self._history[metric_name].append({
            "current_mean": current_mean,
            "deviation": deviation,
            "drift_detected": drift_detected,
            "timestamp": datetime.utcnow()
        })
        
        if len(self._history[metric_name]) > self._window_size:
            self._history[metric_name] = self._history[metric_name][-self._window_size:]
        
        return DriftReport(
            monitor_id=f"drift_{metric_name}_{datetime.utcnow().timestamp()}",
            drift_detected=drift_detected,
            drift_type=drift_type,
            severity=severity,
            metric_name=metric_name,
            baseline_value=baseline_mean,
            current_value=current_mean,
            deviation=deviation,
            p_value=p_value,
            affected_features=affected,
            recommended_action=self._suggest_action(drift_type, severity) if drift_detected else None
        )

    def _classify_severity(self, deviation: float, threshold: float) -> str:
        ratio = deviation / threshold if threshold > 0 else 0
        
        if ratio < 1.0:
            return "none"
        elif ratio < 1.5:
            return "low"
        elif ratio < 2.5:
            return "medium"
        elif ratio < 4.0:
            return "high"
        else:
            return "critical"

    def _compute_p_value(
        self,
        mean1: float,
        std1: float,
        n1: int,
        mean2: float,
        std2: float,
        n2: int
    ) -> Optional[float]:
        try:
            pooled_std = math.sqrt(
                ((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2)
            ) if n1 + n2 > 2 else 0
            
            if pooled_std == 0:
                return None
            
            se = pooled_std * math.sqrt(1/n1 + 1/n2)
            t_stat = abs(mean1 - mean2) / se if se > 0 else 0
            
            # Simplified p-value approximation
            return max(0.0, min(1.0, 1.0 - min(t_stat / 3.0, 1.0)))
        except Exception:
            return None

    async def _identify_affected_features(
        self,
        current_values: List[float],
        baseline: Dict[str, Any]
    ) -> List[str]:
        metadata = baseline.get("metadata", {})
        features = metadata.get("features", [])
        
        if not features:
            return ["unknown"]
        
        # Simplified feature impact analysis
        return features[:3]

    def _suggest_action(self, drift_type: str, severity: str) -> str:
        actions = {
            "data_drift": {
                "low": "Monitor and collect more samples",
                "medium": "Retrain model with recent data",
                "high": "Immediate retraining required",
                "critical": "Halt predictions, full investigation"
            },
            "concept_drift": {
                "low": "Review feature importance",
                "medium": "Update feature engineering",
                "high": "Redesign model architecture",
                "critical": "Full system redesign"
            },
            "performance_drift": {
                "low": "Adjust thresholds",
                "medium": "Hyperparameter tuning",
                "high": "Model replacement",
                "critical": "Emergency rollback"
            }
        }
        
        type_actions = actions.get(drift_type, {})
        return type_actions.get(severity, "Investigate and monitor")

    async def get_trend(
        self,
        metric_name: str,
        hours: int = 24
    ) -> Dict[str, Any]:
        history = self._history.get(metric_name, [])
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent = [
            h for h in history
            if h["timestamp"] > cutoff
        ]
        
        if not recent:
            return {"trend": "insufficient_data", "points": 0}
        
        deviations = [h["deviation"] for h in recent]
        drift_events = sum(1 for h in recent if h["drift_detected"])
        
        return {
            "trend": "increasing" if deviations[-1] > deviations[0] else "stable",
            "points": len(recent),
            "avg_deviation": mean(deviations),
            "max_deviation": max(deviations),
            "drift_events": drift_events,
            "drift_rate": drift_events / len(recent) if recent else 0
        }

    async def get_all_monitors(self) -> List[Dict[str, Any]]:
        return [
            {
                "metric_name": name,
                "baseline_established": b["established_at"].isoformat(),
                "baseline_mean": b["mean"],
                "current_status": "active",
                "history_points": len(self._history.get(name, []))
            }
            for name, b in self._baselines.items()
        ]

    async def update_threshold(
        self,
        drift_type: str,
        new_threshold: float
    ) -> bool:
        if drift_type not in self._thresholds:
            return False
        
        self._thresholds[drift_type] = new_threshold
        logger.info(f"Threshold updated for {drift_type}: {new_threshold}")
        return True