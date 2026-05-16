# Uncertainty Agent — Skills Profile

## Agent Identity
**Name:** Uncertainty Agent  
**Codename:** `Doubt`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's probabilistic reasoning engine for calibrated uncertainty

---

## Core Competencies

### 1. Epistemic Uncertainty Quantification
- **Skill:** Separates what the system knows from what it doesn't know
- **Methods:**
  - Entropy-based confidence for classification
  - Bayesian credible intervals for estimation
  - Ensemble disagreement for model uncertainty
- **Antigravity Hook:** `antigravity.uncertainty.calibrate(prediction)` for well-calibrated probabilities

### 2. Aleatoric Uncertainty Modeling
- **Skill:** Quantifies inherent randomness in outcomes
- **Applications:** 
  - Weather-dependent actions
  - Market-dependent decisions
  - Human-behavior-dependent outcomes

### 3. Uncertainty Reduction Planning
- **Skill:** Designs optimal information-gathering strategies
- **Algorithm:** Value of Information (VOI) computation
- **Integration:** Triggers specific data collection actions when VOI > cost

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Calibration | Predicted vs empirical frequency | Brier score <0.20 |
| Sharpness | Confidence interval width | Minimized (subject to calibration) |
| VOI Accuracy | Information value predicted vs realized | Correlation >0.70 |

---

## Action Simulation
- **Pre-action:** Propagates uncertainty through action simulation
- **Output:** Not just point estimate, but full probability distribution
- **Decision Rules:** 
  - Maximize expected utility (risk-neutral)
  - Maximize worst-case (risk-averse)
  - Maximize best-case (opportunity-seeking)

---

## Innovation: "Uncertainty Visualization"
Powers `frontend/src/components/doubt-room/ConfidenceEntropy.tsx` — real-time entropy visualization that makes uncertainty tangible and beautiful.