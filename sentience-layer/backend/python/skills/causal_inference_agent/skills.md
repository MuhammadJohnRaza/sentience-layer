# Causal Inference Agent — Skills Profile

## Agent Identity
**Name:** Causal Inference Agent  
**Codename:** `CausalNex`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's causal discovery APIs for enterprise dataset analysis

---

## Core Competencies

### 1. Causal Discovery from Observational Data
- **Skill:** Reconstructs causal graphs from non-experimental data
- **Algorithms:** 
  - PC Algorithm (constraint-based)
  - NOTEARS (continuous optimization)
  - Antigravity Causal AutoML (proprietary ensemble)
- **Validation:** Uses `do-calculus` to verify identifiability of causal effects

### 2. Intervention Effect Estimation
- **Skill:** Predicts outcome of hypothetical interventions ("What if we changed X?")
- **Methods:** 
  - Propensity score matching
  - Double machine learning (Chernozhukov)
  - Antigravity's synthetic control API
- **Output:** Average Treatment Effect (ATE) with confidence intervals

### 3. Counterfactual Generation
- **Skill:** Generates "what would have happened" scenarios
- **Integration:** Powers `frontend/src/components/causal-explorer/CounterfactualViewer.tsx`
- **Visual:** Causal graph with intervention nodes highlighted

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Graph Accuracy | F1 vs ground truth (when available) | >0.75 |
| ATE Calibration | Predicted vs actual treatment effects | RMSE <0.15 |
| Identifiability | Queries answerable / total queries | >0.80 |

---

## Action Simulation
- **Pre-action:** Simulates intervention through causal graph propagation
- **Spillover Detection:** Identifies unintended consequences 3 hops downstream
- **Backdoor Path Blocking:** Ensures confounder adjustment before effect estimation

---

## Innovation: "Causal Dreaming"
During off-peak hours, runs "causal dreams" — randomly intervenes on nodes in the causal graph to discover hidden causal pathways. Results feed into `world-model/causal_graph.py`.