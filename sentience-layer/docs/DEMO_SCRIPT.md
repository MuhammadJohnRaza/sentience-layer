# 🎬 Sentience Layer - Demo Script

## Demo Overview

**Duration**: 5 minutes  
**Goal**: Showcase Google Antigravity integration, agentic reasoning, and action simulation  
**Audience**: Hackathon judges

## Pre-Demo Setup

### 1. Environment Check
```bash
# Ensure all services are running
docker-compose ps

# Expected output:
# sentience-postgres     Up
# sentience-redis        Up
# sentience-backend-python   Up
# sentience-frontend     Up
```

### 2. Browser Setup
- Open http://localhost:3000
- Open http://localhost:8000/docs (API docs in background tab)
- Clear browser cache
- Zoom to 100%

### 3. Sample Data
```bash
# Load sample sales data
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d @sample_data/sales_q4_2024.json
```

## Demo Script (5 Minutes)

### Act 1: The Problem (30 seconds)

**Narration**:
> "Imagine you're a CEO. Your Q4 revenue just dropped 15%. Traditional BI tools show you charts and correlations, but they can't tell you WHY it happened or WHAT to do about it."

**Action**:
- Show traditional dashboard (static charts)
- Point to revenue decline graph

---

### Act 2: Enter Sentience Layer (30 seconds)

**Narration**:
> "This is Sentience Layer - a Cognitive Operating System powered by Google Antigravity. Instead of just showing data, it THINKS about your business using 18 specialized AI agents."

**Action**:
- Navigate to Sentience Layer dashboard
- Show agent status panel (18 agents online)
- Highlight "Powered by Google Antigravity" badge

---

### Act 3: Ask the Question (1 minute)

**Narration**:
> "Let's ask the system: Why did Q4 revenue drop?"

**Action**:
1. Type in query box: "Why did revenue drop in Q4 2024?"
2. Click "Analyze"
3. **Show real-time agent reasoning** (key differentiator!)

**Expected Output** (streaming):
```
[Causal Inference Agent] Analyzing 47 variables...
[Causal Inference Agent] Found correlation: marketing_spend → revenue (r=0.85)
[Causal Inference Agent] Running Granger causality test...
[Causal Inference Agent] ✓ Causal relationship confirmed (p<0.01)

[Debate Agent - Pro] Strong statistical evidence supports causation
[Debate Agent - Con] Could be confounded by seasonality
[Debate Agent - Pro] Counterfactual analysis rules out seasonality

[Uncertainty Agent] Testing counterfactual scenarios...
[Uncertainty Agent] ✓ Revenue stable when marketing constant

[Consensus Agent] Synthesizing findings...
[Consensus Agent] ✓ High confidence (92%) - Marketing caused decline
```

**Narration during streaming**:
> "Notice how multiple agents are working together - debating, validating, reaching consensus. This is agentic reasoning powered by Google Antigravity."

---

### Act 4: The Insight (45 seconds)

**Action**:
- Show final insight card

**Expected Output**:
```json
{
  "finding": "Marketing budget cut on July 1st CAUSED 15% revenue decline",
  "confidence": 92%,
  "causal_chain": [
    "Marketing spend reduced 30%",
    "Lead volume dropped 35% in August", 
    "Pipeline decreased 28% in September",
    "Revenue declined 15% in Q4"
  ],
  "mechanism": "Reduced ad spend → Fewer leads → Smaller pipeline → Revenue drop",
  "evidence": {
    "granger_test": "p < 0.01",
    "counterfactual": "Revenue stable when marketing constant",
    "confounders": "None detected"
  }
}
```

**Narration**:
> "The system didn't just find a correlation - it proved CAUSATION. It shows the mechanism, the evidence, and quantifies confidence. This is the power of causal AI."

---

### Act 5: The Recommendation (45 seconds)

**Action**:
- Scroll to recommendation section

**Expected Output**:
```
Recommended Action: Restore marketing budget to Q3 levels ($75K/month)

Expected Outcome: +12% revenue within 90 days
Confidence: 88%
ROI: 2.4x

Why this works:
✓ Proven causal relationship
✓ Historical ROI of 2.4x
✓ Low execution risk
```

**Narration**:
> "But we don't stop at insights. The system recommends a specific action with expected outcomes."

---

### Act 6: Simulate Before You Act (1 minute)

**Narration**:
> "Before investing $75K, let's test it in simulation."

**Action**:
1. Click "Simulate This Action"
2. Show simulation running (progress bar)
3. Display results

**Expected Output**:
```
Simulation Complete: 1000 scenarios analyzed

Outcome Distribution:
├─ Best case (10%): +18% revenue, ROI 3.6x
├─ Expected (50%): +12% revenue, ROI 2.4x
└─ Worst case (10%): +6% revenue, ROI 1.6x

State Changes:
Day 1-7:   Marketing spend increases → Ad impressions +50%
Day 7-30:  More impressions → Leads increase +55%
Day 30-60: More leads → Pipeline grows +45%
Day 60-90: Larger pipeline → Revenue increases +12%

Risk Analysis:
✓ 92% probability of positive ROI
✓ Only 8% chance of loss
✓ Low risk, high confidence

Decision: PROCEED ✓
```

**Narration**:
> "We just ran 1000 Monte Carlo simulations in 30 seconds. We see the full outcome distribution, state changes over time, and risk analysis. Now you can invest with confidence."

