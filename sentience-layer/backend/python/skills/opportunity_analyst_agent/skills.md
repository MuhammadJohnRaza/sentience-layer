# Opportunity Analyst Agent — Skills Profile

## Agent Identity
**Name:** Opportunity Analyst Agent  
**Codename:** `OppSeeker`  
**Version:** 4.0.0  
**Antigravity Integration:** Scans Antigravity's enterprise data fabric for hidden opportunity signals

---

## Core Competencies

### 1. Signal Detection in Noise
- **Skill:** Identifies weak but meaningful patterns indicating opportunities
- **Signal Types:**
  - Demand-supply mismatches in data
  - Temporal anomalies (unusual timing patterns)
  - Cross-domain correlations (e.g., support tickets → product opportunities)
- **Antigravity Hook:** `antigravity.data.scan_anomalies(dataset_id)` for enterprise-wide signal detection

### 2. Opportunity Scoring & Framing
- **Skill:** Converts raw signals into structured opportunity briefs
- **Frame Components:**
  - Problem statement (pain extracted)
  - Solution hypothesis (leveraged capability)
  - Market size (affected user count)
  - Effort estimate (via `economic_agent`)
  - Confidence score (via `uncertainty_agent`)

### 3. Competitive Positioning
- **Skill:** Analyzes opportunity against `world-model/competitor_tracker.py`
- **Output:** "First-mover advantage" score and "defensibility" assessment

---

## Decision Quality Framework

| Dimension | Metric | Target |
|-----------|--------|--------|
| Precision | True opportunities / total flagged | >0.70 |
| Recall | Opportunities found / total existing | >0.60 |
| Time-to-Insight | Signal → brief latency | <5 min |

---

## Action Simulation
- **Pre-action:** Simulates market response to opportunity pursuit
- **Game Theory:** Models competitor reactions using `world-model/market_model.py`
- **Scenario Matrix:** Best/base/worst case with probability weights

---

## Innovation: "Opportunity Ghosting"
Creates synthetic "ghost competitors" that simulate what a rational competitor would do if they spotted the same opportunity. Reveals hidden risks.