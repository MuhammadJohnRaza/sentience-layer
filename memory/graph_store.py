import asyncio
import uuid
from typing import Optional, Dict, Any, List, Set
from dataclasses import dataclass, field
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class GraphNode:
    id: str
    label: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    relation: str
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)

class MemoryGraphStore:
    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}
        self._adjacency: Dict[str, Dict[str, List[str]]] = {}
        self._lock = asyncio.Lock()

    async def add_node(
        self,
        label: str,
        node_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        node_id = f"node_{uuid.uuid4().hex[:12]}"
        
        node = GraphNode(
            id=node_id,
            label=label,
            type=node_type,
            properties=properties or {}
        )
        
        async with self._lock:
            self._nodes[node_id] = node
            self._adjacency[node_id] = {"outgoing": [], "incoming": []}
        
        logger.info(f"Graph node added: {node_id}")
        return node_id

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 1.0,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        if source_id not in self._nodes or target_id not in self._nodes:
            raise ValueError("Source or target node not found")
        
        edge_id = f"edge_{uuid.uuid4().hex[:12]}"
        
        edge = GraphEdge(
            id=edge_id,
            source=source_id,
            target=target_id,
            relation=relation,
            weight=weight,
            properties=properties or {}
        )
        
        async with self._lock:
            self._edges[edge_id] = edge
            self._adjacency[source_id]["outgoing"].append(edge_id)
            self._adjacency[target_id]["incoming"].append(edge_id)
        
        logger.info(f"Graph edge added: {edge_id}")
        return edge_id

    async def get_subgraph(
        self,
        center_node: Optional[str] = None,
        depth: int = 2
    ) -> Dict[str, Any]:
        if center_node and center_node not in self._nodes:
            return {"nodes": [], "edges": []}
        
        if not center_node:
            return {
                "nodes": [self._node_to_dict(n) for n in self._nodes.values()],
                "edges": [self._edge_to_dict(e) for e in self._edges.values()]
            }
        
        visited_nodes: Set[str] = {center_node}
        visited_edges: Set[str] = set()
        current_layer = {center_node}
        
        for _ in range(depth):
            next_layer: Set[str] = set()
            
            for node_id in current_layer:
                edge_ids = (
                    self._adjacency[node_id]["outgoing"] +
                    self._adjacency[node_id]["incoming"]
                )
                
                for edge_id in edge_ids:
                    if edge_id in self._edges:
                        edge = self._edges[edge_id]
                        visited_edges.add(edge_id)
                        next_layer.add(edge.source)
                        next_layer.add(edge.target)
            
            visited_nodes.update(next_layer)
            current_layer = next_layer
        
        return {
            "nodes": [self._node_to_dict(self._nodes[nid]) for nid in visited_nodes if nid in self._nodes],
            "edges": [self._edge_to_dict(self._edges[eid]) for eid in visited_edges if eid in self._edges]
        }

    async def find_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> Optional[List[str]]:
        if source_id not in self._nodes or target_id not in self._nodes:
            return None
        
        visited: Set[str] = set()
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target_id:
                return path
            
            if len(path) > max_depth:
                continue
            
            visited.add(current)
            
            for edge_id in self._adjacency[current]["outgoing"]:
                edge = self._edges.get(edge_id)
                if edge and edge.target not in visited:
                    queue.append((edge.target, path + [edge.target]))
        
        return None

    async def get_node_neighbors(
        self,
        node_id: str
    ) -> List[Dict[str, Any]]:
        if node_id not in self._nodes:
            return []
        
        edge_ids = (
            self._adjacency[node_id]["outgoing"] +
            self._adjacency[node_id]["incoming"]
        )
        
        neighbors = []
        for edge_id in edge_ids:
            edge = self._edges.get(edge_id)
            if not edge:
                continue
            
            other_id = edge.target if edge.source == node_id else edge.source
            other = self._nodes.get(other_id)
            
            if other:
                neighbors.append({
                    "node": self._node_to_dict(other),
                    "relation": edge.relation,
                    "weight": edge.weight,
                    "direction": "outgoing" if edge.source == node_id else "incoming"
                })
        
        return neighbors

    async def delete_node(self, node_id: str) -> bool:
        async with self._lock:
            if node_id not in self._nodes:
                return False
            
            edge_ids = (
                self._adjacency[node_id]["outgoing"] +
                self._adjacency[node_id]["incoming"]
            )
            
            for edge_id in edge_ids:
                await self.delete_edge(edge_id)
            
            del self._adjacency[node_id]
            del self._nodes[node_id]
            
            logger.info(f"Graph node deleted: {node_id}")
            return True

    async def delete_edge(self, edge_id: str) -> bool:
        async with self._lock:
            if edge_id not in self._edges:
                return False
            
            edge = self._edges[edge_id]
            
            self._adjacency[edge.source]["outgoing"] = [
                eid for eid in self._adjacency[edge.source]["outgoing"]
                if eid != edge_id
            ]
            self._adjacency[edge.target]["incoming"] = [
                eid for eid in self._adjacency[edge.target]["incoming"]
                if eid != edge_id
            ]
            
            del self._edges[edge_id]
            return True

    def _node_to_dict(self, node: GraphNode) -> Dict[str, Any]:
        return {
            "id": node.id,
            "label": node.label,
            "type": node.type,
            "properties": node.properties
        }

    def _edge_to_dict(self, edge: GraphEdge) -> Dict[str, Any]:
        return {
            "id": edge.id,
            "source": edge.source,
            "target": edge.target,
            "relation": edge.relation,
            "weight": edge.weight,
            "properties": edge.properties
        }

    async def get_stats(self) -> Dict[str, Any]:
        return {
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "density": len(self._edges) / (len(self._nodes) * (len(self._nodes) - 1)) if len(self._nodes) > 1 else 0
        }