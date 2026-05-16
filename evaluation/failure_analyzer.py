import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

class FailureCategory(Enum):
    TIMEOUT = "timeout"
    EXCEPTION = "exception"
    VALIDATION = "validation"
    RESOURCE = "resource"
    DEPENDENCY = "dependency"
    LOGIC = "logic"
    SECURITY = "security"
    UNKNOWN = "unknown"

@dataclass
class FailureReport:
    failure_id: str
    execution_id: str
    category: FailureCategory
    root_cause: str
    stack_trace: Optional[str] = None
    recovery_suggested: bool = False
    recovery_strategy: Optional[str] = None
    similar_failures: List[str] = field(default_factory=list)
    frequency: int = 1
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)

class FailureAnalyzer:
    def __init__(self):
        self._failure_patterns: Dict[str, List[Dict[str, Any]]] = {}
        self._reports: Dict[str, FailureReport] = {}
        self._max_patterns: int = 1000

    async def analyze(
        self,
        execution_id: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> FailureReport:
        error_type = type(error).__name__
        error_message = str(error)
        
        category = self._classify_error(error_type, error_message)
        root_cause = await self._identify_root_cause(error, context)
        pattern_key = f"{category.value}:{error_type}:{hash(error_message) % 10000}"
        
        if pattern_key in self._failure_patterns:
            self._failure_patterns[pattern_key].append({
                "execution_id": execution_id,
                "timestamp": datetime.utcnow(),
                "context": context
            })
            
            if len(self._failure_patterns[pattern_key]) > self._max_patterns:
                self._failure_patterns[pattern_key] = self._failure_patterns[pattern_key][-self._max_patterns:]
        else:
            self._failure_patterns[pattern_key] = [{
                "execution_id": execution_id,
                "timestamp": datetime.utcnow(),
                "context": context
            }]
        
        similar = self._find_similar_failures(pattern_key, execution_id)
        
        recovery = await self._suggest_recovery(category, root_cause)
        
        report = FailureReport(
            failure_id=f"fail_{hash(str(error))}",
            execution_id=execution_id,
            category=category,
            root_cause=root_cause,
            stack_trace=self._extract_stack_trace(error),
            recovery_suggested=recovery is not None,
            recovery_strategy=recovery,
            similar_failures=[s["execution_id"] for s in similar[:5]],
            frequency=len(self._failure_patterns[pattern_key]),
            last_seen=datetime.utcnow()
        )
        
        if pattern_key in self._reports:
            existing = self._reports[pattern_key]
            report.first_seen = existing.first_seen
            report.frequency = existing.frequency + 1
        
        self._reports[pattern_key] = report
        
        logger.error(f"Failure analyzed: {report.failure_id} - {category.value}: {root_cause}")
        return report

    def _classify_error(self, error_type: str, message: str) -> FailureCategory:
        timeout_keywords = ["timeout", "timed out", "deadline", "expired"]
        if any(k in message.lower() for k in timeout_keywords):
            return FailureCategory.TIMEOUT
        
        resource_keywords = ["memory", "disk", "cpu", "quota", "limit", "exceeded"]
        if any(k in message.lower() for k in resource_keywords):
            return FailureCategory.RESOURCE
        
        dependency_keywords = ["connection", "unavailable", "refused", "dns", "network"]
        if any(k in message.lower() for k in dependency_keywords):
            return FailureCategory.DEPENDENCY
        
        validation_keywords = ["invalid", "validation", "schema", "format", "required"]
        if any(k in message.lower() for k in validation_keywords):
            return FailureCategory.VALIDATION
        
        security_keywords = ["auth", "permission", "forbidden", "unauthorized", "security"]
        if any(k in message.lower() for k in security_keywords):
            return FailureCategory.SECURITY
        
        logic_keywords = ["assertion", "invariant", "logic", "state", "consistency"]
        if any(k in message.lower() for k in logic_keywords):
            return FailureCategory.LOGIC
        
        return FailureCategory.UNKNOWN

    async def _identify_root_cause(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]]
    ) -> str:
        cause = getattr(error, "__cause__", None)
        
        if cause:
            return f"Caused by {type(cause).__name__}: {str(cause)}"
        
        if context:
            last_action = context.get("last_action")
            if last_action:
                return f"Failed during action: {last_action}"
        
        return str(error)

    def _extract_stack_trace(self, error: Exception) -> Optional[str]:
        import traceback
        try:
            return "".join(traceback.format_exception(type(error), error, error.__traceback__))
        except Exception:
            return None

    def _find_similar_failures(
        self,
        pattern_key: str,
        exclude_execution: str
    ) -> List[Dict[str, Any]]:
        patterns = self._failure_patterns.get(pattern_key, [])
        return [
            p for p in patterns
            if p["execution_id"] != exclude_execution
        ]

    async def _suggest_recovery(
        self,
        category: FailureCategory,
        root_cause: str
    ) -> Optional[str]:
        recovery_map = {
            FailureCategory.TIMEOUT: "increase_timeout_or_retry_with_backoff",
            FailureCategory.RESOURCE: "scale_resources_or_reduce_load",
            FailureCategory.DEPENDENCY: "check_dependency_health_or_use_fallback",
            FailureCategory.VALIDATION: "fix_input_data_or_update_schema",
            FailureCategory.SECURITY: "refresh_credentials_or_check_permissions",
            FailureCategory.LOGIC: "review_state_management_or_fix_bug"
        }
        
        return recovery_map.get(category)

    async def get_failure_stats(self) -> Dict[str, Any]:
        return {
            "total_unique_failures": len(self._reports),
            "total_occurrences": sum(r.frequency for r in self._reports.values()),
            "by_category": {
                cat.value: sum(1 for r in self._reports.values() if r.category == cat)
                for cat in FailureCategory
            },
            "most_frequent": sorted(
                [{"id": k, "frequency": r.frequency, "category": r.category.value}
                 for k, r in self._reports.items()],
                key=lambda x: x["frequency"],
                reverse=True
            )[:10]
        }

    async def get_trend(self, hours: int = 24) -> Dict[str, Any]:
        cutoff = datetime.utcnow().timestamp() - (hours * 3600)
        
        recent = [
            r for r in self._reports.values()
            if r.last_seen.timestamp() > cutoff
        ]
        
        return {
            "period_hours": hours,
            "failure_count": len(recent),
            "trend": "increasing" if len(recent) > 10 else "stable",
            "top_category": max(
                set(r.category for r in recent),
                key=lambda c: sum(1 for r in recent if r.category == c)
            ).value if recent else "none"
        }