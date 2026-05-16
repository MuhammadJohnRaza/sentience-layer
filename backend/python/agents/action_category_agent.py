from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import re

from .base_agent import BaseAgent, AgentMessage, AgentResult

class ActionCategoryAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "action_categorizer",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.categories: Dict[str, Dict[str, Any]] = {}
        self.taxonomy: Dict[str, List[str]] = defaultdict(list)
        self.keywords: Dict[str, Set[str]] = defaultdict(set)
        self.classification_rules: List[Dict[str, Any]] = []
        self.confidence_threshold = config.get("confidence_threshold", 0.6)
        
    async def initialize(self):
        self.register_skill("categorize", self._categorize)
        self.register_skill("define_category", self._define_category)
        self.register_skill("auto_classify", self._auto_classify)
        self.register_skill("taxonomy", self._get_taxonomy)
        
        self._load_default_categories()
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "categorize")
        
        if skill == "categorize":
            return await self._categorize(
                message.content,
                message.metadata.get("target_categories")
            )
        elif skill == "define_category":
            return await self._define_category(message.content)
        elif skill == "auto_classify":
            return await self._auto_classify(message.content)
        elif skill == "taxonomy":
            return await self._get_taxonomy()
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _categorize(
        self,
        action: Dict[str, Any],
        target_categories: Optional[List[str]] = None
    ) -> AgentResult:
        text = f"{action.get('description', '')} {action.get('name', '')}"
        scores = {}
        
        categories = target_categories or list(self.categories.keys())
        
        for cat_id in categories:
            cat = self.categories.get(cat_id, {})
            score = self._match_category(text, cat)
            scores[cat_id] = score
            
        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        best_match = sorted_scores[0] if sorted_scores else (None, 0.0)
        
        classifications = [
            {
                "category_id": cat_id,
                "category_name": self.categories.get(cat_id, {}).get("name", cat_id),
                "confidence": round(score, 4),
                "matches": self._get_matching_keywords(text, cat_id)
            }
            for cat_id, score in sorted_scores[:3]
            if score > self.confidence_threshold
        ]
        
        return AgentResult(
            success=True,
            data={
                "action_id": action.get("id"),
                "primary_category": {
                    "id": best_match[0],
                    "confidence": round(best_match[1], 4)
                } if best_match[1] > self.confidence_threshold else None,
                "all_matches": classifications,
                "uncertain": best_match[1] < self.confidence_threshold
            },
            confidence=best_match[1]
        )
        
    async def _define_category(self, category_def: Dict[str, Any]) -> AgentResult:
        cat_id = category_def.get("id")
        
        self.categories[cat_id] = {
            "id": cat_id,
            "name": category_def.get("name", cat_id),
            "description": category_def.get("description", ""),
            "parent": category_def.get("parent"),
            "keywords": set(category_def.get("keywords", [])),
            "rules": category_def.get("rules", []),
            "examples": category_def.get("examples", [])
        }
        
        for keyword in category_def.get("keywords", []):
            self.keywords[cat_id].add(keyword.lower())
            
        parent = category_def.get("parent")
        if parent:
            self.taxonomy[parent].append(cat_id)
            
        return AgentResult(
            success=True,
            data={
                "category_id": cat_id,
                "defined": True,
                "total_categories": len(self.categories)
            }
        )
        
    async def _auto_classify(self, actions: List[Dict[str, Any]]) -> AgentResult:
        results = []
        
        for action in actions:
            result = await self._categorize(action)
            results.append(result.data)
            
        category_distribution = defaultdict(int)
        for r in results:
            if r["primary_category"]:
                category_distribution[r["primary_category"]["id"]] += 1
                
        return AgentResult(
            success=True,
            data={
                "classifications": results,
                "distribution": dict(category_distribution),
                "uncertain_count": sum(1 for r in results if r["uncertain"])
            }
        )
        
    async def _get_taxonomy(self) -> AgentResult:
        def build_tree(parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
            children = self.taxonomy.get(parent_id, [])
            return [
                {
                    "id": child,
                    "name": self.categories[child]["name"],
                    "children": build_tree(child)
                }
                for child in children
                if child in self.categories
            ]
            
        return AgentResult(
            success=True,
            data={
                "taxonomy": build_tree(),
                "total_categories": len(self.categories),
                "root_categories": len(self.taxonomy.get(None, []))
            }
        )
        
    def _match_category(self, text: str, category: Dict[str, Any]) -> float:
        text_lower = text.lower()
        score = 0.0
        
        keywords = category.get("keywords", set())
        for keyword in keywords:
            if keyword in text_lower:
                score += 0.3
                
        for rule in category.get("rules", []):
            pattern = rule.get("pattern", "")
            weight = rule.get("weight", 0.2)
            if re.search(pattern, text_lower):
                score += weight
                
        examples = category.get("examples", [])
        for example in examples:
            similarity = self._text_similarity(text_lower, example.lower())
            score += similarity * 0.2
            
        return min(1.0, score)
        
    def _get_matching_keywords(self, text: str, cat_id: str) -> List[str]:
        text_lower = text.lower()
        return [
            kw for kw in self.keywords.get(cat_id, set())
            if kw in text_lower
        ]
        
    def _text_similarity(self, a: str, b: str) -> float:
        words_a = set(a.split())
        words_b = set(b.split())
        
        if not words_a or not words_b:
            return 0.0
            
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)
        
        return intersection / union if union > 0 else 0.0
        
    def _load_default_categories(self):
        defaults = [
            {
                "id": "strategic",
                "name": "Strategic",
                "keywords": ["strategy", "vision", "goal", "objective", "plan", "roadmap"],
                "parent": None
            },
            {
                "id": "operational",
                "name": "Operational",
                "keywords": ["process", "workflow", "execute", "implement", "deploy"],
                "parent": None
            },
            {
                "id": "analytical",
                "name": "Analytical",
                "keywords": ["analyze", "measure", "evaluate", "assess", "report", "metric"],
                "parent": None
            },
            {
                "id": "creative",
                "name": "Creative",
                "keywords": ["design", "create", "innovate", "prototype", "experiment"],
                "parent": None
            },
            {
                "id": "communication",
                "name": "Communication",
                "keywords": ["communicate", "present", "document", "share", "collaborate"],
                "parent": None
            }
        ]
        
        for cat in defaults:
            self._define_category(cat)