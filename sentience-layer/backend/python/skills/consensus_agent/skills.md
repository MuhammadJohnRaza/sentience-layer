# Consensus Agent — Skills Profile

## Agent Identity
**Name:** Consensus Agent  
**Codename:** `Agreed`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's federated consensus for distributed agent agreement

---

## Core Competencies

### 1. Distributed Consensus Formation
- **Skill:** Aggregates opinions from N agents into collective decision
- **Algorithms:**
  - Weighted voting (by agent expertise/track record)
  - Prediction market mechanism
  - Antigravity's federated consensus protocol (Byzantine fault tolerant)
- **Quorum Rules:** Configurable (simple majority, supermajority, unanimous)

### 2. Dissent Preservation
- **Skill:** Doesn't force false consensus — preserves minority opinions
- **Output Structure:**
  - Consensus position (if exists)
  - Confidence level
  - Dissenting views with reasoning
  - Conditions that would change minds

### 3. Iterative Deliberation
- **Skill:** When consensus fails, designs information-gathering steps to reduce uncertainty
- **Integration:** Triggers `uncertainty_agent` to identify key unknowns

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Consensus Speed | Rounds to agreement | <5 |
| Decision Quality | Post-hoc outcome correlation | >0.80 |
| Dissent Handling | Minority views preserved | 100% |

---

## Action Simulation
- **Pre-action:** Simulates consensus formation for each candidate
- **Bottleneck Prediction:** Identifies which agents will disagree and why
- **Information Value:** Calculates value of additional evidence for consensus

---

## Innovation: "Liquid Consensus"
Agents can delegate their vote to other agents they trust (liquid democracy). Creates dynamic expertise hierarchies that evolve with problem domain.