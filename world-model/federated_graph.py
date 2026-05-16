"""Federated graph management for distributed world model synchronization."""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class GraphNode:
    id: str
    node_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    source: str = "local"
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    edge_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    source: str = "local"


@dataclass
class SyncState:
    peer_id: str
    last_sync: datetime
    sync_hash: str
    pending_updates: List[Dict[str, Any]] = field(default_factory=list)


class FederatedGraph:
    """Manages a federated graph structure with sync capabilities."""

    def __init__(self, node_id: str = "default", config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.config = config or {}
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.peer_states: Dict[str, SyncState] = {}
        self.conflict_resolution = self.config.get("conflict_resolution", "last_write_wins")

    def add_node(self, node: GraphNode) -> None:
        """Add or update a node in the graph."""
        if node.id in self.nodes:
            existing = self.nodes[node.id]
            if self._should_update(existing, node):
                node.version = existing.version + 1
                self.nodes[node.id] = node
        else:
            self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the graph."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.edges = [e for e in self.edges if e.source_id != node_id and e.target_id != node_id]
            return True
        return False

    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph."""
        if edge.source_id in self.nodes and edge.target_id in self.nodes:
            self.edges.append(edge)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str, edge_type: Optional[str] = None) -> List[GraphNode]:
        """Get neighboring nodes."""
        neighbor_ids: Set[str] = set()
        for edge in self.edges:
            if edge.source_id == node_id:
                if edge_type is None or edge.edge_type == edge_type:
                    neighbor_ids.add(edge.target_id)
            elif edge.target_id == node_id:
                if edge_type is None or edge.edge_type == edge_type:
                    neighbor_ids.add(edge.source_id)
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]

    def get_state_hash(self) -> str:
        """Get a hash representing the current graph state."""
        state_str = f"{len(self.nodes)}:{len(self.edges)}:{max((n.version for n in self.nodes.values()), default=0)}"
        return hashlib.sha256(state_str.encode()).hexdigest()

    def sync_with_peer(self, peer_id: str, peer_state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize with a peer node."""
        local_hash = self.get_state_hash()
        peer_hash = peer_state.get("state_hash", "")

        if local_hash == peer_hash:
            return {"status": "synced", "changes": 0}

        # Exchange updates
        updates_sent = self._get_updates_since(peer_state.get("last_sync_hash", ""))
        updates_received = peer_state.get("updates", [])

        # Apply received updates
        changes = self._apply_updates(updates_received)

        # Update peer state
        self.peer_states[peer_id] = SyncState(
            peer_id=peer_id,
            last_sync=datetime.utcnow(),
            sync_hash=self.get_state_hash(),
            pending_updates=updates_sent
        )

        return {
            "status": "synced",
            "changes": changes,
            "updates_sent": len(updates_sent),
            "updates_received": len(updates_received)
        }

    def _should_update(self, existing: GraphNode, new: GraphNode) -> bool:
        """Determine if a node should be updated."""
        if self.conflict_resolution == "last_write_wins":
            return new.last_updated > existing.last_updated
        elif self.conflict_resolution == "higher_version_wins":
            return new.version > existing.version
        return True

    def _get_updates_since(self, since_hash: str) -> List[Dict[str, Any]]:
        """Get updates since a given state hash."""
        updates = []
        for node in self.nodes.values():
            updates.append({
                "type": "node",
                "action": "update",
                "data": {
                    "id": node.id,
                    "node_type": node.node_type,
                    "properties": node.properties,
                    "version": node.version,
                    "last_updated": node.last_updated.isoformat()
                }
            })
        return updates

    def _apply_updates(self, updates: List[Dict[str, Any]]) -> int:
        """Apply updates from a peer."""
        changes = 0
        for update in updates:
            if update["type"] == "node":
                data = update["data"]
                node = GraphNode(
                    id=data["id"],
                    node_type=data["node_type"],
                    properties=data["properties"],
                    version=data["version"]
                )
                if node.id in self.nodes:
                    if self._should_update(self.nodes[node.id], node):
                        self.nodes[node.id] = node
                        changes += 1
                else:
                    self.nodes[node.id] = node
                    changes += 1
        return changes

    def get_graph_summary(self) -> Dict[str, Any]:
        """Get a summary of the graph state."""
        return {
            "node_id": self.node_id,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "state_hash": self.get_state_hash(),
            "peer_count": len(self.peer_states),
            "node_types": dict(self._count_by_type(self.nodes.values(), lambda n: n.node_type)),
            "edge_types": dict(self._count_by_type(self.edges, lambda e: e.edge_type))
        }

    def _count_by_type(self, items, type_getter):
        counts = {}
        for item in items:
            t = type_getter(item)
            counts[t] = counts.get(t, 0) + 1
        return counts