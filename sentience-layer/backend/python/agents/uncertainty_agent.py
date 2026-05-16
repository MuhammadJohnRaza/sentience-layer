from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage, AgentResult

class UncertaintyAgent(BaseAgent):
    def __init__(self, agent_id: str = "uncertainty", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        
    async def initialize(self):
        self.register_skill("quantify_uncertainty", self.quantify_uncertainty)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        return await self.quantify_uncertainty(message)
        
    async def quantify_uncertainty(self, message: AgentMessage) -> AgentResult:
        return AgentResult(success=True, data={"uncertainty_level": 0.45, "factors": ["missing_data"]})
