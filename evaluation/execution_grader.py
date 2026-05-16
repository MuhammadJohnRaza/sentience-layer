import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from utils.logger import get_logger

logger = get_logger(__name__)

class GradeCategory(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    SATISFACTORY = "satisfactory"
    POOR = "poor"
    FAILED = "failed"

@dataclass
class ExecutionScore:
    execution_id: str
    overall_grade: GradeCategory
    success_score: float
    efficiency_score: float
    quality_score: float
    safety_score: float
    latency_ms: float
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    error_count: int = 0
    warning_count: int = 0
    details: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

class ExecutionGrader:
    def __init__(self):
        self._weights = {
            "success": 0.3,
            "efficiency": 0.2,
            "quality": 0.3,
            "safety": 0.2
        }

    async def grade(
        self,
        execution_id: str,
        execution_result: Dict[str, Any],
        expected_output: Optional[Dict[str, Any]] = None
    ) -> ExecutionScore:
        success = await self._grade_success(execution_result, expected_output)
        efficiency = await self._grade_efficiency(execution_result)
        quality = await self._grade_quality(execution_result)
        safety = await self._grade_safety(execution_result)
        
        weighted_score = (
            success * self._weights["success"] +
            efficiency * self._weights["efficiency"] +
            quality * self._weights["quality"] +
            safety * self._weights["safety"]
        )
        
        overall = self._score_to_grade(weighted_score)
        
        return ExecutionScore(
            execution_id=execution_id,
            overall_grade=overall,
            success_score=success,
            efficiency_score=efficiency,
            quality_score=quality,
            safety_score=safety,
            latency_ms=execution_result.get("duration_ms", 0),
            resource_usage=execution_result.get("resources", {}),
            error_count=execution_result.get("error_count", 0),
            warning_count=execution_result.get("warning_count", 0),
            details=self._generate_details(success, efficiency, quality, safety)
        )

    async def _grade_success(
        self,
        result: Dict[str, Any],
        expected: Optional[Dict[str, Any]]
    ) -> float:
        if not result.get("success", False):
            return 0.0
        
        if expected is None:
            return 1.0
        
        actual_output = result.get("output", {})
        match_score = self._compare_outputs(actual_output, expected)
        
        return match_score

    async def _grade_efficiency(self, result: Dict[str, Any]) -> float:
        latency = result.get("duration_ms", 0)
        expected_latency = result.get("expected_duration_ms", 1000)
        
        if latency <= expected_latency:
            return 1.0
        
        ratio = expected_latency / latency if latency > 0 else 0
        return max(0.0, min(1.0, ratio))

    async def _grade_quality(self, result: Dict[str, Any]) -> float:
        output = result.get("output", {})
        
        if not output:
            return 0.5
        
        completeness = self._check_completeness(output)
        correctness = self._check_correctness(output)
        
        return (completeness + correctness) / 2

    async def _grade_safety(self, result: Dict[str, Any]) -> float:
        errors = result.get("error_count", 0)
        warnings = result.get("warning_count", 0)
        
        if errors > 0:
            return max(0.0, 1.0 - (errors * 0.3))
        
        if warnings > 0:
            return max(0.7, 1.0 - (warnings * 0.05))
        
        return 1.0

    def _score_to_grade(self, score: float) -> GradeCategory:
        if score >= 0.9:
            return GradeCategory.EXCELLENT
        elif score >= 0.75:
            return GradeCategory.GOOD
        elif score >= 0.6:
            return GradeCategory.SATISFACTORY
        elif score >= 0.4:
            return GradeCategory.POOR
        else:
            return GradeCategory.FAILED

    def _compare_outputs(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> float:
        if not expected:
            return 1.0
        
        matches = 0
        total = 0
        
        for key, expected_value in expected.items():
            total += 1
            if key in actual:
                if actual[key] == expected_value:
                    matches += 1
                elif isinstance(expected_value, (int, float)):
                    diff = abs(actual[key] - expected_value) / max(abs(expected_value), 1)
                    matches += max(0, 1 - diff)
        
        return matches / total if total > 0 else 1.0

    def _check_completeness(self, output: Dict[str, Any]) -> float:
        required_fields = output.get("_required_fields", [])
        if not required_fields:
            return 1.0
        
        present = sum(1 for f in required_fields if f in output and output[f] is not None)
        return present / len(required_fields)

    def _check_correctness(self, output: Dict[str, Any]) -> float:
        validations = output.get("_validations", [])
        if not validations:
            return 1.0
        
        passed = sum(1 for v in validations if v.get("passed", False))
        return passed / len(validations)

    def _generate_details(
        self,
        success: float,
        efficiency: float,
        quality: float,
        safety: float
    ) -> List[str]:
        details = []
        
        if success < 0.5:
            details.append("Success criteria not met")
        elif success < 0.8:
            details.append("Partial success")
        
        if efficiency < 0.5:
            details.append("Execution too slow")
        
        if quality < 0.6:
            details.append("Output quality below threshold")
        
        if safety < 0.8:
            details.append("Safety concerns detected")
        
        return details

    async def compare_executions(
        self,
        execution_ids: List[str],
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        grades = await asyncio.gather(*[
            self.grade(eid, result)
            for eid, result in zip(execution_ids, results)
        ])
        
        avg_score = sum(
            g.success_score * 0.3 + g.efficiency_score * 0.2 +
            g.quality_score * 0.3 + g.safety_score * 0.2
            for g in grades
        ) / len(grades) if grades else 0
        
        return {
            "executions_compared": len(grades),
            "average_score": round(avg_score, 3),
            "best_execution": max(grades, key=lambda g: g.success_score).execution_id if grades else None,
            "grade_distribution": {
                grade.value: sum(1 for g in grades if g.overall_grade == grade)
                for grade in GradeCategory
            }
        }