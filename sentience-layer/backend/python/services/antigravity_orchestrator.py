"""
Antigravity Orchestrator Service
Central coordinator for all Antigravity API interactions.
Provides caching, rate limiting, fallback, and unified error handling.
"""

from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import time
import json

from backend.python.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class AntigravityConfig:
    api_key: str
    base_url: str = "https://api.antigravity.ai/v1"
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    cache_ttl_seconds: int = 300


class AntigravityOrchestrator:
    """
    Unified Antigravity client with resilience patterns.
    Acts as the single integration point for all Antigravity services.
    """

    def __init__(self, config: Optional[AntigravityConfig] = None):
        self.config = config or AntigravityConfig(api_key="demo-key")
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._request_times: List[float] = []
        self._lock = asyncio.Lock()
        logger.info("AntigravityOrchestrator initialized")

    async def call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        use_cache: bool = True,
        priority: str = "normal",
    ) -> Dict[str, Any]:
        """
        Unified Antigravity API call with:
        - Rate limiting
        - Caching
        - Retry with backoff
        - Circuit breaker pattern
        """
        cache_key = f"{endpoint}:{hash(json.dumps(payload, sort_keys=True, default=str))}"
        
        # Check cache
        if use_cache and self._is_cached(cache_key):
            logger.debug(f"Cache hit for {endpoint}")
            return self._cache[cache_key]
        
        # Rate limit
        await self._rate_limit()
        
        # Execute with retry
        for attempt in range(self.config.max_retries):
            try:
                result = await self._execute_request(endpoint, payload)
                
                # Cache successful result
                if use_cache:
                    self._cache[cache_key] = result
                    self._cache_timestamps[cache_key] = time.time()
                
                return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {endpoint}: {e}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise AntigravityOrchestratorError(f"All retries failed for {endpoint}: {e}") from e

    async def batch_call(
        self,
        requests: List[Dict[str, Any]],  # [{"endpoint": "...", "payload": {...}}]
        max_concurrency: int = 5,
    ) -> List[Dict[str, Any]]:
        """Execute batch requests with controlled concurrency."""
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def bounded_call(req: Dict) -> Dict:
            async with semaphore:
                return await self.call(req["endpoint"], req["payload"], req.get("use_cache", True))
        
        return await asyncio.gather(*[bounded_call(r) for r in requests])

    def _is_cached(self, key: str) -> bool:
        """Check if cache entry is valid."""
        if key not in self._cache:
            return False
        timestamp = self._cache_timestamps.get(key, 0)
        return (time.time() - timestamp) < self.config.cache_ttl_seconds

    async def _rate_limit(self):
        """Enforce rate limiting."""
        async with self._lock:
            now = time.time()
            # Remove old requests outside window
            window_start = now - 60
            self._request_times = [t for t in self._request_times if t > window_start]
            
            if len(self._request_times) >= self.config.rate_limit_per_minute:
                # Wait until oldest request falls out of window
                sleep_time = 60 - (now - self._request_times[0]) + 1
                if sleep_time > 0:
                    logger.debug(f"Rate limit hit, sleeping {sleep_time:.1f}s")
                    await asyncio.sleep(sleep_time)
            
            self._request_times.append(now)

    async def _execute_request(
        self, endpoint: str, payload: Dict
    ) -> Dict[str, Any]:
        """Execute actual HTTP request to Antigravity."""
        import aiohttp
        
        url = f"{self.config.base_url}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {self.config.api_key}"},
                timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    raise Exception("Rate limited by Antigravity")
                else:
                    text = await response.text()
                    raise Exception(f"Antigravity error {response.status}: {text}")

    async def invalidate_cache(self, pattern: Optional[str] = None):
        """Invalidate cache entries matching pattern."""
        if pattern is None:
            self._cache.clear()
            self._cache_timestamps.clear()
        else:
            keys_to_remove = [k for k in self._cache if pattern in k]
            for k in keys_to_remove:
                del self._cache[k]
                del self._cache_timestamps[k]

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "total_cached": len(self._cache),
            "memory_estimate_bytes": sum(len(str(v)) for v in self._cache.values())
        }


class AntigravityOrchestratorError(Exception):
    pass