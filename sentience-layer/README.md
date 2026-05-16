# 🧠 Sentience Layer v4.0

> **A Cognitive Operating System for Business Intelligence**  
> Google Antigravity Hackathon 2024 Entry

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.3-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

**Sentience Layer** is an advanced multi-agent AI system that transforms raw business data into actionable insights through cognitive reasoning, causal inference, and predictive analytics. Built for the Google Antigravity Hackathon, it leverages Google's Gemini AI and Cloud AI Platform to create a "thinking layer" for enterprise decision-making.

### 🎯 Key Innovation

Unlike traditional BI tools that simply visualize data, Sentience Layer **understands context, debates alternatives, predicts outcomes, and recommends actions** through a network of 18 specialized AI agents working in concert.

## ✨ Features

### 🤖 18 Specialized AI Agents

| Agent | Purpose |
|-------|---------|
| **Action Category** | Classifies business actions into strategic categories |
| **Action Playbook** | Generates step-by-step execution plans |
| **Action Priority** | Ranks actions by impact and urgency |
| **Action Ranking** | Scores and compares multiple strategies |
| **Adversarial Test** | Stress-tests decisions against worst-case scenarios |
| **Causal Inference** | Identifies true cause-effect relationships in data |
| **Consensus** | Synthesizes multiple agent perspectives |
| **Critic** | Challenges assumptions and identifies blind spots |
| **Debate** | Argues multiple viewpoints for balanced decisions |
| **Deterministic** | Provides rule-based, explainable reasoning |
| **Dream** | Explores creative, unconventional solutions |
| **Economic** | Analyzes financial impact and ROI |
| **Ethics** | Evaluates decisions against ethical frameworks |
| **Memory-Enabled** | Learns from past decisions and outcomes |
| **Opportunity Analyst** | Identifies hidden opportunities in data |
| **Personalization** | Tailors insights to user roles and preferences |
| **Premonition** | Predicts future trends and outcomes |
| **Uncertainty** | Quantifies risk and confidence intervals |

### 🔥 Core Capabilities

- **🧩 Multi-Agent Orchestration**: Agents collaborate, debate, and reach consensus
- **🔮 Predictive Analytics**: Forecast business outcomes with confidence intervals
- **🎯 Causal Reasoning**: Understand *why* things happen, not just *what* happened
- **💡 Action Recommendations**: Get concrete, prioritized action plans
- **🌐 Real-Time Insights**: WebSocket-based live updates
- **🔐 Enterprise Security**: Role-based access control and data encryption
- **📊 Interactive Dashboard**: Beautiful Next.js UI with real-time visualizations
- **🔌 Extensible Architecture**: Plugin system for custom agents and data sources

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  Dashboard • Insights • Simulations • Memory • Vault        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐         ┌────────▼────────┐
│  Node.js API   │         │   Python API    │
│  (TypeScript)  │         │    (FastAPI)    │
│                │         │                 │
│ • WebSockets   │         │ • Agent Engine  │
│ • Rate Limit   │         │ • ML Models     │
│ • Auth         │         │ • Causal AI     │
└───────┬────────┘         └────────┬────────┘
        │                           │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │                           │
   ┌────▼────┐  ┌────▼────┐  ┌─────▼─────┐
   │PostgreSQL│  │  Redis  │  │ ChromaDB  │
   │         │  │ (Cache) │  │ (Vectors) │
   └─────────┘  └─────────┘  └───────────┘
```

### Technology Stack

**Backend:**
- **Python 3.11+**: FastAPI, Pydantic, SQLAlchemy
- **Node.js**: Express, TypeScript, WebSocket
- **AI/ML**: Google Gemini, Transformers, Scikit-learn
- **Causal AI**: DoWhy, CausalNex
- **Vector DB**: ChromaDB, FAISS, Sentence Transformers

**Frontend:**
- **Next.js 14**: React 18, TypeScript
- **UI**: Tailwind CSS, Radix UI, Lucide Icons
- **State**: React Hooks, Context API

**Infrastructure:**
- **Database**: PostgreSQL, Redis
- **Orchestration**: N8N, Celery
- **Deployment**: Docker, Docker Compose
- **Monitoring**: Prometheus, Loguru

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentience-layer.git
cd sentience-layer
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Node.js dependencies**
```bash
# Backend Node.js
cd backend/node
npm install

