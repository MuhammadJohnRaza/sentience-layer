import asyncio
import random
from typing import Optional, Callable, TypeVar
from abc import ABC, abstractmethod
from dataclasses import dataclass

from utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: tuple = (Exception,)

class RetryPolicy(ABC):
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()

    @abstractmethod
    def calculate_delay(self, attempt: int) -> float:
        pass

    async def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            except self.config.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.config.max_retries:
                    logger.error(f"All retries exhausted: {str(e)}")
                    raise last_exception
                
                delay = self.calculate_delay(attempt)
                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {str(e)}"
                )
                await asyncio.sleep(delay)
        
        raise last_exception if last_exception else Exception("Retry failed")

class ExponentialBackoff(RetryPolicy):
    def calculate_delay(self, attempt: int) -> float:
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        
        if self.config.jitter:
            delay *= random.uniform(0.5, 1.5)
        
        return min(delay, self.config.max_delay)

class LinearBackoff(RetryPolicy):
    def calculate_delay(self, attempt: int) -> float:
        delay = self.config.base_delay * (attempt + 1)
        
        if self.config.jitter:
            delay *= random.uniform(0.8, 1.2)
        
        return min(delay, self.config.max_delay)

class FixedDelay(RetryPolicy):
    def __init__(self, fixed_delay: float, config: Optional[RetryConfig] = None):
        super().__init__(config)
        self.fixed_delay = fixed_delay

    def calculate_delay(self, attempt: int) -> float:
        delay = self.fixed_delay
        
        if self.config.jitter:
            delay *= random.uniform(0.9, 1.1)
        
        return min(delay, self.config.max_delay)

class CircuitBreakerRetry(RetryPolicy):
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        config: Optional[RetryConfig] = None
    ):
        super().__init__(config)
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failures = 0
        self._last_failure_time: Optional[float] = None
        self._state = "closed"

    def calculate_delay(self, attempt: int) -> float:
        if self._state == "open":
            if self._last_failure_time:
                elapsed = asyncio.get_event_loop().time() - self._last_failure_time
                if elapsed >= self.recovery_timeout:
                    self._state = "half-open"
                    self._failures = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        return min(delay, self.config.max_delay)

    async def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        try:
            result = await super().execute(func, *args, **kwargs)
            
            if self._state == "half-open":
                self._state = "closed"
                self._failures = 0
            
            return result
            
        except Exception as e:
            self._failures += 1
            self._last_failure_time = asyncio.get_event_loop().time()
            
            if self._failures >= self.failure_threshold:
                self._state = "open"
                logger.error(f"Circuit breaker OPENED after {self._failures} failures")
            
            raise