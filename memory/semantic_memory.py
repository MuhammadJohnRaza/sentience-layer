import asyncio
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger
from memory.embedding_engine import EmbeddingEngine

logger = get_logger(__name__)

@dataclass
class SemanticConcept:
    id: str
    concept: str
    category: str
    description: str
    embedding: Optional[List[float]] = None
    confidence: float = 0.8
    source_episodes: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    access_count: int = 0

class SemanticMemoryStore:
    def __init__(self):
        self._concepts: Dict[str, SemanticConcept] = {}
        self._category_index: Dict[str, List[str]] = {}
        self._embedding_engine = EmbeddingEngine()
        self._lock = asyncio.Lock()

    async def store(
        self,
        concept: str,
        description: str,
        category: str = "general",
        source_episodes: Optional[List[str]] = None,
        confidence: float = 0.8
    ) -> str:
        concept_id = f"sem_{uuid.uuid4().hex[:12]}"
        
        embedding = await self._embedding_engine.embed(f"{concept}: {description}")
        
        semantic = SemanticConcept(
            id=concept_id,
            concept=concept,
            category=category,
            description=description,
            embedding=embedding,
            confidence=confidence,
            source_episodes=source_episodes or []
        )
        
        async with self._lock:
            self._concepts[concept_id] = semantic
            
            if category not in self._category_index:
                self._category_index[category] = []
            self._category_index[category].append(concept_id)
        
        logger.info(f"Semantic concept stored: {concept_id}")
        return concept_id

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        similarity_threshold: float = 0.7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query_embedding = await self._embedding_engine.embed(query)
        
        candidates = self._concepts.values()
        if category:
            candidates = [
                self._concepts.get(cid) for cid in self._category_index.get(category, [])
            ]
            candidates = [c for c in candidates if c is not None]
        
        scored = []
        for concept in candidates:
            if concept.embedding:
                similarity = self._cosine_similarity(query_embedding, concept.embedding)
                if similarity >= similarity_threshold:
                    scored.append((concept, similarity))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for concept, similarity in scored[:limit]:
            concept.last_accessed = datetime.utcnow()
            concept.access_count += 1
            
            results.append({
                "concept_id": concept.id,
                "concept": concept.concept,
                "description": concept.description,
                "category": concept.category,
                "similarity": similarity,
                "confidence": concept.confidence,
                "access_count": concept.access_count
            })
        
        return results

    async def get_stale_concepts(
        self,
        cutoff: datetime
    ) -> List[Dict[str, Any]]:
        return [
            {
                "id": c.id,
                "concept": c.concept,
                "last_accessed": c.last_accessed,
                "access_count": c.access_count
            }
            for c in self._concepts.values()
            if c.last_accessed and c.last_accessed < cutoff
        ]

    async def add_relation(
        self,
        concept_id: str,
        related_id: str
    ) -> bool:
        concept = self._concepts.get(concept_id)
        if not concept:
            return False
        
        if related_id not in concept.related_concepts:
            concept.related_concepts.append(related_id)
        
        related = self._concepts.get(related_id)
        if related and concept_id not in related.related_concepts:
            related.related_concepts.append(concept_id)
        
        return True

    async def delete(
        self,
        concept_id: str
    ) -> bool:
        async with self._lock:
            if concept_id not in self._concepts:
                return False
            
            concept = self._concepts[concept_id]
            
            if concept.category in self._category_index:
                self._category_index[concept.category] = [
                    cid for cid in self._category_index[concept.category]
                    if cid != concept_id
                ]
            
            del self._concepts[concept_id]
            logger.info(f"Semantic concept deleted: {concept_id}")
            return True

    async def get_learning_progress(self) -> Dict[str, Any]:
        total = len(self._concepts)
        by_category = {
            cat: len(cids)
            for cat, cids in self._category_index.items()
        }
        
        avg_confidence = sum(c.confidence for c in self._concepts.values()) / total if total > 0 else 0
        
        return {
            "total_concepts": total,
            "by_category": by_category,
            "average_confidence": avg_confidence,
            "total_accesses": sum(c.access_count for c in self._concepts.values())
        }

    def _cosine_similarity(
        self,
        a: List[float],
        b: List[float]
    ) -> float:
        import math
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)