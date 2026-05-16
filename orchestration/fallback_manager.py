import asyncio
from typing import Optional, Dict, Any, List, Callable, TypeVar
from dataclasses import dataclass
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

class FallbackStrategy(Enum):
    STATIC = "static"
    DEGRADED = "degraded"
    ALTERNATIVE = "alternative"
    QUEUE = "queue"
    REJECT = "reject"

@dataclass
class FallbackConfig:
    strategy: FallbackStrategy
    timeout_seconds: int = 30
    max_queue_size: int = 100
    degraded_response: Optional[Any] = None
    alternative_endpoint: Optional[str] = None

class FallbackManager:
    def __init__(self):
        self._fallbacks: Dict[str, FallbackConfig] = {}
        self._handlers: Dict[str, Callable] = {}
        self._queue: asyncio.Queue = asyncio.Queue()
        self._processing = False

    def register_fallback(
        self,
        service_name: str,
        config: FallbackConfig,
        handler: Optional[Callable] = None
    ) -> None:
        self._fallbacks[service_name] = config
        if handler:
            self._handlers[service_name] = handler
        logger.info(f"Fallback registered for {service_name}: {config.strategy.value}")

    async def execute_with_fallback(
        self,
        service_name: str,
        primary_func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        config = self._fallbacks.get(service_name)
        
        try:
            if config:
                return await asyncio.wait_for(
                    primary_func(*args, **kwargs),
                    timeout=config.timeout_seconds
                )
            return await primary_func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Primary failed for {service_name}: {str(e)}")
            
            if not config:
                raise
            
            return await self._apply_fallback(service_name, config, args, kwargs)

    async def _apply_fallback(
        self,
        service_name: str,
        config: FallbackConfig,
        args: tuple,
        kwargs: Dict[str, Any]
    ) -> Any:
        if config.strategy == FallbackStrategy.STATIC:
            return config.degraded_response
        
        elif config.strategy == FallbackStrategy.DEGRADED:
            return await self._degraded_response(service_name, args, kwargs)
        
        elif config.strategy == FallbackStrategy.ALTERNATIVE:
            return await self._alternative_endpoint(service_name, config, args, kwargs)
        
        elif config.strategy == FallbackStrategy.QUEUE:
            return await self._queue_request(service_name, args, kwargs)
        
        elif config.strategy == FallbackStrategy.REJECT:
            raise Exception(f"Service {service_name} unavailable - request rejected")

    async def _degraded_response(
        self,
        service_name: str,
        args: tuple,
        kwargs: Dict[str, Any]
    ) -> Any:
        handler = self._handlers.get(service_name)
        if handler:
            return await handler("degraded", *args, **kwargs)
        
        return {
            "status": "degraded",
            "service": service_name,
            "message": "Operating in degraded mode",
            "timestamp": datetime.utcnow().isoformat()
        }

    async def _alternative_endpoint(
        self,
        service_name: str,
        config: FallbackConfig,
        args: tuple,
        kwargs: Dict[str, Any]
    ) -> Any:
        if not config.alternative_endpoint:
            raise ValueError(f"No alternative endpoint configured for {service_name}")
        
        # Route to alternative
        logger.info(f"Routing to alternative: {config.alternative_endpoint}")
        return {
            "status": "routed",
            "endpoint": config.alternative_endpoint,
            "original_service": service_name
        }

    async def _queue_request(
        self,
        service_name: str,
        args: tuple,
        kwargs: Dict[str, Any]
    ) -> Any:
        if self._queue.qsize() >= self._fallbacks[service_name].max_queue_size:
            raise Exception(f"Queue full for {service_name}")
        
        await self._queue.put({
            "service": service_name,
            "args": args,
            "kwargs": kwargs,
            "timestamp": datetime.utcnow()
        })
        
        if not self._processing:
            asyncio.create_task(self._process_queue())
        
        return {
            "status": "queued",
            "position": self._queue.qsize(),
            "estimated_wait": self._queue.qsize() * 5
        }

    async def _process_queue(self):
        self._processing = True
        
        while not self._queue.empty():
            try:
                item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                # Process queued request
                logger.info(f"Processing queued request for {item['service']}")
            except asyncio.TimeoutError:
                break
        
        self._processing = False

    async def get_queue_status(self) -> Dict[str, Any]:
        return {
            "queue_size": self._queue.qsize(),
            "processing": self._processing,
            "max_size": max(
                cfg.max_queue_size for cfg in self._fallbacks.values()
                if cfg.strategy == FallbackStrategy.QUEUE
            ) if self._fallbacks else 0
        }