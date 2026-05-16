import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .base_agent import BaseAgent, AgentMessage, AgentResult

class Stance(Enum):
    PRO = "pro"
    CON = "con"
    NEUTRAL = "neutral"

@dataclass
class Argument:
    argument_id: str
    claim: str
    evidence: List[str]
    stance: Stance
    strength: float
    rebuttals: List[str] = field(default_factory=list)

@dataclass
class DebateRound:
    round_number: int
    pro_arguments: List[Argument]
    con_arguments: List[Argument]
    synthesis: Optional[str] = None

class DebateAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "debater",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.arguments: Dict[str, Argument] = {}
        self.rounds: List[DebateRound] = []
        self.topic: Optional[str] = None
        self.max_rounds = config.get("max_rounds", 5)
        self.consensus_threshold = config.get("consensus_threshold", 0.7)
        
    async def initialize(self):
        self.register_skill("debate", self._conduct_debate)
        self.register_skill("argue", self._generate_argument)
        self.register_skill("rebut", self._generate_rebuttal)
        self.register_skill("synthesize", self._synthesize_debate)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "debate")
        
        if skill == "debate":
            return await self._conduct_debate(
                message.content,
                message.metadata.get("rounds", self.max_rounds)
            )
        elif skill == "argue":
            return await self._generate_argument(
                message.content,
                message.metadata.get("stance", "pro")
            )
        elif skill == "rebut":
            return await self._generate_rebuttal(
                message.content,
                message.metadata.get("target_argument")
            )
        elif skill == "synthesize":
            return await self._synthesize_debate()
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _conduct_debate(
        self,
        topic: str,
        rounds: int
    ) -> AgentResult:
        self.topic = topic
        self.arguments.clear()
        self.rounds.clear()
        
        for round_num in range(1, rounds + 1):
            pro_args = await self._generate_stance_arguments(topic, Stance.PRO, round_num)
            con_args = await self._generate_stance_arguments(topic, Stance.CON, round_num)
            
            for arg in pro_args:
                self.arguments[arg.argument_id] = arg
            for arg in con_args:
                self.arguments[arg.argument_id] = arg
                
            if round_num > 1:
                await self._generate_rebuttals_for_round(pro_args, con_args)
                
            debate_round = DebateRound(
                round_number=round_num,
                pro_arguments=pro_args,
                con_arguments=con_args
            )
            self.rounds.append(debate_round)
            
        synthesis = await self._synthesize_debate()
        
        pro_strength = sum(a.strength for a in self.arguments.values() if a.stance == Stance.PRO)
        con_strength = sum(a.strength for a in self.arguments.values() if a.stance == Stance.CON)
        
        winner = "pro" if pro_strength > con_strength * 1.2 else "con" if con_strength > pro_strength * 1.2 else "tie"
        
        return AgentResult(
            success=True,
            data={
                "topic": topic,
                "rounds_conducted": len(self.rounds),
                "total_arguments": len(self.arguments),
                "pro_strength": round(pro_strength, 4),
                "con_strength": round(con_strength, 4),
                "winner": winner,
                "synthesis": synthesis,
                "key_arguments": {
                    "pro": [
                        {
                            "claim": a.claim,
                            "strength": round(a.strength, 4)
                        }
                        for a in sorted(
                            [arg for arg in self.arguments.values() if arg.stance == Stance.PRO],
                            key=lambda x: x.strength,
                            reverse=True
                        )[:3]
                    ],
                    "con": [
                        {
                            "claim": a.claim,
                            "strength": round(a.strength, 4)
                        }
                        for a in sorted(
                            [arg for arg in self.arguments.values() if arg.stance == Stance.CON],
                            key=lambda x: x.strength,
                            reverse=True
                        )[:3]
                    ]
                }
            }
        )
        
    async def _generate_argument(
        self,
        claim: str,
        stance_str: str
    ) -> AgentResult:
        stance = Stance(stance_str)
        
        argument = Argument(
            argument_id=f"arg_{len(self.arguments)}",
            claim=claim,
            evidence=self._generate_evidence(claim, stance),
            stance=stance,
            strength=self._assess_argument_strength(claim, stance)
        )
        
        self.arguments[argument.argument_id] = argument
        
        return AgentResult(
            success=True,
            data={
                "argument_id": argument.argument_id,
                "claim": claim,
                "stance": stance.value,
                "strength": round(argument.strength, 4),
                "evidence_count": len(argument.evidence)
            }
        )
        
    async def _generate_rebuttal(
        self,
        argument_id: str,
        target_id: Optional[str]
    ) -> AgentResult:
        if target_id not in self.arguments:
            return AgentResult(
                success=False,
                error=f"Target argument {target_id} not found"
            )
            
        target = self.arguments[target_id]
        rebuttal_stance = Stance.PRO if target.stance == Stance.CON else Stance.CON
        
        rebuttal_claim = f"Counter to: {target.claim}"
        rebuttal = Argument(
            argument_id=f"reb_{len(self.arguments)}",
            claim=rebuttal_claim,
            evidence=self._generate_evidence(rebuttal_claim, rebuttal_stance),
            stance=rebuttal_stance,
            strength=self._assess_argument_strength(rebuttal_claim, rebuttal_stance)
        )
        
        self.arguments[rebuttal.argument_id] = rebuttal
        target.rebuttals.append(rebuttal.argument_id)
        
        return AgentResult(
            success=True,
            data={
                "rebuttal_id": rebuttal.argument_id,
                "target_id": target_id,
                "claim": rebuttal_claim
            }
        )

    async def _generate_stance_arguments(self, topic: str, stance: Stance, round_num: int) -> List[Argument]:
        return [
            Argument(
                argument_id=f"arg_{stance.value}_{round_num}_{i}",
                claim=f"{stance.value.capitalize()} argument {i} for {topic}",
                evidence=[f"Evidence {j}" for j in range(2)],
                stance=stance,
                strength=random.random()
            )
            for i in range(2)
        ]

    async def _generate_rebuttals_for_round(self, pro_args: List[Argument], con_args: List[Argument]):
        for pro in pro_args:
            target = random.choice(con_args)
            pro.rebuttals.append(target.argument_id)
        for con in con_args:
            target = random.choice(pro_args)
            con.rebuttals.append(target.argument_id)

    async def _assess_argument_strength(self, claim: str, stance: Stance) -> float:
        return random.random()

    def _generate_evidence(self, claim: str, stance: Stance) -> List[str]:
        return [f"Evidence for {claim}"]

    async def _synthesize_debate(self) -> str:
        return f"Consensus reached on topic: {self.topic}"