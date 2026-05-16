# 📚 Sentience Layer Documentation

Welcome to the Sentience Layer documentation! This guide will help you understand, set up, and use the Cognitive Operating System for Business Intelligence.

## 📖 Documentation Index

### Getting Started
- **[Setup Guide](SETUP.md)** - Installation and configuration
- **[API Documentation](API.md)** - REST API reference
- **[Architecture Overview](ARCHITECTURE.md)** - Technical architecture

### Core Concepts
- **[Sentience Layer Concept](SENTIENCE_LAYER.md)** - What is Sentience Layer?
- **[Cognitive OS](COGNITIVE_OS.md)** - Operating system for AI reasoning
- **[World Model](WORLD_MODEL.md)** - Temporal knowledge graph

### Agent System
- **[Agent Architecture](AGENTS.md)** - 18 specialized AI agents
- **[Dream Mode](DREAM_MODE.md)** - Creative reasoning mode
- **[Agentic Reasoning](AGENTS.md#multi-agent-workflows)** - Multi-agent collaboration

### Features
- **[Action Simulation](EVALUATION.md)** - Monte Carlo simulation
- **[Causal Inference](AGENTS.md#causal-inference-agent)** - Root cause analysis
- **[Multi-Agent Debate](AGENTS.md#debate-agent)** - Perspective exploration

### Hackathon
- **[Hackathon Pitch](HACKATHON_PITCH.md)** - Competition submission
- **[Evaluation Criteria](EVALUATION.md)** - How we meet criteria
- **[Demo Script](DEMO_SCRIPT.md)** - Live demonstration guide

### Business
- **[Enterprise Roadmap](ENTERPRISE_ROADMAP.md)** - Future plans
- **[Security Policy](../SECURITY.md)** - Security features

## 🎯 Quick Links

### For Users
- [How to get insights](API.md#3-generate-insights)
- [How to run simulations](API.md#4-run-simulation)
- [How to get recommendations](API.md#5-get-action-recommendations)

### For Developers
- [Setup development environment](SETUP.md#method-2-manual-setup)
- [Add a new agent](../CONTRIBUTING.md#adding-a-new-agent)
- [Run tests](SETUP.md#testing)

### For Evaluators
- [Google Antigravity usage](HACKATHON_PITCH.md#why-google-antigravity-is-central)
- [Agentic reasoning examples](AGENTS.md#multi-agent-workflows)
- [Insight quality](SENTIENCE_LAYER.md#key-innovations)
- [Simulation examples](EVALUATION.md#real-simulation-example)

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/sentience-layer.git
cd sentience-layer

# 2. Run setup
./setup.sh

# 3. Configure API keys
nano .env

# 4. Start services
docker-compose up -d

# 5. Access application
open http://localhost:3000
```

## 📊 Architecture Overview

```
Frontend (Next.js) → Node.js API → Python API → Agents
                                              ↓
                                    PostgreSQL + Redis + ChromaDB
```

## 🤖 18 AI Agents

1. **Causal Inference** - Identify true causes
2. **Debate** - Argue multiple perspectives
3. **Consensus** - Synthesize viewpoints
4. **Action Priority** - Rank by impact
5. **Action Playbook** - Generate execution plans
6. **Action Ranking** - Compare alternatives
7. **Adversarial Test** - Stress-test decisions
8. **Uncertainty** - Quantify risk
9. **Opportunity Analyst** - Find hidden opportunities
10. **Premonition** - Predict future events
11. **Dream** - Explore creative solutions
12. **Economic** - Analyze financial impact
13. **Ethics** - Evaluate ethical implications
14. **Memory-Enabled** - Learn from outcomes
15. **Personalization** - Tailor to user
16. **Deterministic** - Rule-based reasoning
17. **Critic** - Challenge assumptions
18. **Action Category** - Classify actions

## 🎯 Key Features

### Causal Reasoning
```python
# Not just correlation
"Revenue and marketing are correlated (r=0.85)"

# True causation
"Marketing CAUSES revenue with 92% confidence
 Mechanism: Spend → Leads → Pipeline → Revenue"
```

### Multi-Agent Debate
```python
# Explore perspectives
debate = await debate_agent.discuss(
    question="Should we expand to Asia?",
    agents=["economic", "ethics", "uncertainty"]
)
# Returns: Pros, cons, risks, consensus
```

### Action Simulation
```python
# Test before investing
simulation = await simulate(
    action="increase_marketing_budget",
    scenarios=1000
)
# Returns: Expected ROI with confidence intervals
```

## 📈 Use Cases

### 1. Revenue Decline Investigation
**Question**: "Why did Q4 revenue drop?"
**Output**: Root cause, impact quantification, recommended action

### 2. Customer Churn Prevention
**Question**: "Which customers will churn?"
**Output**: Risk scores, factors, retention strategies

### 3. Strategic Decision Making
**Question**: "Should we expand to Asia?"
**Output**: Multi-perspective analysis, simulated outcomes

## 🔐 Security

- JWT authentication
- Role-based access control
- Data encryption (AES-256)
- Rate limiting
- Audit logging

See [SECURITY.md](../SECURITY.md) for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📞 Support

- **Documentation**: This folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/sentience-layer/issues)
- **Email**: support@sentiencelayer.ai

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

## 🏆 Hackathon

Built for **Google AI Sekho - Build with Antigravity Hackathon**

### Evaluation Criteria Alignment

| Criteria | Weight | Our Approach |
|----------|--------|--------------|
| Google Antigravity Usage | 25% | [Deep integration](HACKATHON_PITCH.md#why-google-antigravity-is-central) |
| Agentic Reasoning | 20% | [18 specialized agents](AGENTS.md) |
| Insight Quality | 20% | [Causal explanations](SENTIENCE_LAYER.md#key-innovations) |
| Action Simulation | 15% | [Monte Carlo simulation](EVALUATION.md) |
| Technical Implementation | 10% | [Clean architecture](ARCHITECTURE.md) |
| Innovation & UX | 10% | [Transparent AI](COGNITIVE_OS.md) |

## 🗺️ Roadmap

- **Q1 2025**: Production-ready platform
- **Q2-Q3 2025**: Industry specialization
- **Q4 2025**: Advanced features
- **2026**: Global scale

See [ENTERPRISE_ROADMAP.md](ENTERPRISE_ROADMAP.md) for details.

---

**Built with ❤️ and Google Antigravity**
