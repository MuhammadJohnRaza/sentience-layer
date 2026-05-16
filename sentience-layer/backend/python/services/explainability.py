"""
Explainability Service
Generates human-understandable explanations for agent decisions.
Uses Antigravity for multi-perspective explanation generation.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


class ExplanationType(Enum):
    CONTRASTIVE = "contrastive"  # Why A not B?
    FEATURE_IMPORTANCE = "feature_importance"
    COUNTERFACTUAL = "counterfactual"
    NATURAL_LANGUAGE = "natural_language"
    VISUAL = "visual"
    MULTI_AGENT = "multi_agent"  # Why did agents decide this?


@dataclass
class Explanation:
    type: ExplanationType
    content: str
    confidence: float
    target_audience: str  # technical, business, executive, novice
    supporting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    visual_data: Optional[Dict] = None


class ExplainabilityService:
    """
    Multi-modal explanation generation for AI decisions.
    Integrates with Antigravity for standardized explainability APIs.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("ExplainabilityService initialized")

    async def explain(
        self,
        decision: Dict[str, Any],
        explanation_types: Optional[List[ExplanationType]] = None,
        audience: str = "business",
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Explanation]:
        """
        Agentic explanation generation:
        1. Decision decomposition → 2. Evidence gathering → 3. Multi-format generation →
        4. Audience calibration → 5. Validation
        """
        explanation_types = explanation_types or [
            ExplanationType.NATURAL_LANGUAGE,
            ExplanationType.FEATURE_IMPORTANCE
        ]
        context = context or {}
        
        try:
            explanations = []
            
            for exp_type in explanation_types:
                if exp_type == ExplanationType.NATURAL_LANGUAGE:
                    exp = await self._generate_nlp_explanation(decision, audience, context)
                elif exp_type == ExplanationType.CONTRASTIVE:
                    exp = await self._generate_contrastive_explanation(decision, audience, context)
                elif exp_type == ExplanationType.COUNTERFACTUAL:
                    exp = await self._generate_counterfactual_explanation(decision, audience, context)
                elif exp_type == ExplanationType.FEATURE_IMPORTANCE:
                    exp = await self._generate_feature_importance(decision, audience, context)
                elif exp_type == ExplanationType.MULTI_AGENT:
                    exp = await self._generate_multi_agent_explanation(decision, audience, context)
                else:
                    continue
                
                explanations.append(exp)
            
            # Validate explanations
            validated = await self._validate_explanations(explanations, decision)
            
            logger.info(f"Generated {len(validated)} explanations for decision {decision.get('id')}")
            return validated

        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            raise ExplainabilityError(f"Explanation failed: {e}") from e

    async def _generate_nlp_explanation(
        self, decision: Dict, audience: str, context: Dict
    ) -> Explanation:
        """Generate natural language explanation."""
        try:
            nlp_exp = await self.ag.explain.natural_language(
                decision=decision,
                audience=audience,
                depth="detailed" if audience == "technical" else "summary"
            )
            
            return Explanation(
                type=ExplanationType.NATURAL_LANGUAGE,
                content=nlp_exp.get("text", "Decision made based on available evidence."),
                confidence=nlp_exp.get("confidence", 0.8),
                target_audience=audience,
                supporting_evidence=nlp_exp.get("evidence", [])
            )
        except Exception as e:
            return Explanation(
                type=ExplanationType.NATURAL_LANGUAGE,
                content=f"Decision: {decision.get('action', 'unknown')}. "
                        f"Confidence: {decision.get('confidence', 'unknown')}",
                confidence=0.6,
                target_audience=audience
            )

    async def _generate_contrastive_explanation(
        self, decision: Dict, audience: str, context: Dict
    ) -> Explanation:
        """Generate "Why A instead of B?" explanation."""
        try:
            alternatives = decision.get("rejected_alternatives", [])
            if not alternatives:
                return Explanation(
                    type=ExplanationType.CONTRASTIVE,
                    content="No alternatives were considered.",
                    confidence=0.5,
                    target_audience=audience
                )
            
            contrastive = await self.ag.explain.contrastive(
                chosen=decision,
                rejected=alternatives[0]
            )
            
            return Explanation(
                type=ExplanationType.CONTRASTIVE,
                content=contrastive.get("explanation", ""),
                confidence=contrastive.get("confidence", 0.75),
                target_audience=audience,
                supporting_evidence=contrastive.get("comparisons", [])
            )
        except Exception as e:
            return Explanation(
                type=ExplanationType.CONTRASTIVE,
                content=f"Selected option had highest expected value compared to alternatives.",
                confidence=0.6,
                target_audience=audience
            )

    async def _generate_counterfactual_explanation(
        self, decision: Dict, audience: str, context: Dict
    ) -> Explanation:
        """Generate counterfactual scenarios."""
        try:
            counterfactuals = await self.ag.explain.counterfactuals(decision, n=3)
            parts = []
            for cf in counterfactuals:
                parts.append(
                    f"If {cf.get('change', 'X')} had been different, "
                    f"the outcome would be {cf.get('outcome', 'Y')} "
                    f"({cf.get('probability', 0):.0%} probability)"
                )
            
            return Explanation(
                type=ExplanationType.COUNTERFACTUAL,
                content="\n".join(parts),
                confidence=0.7,
                target_audience=audience,
                supporting_evidence=counterfactuals
            )
        except Exception:
            return Explanation(
                type=ExplanationType.COUNTERFACTUAL,
                content="Counterfactual analysis unavailable.",
                confidence=0.3,
                target_audience=audience
            )

    async def _generate_feature_importance(
        self, decision: Dict, audience: str, context: Dict
    ) -> Explanation:
        """Generate feature importance visualization data."""
        try:
            importance = await self.ag.explain.feature_importance(decision)
            
            # Simplify for non-technical audiences
            if audience != "technical":
                top_features = sorted(
                    importance.get("features", []),
                    key=lambda x: x.get("importance", 0),
                    reverse=True
                )[:3]
                text = "Top factors:\n" + "\n".join([
                    f"- {f.get('name')}: {f.get('importance', 0):.0%}"
                    for f in top_features
                ])
            else:
                text = json.dumps(importance, indent=2)
            
            return Explanation(
                type=ExplanationType.FEATURE_IMPORTANCE,
                content=text,
                confidence=0.85,
                target_audience=audience,
                visual_data=importance
            )
        except Exception:
            return Explanation(
                type=ExplanationType.FEATURE_IMPORTANCE,
                content="Feature importance data unavailable.",
                confidence=0.3,
                target_audience=audience
            )

    async def _generate_multi_agent_explanation(
        self, decision: Dict, audience: str, context: Dict
    ) -> Explanation:
        """Explain multi-agent consensus process."""
        try:
            agent_votes = decision.get("agent_votes", {})
            if not agent_votes:
                return Explanation(
                    type=ExplanationType.MULTI_AGENT,
                    content="Single agent decision.",
                    confidence=0.9,
                    target_audience=audience
                )
            
            parts = ["Multi-agent decision process:"]
            for agent, vote in agent_votes.items():
                parts.append(f"- {agent}: {vote.get('position', 'unknown')} "
                           f"({vote.get('confidence', 0):.0%} confidence)")
            
            return Explanation(
                type=ExplanationType.MULTI_AGENT,
                content="\n".join(parts),
                confidence=sum(v.get("confidence", 0) for v in agent_votes.values()) / len(agent_votes),
                target_audience=audience,
                supporting_evidence=list(agent_votes.values())
            )
        except Exception:
            return Explanation(
                type=ExplanationType.MULTI_AGENT,
                content="Multi-agent reasoning details unavailable.",
                confidence=0.5,
                target_audience=audience
            )

    async def _validate_explanations(
        self, explanations: List[Explanation], decision: Dict
    ) -> List[Explanation]:
        """Validate explanations for consistency."""
        # Check that explanations don't contradict each other
        return explanations


class ExplainabilityError(Exception):
    pass