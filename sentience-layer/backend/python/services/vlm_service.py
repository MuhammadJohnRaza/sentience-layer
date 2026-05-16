"""
VLM Service
Vision Language Model for image understanding, description, and reasoning.
Uses Antigravity's multimodal capabilities for visual intelligence.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class ImageDescription:
    caption: str
    detailed_description: str
    objects: List[Dict[str, Any]]
    scenes: List[str]
    activities: List[str]
    text_found: List[str]
    colors: List[str]
    mood: Optional[str]
    confidence: float


@dataclass
class VisualQAResult:
    question: str
    answer: str
    confidence: float
    reasoning: Optional[str]
    relevant_regions: List[Dict[str, Any]] = field(default_factory=list)


class VLMService:
    """
    Vision-Language integration for comprehensive image understanding.
    Uses Antigravity for state-of-the-art visual reasoning.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("VLMService initialized")

    async def describe_image(
        self,
        image_bytes: bytes,
        detail_level: str = "standard",  # brief, standard, detailed
        context: Optional[Dict[str, Any]] = None,
    ) -> ImageDescription:
        """
        Agentic image description:
        1. Object detection → 2. Scene classification → 3. Activity recognition →
        4. OCR for text → 5. Aesthetic analysis → 6. Synthesis
        """
        context = context or {}
        
        try:
            # Parallel visual analysis via Antigravity
            objects, scene, text, aesthetic = await self.ag.vision.analyze(
                image_bytes,
                tasks=["objects", "scene", "text", "aesthetic"],
                detail=detail_level
            )
            
            # Synthesize description
            caption = await self.ag.vision.generate_caption(
                image_bytes,
                objects=objects,
                scene=scene
            )
            
            return ImageDescription(
                caption=caption,
                detailed_description=self._generate_detailed_description(objects, scene, text),
                objects=objects.get("objects", []),
                scenes=scene.get("scenes", []),
                activities=scene.get("activities", []),
                text_found=text.get("text", []),
                colors=aesthetic.get("colors", []),
                mood=aesthetic.get("mood"),
                confidence=min(
                    objects.get("confidence", 0.9),
                    scene.get("confidence", 0.9),
                    0.95
                )
            )

        except Exception as e:
            logger.error(f"Image description failed: {e}")
            raise VLMServiceError(f"Description failed: {e}") from e

    async def visual_qa(
        self,
        image_bytes: bytes,
        question: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> VisualQAResult:
        """
        Visual Question Answering with attention mapping.
        """
        try:
            result = await self.ag.vision.visual_qa(image_bytes, question)
            
            return VisualQAResult(
                question=question,
                answer=result.get("answer", ""),
                confidence=result.get("confidence", 0.8),
                reasoning=result.get("reasoning"),
                relevant_regions=result.get("attention_regions", [])
            )
        except Exception as e:
            logger.error(f"Visual QA failed: {e}")
            raise VLMServiceError(f"QA failed: {e}") from e

    async def compare_images(
        self,
        image1: bytes,
        image2: bytes,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Compare two images and identify differences/similarities.
        """
        try:
            comparison = await self.ag.vision.compare(image1, image2)
            return {
                "similarity_score": comparison.get("similarity", 0.0),
                "differences": comparison.get("differences", []),
                "common_elements": comparison.get("common", []),
                "confidence": comparison.get("confidence", 0.8)
            }
        except Exception as e:
            raise VLMServiceError(f"Comparison failed: {e}") from e

    def _generate_detailed_description(
        self, objects: Dict, scene: Dict, text: Dict
    ) -> str:
        """Generate rich textual description from visual elements."""
        parts = []
        
        if scene.get("scenes"):
            parts.append(f"Scene: {', '.join(scene['scenes'])}")
        
        if objects.get("objects"):
            obj_desc = ", ".join([
                f"{o.get('name', 'object')} ({o.get('confidence', 0):.0%})"
                for o in objects["objects"][:5]
            ])
            parts.append(f"Objects: {obj_desc}")
        
        if scene.get("activities"):
            parts.append(f"Activities: {', '.join(scene['activities'])}")
        
        if text.get("text"):
            parts.append(f"Text visible: {'; '.join(text['text'][:3])}")
        
        return ". ".join(parts) if parts else "Image analysis complete."


class VLMServiceError(Exception):
    pass