# Frontend
cd ../../frontend
npm install
```

5. **Initialize database**
```bash
# Run database migrations
python -m alembic upgrade head
```

6. **Start the services**

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Manual Start**
```bash
# Terminal 1: Python API
cd backend/python
uvicorn main:app --reload --port 8000

# Terminal 2: Node.js API
cd backend/node
npm run dev

# Terminal 3: Frontend
cd frontend
npm run dev

# Terminal 4: Celery Workers
celery -A celery_app worker --loglevel=info
```

7. **Access the application**
- Frontend: http://localhost:3000
- Python API: http://localhost:8000
- Node.js API: http://localhost:3001
- API Docs: http://localhost:8000/docs

## 📖 Usage

### Basic Workflow

1. **Ingest Data**: Upload CSV, connect databases, or use API integrations
2. **Ask Questions**: Natural language queries like "Why did sales drop last quarter?"
3. **Get Insights**: Multi-agent analysis with causal reasoning
4. **Simulate Scenarios**: Test "what-if" scenarios before taking action
5. **Execute Actions**: Get prioritized, step-by-step playbooks

### API Examples

**Ingest Data**
```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source": "csv",
    "data": "sales_data.csv",
    "metadata": {"department": "sales"}
  }'
```

**Get Insights**
```bash
curl -X POST http://localhost:8000/api/insights \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What factors caused the revenue decline?",
    "context": {"timeframe": "Q4 2023"}
  }'
```

**Run Simulation**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "increase_marketing_budget",
    "parameters": {"budget_increase": 0.2}
  }'
```

## 🧪 Testing

```bash
# Python tests
pytest tests/ -v --cov

# Node.js tests
cd backend/node
npm test

# Frontend tests
cd frontend
npm test

# End-to-end tests
npm run test:e2e
```

## 📁 Project Structure

```
sentience-layer/
├── backend/
│   ├── python/              # FastAPI backend
│   │   ├── agents/          # 18 AI agents
│   │   ├── api/             # API routes
│   │   ├── models/          # Database models
│   │   ├── tasks/           # Celery tasks
│   │   └── utils/           # Utilities
│   └── node/                # Node.js backend
│       ├── src/
│       │   ├── routes/      # API endpoints
│       │   ├── services/    # Business logic
│       │   └── middleware/  # Auth, rate limiting
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # App router pages
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   └── store/          # State management
├── database/               # Database schemas
├── ml-models/              # Trained models
├── n8n/                    # Workflow automation
├── docs/                   # Documentation
├── tests/                  # Test suites
└── docker/                 # Docker configs
```

## 🎨 Key Features Demo

### 1. Causal Inference
```python
# Identify true causes, not just correlations
result = await causal_agent.analyze(
    data=sales_data,
    outcome="revenue",
    treatment="marketing_spend"
)
# Returns: "20% increase in marketing → 8% revenue lift (p<0.05)"
```

### 2. Multi-Agent Debate
```python
# Get balanced perspectives
debate = await debate_agent.discuss(
    question="Should we expand to Asia?",
    agents=["economic", "ethics", "uncertainty"]
)
# Returns: Pros, cons, risks, and consensus recommendation
```

### 3. Predictive Simulations
```python
# Test scenarios before committing
simulation = await simulate(
    action="hire_10_engineers",
    horizon="6_months"
)
# Returns: Predicted outcomes with confidence intervals
```

## 🔐 Security

- **Authentication**: JWT-based auth with refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **Data Encryption**: AES-256 for data at rest, TLS 1.3 in transit
- **Rate Limiting**: Configurable per-endpoint limits
- **Audit Logging**: Complete audit trail of all actions
- **Input Validation**: Pydantic schemas for all inputs

See [SECURITY.md](SECURITY.md) for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud AI Platform** for Gemini API access
- **Anthropic** for Claude integration
- **DoWhy & CausalNex** for causal inference capabilities
- **FastAPI & Next.js** communities for excellent frameworks

## 📞 Contact

- **Project Lead**: [Your Name]
- **Email**: your.email@example.com
- **Hackathon**: Google Antigravity 2024
- **Demo**: [Live Demo Link]

## 🗺️ Roadmap

- [ ] Real-time collaborative insights
- [ ] Mobile app (iOS/Android)
- [ ] Advanced visualization engine
- [ ] Multi-language support
- [ ] Enterprise SSO integration
- [ ] Custom agent builder UI
- [ ] Automated report generation
- [ ] Slack/Teams integration

---

**Built with ❤️ for Google Antigravity Hackathon 2024**
