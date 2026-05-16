"""Objective tree for hierarchical goal decomposition and tracking."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ObjectiveStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    ABANDONED = "abandoned"


class ObjectivePriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Objective:
    id: str
    name: str
    description: str = ""
    status: ObjectiveStatus = ObjectiveStatus.NOT_STARTED
    priority: ObjectivePriority = ObjectivePriority.MEDIUM
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class ObjectiveTree:
    """Hierarchical objective tree for goal management."""

    def __init__(self, root_name: str = "Root Objective"):
        self.objectives: Dict[str, Objective] = {}
        self.root_id = "root"
        self.root = Objective(
            id=self.root_id,
            name=root_name,
            status=ObjectiveStatus.IN_PROGRESS
        )
        self.objectives[self.root_id] = self.root

    def add_objective(
        self,
        name: str,
        parent_id: Optional[str] = None,
        description: str = "",
        priority: ObjectivePriority = ObjectivePriority.MEDIUM
    ) -> Objective:
        """Add a new objective to the tree."""
        obj_id = f"obj_{len(self.objectives)}_{name.lower().replace(' ', '_')}"
        objective = Objective(
            id=obj_id,
            name=name,
            description=description,
            priority=priority,
            parent_id=parent_id or self.root_id
        )
        self.objectives[obj_id] = objective

        # Add to parent's children
        parent = self.objectives.get(objective.parent_id)
        if parent:
            parent.children.append(obj_id)
            parent.updated_at = datetime.utcnow()

        return objective

    def get_objective(self, obj_id: str) -> Optional[Objective]:
        """Get an objective by ID."""
        return self.objectives.get(obj_id)

    def update_progress(self, obj_id: str, progress: float) -> None:
        """Update the progress of an objective."""
        objective = self.objectives.get(obj_id)
        if objective:
            objective.progress = min(100.0, max(0.0, progress))
            objective.updated_at = datetime.utcnow()

            # Update status based on progress
            if progress >= 100:
                objective.status = ObjectiveStatus.COMPLETED
            elif progress > 0:
                objective.status = ObjectiveStatus.IN_PROGRESS

            # Propagate progress up the tree
            self._update_parent_progress(obj_id)

    def _update_parent_progress(self, obj_id: str) -> None:
        """Recursively update parent progress."""
        objective = self.objectives.get(obj_id)
        if objective and objective.parent_id:
            parent = self.objectives.get(objective.parent_id)
            if parent and parent.children:
                # Calculate parent progress as average of children
                children_progress = [
                    self.objectives[cid].progress
                    for cid in parent.children
                    if cid in self.objectives
                ]
                if children_progress:
                    parent.progress = sum(children_progress) / len(children_progress)
                    parent.updated_at = datetime.utcnow()
                self._update_parent_progress(parent.id)

    def get_tree(self) -> Dict[str, Any]:
        """Get the full objective tree as a nested dictionary."""
        return self._build_tree_dict(self.root_id)

    def _build_tree_dict(self, obj_id: str) -> Dict[str, Any]:
        """Build a nested dictionary representation of the tree."""
        objective = self.objectives.get(obj_id)
        if not objective:
            return {}

        return {
            "id": objective.id,
            "name": objective.name,
            "description": objective.description,
            "status": objective.status.value,
            "priority": objective.priority.value,
            "progress": objective.progress,
            "children": [self._build_tree_dict(cid) for cid in objective.children]
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the objective tree."""
        total = len(self.objectives) - 1  # Exclude root
        status_counts = {}
        for obj in self.objectives.values():
            if obj.id == self.root_id:
                continue
            status_counts[obj.status.value] = status_counts.get(obj.status.value, 0) + 1

        return {
            "total_objectives": total,
            "status_breakdown": status_counts,
            "overall_progress": self.root.progress,
            "root_status": self.root.status.value
        }