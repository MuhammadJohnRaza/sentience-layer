import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from .base_agent import BaseAgent, AgentMessage, AgentResult

@dataclass
class Opportunity:
    opportunity_id: str
    description: str
    category: str
    estimated_value: float
    probability: float
    time_window: float
    required_resources: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    signals: List[Dict[str, Any]] = field(default_factory=list)

class OpportunityAnalystAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "opportunity_analyst",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.opportunities: Dict[str, Opportunity] = {}
        self.signal_history: List[Dict[str, Any]] = []
        self.market_indicators: Dict[str, List[float]] = defaultdict(list)
        self.detection_threshold = config.get("detection_threshold", 0.6)
        self.value_decay_rate = config.get("value_decay_rate", 0.1)
        
    async def initialize(self):
        self.register_skill("scan", self._scan_for_opportunities)
        self.register_skill("evaluate", self._evaluate_opportunity)
        self.register_skill("track", self._track_signals)
        self.register_skill("forecast", self._forecast_timeline)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "scan")
        
        if skill == "scan":
            return await self._scan_for_opportunities(
                message.content,
                message.metadata.get("context", {})
            )
        elif skill == "evaluate":
            return await self._evaluate_opportunity(message.content)
        elif skill == "track":
            return await self._track_signals(message.content)
        elif skill == "forecast":
            return await self._forecast_timeline(message.content)
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _scan_for_opportunities(
        self,
        data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> AgentResult:
        detected = []
        
        market_signals = data.get("market_signals", [])
        internal_metrics = data.get("internal_metrics", {})
        external_events = data.get("external_events", [])
        
        for signal in market_signals:
            opportunity = self._detect_from_signal(signal, "market")
            if opportunity and opportunity.probability > self.detection_threshold:
                detected.append(opportunity)
                
        for metric_name, metric_value in internal_metrics.items():
            opportunity = self._detect_from_metric(metric_name, metric_value)
            if opportunity:
                detected.append(opportunity)
                
        for event in external_events:
            opportunity = self._detect_from_event(event)
            if opportunity:
                detected.append(opportunity)
                
        scored = [
            {
                "opportunity": opp,
                "expected_return": opp.estimated_value * opp.probability,
                "urgency": 1.0 / (1.0 + opp.time_window),
                "score": self._opportunity_score(opp)
            }
            for opp in detected
        ]
        
        scored.sort(key=lambda x: x["score"], reverse=True)
        
        for item in scored:
            self.opportunities[item["opportunity"].opportunity_id] = item["opportunity"]
            
        return AgentResult(
            success=True,
            data={
                "opportunities_detected": len(detected),
                "top_opportunities": [
                    {
                        "id": item["opportunity"].opportunity_id,
                        "description": item["opportunity"].description,
                        "category": item["opportunity"].category,
                        "expected_return": round(item["expected_return"], 2),
                        "score": round(item["score"], 4),
                        "time_window": item["opportunity"].time_window
                    }
                    for item in scored[:5]
                ],
                "categories": self._categorize_opportunities(detected)
            }
        )
        
    async def _evaluate_opportunity(
        self,
        opportunity_id: str
    ) -> AgentResult:
        if opportunity_id not in self.opportunities:
            return AgentResult(
                success=False,
                error=f"Opportunity {opportunity_id} not found"
            )
            
        opp = self.opportunities[opportunity_id]
        
        swot = self._generate_swot(opp)
        risk_adjusted_value = opp.estimated_value * opp.probability * (
            1 - self.value_decay_rate * opp.time_window
        )
        
        competitive_analysis = self._analyze_competitive_position(opp)
        
        return AgentResult(
            success=True,
            data={
                "opportunity_id": opportunity_id,
                "base_value": opp.estimated_value,
                "probability": opp.probability,
                "risk_adjusted_value": round(risk_adjusted_value, 2),
                "swot": swot,
                "competitive_position": competitive_analysis,
                "feasibility": self._assess_feasibility(opp),
                "recommended_action": self._recommend_action(opp)
            }
        )
        
    async def _track_signals(self, signals: List[Dict[str, Any]]) -> AgentResult:
        for signal in signals:
            self.signal_history.append({
                "timestamp": __import__('time').time(),
                "type": signal.get("type"),
                "source": signal.get("source"),
                "value": signal.get("value"),
                "confidence": signal.get("confidence", 0.5)
            })
            
            indicator_type = signal.get("type", "general")
            self.market_indicators[indicator_type].append(signal.get("value", 0))
            
        trends = {}
        for indicator, values in self.market_indicators.items():
            if len(values) >= 2:
                trend = "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "stable"
                volatility = math.sqrt(sum((v - sum(values)/len(values))**2 for v in values) / len(values)) if values else 0
                trends[indicator] = {
                    "trend": trend,
                    "volatility": round(volatility, 4),
                    "data_points": len(values)
                }
                
        return AgentResult(
            success=True,
            data={
                "signals_tracked": len(signals),
                "indicators_monitored": len(self.market_indicators),
                "trends": trends
            }
        )
        
    async def _forecast_timeline(
        self,
        opportunity_id: str
    ) -> AgentResult:
        if opportunity_id not in self.opportunities:
            return AgentResult(
                success=False,
                error=f"Opportunity {opportunity_id} not found"
            )
            
        opp = self.opportunities[opportunity_id]
        
        scenarios = []
        for scenario in ["optimistic", "realistic", "pessimistic"]:
            if scenario == "optimistic":
                prob = min(1.0, opp.probability * 1.3)
                value = opp.estimated_value * 1.2
            elif scenario == "pessimistic":
                prob = opp.probability * 0.7
                value = opp.estimated_value * 0.8
            else:
                prob = opp.probability
                value = opp.estimated_value
                
            scenarios.append({
                "scenario": scenario,
                "probability": round(prob, 4),
                "expected_value": round(value * prob, 2),
                "timeline": opp.time_window * (0.8 if scenario == "optimistic" else 1.2 if scenario == "pessimistic" else 1.0)
            })
            
        return AgentResult(
            success=True,
            data={
                "opportunity_id": opportunity_id,
                "scenarios": scenarios,
                "expected_timeline": opp.time_window,
                "confidence_interval": [
                    opp.time_window * 0.7,
                    opp.time_window * 1.3
                ]
            }
        )
        
    def _detect_from_signal(
        self,
        signal: Dict[str, Any],
        category: str
    ) -> Optional[Opportunity]:
        value = signal.get("value", 0)
        threshold = signal.get("threshold", 0.5)
        
        if value > threshold:
            return Opportunity(
                opportunity_id=f"opp_{len(self.opportunities)}",
                description=f"Detected from {signal.get('type', 'signal')}",
                category=category,
                estimated_value=value * 100,
                probability=min(1.0, value),
                time_window=signal.get("time_window", 30)
            )
        return None
        
    def _detect_from_metric(
        self,
        metric_name: str,
        metric_value: float
    ) -> Optional[Opportunity]:
        if metric_value > 0.8:
            return Opportunity(
                opportunity_id=f"opp_{len(self.opportunities)}",
                description=f"High performance in {metric_name}",
                category="internal",
                estimated_value=metric_value * 50,
                probability=metric_value,
                time_window=14
            )
        return None
        
    def _detect_from_event(self, event: Dict[str, Any]) -> Optional[Opportunity]:
        impact = event.get("impact", 0)
        if impact > 0.6:
            return Opportunity(
                opportunity_id=f"opp_{len(self.opportunities)}",
                description=event.get("description", "External event opportunity"),
                category="external",
                estimated_value=impact * 200,
                probability=impact,
                time_window=event.get("time_window", 7)
            )
        return None
        
    def _opportunity_score(self, opp: Opportunity) -> float:
        time_urgency = 1.0 / (1.0 + opp.time_window * 0.1)
        return (opp.estimated_value * opp.probability * time_urgency) / 100.0
        
    def _generate_swot(self, opp: Opportunity) -> Dict[str, List[str]]:
        return {
            "strengths": [
                f"Estimated value: {opp.estimated_value}",
                f"Probability: {opp.probability:.1%}"
            ],
            "weaknesses": [
                f"Time constraint: {opp.time_window} days",
                f"Resource requirements: {len(opp.required_resources)}"
            ],
            "opportunities": [
                "Market timing favorable",
                "First-mover advantage potential"
            ],
            "threats": opp.constraints
        }
        
    def _analyze_competitive_position(self, opp: Opportunity) -> Dict[str, Any]:
        return {
            "barriers": len(opp.constraints),
            "differentiation_potential": "high" if opp.estimated_value > 500 else "medium",
            "speed_to_market": "fast" if opp.time_window < 7 else "moderate"
        }
        
    def _assess_feasibility(self, opp: Opportunity) -> Dict[str, Any]:
        resource_score = 1.0 / (1.0 + len(opp.required_resources) * 0.2)
        constraint_score = 1.0 / (1.0 + len(opp.constraints) * 0.3)
        
        return {
            "score": round((resource_score + constraint_score) / 2, 4),
            "resource_ready": len(opp.required_resources) < 3,
            "constraints_manageable": len(opp.constraints) < 5
        }
        
    def _recommend_action(self, opp: Opportunity) -> str:
        score = self._opportunity_score(opp)
        if score > 5.0:
            return "Immediate action required"
        elif score > 2.0:
            return "Evaluate and prepare"
        elif score > 1.0:
            return "Monitor and plan"
        else:
            return "Low priority, maintain awareness"
            
    def _categorize_opportunities(
        self,
        opportunities: List[Opportunity]
    ) -> Dict[str, int]:
        categories = defaultdict(int)
        for opp in opportunities:
            categories[opp.category] += 1
        return dict(categories)