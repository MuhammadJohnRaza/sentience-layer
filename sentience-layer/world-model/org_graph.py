import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field

@dataclass
class OrgNode:
    node_id: str
    node_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    relationships: List[str] = field(default_factory=list)

@dataclass
class InfluencePath:
    path: List[str]
    strength: float
    mechanism: str

class OrgGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, OrgNode] = {}
        self.influence_cache: Dict[Tuple[str, str], List[InfluencePath]] = {}
        
    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        attributes: Dict[str, Any] = None,
        parent: Optional[str] = None
    ):
        node = OrgNode(
            node_id=entity_id,
            node_type=entity_type,
            attributes=attributes or {}
        )
        self.nodes[entity_id] = node
        self.graph.add_node(entity_id, type=entity_type, **(attributes or {}))
        
        if parent and parent in self.nodes:
            self.add_relationship(parent, entity_id, "contains", 1.0)
            
    def add_relationship(
        self,
        source: str,
        target: str,
        rel_type: str,
        strength: float = 0.5,
        bidirectional: bool = False
    ):
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Both entities must exist in the graph")
            
        self.graph.add_edge(
            source, target,
            type=rel_type,
            strength=strength
        )
        
        self.nodes[source].relationships.append(target)
        
        if bidirectional:
            self.graph.add_edge(
                target, source,
                type=f"inverse_{rel_type}",
                strength=strength
            )
            self.nodes[target].relationships.append(source)
            
        self.influence_cache.clear()
        
    def get_influence_paths(
        self,
        source: str,
        target: str,
        max_depth: int = 5
    ) -> List[InfluencePath]:
        cache_key = (source, target)
        if cache_key in self.influence_cache:
            return self.influence_cache[cache_key]
            
        try:
            paths = list(nx.all_simple_paths(
                self.graph, source, target, cutoff=max_depth
            ))
        except nx.NetworkXNoPath:
            return []
            
        influence_paths = []
        for path in paths:
            strength = 1.0
            mechanism_parts = []
            
            for i in range(len(path) - 1):
                edge_data = self.graph.get_edge_data(path[i], path[i+1])
                if edge_data:
                    strength *= edge_data.get("strength", 0.5)
                    mechanism_parts.append(edge_data.get("type", "unknown"))
                    
            influence_paths.append(InfluencePath(
                path=path,
                strength=strength,
                mechanism=" -> ".join(mechanism_parts)
            ))
            
        self.influence_cache[cache_key] = influence_paths
        return influence_paths
        
    def find_key_influencers(self, target: str, top_n: int = 5) -> List[Dict[str, Any]]:
        predecessors = list(self.graph.predecessors(target))
        
        influencer_scores = []
        for pred in predecessors:
            edge_data = self.graph.get_edge_data(pred, target)
            strength = edge_data.get("strength", 0.5) if edge_data else 0.5
            
            indirect_paths = []
            for node in self.graph.nodes():
                if node != pred and node != target:
                    paths = self.get_influence_paths(pred, node)
                    indirect_paths.extend(paths)
                    
            indirect_influence = sum(p.strength for p in indirect_paths)
            
            score = strength + (indirect_influence * 0.3)
            influencer_scores.append({
                "entity_id": pred,
                "direct_strength": strength,
                "indirect_influence": indirect_influence,
                "total_score": score
            })
            
        influencer_scores.sort(key=lambda x: x["total_score"], reverse=True)
        return influencer_scores[:top_n]
        
    def get_subgraph(self, root: str, depth: int = 2) -> nx.DiGraph:
        nodes = {root}
        current = {root}
        
        for _ in range(depth):
            next_level = set()
            for node in current:
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            nodes.update(next_level)
            current = next_level
            
        return self.graph.subgraph(nodes).copy()
        
    def detect_cycles(self) -> List[List[str]]:
        return list(nx.simple_cycles(self.graph))
        
    def calculate_centrality(self) -> Dict[str, float]:
        return nx.betweenness_centrality(self.graph)
        
    def find_bottlenecks(self) -> List[str]:
        centrality = self.calculate_centrality()
        avg = sum(centrality.values()) / max(len(centrality), 1)
        return [node for node, score in centrality.items() if score > avg * 2]
        
    def get_department_metrics(self, dept_id: str) -> Dict[str, Any]:
        subgraph = self.get_subgraph(dept_id, depth=1)
        
        return {
            "size": subgraph.number_of_nodes(),
            "connections": subgraph.number_of_edges(),
            "density": nx.density(subgraph),
            "avg_clustering": nx.average_clustering(subgraph.to_undirected()),
            "is_connected": nx.is_weakly_connected(subgraph)
        }
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type,
                    "attributes": n.attributes
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    **data
                }
                for u, v, data in self.graph.edges(data=True)
            ]
        }