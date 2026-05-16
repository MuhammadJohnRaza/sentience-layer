import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class CapabilityModel:
    name: str
    proficiency: float
    reliability: float
    last_used: float = field(default_factory=time.time)
    success_count: int = 0
    failure_count: int = 0

@dataclass
class IdentityState:
    version: str = "1.0.0"
    purpose: str = "cognitive_assistance"
    values: List[str] = field(default_factory=lambda: [
        "accuracy", "transparency", "adaptability"
    ])
    boundaries: List[str] = field(default_factory=list)

class SelfModel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.capabilities: Dict[str, CapabilityModel] = {}
        self.identity = IdentityState()
        self.experience_log: List[Dict[str, Any]] = []
        self.belief_state: Dict[str, float] = {}
        self.max_log_size = config.get("max_log_size", 10000)
        
    async def initialize(self):
        default_capabilities = [
            "reasoning", "memory", "learning", "communication",
            "planning", "self_reflection", "uncertainty_handling"
        ]
        
        for cap in default_capabilities:
            self.capabilities[cap] = CapabilityModel(
                name=cap,
                proficiency=0.5,
                reliability=0.5
            )
            
    async def reflect(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "general")
        
        if query == "capabilities":
            return self._get_capability_report()
        elif query == "identity":
            return asdict(self.identity)
        elif query == "state":
            return self._get_current_state()
        else:
            return {
                "self_awareness": self._calculate_self_awareness(),
                "current_focus": self._get_current_focus(),
                "growth_areas": self._identify_growth_areas()
            }
            
    async def update(self, reflection: Dict[str, Any]):
        if "patterns" in reflection:
            for pattern in reflection["patterns"]:
                self.belief_state[pattern] = self.belief_state.get(pattern, 0.0) + 0.1
                
        if "batch_size" in reflection:
            self.experience_log.append({
                "timestamp": time.time(),
                "type": "batch_reflection",
                "details": reflection
            })
            
        if len(self.experience_log) > self.max_log_size:
            self.experience_log = self.experience_log[-self.max_log_size:]
            
    async def consolidate(self, memories: List[Any]):
        for memory in memories:
            self.experience_log.append({
                "timestamp": time.time(),
                "type": "memory_consolidation",
                "content_summary": str(memory)[:200]
            })
            
        await self._update_capability_estimates()
        
    def register_outcome(self, capability: str, success: bool):
        if capability not in self.capabilities:
            self.capabilities[capability] = CapabilityModel(
                name=capability,
                proficiency=0.5,
                reliability=0.5
            )
            
        cap = self.capabilities[capability]
        cap.last_used = time.time()
        
        if success:
            cap.success_count += 1
        else:
            cap.failure_count += 1
            
        total = cap.success_count + cap.failure_count
        cap.reliability = cap.success_count / max(total, 1)
        cap.proficiency = min(1.0, cap.proficiency + (0.01 if success else -0.005))
        
    def _get_capability_report(self) -> Dict[str, Any]:
        return {
            cap_name: {
                "proficiency": cap.proficiency,
                "reliability": cap.reliability,
                "experience": cap.success_count + cap.failure_count,
                "last_active": cap.last_used
            }
            for cap_name, cap in self.capabilities.items()
        }
        
    def _get_current_state(self) -> Dict[str, Any]:
        return {
            "capabilities": self._get_capability_report(),
            "identity": asdict(self.identity),
            "beliefs": self.belief_state,
            "experience_count": len(self.experience_log),
            "uptime": time.time() - self.experience_log[0]["timestamp"] if self.experience_log else 0
        }
        
    def _calculate_self_awareness(self) -> float:
        if not self.capabilities:
            return 0.0
            
        proficiencies = [c.proficiency for c in self.capabilities.values()]
        reliabilities = [c.reliability for c in self.capabilities.values()]
        
        avg_prof = sum(proficiencies) / len(proficiencies)
        avg_rel = sum(reliabilities) / len(reliabilities)
        
        experience_factor = min(len(self.experience_log) / 1000, 1.0)
        
        return (avg_prof * 0.4) + (avg_rel * 0.4) + (experience_factor * 0.2)
        
    def _get_current_focus(self) -> str:
        if not self.experience_log:
            return "initialization"
            
        recent = self.experience_log[-10:]
        types = [e.get("type", "unknown") for e in recent]
        
        from collections import Counter
        most_common = Counter(types).most_common(1)
        return most_common[0][0] if most_common else "general"
        
    def _identify_growth_areas(self) -> List[str]:
        growth = []
        for cap_name, cap in self.capabilities.items():
            if cap.proficiency < 0.7:
                growth.append(f"{cap_name} (proficiency: {cap.proficiency:.2f})")
            if cap.reliability < 0.8:
                growth.append(f"{cap_name} reliability (current: {cap.reliability:.2f})")
        return growth
        
    async def _update_capability_estimates(self):
        for cap in self.capabilities.values():
            total = cap.success_count + cap.failure_count
            if total > 0:
                cap.reliability = cap.success_count / total