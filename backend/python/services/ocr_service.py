"""
OCR Service
Optical Character Recognition with layout preservation.
Uses Antigravity for document intelligence and handwriting recognition.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import io

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class OCRResult:
    text: str
    confidence: float
    blocks: List[Dict[str, Any]]
    language: str
    layout_type: str  # single_column, multi_column, form, table, mixed
    tables: List[List[List[str]]]  # Extracted tables
    images_described: List[str]  # Alt text for images in document


@dataclass
class OCRBlock:
    text: str
    bbox: Dict[str, float]  # x, y, width, height
    confidence: float
    block_type: str  # paragraph, heading, table, image, list_item
    font_size: Optional[int] = None
    is_bold: bool = False
    is_italic: bool = False


class OCRService:
    """
    Advanced OCR with layout analysis and table extraction.
    Integrates with Antigravity for enterprise document understanding.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("OCRService initialized")

    async def recognize(
        self,
        image_bytes: bytes,
        options: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> OCRResult:
        """
        Agentic OCR pipeline:
        1. Preprocessing → 2. Text detection → 3. Recognition → 4. Layout analysis →
        5. Table extraction → 6. Post-processing
        """
        options = options or {}
        context = context or {}
        
        try:
            # Step 1: Preprocess image
            preprocessed = await self._preprocess(image_bytes, options)
            
            # Step 2-3: Recognize text via Antigravity
            raw_result = await self.ag.vision.ocr(preprocessed, options)
            
            # Step 4: Layout analysis
            layout = await self._analyze_layout(raw_result)
            
            # Step 5: Table extraction
            tables = await self._extract_tables(preprocessed, raw_result)
            
            # Step 6: Post-process and validate
            validated = await self._post_process(raw_result, layout, tables)
            
            logger.info(f"OCR complete: {len(validated.text)} chars, {len(tables)} tables")
            return validated

        except Exception as e:
            logger.error(f"OCR failed: {e}")
            raise OCRServiceError(f"Recognition failed: {e}") from e

    async def _preprocess(
        self, image_bytes: bytes, options: Dict
    ) -> bytes:
        """Image preprocessing for optimal OCR."""
        # In production: deskew, denoise, binarization
        # Here we pass through
        return image_bytes

    async def _analyze_layout(self, raw_result: Dict) -> str:
        """Determine document layout type."""
        blocks = raw_result.get("blocks", [])
        if len(blocks) < 3:
            return "single_column"
        
        # Analyze block positions
        x_positions = [b.get("bbox", {}).get("x", 0) for b in blocks]
        unique_x = len(set(round(x, 1) for x in x_positions))
        
        if unique_x > 2:
            return "multi_column"
        elif any(b.get("type") == "table" for b in blocks):
            return "table"
        else:
            return "mixed"

    async def _extract_tables(
        self, image_bytes: bytes, raw_result: Dict
    ) -> List[List[List[str]]]:
        """Extract table structures from image."""
        try:
            tables = await self.ag.vision.extract_tables(image_bytes)
            return tables
        except Exception:
            return []

    async def _post_process(
        self,
        raw: Dict,
        layout: str,
        tables: List[List[List[str]]]
    ) -> OCRResult:
        """Post-process and validate OCR output."""
        blocks = [
            OCRBlock(
                text=b.get("text", ""),
                bbox=b.get("bbox", {}),
                confidence=b.get("confidence", 0.9),
                block_type=b.get("type", "paragraph"),
                font_size=b.get("font_size"),
                is_bold=b.get("bold", False),
                is_italic=b.get("italic", False)
            )
            for b in raw.get("blocks", [])
        ]
        
        full_text = "\n\n".join(b.text for b in blocks)
        
        # Generate image descriptions
        image_desc = []
        for b in blocks:
            if b.block_type == "image":
                try:
                    desc = await self.ag.vision.describe_image_region(b.bbox)
                    image_desc.append(desc)
                except Exception:
                    image_desc.append("[Image]")
        
        return OCRResult(
            text=full_text,
            confidence=sum(b.confidence for b in blocks) / max(len(blocks), 1),
            blocks=[b.__dict__ for b in blocks],
            language=raw.get("language", "unknown"),
            layout_type=layout,
            tables=tables,
            images_described=image_desc
        )

    async def batch_recognize(
        self,
        images: List[bytes],
        options: Optional[Dict] = None,
        context: Optional[Dict] = None,
    ) -> List[OCRResult]:
        """Batch OCR with parallel processing."""
        import asyncio
        return await asyncio.gather(*[
            self.recognize(img, options, context) for img in images
        ])


class OCRServiceError(Exception):
    pass