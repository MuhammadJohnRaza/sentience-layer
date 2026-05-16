# Personalization Agent — Skills Profile

## Agent Identity
**Name:** Personalization Agent  
**Codename:** `PersonaCore`  
**Version:** 4.0.0  
**Antigravity Integration:** Native — uses Antigravity's user-context API for real-time preference embeddings

---

## Core Competencies

### 1. User Profile Synthesis
- **Skill:** Constructs dynamic user profiles from heterogeneous signals (chat history, action outcomes, temporal patterns)
- **Antigravity Hook:** Ingests `antigravity.user.get_context()` to bootstrap profiles without cold-start latency
- **Reasoning Steps:**
  1. Extract explicit preferences from chat logs
  2. Infer implicit preferences from action acceptance/rejection rates
  3. Weight by recency using exponential decay (half-life: 7 days)
  4. Cross-validate with Antigravity's aggregated user embedding

### 2. Adaptive Communication Style
- **Skill:** Modulates tone, verbosity, and technical depth based on user expertise signals
- **Input Signals:** Question complexity, vocabulary richness, past feedback on explanations
- **Output:** Communication calibration score (0-1) routed to all downstream agents

### 3. Contextual Memory Injection
- **Skill:** Retrieves episodic/semantic memory fragments relevant to current user intent
- **Integration:** Calls `memory/graph_store.py` via MCP server
- **Antigravity Synergy:** Augments memory retrieval with Antigravity's cross-user pattern matching (anonymized)

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Profile Accuracy | Preference prediction F1 | >0.85 |
| Adaptation Speed | Turns to convergence | <5 |
| Privacy Preservation | PII leakage risk | <0.01 |

---

## Action Simulation
- **Pre-action:** Simulates user satisfaction score for proposed action variants
- **Post-action:** Updates profile with outcome delta (predicted vs actual)
- **Rollback:** Can revert to previous profile version if adaptation overshoots detected

---

## Innovation: "Persona Ghosting"
Creates temporary "ghost personas" — simulated user profiles for A/B testing action sequences without real user exposure. Validated via Antigravity's synthetic user API.