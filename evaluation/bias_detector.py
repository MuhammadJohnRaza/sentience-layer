import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

class BiasType(Enum):
    DEMOGRAPHIC = "demographic"
    CONFIRMATION = "confirmation"
    RECENCY = "recency"
    AVAILABILITY = "availability"
    ANCHORING = "anchoring"
    SELECTION = "selection"
    ALGORITHMIC = "algorithmic"
    UNKNOWN = "unknown"

@dataclass
class BiasReport:
    analysis_id: str
    bias_detected: bool
    bias_types: List[BiasType] = field(default_factory=list)
    severity_score: float = 0.0
    affected_dimensions: List[str] = field(default_factory=list)
    mitigation_suggestions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

class BiasDetector:
    def __init__(self):
        self._sensitivity: float = 0.7
        self._dimensions: List[str] = [
            "gender", "age", "race", "ethnicity", "religion",
            "socioeconomic", "geographic", "temporal"
        ]

    async def analyze(
        self,
        data: Dict[str, Any],
        decisions: Optional[List[Dict[str, Any]]] = None,
        model_outputs: Optional[List[str]] = None
    ) -> BiasReport:
        detected_types: List[BiasType] = []
        affected: List[str] = []
        mitigations: List[str] = []
        
        demographic_check = await self._check_demographic_bias(data, decisions)
        if demographic_check["detected"]:
            detected_types.append(BiasType.DEMOGRAPHIC)
            affected.extend(demographic_check["dimensions"])
            mitigations.extend(demographic_check["mitigations"])
        
        confirmation_check = await self._check_confirmation_bias(data, model_outputs)
        if confirmation_check["detected"]:
            detected_types.append(BiasType.CONFIRMATION)
            affected.extend(confirmation_check["dimensions"])
            mitigations.extend(confirmation_check["mitigations"])
        
        recency_check = await self._check_recency_bias(data)
        if recency_check["detected"]:
            detected_types.append(BiasType.RECENCY)
            affected.extend(recency_check["dimensions"])
            mitigations.extend(recency_check["mitigations"])
        
        algorithmic_check = await self._check_algorithmic_bias(model_outputs)
        if algorithmic_check["detected"]:
            detected_types.append(BiasType.ALGORITHMIC)
            affected.extend(algorithmic_check["dimensions"])
            mitigations.extend(algorithmic_check["mitigations"])
        
        severity = self._calculate_severity(detected_types, affected)
        confidence = self._calculate_confidence(detected_types)
        
        return BiasReport(
            analysis_id=f"bias_{hash(str(data))}",
            bias_detected=len(detected_types) > 0,
            bias_types=list(set(detected_types)),
            severity_score=severity,
            affected_dimensions=list(set(affected)),
            mitigation_suggestions=list(set(mitigations)),
            confidence=confidence
        )

    async def _check_demographic_bias(
        self,
        data: Dict[str, Any],
        decisions: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        if not decisions:
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        groups: Dict[str, Dict[str, int]] = {}
        
        for decision in decisions:
            group = decision.get("demographic_group", "unknown")
            outcome = decision.get("outcome", "neutral")
            
            if group not in groups:
                groups[group] = {"positive": 0, "negative": 0, "total": 0}
            
            groups[group]["total"] += 1
            if outcome in ["approved", "success", "positive"]:
                groups[group]["positive"] += 1
            else:
                groups[group]["negative"] += 1
        
        if len(groups) < 2:
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        rates = {
            g: counts["positive"] / counts["total"] if counts["total"] > 0 else 0
            for g, counts in groups.items()
        }
        
        max_rate = max(rates.values())
        min_rate = min(rates.values())
        
        if max_rate - min_rate > 0.2:
            return {
                "detected": True,
                "dimensions": ["demographic"],
                "mitigations": [
                    "Review decision criteria for demographic neutrality",
                    "Apply fairness constraints",
                    "Rebalance training data"
                ]
            }
        
        return {"detected": False, "dimensions": [], "mitigations": []}

    async def _check_confirmation_bias(
        self,
        data: Dict[str, Any],
        model_outputs: Optional[List[str]]
    ) -> Dict[str, Any]:
        if not model_outputs:
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        hypotheses = data.get("hypotheses", [])
        if not hypotheses:
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        confirming = 0
        total = len(model_outputs)
        
        for output in model_outputs:
            for hypothesis in hypotheses:
                if hypothesis.lower() in output.lower():
                    confirming += 1
                    break
        
        ratio = confirming / total if total > 0 else 0
        
        if ratio > 0.8:
            return {
                "detected": True,
                "dimensions": ["hypothesis_confirmation"],
                "mitigations": [
                    "Actively seek disconfirming evidence",
                    "Include devil's advocate reasoning",
                    "Apply red team testing"
                ]
            }
        
        return {"detected": False, "dimensions": [], "mitigations": []}

    async def _check_recency_bias(self, data: Dict[str, Any]) -> Dict[str, Any]:
        timestamps = data.get("timestamps", [])
        weights = data.get("weights", [])
        
        if not timestamps or not weights or len(timestamps) != len(weights):
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        sorted_pairs = sorted(zip(timestamps, weights))
        recent_weight = sum(w for _, w in sorted_pairs[-3:])
        total_weight = sum(weights)
        
        recency_ratio = recent_weight / total_weight if total_weight > 0 else 0
        
        if recency_ratio > 0.6:
            return {
                "detected": True,
                "dimensions": ["temporal"],
                "mitigations": [
                    "Apply time-decay weighting",
                    "Include historical context",
                    "Use rolling averages"
                ]
            }
        
        return {"detected": False, "dimensions": [], "mitigations": []}

    async def _check_algorithmic_bias(
        self,
        model_outputs: Optional[List[str]]
    ) -> Dict[str, Any]:
        if not model_outputs:
            return {"detected": False, "dimensions": [], "mitigations": []}
        
        # Check for repetitive patterns indicating model bias
        from collections import Counter
        first_words = [out.split()[0].lower() if out else "" for out in model_outputs]
        word_counts = Counter(first_words)
        
        most_common = word_counts.most_common(1)[0][1] if word_counts else 0
        diversity = len(word_counts) / len(model_outputs) if model_outputs else 1
        
        if most_common > len(model_outputs) * 0.4 or diversity < 0.3:
            return {
                "detected": True,
                "dimensions": ["output_diversity"],
                "mitigations": [
                    "Increase temperature for generation",
                    "Use diverse prompting",
                    "Apply output filtering"
                ]
            }
        
        return {"detected": False, "dimensions": [], "mitigations": []}

    def _calculate_severity(self, bias_types: List[BiasType], affected: List[str]) -> float:
        base_severity = len(bias_types) * 0.15
        dimension_severity = len(affected) * 0.05
        
        if BiasType.DEMOGRAPHIC in bias_types:
            base_severity += 0.3
        
        return min(1.0, base_severity + dimension_severity)

    def _calculate_confidence(self, bias_types: List[BiasType]) -> float:
        return min(1.0, 0.5 + len(bias_types) * 0.1)

    async def batch_analyze(
        self,
        items: List[Dict[str, Any]]
    ) -> List[BiasReport]:
        tasks = [self.analyze(item) for item in items]
        return await asyncio.gather(*tasks)

    async def get_mitigation_guide(self, bias_type: BiasType) -> Dict[str, Any]:
        guides = {
            BiasType.DEMOGRAPHIC: {
                "description": "Unequal treatment across demographic groups",
                "techniques": ["Demographic parity", "Equalized odds", "Calibration"],
                "tools": ["Fairness indicators", "Bias bounties"]
            },
            BiasType.CONFIRMATION: {
                "description": "Seeking evidence that confirms pre-existing beliefs",
                "techniques": ["Red teaming", "Adversarial testing", "Blind evaluation"],
                "tools": ["Devil's advocate agent", "Contrarian prompting"]
            },
            BiasType.RECENCY: {
                "description": "Overweighting recent events",
                "techniques": ["Time decay", "Historical weighting", "Long-term evaluation"],
                "tools": ["Temporal calibration", "Lookback windows"]
            },
            BiasType.ALGORITHMIC: {
                "description": "Systematic errors from model architecture or training",
                "techniques": ["Diverse training data", "Regularization", "Ensemble methods"],
                "tools": ["Model cards", "Evaluation suites"]
            }
        }
        
        return guides.get(bias_type, {
            "description": "Unknown bias type",
            "techniques": [],
            "tools": []
        })