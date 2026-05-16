import asyncio
import uuid
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ProceduralRule:
    id: str
    name: str
    description: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    success_count: int = 0
    failure_count: int = 0
    last_executed: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    priority: int = 1

class ProceduralMemoryStore:
    def __init__(self):
        self._rules: Dict[str, ProceduralRule] = {}
        self._lock = asyncio.Lock()

    async def store(
        self,
        name: str,
        description: str,
        condition: Dict[str, Any],
        action: Dict[str, Any],
        priority: int = 1
    ) -> str:
        rule_id = f"proc_{uuid.uuid4().hex[:12]}"
        
        rule = ProceduralRule(
            id=rule_id,
            name=name,
            description=description,
            condition=condition,
            action=action,
            priority=priority
        )
        
        async with self._lock:
            self._rules[rule_id] = rule
        
        logger.info(f"Procedural rule stored: {rule_id}")
        return rule_id

    async def find_applicable(
        self,
        situation: Dict[str, Any]
    ) -> List[ProceduralRule]:
        applicable = []
        
        for rule in self._rules.values():
            if self._matches_condition(rule.condition, situation):
                applicable.append(rule)
        
        applicable.sort(key=lambda r: r.priority, reverse=True)
        return applicable

    async def execute_rule(
        self,
        rule_id: str,
        execution_context: Dict[str, Any],
        executor: Callable
    ) -> Dict[str, Any]:
        rule = self._rules.get(rule_id)
        if not rule:
            raise ValueError(f"Rule not found: {rule_id}")
        
        try:
            result = await executor(rule.action, execution_context)
            rule.success_count += 1
            rule.last_executed = datetime.utcnow()
            return {"success": True, "result": result}
        except Exception as e:
            rule.failure_count += 1
            logger.error(f"Rule execution failed: {rule_id} - {str(e)}")
            return {"success": False, "error": str(e)}

    def _matches_condition(
        self,
        condition: Dict[str, Any],
        situation: Dict[str, Any]
    ) -> bool:
        for key, expected in condition.items():
            if key not in situation:
                return False
            
            actual = situation[key]
            
            if isinstance(expected, dict):
                if "eq" in expected and actual != expected["eq"]:
                    return False
                if "gt" in expected and actual <= expected["gt"]:
                    return False
                if "lt" in expected and actual >= expected["lt"]:
                    return False
                if "in" in expected and actual not in expected["in"]:
                    return False
            elif actual != expected:
                return False
        
        return True

    async def get_rule_stats(self, rule_id: str) -> Optional[Dict[str, Any]]:
        rule = self._rules.get(rule_id)
        if not rule:
            return None
        
        total = rule.success_count + rule.failure_count
        success_rate = rule.success_count / total if total > 0 else 0
        
        return {
            "rule_id": rule_id,
            "name": rule.name,
            "success_count": rule.success_count,
            "failure_count": rule.failure_count,
            "success_rate": success_rate,
            "last_executed": rule.last_executed.isoformat() if rule.last_executed else None
        }

    async def delete(self, rule_id: str) -> bool:
        async with self._lock:
            if rule_id not in self._rules:
                return False
            
            del self._rules[rule_id]
            logger.info(f"Procedural rule deleted: {rule_id}")
            return True

    async def get_all_rules(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "priority": r.priority,
                "success_rate": r.success_count / (r.success_count + r.failure_count) if (r.success_count + r.failure_count) > 0 else 0
            }
            for r in self._rules.values()
        ]import asyncio
import uuid
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ProceduralRule:
    id: str
    name: str
    description: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    success_count: int = 0
    failure_count: int = 0
    last_executed: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    priority: int = 1

class ProceduralMemoryStore:
    def __init__(self):
        self._rules: Dict[str, ProceduralRule] = {}
        self._lock = asyncio.Lock()

    async def store(
        self,
        name: str,
        description: str,
        condition: Dict[str, Any],
        action: Dict[str, Any],
        priority: int = 1
    ) -> str:
        rule_id = f"proc_{uuid.uuid4().hex[:12]}"
        
        rule = ProceduralRule(
            id=rule_id,
            name=name,
            description=description,
            condition=condition,
            action=action,
            priority=priority
        )
        
        async with self._lock:
            self._rules[rule_id] = rule
        
        logger.info(f"Procedural rule stored: {rule_id}")
        return rule_id

    async def find_applicable(
        self,
        situation: Dict[str, Any]
    ) -> List[ProceduralRule]:
        applicable = []
        
        for rule in self._rules.values():
            if self._matches_condition(rule.condition, situation):
                applicable.append(rule)
        
        applicable.sort(key=lambda r: r.priority, reverse=True)
        return applicable

    async def execute_rule(
        self,
        rule_id: str,
        execution_context: Dict[str, Any],
        executor: Callable
    ) -> Dict[str, Any]:
        rule = self._rules.get(rule_id)
        if not rule:
            raise ValueError(f"Rule not found: {rule_id}")
        
        try:
            result = await executor(rule.action, execution_context)
            rule.success_count += 1
            rule.last_executed = datetime.utcnow()
            return {"success": True, "result": result}
        except Exception as e:
            rule.failure_count += 1
            logger.error(f"Rule execution failed: {rule_id} - {str(e)}")
            return {"success": False, "error": str(e)}

    def _matches_condition(
        self,
        condition: Dict[str, Any],
        situation: Dict[str, Any]
    ) -> bool:
        for key, expected in condition.items():
            if key not in situation:
                return False
            
            actual = situation[key]
            
            if isinstance(expected, dict):
                if "eq" in expected and actual != expected["eq"]:
                    return False
                if "gt" in expected and actual <= expected["gt"]:
                    return False
                if "lt" in expected and actual >= expected["lt"]:
                    return False
                if "in" in expected and actual not in expected["in"]:
                    return False
            elif actual != expected:
                return False
        
        return True

    async def get_rule_stats(self, rule_id: str) -> Optional[Dict[str, Any]]:
        rule = self._rules.get(rule_id)
        if not rule:
            return None
        
        total = rule.success_count + rule.failure_count
        success_rate = rule.success_count / total if total > 0 else 0
        
        return {
            "rule_id": rule_id,
            "name": rule.name,
            "success_count": rule.success_count,
            "failure_count": rule.failure_count,
            "success_rate": success_rate,
            "last_executed": rule.last_executed.isoformat() if rule.last_executed else None
        }

    async def delete(self, rule_id: str) -> bool:
        async with self._lock:
            if rule_id not in self._rules:
                return False
            
            del self._rules[rule_id]
            logger.info(f"Procedural rule deleted: {rule_id}")
            return True

    async def get_all_rules(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "priority": r.priority,
                "success_rate": r.success_count / (r.success_count + r.failure_count) if (r.success_count + r.failure_count) > 0 else 0
            }
            for r in self._rules.values()
        ]