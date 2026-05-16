"""
Premonition Engine Service
Predicts future events and anomalies using weak signal detection.
Uses Antigravity for enterprise-scale early warning systems.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class Premonition:
    id: str
    event_type: str
    description: str
    predicted_time: datetime
    confidence: float
    lead_time: timedelta
    severity: str
    indicators: List[Dict[str, Any]]
    recommended_actions: List[str]
    status: str = "active"  # active, confirmed, false_positive, prevented


class PremonitionEngineService:
    """
    Weak signal amplification and early warning system.
    Integrates with Antigravity for predictive analytics.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._premonitions: List[Premonition] = []
        self._confirmed: List[str] = []
        self._false_positives: List[str] = []
        logger.info("PremonitionEngineService initialized")

    async def scan(
        self,
        signals: List[Dict[str, Any]],
        horizon: timedelta = timedelta(days=7),
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Premonition]:
        """
        Agentic premonition scanning:
        1. Signal preprocessing → 2. Anomaly detection → 3. Pattern matching →
        4. Causal projection → 5. Confidence calibration → 6. Action linking
        """
        context = context or {}
        
        try:
            # Step 1: Preprocess signals
            clean_signals = self._preprocess_signals(signals)
            
            # Step 2: Detect anomalies
            anomalies = await self._detect_anomalies(clean_signals)
            
            # Step 3: Match to historical patterns
            matched = await self._match_patterns(anomalies, context)
            
            # Step 4: Project forward causally
            projected = await self._project_forward(matched, horizon, context)
            
            # Step 5: Calibrate confidence
            calibrated = self._calibrate_confidence(projected)
            
            # Step 6: Link actions
            actionable = await self._link_actions(calibrated)
            
            self._premonitions.extend(actionable)
            logger.info(f"Generated {len(actionable)} premonitions")
            return actionable

        except Exception as e:
            logger.error(f"Premonition scan failed: {e}")
            raise PremonitionEngineError(f"Scan failed: {e}") from e

    def _preprocess_signals(
        self, signals: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Clean and normalize signal data."""
        clean = []
        for s in signals:
            clean.append({
                "timestamp": s.get("timestamp", datetime.utcnow().isoformat()),
                "value": s.get("value", 0),
                "source": s.get("source", "unknown"),
                "type": s.get("type", "metric")
            })
        return clean

    async def _detect_anomalies(
        self, signals: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Detect anomalous signals."""
        try:
            anomalies = await self.ag.analytics.detect_anomalies(signals)
            return anomalies
        except Exception:
            # Simple threshold-based fallback
            mean = sum(s["value"] for s in signals) / max(len(signals), 1)
            std = (sum((s["value"] - mean) ** 2 for s in signals) / max(len(signals), 1)) ** 0.5
            return [
                s for s in signals
                if abs(s["value"] - mean) > 2 * std
            ]

    async def _match_patterns(
        self, anomalies: List[Dict], context: Dict
    ) -> List[Dict[str, Any]]:
        """Match anomalies to known precursor patterns."""
        matched = []
        for anomaly in anomalies:
            try:
                patterns = await self.ag.patterns.find_precursors(
                    anomaly,
                    context.get("domain", "general")
                )
                matched.append({
                    "anomaly": anomaly,
                    "precursor_patterns": patterns
                })
            except Exception:
                matched.append({
                    "anomaly": anomaly,
                    "precursor_patterns": []
                })
        return matched

    async def _project_forward(
        self,
        matched: List[Dict],
        horizon: timedelta,
        context: Dict
    ) -> List[Premonition]:
        """Project anomalies forward to predicted events."""
        premonitions = []
        for m in matched:
            for pattern in m.get("precursor_patterns", []):
                try:
                    projection = await self.ag.predict.project(
                        pattern=pattern,
                        current_anomaly=m["anomaly"],
                        horizon=horizon
                    )
                    
                    premonitions.append(Premonition(
                        id=f"prem-{hash(json.dumps(m, default=str)) % 1000000}",
                        event_type=projection.get("event_type", "unknown"),
                        description=projection.get("description", "Event predicted"),
                        predicted_time=datetime.utcnow() + horizon,
                        confidence=projection.get("confidence", 0.5),
                        lead_time=horizon,
                        severity=projection.get("severity", "medium"),
                        indicators=[m["anomaly"]],
                        recommended_actions=projection.get("actions", [])
                    ))
                except Exception:
                    pass
        return premonitions

    def _calibrate_confidence(
        self, premonitions: List[Premonition]
    ) -> List[Premonition]:
        """Calibrate confidence based on historical accuracy."""
        # Adjust based on base rates
        for p in premonitions:
            if p.event_type in self._confirmed:
                p.confidence = min(1.0, p.confidence + 0.1)
            if p.event_type in self._false_positives:
                p.confidence = max(0.0, p.confidence - 0.2)
        return premonitions

    async def _link_actions(
        self, premonitions: List[Premonition]
    ) -> List[Premonition]:
        """Link recommended actions to premonitions."""
        for p in premonitions:
            if not p.recommended_actions:
                if p.severity == "critical":
                    p.recommended_actions = ["Immediate escalation", "Prepare contingency"]
                elif p.severity == "high":
                    p.recommended_actions = ["Increase monitoring", "Alert stakeholders"]
                else:
                    p.recommended_actions = ["Log for review"]
        return premonitions

    async def validate_premonition(
        self,
        premonition_id: str,
        outcome: str,  # confirmed, false_positive, prevented
    ):
        """Update premonition status for calibration."""
        for p in self._premonitions:
            if p.id == premonition_id:
                p.status = outcome
                if outcome == "confirmed":
                    self._confirmed.append(p.event_type)
                elif outcome == "false_positive":
                    self._false_positives.append(p.event_type)
                break


class PremonitionEngineError(Exception):
    pass