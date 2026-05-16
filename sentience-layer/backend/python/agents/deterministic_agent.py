import re
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentMessage, AgentResult

@dataclass
class Rule:
    condition: str
    action: str
    priority: int = 0
    confidence: float = 1.0

class DeterministicAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "deterministic",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.rules: List[Rule] = []
        self.facts: Dict[str, Any] = {}
        self.rule_engine = RuleEngine()
        self.inference_depth = config.get("inference_depth", 5)
        
    async def initialize(self):
        self.register_skill("assert_fact", self._assert_fact)
        self.register_skill("query", self._query_facts)
        self.register_skill("add_rule", self._add_rule)
        self.register_skill("infer", self._run_inference)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "query")
        
        if skill == "assert_fact":
            return await self._assert_fact(
                message.content,
                message.metadata.get("fact_id")
            )
        elif skill == "query":
            return await self._query_facts(message.content)
        elif skill == "add_rule":
            return await self._add_rule(message.content)
        elif skill == "infer":
            return await self._run_inference(
                message.content,
                message.metadata.get("goal")
            )
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _assert_fact(
        self,
        fact: Any,
        fact_id: Optional[str] = None
    ) -> AgentResult:
        if fact_id is None:
            fact_id = f"fact_{len(self.facts)}"
            
        self.facts[fact_id] = {
            "value": fact,
            "timestamp": __import__('time').time(),
            "derived": False
        }
        
        new_inferences = await self._forward_chain(fact_id)
        
        return AgentResult(
            success=True,
            data={
                "fact_id": fact_id,
                "new_inferences": len(new_inferences)
            },
            confidence=1.0
        )
        
    async def _query_facts(self, query: Any) -> AgentResult:
        if isinstance(query, str):
            matches = self._pattern_match(query)
        else:
            matches = {
                k: v for k, v in self.facts.items()
                if self._value_matches(v["value"], query)
            }
            
        return AgentResult(
            success=True,
            data={
                "matches": {
                    k: v["value"] for k, v in matches.items()
                },
                "count": len(matches)
            },
            confidence=1.0 if len(matches) > 0 else 0.0
        )
        
    async def _add_rule(self, rule_spec: Dict[str, Any]) -> AgentResult:
        rule = Rule(
            condition=rule_spec.get("condition", ""),
            action=rule_spec.get("action", ""),
            priority=rule_spec.get("priority", 0),
            confidence=rule_spec.get("confidence", 1.0)
        )
        
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        
        return AgentResult(
            success=True,
            data={"rule_added": True, "total_rules": len(self.rules)},
            confidence=1.0
        )
        
    async def _run_inference(
        self,
        premises: List[str],
        goal: Optional[str]
    ) -> AgentResult:
        inferred = set(premises)
        depth = 0
        
        while depth < self.inference_depth:
            new_inferences = set()
            
            for rule in self.rules:
                if self._evaluate_condition(rule.condition, inferred):
                    conclusion = self._apply_action(rule.action, inferred)
                    if conclusion and conclusion not in inferred:
                        new_inferences.add(conclusion)
                        
            if not new_inferences:
                break
                
            inferred.update(new_inferences)
            depth += 1
            
        result = {
            "inferred": list(inferred),
            "depth_reached": depth,
            "goal_reached": goal in inferred if goal else None
        }
        
        return AgentResult(
            success=True,
            data=result,
            confidence=1.0 if not goal or goal in inferred else 0.0
        )
        
    async def _forward_chain(self, new_fact_id: str) -> List[str]:
        new_inferences = []
        fact_value = self.facts[new_fact_id]["value"]
        
        for rule in self.rules:
            if self._condition_matches(rule.condition, new_fact_id, fact_value):
                conclusion = self._derive_conclusion(rule.action, new_fact_id)
                if conclusion:
                    conf_id = f"derived_{len(self.facts)}"
                    self.facts[conf_id] = {
                        "value": conclusion,
                        "timestamp": __import__('time').time(),
                        "derived": True,
                        "from_rule": rule.condition,
                        "source_fact": new_fact_id
                    }
                    new_inferences.append(conf_id)
                    
        return new_inferences
        
    def _pattern_match(self, pattern: str) -> Dict[str, Dict[str, Any]]:
        regex = re.compile(pattern, re.IGNORECASE)
        return {
            k: v for k, v in self.facts.items()
            if regex.search(str(v["value"]))
        }
        
    def _value_matches(self, value: Any, query: Any) -> bool:
        if isinstance(query, dict) and isinstance(value, dict):
            return all(
                k in value and self._value_matches(value[k], v)
                for k, v in query.items()
            )
        return str(value).lower() == str(query).lower()
        
    def _evaluate_condition(self, condition: str, facts: set) -> bool:
        tokens = condition.split()
        required = [t for t in tokens if not t in ("AND", "OR", "NOT")]
        
        if "AND" in tokens:
            return all(r in facts for r in required)
        elif "OR" in tokens:
            return any(r in facts for r in required)
        else:
            return required[0] in facts if required else False
            
    def _apply_action(self, action: str, facts: set) -> Optional[str]:
        if action.startswith("CONCLUDE:"):
            return action.replace("CONCLUDE:", "").strip()
        return None
        
    def _condition_matches(
        self,
        condition: str,
        fact_id: str,
        fact_value: Any
    ) -> bool:
        return fact_id in condition or str(fact_value) in condition
        
    def _derive_conclusion(self, action: str, source_fact: str) -> Optional[str]:
        if action.startswith("CONCLUDE:"):
            base = action.replace("CONCLUDE:", "").strip()
            return f"{base} [from {source_fact}]"
        return None
        
    def get_knowledge_base(self) -> Dict[str, Any]:
        return {
            "facts": {
                k: {
                    "value": v["value"],
                    "derived": v.get("derived", False)
                }
                for k, v in self.facts.items()
            },
            "rules": [
                {
                    "condition": r.condition,
                    "action": r.action,
                    "priority": r.priority
                }
                for r in self.rules
            ],
            "inference_depth": self.inference_depth
        }

class RuleEngine:
    def __init__(self):
        self.compiled_rules: List[Callable] = []
        
    def compile_rule(self, rule: Rule) -> Callable:
        def evaluate(facts: Dict[str, Any]) -> Optional[str]:
            if rule.condition in facts:
                return rule.action
            return None
        return evaluate