"""
Insight Extraction Service
Transforms raw understanding into structured, actionable insights.
Uses multi-step reasoning and Antigravity for cross-domain pattern matching.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from .content_understanding import ContentUnderstandingService, UnderstandingResult

logger = get_logger(__name__)


@dataclass
class Evidence:
    source: str
    excerpt: str
    confidence: float
    chunk_ids: List[str]
    validation_status: str = "unverified"  # unverified, confirmed, disputed


@dataclass
class Insight:
    id: str
    type: str  # pattern, anomaly, prediction, recommendation, risk
    title: str
    description: str
    confidence: float
    severity: str  # low, medium, high, critical
    evidence: List[Evidence]
    related_insights: List[str] = field(default_factory=list)
    action_suggestions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


class InsightExtractionService:
    """
    Multi-step insight extraction with causal reasoning and novelty detection.
    Integrates with Antigravity for cross-user pattern validation.
    """

    INSIGHT_TYPES = ["pattern", "anomaly", "prediction", "recommendation", "risk", "opportunity"]

    def __init__(
        self,
        antigravity_client: Optional[AntigravityClient] = None,
        content_service: Optional[ContentUnderstandingService] = None,
    ):
        self.ag = antigravity_client or AntigravityClient()
        self.content = content_service or ContentUnderstandingService(self.ag)
        self._insight_history: List[Insight] = []
        logger.info("InsightExtractionService initialized")

    async def extract(
        self,
        understanding: UnderstandingResult,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Insight]:
        """
        Agentic insight extraction pipeline:
        1. Pattern detection → 2. Anomaly detection → 3. Causal inference → 
        4. Cross-reference → 5. Novelty filter → 6. Action linking
        """
        context = context or {}
        insights: List[Insight] = []
        
        try:
            # Step 1: Pattern detection
            patterns = await self._detect_patterns(understanding, context)
            insights.extend(patterns)
            
            # Step 2: Anomaly detection
            anomalies = await self._detect_anomalies(understanding, context)
            insights.extend(anomalies)
            
            # Step 3: Causal inference
            causal = await self._infer_causal_insights(understanding, context)
            insights.extend(causal)
            
            # Step 4: Cross-reference with Antigravity global insights
            validated = await self._cross_reference_insights(insights)
            
            # Step 5: Novelty filter (don't repeat obvious insights)
            novel = self._filter_novel(validated)
            
            # Step 6: Link to actions
            actionable = await self._link_actions(novel, understanding)
            
            self._insight_history.extend(actionable)
            logger.info(f"Extracted {len(actionable)} novel insights")
            return actionable

        except Exception as e:
            logger.error(f"Insight extraction failed: {e}")
            raise InsightExtractionError(f"Extraction pipeline failed: {e}") from e

    async def _detect_patterns(
        self, understanding: UnderstandingResult, context: Dict
    ) -> List[Insight]:
        """Detect recurring patterns in content."""
        insights = []
        
        # Temporal patterns
        if len(understanding.raw_chunks) > 3:
            pattern_id = hashlib.md5(f"pattern-temporal-{context.get('user_id','')}".encode()).hexdigest()
            insights.append(Insight(
                id=pattern_id,
                type="pattern",
                title="Multi-part content detected",
                description="Content contains multiple distinct sections that may represent a workflow or process.",
                confidence=0.85,
                severity="low",
                evidence=[Evidence(
                    source="chunk_analysis",
                    excerpt=f"Found {len(understanding.raw_chunks)} semantic chunks",
                    confidence=0.85,
                    chunk_ids=[c.id for c in understanding.raw_chunks[:3]]
                )],
                metadata={"pattern_subtype": "structural"}
            ))
        
        # Topic convergence
        if len(understanding.topics) >= 2:
            # Check if topics are related via Antigravity KG
            try:
                relatedness = await self.ag.knowledge_graph.topic_relatedness(understanding.topics)
                if relatedness > 0.7:
                    pattern_id = hashlib.md5(f"pattern-convergence-{','.join(understanding.topics)}".encode()).hexdigest()
                    insights.append(Insight(
                        id=pattern_id,
                        type="pattern",
                        title="Topic convergence detected",
                        description=f"Topics {understanding.topics} show strong semantic convergence, suggesting a unified underlying theme.",
                        confidence=relatedness,
                        severity="medium",
                        evidence=[Evidence(
                            source="antigravity_kg",
                            excerpt=f"Relatedness score: {relatedness:.2f}",
                            confidence=relatedness,
                            chunk_ids=[]
                        )],
                        metadata={"pattern_subtype": "semantic_convergence"}
                    ))
            except Exception as e:
                logger.warning(f"Topic convergence check failed: {e}")
        
        return insights

    async def _detect_anomalies(
        self, understanding: UnderstandingResult, context: Dict
    ) -> List[Insight]:
        """Detect anomalies against user baseline."""
        insights = []
        
        # Sentiment anomaly
        sentiment = understanding.sentiment
        if sentiment.get("negative", 0) > 0.7:
            anomaly_id = hashlib.md5(f"anomaly-sentiment-{context.get('user_id','')}".encode()).hexdigest()
            insights.append(Insight(
                id=anomaly_id,
                type="anomaly",
                title="Negative sentiment spike",
                description="Content shows unusually negative sentiment compared to typical baseline.",
                confidence=sentiment.get("negative", 0),
                severity="high" if sentiment.get("negative", 0) > 0.9 else "medium",
                evidence=[Evidence(
                    source="sentiment_analysis",
                    excerpt=f"Negative score: {sentiment.get('negative', 0):.2f}",
                    confidence=0.9,
                    chunk_ids=[understanding.raw_chunks[0].id] if understanding.raw_chunks else []
                )],
                metadata={"anomaly_subtype": "sentiment"}
            ))
        
        # Urgency anomaly
        if understanding.urgency_score > 0.7:
            anomaly_id = hashlib.md5(f"anomaly-urgency-{context.get('user_id','')}".encode()).hexdigest()
            insights.append(Insight(
                id=anomaly_id,
                type="anomaly",
                title="Unusual urgency detected",
                description="Content contains urgency markers that exceed typical patterns.",
                confidence=understanding.urgency_score,
                severity="high",
                evidence=[Evidence(
                    source="urgency_scoring",
                    excerpt=f"Urgency score: {understanding.urgency_score:.2f}",
                    confidence=0.88,
                    chunk_ids=[]
                )],
                metadata={"anomaly_subtype": "urgency"}
            ))
        
        return insights

    async def _infer_causal_insights(
        self, understanding: UnderstandingResult, context: Dict
    ) -> List[Insight]:
        """Infer causal relationships using causal inference service."""
        from .causal_inference import CausalInferenceService
        causal = CausalInferenceService(antigravity_client=self.ag)
        
        insights = []
        # Look for causal language
        causal_markers = ["because", "caused", "led to", "resulted in", "due to", "therefore"]
        text = " ".join([c.content for c in understanding.raw_chunks])
        
        for marker in causal_markers:
            if marker in text.lower():
                # Extract causal hypothesis
                try:
                    causal_graph = await causal.discover_causal_links(text)
                    if causal_graph and len(causal_graph.get("edges", [])) > 0:
                        insight_id = hashlib.md5(f"causal-{marker}-{text[:50]}".encode()).hexdigest()
                        insights.append(Insight(
                            id=insight_id,
                            type="prediction",
                            title=f"Causal link detected via '{marker}'",
                            description=f"Potential causal relationship identified. Graph contains {len(causal_graph['edges'])} edges.",
                            confidence=0.75,
                            severity="medium",
                            evidence=[Evidence(
                                source="causal_inference",
                                excerpt=json.dumps(causal_graph["edges"][:2]),
                                confidence=0.75,
                                chunk_ids=[]
                            )],
                            metadata={"causal_graph": causal_graph}
                        ))
                except Exception as e:
                    logger.warning(f"Causal inference failed: {e}")
                break  # One causal insight is enough
        
        return insights

    async def _cross_reference_insights(self, insights: List[Insight]) -> List[Insight]:
        """Validate insights against Antigravity global knowledge."""
        validated = []
        for insight in insights:
            try:
                global_similar = await self.ag.insights.find_similar(insight.title, threshold=0.85)
                if global_similar:
                    insight.confidence = min(1.0, insight.confidence + 0.1)
                    insight.metadata["global_validation"] = True
                    insight.metadata["similar_insights_count"] = len(global_similar)
                else:
                    insight.metadata["global_validation"] = False
            except Exception:
                pass
            validated.append(insight)
        return validated

    def _filter_novel(self, insights: List[Insight]) -> List[Insight]:
        """Filter out insights that are too similar to recent history."""
        novel = []
        for insight in insights:
            is_duplicate = any(
                self._similarity(insight, hist) > 0.85 for hist in self._insight_history[-50:]
            )
            if not is_duplicate:
                novel.append(insight)
        return novel

    def _similarity(self, a: Insight, b: Insight) -> float:
        """Simple title-based similarity."""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a.title.lower(), b.title.lower()).ratio()

    async def _link_actions(
        self, insights: List[Insight], understanding: UnderstandingResult
    ) -> List[Insight]:
        """Suggest actions for each insight."""
        for insight in insights:
            if insight.type == "anomaly" and insight.severity in ["high", "critical"]:
                insight.action_suggestions.append("Escalate to human review")
                insight.action_suggestions.append("Create monitoring alert")
            elif insight.type == "pattern":
                insight.action_suggestions.append("Save to playbook")
                insight.action_suggestions.append("Share with team")
            elif insight.type == "prediction":
                insight.action_suggestions.append("Run simulation")
                insight.action_suggestions.append("Prepare contingency")
            
            # Antigravity action recommendation
            try:
                recs = await self.ag.actions.recommend_for_insight(insight.id)
                insight.action_suggestions.extend(recs)
            except Exception:
                pass
        
        return insights

    async def get_insight_history(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Insight]:
        """Retrieve insight history with optional filtering."""
        insights = self._insight_history
        if filters:
            if "type" in filters:
                insights = [i for i in insights if i.type == filters["type"]]
            if "severity" in filters:
                insights = [i for i in insights if i.severity == filters["severity"]]
        return insights[-100:]  # Last 100


class InsightExtractionError(Exception):
    pass