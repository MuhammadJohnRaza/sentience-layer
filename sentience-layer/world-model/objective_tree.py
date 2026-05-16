from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class ObjectiveStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Objective:
    objective_id: str
    description: str
    parent_id: Optional[str] = None
    status: ObjectiveStatus = ObjectiveStatus.PENDING
    priority: float = 0.5
    progress: float = 0.0
    children: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: __import__('time').time())
    completed_at: Optional[float] = None

class ObjectiveTree:
    def __init__(self):
        self.objectives: Dict[str, Objective] = {}
        self.root_id: Optional[str] = None
        
    def add_objective(
        self,
        objective_id: str,
        description: str,
        parent_id: Optional[str] = None,
        priority: float = 0.5,
        dependencies: List[str] = None,
        metadata: Dict[str, Any] = None
    ):
        obj = Objective(
            objective_id=objective_id,
            description=description,
            parent_id=parent_id,
            priority=priority,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        
        self.objectives[objective_id] = obj
        
        if parent_id and parent_id in self.objectives:
            self.objectives[parent_id].children.append(objective_id)
        elif not self.root_id:
            self.root_id = objective_id
            
    def update_status(self, objective_id: str, status: ObjectiveStatus):
        if objective_id not in self.objectives:
            raise ValueError(f"Objective {objective_id} not found")
            
        obj = self.objectives[objective_id]
        obj.status = status
        
        if status == ObjectiveStatus.COMPLETED:
            import time
            obj.completed_at = time.time()
            obj.progress = 1.0
            self._propagate_progress(obj.parent_id)
        elif status == ObjectiveStatus.FAILED:
            self._handle_failure(objective_id)
            
    def update_progress(self, objective_id: str, progress: float):
        if objective_id not in self.objectives:
            raise ValueError(f"Objective {objective_id} not found")
            
        obj = self.objectives[objective_id]
        obj.progress = min(1.0, max(0.0, progress))
        
        if obj.progress >= 1.0:
            self.update_status(objective_id, ObjectiveStatus.COMPLETED)
        else:
            self._propagate_progress(obj.parent_id)
            
    def get_path(self, objective_id: str) -> List[Objective]:
        path = []
        current = objective_id
        
        while current:
            if current not in self.objectives:
                break
            obj = self.objectives[current]
            path.append(obj)
            current = obj.parent_id
            
        return list(reversed(path))
        
    def get_subtree(self, objective_id: str) -> List[Objective]:
        if objective_id not in self.objectives:
            return []
            
        result = [self.objectives[objective_id]]
        queue = list(self.objectives[objective_id].children)
        
        while queue:
            current = queue.pop(0)
            if current in self.objectives:
                result.append(self.objectives[current])
                queue.extend(self.objectives[current].children)
                
        return result
        
    def get_ready_objectives(self) -> List[Objective]:
        ready = []
        
        for obj_id, obj in self.objectives.items():
            if obj.status != ObjectiveStatus.PENDING:
                continue
                
            blocked = False
            for dep_id in obj.dependencies:
                if dep_id in self.objectives:
                    if self.objectives[dep_id].status != ObjectiveStatus.COMPLETED:
                        blocked = True
                        break
                        
            if not blocked:
                ready.append(obj)
                
        ready.sort(key=lambda x: x.priority, reverse=True)
        return ready
        
    def get_critical_path(self) -> List[str]:
        if not self.root_id:
            return []
            
        def path_duration(obj_id: str) -> float:
            obj = self.objectives.get(obj_id)
            if not obj:
                return 0.0
                
            duration = obj.metadata.get("estimated_duration", 1.0)
            
            if not obj.children:
                return duration
                
            child_durations = [path_duration(child) for child in obj.children]
            return duration + max(child_durations) if child_durations else duration
            
        def build_critical_path(obj_id: str) -> List[str]:
            obj = self.objectives.get(obj_id)
            if not obj or not obj.children:
                return [obj_id]
                
            child_paths = {
                child: path_duration(child)
                for child in obj.children
            }
            
            if not child_paths:
                return [obj_id]
                
            critical_child = max(child_paths, key=child_paths.get)
            return [obj_id] + build_critical_path(critical_child)
            
        return build_critical_path(self.root_id)
        
    def calculate_completion(self) -> float:
        if not self.objectives:
            return 0.0
            
        total_progress = sum(obj.progress for obj in self.objectives.values())
        return total_progress / len(self.objectives)
        
    def get_blocked_objectives(self) -> List[Dict[str, Any]]:
        blocked = []
        
        for obj_id, obj in self.objectives.items():
            if obj.status == ObjectiveStatus.BLOCKED:
                blockers = []
                for dep_id in obj.dependencies:
                    if dep_id in self.objectives:
                        dep = self.objectives[dep_id]
                        if dep.status != ObjectiveStatus.COMPLETED:
                            blockers.append({
                                "objective_id": dep_id,
                                "status": dep.status.value,
                                "progress": dep.progress
                            })
                            
                blocked.append({
                    "objective": obj,
                    "blockers": blockers
                })
                
        return blocked
        
    def _propagate_progress(self, parent_id: Optional[str]):
        if not parent_id or parent_id not in self.objectives:
            return
            
        parent = self.objectives[parent_id]
        if not parent.children:
            return
            
        child_progress = [
            self.objectives[child].progress
            for child in parent.children
            if child in self.objectives
        ]
        
        if child_progress:
            parent.progress = sum(child_progress) / len(child_progress)
            
        self._propagate_progress(parent.parent_id)
        
    def _handle_failure(self, objective_id: str):
        obj = self.objectives[objective_id]
        
        for child_id in obj.children:
            if child_id in self.objectives:
                self.objectives[child_id].status = ObjectiveStatus.BLOCKED
                
        if obj.parent_id and obj.parent_id in self.objectives:
            parent = self.objectives[obj.parent_id]
            if all(
                self.objectives[c].status == ObjectiveStatus.FAILED
                for c in parent.children
                if c in self.objectives
            ):
                self.update_status(obj.parent_id, ObjectiveStatus.FAILED)
                
    def to_dict(self) -> Dict[str, Any]:
        return {
            "root_id": self.root_id,
            "objectives": {
                obj_id: {
                    "objective_id": obj.objective_id,
                    "description": obj.description,
                    "parent_id": obj.parent_id,
                    "status": obj.status.value,
                    "priority": obj.priority,
                    "progress": obj.progress,
                    "children": obj.children,
                    "dependencies": obj.dependencies,
                    "metadata": obj.metadata
                }
                for obj_id, obj in self.objectives.items()
            },
            "overall_completion": self.calculate_completion()
        }