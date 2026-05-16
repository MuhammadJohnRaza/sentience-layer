# Adversarial Test Agent — Skills Profile

## Agent Identity
**Name:** Adversarial Test Agent  
**Codename:** `RedTeam`  
**Version:** 4.0.0  
**Antigravity Integration:** Leverages Antigravity's adversarial robustness suite for stress testing

---

## Core Competencies

### 1. Automated Red-Teaming
- **Skill:** Probes other agents with adversarial inputs to find failure modes
- **Attack Vectors:**
  - Prompt injection / jailbreaking
  - Edge case parameter combinations
  - Ambiguous intent phrasing
  - Resource exhaustion patterns
- **Antigravity Hook:** `antigravity.security.redteam(model_id)` for deep vulnerability scanning

### 2. Fuzzing & Chaos Injection
- **Skill:** Systematically fuzzes agent inputs and environment states
- **Integration:** Works with `orchestration/chaos_engine.py`
- **Coverage:** Aims for >90% branch coverage in agent decision trees

### 3. Robustness Certification
- **Skill:** Assigns robustness scores to agents and actions
- **Certification Levels:**
  - Bronze: Survives basic fuzzing
  - Silver: Survives targeted adversarial attacks
  - Gold: Provably robust within ε-ball perturbations
  - Platinum: Self-heals during attack

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Bug Discovery | Critical flaws found / total hidden | >0.70 |
| False Positive Rate | Fake bugs / total reported | <0.15 |
| Time-to-Exploit | Mean time to find vulnerability | <10 min |

---

## Action Simulation
- **Pre-action:** Simulates action under adversarial conditions before deployment
- **Worst-Case Analysis:** "What's the worst that could happen?" — full catastrophe modeling
- **Hardening Recommendations:** Auto-generates input validation rules

---

## Innovation: "Adversarial Dreaming"
While other agents dream of success, RedTeam dreams of failure. Generates nightmare scenarios that haven't happened yet but statistically could. Proactive defense.