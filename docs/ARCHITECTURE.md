# 🏗️ Sentience Layer - Technical Architecture

## System Overview

Sentience Layer is built as a **microservices architecture** with three main layers:
1. **Frontend Layer** (Next.js)
2. **Backend Layer** (FastAPI + Node.js)
3. **Data Layer** (PostgreSQL, Redis, ChromaDB)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│                    Next.js 14 + React 18                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐     │
│  │Dashboard │ Insights │Simulation│  Memory  │  Vault   │     │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/WebSocket
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼────────┐             ┌────────▼────────┐
│  Node.js API    │             │   Python API    │
│  (TypeScript)   │             │    (FastAPI)    │
│                 │             │                 │
│ • WebSocket     │◄───────────►│ • Agent Engine │
│ • Rate Limit    │   HTTP      │ • ML Models    │
│ • Auth          │             │ • Causal AI    │
│ • Routing       │             │ • Simulation   │
└────────┬────────┘             └────────┬────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼────┐  ┌────▼────┐  ┌─────▼─────┐  ┌────▼────┐
    │PostgreSQL│  │  Redis  │  │ ChromaDB  │  │ Celery  │
    │         │  │ (Cache) │  │ (Vectors) │  │ Workers │
    └─────────┘  └─────────┘  └───────────┘  └─────────┘
```

## Component Details

### 1. Frontend (Next.js)

**Technology Stack**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Radix UI components
- Lucide icons

**Key Features**
- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes
- Real-time updates via WebSocket
- Responsive design

**Directory Structure**
```
frontend/
├── src/
│   ├── app/              # App router pages
│   │   ├── page.tsx      # Landing page
│   │   ├── dashboard/    # Dashboard pages
│   │   ├── insights/     # Insights pages
│   │   └── simulations/  # Simulation pages
│   ├── components/       # React components
│   │   ├── ui/          # Base UI components
│   │   ├── insights/    # Insight components
│   │   └── charts/      # Chart components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utilities
│   ├── store/           # State management
│   └── types/           # TypeScript types
├── public/              # Static assets
└── package.json
```

### 2. Python Backend (FastAPI)

**Technology Stack**
- FastAPI 0.109.0
- Python 3.11+
- Pydantic for validation
- SQLAlchemy for ORM
- Asyncio for concurrency

**Key Components**

**Agent System**
```python
backend/python/agents/
├── base_agent.py           # Base agent class
├── causal_inference_agent.py
├── debate_agent.py
├── consensus_agent.py
├── action_priority_agent.py
└── ... (18 agents total)
```

**API Routes**
```python
backend/python/api/routes/
├── health.py      # Health checks
├── ingest.py      # Data ingestion
├── insights.py    # Insight generation
├── simulate.py    # Action simulation
├── causal.py      # Causal analysis
├── debate.py      # Multi-agent debate
└── actions.py     # Action recommendations
```

**Core Services**
```python
backend/python/
├── main.py              # FastAPI app
├── config.py            # Configuration
├── simulation.py        # Simulation engine
├── strategist.py        # Strategy planning
├── analysis.py          # Data analysis
├── ingestion.py         # Data ingestion
└── celery_app.py        # Celery tasks
```

### 3. Node.js Backend (TypeScript)

**Technology Stack**
- Node.js 18+
- TypeScript
- Express.js
- Socket.io for WebSocket
- Redis for caching

**Responsibilities**
- WebSocket connections for real-time updates
- Rate limiting
- Authentication middleware
- Request routing
- Session management

**Directory Structure**
```
backend/node/
├── src/
│   ├── server.ts         # Main server
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   │   ├── n8nClient.ts  # N8N integration
│   │   └── websocket.ts  # WebSocket handler
│   ├── middleware/       # Express middleware
│   │   ├── auth.ts       # Authentication
│   │   ├── rateLimiter.ts
│   │   └── errorHandler.ts
│   └── utils/
│       └── logger.ts     # Logging
└── package.json
```

### 4. Data Layer

**PostgreSQL**
- Primary data store
- Stores: users, insights, simulations, decisions
- ACID compliance for transactions

**Schema**
```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    role VARCHAR(50),
    created_at TIMESTAMP
);

-- Insights
CREATE TABLE insights (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    query TEXT,
    finding TEXT,
    confidence FLOAT,
    agents_consulted JSONB,
    created_at TIMESTAMP
);

-- Simulations
CREATE TABLE simulations (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action JSONB,
    outcomes JSONB,
    recommendation TEXT,
    created_at TIMESTAMP
);
```

**Redis**
- Session storage
- Cache for frequent queries
- Celery message broker
- Rate limiting counters

**ChromaDB**
- Vector embeddings for semantic search
- Stores document embeddings
- Fast similarity search

### 5. Background Workers (Celery)

**Task Types**
```python
# Agent tasks
@celery.task
def run_agent_analysis(query, context):
    # Long-running agent analysis
    pass

# Cleanup tasks
@celery.task
def cleanup_old_data():
    # Periodic cleanup
    pass

# Report generation
@celery.task
def generate_weekly_report(user_id):
    # Scheduled reports
    pass
```

## Data Flow

### Example: Insight Generation

```
1. User submits query via frontend
   ↓
