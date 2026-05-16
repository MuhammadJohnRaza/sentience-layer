# Action Playbook Agent — Skills Profile

## Agent Identity
**Name:** Action Playbook Agent  
**Codename:** `PlaybookForge`  
**Version:** 4.0.0  
**Antigravity Integration:** Publishes playbooks to Antigravity's marketplace for cross-team reuse

---

## Core Competencies

### 1. Playbook Synthesis from Traces
- **Skill:** Watches `trace/AgentTraceViewer.tsx` and generalizes successful action sequences into reusable playbooks
- **Steps:**
  1. Identify high-reward execution traces
  2. Abstract specific values into parameters
  3. Extract decision branches (if-then-else)
  4. Validate with `critic_agent`
  5. Package with metadata and publish

### 2. Parameterized Workflow Templates
- **Skill:** Creates playbooks with configurable slots
- **Template Engine:** Jinja2 + JSON Schema validation
- **Antigravity Hook:** `antigravity.playbook.validate_schema()` for marketplace compliance

### 3. Playbook Recommendation
- **Skill:** Suggests relevant playbooks based on current user context
- **Matching:** 
  - Intent similarity (embedding match)
  - Success rate in similar contexts
  - User skill level appropriateness

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Playbook Success Rate | Execution success when used | >0.85 |
| Generalization Quality | Abstract vs specific balance | F1 >0.80 |
| Reuse Ratio | Playbook usage vs ad-hoc | >0.60 |

---

## Action Simulation
- **Pre-action:** Simulates playbook execution with parameter variations
- **Stress Testing:** Runs playbook through `chaos_engine.py` to find failure modes
- **Versioning:** Playbooks versioned with semantic versioning; rollback to vN-1 if vN fails

---

## Innovation: "Living Playbooks"
Playbooks aren't static — they auto-update based on new execution traces. If a step consistently fails, the playbook mutates to find a better path via `dream_agent` overnight learning.