import json
import time
from typing import Dict, List, Any, Optional
from collections import defaultdict

from .base_agent import BaseAgent, AgentMessage, AgentResult

class PersonalizationAgent(BaseAgent):
    def __init__(self, agent_id: str = "personalization", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.interaction_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.preference_models: Dict[str, Dict[str, float]] = {}
        self.max_history_per_user = config.get("max_history_per_user", 500)
        
    async def initialize(self):
        self.register_skill("adapt_response", self._adapt_response)
        self.register_skill("learn_preferences", self._learn_preferences)
        self.register_skill("generate_profile", self._generate_profile)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "adapt_response")
        user_id = message.metadata.get("user_id", "anonymous")
        
        if skill == "adapt_response":
            return await self._adapt_response(message, user_id)
        elif skill == "learn_preferences":
            return await self._learn_preferences(message, user_id)
        elif skill == "generate_profile":
            return await self._generate_profile(user_id)
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _adapt_response(
        self, 
        message: AgentMessage, 
        user_id: str
    ) -> AgentResult:
        content = message.content
        profile = self.user_profiles.get(user_id, {})
        
        tone = profile.get("preferred_tone", "neutral")
        detail_level = profile.get("detail_level", "medium")
        format_pref = profile.get("format_preference", "structured")
        
        adapted = self._apply_adaptation(content, tone, detail_level, format_pref)
        
        self._record_interaction(user_id, "adapt", {
            "original": content,
            "adapted": adapted,
            "tone": tone
        })
        
        return AgentResult(
            success=True,
            data={
                "adapted_content": adapted,
                "adaptations_applied": {
                    "tone": tone,
                    "detail_level": detail_level,
                    "format": format_pref
                }
            },
            confidence=self._calculate_adaptation_confidence(user_id)
        )
        
    async def _learn_preferences(
        self, 
        message: AgentMessage, 
        user_id: str
    ) -> AgentResult:
        feedback = message.content
        
        if isinstance(feedback, dict):
            for key, value in feedback.items():
                if user_id not in self.preference_models:
                    self.preference_models[user_id] = {}
                    
                current = self.preference_models[user_id].get(key, 0.5)
                self.preference_models[user_id][key] = (
                    current * 0.7 + value * 0.3
                )
                
        self._update_profile(user_id)
        
        return AgentResult(
            success=True,
            data={
                "preferences_updated": list(feedback.keys()) if isinstance(feedback, dict) else [],
                "current_model": self.preference_models.get(user_id, {})
            }
        )
        
    async def _generate_profile(self, user_id: str) -> AgentResult:
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self._create_default_profile()
            
        profile = self.user_profiles[user_id]
        history = self.interaction_history.get(user_id, [])
        
        profile["interaction_count"] = len(history)
        profile["last_active"] = history[-1]["timestamp"] if history else None
        profile["preference_stability"] = self._calculate_stability(user_id)
        
        return AgentResult(
            success=True,
            data=profile
        )
        
    def _apply_adaptation(
        self, 
        content: Any, 
        tone: str, 
        detail: str, 
        format_pref: str
    ) -> Any:
        adapted = content
        
        if isinstance(content, str):
            if tone == "formal":
                adapted = adapted.replace("!", ".").replace("hey", "hello")
            elif tone == "casual":
                adapted = adapted.replace("hello", "hey").replace("regards", "cheers")
                
            if detail == "high":
                adapted += "\n\n[Additional context and references included]"
            elif detail == "low":
                lines = adapted.split("\n")
                adapted = lines[0] if lines else adapted
                
            if format_pref == "bullet":
                if isinstance(adapted, str) and "\n" in adapted:
                    lines = [f"- {line.strip()}" for line in adapted.split("\n") if line.strip()]
                    adapted = "\n".join(lines)
                    
        return adapted
        
    def _update_profile(self, user_id: str):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self._create_default_profile()
            
        prefs = self.preference_models.get(user_id, {})
        
        if "formality" in prefs:
            self.user_profiles[user_id]["preferred_tone"] = (
                "formal" if prefs["formality"] > 0.6 else
                "casual" if prefs["formality"] < 0.4 else "neutral"
            )
            
        if "detail" in prefs:
            self.user_profiles[user_id]["detail_level"] = (
                "high" if prefs["detail"] > 0.6 else
                "low" if prefs["detail"] < 0.4 else "medium"
            )
            
    def _create_default_profile(self) -> Dict[str, Any]:
        return {
            "preferred_tone": "neutral",
            "detail_level": "medium",
            "format_preference": "structured",
            "topics_of_interest": [],
            "avoid_topics": [],
            "created_at": time.time()
        }
        
    def _record_interaction(self, user_id: str, interaction_type: str, data: Dict[str, Any]):
        record = {
            "timestamp": time.time(),
            "type": interaction_type,
            "data": data
        }
        
        self.interaction_history[user_id].append(record)
        
        if len(self.interaction_history[user_id]) > self.max_history_per_user:
            self.interaction_history[user_id] = self.interaction_history[user_id][-self.max_history_per_user:]
            
    def _calculate_adaptation_confidence(self, user_id: str) -> float:
        history = self.interaction_history.get(user_id, [])
        if not history:
            return 0.3
            
        interactions = len(history)
        return min(0.95, 0.3 + (interactions * 0.01))
        
    def _calculate_stability(self, user_id: str) -> float:
        history = self.interaction_history.get(user_id, [])
        if len(history) < 10:
            return 0.5
            
        recent = history[-10:]
        types = [h["type"] for h in recent]
        
        from collections import Counter
        most_common = Counter(types).most_common(1)[0][1]
        
        return most_common / len(recent)