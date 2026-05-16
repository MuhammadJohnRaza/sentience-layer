from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class AgentCapability(Enum):
    REASONING = "reasoning"
    MEMORY = "memory"
    ACTION = "action"
    SIMULATION = "simulation"
    DEBATE = "debate"
    CRITIQUE = "critique"
    DREAM = "dream"
    PREMONITION = "premonition"
    ETHICS = "ethics"
    ECONOMIC = "economic"
    CAUSAL = "causal"
    PERSONALIZATION = "personalization"
    UNCERTAINTY = "uncertainty"
    CONSENSUS = "consensus"
    OPPORTUNITY = "opportunity"

class AgentTier(Enum):
    FOUNDATION = "foundation"
    SPECIALIZED = "specialized"
    COMPOSITE = "composite"
    META = "meta"

@dataclass
class AgentDefinition:
    id: str
    name: str
    description: str
    tier: AgentTier
    capabilities: List[AgentCapability]
    model: str = "claude-3"
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: str = ""
    tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    fallback_agents: List[str] = field(default_factory=list)
    rate_limit: int = 100
    timeout_seconds: int = 30
    memory_enabled: bool = False
    trace_enabled: bool = True
    ethical_constraints: List[str] = field(default_factory=list)

AGENT_REGISTRY: Dict[str, AgentDefinition] = {
    "personalization": AgentDefinition(
        id="personalization",
        name="Personalization Agent",
        description="Adapts responses and strategies based on user history, preferences, and context",
        tier=AgentTier.FOUNDATION,
        capabilities=[AgentCapability.PERSONALIZATION, AgentCapability.MEMORY],
        model="claude-3",
        temperature=0.5,
        system_prompt="You are a personalization engine. Analyze user patterns and adapt outputs to maximize relevance and engagement.",
        memory_enabled=True,
        ethical_constraints=["privacy_preservation", "bias_mitigation"]
    ),
    
    "memory_enabled": AgentDefinition(
        id="memory_enabled",
        name="Memory-Enabled Agent",
        description="Maintains and retrieves episodic, semantic, and procedural memories",
        tier=AgentTier.FOUNDATION,
        capabilities=[AgentCapability.MEMORY],
        model="claude-3",
        temperature=0.3,
        system_prompt="You are a memory management system. Store, retrieve, and consolidate memories with high fidelity.",
        memory_enabled=True,
        tools=["memory_store", "memory_retrieve", "memory_consolidate"]
    ),
    
    "deterministic": AgentDefinition(
        id="deterministic",
        name="Deterministic Agent",
        description="Provides consistent, reproducible outputs for structured tasks",
        tier=AgentTier.FOUNDATION,
        capabilities=[AgentCapability.REASONING],
        model="claude-3",
        temperature=0.0,
        system_prompt="You are a deterministic reasoning engine. Provide consistent, verifiable outputs."
    ),
    
    "action_ranking": AgentDefinition(
        id="action_ranking",
        name="Action Ranking Agent",
        description="Ranks and prioritizes actions based on multiple criteria",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.ACTION, AgentCapability.ECONOMIC],
        model="claude-3",
        temperature=0.4,
        system_prompt="You are an action ranking system. Evaluate actions across dimensions: impact, cost, risk, and alignment.",
        tools=["impact_analysis", "roi_calculator"]
    ),
    
    "action_priority": AgentDefinition(
        id="action_priority",
        name="Action Priority Agent",
        description="Determines execution order and urgency of actions",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.ACTION],
        model="claude-3",
        temperature=0.3,
        system_prompt="You are a priority scheduling system. Sequence actions to maximize throughput and minimize conflicts."
    ),
    
    "action_category": AgentDefinition(
        id="action_category",
        name="Action Category Agent",
        description="Classifies actions into categories and types",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.ACTION],
        model="claude-3",
        temperature=0.2,
        system_prompt="You are a classification system. Categorize actions with high precision and consistency."
    ),
    
    "action_playbook": AgentDefinition(
        id="action_playbook",
        name="Action Playbook Agent",
        description="Generates and manages reusable action sequences",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.ACTION, AgentCapability.MEMORY],
        model="claude-3",
        temperature=0.5,
        system_prompt="You are a playbook management system. Create, optimize, and execute reusable action sequences.",
        memory_enabled=True
    ),
    
    "opportunity_analyst": AgentDefinition(
        id="opportunity_analyst",
        name="Opportunity Analyst Agent",
        description="Identifies and evaluates opportunities in data and market conditions",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.OPPORTUNITY, AgentCapability.ECONOMIC],
        model="claude-3",
        temperature=0.6,
        system_prompt="You are an opportunity detection system. Identify latent opportunities and evaluate their potential.",
        tools=["market_scan", "trend_analysis"]
    ),
    
    "causal_inference": AgentDefinition(
        id="causal_inference",
        name="Causal Inference Agent",
        description="Discovers and validates causal relationships",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.CAUSAL, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.3,
        system_prompt="You are a causal reasoning system. Discover, validate, and explain causal mechanisms.",
        tools=["causal_graph", "intervention_simulator"]
    ),
    
    "adversarial_test": AgentDefinition(
        id="adversarial_test",
        name="Adversarial Test Agent",
        description="Tests plans and strategies against worst-case scenarios",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.SIMULATION, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.8,
        system_prompt="You are an adversarial testing system. Challenge assumptions and expose vulnerabilities."
    ),
    
    "debate": AgentDefinition(
        id="debate",
        name="Debate Agent",
        description="Facilitates structured debate between multiple perspectives",
        tier=AgentTier.COMPOSITE,
        capabilities=[AgentCapability.DEBATE, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.7,
        system_prompt="You are a debate facilitation system. Ensure balanced, rigorous argumentation across perspectives.",
        dependencies=["critic", "consensus"]
    ),
    
    "critic": AgentDefinition(
        id="critic",
        name="Critic Agent",
        description="Critiques outputs for flaws, biases, and weaknesses",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.CRITIQUE, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.6,
        system_prompt="You are a critical evaluation system. Identify flaws, biases, and improvement opportunities."
    ),
    
    "consensus": AgentDefinition(
        id="consensus",
        name="Consensus Agent",
        description="Resolves conflicts and synthesizes agreement",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.CONSENSUS, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.4,
        system_prompt="You are a consensus building system. Identify common ground and synthesize agreement."
    ),
    
    "uncertainty": AgentDefinition(
        id="uncertainty",
        name="Uncertainty Agent",
        description="Quantifies and communicates uncertainty in predictions",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.UNCERTAINTY],
        model="claude-3",
        temperature=0.3,
        system_prompt="You are an uncertainty quantification system. Express confidence levels and confidence intervals explicitly."
    ),
    
    "economic": AgentDefinition(
        id="economic",
        name="Economic Agent",
        description="Analyzes economic impact and optimizes resource allocation",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.ECONOMIC],
        model="claude-3",
        temperature=0.4,
        system_prompt="You are an economic analysis system. Optimize for ROI, cost-effectiveness, and resource efficiency.",
        tools=["roi_calculator", "cost_benefit", "resource_allocator"]
    ),
    
    "dream": AgentDefinition(
        id="dream",
        name="Dream Agent",
        description="Generates creative insights through simulated dreaming",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.DREAM, AgentCapability.MEMORY],
        model="claude-3",
        temperature=0.9,
        system_prompt="You are a creative insight generation system. Explore unconventional connections and emergent patterns.",
        memory_enabled=True,
        dependencies=["memory_enabled"]
    ),
    
    "premonition": AgentDefinition(
        id="premonition",
        name="Premonition Agent",
        description="Predicts future events based on pattern recognition",
        tier=AgentTier.SPECIALIZED,
        capabilities=[AgentCapability.PREMONITION, AgentCapability.REASONING],
        model="claude-3",
        temperature=0.6,
        system_prompt="You are a predictive analysis system. Identify early signals and forecast likely outcomes.",
        dependencies=["causal_inference", "uncertainty"]
    ),
    
    "ethics": AgentDefinition(
        id="ethics",
        name="Ethics Agent",
        description="Evaluates actions against ethical frameworks",
        tier=AgentTier.META,
        capabilities=[AgentCapability.ETHICS],
        model="claude-3",
        temperature=0.3,
        system_prompt="You are an ethical evaluation system. Assess actions against fairness, transparency, and harm reduction.",
        ethical_constraints=["do_no_harm", "fairness", "transparency", "autonomy"]
    )
}

def get_agent_definition(agent_id: str) -> Optional[AgentDefinition]:
    return AGENT_REGISTRY.get(agent_id)

def list_agents(
    tier: Optional[AgentTier] = None,
    capability: Optional[AgentCapability] = None
) -> List[AgentDefinition]:
    agents = list(AGENT_REGISTRY.values())
    
    if tier:
        agents = [a for a in agents if a.tier == tier]
    
    if capability:
        agents = [a for a in agents if capability in a.capabilities]
    
    return agents

def get_agent_dependencies(agent_id: str) -> List[str]:
    agent = get_agent_definition(agent_id)
    return agent.dependencies if agent else []

def get_agent_fallbacks(agent_id: str) -> List[str]:
    agent = get_agent_definition(agent_id)
    return agent.fallback_agents if agent else []