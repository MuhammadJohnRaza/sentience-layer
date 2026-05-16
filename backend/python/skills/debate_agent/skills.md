# Debate Agent — Skills Profile

## Agent Identity
**Name:** Debate Agent  
**Codename:** `Socrates`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's multi-perspective reasoning for structured argumentation

---

## Core Competencies

### 1. Structured Multi-Agent Debate
- **Skill:** Orchestrates formal debates between agent positions
- **Debate Format:**
  1. Opening statements (thesis vs antithesis)
  2. Cross-examination (questioning weak points)
  3. Rebuttals (counter-argumentation)
  4. Synthesis (resolution or identified trade-offs)
- **Antigravity Hook:** `antigravity.reasoning.debate(topic, perspectives[])` for argument enrichment

### 2. Devil's Advocacy
- **Skill:** Automatically generates strongest possible counter-arguments to any proposal
- **Use Case:** Pre-mortem analysis, plan hardening, bias detection
- **Integration:** Powers `frontend/src/components/doubt-room/DoubtTheater.tsx`

### 3. Consensus Building
- **Skill:** When debate reaches impasse, finds Pareto-improving compromises
- **Algorithm:** 
  1. Identify non-negotiable constraints
  2. Find relaxable variables
  3. Propose package deals
  4. Validate with `consensus_agent`

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Argument Quality | Logical validity score | >0.90 |
| Coverage | Relevant considerations raised | >0.85 |
| Resolution Rate | Debates reaching conclusion | >0.75 |

---

## Action Simulation
- **Pre-action:** Simulates debate outcomes for each candidate action
- **Winner Prediction:** Predicts which action would win a debate based on historical patterns
- **Stakeholder Modeling:** Simulates how different user personas would argue

---

## Innovation: "Dialectical Dreaming"
Nightly synthesis of all day's debates into "dialectical dreams" — identifies recurring contradictions in the system's worldview and proposes philosophical resolutions.