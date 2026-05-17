# 📡 Sentience Layer - API Documentation

## Base URLs

- **Python API**: `http://localhost:8000`
- **Node.js API**: `http://localhost:3001`
- **Interactive Docs**: `http://localhost:8000/docs`

## Authentication

All API endpoints require JWT authentication (except health check).

### Get Access Token
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "your_password"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Use Token
```bash
# Include in Authorization header
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Core Endpoints

### 1. Health Check

**GET** `/api/health`

Check system status.

```bash
curl http://localhost:8000/api/health
```

**Response**
```json
{
  "status": "healthy",
  "components": {
    "kernel": "online",
    "world_model": "online",
    "agents": 18
  },
  "timestamp": "2024-11-15T10:30:00Z"
}
```

### 2. Data Ingestion

**POST** `/api/ingest`

Ingest data for analysis.

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "csv",
    "data": "sales_data.csv",
    "metadata": {
      "department": "sales",
      "period": "Q4_2024"
    }
  }'
```

**Request Body**
```typescript
{
  source: "csv" | "json" | "database" | "api";
  data: string | object;
  metadata?: {
    [key: string]: any;
  };
}
```

**Response**
```json
{
  "ingestion_id": "ING-2024-001",
  "status": "success",
  "records_processed": 1247,
  "timestamp": "2024-11-15T10:30:00Z"
}
```

### 3. Generate Insights

**POST** `/api/insights`

Get AI-powered insights from data.

```bash
curl -X POST http://localhost:8000/api/insights \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why did revenue drop in Q4?",
    "context": {
      "timeframe": "Q4_2024",
      "department": "sales"
    }
  }'
```

**Request Body**
```typescript
{
  query: string;
  context?: {
    timeframe?: string;
    department?: string;
    [key: string]: any;
  };
  agents?: string[];  // Specific agents to use
}
```

**Response**
```json
{
  "insight_id": "INS-2024-Q4-001",
  "query": "Why did revenue drop in Q4?",
  "finding": "Marketing budget cut caused 15% revenue decline",
  "confidence": 0.92,
  "causal_chain": [
    "Marketing spend reduced 30% on 2024-07-01",
    "Lead volume dropped 35% in August",
    "Pipeline decreased 28% in September",
    "Revenue declined 15% in Q4"
  ],
  "recommendation": {
    "action": "Restore marketing budget to Q3 levels",
    "expected_outcome": "+12% revenue within 90 days",
    "confidence": 0.88
  },
  "agents_consulted": ["causal_inference", "economic", "uncertainty"],
  "processing_time_ms": 2847
}
```

### 4. Run Simulation

**POST** `/api/simulate`

Simulate action outcomes before execution.

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "type": "budget_increase",
      "category": "marketing",
      "amount": 25000
    },
    "scenarios": 1000,
    "horizon_days": 90
  }'
```

**Request Body**
```typescript
{
  action: {
    type: string;
    category: string;
    amount?: number;
    [key: string]: any;
  };
  scenarios?: number;  // Default: 1000
  horizon_days?: number;  // Default: 90
}
```

**Response**
```json
{
  "simulation_id": "SIM-2024-11-15-001",
  "action": "Increase marketing budget by $25K",
  "scenarios_run": 1000,
  "outcome_distribution": {
    "revenue": {
      "p10": 1080000,
      "p50": 1120000,
      "p90": 1180000,
      "mean": 1122000
    },
    "roi": {
      "p50": 2.4,
      "confidence_90": [1.6, 3.6]
    }
  },
  "recommendation": {
    "decision": "PROCEED",
    "confidence": 0.88,
    "rationale": "92% probability of positive ROI"
  }
}
```

### 5. Get Action Recommendations

**POST** `/api/actions/recommend`

Get prioritized action recommendations.

```bash
curl -X POST http://localhost:8000/api/actions/recommend \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Increase revenue by 20%",
    "constraints": {
      "budget": 100000,
      "timeframe_days": 90
    }
  }'
```

**Response**
```json
{
  "recommendations": [
    {
      "action": "Restore marketing budget",
      "priority": 1,
      "expected_impact": "+12% revenue",
      "confidence": 0.88,
      "effort": "low",
      "risk": "low",
      "playbook": {
        "steps": [
          "Secure CFO approval",
          "Restore budget to existing channels",
          "Monitor CAC daily"
        ],
        "timeline_days": 7
      }
    }
  ]
}
```

### 6. Causal Analysis

**POST** `/api/causal/analyze`

Identify causal relationships in data.

```bash
curl -X POST http://localhost:8000/api/causal/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [...],
    "cause": "marketing_spend",
    "effect": "revenue"
  }'
```

**Response**
```json
{
  "causal_relationship": {
    "cause": "marketing_spend",
    "effect": "revenue",
    "strength": 0.85,
    "confidence": 0.92,
    "mechanism": "Spend → Leads → Pipeline → Revenue"
  },
  "evidence": {
    "granger_test": {"p_value": 0.003},
    "counterfactual": "Revenue stable when marketing constant",
    "confounders": []
  }
}
```

### 7. Multi-Agent Debate

**POST** `/api/debate`

Run multi-agent debate on a topic.

```bash
curl -X POST http://localhost:8000/api/debate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Should we expand to Asian markets?",
    "agents": ["economic", "ethics", "uncertainty"],
    "rounds": 3
  }'
```

**Response**
```json
{
  "debate_id": "DEB-2024-001",
  "topic": "Should we expand to Asian markets?",
  "rounds_conducted": 3,
  "arguments": {
    "pro": [
      {
        "claim": "Market size: 4.5B potential customers",
        "strength": 0.85,
        "agent": "economic"
      }
    ],
    "con": [
      {
        "claim": "Regulatory complexity: 12 frameworks",
        "strength": 0.78,
        "agent": "ethics"
      }
    ]
  },
  "consensus": {
    "recommendation": "Expand with phased approach",
    "confidence": 0.78,
    "conditions": ["Start with Singapore", "Pilot for 6 months"]
  }
}
```

## WebSocket API

### Real-Time Insights Stream

Connect to WebSocket for real-time reasoning updates.

```javascript
const ws = new WebSocket('ws://localhost:3001/ws/insights');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    query: 'Why did revenue drop?'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Reasoning step:', data);
  // {
  //   agent: "causal_inference",
  //   thought: "Analyzing correlation...",
  //   confidence: 0.75
  // }
};
```

## Rate Limits

- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise**: Unlimited

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |

## SDKs

### Python SDK
```python
from sentience import SentienceClient

client = SentienceClient(api_key="YOUR_API_KEY")

# Get insights
result = client.insights.create(
    query="Why did revenue drop?",
    context={"timeframe": "Q4_2024"}
)

print(result.finding)
```

### JavaScript SDK
```javascript
import { SentienceClient } from '@sentience/sdk';

const client = new SentienceClient({ apiKey: 'YOUR_API_KEY' });

// Run simulation
const simulation = await client.simulations.create({
  action: { type: 'budget_increase', amount: 25000 },
  scenarios: 1000
});

console.log(simulation.recommendation);
```

## Support

- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Email**: api-support@sentiencelayer.ai
