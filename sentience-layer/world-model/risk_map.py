import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

class RiskLevel(Enum):
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RiskEvent:
    event_id: str
    description: str
    probability: float
    impact: float
    category: str
    mitigation: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    cascading_effects: List[str] = field(default_factory=list)

class RiskMap:
    def __init__(self):
        self.risks: Dict[str, RiskEvent] = {}
        self.correlations: Dict[Tuple[str, str], float] = {}
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        
    def add_risk(
        self,
        event_id: str,
        description: str,
        probability: float,
        impact: float,
        category: str,
        mitigation: List[str] = None,
        triggers: List[str] = None,
        cascading_effects: List[str] = None
    ):
        risk = RiskEvent(
            event_id=event_id,
            description=description,
            probability=min(1.0, max(0.0, probability)),
            impact=min(1.0, max(0.0, impact)),
            category=category,
            mitigation=mitigation or [],
            triggers=triggers or [],
            cascading_effects=cascading_effects or []
        )
        self.risks[event_id] = risk
        
    def add_correlation(self, risk_a: str, risk_b: str, correlation: float):
        if risk_a not in self.risks or risk_b not in self.risks:
            raise ValueError("Both risks must exist")
            
        key = tuple(sorted([risk_a, risk_b]))
        self.correlations[key] = min(1.0, max(-1.0, correlation))
        
    def get_risk_level(self, risk_id: str) -> RiskLevel:
        if risk_id not in self.risks:
            return RiskLevel.NEGLIGIBLE
            
        risk = self.risks[risk_id]
        score = risk.probability * risk.impact
        
        if score < 0.05:
            return RiskLevel.NEGLIGIBLE
        elif score < 0.15:
            return RiskLevel.LOW
        elif score < 0.35:
            return RiskLevel.MEDIUM
        elif score < 0.6:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
            
    def get_exposure(self, category: Optional[str] = None) -> float:
        risks = self.risks.values()
        if category:
            risks = [r for r in risks if r.category == category]
            
        if not risks:
            return 0.0
            
        total_exposure = sum(r.probability * r.impact for r in risks)
        
        for (a, b), corr in self.correlations.items():
            if a in self.risks and b in self.risks:
                risk_a = self.risks[a]
                risk_b = self.risks[b]
                if category is None or (risk_a.category == category and risk_b.category == category):
                    combined = risk_a.probability * risk_b.probability * corr
                    total_exposure += combined * 0.5
                    
        return total_exposure
        
    def simulate_scenario(
        self,
        scenario_name: str,
        triggered_risks: List[str],
        iterations: int = 1000
    ) -> Dict[str, Any]:
        results = {
            "total_losses": [],
            "affected_risks": [],
            "cascade_depths": []
        }
        
        for _ in range(iterations):
            active = set(triggered_risks)
            cascade = set()
            depth = 0
            
            queue = list(triggered_risks)
            while queue and depth < 10:
                next_queue = []
                for risk_id in queue:
                    if risk_id not in self.risks:
                        continue
                        
                    risk = self.risks[risk_id]
                    
                    for effect in risk.cascading_effects:
                        if effect in self.risks and effect not in active:
                            if random.random() < self.risks[effect].probability:
                                active.add(effect)
                                cascade.add(effect)
                                next_queue.append(effect)
                                
                queue = next_queue
                if queue:
                    depth += 1
                    
            total_loss = sum(
                self.risks[r].impact
                for r in active
                if r in self.risks
            )
            
            results["total_losses"].append(total_loss)
            results["affected_risks"].append(len(active))
            results["cascade_depths"].append(depth)
            
        self.scenarios[scenario_name] = {
            "triggered": triggered_risks,
            "iterations": iterations,
            "results": results
        }
        
        return {
            "expected_loss": sum(results["total_losses"]) / iterations,
            "max_loss": max(results["total_losses"]),
            "avg_affected": sum(results["affected_risks"]) / iterations,
            "avg_cascade_depth": sum(results["cascade_depths"]) / iterations,
            "p95_loss": sorted(results["total_losses"])[int(iterations * 0.95)]
        }
        
    def get_mitigation_priority(self) -> List[Dict[str, Any]]:
        priorities = []
        
        for risk_id, risk in self.risks.items():
            level = self.get_risk_level(risk_id)
            reduction_potential = len(risk.mitigation) * 0.1
            
            priorities.append({
                "risk_id": risk_id,
                "current_level": level.value,
                "exposure": risk.probability * risk.impact,
                "mitigation_count": len(risk.mitigation),
                "reduction_potential": reduction_potential,
                "priority_score": risk.probability * risk.impact * (1 + reduction_potential)
            })
            
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        return priorities
        
    def get_heat_map(self) -> Dict[str, List[Dict[str, Any]]]:
        categories = {}
        
        for risk_id, risk in self.risks.items():
            if risk.category not in categories:
                categories[risk.category] = []
                
            categories[risk.category].append({
                "risk_id": risk_id,
                "probability": risk.probability,
                "impact": risk.impact,
                "level": self.get_risk_level(risk_id).value
            })
            
        return categories
        
    def find_correlated_clusters(self, threshold: float = 0.5) -> List[List[str]]:
        clusters = []
        visited = set()
        
        for risk_id in self.risks:
            if risk_id in visited:
                continue
                
            cluster = self._build_cluster(risk_id, threshold, set())
            if len(cluster) > 1:
                clusters.append(list(cluster))
                visited.update(cluster)
                
        return clusters
        
    def _build_cluster(
        self,
        risk_id: str,
        threshold: float,
        current: set
    ) -> set:
        if risk_id in current:
            return current
            
        current.add(risk_id)
        
        for (a, b), corr in self.correlations.items():
            if abs(corr) >= threshold:
                if a == risk_id and b not in current:
                    self._build_cluster(b, threshold, current)
                elif b == risk_id and a not in current:
                    self._build_cluster(a, threshold, current)
                    
        return current
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "risks": {
                r.event_id: {
                    "description": r.description,
                    "probability": r.probability,
                    "impact": r.impact,
                    "category": r.category,
                    "mitigation": r.mitigation,
                    "triggers": r.triggers,
                    "cascading_effects": r.cascading_effects
                }
                for r in self.risks.values()
            },
            "correlations": {
                f"{a}-{b}": corr
                for (a, b), corr in self.correlations.items()
            },
            "exposure": self.get_exposure()
        }
