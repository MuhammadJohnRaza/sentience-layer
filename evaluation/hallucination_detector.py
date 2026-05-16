import asyncio
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger
from services.content_understanding import ContentUnderstandingService
from memory.semantic_memory import SemanticMemoryStore

logger = get_logger(__name__)

@dataclass
class HallucinationReport:
    claim_id: str
    claim: str
    is_hallucinated: bool
    confidence: float
    evidence_found: List[Dict[str, Any]] = field(default_factory=list)
    evidence_missing: List[str] = field(default_factory=list)
    source_documents: List[str] = field(default_factory=list)
    detection_method: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

class HallucinationDetector:
    def __init__(self):
        self.content_service = ContentUnderstandingService()
        self.semantic_store = SemanticMemoryStore()
        self._threshold: float = 0.7
        self._methods: List[str] = ["retrieval", "consistency", "fact_checking"]

    async def detect(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
        source_documents: Optional[List[str]] = None
    ) -> HallucinationReport:
        claims = await self._extract_claims(text)
        
        if not claims:
            return HallucinationReport(
                claim_id=f"empty_{hash(text)}",
                claim=text,
                is_hallucinated=False,
                confidence=1.0,
                detection_method="no_claims_found"
            )
        
        verification_tasks = [
            self._verify_claim(claim, context, source_documents)
            for claim in claims
        ]
        
        results = await asyncio.gather(*verification_tasks)
        
        hallucinated_count = sum(1 for r in results if r["is_hallucinated"])
        total_claims = len(results)
        
        is_hallucinated = hallucinated_count > 0
        confidence = hallucinated_count / total_claims if total_claims > 0 else 0.0
        
        evidence_found = []
        evidence_missing = []
        
        for r in results:
            if r["is_hallucinated"]:
                evidence_missing.extend(r.get("missing_evidence", []))
            else:
                evidence_found.extend(r.get("supporting_evidence", []))
        
        return HallucinationReport(
            claim_id=f"claim_{hash(text)}",
            claim=text[:200],
            is_hallucinated=is_hallucinated,
            confidence=confidence,
            evidence_found=evidence_found,
            evidence_missing=list(set(evidence_missing)),
            source_documents=source_documents or [],
            detection_method="multi_method_verification"
        )

    async def _extract_claims(self, text: str) -> List[Dict[str, Any]]:
        try:
            extracted = await self.content_service.extract_entities(text)
            return extracted.get("claims", [])
        except Exception:
            sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
            return [{"text": s, "type": "statement"} for s in sentences]

    async def _verify_claim(
        self,
        claim: Dict[str, Any],
        context: Optional[Dict[str, Any]],
        source_documents: Optional[List[str]]
    ) -> Dict[str, Any]:
        claim_text = claim.get("text", "")
        
        retrieval_result = await self._retrieval_verification(claim_text)
        consistency_result = await self._consistency_verification(claim_text, context)
        fact_result = await self._fact_checking(claim_text)
        
        scores = [
            retrieval_result.get("score", 0.0),
            consistency_result.get("score", 0.0),
            fact_result.get("score", 0.0)
        ]
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            "is_hallucinated": avg_score < self._threshold,
            "score": avg_score,
            "supporting_evidence": retrieval_result.get("evidence", []) + fact_result.get("evidence", []),
            "missing_evidence": consistency_result.get("inconsistencies", []),
            "methods": {
                "retrieval": retrieval_result,
                "consistency": consistency_result,
                "fact_checking": fact_result
            }
        }

    async def _retrieval_verification(self, claim_text: str) -> Dict[str, Any]:
        try:
            memories = await self.semantic_store.search(
                query=claim_text,
                similarity_threshold=0.8
            )
            
            if memories:
                return {
                    "score": 0.9,
                    "evidence": [{"source": "memory", "content": m.get("description", "")} for m in memories[:3]]
                }
            
            return {"score": 0.3, "evidence": []}
        except Exception as e:
            logger.warning(f"Retrieval verification failed: {str(e)}")
            return {"score": 0.5, "evidence": []}

    async def _consistency_verification(
        self,
        claim_text: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not context:
            return {"score": 0.5, "inconsistencies": []}
        
        inconsistencies = []
        
        for key, value in context.items():
            if isinstance(value, str) and self._contradicts(claim_text, value):
                inconsistencies.append(f"Contradicts context: {key}")
        
        score = 1.0 if not inconsistencies else 0.4
        
        return {
            "score": score,
            "inconsistencies": inconsistencies
        }

    async def _fact_checking(self, claim_text: str) -> Dict[str, Any]:
        return {
            "score": 0.6,
            "evidence": [{"source": "fact_check", "status": "unverified"}]
        }

    def _contradicts(self, claim: str, context: str) -> bool:
        claim_words = set(claim.lower().split())
        context_words = set(context.lower().split())
        
        negations = {"not", "no", "never", "none", "without"}
        
        has_negation_claim = bool(claim_words & negations)
        has_negation_context = bool(context_words & negations)
        
        return has_negation_claim != has_negation_context

    async def batch_detect(
        self,
        texts: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[HallucinationReport]:
        tasks = [self.detect(text, context) for text in texts]
        return await asyncio.gather(*tasks)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "threshold": self._threshold,
            "methods": self._methods,
            "detections_run": 0
        }