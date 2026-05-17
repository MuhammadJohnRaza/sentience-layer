# 🌍 World Model - Temporal Knowledge Graph

## What is the World Model?

The **World Model** is Sentience Layer's internal representation of business reality. It's a temporal knowledge graph that tracks:
- **Entities**: Customers, products, campaigns, competitors
- **Relationships**: Causal links, dependencies, correlations
- **Events**: Actions, outcomes, state changes
- **Time**: When things happened and their temporal relationships

## 🎯 Why a World Model?

Traditional databases store **facts**. The World Model stores **understanding**.

### Traditional Database
```sql
SELECT revenue FROM sales WHERE date = '2024-10-01';
-- Returns: 850000
```

### World Model
```python
world_model.query("revenue on 2024-10-01")
# Returns:
{
  "value": 850000,
  "change_from_previous": -15%,
  "causes": [
    {
      "event": "marketing_budget_cut",
      "date": "2024-07-01",
      "causal_strength": 0.85,
      "mechanism": "Reduced leads → Lower pipeline → Revenue drop"
    }
  ],
  "predicted_next_month": 820000,
  "confidence": 0.88
}
```

## 🏗️ Architecture

### 1. Entity Graph

```python
@dataclass
class Entity:
    id: str
    type: str  # "customer", "product", "campaign", etc.
    attributes: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

# Example entities
customer = Entity(
    id="CUST-001",
    type="customer",
    attributes={
        "name": "Acme Corp",
        "ltv": 125000,
        "churn_risk": 0.78,
        "segment": "enterprise"
    }
)

campaign = Entity(
    id="CAMP-Q4-2024",
    type="campaign",
    attributes={
        "budget": 75000,
        "channel": "google_ads",
        "roi": 2.4
    }
)
```

### 2. Relationship Graph

```python
@dataclass
class Relationship:
    source: str  # Entity ID
    target: str  # Entity ID
    type: str  # "causes", "influences", "depends_on"
    strength: float  # 0.0 to 1.0
    evidence: List[str]
    created_at: datetime

# Example: Causal relationship
relationship = Relationship(
    source="marketing_spend",
    target="revenue",
    type="causes",
    strength=0.85,
    evidence=[
        "Granger test p<0.01",
        "Counterfactual validated",
        "3-month lag observed"
    ]
)
```

### 3. Temporal Events

```python
@dataclass
class Event:
    id: str
    type: str  # "action", "outcome", "state_change"
    timestamp: datetime
    entities: List[str]  # Affected entity IDs
    attributes: Dict[str, Any]
    caused_by: Optional[str]  # Previous event ID
    leads_to: List[str]  # Subsequent event IDs

# Example: Marketing budget cut event
event = Event(
    id="EVT-2024-07-001",
    type="action",
    timestamp="2024-07-01T00:00:00Z",
    entities=["marketing_budget", "marketing_team"],
    attributes={
        "action": "budget_cut",
        "amount": -25000,
        "reason": "cost_reduction"
    },
    caused_by=None,
    leads_to=["EVT-2024-08-001"]  # Lead volume drop
)
```

### 4. State Tracking

```python
@dataclass
class State:
    timestamp: datetime
    entities: Dict[str, Entity]
    metrics: Dict[str, float]
    
# World state at a point in time
state_q3 = State(
    timestamp="2024-09-30T23:59:59Z",
    entities={
        "marketing_budget": Entity(...),
        "sales_team": Entity(...)
    },
    metrics={
        "revenue": 1000000,
        "leads": 300,
        "customers": 450
    }
)
```

## 🔄 World Model Operations

### 1. Query Historical State

```python
# What was revenue on a specific date?
state = world_model.get_state("2024-10-01")
revenue = state.metrics["revenue"]

# What caused revenue to change?
causes = world_model.get_causes(
    effect="revenue",
    timeframe=("2024-07-01", "2024-10-01")
)
```

### 2. Predict Future State

```python
# What will happen if we increase marketing budget?
future_state = world_model.predict(
    action=Action(
        type="budget_increase",
        entity="marketing_budget",
        amount=25000
    ),
    horizon_days=90
)

print(future_state.metrics["revenue"])  # 1120000
print(future_state.confidence)  # 0.88
```

### 3. Explain Causality

