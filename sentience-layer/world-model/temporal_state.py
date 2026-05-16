import time
import copy
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class StateSnapshot:
    timestamp: float
    state: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
class TemporalState:
    """
    Manages the temporal evolution of the world model's state,
    supporting history tracking, rollbacks, and timeline queries.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.history: List[StateSnapshot] = []
        self.current_state: Dict[str, Any] = {}
        self.max_history = self.config.get("max_history", 1000)

    def initialize(self, initial_state: Optional[Dict[str, Any]] = None) -> bool:
        self.current_state = initial_state or {}
        self.record_snapshot(metadata={"event": "initialization"})
        return True

    def update_state(self, updates: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Applies updates to the current state and records a snapshot."""
        for k, v in updates.items():
            self.current_state[k] = v
        self.record_snapshot(metadata=metadata)

    def record_snapshot(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Records the current state into the history."""
        snapshot = StateSnapshot(
            timestamp=time.time(),
            state=copy.deepcopy(self.current_state),
            metadata=metadata or {}
        )
        self.history.append(snapshot)
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_state_at(self, timestamp: float) -> Optional[Dict[str, Any]]:
        """Finds the state at a specific timestamp (closest prior state)."""
        if not self.history:
            return None
            
        closest_snapshot = self.history[0]
        for snapshot in self.history:
            if snapshot.timestamp > timestamp:
                break
            closest_snapshot = snapshot
            
        return closest_snapshot.state
        
    def rollback(self, timestamp: float) -> bool:
        """Rolls back the current state to a previous point in time."""
        state = self.get_state_at(timestamp)
        if state is not None:
            self.current_state = copy.deepcopy(state)
            self.record_snapshot(metadata={"event": "rollback", "target_timestamp": timestamp})
            return True
        return False

    def compare_states(self, t1: float, t2: float) -> Dict[str, Any]:
        """Compares states between two timestamps."""
        state1 = self.get_state_at(t1) or {}
        state2 = self.get_state_at(t2) or {}
        
        all_keys = set(state1.keys()) | set(state2.keys())
        diff = {}
        for k in all_keys:
            v1 = state1.get(k)
            v2 = state2.get(k)
            if v1 != v2:
                diff[k] = {"from": v1, "to": v2}
                
        return diff
        
    def get_timeline(self, key: str) -> List[Dict[str, Any]]:
        """Returns the timeline of changes for a specific key."""
        timeline = []
        for snapshot in self.history:
            if key in snapshot.state:
                timeline.append({
                    "timestamp": snapshot.timestamp,
                    "value": snapshot.state[key],
                    "metadata": snapshot.metadata
                })
        return timeline

def get_instance() -> TemporalState:
    return TemporalState()