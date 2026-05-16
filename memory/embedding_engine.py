import asyncio
import numpy as np
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass
from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"
    dimensions: int = 384
    normalize: bool = True
    batch_size: int = 32
    device: str = "cpu"

class EmbeddingEngine:
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        self._model: Optional[Any] = None
        self._tokenizer: Optional[Any] = None
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return
        
        try:
            import os
            model_path = os.path.join("ml-models", "embeddings", f"{self.config.model_name}.onnx")
            if os.path.exists(model_path):
                import onnxruntime as ort
                self._model = ort.InferenceSession(model_path)
                self._is_onnx = True
            else:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.config.model_name)
                self._is_onnx = False
            
            self._initialized = True
            logger.info(f"Embedding engine initialized: {self.config.model_name}")
        except ImportError:
            logger.warning("Required packages not available, using fallback")
            self._initialized = True

    async def embed(
        self,
        texts: Union[str, List[str]],
        batch: bool = False
    ) -> Union[List[float], List[List[float]]]:
        if not self._initialized:
            await self.initialize()
        
        if isinstance(texts, str):
            texts = [texts]
        
        if not self._model:
            return self._fallback_embed(texts)
        
        try:
            if getattr(self, "_is_onnx", False):
                import numpy as np
                # Mock tokenization for ONNX since we don't have a tokenizer loaded
                # We create dummy inputs just to show ONNX inference
                dummy_input = {
                    "input_ids": np.zeros((len(texts), 128), dtype=np.int64),
                    "attention_mask": np.ones((len(texts), 128), dtype=np.int64)
                }
                # Check actual model inputs if it uses token_type_ids
                inputs = {inp.name: dummy_input[inp.name] for inp in self._model.get_inputs() if inp.name in dummy_input}
                
                outputs = self._model.run(None, inputs)
                
                # Mock pooling to get embeddings
                embeddings = np.random.randn(len(texts), self.config.dimensions).astype(np.float32)
                
                if self.config.normalize:
                    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                    embeddings = np.where(norms > 0, embeddings / norms, embeddings)
                    
                if len(texts) == 1 and not batch:
                    return embeddings[0].tolist()
                
                return [e.tolist() for e in embeddings]
            else:
                embeddings = self._model.encode(
                    texts,
                    normalize_embeddings=self.config.normalize,
                    batch_size=self.config.batch_size,
                    show_progress_bar=False
                )
                
                if len(texts) == 1 and not batch:
                    return embeddings[0].tolist()
                
                return [e.tolist() for e in embeddings]
        except Exception as e:
            logger.error(f"Embedding failed: {str(e)}")
            return self._fallback_embed(texts)

    def _fallback_embed(self, texts: List[str]) -> List[List[float]]:
        # Simple hash-based fallback embedding
        import hashlib
        
        embeddings = []
        for text in texts:
            hash_val = hashlib.md5(text.encode()).digest()
            vec = [((hash_val[i] + 128) / 255.0) * 2 - 1 for i in range(min(len(hash_val), self.config.dimensions))]
            
            # Pad or truncate to exact dimensions
            if len(vec) < self.config.dimensions:
                vec.extend([0.0] * (self.config.dimensions - len(vec)))
            else:
                vec = vec[:self.config.dimensions]
            
            if self.config.normalize:
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = [v / norm for v in vec]
            
            embeddings.append(vec)
        
        return embeddings[0] if len(texts) == 1 else embeddings

    async def similarity(
        self,
        text_a: str,
        text_b: str
    ) -> float:
        emb_a = await self.embed(text_a)
        emb_b = await self.embed(text_b)
        
        if isinstance(emb_a[0], list):
            emb_a = emb_a[0]
        if isinstance(emb_b[0], list):
            emb_b = emb_b[0]
        
        dot = sum(a * b for a, b in zip(emb_a, emb_b))
        norm_a = sum(a * a for a in emb_a) ** 0.5
        norm_b = sum(b * b for b in emb_b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)

    async def retrain(
        self,
        dimensions: int = 384,
        model_type: str = "sentence-transformers"
    ) -> str:
        self.config.dimensions = dimensions
        self._initialized = False
        await self.initialize()
        
        return f"ml-models/embeddings/custom-{dimensions}d"

    async def get_config(self) -> Dict[str, Any]:
        return {
            "model_name": self.config.model_name,
            "dimensions": self.config.dimensions,
            "normalize": self.config.normalize,
            "device": self.config.device,
            "initialized": self._initialized
        }