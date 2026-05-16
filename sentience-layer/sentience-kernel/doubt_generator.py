import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class DoubtPattern:
    target: str
    doubt_type: str
    severity: float
    evidence: List[str]

class DoubtGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.doubt_types = [
            "epistemic",
            "methodological", 
            "ethical",
            "temporal",
            "causal",
            "completeness"
        ]
        self.severity_threshold = config.get("severity_threshold", 0.5)
        self.max_doubts = config.get("max_doubts", 5)
        
    async def evaluate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        content = params.get("content", "")
        context = params.get("context", {})
        
        doubts = []
        
        for doubt_type in self.doubt_types:
            pattern = await self._generate_doubt(content, context, doubt_type)
            if pattern and pattern.severity > self.severity_threshold:
                doubts.append(pattern)
                
        doubts.sort(key=lambda x: x.severity, reverse=True)
        top_doubts = doubts[:self.max_doubts]
        
        return {
            "doubts": [
                {
                    "target": d.target,
                    "type": d.doubt_type,
                    "severity": d.severity,
                    "evidence": d.evidence
                }
                for d in top_doubts
            ],
            "overall_confidence": 1.0 - (sum(d.severity for d in top_doubts) / max(len(top_doubts), 1)),
            "recommendation": await self._recommend_action(top_doubts)
        }
        
    async def _generate_doubt(
        self, 
        content: str, 
        context: Dict[str, Any], 
        doubt_type: str
    ) -> Optional[DoubtPattern]:
        generators = {
            "epistemic": self._epistemic_doubt,
            "methodological": self._methodological_doubt,
            "ethical": self._ethical_doubt,
            "temporal": self._temporal_doubt,
            "causal": self._causal_doubt,
            "completeness": self._completeness_doubt
        }
        
        generator = generators.get(doubt_type)
        if generator:
            return await generator(content, context)
        return None
        
    async def _epistemic_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Source reliability uncertain",
            "Information may be incomplete",
            "Alternative interpretations exist"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="epistemic",
            severity=random.uniform(0.2, 0.9),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _methodological_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Approach may have blind spots",
            "Method assumptions not verified",
            "Better alternatives may exist"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="methodological",
            severity=random.uniform(0.1, 0.8),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _ethical_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Potential for unintended harm",
            "Bias in decision criteria",
            "Stakeholder impact unclear"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="ethical",
            severity=random.uniform(0.3, 0.95),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _temporal_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Timing assumptions may be wrong",
            "Future states are uncertain",
            "Historical patterns may not repeat"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="temporal",
            severity=random.uniform(0.2, 0.7),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _causal_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Correlation vs causation unclear",
            "Confounding variables possible",
            "Causal chain may be incomplete"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="causal",
            severity=random.uniform(0.3, 0.85),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _completeness_doubt(self, content: str, context: Dict[str, Any]) -> DoubtPattern:
        evidence = [
            "Edge cases not considered",
            "Missing data points",
            "Alternative scenarios unexplored"
        ]
        return DoubtPattern(
            target=content[:50],
            doubt_type="completeness",
            severity=random.uniform(0.1, 0.6),
            evidence=random.sample(evidence, min(2, len(evidence)))
        )
        
    async def _recommend_action(self, doubts: List[DoubtPattern]) -> str:
        if not doubts:
            return "Proceed with confidence"
            
        max_severity = max(d.severity for d in doubts)
        
        if max_severity > 0.8:
            return "Halt and re-evaluate before proceeding"
        elif max_severity > 0.6:
            return "Proceed with caution and monitoring"
        elif max_severity > 0.4:
            return "Note concerns and continue"
        else:
            return "Proceed normally"