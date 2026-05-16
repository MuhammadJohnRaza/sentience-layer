"""
Recovery Engine Service
Handles failures with intelligent retry, fallback, and state recovery.
Uses Antigravity for resilience patterns and chaos engineering.
"""

from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


class RecoveryStrategy(Enum):
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAK = "circuit_break"
    DEGRADE = "degrade"
    ESCALATE = "escalate"
    IGNORE = "ignore"


@dataclass
class RecoveryResult:
    success: bool
    strategy_used: RecoveryStrategy
    attempts: int
    final_state: Dict[str, Any]
    error_log: List[str] = field(default_factory=list)
    recovery_time_ms: int = 0


class RecoveryEngineService:
    """
    Intelligent failure recovery with adaptive strategies.
    Integrates with Antigravity for resilience monitoring.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        self._circuit_states: Dict[str, str] = {}  # service -> closed/open/half-open
        self._failure_counts: Dict[str, int] = {}
        logger.info("RecoveryEngineService initialized")

    async def execute_with_recovery(
        self,
        operation: Callable,
        operation_name: str,
        args: Optional[List] = None,
        kwargs: Optional[Dict] = None,
        max_retries: int = 3,
        fallback: Optional[Callable] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> RecoveryResult:
        """
        Agentic recovery execution:
        1. Pre-check circuit breaker → 2. Execute with retry → 3. Fallback if needed →
        4. Post-execution validation → 5. Circuit state update
        """
        args = args or []
        kwargs = kwargs or {}
        context = context or {}
        start_time = time.time()
        errors = []
        
        try:
            # Step 1: Check circuit breaker
            if self._circuit_states.get(operation_name) == "open":
                logger.warning(f"Circuit open for {operation_name}, using fallback")
                if fallback:
                    result = await fallback(*args, **kwargs)
                    return RecoveryResult(
                        success=True,
                        strategy_used=RecoveryStrategy.FALLBACK,
                        attempts=0,
                        final_state={"result": result},
                        recovery_time_ms=int((time.time() - start_time) * 1000)
                    )
                else:
                    raise RecoveryError(f"Circuit open and no fallback for {operation_name}")
            
            # Step 2: Execute with retry
            for attempt in range(max_retries):
                try:
                    result = await operation(*args, **kwargs)
                    
                    # Success: reset failure count
                    self._failure_counts[operation_name] = 0
                    
                    # Validate result
                    if await self._validate_result(result, context):
                        return RecoveryResult(
                            success=True,
                            strategy_used=RecoveryStrategy.RETRY if attempt > 0 else RecoveryStrategy.IGNORE,
                            attempts=attempt + 1,
                            final_state={"result": result},
                            error_log=errors,
                            recovery_time_ms=int((time.time() - start_time) * 1000)
                        )
                    else:
                        raise ValueError("Result validation failed")
                        
                except Exception as e:
                    errors.append(str(e))
                    logger.warning(f"Attempt {attempt + 1} failed for {operation_name}: {e}")
                    
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait = (2 ** attempt) + (hash(operation_name) % 1000 / 1000)
                        await asyncio.sleep(wait)
                    else:
                        # Max retries reached
                        self._failure_counts[operation_name] = self._failure_counts.get(operation_name, 0) + 1
                        
                        # Check if circuit should open
                        if self._failure_counts[operation_name] >= 5:
                            self._circuit_states[operation_name] = "open"
                            logger.error(f"Circuit opened for {operation_name}")
            
            # Step 3: Fallback
            if fallback:
                logger.info(f"Executing fallback for {operation_name}")
                result = await fallback(*args, **kwargs)
                return RecoveryResult(
                    success=True,
                    strategy_used=RecoveryStrategy.FALLBACK,
                    attempts=max_retries,
                    final_state={"result": result},
                    error_log=errors,
                    recovery_time_ms=int((time.time() - start_time) * 1000)
                )
            
            # Step 4: Degrade or escalate
            return await self._handle_final_failure(
                operation_name, errors, context, start_time
            )

        except Exception as e:
            logger.error(f"Recovery failed for {operation_name}: {e}")
            raise RecoveryError(f"Recovery failed: {e}") from e

    async def _validate_result(
        self, result: Any, context: Dict
    ) -> bool:
        """Validate operation result."""
        try:
            validation = await self.ag.resilience.validate_result(result, context)
            return validation.get("valid", True)
        except Exception:
            return True

    async def _handle_final_failure(
        self,
        operation_name: str,
        errors: List[str],
        context: Dict,
        start_time: float
    ) -> RecoveryResult:
        """Handle case where all retries and fallback failed."""
        try:
            # Try graceful degradation
            degraded = await self._degrade_operation(operation_name, context)
            if degraded:
                return RecoveryResult(
                    success=True,
                    strategy_used=RecoveryStrategy.DEGRADE,
                    attempts=len(errors),
                    final_state={"degraded": True, "result": degraded},
                    error_log=errors,
                    recovery_time_ms=int((time.time() - start_time) * 1000)
                )
        except Exception:
            pass
        
        # Final: escalate
        try:
            await self.ag.alerts.escalate(
                operation=operation_name,
                errors=errors,
                severity="critical"
            )
        except Exception:
            pass
        
        return RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.ESCALATE,
            attempts=len(errors),
            final_state={},
            error_log=errors,
            recovery_time_ms=int((time.time() - start_time) * 1000)
        )

    async def _degrade_operation(
        self, operation_name: str, context: Dict
    ) -> Optional[Any]:
        """Attempt graceful degradation."""
        try:
            degraded = await self.ag.resilience.get_degraded_mode(
                operation_name,
                context
            )
            return degraded
        except Exception:
            return None

    async def reset_circuit(self, operation_name: str):
        """Manually reset circuit breaker."""
        self._circuit_states[operation_name] = "closed"
        self._failure_counts[operation_name] = 0
        logger.info(f"Circuit reset for {operation_name}")


class RecoveryError(Exception):
    pass