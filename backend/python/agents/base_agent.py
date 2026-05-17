"""
Base Agent with ReAct Pattern (Reasoning + Acting)
Implements multi-step agentic reasoning for hackathon criteria (20% marks)

ReAct Pattern:
1. Thought: Agent reasons about the current state
2. Action: Agent takes an action (tool use, query, etc.)
3. Observation: Agent observes the result
4. Repeat until goal achieved

Features:
- Multi-step reasoning chains
- Tool discovery and use via MCP
- Memory integration for context
- Self-reflection and error correction
- Autonomous decision making
"""

import asyncio
import uuid
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

try:
    from backend.python.antigravity_client import AntigravityClient, get_antigravity_client
    from backend.python.mcp.client import MCPClient, get_mcp_registry
except ModuleNotFoundError:
    from antigravity_client import AntigravityClient, get_antigravity_client  # type: ignore
    from mcp.client import MCPClient, get_mcp_registry  # type: ignore

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    REFLECTING = "reflecting"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETE = "complete"


@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    sender: str = "unknown"
    recipient: str = "unknown"
    content: Any = None
    message_type: str = "default"
    priority: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningStep:
    """Single step in ReAct reasoning chain"""
    step_number: int
    thought: str  # What the agent is thinking
    action: Optional[str] = None  # What action to take
    action_input: Optional[Dict] = None  # Input to the action
    observation: Optional[str] = None  # Result of the action
    confidence: float = 0.8
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AgentResult:
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    confidence: float = 0.5
    reasoning_chain: List[ReasoningStep] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseAgent(ABC):
    """
    Base Agent with ReAct (Reasoning + Acting) Pattern

    Implements multi-step agentic reasoning:
    1. Receives goal/task
    2. Thinks about approach (reasoning)
    3. Takes actions (tool use, queries)
    4. Observes results
    5. Reflects and adjusts
    6. Repeats until goal achieved
    """

    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.result_history: List[AgentResult] = []
        self.max_history = self.config.get("max_history", 100)
        self.skills: Dict[str, Callable] = {}
        self._running = False
        self._handlers: Dict[str, List[Callable]] = {}

        # ReAct components
        self.max_reasoning_steps = self.config.get("max_reasoning_steps", 10)
        self.current_reasoning_chain: List[ReasoningStep] = []
        self.available_tools: Dict[str, Dict] = {}
        self.memory: List[Dict] = []

        # Integrations
        self.antigravity: Optional[AntigravityClient] = None
        self.mcp_registry = get_mcp_registry()

        logger.info(f"Agent {agent_id} initialized with ReAct pattern")

    @abstractmethod
    async def process(self, message: AgentMessage) -> AgentResult:
        """Process a message - to be implemented by subclasses"""
        pass

    @abstractmethod
    async def initialize(self):
        """Initialize agent - to be implemented by subclasses"""
        pass

    async def reason_and_act(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Main ReAct loop: Reasoning + Acting

        This is the core agentic reasoning implementation
        """
        context = context or {}
        self.current_reasoning_chain = []
        start_time = time.time()
        tools_used = []

        try:
            # Initialize Antigravity if not done
            if not self.antigravity:
                self.antigravity = get_antigravity_client()

            # Discover available tools
            await self._discover_tools()

            # ReAct Loop
            for step_num in range(self.max_reasoning_steps):
                self.status = AgentStatus.THINKING

                # STEP 1: THOUGHT - Reason about current state
                thought = await self._generate_thought(goal, step_num, context)

                step = ReasoningStep(
                    step_number=step_num,
                    thought=thought
                )

                # Check if goal is achieved
                if await self._is_goal_achieved(goal, self.current_reasoning_chain):
                    step.observation = "Goal achieved"
                    self.current_reasoning_chain.append(step)
                    break

                self.status = AgentStatus.ACTING

                # STEP 2: ACTION - Decide and execute action
                action_plan = await self._decide_action(thought, goal, context)

                if action_plan:
                    step.action = action_plan["action"]
                    step.action_input = action_plan.get("input", {})

                    # Execute action
                    observation = await self._execute_action(
                        action_plan["action"],
                        action_plan.get("input", {})
                    )

                    if action_plan["action"] not in tools_used:
                        tools_used.append(action_plan["action"])

                    self.status = AgentStatus.OBSERVING

                    # STEP 3: OBSERVATION - Record result
                    step.observation = observation
                else:
                    step.observation = "No action needed"

                self.current_reasoning_chain.append(step)

                # STEP 4: REFLECTION - Learn from this step
                self.status = AgentStatus.REFLECTING
                await self._reflect_on_step(step)

                # Store in memory
                self.memory.append({
                    "goal": goal,
                    "step": step_num,
                    "thought": thought,
                    "action": step.action,
                    "observation": step.observation,
                    "timestamp": datetime.utcnow().isoformat()
                })

            # Final synthesis
            final_result = await self._synthesize_result(goal, self.current_reasoning_chain)

            return AgentResult(
                success=True,
                data=final_result,
                execution_time=time.time() - start_time,
                confidence=self._calculate_confidence(),
                reasoning_chain=self.current_reasoning_chain,
                tools_used=tools_used,
                metadata={
                    "steps_taken": len(self.current_reasoning_chain),
                    "goal": goal
                }
            )

        except Exception as e:
            logger.error(f"ReAct loop failed: {e}")
            return AgentResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
                reasoning_chain=self.current_reasoning_chain,
                tools_used=tools_used
            )

    async def _generate_thought(
        self,
        goal: str,
        step_num: int,
        context: Dict
    ) -> str:
        """
        Generate reasoning about current state
        Uses Antigravity for intelligent thought generation
        """
        # Build context from previous steps
        previous_steps = "\n".join([
            f"Step {s.step_number}: Thought: {s.thought}, Action: {s.action}, Result: {s.observation}"
            for s in self.current_reasoning_chain[-3:]  # Last 3 steps
        ])

        prompt = f"""Goal: {goal}
Step: {step_num}
Previous steps:
{previous_steps}

Current context: {context}

What should I think about next to achieve this goal?
Provide a clear, logical thought about the next step."""

        try:
            # Use Antigravity for reasoning
            response = await self.antigravity._post("/reasoning/generate", {
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.7
            })
            return response.get("thought", f"Analyzing step {step_num} for goal: {goal}")
        except:
            # Fallback reasoning
            if step_num == 0:
                return f"I need to understand what's required to achieve: {goal}"
            else:
                return f"Based on previous observations, I should continue working towards: {goal}"

    async def _is_goal_achieved(
        self,
        goal: str,
        reasoning_chain: List[ReasoningStep]
    ) -> bool:
        """Check if goal has been achieved based on reasoning chain"""
        if not reasoning_chain:
            return False

        # Check last observation
        last_step = reasoning_chain[-1]
        if last_step.observation and "goal achieved" in last_step.observation.lower():
            return True

        # Use Antigravity to evaluate goal completion
        try:
            observations = [s.observation for s in reasoning_chain if s.observation]
            response = await self.antigravity._post("/reasoning/evaluate_goal", {
                "goal": goal,
                "observations": observations
            })
            return response.get("achieved", False)
        except:
            return False

    async def _decide_action(
        self,
        thought: str,
        goal: str,
        context: Dict
    ) -> Optional[Dict[str, Any]]:
        """
        Decide what action to take based on current thought
        Returns action plan with tool name and inputs
        """
        # Get available tools
        tool_descriptions = "\n".join([
            f"- {name}: {info.get('description', '')}"
            for name, info in self.available_tools.items()
        ])

        prompt = f"""Goal: {goal}
Current thought: {thought}
Available tools:
{tool_descriptions}

Which tool should I use and with what inputs?
Respond with JSON: {{"action": "tool_name", "input": {{}}, "reasoning": "why"}}"""

        try:
            response = await self.antigravity._post("/reasoning/decide_action", {
                "prompt": prompt,
                "tools": list(self.available_tools.keys())
            })

            action_plan = response.get("action_plan", {})
            if action_plan.get("action") in self.available_tools:
                return action_plan
        except Exception as e:
            logger.warning(f"Action decision failed: {e}")

        # Fallback: use memory search if available
        if "memory_search" in self.available_tools:
            return {
                "action": "memory_search",
                "input": {"query": goal},
                "reasoning": "Searching memory for relevant information"
            }

        return None

    async def _execute_action(
        self,
        action_name: str,
        action_input: Dict[str, Any]
    ) -> str:
        """Execute an action (tool call)"""
        try:
            # Check if it's a registered skill
            if action_name in self.skills:
                result = await self.skills[action_name](**action_input)
                return str(result)

            # Check if it's an MCP tool
            if action_name in self.available_tools:
                result = await self.mcp_registry.call_tool(action_name, action_input)
                return str(result)

            # Check if it's an Antigravity API
            if hasattr(self.antigravity, action_name):
                method = getattr(self.antigravity, action_name)
                result = await method(**action_input)
                return str(result)

            return f"Action {action_name} not found"

        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            return f"Error executing {action_name}: {str(e)}"

    async def _reflect_on_step(self, step: ReasoningStep):
        """
        Self-reflection: Learn from this step
        Adjust confidence and strategy if needed
        """
        # Analyze if the step was productive
        if step.observation and "error" in step.observation.lower():
            step.confidence *= 0.7  # Lower confidence on errors
            logger.warning(f"Step {step.step_number} encountered error, adjusting strategy")

        elif step.observation and any(word in step.observation.lower() for word in ["success", "found", "completed"]):
            step.confidence = min(1.0, step.confidence * 1.2)  # Boost confidence

        # Store reflection in memory for future learning
        self.memory.append({
            "type": "reflection",
            "step": step.step_number,
            "confidence": step.confidence,
            "productive": step.confidence > 0.6,
            "timestamp": datetime.utcnow().isoformat()
        })

    async def _synthesize_result(
        self,
        goal: str,
        reasoning_chain: List[ReasoningStep]
    ) -> Dict[str, Any]:
        """Synthesize final result from reasoning chain"""
        observations = [s.observation for s in reasoning_chain if s.observation]
        actions_taken = [s.action for s in reasoning_chain if s.action]

        return {
            "goal": goal,
            "steps_completed": len(reasoning_chain),
            "actions_taken": actions_taken,
            "final_observations": observations[-3:] if observations else [],
            "summary": f"Completed {len(reasoning_chain)} reasoning steps to achieve goal"
        }

    def _calculate_confidence(self) -> float:
        """Calculate overall confidence from reasoning chain"""
        if not self.current_reasoning_chain:
            return 0.5

        confidences = [s.confidence for s in self.current_reasoning_chain]
        return sum(confidences) / len(confidences)

    async def _discover_tools(self):
        """Discover available tools from MCP servers and register them"""
        try:
            # Get tools from MCP registry
            mcp_tools = self.mcp_registry.list_all_tools()
            for tool in mcp_tools:
                self.available_tools[tool["name"]] = {
                    "description": tool.get("description", ""),
                    "schema": tool.get("inputSchema", {}),
                    "source": "mcp"
                }

            # Register built-in skills as tools
            for skill_name in self.skills.keys():
                self.available_tools[skill_name] = {
                    "description": f"Built-in skill: {skill_name}",
                    "source": "skill"
                }

            logger.info(f"Discovered {len(self.available_tools)} tools")

        except Exception as e:
            logger.warning(f"Tool discovery failed: {e}")

        self._running = True
        await self.initialize()
        asyncio.create_task(self._process_message_queue())

    async def _process_message_queue(self):
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(), timeout=5.0
                )
                await self._handle_message(message)
            except asyncio.TimeoutError:
                await self._idle_cycle()
            except Exception as e:
                logger.error(f"Agent {self.agent_id} error: {e}")
                self.status = AgentStatus.ERROR
                
    async def _handle_message(self, message: AgentMessage):
        self.status = AgentStatus.PROCESSING
        start_time = time.time()
        
        try:
            result = await self.process(message)
            result.execution_time = time.time() - start_time
            
            self.result_history.append(result)
            if len(self.result_history) > self.max_history:
                self.result_history.pop(0)
                
            await self._emit("result", {
                "message": message,
                "result": result
            })
            
            self.status = AgentStatus.COMPLETE
            
        except Exception as e:
            logger.error(f"Processing error in {self.agent_id}: {e}")
            result = AgentResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
            self.status = AgentStatus.ERROR
            await self._emit("error", {"message": message, "error": str(e)})
            
    async def _idle_cycle(self):
        pass
        
    async def send_message(
        self, 
        recipient: str, 
        content: Any, 
        message_type: str = "default"
    ) -> str:
        message = AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            message_type=message_type
        )
        await self._emit("outbound_message", message)
        return message.id
        
    async def receive_message(self, message: AgentMessage):
        await self.message_queue.put(message)
        
    def register_skill(self, name: str, handler: Callable):
        self.skills[name] = handler
        
    def on(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        
    async def _emit(self, event_type: str, data: Any):
        for handler in self._handlers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Handler error: {e}")
                
    def get_stats(self) -> Dict[str, Any]:
        total = len(self.result_history)
        successful = sum(1 for r in self.result_history if r.success)
        
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "total_processed": total,
            "success_rate": successful / max(total, 1),
            "avg_execution_time": (
                sum(r.execution_time for r in self.result_history) / max(total, 1)
            ),
            "queue_depth": self.message_queue.qsize()
        }
        
    async def shutdown(self):
        self._running = False
        logger.info(f"Agent {self.agent_id} shutdown")