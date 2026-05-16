"""
Ethics Guardrail Service
Evaluates actions for ethical compliance, bias, and stakeholder impact.
Uses Antigravity's responsible AI framework for governance.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


class EthicsFramework(Enum):
    CONSEQUENTIALIST = "consequentialist"
    DEONTOLOGICAL = "deontological"
    VIRTUE = "virtue"
    CARE = "care"
    JUSTICE = "justice"


@dataclass
class EthicsAssessment:
    action_id: str
    overall_score: float  # 0-1, higher is better
    framework_scores: Dict[str, float]
    bias_detected: List[Dict[str, Any]]
    stakeholder_impacts: List[Dict[str, Any]]
    red_flags: List[str]
    recommendations: List[str]
    is_blocked: bool = False
    block_reason: Optional[str] = None


class EthicsGuardrailService:
    """
    Multi-framework ethical evaluation with bias detection.
    Integrates with Antigravity for enterprise governance.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._blocked_actions: List[str] = []
        logger.info("EthicsGuardrailService initialized")

    async def evaluate(
        self,
        action: Dict[str, Any],
        frameworks: Optional[List[EthicsFramework]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> EthicsAssessment:
        """
        Agentic ethical evaluation:
        1. Intent analysis → 2. Multi-framework evaluation → 3. Bias audit →
        4. Stakeholder mapping → 5. Red flag detection → 6. Recommendation synthesis
        """
        frameworks = frameworks or list(EthicsFramework)
        context = context or {}
        
        try:
            # Step 1: Analyze intent
            intent = await self._analyze_intent(action, context)
            
            # Step 2: Multi-framework evaluation
            framework_scores = {}
            for framework in frameworks:
                score = await self._evaluate_framework(action, intent, framework, context)
                framework_scores[framework.value] = score
            
            # Step 3: Bias audit
            bias = await self._audit_bias(action, context)
            
            # Step 4: Stakeholder impact
            stakeholders = await self._map_stakeholders(action, context)
            
            # Step 5: Red flag detection
            red_flags = self._detect_red_flags(action, framework_scores, bias)
            
            # Step 6: Block if necessary
            is_blocked, block_reason = self._should_block(red_flags, framework_scores)
            
            if is_blocked:
                self._blocked_actions.append(action.get("id", "unknown"))
            
            # Step 7: Generate recommendations
            recommendations = await self._generate_recommendations(
                framework_scores, bias, red_flags
            )
            
            overall = sum(framework_scores.values()) / max(len(framework_scores), 1)
            
            return EthicsAssessment(
                action_id=action.get("id", "unknown"),
                overall_score=overall,
                framework_scores=framework_scores,
                bias_detected=bias,
                stakeholder_impacts=stakeholders,
                red_flags=red_flags,
                recommendations=recommendations,
                is_blocked=is_blocked,
                block_reason=block_reason
            )

        except Exception as e:
            logger.error(f"Ethics evaluation failed: {e}")
            raise EthicsGuardrailError(f"Evaluation failed: {e}") from e

    async def _analyze_intent(
        self, action: Dict, context: Dict
    ) -> Dict[str, Any]:
        """Analyze action intent."""
        try:
            return await self.ag.ethics.analyze_intent(action, context)
        except Exception:
            return {"intent": "unknown", "benign": True}

    async def _evaluate_framework(
        self,
        action: Dict,
        intent: Dict,
        framework: EthicsFramework,
        context: Dict
    ) -> float:
        """Evaluate action under specific ethical framework."""
        try:
            result = await self.ag.ethics.evaluate_framework(
                action=action,
                framework=framework.value,
                context=context
            )
            return result.get("score", 0.8)
        except Exception:
            # Fallback scoring
            if framework == EthicsFramework.CONSEQUENTIALIST:
                return 0.8 if intent.get("benign", True) else 0.3
            elif framework == EthicsFramework.DEONTOLOGICAL:
                return 0.9 if not action.get("violates_rules") else 0.2
            return 0.7

    async def _audit_bias(
        self, action: Dict, context: Dict
    ) -> List[Dict[str, Any]]:
        """Audit for demographic bias."""
        try:
            audit = await self.ag.ethics.audit_bias(action, context)
            return audit.get("biases", [])
        except Exception:
            return []

    async def _map_stakeholders(
        self, action: Dict, context: Dict
    ) -> List[Dict[str, Any]]:
        """Map affected stakeholders."""
        try:
            mapping = await self.ag.ethics.map_stakeholders(action, context)
            return mapping.get("stakeholders", [])
        except Exception:
            return []

    def _detect_red_flags(
        self,
        action: Dict,
        scores: Dict[str, float],
        bias: List[Dict]
    ) -> List[str]:
        """Detect ethical red flags."""
        flags = []
        
        # Low score in any framework
        for framework, score in scores.items():
            if score < 0.3:
                flags.append(f"Low {framework} ethics score: {score:.2f}")
        
        # Bias detected
        if bias:
            flags.append(f"Bias detected: {len(bias)} instances")
        
        # High risk actions
        if action.get("risk_level") == "critical":
            flags.append("Critical risk level action")
        
        # Irreversible without consent
        if action.get("irreversible") and not action.get("user_consent"):
            flags.append("Irreversible action without explicit consent")
        
        return flags

    def _should_block(
        self, red_flags: List[str], scores: Dict[str, float]
    ) -> Tuple[bool, Optional[str]]:
        """Determine if action should be blocked."""
        if len(red_flags) >= 3:
            return True, f"Multiple red flags: {red_flags[0]}"
        
        if any(score < 0.2 for score in scores.values()):
            return True, "Ethics score below threshold in at least one framework"
        
        return False, None

    async def _generate_recommendations(
        self,
        scores: Dict[str, float],
        bias: List[Dict],
        red_flags: List[str]
    ) -> List[str]:
        """Generate ethical improvement recommendations."""
        recs = []
        
        if bias:
            recs.append("Apply bias mitigation techniques before execution")
        
        if any(s < 0.5 for s in scores.values()):
            recs.append("Review action with ethics board")
        
        if red_flags:
            recs.append(f"Address {len(red_flags)} identified red flags")
        
        # Antigravity recommendations
        try:
            ag_recs = await self.ag.ethics.get_recommendations(scores, bias)
            recs.extend(ag_recs)
        except Exception:
            pass
        
        return list(set(recs))


class EthicsGuardrailError(Exception):
    pass