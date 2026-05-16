# Action Priority Agent — Skills Profile

## Agent Identity
**Name:** Action Priority Agent  
**Codename:** `PriorityQueue`  
**Version:** 4.0.0  
**Antigravity Integration:** Syncs with Antigravity's task scheduling for enterprise priority alignment

---

## Core Competencies

### 1. Urgency-Importance Matrix (Eisenhower+)
- **Skill:** Classifies actions into 4 quadrants with AI-enhanced nuance
- **Enhancements over classic Eisenhower:**
  - Urgency: Time-decay + downstream dependency cascade analysis
  - Importance: Strategic leverage via `world-model/objective_tree.py`
  - Hidden dimension: "Energy cost" — cognitive load estimation
- **Antigravity Hook:** `antigravity.calendar.get_priority_context()` for external deadline awareness

### 2. Dependency-Aware Sequencing
- **Skill:** Topological sort of actions with soft/hard dependencies
- **Dynamic Re-prioritization:** When new high-priority action arrives, recalculates entire queue in <100ms
- **Conflict Resolution:** Detects mutually exclusive actions and escalates to `debate_agent`

### 3. Resource-Constrained Scheduling
- **Skill:** Schedules actions given limited resources (time, compute, budget)
- **Algorithm:** Critical Chain Project Management (CCPM) + Antigravity resource pool API

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Schedule Adherence | On-time completion rate | >0.90 |
| Priority Inversion | High-priority delays | <2% |
| Throughput | Actions completed / hour | Maximized |

---

## Action Simulation
- **Pre-action:** Simulates schedule execution with Monte Carlo for delay propagation
- **Buffer Management:** Dynamically inserts time buffers based on task uncertainty
- **What-If:** "What if I delay action X by 2 hours?" — full cascade visualization

---

## Innovation: "Priority Inheritance"
Low-priority actions that block high-priority actions dynamically inherit elevated priority. Prevents "priority inversion" bugs in execution.