2. Frontend → Node.js API (WebSocket connection)
   ↓
3. Node.js → Python API (HTTP request)
   ↓
4. Python API routes to agent orchestrator
   ↓
5. Orchestrator spawns relevant agents in parallel
   ├─ Causal Inference Agent
   ├─ Debate Agent
   └─ Uncertainty Agent
   ↓
6. Agents query World Model (PostgreSQL + ChromaDB)
   ↓
7. Agents perform reasoning (Google Antigravity)
   ↓
8. Consensus Agent synthesizes results
   ↓
9. Result stored in PostgreSQL
   ↓
10. Response streamed via WebSocket to frontend
    ↓
11. Frontend updates UI in real-time
```

## Security Architecture

### Authentication Flow
```
1. User login → JWT token issued
2. Token stored in httpOnly cookie
3. Every request includes token
4. Middleware validates token
5. User context attached to request
```

### Authorization
```python
@app.get("/api/insights")
async def get_insights(
    user: User = Depends(get_current_user),
    required_role: str = "analyst"
):
    if user.role not in ["analyst", "admin"]:
        raise HTTPException(403, "Forbidden")
    # Process request
```

### Data Encryption
- **At Rest**: AES-256 for sensitive fields
- **In Transit**: TLS 1.3 for all connections
- **Secrets**: Environment variables, never in code

## Scalability

### Horizontal Scaling

**Frontend**
- Deploy multiple Next.js instances
- Load balancer (Nginx/AWS ALB)
- CDN for static assets (CloudFront)

**Backend**
- Multiple FastAPI workers (Gunicorn)
- Multiple Node.js instances
- Redis for session sharing

**Database**
- PostgreSQL read replicas
- Connection pooling (PgBouncer)
- Database sharding for multi-tenant

### Caching Strategy

**L1: In-Memory Cache**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_agent_config(agent_id: str):
    # Cached in memory
    pass
```

**L2: Redis Cache**
```python
async def get_insight(insight_id: str):
    # Check Redis first
    cached = await redis.get(f"insight:{insight_id}")
    if cached:
        return cached
    
    # Fetch from database
    insight = await db.query(...)
    
    # Cache for 1 hour
    await redis.setex(f"insight:{insight_id}", 3600, insight)
    return insight
```

**L3: Database**
- PostgreSQL with indexes
- Query optimization
- Materialized views for complex queries

## Monitoring & Observability

### Metrics (Prometheus)
```python
from prometheus_client import Counter, Histogram

# Request metrics
request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    request_count.inc()
    with request_duration.time():
        response = await call_next(request)
    return response
```

### Logging (Structured)
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "insight_generated",
    insight_id=insight.id,
    user_id=user.id,
    confidence=insight.confidence,
    agents_used=len(insight.agents)
)
```

### Tracing (Distributed)
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("generate_insight")
async def generate_insight(query: str):
    # Traced operation
    pass
```

## Deployment

### Docker Compose (Development)
```yaml
services:
  postgres:
    image: postgres:14
  redis:
    image: redis:7
  backend-python:
    build: ./backend/python
  backend-node:
    build: ./backend/node
  frontend:
    build: ./frontend
```

### Kubernetes (Production)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentience-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentience-backend
  template:
    spec:
      containers:
      - name: backend
        image: sentience-backend:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## Performance Optimization

### Database Optimization
```sql
-- Indexes for common queries
CREATE INDEX idx_insights_user_id ON insights(user_id);
CREATE INDEX idx_insights_created_at ON insights(created_at DESC);
CREATE INDEX idx_simulations_user_id ON simulations(user_id);

-- Partial index for active users
CREATE INDEX idx_active_users ON users(id) WHERE active = true;
```

### Query Optimization
```python
# Bad: N+1 query problem
for insight in insights:
    user = await db.get_user(insight.user_id)  # N queries

# Good: Eager loading
insights = await db.query(Insight).options(
    joinedload(Insight.user)
).all()  # 1 query
```

### Async Operations
```python
# Parallel agent execution
results = await asyncio.gather(
    causal_agent.analyze(query),
    debate_agent.discuss(query),
    uncertainty_agent.assess(query)
)
```

## Technology Choices Rationale

### Why FastAPI?
- Async/await support for concurrency
- Automatic API documentation
- Type validation with Pydantic
- High performance (comparable to Node.js)

### Why Next.js?
- Server-side rendering for SEO
- File-based routing
- API routes for backend-for-frontend
- Excellent developer experience

### Why PostgreSQL?
- ACID compliance for critical data
- Rich query capabilities
- JSON support for flexible schemas
- Mature ecosystem

### Why Redis?
- In-memory speed for caching
- Pub/sub for real-time features
- Atomic operations for rate limiting
- Celery integration

## Future Architecture Improvements

### Phase 1
- [ ] GraphQL API for flexible queries
- [ ] gRPC for inter-service communication
- [ ] Event sourcing for audit trail

### Phase 2
- [ ] Microservices per agent type
- [ ] Service mesh (Istio)
- [ ] Multi-region deployment

### Phase 3
- [ ] Edge computing for low latency
- [ ] Serverless functions for scaling
- [ ] Real-time data streaming (Kafka)

---

**This architecture supports the hackathon demo and scales to enterprise production.**
