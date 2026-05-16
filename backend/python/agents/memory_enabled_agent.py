import hashlib
import time
from typing import Dict, List, Any, Optional
from collections import OrderedDict

from .base_agent import BaseAgent, AgentMessage, AgentResult

class MemoryEnabledAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "memory_agent",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.episodic_memory: OrderedDict = OrderedDict()
        self.semantic_memory: Dict[str, Any] = {}
        self.working_memory: Dict[str, Any] = {}
        self.memory_capacity = config.get("memory_capacity", 1000)
        self.retrieval_threshold = config.get("retrieval_threshold", 0.6)
        self.decay_rate = config.get("decay_rate", 0.01)
        
    async def initialize(self):
        self.register_skill("store", self._store_memory)
        self.register_skill("retrieve", self._retrieve_memory)
        self.register_skill("forget", self._forget_memory)
        self.register_skill("consolidate", self._consolidate_memories)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "retrieve")
        memory_type = message.metadata.get("memory_type", "episodic")
        
        if skill == "store":
            return await self._store_memory(message.content, memory_type)
        elif skill == "retrieve":
            return await self._retrieve_memory(
                message.content,
                message.metadata.get("query", ""),
                memory_type
            )
        elif skill == "forget":
            return await self._forget_memory(message.content)
        elif skill == "consolidate":
            return await self._consolidate_memories()
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _store_memory(
        self,
        content: Any,
        memory_type: str
    ) -> AgentResult:
        memory_id = self._hash_content(content)
        timestamp = time.time()
        
        memory_entry = {
            "id": memory_id,
            "content": content,
            "type": memory_type,
            "timestamp": timestamp,
            "access_count": 0,
            "last_accessed": timestamp,
            "associations": []
        }
        
        if memory_type == "episodic":
            self.episodic_memory[memory_id] = memory_entry
            self._enforce_capacity()
        elif memory_type == "semantic":
            self.semantic_memory[memory_id] = memory_entry
        elif memory_type == "working":
            self.working_memory[memory_id] = memory_entry
            
        return AgentResult(
            success=True,
            data={"memory_id": memory_id, "type": memory_type},
            confidence=1.0
        )
        
    async def _retrieve_memory(
        self,
        content: Any,
        query: str,
        memory_type: str
    ) -> AgentResult:
        memories = self._get_memory_store(memory_type)
        
        if not memories:
            return AgentResult(
                success=True,
                data={"results": [], "message": "No memories of this type"},
                confidence=0.0
            )
            
        scored_memories = []
        for mem_id, mem in memories.items():
            relevance = self._calculate_relevance(mem, query, content)
            recency = self._calculate_recency(mem)
            frequency = min(mem["access_count"] / 10, 1.0)
            
            score = (relevance * 0.5) + (recency * 0.3) + (frequency * 0.2)
            
            scored_memories.append({
                "memory": mem,
                "score": score,
                "relevance": relevance
            })
            
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        
        top_results = [
            m for m in scored_memories
            if m["score"] > self.retrieval_threshold
        ][:5]
        
        for result in top_results:
            mem = result["memory"]
            mem["access_count"] += 1
            mem["last_accessed"] = time.time()
            
        return AgentResult(
            success=True,
            data={
                "results": [
                    {
                        "id": r["memory"]["id"],
                        "content": r["memory"]["content"],
                        "score": r["score"],
                        "relevance": r["relevance"]
                    }
                    for r in top_results
                ],
                "total_matches": len(scored_memories),
                "returned": len(top_results)
            },
            confidence=top_results[0]["score"] if top_results else 0.0
        )
        
    async def _forget_memory(self, memory_id: str) -> AgentResult:
        removed = False
        
        if memory_id in self.episodic_memory:
            del self.episodic_memory[memory_id]
            removed = True
        if memory_id in self.semantic_memory:
            del self.semantic_memory[memory_id]
            removed = True
        if memory_id in self.working_memory:
            del self.working_memory[memory_id]
            removed = True
            
        return AgentResult(
            success=removed,
            data={"forgotten": removed, "memory_id": memory_id},
            confidence=1.0 if removed else 0.0
        )
        
    async def _consolidate_memories(self) -> AgentResult:
        if len(self.episodic_memory) < 10:
            return AgentResult(
                success=True,
                data={"message": "Insufficient memories for consolidation"},
                confidence=0.5
            )
            
        patterns = self._extract_patterns()
        abstractions = self._create_abstractions(patterns)
        
        for abstraction in abstractions:
            mem_id = self._hash_content(str(abstraction))
            self.semantic_memory[mem_id] = {
                "id": mem_id,
                "content": abstraction,
                "type": "semantic",
                "timestamp": time.time(),
                "derived_from": list(self.episodic_memory.keys())[:10],
                "access_count": 0,
                "last_accessed": time.time(),
                "associations": []
            }
            
        oldest_keys = list(self.episodic_memory.keys())[
            :len(self.episodic_memory) // 4
        ]
        for key in oldest_keys:
            del self.episodic_memory[key]
            
        return AgentResult(
            success=True,
            data={
                "patterns_found": len(patterns),
                "abstractions_created": len(abstractions),
                "memories_consolidated": len(oldest_keys)
            },
            confidence=0.8
        )
        
    def _get_memory_store(self, memory_type: str) -> Dict[str, Any]:
        if memory_type == "episodic":
            return dict(self.episodic_memory)
        elif memory_type == "semantic":
            return self.semantic_memory
        elif memory_type == "working":
            return self.working_memory
        return {}
        
    def _hash_content(self, content: Any) -> str:
        content_str = str(content)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]
        
    def _calculate_relevance(self, memory: Dict[str, Any], query: str, context: Any) -> float:
        mem_content = str(memory.get("content", "")).lower()
        query_lower = str(query).lower()
        context_str = str(context).lower()
        
        query_score = 0.0
        if query_lower:
            query_words = set(query_lower.split())
            mem_words = set(mem_content.split())
            overlap = len(query_words & mem_words)
            query_score = overlap / max(len(query_words), 1)
            
        context_score = 0.0
        if context_str:
            context_words = set(context_str.split())
            mem_words = set(mem_content.split())
            overlap = len(context_words & mem_words)
            context_score = overlap / max(len(context_words), 1)
            
        return (query_score * 0.6) + (context_score * 0.4)
        
    def _calculate_recency(self, memory: Dict[str, Any]) -> float:
        now = time.time()
        age = now - memory.get("timestamp", now)
        return max(0, 1 - (age / 86400))
        
    def _enforce_capacity(self):
        while len(self.episodic_memory) > self.memory_capacity:
            oldest = next(iter(self.episodic_memory))
            del self.episodic_memory[oldest]
            
    def _extract_patterns(self) -> List[Dict[str, Any]]:
        contents = [
            str(m["content"]) for m in self.episodic_memory.values()
        ]
        
        words = []
        for content in contents:
            words.extend(content.lower().split())
            
        from collections import Counter
        common = Counter(words).most_common(20)
        
        return [
            {"word": word, "frequency": count}
            for word, count in common
        ]
        
    def _create_abstractions(self, patterns: List[Dict[str, Any]]) -> List[str]:
        if not patterns:
            return []
            
        top_patterns = patterns[:5]
        abstraction = f"Common theme: {', '.join(p['word'] for p in top_patterns)}"
        
        return [abstraction]
        
    def get_memory_stats(self) -> Dict[str, Any]:
        return {
            "episodic_count": len(self.episodic_memory),
            "semantic_count": len(self.semantic_memory),
            "working_count": len(self.working_memory),
            "total_capacity": self.memory_capacity,
            "utilization": len(self.episodic_memory) / self.memory_capacity
        }