"""Organizational graph for modeling company structures and relationships."""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OrgNode:
    id: str
    name: str
    node_type: str  # company, department, team, person, role
    properties: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrgRelationship:
    source_id: str
    target_id: str
    relationship_type: str  # reports_to, collaborates_with, manages, owns
    strength: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)


class OrgGraph:
    """Organizational graph for modeling company structures."""

    def __init__(self, name: str = "Organization"):
        self.name = name
        self.nodes: Dict[str, OrgNode] = {}
        self.relationships: List[OrgRelationship] = []
        self.created_at = datetime.utcnow()

    def add_node(
        self,
        node_id: str,
        name: str,
        node_type: str,
        parent_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> OrgNode:
        """Add a node to the organizational graph."""
        node = OrgNode(
            id=node_id,
            name=name,
            node_type=node_type,
            parent_id=parent_id,
            properties=properties or {}
        )
        self.nodes[node_id] = node

        # Add to parent's children
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children.append(node_id)

        return node

    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        strength: float = 1.0,
        properties: Optional[Dict[str, Any]] = None
    ) -> OrgRelationship:
        """Add a relationship between nodes."""
        rel = OrgRelationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            strength=strength,
            properties=properties or {}
        )
        self.relationships.append(rel)
        return rel

    def get_node(self, node_id: str) -> Optional[OrgNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_children(self, node_id: str) -> List[OrgNode]:
        """Get direct children of a node."""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[cid] for cid in node.children if cid in self.nodes]

    def get_hierarchy(self, node_id: str) -> List[OrgNode]:
        """Get the full hierarchy from root to a node."""
        hierarchy = []
        current_id = node_id
        while current_id:
            node = self.nodes.get(current_id)
            if not node:
                break
            hierarchy.insert(0, node)
            current_id = node.parent_id
        return hierarchy

    def get_relationships(
        self,
        node_id: str,
        relationship_type: Optional[str] = None
    ) -> List[OrgRelationship]:
        """Get relationships for a node."""
        rels = [r for r in self.relationships if r.source_id == node_id or r.target_id == node_id]
        if relationship_type:
            rels = [r for r in rels if r.relationship_type == relationship_type]
        return rels

    def find_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Find the shortest path between two nodes."""
        if source_id == target_id:
            return [source_id]

        visited: Set[str] = set()
        queue = [(source_id, [source_id])]

        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            node = self.nodes.get(current)
            if not node:
                continue

            # Check parent and children
            neighbors = node.children.copy()
            if node.parent_id:
                neighbors.append(node.parent_id)

            for neighbor in neighbors:
                if neighbor == target_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the organizational graph."""
        type_counts = {}
        for node in self.nodes.values():
            type_counts[node.node_type] = type_counts.get(node.node_type, 0) + 1

        rel_type_counts = {}
        for rel in self.relationships:
            rel_type_counts[rel.relationship_type] = rel_type_counts.get(rel.relationship_type, 0) + 1

        return {
            "name": self.name,
            "total_nodes": len(self.nodes),
            "total_relationships": len(self.relationships),
            "node_types": type_counts,
            "relationship_types": rel_type_counts,
            "root_nodes": [n.id for n in self.nodes.values() if n.parent_id is None]
        }