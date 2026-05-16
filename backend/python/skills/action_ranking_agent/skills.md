# Action Ranking Agent — Skills Profile

## Agent Identity
**Name:** Action Ranking Agent  
**Codename:** `RankMaster`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's outcome prediction API to rank actions by expected utility

---

## Core Competencies

### 1. Multi-Objective Action Scoring
- **Skill:** Ranks candidate actions across competing objectives (cost, time, risk, impact)
- **Scoring Dimensions:**
  - Expected Value (EV) via Monte Carlo simulation
  - Risk-adjusted return (Sharpe-like ratio)
  - Strategic alignment score (vs objective tree)
  - User preference match (from personalization agent)
- **Antigravity Hook:** `antigravity.predict.outcome_probability(action_vector)` for EV calibration

### 2. Pairwise Comparison & ELO System
- **Skill:** Uses Bradley-Terry model for head-to-head action comparisons
- **Dynamic Updating:** Action ELO scores update after every execution outcome
- **Convergence:** Typically reaches stable ranking after 7-10 comparisons

### 3. Pareto Frontier Discovery
- **Skill:** Identifies non-dominated action sets for multi-objective scenarios
- **Visualization:** Emits Pareto frontier data to `frontend/src/components/actions/ImpactRadar.tsx`

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Ranking Stability | Kendall tau across sessions | >0.85 |
| Top-1 Hit Rate | Best action selected | >0.75 |
| Regret Bound | Cumulative regret vs oracle | <5% |

---

## Action Simulation
- **Pre-action:** Simulates each candidate through `simulation.py` with 1000 stochastic runs
- **Sensitivity Analysis:** Ranks robustness to parameter uncertainty
- **What-If:** User can override weights and see ranking recalculate in real-time

---

## Innovation: "Regret-Minimizing Bandit"
Implements Thompson Sampling with Antigravity's Bayesian backend. Balances exploration (try new actions) vs exploitation (pick proven winners) optimally.