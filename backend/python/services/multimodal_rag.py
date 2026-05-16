"""
Multimodal RAG Service
Retrieval-Augmented Generation across text, image, and structured data.
Uses Antigravity's vector store for cross-modal retrieval.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import asyncio
import hashlib

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient
from backend.python.memory.embedding_engine import EmbeddingEngine
from backend.python.memory.graph_store import GraphStore

logger = get_logger(__name__)


@dataclass
class RetrievedContext:
    content: str
    modality: str  # text, image, table, code
    source: str
    relevance_score: float
    metadata: Dict[str, Any]


@dataclass
class RAGResult:
    query: str
    contexts: List[RetrievedContext]
    synthesized_answer: str
    confidence: float
    sources_used: List[str]


class MultimodalRAGService:
    """
    Multi-modal retrieval with dense, sparse, and graph-based strategies.
    Integrates with Antigravity for enterprise-scale vector search.
    """

    def __init__(
        self,
        antigravity_client: Optional[AntigravityClient] = None,
        embedding_engine: Optional[EmbeddingEngine] = None,
        graph_store: Optional[GraphStore] = None,
    ):
        self.ag = antigravity_client or AntigravityClient()
        self.embedder = embedding_engine or EmbeddingEngine()
        self.graph = graph_store or GraphStore()
        logger.info("MultimodalRAGService initialized")

    async def retrieve_and_generate(
        self,
        query: str,
        modalities: Optional[List[str]] = None,
        top_k: int = 5,
        context: Optional[Dict[str, Any]] = None,
    ) -> RAGResult:
        """
        Agentic RAG pipeline:
        1. Query understanding → 2. Multi-strategy retrieval → 3. Reranking →
        4. Context synthesis → 5. Answer generation
        """
        modalities = modalities or ["text", "image", "table", "code"]
        context = context or {}
        
        try:
            # Step 1: Query understanding and expansion
            expanded_query = await self._expand_query(query, context)
            
            # Step 2: Parallel multi-strategy retrieval
            dense_results, sparse_results, graph_results = await asyncio.gather(
                self._dense_retrieval(expanded_query, modalities, top_k * 2),
                self._sparse_retrieval(expanded_query, modalities, top_k * 2),
                self._graph_retrieval(expanded_query, top_k)
            )
            
            # Step 3: Fusion and reranking
            fused = self._fuse_results(dense_results, sparse_results, graph_results)
            reranked = await self._rerank(fused, query)
            
            # Step 4: Context synthesis
            synthesized = await self._synthesize_contexts(reranked[:top_k], query)
            
            # Step 5: Generate answer
            answer = await self._generate_answer(synthesized, query, context)
            
            return RAGResult(
                query=query,
                contexts=reranked[:top_k],
                synthesized_answer=answer,
                confidence=sum(c.relevance_score for c in reranked[:top_k]) / top_k,
                sources_used=list(set(c.source for c in reranked[:top_k]))
            )

        except Exception as e:
            logger.error(f"RAG failed: {e}")
            raise RAGError(f"Retrieval failed: {e}") from e

    async def _expand_query(self, query: str, context: Dict) -> str:
        """Expand query with synonyms and context."""
        try:
            expansion = await self.ag.nlp.expand_query(query, context.get("user_id"))
            return expansion
        except Exception:
            return query

    async def _dense_retrieval(
        self, query: str, modalities: List[str], k: int
    ) -> List[RetrievedContext]:
        """Embedding-based dense retrieval."""
        try:
            query_embedding = await self.embedder.embed(query)
            results = await self.ag.vector_store.search(
                vector=query_embedding,
                modalities=modalities,
                top_k=k
            )
            return [
                RetrievedContext(
                    content=r.get("content", ""),
                    modality=r.get("modality", "text"),
                    source=r.get("source", "unknown"),
                    relevance_score=r.get("score", 0.0),
                    metadata=r.get("metadata", {})
                )
                for r in results
            ]
        except Exception as e:
            logger.warning(f"Dense retrieval failed: {e}")
            return []

    async def _sparse_retrieval(
        self, query: str, modalities: List[str], k: int
    ) -> List[RetrievedContext]:
        """BM25/keyword-based sparse retrieval."""
        try:
            results = await self.ag.search.keyword_search(query, limit=k)
            return [
                RetrievedContext(
                    content=r.get("content", ""),
                    modality=r.get("modality", "text"),
                    source=r.get("source", "unknown"),
                    relevance_score=r.get("score", 0.0) * 0.9,  # Slight penalty vs dense
                    metadata=r.get("metadata", {})
                )
                for r in results
            ]
        except Exception as e:
            logger.warning(f"Sparse retrieval failed: {e}")
            return []

    async def _graph_retrieval(
        self, query: str, k: int
    ) -> List[RetrievedContext]:
        """Knowledge graph traversal retrieval."""
        try:
            # Find seed nodes in graph
            seed_nodes = await self.graph.find_nodes(query, limit=3)
            contexts = []
            for node in seed_nodes:
                neighbors = await self.graph.get_neighbors(node["id"], depth=2)
                for n in neighbors:
                    contexts.append(RetrievedContext(
                        content=n.get("description", ""),
                        modality="text",
                        source=f"kg:{n.get('id')}",
                        relevance_score=n.get("relevance", 0.7),
                        metadata={"graph_path": n.get("path", [])}
                    ))
            return contexts[:k]
        except Exception as e:
            logger.warning(f"Graph retrieval failed: {e}")
            return []

    def _fuse_results(
        self,
        dense: List[RetrievedContext],
        sparse: List[RetrievedContext],
        graph: List[RetrievedContext]
    ) -> List[RetrievedContext]:
        """Fuse results from multiple strategies using RRF."""
        from collections import defaultdict
        
        scores = defaultdict(float)
        contents = {}
        
        # Reciprocal Rank Fusion
        for rank, ctx in enumerate(dense):
            scores[(ctx.content, ctx.source)] += 1.0 / (rank + 60)
            contents[(ctx.content, ctx.source)] = ctx
        
        for rank, ctx in enumerate(sparse):
            scores[(ctx.content, ctx.source)] += 1.0 / (rank + 60)
            contents[(ctx.content, ctx.source)] = ctx
        
        for rank, ctx in enumerate(graph):
            scores[(ctx.content, ctx.source)] += 1.0 / (rank + 60)
            contents[(ctx.content, ctx.source)] = ctx
        
        # Update scores
        for key, ctx in contents.items():
            ctx.relevance_score = scores[key]
        
        return sorted(contents.values(), key=lambda x: x.relevance_score, reverse=True)

    async def _rerank(
        self, contexts: List[RetrievedContext], query: str
    ) -> List[RetrievedContext]:
        """Cross-encoder reranking."""
        try:
            reranked = await self.ag.rerank.rerank(
                query=query,
                documents=[c.content for c in contexts]
            )
            # Update scores
            for ctx, score in zip(contexts, reranked.get("scores", [])):
                ctx.relevance_score = score
            return sorted(contexts, key=lambda x: x.relevance_score, reverse=True)
        except Exception:
            return contexts

    async def _synthesize_contexts(
        self, contexts: List[RetrievedContext], query: str
    ) -> str:
        """Synthesize retrieved contexts into coherent context string."""
        parts = []
        for i, ctx in enumerate(contexts):
            parts.append(f"[{i+1}] Source: {ctx.source} (Score: {ctx.relevance_score:.2f})\n{ctx.content}")
        return "\n\n".join(parts)

    async def _generate_answer(
        self, context_str: str, query: str, user_context: Dict
    ) -> str:
        """Generate final answer with grounded context."""
        try:
            answer = await self.ag.generate.rag_answer(
                query=query,
                context=context_str,
                user_id=user_context.get("user_id")
            )
            return answer
        except Exception:
            # Fallback: return context summary
            return f"Based on retrieved information:\n\n{context_str[:1000]}..."


class RAGError(Exception):
    pass