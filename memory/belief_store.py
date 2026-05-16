import asyncio
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Belief:
    id: str
    statement: str
    topic: str
    confidence: float = 0.5
    evidence_for: List[Dict[str, Any]] = field(default_factory=list)
    evidence_against: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    stability: float = 0.5

class BeliefStore:
    def __init__(self):
        self._beliefs: Dict[str, Belief] = {}
        self._topic_index: Dict[str, List[str]] = {}
        self._lock = asyncio.Lock()

    async def store(
        self,
        statement: str,
        topic: str,
        confidence: float = 0.5,
        evidence: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        belief_id = f"belief_{uuid.uuid4().hex[:12]}"
        
        belief = Belief(
            id=belief_id,
            statement=statement,
            topic=topic,
            confidence=confidence,
            evidence_for=evidence or []
        )
        
        async with self._lock:
            self._beliefs[belief_id] = belief
            
            if topic not in self._topic_index:
                self._topic_index[topic] = []
            self._topic_index[topic].append(belief_id)
        
        logger.info(f"Belief stored: {belief_id}")
        return belief_id

    async def get_beliefs(
        self,
        topic: Optional[str] = None,
        min_confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        beliefs = self._beliefs.values()
        
        if topic:
            belief_ids = self._topic_index.get(topic, [])
            beliefs = [self._beliefs.get(bid) for bid in belief_ids]
            beliefs = [b for b in beliefs if b is not None]
        
        if min_confidence is not None:
            beliefs = [b for b in beliefs if b.confidence >= min_confidence]
        
        return [
            {
                "id": b.id,
                "statement": b.statement,
                "topic": b.topic,
                "confidence": b.confidence,
                "stability": b.stability,
                "evidence_count": len(b.evidence_for) + len(b.evidence_against)
            }
            for b in beliefs
        ]

    async def update_confidence(
        self,
        belief_id: str,
        new_confidence: float,
        evidence: Optional[Dict[str, Any]] = None
    ) -> bool:
        belief = self._beliefs.get(belief_id)
        if not belief:
            return False
        
        old_confidence = belief.confidence
        belief.confidence = max(0.0, min(1.0, new_confidence))
        belief.updated_at = datetime.utcnow()
        
        # Update stability based on confidence change
        change = abs(belief.confidence - old_confidence)
        belief.stability = max(0.0, belief.stability - change * 0.5)
        
        if evidence:
            if evidence.get("supports", True):
                belief.evidence_for.append(evidence)
            else:
                belief.evidence_against.append(evidence)
        
        logger.info(f"Belief confidence updated: {belief_id} -> {belief.confidence:.3f}")
        return True

    async def challenge(
        self,
        belief_id: str,
        counter_evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        belief = self._beliefs.get(belief_id)
        if not belief:
            return {"error": "Belief not found"}
        
        belief.evidence_against.append(counter_evidence)
        
        # Bayesian-like confidence update
        prior = belief.confidence
        likelihood = 0.3
        evidence_strength = counter_evidence.get("strength", 0.5)
        
        posterior = prior * (1 - likelihood * evidence_strength)
        belief.confidence = max(0.0, posterior)
        belief.updated_at = datetime.utcnow()
        belief.stability = max(0.0, belief.stability - 0.1)
        
        return {
            "belief_id": belief_id,
            "old_confidence": prior,
            "new_confidence": belief.confidence,
            "evidence_against_count": len(belief.evidence_against)
        }

    async def reinforce(
        self,
        belief_id: str,
        supporting_evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        belief = self._beliefs.get(belief_id)
        if not belief:
            return {"error": "Belief not found"}
        
        belief.evidence_for.append(supporting_evidence)
        
        prior = belief.confidence
        evidence_strength = supporting_evidence.get("strength", 0.5)
        
        posterior = prior + (1 - prior) * evidence_strength * 0.3
        belief.confidence = min(1.0, posterior)
        belief.updated_at = datetime.utcnow()
        belief.stability = min(1.0, belief.stability + 0.05)
        
        return {
            "belief_id": belief_id,
            "old_confidence": prior,
            "new_confidence": belief.confidence,
            "evidence_for_count": len(belief.evidence_for)
        }

    async def delete(self, belief_id: str) -> bool:
        async with self._lock:
            if belief_id not in self._beliefs:
                return False
            
            belief = self._beliefs[belief_id]
            
            if belief.topic in self._topic_index:
                self._topic_index[belief.topic] = [
                    bid for bid in self._topic_index[belief.topic]
                    if bid != belief_id
                ]
            
            del self._beliefs[belief_id]
            logger.info(f"Belief deleted: {belief_id}")
            return True

    async def get_stats(self) -> Dict[str, Any]:
        total = len(self._beliefs)
        by_topic = {
            topic: len(bids)
            for topic, bids in self._topic_index.items()
        }
        
        avg_confidence = sum(b.confidence for b in self._beliefs.values()) / total if total > 0 else 0
        avg_stability = sum(b.stability for b in self._beliefs.values()) / total if total > 0 else 0
        
        return {
            "total_beliefs": total,
            "by_topic": by_topic,
            "average_confidence": avg_confidence,
            "average_stability": avg_stability,
            "high_confidence_beliefs": sum(1 for b in self._beliefs.values() if b.confidence > 0.8)
        }