from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage, AgentResult

class CriticAgent(BaseAgent):
    def __init__(self, agent_id: str = "critic", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        
    async def initialize(self):
        self.register_skill("critique", self.critique)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        return await self.critique(message)
        
    async def critique(self, message: AgentMessage) -> AgentResult:
        return AgentResult(success=True, data={"critique": "The proposal lacks detailed edge-case handling.", "severity": "medium"})
