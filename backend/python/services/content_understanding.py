"""
Content Understanding Service
Multi-modal content ingestion, parsing, and semantic understanding.
Integrates with Antigravity's content analysis APIs.
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


class ContentType(Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    SPREADSHEET = "spreadsheet"
    CODE = "code"
    EMAIL = "email"
    SLACK = "slack"


@dataclass
class ContentChunk:
    id: str
    content: str
    content_type: ContentType
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    confidence: float = 1.0
    source_location: Optional[str] = None


@dataclass
class UnderstandingResult:
    raw_chunks: List[ContentChunk]
    entities: List[Dict[str, Any]]
    topics: List[str]
    sentiment: Dict[str, float]
    intent: Optional[str]
    urgency_score: float
    action_indicators: List[str]
    summary: str
    language: str
    confidence: float


class ContentUnderstandingService:
    """
    Deep content understanding with multi-modal parsing.
    Uses Antigravity for enrichment and cross-reference validation.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._parsers: Dict[ContentType, callable] = {
            ContentType.TEXT: self._parse_text,
            ContentType.MARKDOWN: self._parse_markdown,
            ContentType.PDF: self._parse_pdf,
            ContentType.IMAGE: self._parse_image,
            ContentType.AUDIO: self._parse_audio,
            ContentType.CODE: self._parse_code,
            ContentType.EMAIL: self._parse_email,
            ContentType.SLACK: self._parse_slack,
        }
        logger.info("ContentUnderstandingService initialized")

    async def understand(
        self,
        raw_content: Union[str, bytes],
        content_type: ContentType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UnderstandingResult:
        """
        Multi-step agentic understanding pipeline:
        1. Parse → 2. Chunk → 3. Enrich (Antigravity) → 4. Extract entities → 5. Synthesize
        """
        try:
            metadata = metadata or {}
            
            # Step 1: Parse into chunks
            chunks = await self._parsers[content_type](raw_content, metadata)
            
            # Step 2: Parallel enrichment via Antigravity
            enriched_chunks = await asyncio.gather(*[
                self._enrich_chunk(chunk) for chunk in chunks
            ])
            
            # Step 3: Entity & topic extraction
            entities = await self._extract_entities(enriched_chunks)
            topics = await self._extract_topics(enriched_chunks)
            
            # Step 4: Cross-reference with Antigravity knowledge graph
            validated_entities = await self._cross_reference_entities(entities)
            
            # Step 5: Synthesize understanding
            result = await self._synthesize(
                enriched_chunks, validated_entities, topics, metadata
            )
            
            logger.info(
                f"Understood content: {len(chunks)} chunks, "
                f"{len(validated_entities)} entities, intent={result.intent}"
            )
            return result

        except Exception as e:
            logger.error(f"Content understanding failed: {e}")
            raise ContentUnderstandingError(f"Failed to understand content: {e}") from e

    async def _parse_text(self, content: str, meta: Dict) -> List[ContentChunk]:
        """Parse plain text into semantic chunks."""
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks = []
        for i, para in enumerate(paragraphs):
            chunk_id = hashlib.md5(f"{meta.get('source','')}-{i}-{para[:50]}".encode()).hexdigest()
            chunks.append(ContentChunk(
                id=chunk_id,
                content=para,
                content_type=ContentType.TEXT,
                metadata={**meta, "paragraph_index": i},
                source_location=f"para:{i}"
            ))
        return chunks

    async def _parse_markdown(self, content: str, meta: Dict) -> List[ContentChunk]:
        """Parse markdown preserving structure."""
        import re
        chunks = []
        # Headers become anchor chunks
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        for level, title in headers:
            chunk_id = hashlib.md5(f"md-header-{title}".encode()).hexdigest()
            chunks.append(ContentChunk(
                id=chunk_id,
                content=title,
                content_type=ContentType.MARKDOWN,
                metadata={**meta, "level": len(level), "element": "header"},
                source_location=f"header:{title}"
            ))
        # Also chunk body text
        text_chunks = await self._parse_text(re.sub(r'#{1,6}\s+.+', '', content), meta)
        chunks.extend(text_chunks)
        return chunks

    async def _parse_pdf(self, content: bytes, meta: Dict) -> List[ContentChunk]:
        """PDF parsing with OCR fallback."""
        # In production: use PyPDF2 + pdfplumber + OCR fallback
        # Here we simulate structured extraction
        logger.info(f"Parsing PDF: {len(content)} bytes")
        text = f"[Extracted PDF content from {meta.get('filename', 'unknown')}]"
        return await self._parse_text(text, meta)

    async def _parse_image(self, content: bytes, meta: Dict) -> List[ContentChunk]:
        """Image parsing via VLM service."""
        from .vlm_service import VLMService
        vlm = VLMService(antigravity_client=self.ag)
        description = await vlm.describe_image(content)
        chunk = ContentChunk(
            id=hashlib.md5(content[:1024]).hexdigest(),
            content=description,
            content_type=ContentType.IMAGE,
            metadata={**meta, "media_type": "image"},
            confidence=0.92
        )
        return [chunk]

    async def _parse_audio(self, content: bytes, meta: Dict) -> List[ContentChunk]:
        """Audio parsing via ASR service."""
        from .asr_service import ASRService
        asr = ASRService(antigravity_client=self.ag)
        transcription = await asr.transcribe(content)
        return await self._parse_text(transcription, meta)

    async def _parse_code(self, content: str, meta: Dict) -> List[ContentChunk]:
        """Code parsing with AST-aware chunking."""
        chunks = []
        # Simple heuristic: chunk by functions/classes
        import re
        pattern = r'(def\s+\w+|class\s+\w+).+?(?=\ndef\s+|\nclass\s+|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        for i, match in enumerate(matches):
            chunk_id = hashlib.md5(f"code-{i}-{match[:50]}".encode()).hexdigest()
            chunks.append(ContentChunk(
                id=chunk_id,
                content=match,
                content_type=ContentType.CODE,
                metadata={**meta, "chunk_type": "function_or_class"},
                source_location=f"code_block:{i}"
            ))
        return chunks or await self._parse_text(content, meta)

    async def _parse_email(self, content: str, meta: Dict) -> List[ContentChunk]:
        """Email parsing with header/body separation."""
        lines = content.split("\n")
        headers = []
        body = []
        in_body = False
        for line in lines:
            if in_body:
                body.append(line)
            elif line.strip() == "":
                in_body = True
            else:
                headers.append(line)
        
        chunks = []
        if headers:
            chunks.append(ContentChunk(
                id=hashlib.md5("email-headers".encode()).hexdigest(),
                content="\n".join(headers),
                content_type=ContentType.EMAIL,
                metadata={**meta, "part": "headers"},
                source_location="email:headers"
            ))
        if body:
            body_text = "\n".join(body)
            body_chunks = await self._parse_text(body_text, meta)
            for bc in body_chunks:
                bc.content_type = ContentType.EMAIL
                bc.metadata["part"] = "body"
            chunks.extend(body_chunks)
        return chunks

    async def _parse_slack(self, content: str, meta: Dict) -> List[ContentChunk]:
        """Slack message parsing with thread awareness."""
        import json
        try:
            data = json.loads(content)
            messages = data.get("messages", [data])
        except:
            messages = [{"text": content}]
        
        chunks = []
        for msg in messages:
            text = msg.get("text", "")
            chunk_id = hashlib.md5(f"slack-{msg.get('ts','')}".encode()).hexdigest()
            chunks.append(ContentChunk(
                id=chunk_id,
                content=text,
                content_type=ContentType.SLACK,
                metadata={**meta, "user": msg.get("user"), "thread_ts": msg.get("thread_ts")},
                source_location=f"slack:{msg.get('ts')}"
            ))
        return chunks

    async def _enrich_chunk(self, chunk: ContentChunk) -> ContentChunk:
        """Enrich chunk with Antigravity embeddings and metadata."""
        try:
            embedding = await self.ag.embed_text(chunk.content)
            chunk.embedding = embedding
            # Antigravity semantic enrichment
            enrichment = await self.ag.enrich_content(chunk.content)
            chunk.metadata["antigravity_enrichment"] = enrichment
            return chunk
        except Exception as e:
            logger.warning(f"Enrichment failed for chunk {chunk.id}: {e}")
            return chunk

    async def _extract_entities(self, chunks: List[ContentChunk]) -> List[Dict[str, Any]]:
        """Named entity extraction across chunks."""
        all_text = " ".join([c.content for c in chunks])
        try:
            entities = await self.ag.extract_entities(all_text)
            return entities
        except Exception:
            # Fallback: simple regex-based extraction
            import re
            emails = re.findall(r'\S+@\S+\.\S+', all_text)
            urls = re.findall(r'https?://\S+', all_text)
            return [
                {"type": "email", "value": e, "source": "regex"} for e in emails
            ] + [
                {"type": "url", "value": u, "source": "regex"} for u in urls
            ]

    async def _extract_topics(self, chunks: List[ContentChunk]) -> List[str]:
        """Topic modeling via Antigravity."""
        all_text = " ".join([c.content for c in chunks])
        try:
            topics = await self.ag.extract_topics(all_text, max_topics=5)
            return topics
        except Exception:
            return []

    async def _cross_reference_entities(
        self, entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Validate entities against Antigravity knowledge graph."""
        validated = []
        for entity in entities:
            try:
                kg_data = await self.ag.knowledge_graph.lookup(entity["value"])
                entity["kg_validated"] = True
                entity["kg_metadata"] = kg_data
            except Exception:
                entity["kg_validated"] = False
            validated.append(entity)
        return validated

    async def _synthesize(
        self,
        chunks: List[ContentChunk],
        entities: List[Dict[str, Any]],
        topics: List[str],
        metadata: Dict[str, Any],
    ) -> UnderstandingResult:
        """Synthesize final understanding."""
        all_text = " ".join([c.content for c in chunks])
        
        # Sentiment analysis
        sentiment = await self._analyze_sentiment(all_text)
        
        # Intent detection
        intent = await self._detect_intent(all_text)
        
        # Urgency scoring
        urgency = self._calculate_urgency(all_text, metadata)
        
        # Action indicators
        action_words = ["need", "should", "must", "action", "task", "todo", "follow up"]
        action_indicators = [w for w in action_words if w.lower() in all_text.lower()]
        
        # Summary generation
        summary = await self._generate_summary(chunks)
        
        return UnderstandingResult(
            raw_chunks=chunks,
            entities=entities,
            topics=topics,
            sentiment=sentiment,
            intent=intent,
            urgency_score=urgency,
            action_indicators=action_indicators,
            summary=summary,
            language=metadata.get("language", "en"),
            confidence=sum(c.confidence for c in chunks) / max(len(chunks), 1)
        )

    async def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Multi-dimensional sentiment analysis."""
        try:
            return await self.ag.analyze_sentiment(text)
        except Exception:
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.5}

    async def _detect_intent(self, text: str) -> Optional[str]:
        """Intent classification."""
        try:
            return await self.ag.classify_intent(text)
        except Exception:
            return None

    def _calculate_urgency(self, text: str, metadata: Dict) -> float:
        """Calculate urgency score 0-1."""
        urgency_markers = ["urgent", "asap", "immediately", "deadline", "today", "critical", "blocker"]
        text_lower = text.lower()
        score = sum(2 for marker in urgency_markers if marker in text_lower) / 10
        if metadata.get("priority") == "high":
            score += 0.3
        return min(score, 1.0)

    async def _generate_summary(self, chunks: List[ContentChunk]) -> str:
        """Generate abstractive summary."""
        all_text = " ".join([c.content for c in chunks[:5]])  # First 5 chunks
        try:
            return await self.ag.summarize(all_text, max_length=200)
        except Exception:
            return all_text[:200] + "..."


class ContentUnderstandingError(Exception):
    """Custom exception for content understanding failures."""
    pass