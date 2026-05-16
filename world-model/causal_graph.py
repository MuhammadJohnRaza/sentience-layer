import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
import numpy as np

@dataclass
class CausalEdge:
    source: str
    target: str
    strength: float
    mechanism: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5

@dataclass
class Intervention:
    target: str
    action: str
    expected_effect: Dict[str, float]
    confidence: float = 0.5

class CausalGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.edges: Dict[Tuple[str, str], CausalEdge] = {}
        self.interventions: List[Intervention] = []
        self.confidence_threshold = 0.3
        
    def add_node(self, node_id: str, attributes: Dict[str, Any] = None):
        self.graph.add_node(node_id, **(attributes or {}))
        
    def add_edge(
        self, 
        source: str, 
        target: str, 
        strength: float,
        mechanism: str = "",
        evidence: List[str] = None,
        confidence: float = 0.5
    ):
        self.graph.add_edge(source, target, weight=strength)
        self.edges[(source, target)] = CausalEdge(
            source=source,
            target=target,
            strength=strength,
            mechanism=mechanism,
            evidence=evidence or [],
            confidence=confidence
        )
        
    def get_causes(self, node: str) -> List[str]:
        return list(self.graph.predecessors(node))
        
    def get_effects(self, node: str) -> List[str]:
        return list(self.graph.successors(node))
        
    def find_paths(
        self, 
        source: str, 
        target: str, 
        max_length: int = 5
    ) -> List[List[str]]:
        try:
            paths = list(
                nx.all_simple_paths(
                    self.graph, source, target, cutoff=max_length
                )
            )
            return paths
        except nx.NetworkXNoPath:
            return []
            
    def estimate_effect(
        self, 
        intervention: str, 
        outcome: str
    ) -> Dict[str, float]:
        paths = self.find_paths(intervention, outcome)
        
        if not paths:
            return {"effect": 0.0, "confidence": 0.0, "paths": 0}
            
        total_effect = 0.0
        path_effects = []
        
        for path in paths:
            path_strength = 1.0
            for i in range(len(path) - 1):
                edge = self.edges.get((path[i], path[i+1]))
                if edge:
                    path_strength *= edge.strength * edge.confidence
                    
            path_effects.append(path_strength)
            total_effect += path_strength
            
        avg_effect = total_effect / len(paths)
        
        return {
            "effect": min(1.0, avg_effect),
            "confidence": min(1.0, len(paths) * 0.2),
            "paths": len(paths),
            "path_details": path_effects
        }
        
    def simulate_intervention(
        self, 
        target: str, 
        magnitude: float
    ) -> Dict[str, float]:
        effects = {}
        
        for node in self.graph.nodes():
            if node != target:
                result = self.estimate_effect(target, node)
                if result["effect"] > self.confidence_threshold:
                    effects[node] = result["effect"] * magnitude
                    
        return effects
        
    def detect_confounders(self, cause: str, effect: str) -> List[str]:
        confounders = []
        
        for node in self.graph.nodes():
            if node == cause or node == effect:
                continue
                
            has_path_to_cause = nx.has_path(self.graph, node, cause)
            has_path_to_effect = nx.has_path(self.graph, node, effect)
            
            if has_path_to_cause and has_path_to_effect:
                confounders.append(node)
                
        return confounders
        
    def get_backdoor_paths(self, treatment: str, outcome: str) -> List[List[str]]:
        undirected = self.graph.to_undirected()
        all_paths = list(nx.all_simple_paths(undirected, treatment, outcome))
        
        backdoor_paths = []
        for path in all_paths:
            if len(path) > 2 and path[1] in self.graph.predecessors(treatment):
                backdoor_paths.append(path)
                
        return backdoor_paths
        
    def calculate_average_causal_effect(
        self, 
        treatment: str, 
        outcome: str
    ) -> float:
        direct_effect = 0.0
        if (treatment, outcome) in self.edges:
            direct_effect = self.edges[(treatment, outcome)].strength
            
        indirect_effects = []
        for path in self.find_paths(treatment, outcome):
            if len(path) > 2:
                strength = 1.0
                for i in range(len(path) - 1):
                    edge = self.edges.get((path[i], path[i+1]))
                    if edge:
                        strength *= edge.strength
                indirect_effects.append(strength)
                
        total = direct_effect + sum(indirect_effects)
        return min(1.0, total)
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": list(self.graph.nodes(data=True)),
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "strength": e.strength,
                    "mechanism": e.mechanism,
                    "confidence": e.confidence
                }
                for e in self.edges.values()
            ]
        }