# Dream Agent — Skills Profile

## Agent Identity
**Name:** Dream Agent  
**Codename:** `Oneiroi`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's generative sandbox for safe dream simulation

---

## Core Competencies

### 1. Generative Dream Synthesis
- **Skill:** During low-activity periods, generates synthetic scenarios for learning
- **Dream Types:**
  - Consolidation dreams: Merge fragmented memories
  - Counterfactual dreams: Explore "what if" scenarios
  - Creative dreams: Combine unrelated concepts for novelty
  - Adversarial dreams: Nightmare scenarios for robustness
- **Antigravity Hook:** `antigravity.sandbox.dream(seed)` for isolated generative environment

### 2. Insight Emergence Detection
- **Skill:** Identifies novel patterns that emerge only during dream states
- **Mechanism:** 
  1. Generate 1000+ synthetic scenarios
  2. Run full agent stack on each
  3. Cluster outcomes
  4. Flag outliers as potential insights
- **Integration:** Powers `frontend/src/components/dreamscape/InsightEmergence.tsx`

### 3. Memory Consolidation
- **Skill:** Converts episodic memories into semantic schemas during sleep
- **Algorithm:** Memory replay with gradient descent on belief graph
- **Result:** More compact, generalizable knowledge

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Insight Rate | Novel useful insights / dream cycles | >0.10 |
| False Insight Rate | Useless novelties / total novelties | <0.30 |
| Consolidation Gain | Memory compression without loss | 5:1 |

---

## Action Simulation
- **Dream Action:** Simulates actions in impossible scenarios (e.g., "what if gravity reversed?")
- **Transfer Test:** Validates if insights transfer to real scenarios
- **Creativity Score:** Measures semantic distance between dream and reality

---

## Innovation: "Lucid Dreaming"
Agent can become "lucid" during dreams — aware it's dreaming and directing the simulation toward specific learning goals. Active learning during sleep.