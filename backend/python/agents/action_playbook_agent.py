import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from .base_agent import BaseAgent, AgentMessage, AgentResult

@dataclass
class PlaybookStep:
    step_id: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    validation: List[str] = field(default_factory=list)
    rollback: Optional[str] = None
    timeout: int = 300

@dataclass
class Playbook:
    playbook_id: str
    name: str
    description: str
    steps: List[PlaybookStep] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    triggers: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

class ActionPlaybookAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str = "playbook",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(agent_id, config)
        self.playbooks: Dict[str, Playbook] = {}
        self.executions: Dict[str, Dict[str, Any]] = {}
        self.step_registry: Dict[str, callable] = {}
        self.template_engine = PlaybookTemplateEngine()
        
    async def initialize(self):
        self.register_skill("create", self._create_playbook)
        self.register_skill("execute", self._execute_playbook)
        self.register_skill("validate", self._validate_playbook)
        self.register_skill("generate", self._generate_from_goal)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        skill = message.metadata.get("skill", "execute")
        
        if skill == "create":
            return await self._create_playbook(message.content)
        elif skill == "execute":
            return await self._execute_playbook(
                message.content,
                message.metadata.get("variables", {})
            )
        elif skill == "validate":
            return await self._validate_playbook(message.content)
        elif skill == "generate":
            return await self._generate_from_goal(message.content)
        else:
            return AgentResult(
                success=False,
                error=f"Unknown skill: {skill}"
            )
            
    async def _create_playbook(
        self,
        spec: Dict[str, Any]
    ) -> AgentResult:
        steps = []
        for i, step_data in enumerate(spec.get("steps", [])):
            step = PlaybookStep(
                step_id=step_data.get("id", f"step_{i}"),
                action=step_data.get("action", ""),
                parameters=step_data.get("parameters", {}),
                validation=step_data.get("validation", []),
                rollback=step_data.get("rollback"),
                timeout=step_data.get("timeout", 300)
            )
            steps.append(step)
            
        playbook = Playbook(
            playbook_id=spec.get("id", f"pb_{len(self.playbooks)}"),
            name=spec.get("name", "Untitled"),
            description=spec.get("description", ""),
            steps=steps,
            variables=spec.get("variables", {}),
            triggers=spec.get("triggers", []),
            tags=spec.get("tags", [])
        )
        
        self.playbooks[playbook.playbook_id] = playbook
        
        return AgentResult(
            success=True,
            data={
                "playbook_id": playbook.playbook_id,
                "steps_count": len(steps),
                "created": True
            }
        )
        
    async def _execute_playbook(
        self,
        playbook_id: str,
        variables: Dict[str, Any]
    ) -> AgentResult:
        if playbook_id not in self.playbooks:
            return AgentResult(
                success=False,
                error=f"Playbook {playbook_id} not found"
            )
            
        playbook = self.playbooks[playbook_id]
        execution_id = f"exec_{playbook_id}_{len(self.executions)}"
        
        execution = {
            "id": execution_id,
            "playbook_id": playbook_id,
            "status": "running",
            "steps_completed": [],
            "steps_failed": [],
            "variables": {**playbook.variables, **variables},
            "start_time": __import__('time').time(),
            "log": []
        }
        
        self.executions[execution_id] = execution
        
        for step in playbook.steps:
            step_result = await self._execute_step(
                step, execution["variables"], execution_id
            )
            
            execution["log"].append({
                "step_id": step.step_id,
                "action": step.action,
                "result": step_result
            })
            
            if step_result["success"]:
                execution["steps_completed"].append(step.step_id)
            else:
                execution["steps_failed"].append(step.step_id)
                
                if step.rollback:
                    await self._execute_rollback(step, execution)
                    
                execution["status"] = "failed"
                break
                
        if not execution["steps_failed"]:
            execution["status"] = "completed"
            
        execution["duration"] = __import__('time').time() - execution["start_time"]
        
        return AgentResult(
            success=execution["status"] == "completed",
            data={
                "execution_id": execution_id,
                "status": execution["status"],
                "completed_steps": len(execution["steps_completed"]),
                "failed_steps": len(execution["steps_failed"]),
                "duration": execution["duration"]
            }
        )
        
    async def _validate_playbook(self, playbook_id: str) -> AgentResult:
        if playbook_id not in self.playbooks:
            return AgentResult(
                success=False,
                error=f"Playbook {playbook_id} not found"
            )
            
        playbook = self.playbooks[playbook_id]
        issues = []
        
        if not playbook.steps:
            issues.append("No steps defined")
            
        step_ids = set()
        for step in playbook.steps:
            if step.step_id in step_ids:
                issues.append(f"Duplicate step ID: {step.step_id}")
            step_ids.add(step.step_id)
            
            if not step.action:
                issues.append(f"Step {step.step_id} has no action")
                
            for param in step.parameters:
                if "{{" in str(step.parameters[param]):
                    var_name = re.search(r"\{\{(.*?)\}\}", str(step.parameters[param]))
                    if var_name:
                        var = var_name.group(1).strip()
                        if var not in playbook.variables:
                            issues.append(f"Undefined variable: {var}")
                            
        return AgentResult(
            success=len(issues) == 0,
            data={
                "playbook_id": playbook_id,
                "valid": len(issues) == 0,
                "issues": issues,
                "step_count": len(playbook.steps)
            }
        )
        
    async def _generate_from_goal(self, goal: str) -> AgentResult:
        generated_steps = self._decompose_goal(goal)
        
        playbook_spec = {
            "id": f"auto_{len(self.playbooks)}",
            "name": f"Auto-generated: {goal[:50]}",
            "description": goal,
            "steps": [
                {
                    "id": f"step_{i}",
                    "action": step["action"],
                    "parameters": step.get("parameters", {})
                }
                for i, step in enumerate(generated_steps)
            ],
            "tags": ["auto-generated"]
        }
        
        return await self._create_playbook(playbook_spec)
        
    async def _execute_step(
        self,
        step: PlaybookStep,
        variables: Dict[str, Any],
        execution_id: str
    ) -> Dict[str, Any]:
        resolved_params = {}
        for key, value in step.parameters.items():
            if isinstance(value, str):
                resolved = self.template_engine.render(value, variables)
                resolved_params[key] = resolved
            else:
                resolved_params[key] = value
                
        handler = self.step_registry.get(step.action)
        
        if handler:
            try:
                result = await handler(resolved_params)
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "data": {"action": step.action, "params": resolved_params},
                "note": "No handler registered, simulated"
            }
            
    async def _execute_rollback(
        self,
        step: PlaybookStep,
        execution: Dict[str, Any]
    ):
        if step.rollback:
            handler = self.step_registry.get(step.rollback)
            if handler:
                await handler({"execution_id": execution["id"]})
                
    def _decompose_goal(self, goal: str) -> List[Dict[str, Any]]:
        patterns = [
            (r"create|build|make", "create_resource"),
            (r"update|modify|change", "update_resource"),
            (r"delete|remove|clean", "delete_resource"),
            (r"analyze|evaluate|assess", "analyze_data"),
            (r"notify|alert|inform", "send_notification"),
            (r"deploy|release|publish", "deploy_artifact")
        ]
        
        steps = []
        for pattern, action in patterns:
            if re.search(pattern, goal, re.IGNORECASE):
                steps.append({
                    "action": action,
                    "parameters": {"context": goal}
                })
                
        if not steps:
            steps.append({
                "action": "process_generic",
                "parameters": {"input": goal}
            })
            
        return steps
        
    def register_step_handler(self, action: str, handler: callable):
        self.step_registry[action] = handler
        
    def get_execution_report(self, execution_id: str) -> Optional[Dict[str, Any]]:
        return self.executions.get(execution_id)

class PlaybookTemplateEngine:
    def render(self, template: str, variables: Dict[str, Any]) -> str:
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{ {key} }}}}"
            result = result.replace(placeholder, str(value))
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result