---

### Act 7: The Differentiators (30 seconds)

**Action**:
- Show side-by-side comparison slide

**Narration**:
> "What makes Sentience Layer unique?"

**Show on screen**:
```
Traditional BI          vs.    Sentience Layer
─────────────────────────────────────────────────
Shows correlations      →      Proves causation
Single AI model         →      18 specialized agents
Static dashboards       →      Real-time reasoning
"What happened?"        →      "Why? What if? What next?"
Correlation (r=0.85)    →      Causal (p<0.01, 92% confidence)
```

---

### Act 8: Google Antigravity Integration (30 seconds)

**Action**:
- Open API docs tab
- Show Antigravity integration code

**Code on screen**:
```python
# Every agent powered by Google Antigravity
async def analyze(self, query):
    # Antigravity's causal reasoning
    causal_result = await antigravity.infer_causality(
        data=self.data,
        cause=cause,
        effect=effect
    )
    
    # Antigravity's multi-agent orchestration
    debate = await antigravity.orchestrate_agents([
        {"agent": "economic", "stance": "pro"},
        {"agent": "ethics", "stance": "con"}
    ])
    
    # Antigravity's consensus building
    consensus = await antigravity.synthesize(debate)
    
    return consensus
```

**Narration**:
> "Google Antigravity isn't just an API we call - it's the reasoning engine powering every agent. Causal inference, multi-agent orchestration, consensus building - all Antigravity."

---

### Closing (30 seconds)

**Narration**:
> "Sentience Layer transforms data into decisions through:
> 
> ✓ Causal reasoning - not just correlation
> ✓ Multi-agent intelligence - 18 specialists working together  
> ✓ Action simulation - test before you invest
> ✓ Google Antigravity - powering every decision
> 
> This isn't just a BI tool. It's a Cognitive Operating System for business intelligence.
> 
> Thank you!"

**Action**:
- Show final slide with:
  - GitHub repo QR code
  - Live demo URL
  - Contact info

---

## Backup Demos (If Time Permits)

### Bonus Demo 1: Multi-Agent Debate (1 minute)

**Query**: "Should we expand to Asian markets?"

**Show**:
- Economic Agent: "4.5B potential customers, 8% growth"
- Ethics Agent: "Regulatory complexity, 12 frameworks"
- Uncertainty Agent: "Currency risk 15% volatility"
- Consensus: "Expand with phased approach - start Singapore"

### Bonus Demo 2: Dream Mode (1 minute)

**Query**: "Creative ways to increase revenue by 20%"

**Show**:
- Traditional: "Increase marketing, hire sales reps"
- Dream Mode: "Reverse pricing model, customer-as-investor program"
- Novelty scores and feasibility analysis

---

## Troubleshooting

### If Demo Breaks

**Scenario 1: Services not responding**
```bash
# Quick restart
docker-compose restart

# Or show pre-recorded video
open demo_video.mp4
```

**Scenario 2: Slow response**
```bash
# Use cached results
curl http://localhost:8000/api/insights/cached/demo-001
```

**Scenario 3: Frontend crash**
- Switch to API docs tab
- Show curl commands and JSON responses
- Emphasize backend intelligence

---

## Key Talking Points

### Google Antigravity (25%)
- "Every agent uses Antigravity's reasoning API"
- "Causal inference powered by Antigravity's temporal analysis"
- "Multi-agent orchestration via Antigravity framework"

### Agentic Reasoning (20%)
- "18 specialized agents, not one generic model"
- "Agents debate and reach consensus"
- "Multi-step reasoning chains (5-10 steps per agent)"

### Insight Quality (20%)
- "Causal explanations with statistical evidence"
- "Confidence intervals, not point estimates"
- "Structured decision frameworks"

### Action Simulation (15%)
- "1000 Monte Carlo scenarios in 30 seconds"
- "Realistic state changes tracked"
- "Risk-aware recommendations"

### Technical Implementation (10%)
- "Clean microservices architecture"
- "Async/await for performance"
- "Real-time WebSocket streaming"

### Innovation (10%)
- "Transparent AI - see agents think"
- "Causal, not correlational"
- "Test before you invest"

---

## Post-Demo Q&A Prep

**Q: How is this different from existing BI tools?**
A: Traditional BI shows correlations. We prove causation. We don't just say "revenue and marketing are correlated" - we prove marketing CAUSES revenue with statistical evidence.

**Q: Why 18 agents instead of one model?**
A: Specialization. Just like a company has different departments, we have specialized agents. The Causal Agent is expert at causality, the Debate Agent at exploring perspectives. They collaborate like a human team.

**Q: How accurate are the simulations?**
A: We use historical data to calibrate models, then run 1000+ Monte Carlo scenarios. We provide confidence intervals, not false precision. If we say 88% confidence, we mean it.

**Q: Can this work for my industry?**
A: Yes! The core reasoning is domain-agnostic. We're building industry-specific agents for finance, healthcare, retail, and manufacturing.

**Q: What's the Google Antigravity integration?**
A: Antigravity powers our causal inference, multi-agent orchestration, and consensus building. It's not a wrapper - it's deeply integrated into every agent's reasoning process.

---

**Demo complete! 🎉 Ready to win the hackathon!**
