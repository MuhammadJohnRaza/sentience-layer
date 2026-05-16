import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class ConfidenceEstimate:
    value: float
    source: str
    evidence_count: int
    recency: float
    agreement: float

class ConfidenceEngine:
    def __init__(self):
        self.estimates: Dict[str, List[ConfidenceEstimate]] = defaultdict(list)
        self.calibration_history: List[Dict[str, Any]] = []
        self.source_reliability: Dict[str, float] = {}
        
    def add_estimate(
        self,
        claim_id: str,
        value: float,
        source: str,
        evidence_count: int = 1,
        timestamp: Optional[float] = None
    ):
        import time
        if timestamp is None:
            timestamp = time.time()
            
        estimate = ConfidenceEstimate(
            value=min(1.0, max(0.0, value)),
            source=source,
            evidence_count=evidence_count,
            recency=timestamp,
            agreement=0.5
        )
        
        self.estimates[claim_id].append(estimate)
        self._update_agreement(claim_id)
        
    def get_confidence(self, claim_id: str) -> Dict[str, Any]:
        if claim_id not in self.estimates or not self.estimates[claim_id]:
            return {
                "aggregate": 0.5,
                "method": "default",
                "estimates_count": 0
            }
            
        estimates = self.estimates[claim_id]
        
        weighted = self._weighted_aggregate(estimates)
        bayesian = self._bayesian_aggregate(estimates)
        consensus = self._consensus_aggregate(estimates)
        
        return {
            "aggregate": (weighted + bayesian + consensus) / 3,
            "weighted": weighted,
            "bayesian": bayesian,
            "consensus": consensus,
            "estimates_count": len(estimates),
            "source_diversity": len(set(e.source for e in estimates)),
            "agreement_score": sum(e.agreement for e in estimates) / len(estimates)
        }
        
    def _weighted_aggregate(self, estimates: List[ConfidenceEstimate]) -> float:
        if not estimates:
            return 0.5
            
        total_weight = 0
        weighted_sum = 0
        
        import time
        now = time.time()
        
        for est in estimates:
            source_rel = self.source_reliability.get(est.source, 0.5)
            recency_weight = math.exp(-(now - est.recency) / 86400)
            evidence_weight = min(est.evidence_count / 10, 1.0)
            
            weight = source_rel * recency_weight * evidence_weight
            weighted_sum += est.value * weight
            total_weight += weight
            
        return weighted_sum / total_weight if total_weight > 0 else 0.5
        
    def _bayesian_aggregate(self, estimates: List[ConfidenceEstimate]) -> float:
        if not estimates:
            return 0.5
            
        prior = 0.5
        prior_strength = 1.0
        
        for est in estimates:
            source_rel = self.source_reliability.get(est.source, 0.5)
            likelihood = est.value if est.value > 0.5 else 1 - est.value
            
            posterior = (prior * prior_strength + likelihood * source_rel) / (
                prior_strength + source_rel
            )
            prior = posterior
            prior_strength += source_rel
            
        return prior
        
    def _consensus_aggregate(self, estimates: List[ConfidenceEstimate]) -> float:
        if not estimates:
            return 0.5
            
        values = [e.value for e in estimates]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        
        if variance < 0.01:
            return mean
            
        std = math.sqrt(variance)
        filtered = [v for v in values if abs(v - mean) < 2 * std]
        
        if not filtered:
            return mean
            
        return sum(filtered) / len(filtered)
        
    def _update_agreement(self, claim_id: str):
        estimates = self.estimates[claim_id]
        if len(estimates) < 2:
            return
            
        values = [e.value for e in estimates]
        mean = sum(values) / len(values)
        
        for est in estimates:
            deviation = abs(est.value - mean)
            est.agreement = max(0, 1 - deviation)
            
    def update_source_reliability(
        self,
        source: str,
        actual_outcome: bool,
        predicted_confidence: float
    ):
        if source not in self.source_reliability:
            self.source_reliability[source] = 0.5
            
        current = self.source_reliability[source]
        error = abs(float(actual_outcome) - predicted_confidence)
        
        adjustment = 0.1 * (1 - error) if actual_outcome else -0.1 * error
        self.source_reliability[source] = min(1.0, max(0.1, current + adjustment))
        
        self.calibration_history.append({
            "source": source,
            "outcome": actual_outcome,
            "predicted": predicted_confidence,
            "error": error,
            "new_reliability": self.source_reliability[source]
        })
        
    def get_calibration_report(self, source: Optional[str] = None) -> Dict[str, Any]:
        if source:
            history = [h for h in self.calibration_history if h["source"] == source]
            if not history:
                return {"status": "no_data"}
                
            return {
                "source": source,
                "current_reliability": self.source_reliability.get(source, 0.5),
                "total_predictions": len(history),
                "avg_error": sum(h["error"] for h in history) / len(history),
                "accuracy_trend": [
                    h["error"] for h in history[-20:]
                ]
            }
            
        return {
            "sources": {
                src: {
                    "reliability": rel,
                    "predictions": sum(
                        1 for h in self.calibration_history
                        if h["source"] == src
                    )
                }
                for src, rel in self.source_reliability.items()
            },
            "overall_calibration": sum(
                h["error"] for h in self.calibration_history
            ) / max(len(self.calibration_history), 1)
        }
        
    def find_disagreements(self, threshold: float = 0.3) -> List[Dict[str, Any]]:
        disagreements = []
        
        for claim_id, estimates in self.estimates.items():
            if len(estimates) < 2:
                continue
                
            values = [e.value for e in estimates]
            range_val = max(values) - min(values)
            
            if range_val > threshold:
                disagreements.append({
                    "claim_id": claim_id,
                    "range": range_val,
                    "estimates": [
                        {
                            "source": e.source,
                            "value": e.value,
                            "evidence": e.evidence_count
                        }
                        for e in estimates
                    ],
                    "recommendation": "investigate_sources" if range_val > 0.5 else "monitor"
                })
                
        return disagreements
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "claims_tracked": len(self.estimates),
            "sources_calibrated": len(self.source_reliability),
            "overall_confidence": sum(
                self.get_confidence(c)["aggregate"]
                for c in self.estimates
            ) / max(len(self.estimates), 1)
        }