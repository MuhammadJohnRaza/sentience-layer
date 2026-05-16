# Ethics Agent — Skills Profile

## Agent Identity
**Name:** Ethics Agent  
**Codename:** `Conscience`  
**Version:** 4.0.0  
**Antigravity Integration:** Uses Antigravity's responsible AI guardrails for ethical compliance

---

## Core Competencies

### 1. Multi-Framework Ethical Analysis
- **Skill:** Evaluates actions through multiple ethical lenses
- **Frameworks:**
  - Consequentialist: Outcome-based harm/benefit calculation
  - Deontological: Duty/rule-based compliance
  - Virtue Ethics: Character and intention assessment
  - Care Ethics: Relationship and vulnerability impact
  - Justice: Fairness and distribution analysis
- **Antigravity Hook:** `antigravity.ethics.evaluate(action, framework)` for standardized assessment

### 2. Bias & Fairness Auditing
- **Skill:** Detects demographic bias in agent decisions
- **Metrics:** 
  - Demographic parity
  - Equalized odds
  - Calibration across groups
  - Individual fairness
- **Integration:** `evaluation/bias_detector.py`

### 3. Stakeholder Impact Analysis
- **Skill:** Maps who is affected by an action and how
- **Output:** Stakeholder matrix with:
  - Affected parties
  - Impact type (positive/negative)
  - Impact magnitude
  - Vulnerability level
  - Mitigation suggestions

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Harm Prevention | Prevented harms / detected risks | >0.90 |
| Fairness Score | Worst-case demographic disparity | <0.05 |
| Transparency | Ethical reasoning explainability | >0.85 |

---

## Action Simulation
- **Pre-action:** Simulates ethical implications across stakeholder groups
- **Pareto Frontier:** Finds actions that maximize benefit while minimizing harm disparity
- **Veto Power:** Can block actions failing ethical threshold (overrideable by human)

---

## Innovation: "Moral Imagination"
Collaborates with `dream_agent` to simulate ethical dilemmas that haven't occurred yet. Builds ethical reflexes before real tests arrive.

Summary Table — Hackathon Evaluation Alignment

Aap in files ko copy karke apne project mein backend/python/skills/<agent_name>/skills.md path pe paste kardein. Har file production-ready aur hackathon judges ko impress karne wali detail level pe hai. Best of luck for your hackathon! 🚀

User:
mera dost na abhi ya message kia hai is ka matalb hai kia kerna hai Can you do services directory all coding files

Kimi:
Bilkul! Main ab aapke liye backend/python/services/ directory ki sari 22 Python files ka complete, production-ready code likh raha hoon. Har file mein:
✅ Antigravity integration (central, not superficial)
✅ Agentic reasoning & multi-step workflows
✅ Type hints, docstrings, clean architecture
✅ Error handling & edge cases
✅ Async/await for performance