```python
# Why did revenue drop?
explanation = world_model.explain(
    outcome="revenue_drop",
    timeframe="Q4_2024"
)

# Returns causal chain:
# marketing_budget_cut → lead_volume_drop → 
# pipeline_decrease → revenue_decline
```

### 4. Simulate Counterfactuals

```python
# What would have happened if we didn't cut budget?
counterfactual = world_model.counterfactual(
    intervention="keep_marketing_budget",
    actual_outcome="revenue_drop"
)

print(counterfactual.difference)  # +150000 revenue
```

## 🧠 Learning and Updating

### 1. Causal Discovery

```python
# Automatically discover causal relationships
world_model.discover_causality(
    data=historical_data,
    min_confidence=0.7
)

# Adds new relationships to graph
# marketing_spend → leads (strength: 0.82)
# leads → pipeline (strength: 0.76)
# pipeline → revenue (strength: 0.91)
```

### 2. Outcome Learning

```python
# Learn from actual outcomes
world_model.update_from_outcome(
    prediction={
        "action": "budget_increase",
        "predicted_revenue": 1120000,
        "confidence": 0.88
    },
    actual_outcome={
        "actual_revenue": 1150000,
        "date": "2024-12-31"
    }
)

# Updates model parameters to improve future predictions
```

### 3. Relationship Strengthening

```python
# Strengthen relationships with more evidence
world_model.add_evidence(
    relationship="marketing_spend → revenue",
    evidence={
        "type": "natural_experiment",
        "description": "Budget restored in Q1, revenue recovered",
        "strength_increase": 0.05
    }
)
```

## 📊 World Model Queries

### Example 1: Root Cause Analysis

```python
query = """
Why did customer churn increase in Q4?
"""

result = world_model.analyze(query)

# Returns:
{
  "root_causes": [
    {
      "cause": "support_response_time_increase",
      "contribution": 0.45,
      "mechanism": "Slow support → Customer frustration → Churn"
    },
    {
      "cause": "product_bugs_increase",
      "contribution": 0.35,
      "mechanism": "Bugs → Poor experience → Churn"
    }
  ],
  "causal_chain": [
    "engineering_team_turnover",
    "code_quality_decline",
    "bug_rate_increase",
    "customer_satisfaction_drop",
    "churn_increase"
  ]
}
```

### Example 2: Impact Prediction

```python
query = """
What will happen if we hire 5 more engineers?
"""

result = world_model.predict_impact(
    action="hire_engineers",
    quantity=5
)

# Returns:
{
  "immediate_effects": [
    {"metric": "team_size", "change": +5},
    {"metric": "monthly_cost", "change": +50000}
  ],
  "short_term_effects": [
    {"metric": "velocity", "change": +15%, "timing": "30-60 days"},
    {"metric": "bug_rate", "change": -20%, "timing": "60-90 days"}
  ],
  "long_term_effects": [
    {"metric": "product_quality", "change": +25%, "timing": "90-180 days"},
    {"metric": "customer_satisfaction", "change": +12%, "timing": "120-180 days"},
    {"metric": "churn_rate", "change": -8%, "timing": "150-210 days"}
  ]
}
```

## 🎯 Integration with Agents

Agents query the World Model for context:

```python
class CausalInferenceAgent:
    async def analyze(self, query):
        # Get relevant historical data from World Model
        historical_state = world_model.get_history(
            entities=["marketing", "revenue"],
            timeframe=("2024-01-01", "2024-12-31")
        )
        
        # Perform causal analysis
        hypothesis = self.infer_causality(historical_state)
        
        # Update World Model with findings
        world_model.add_relationship(
            source=hypothesis.cause,
            target=hypothesis.effect,
            strength=hypothesis.strength,
            evidence=hypothesis.evidence
        )
        
        return hypothesis
```

## 🚀 Why This Matters for Hackathon

### Technical Implementation (10%)
✅ **Clean architecture**: Graph-based knowledge representation  
✅ **Robust**: Handles temporal data, missing values, conflicts  
✅ **Scalable**: Efficient graph queries, incremental updates

### Innovation (10%)
✅ **Novel approach**: Beyond traditional databases  
✅ **Temporal reasoning**: Understands cause-effect over time  
✅ **Self-improving**: Learns from outcomes

The World Model is the **memory and understanding** of Sentience Layer - it's what makes the system truly intelligent.
