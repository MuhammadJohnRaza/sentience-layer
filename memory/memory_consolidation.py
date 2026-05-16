import asyncio
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger
from memory.episodic_memory import EpisodicMemoryStore
from memory.semantic_memory import SemanticMemoryStore
from memory.belief_store import BeliefStore

logger = get_logger(__name__)

@dataclass
class ConsolidationResult:
    consolidation_id: str
    episodes_processed: int
    concepts_extracted: int
    beliefs_formed: int
    episodes_consolidated: List[str] = field(default_factory=list)
    concepts_created: List[str] = field(default_factory=list)
    beliefs_created: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

class MemoryConsolidator:
    def __init__(self):
        self.episodic_store = EpisodicMemoryStore()
        self.semantic_store = SemanticMemoryStore()
        self.belief_store = BeliefStore()
        self._lock = asyncio.Lock()
        self._status: Dict[str, Any] = {
            "last_run": None,
            "total_consolidations": 0,
            "status": "idle"
        }

    async def run(
        self,
        force: bool = False,
        max_episodes: int = 100
    ) -> ConsolidationResult:
        async with self._lock:
            self._status["status"] = "running"
            
            try:
                unconsolidated = await self._get_unconsolidated_episodes(max_episodes)
                
                if not unconsolidated and not force:
                    self._status["status"] = "idle"
                    return ConsolidationResult(
                        consolidation_id=f"cons_{uuid.uuid4().hex[:8]}",
                        episodes_processed=0,
                        concepts_extracted=0,
                        beliefs_formed=0
                    )
                
                result = await self._consolidate_batch(unconsolidated)
                
                self._status["last_run"] = datetime.utcnow()
                self._status["total_consolidations"] += 1
                self._status["status"] = "idle"
                
                logger.info(
                    f"Consolidation completed: {result.episodes_processed} episodes, "
                    f"{result.concepts_extracted} concepts, {result.beliefs_formed} beliefs"
                )
                
                return result
                
            except Exception as e:
                self._status["status"] = "error"
                logger.error(f"Consolidation failed: {str(e)}")
                raise

    async def _get_unconsolidated_episodes(
        self,
        limit: int
    ) -> List[Dict[str, Any]]:
        all_episodes = []
        
        for episode_id, episode in self.episodic_store._episodes.items():
            if not episode.consolidated:
                all_episodes.append({
                    "id": episode_id,
                    "content": episode.content,
                    "context": episode.context,
                    "emotional_valence": episode.emotional_valence,
                    "importance": episode.importance
                })
        
        # Sort by importance descending
        all_episodes.sort(key=lambda e: e["importance"], reverse=True)
        return all_episodes[:limit]

    async def _consolidate_batch(
        self,
        episodes: List[Dict[str, Any]]
    ) -> ConsolidationResult:
        consolidation_id = f"cons_{uuid.uuid4().hex[:8]}"
        
        concepts_created = []
        beliefs_created = []
        episodes_consolidated = []
        
        for episode in episodes:
            # Extract concepts from episode
            extracted_concepts = await self._extract_concepts(episode)
            
            for concept_data in extracted_concepts:
                concept_id = await self.semantic_store.store(
                    concept=concept_data["name"],
                    description=concept_data["description"],
                    category=concept_data.get("category", "general"),
                    source_episodes=[episode["id"]],
                    confidence=concept_data.get("confidence", 0.7)
                )
                concepts_created.append(concept_id)
            
            # Form beliefs from high-importance episodes
            if episode["importance"] > 0.6:
                belief_id = await self.belief_store.store(
                    statement=episode["content"][:200],
                    topic=episode["context"].get("topic", "general") if episode["context"] else "general",
                    confidence=min(1.0, episode["importance"]),
                    evidence=[{
                        "source": "episode",
                        "episode_id": episode["id"],
                        "strength": episode["importance"]
                    }]
                )
                beliefs_created.append(belief_id)
            
            # Mark episode as consolidated
            await self.episodic_store.mark_consolidated(episode["id"])
            episodes_consolidated.append(episode["id"])
        
        return ConsolidationResult(
            consolidation_id=consolidation_id,
            episodes_processed=len(episodes),
            concepts_extracted=len(concepts_created),
            beliefs_formed=len(beliefs_created),
            episodes_consolidated=episodes_consolidated,
            concepts_created=concepts_created,
            beliefs_created=beliefs_created
        )

    async def _extract_concepts(
        self,
        episode: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        # Simplified concept extraction
        content = episode["content"]
        words = content.split()
        
        # Extract key phrases (simplified)
        concepts = []
        
        # Look for noun phrases (simplified heuristic)
        for i in range(len(words) - 1):
            if words[i][0].isupper() and words[i+1][0].isupper():
                concept_name = f"{words[i]} {words[i+1]}"
                concepts.append({
                    "name": concept_name,
                    "description": f"Concept extracted from episode: {concept_name}",
                    "category": "extracted",
                    "confidence": 0.6
                })
        
        # If no concepts found, create a general one
        if not concepts:
            concepts.append({
                "name": "general_concept",
                "description": content[:100],
                "category": "general",
                "confidence": 0.5
            })
        
        return concepts[:5]  # Limit concepts per episode

    async def store_episode(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        return await self.episodic_store.store(content=content, context=context)

    async def store_concept(
        self,
        concept: str,
        description: str,
        source_episodes: List[str]
    ) -> str:
        return await self.semantic_store.store(
            concept=concept,
            description=description,
            source_episodes=source_episodes
        )

    async def store_belief(
        self,
        statement: str,
        topic: str,
        confidence: float,
        evidence: List[Dict[str, Any]]
    ) -> str:
        return await self.belief_store.store(
            statement=statement,
            topic=topic,
            confidence=confidence,
            evidence=evidence
        )

    async def get_status(self) -> Dict[str, Any]:
        return {
            **self._status,
            "last_run": self._status["last_run"].isoformat() if self._status["last_run"] else None
        }

    async def trigger_background_consolidation(self) -> str:
        task_id = f"cons_bg_{uuid.uuid4().hex[:8]}"
        
        asyncio.create_task(self._background_run(task_id))
        
        return task_id

    async def _background_run(self, task_id: str):
        try:
            await self.run()
            logger.info(f"Background consolidation completed: {task_id}")
        except Exception as e:
            logger.error(f"Background consolidation failed: {task_id} - {str(e)}")