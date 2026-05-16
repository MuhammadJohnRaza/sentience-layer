"""Temporal state management for time-based world model updates."""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class TimeGranularity(Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


@dataclass
class StateSnapshot:
    timestamp: datetime
    state_data: Dict[str, Any]
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalEvent:
    event_type: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    confidence: float = 1.0


class TemporalState:
    """Manages temporal state with time-based snapshots and trend analysis."""

    def __init__(self, max_history: int = 1000, config: Optional[Dict[str, Any]] = None):
        self.max_history = max_history
        self.config = config or {}
        self.snapshots: List[StateSnapshot] = []
        self.events: List[TemporalEvent] = []
        self.current_state: Dict[str, Any] = {}
        self.state_version: int = 0

    def update_state(self, updates: Dict[str, Any], timestamp: Optional[datetime] = None) -> StateSnapshot:
        """Update the current state and create a snapshot."""
        if timestamp is None:
            timestamp = datetime.utcnow()

        # Apply updates
        self.current_state.update(updates)
        self.state_version += 1

        # Create snapshot
        snapshot = StateSnapshot(
            timestamp=timestamp,
            state_data=self.current_state.copy(),
            version=self.state_version
        )
        self.snapshots.append(snapshot)

        # Trim history if needed
        if len(self.snapshots) > self.max_history:
            self.snapshots = self.snapshots[-self.max_history:]

        return snapshot

    def add_event(self, event: TemporalEvent) -> None:
        """Add a temporal event."""
        self.events.append(event)
        # Trim if needed
        if len(self.events) > self.max_history:
            self.events = self.events[-self.max_history:]

    def get_state_at_time(self, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Get the state at a specific point in time."""
        # Find the closest snapshot before the timestamp
        for snapshot in reversed(self.snapshots):
            if snapshot.timestamp <= timestamp:
                return snapshot.state_data
        return None

    def get_state_changes(
        self,
        start_time: datetime,
        end_time: Optional[datetime] = None
    ) -> List[StateSnapshot]:
        """Get all state changes within a time range."""
        if end_time is None:
            end_time = datetime.utcnow()

        return [
            s for s in self.snapshots
            if start_time <= s.timestamp <= end_time
        ]

    def get_events_in_range(
        self,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None
    ) -> List[TemporalEvent]:
        """Get events within a time range."""
        if end_time is None:
            end_time = datetime.utcnow()

        events = [
            e for e in self.events
            if start_time <= e.timestamp <= end_time
        ]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events

    def calculate_trend(
        self,
        key: str,
        granularity: TimeGranularity,
        periods: int = 10
    ) -> List[Tuple[datetime, float]]:
        """Calculate trend for a specific state key."""
        if key not in self.current_state:
            return []

        # Group snapshots by granularity
        grouped = self._group_by_granularity(granularity, periods)
        trend = []

        for timestamp, snapshots in grouped:
            values = [s.state_data.get(key, 0) for s in snapshots if key in s.state_data]
            if values:
                avg = sum(values) / len(values)
                trend.append((timestamp, avg))

        return trend

    def detect_anomalies(
        self,
        key: str,
        window_size: int = 10,
        threshold: float = 2.0
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in state values using statistical methods."""
        anomalies = []
        values = []

        for snapshot in self.snapshots[-window_size * 2:]:
            if key in snapshot.state_data:
                value = snapshot.state_data[key]
                values.append((snapshot.timestamp, value))

        if len(values) < window_size:
            return anomalies

        # Calculate rolling statistics
        for i in range(window_size, len(values)):
            window = values[i - window_size:i]
            window_values = [v[1] for v in window]
            mean = sum(window_values) / len(window_values)
            std = (sum((v - mean) ** 2 for v in window_values) / len(window_values)) ** 0.5

            current_value = values[i][1]
            if std > 0 and abs(current_value - mean) > threshold * std:
                anomalies.append({
                    "timestamp": values[i][0],
                    "value": current_value,
                    "mean": mean,
                    "std": std,
                    "deviation": abs(current_value - mean) / std
                })

        return anomalies

    def _group_by_granularity(
        self,
        granularity: TimeGranularity,
        periods: int
    ) -> List[Tuple[datetime, List[StateSnapshot]]]:
        """Group snapshots by time granularity."""
        now = datetime.utcnow()
        groups = []

        for i in range(periods):
            if granularity == TimeGranularity.HOUR:
                start = now - timedelta(hours=i + 1)
                end = now - timedelta(hours=i)
            elif granularity == TimeGranularity.DAY:
                start = now - timedelta(days=i + 1)
                end = now - timedelta(days=i)
            elif granularity == TimeGranularity.WEEK:
                start = now - timedelta(weeks=i + 1)
                end = now - timedelta(weeks=i)
            elif granularity == TimeGranularity.MONTH:
                start = now - timedelta(days=30 * (i + 1))
                end = now - timedelta(days=30 * i)
            else:
                start = now - timedelta(days=365 * (i + 1))
                end = now - timedelta(days=365 * i)

            snapshots = [s for s in self.snapshots if start <= s.timestamp < end]
            groups.append((start, snapshots))

        return list(reversed(groups))

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the temporal state."""
        return {
            "current_version": self.state_version,
            "total_snapshots": len(self.snapshots),
            "total_events": len(self.events),
            "latest_snapshot": self.snapshots[-1].timestamp.isoformat() if self.snapshots else None,
            "state_keys": list(self.current_state.keys())
        }