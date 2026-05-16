import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ResilienceMetrics:
    timestamp: datetime
    availability: float
    latency_p50: float
    latency_p99: float
    error_rate: float
    throughput: float
    recovery_time_avg: float
    circuit_breaker_events: int = 0
    fallback_invocations: int = 0
    retry_attempts: int = 0

class ResilienceMonitor:
    def __init__(self, window_minutes: int = 5):
        self._metrics: deque = deque(maxlen=window_minutes * 60)
        self._errors: deque = deque(maxlen=1000)
        self._latencies: deque = deque(maxlen=1000)
        self._recoveries: deque = deque(maxlen=100)
        self._circuit_events = 0
        self._fallback_count = 0
        self._retry_count = 0
        self._start_time = datetime.utcnow()
        self._total_requests = 0
        self._successful_requests = 0

    async def record_request(
        self,
        latency_ms: float,
        success: bool,
        service: Optional[str] = None
    ) -> None:
        self._total_requests += 1
        if success:
            self._successful_requests += 1
        
        self._latencies.append({
            "latency": latency_ms,
            "timestamp": datetime.utcnow(),
            "service": service
        })

    async def record_error(
        self,
        error_type: str,
        service: Optional[str] = None,
        recovered: bool = False
    ) -> None:
        self._errors.append({
            "type": error_type,
            "service": service,
            "timestamp": datetime.utcnow(),
            "recovered": recovered
        })

    async def record_recovery(self, duration_ms: float) -> None:
        self._recoveries.append({
            "duration": duration_ms,
            "timestamp": datetime.utcnow()
        })

    async def record_circuit_event(self) -> None:
        self._circuit_events += 1

    async def record_fallback(self) -> None:
        self._fallback_count += 1

    async def record_retry(self) -> None:
        self._retry_count += 1

    async def get_current_metrics(self) -> ResilienceMetrics:
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=5)
        
        recent_latencies = [
            e["latency"] for e in self._latencies
            if e["timestamp"] > window_start
        ]
        
        recent_errors = [
            e for e in self._errors
            if e["timestamp"] > window_start
        ]
        
        recent_recoveries = [
            r["duration"] for r in self._recoveries
            if r["timestamp"] > window_start
        ]
        
        return ResilienceMetrics(
            timestamp=now,
            availability=self._calculate_availability(),
            latency_p50=self._percentile(recent_latencies, 0.5) if recent_latencies else 0,
            latency_p99=self._percentile(recent_latencies, 0.99) if recent_latencies else 0,
            error_rate=len(recent_errors) / max(len(recent_latencies), 1),
            throughput=len(recent_latencies) / 300,
            recovery_time_avg=sum(recent_recoveries) / len(recent_recoveries) if recent_recoveries else 0,
            circuit_breaker_events=self._circuit_events,
            fallback_invocations=self._fallback_count,
            retry_attempts=self._retry_count
        )

    def _calculate_availability(self) -> float:
        if self._total_requests == 0:
            return 1.0
        return self._successful_requests / self._total_requests

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile)
        return sorted_data[min(index, len(sorted_data) - 1)]

    async def get_health_status(self) -> Dict[str, Any]:
        metrics = await self.get_current_metrics()
        
        status = "healthy"
        if metrics.error_rate > 0.1 or metrics.availability < 0.95:
            status = "degraded"
        if metrics.error_rate > 0.25 or metrics.availability < 0.9:
            status = "unhealthy"
        
        return {
            "status": status,
            "metrics": {
                "availability": round(metrics.availability, 4),
                "latency_p99_ms": round(metrics.latency_p99, 2),
                "error_rate": round(metrics.error_rate, 4),
                "throughput_per_second": round(metrics.throughput, 2)
            },
            "recommendations": self._generate_recommendations(metrics)
        }

    def _generate_recommendations(self, metrics: ResilienceMetrics) -> List[str]:
        recommendations = []
        
        if metrics.error_rate > 0.05:
            recommendations.append("Investigate error sources - error rate elevated")
        
        if metrics.latency_p99 > 1000:
            recommendations.append("High latency detected - consider scaling")
        
        if metrics.availability < 0.99:
            recommendations.append("Availability below target - review fault tolerance")
        
        if metrics.circuit_breaker_events > 0:
            recommendations.append("Circuit breakers triggered - check downstream services")
        
        return recommendations

    async def get_historical_metrics(
        self,
        minutes: int = 60
    ) -> List[Dict[str, Any]]:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        
        return [
            {
                "timestamp": e["timestamp"].isoformat(),
                "latency": e["latency"],
                "service": e.get("service")
            }
            for e in self._latencies
            if e["timestamp"] > cutoff
        ]