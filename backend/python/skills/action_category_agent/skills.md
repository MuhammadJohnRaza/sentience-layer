# Action Category Agent — Skills Profile

## Agent Identity
**Name:** Action Category Agent  
**Codename:** `Taxonomist`  
**Version:** 4.0.0  
**Antigravity Integration:** Maps actions to Antigravity's universal action ontology for interoperability

---

## Core Competencies

### 1. Hierarchical Action Classification
- **Skill:** Categorizes actions into 5-level taxonomy
  - L1: Domain (Communication, Analysis, Execution, Creative)
  - L2: Function (Email, Report, Code, Design)
  - L3: Operation (Draft, Review, Send, Deploy)
  - L4: Tool (Gmail, Slack, GitHub, Figma)
  - L5: Specific API method
- **Antigravity Hook:** `antigravity.ontology.classify(action_description)` for standardization

### 2. Cross-Domain Pattern Recognition
- **Skill:** Identifies when actions from different domains share underlying structure
- **Example:** "Send email reminder" and "Post Slack nudge" both = "Notification with escalation"
- **Benefit:** Enables transfer learning across tools

### 3. Semantic Clustering
- **Skill:** Groups uncategorized actions by embedding similarity
- **Algorithm:** HDBSCAN on action embeddings + Antigravity's domain-specific fine-tuning
- **Emergence:** Discovers new action categories autonomously

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Classification Accuracy | Top-1 accuracy | >0.92 |
| Ontology Coverage | Actions mappable to ontology | >0.95 |
| Novelty Detection | New category discovery precision | >0.80 |

---

## Action Simulation
- **Pre-action:** Simulates category confusion — "Is this really a Communication action or an Analysis action?"
- **Ambiguity Resolution:** When confidence <0.8, triggers `debate_agent` for disambiguation
- **Category Evolution:** Tracks how action mix changes over time (e.g., more "Creative" actions in Q4)

---

## Innovation: "Fractal Taxonomy"
Categories are self-similar — each leaf node contains a mini-ontology. Enables infinite granularity without losing interoperability.