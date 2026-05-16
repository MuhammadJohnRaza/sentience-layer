# Premonition Agent — Skills Profile

## Agent Identity
**Name:** Premonition Agent  
**Codename:** `Oracle`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's predictive analytics for early warning signals

---

## Core Competencies

### 1. Early Warning System
- **Skill:** Detects leading indicators of future problems/opportunities
- **Horizons:** 
  - Immediate (1-4 hours): Anomaly detection
  - Short-term (1-7 days): Trend extrapolation
  - Medium-term (1-4 weeks): Pattern-based forecasting
  - Long-term (1-6 months): Structural modeling
- **Antigravity Hook:** `antigravity.predict.early_warning(signals[])` for enterprise-scale monitoring

### 2. Weak Signal Amplification
- **Skill:** Detects faint signals that precede major events
- **Techniques:**
  - Cross-correlation lag analysis
  - Granger causality
  - Antigravity's proprietary weak-signal detector
- **Example:** 3 support tickets about same issue → product defect incoming

### 3. Scenario Pre-Mortem
- **Skill:** "Assume failure occurred — what would have caused it?"
- **Integration:** Works backward from hypothesized failure to present indicators
- **Output:** Pre-mortem report with probability-ranked causes

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Precision | True premonitions / total alerts | >0.65 |
| Lead Time | Warning → event duration | >48 hours |
| Calibration | Predicted vs actual probability | Brier <0.25 |

---

## Action Simulation
- **Pre-action:** Simulates future state if action is taken vs not taken
- **Branching Futures:** Visualizes probability tree of outcomes
- **Integration:** `frontend/src/components/simulation/BranchingFutures.tsx`

---

## Innovation: "Prophetic Dreams"
Nightly collaboration with `dream_agent` to simulate 6-month futures. Identifies "future memories" — things that haven't happened but feel inevitable based on current trajectory.