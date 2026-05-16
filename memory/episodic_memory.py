import asyncio
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from utils.logger import get_logger
from memory.embedding_engine import EmbeddingEngine

logger = get_logger(__name__)

@dataclass
class MemoryEpisode:
    id: str
    content: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    emotional_valence: float = 0.0
    importance: float = 0.5
    created_at: datetime = field(default_factory=datetime.utcnow)
    consolidated: bool = False
    consolidated_at: Optional[datetime] = None
    related_episodes: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None

class EpisodicMemoryStore:
    def __init__(self):
        self._episodes: Dict[str, MemoryEpisode] = {}
        self._session_index: Dict[str, List[str]] = {}
        self._embedding_engine = EmbeddingEngine()
        self._lock = asyncio.Lock()

    async def store(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        emotional_valence: float = 0.0,
        importance: float = 0.5
    ) -> str:
        episode_id = f"ep_{uuid.uuid4().hex[:12]}"
        
        embedding = await self._embedding_engine.embed(content)
        
        episode = MemoryEpisode(
            id=episode_id,
            content=content,
            session_id=session_id,
            context=context,
            emotional_valence=emotional_valence,
            importance=importance,
            embedding=embedding
        )
        
        async with self._lock:
            self._episodes[episode_id] = episode
            
            if session_id:
                if session_id not in self._session_index:
                    self._session_index[session_id] = []
                self._session_index[session_id].append(episode_id)
        
        logger.info(f"Episode stored: {episode_id}")
        return episode_id

    async def retrieve(
        self,
        episode_id: str
    ) -> Optional[MemoryEpisode]:
        return self._episodes.get(episode_id)

    async def retrieve_by_session(
        self,
        session_id: str,
        limit: int = 100
    ) -> List[MemoryEpisode]:
        episode_ids = self._session_index.get(session_id, [])
        episodes = [self._episodes.get(eid) for eid in episode_ids]
        return [e for e in episodes if e is not None][-limit:]

    async def search(
        self,
        query: str,
        limit: int = 10,
        min_similarity: float = 0.7
    ) -> List[Dict[str, Any]]:
        query_embedding = await self._embedding_engine.embed(query)
        
        scored = []
        for episode in self._episodes.values():
            if episode.embedding:
                similarity = self._cosine_similarity(query_embedding, episode.embedding)
                if similarity >= min_similarity:
                    scored.append((episode, similarity))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {
                "episode_id": ep.id,
                "content": ep.content,
                "similarity": sim,
                "created_at": ep.created_at.isoformat()
            }
            for ep, sim in scored[:limit]
        ]

    async def get_before_date(
        self,
        cutoff: datetime
    ) -> List[Dict[str, Any]]:
        return [
            {
                "id": ep.id,
                "content": ep.content,
                "created_at": ep.created_at,
                "consolidated": ep.consolidated
            }
            for ep in self._episodes.values()
            if ep.created_at < cutoff
        ]

    async def mark_consolidated(
        self,
        episode_id: str
    ) -> bool:
        episode = self._episodes.get(episode_id)
        if not episode:
            return False
        
        episode.consolidated = True
        episode.consolidated_at = datetime.utcnow()
        logger.info(f"Episode marked consolidated: {episode_id}")
        return True

    async def add_relation(
        self,
        episode_id: str,
        related_id: str
    ) -> bool:
        episode = self._episodes.get(episode_id)
        if not episode:
            return False
        
        if related_id not in episode.related_episodes:
            episode.related_episodes.append(related_id)
        
        return True

    async def delete(
        self,
        episode_id: str
    ) -> bool:
        async with self._lock:
            if episode_id not in self._episodes:
                return False
            
            episode = self._episodes[episode_id]
            
            if episode.session_id and episode.session_id in self._session_index:
                self._session_index[episode.session_id] = [
                    eid for eid in self._session_index[episode.session_id]
                    if eid != episode_id
                ]
            
            del self._episodes[episode_id]
            logger.info(f"Episode deleted: {episode_id}")
            return True

    async def get_stats(self) -> Dict[str, Any]:
        total = len(self._episodes)
        consolidated = sum(1 for ep in self._episodes.values() if ep.consolidated)
        by_session = {
            sid: len(eids)
            for sid, eids in self._session_index.items()
        }
        
        return {
            "total_episodes": total,
            "consolidated": consolidated,
            "unconsolidated": total - consolidated,
            "sessions": len(by_session),
            "episodes_per_session": by_session
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