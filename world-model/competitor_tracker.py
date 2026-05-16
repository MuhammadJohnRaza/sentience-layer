"""Competitor tracking and analysis for market intelligence."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CompetitorAction(Enum):
    PRODUCT_LAUNCH = "product_launch"
    PRICING_CHANGE = "pricing_change"
    MARKETING_CAMPAIGN = "marketing_campaign"
    PARTNERSHIP = "partnership"
    ACQUISITION = "acquisition"
    HIRING = "hiring"
    TECHNOLOGY_SHIFT = "technology_shift"


@dataclass
class CompetitorProfile:
    name: str
    market_segment: str
    market_share: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recent_actions: List[Dict[str, Any]] = field(default_factory=list)
    threat_level: str = "medium"
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MarketSignal:
    source: str
    signal_type: CompetitorAction
    confidence: float
    impact_score: float
    description: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CompetitorTracker:
    """Tracks competitor activities and market signals."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.competitors: Dict[str, CompetitorProfile] = {}
        self.signals: List[MarketSignal] = []
        self.alert_thresholds = self.config.get("alert_thresholds", {
            "market_share_change": 0.05,
            "threat_level": "high"
        })

    def add_competitor(self, profile: CompetitorProfile) -> None:
        """Add or update a competitor profile."""
        self.competitors[profile.name] = profile

    def get_competitor(self, name: str) -> Optional[CompetitorProfile]:
        """Get a competitor profile by name."""
        return self.competitors.get(name)

    def add_signal(self, signal: MarketSignal) -> None:
        """Add a market signal and update competitor profiles."""
        self.signals.append(signal)
        self._process_signal(signal)

    def _process_signal(self, signal: MarketSignal) -> None:
        """Process a signal and update relevant competitor profiles."""
        # Update competitor profiles based on signal
        if signal.source in self.competitors:
            competitor = self.competitors[signal.source]
            competitor.recent_actions.append({
                "type": signal.signal_type.value,
                "description": signal.description,
                "timestamp": signal.timestamp.isoformat(),
                "impact": signal.impact_score
            })
            competitor.last_updated = datetime.utcnow()
            self._update_threat_level(competitor)

    def _update_threat_level(self, competitor: CompetitorProfile) -> None:
        """Update threat level based on recent activities."""
        recent_actions = len(competitor.recent_actions)
        if recent_actions > 10:
            competitor.threat_level = "high"
        elif recent_actions > 5:
            competitor.threat_level = "medium"
        else:
            competitor.threat_level = "low"

    def get_market_overview(self) -> Dict[str, Any]:
        """Get an overview of the competitive landscape."""
        return {
            "total_competitors": len(self.competitors),
            "high_threat_count": sum(1 for c in self.competitors.values() if c.threat_level == "high"),
            "recent_signals": len([s for s in self.signals if (datetime.utcnow() - s.timestamp).days < 7]),
            "top_competitors": sorted(
                self.competitors.values(),
                key=lambda c: c.market_share,
                reverse=True
            )[:5]
        }

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get alerts for significant competitor activities."""
        alerts = []
        for competitor in self.competitors.values():
            if competitor.threat_level == "high":
                alerts.append({
                    "type": "high_threat",
                    "competitor": competitor.name,
                    "market_share": competitor.market_share,
                    "recent_actions": len(competitor.recent_actions)
                })
        return alerts