"""Risk mapping and assessment for strategic planning."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    COMPLIANCE = "compliance"
    REPUTATIONAL = "reputational"
    TECHNOLOGICAL = "technological"


@dataclass
class Risk:
    id: str
    name: str
    description: str = ""
    category: RiskCategory = RiskCategory.OPERATIONAL
    probability: float = 0.5  # 0-1
    impact: float = 0.5  # 0-1
    severity: float = 0.0  # calculated
    risk_level: RiskLevel = RiskLevel.MEDIUM
    mitigation_status: str = "identified"  # identified, assessed, mitigated, monitored
    owner: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MitigationPlan:
    risk_id: str
    actions: List[str] = field(default_factory=list)
    timeline: Optional[str] = None
    estimated_cost: float = 0.0
    effectiveness: float = 0.0
    status: str = "planned"


class RiskMap:
    """Risk mapping and assessment system."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.risks: Dict[str, Risk] = {}
        self.mitigation_plans: Dict[str, MitigationPlan] = {}
        self.thresholds = self.config.get("thresholds", {
            "low": 0.25,
            "medium": 0.5,
            "high": 0.75,
            "critical": 0.9
        })

    def add_risk(
        self,
        name: str,
        category: RiskCategory,
        probability: float,
        impact: float,
        description: str = "",
        owner: Optional[str] = None
    ) -> Risk:
        """Add a new risk to the map."""
        risk_id = f"risk_{len(self.risks)}_{name.lower().replace(' ', '_')}"
        severity = self._calculate_severity(probability, impact)
        risk_level = self._determine_risk_level(severity)

        risk = Risk(
            id=risk_id,
            name=name,
            description=description,
            category=category,
            probability=probability,
            impact=impact,
            severity=severity,
            risk_level=risk_level,
            owner=owner
        )
        self.risks[risk_id] = risk
        return risk

    def update_risk(
        self,
        risk_id: str,
        probability: Optional[float] = None,
        impact: Optional[float] = None,
        mitigation_status: Optional[str] = None
    ) -> Optional[Risk]:
        """Update a risk's parameters."""
        risk = self.risks.get(risk_id)
        if not risk:
            return None

        if probability is not None:
            risk.probability = probability
        if impact is not None:
            risk.impact = impact

        # Recalculate severity and level
        risk.severity = self._calculate_severity(risk.probability, risk.impact)
        risk.risk_level = self._determine_risk_level(risk.severity)
        risk.updated_at = datetime.utcnow()

        if mitigation_status:
            risk.mitigation_status = mitigation_status

        return risk

    def add_mitigation_plan(
        self,
        risk_id: str,
        actions: List[str],
        timeline: Optional[str] = None,
        estimated_cost: float = 0.0
    ) -> Optional[MitigationPlan]:
        """Add a mitigation plan for a risk."""
        if risk_id not in self.risks:
            return None

        plan = MitigationPlan(
            risk_id=risk_id,
            actions=actions,
            timeline=timeline,
            estimated_cost=estimated_cost
        )
        self.mitigation_plans[risk_id] = plan
        return plan

    def get_risk_heatmap(self) -> Dict[str, List[Risk]]:
        """Get risks organized by risk level (heatmap)."""
        heatmap = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        for risk in self.risks.values():
            heatmap[risk.risk_level.value].append(risk)
        return heatmap

    def get_risks_by_category(self) -> Dict[str, List[Risk]]:
        """Get risks organized by category."""
        by_category = {}
        for risk in self.risks.values():
            cat = risk.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(risk)
        return by_category

    def get_top_risks(self, n: int = 10) -> List[Risk]:
        """Get the top N risks by severity."""
        return sorted(
            self.risks.values(),
            key=lambda r: r.severity,
            reverse=True
        )[:n]

    def get_total_exposure(self) -> Dict[str, float]:
        """Calculate total risk exposure."""
        total_severity = sum(r.severity for r in self.risks.values())
        by_category = {}
        for risk in self.risks.values():
            cat = risk.category.value
            by_category[cat] = by_category.get(cat, 0) + risk.severity

        return {
            "total_severity": total_severity,
            "average_severity": total_severity / len(self.risks) if self.risks else 0,
            "by_category": by_category,
            "high_risk_count": len([r for r in self.risks.values() if r.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        }

    def _calculate_severity(self, probability: float, impact: float) -> float:
        """Calculate risk severity from probability and impact."""
        # Using a non-linear formula that emphasizes high impact events
        return math.sqrt(probability * impact)

    def _determine_risk_level(self, severity: float) -> RiskLevel:
        """Determine risk level from severity score."""
        if severity >= self.thresholds["critical"]:
            return RiskLevel.CRITICAL
        elif severity >= self.thresholds["high"]:
            return RiskLevel.HIGH
        elif severity >= self.thresholds["medium"]:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the risk map."""
        return {
            "total_risks": len(self.risks),
            "exposure": self.get_total_exposure(),
            "mitigation_plans": len(self.mitigation_plans),
            "heatmap": {level: len(risks) for level, risks in self.get_risk_heatmap().items()}
        }