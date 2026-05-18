# 🧠 Sentience Layer v4.0

> **A Cognitive Operating System for Business Intelligence & Swarm Intelligence Orchestration**  
> Google Antigravity Hackathon Award-Winning Enterprise Reasoning Architecture

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.3-black.svg?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![CapacitorJS](https://img.shields.io/badge/Capacitor-8.0-red.svg?style=for-the-badge&logo=capacitor&logoColor=white)](https://capacitorjs.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Hosting-FFCA28.svg?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

**Sentience Layer** is an advanced cognitive operating system that transforms raw business telemetry into strategic recommendations through distributed causal inference, multi-agent debates, and Monte Carlo scenario simulations. 

Unlike legacy BI tools that only chart what has already happened, Sentience Layer **reasons, doubts, stress-tests assumptions, and suggests concrete step-by-step playbooks** through a network of 18 specialized AI agents working together via formal agent-to-agent message envelopes.

---

## ✨ System Highlights

- 🧠 **Swarm Orchestrator Pipeline**: Initiates a formal Critic 🔍 → Consensus 🤝 → Action Playbook 📋 chain running on Google Antigravity LLM.
- ✉️ **Signed Message Envelopes**: Agents communicate via stateful, signed JSON envelopes containing validation headers, transaction IDs, and cryptographic verification signatures.
- ⚡ **WebSocket Telemetry Stream**: Broadcasts internal thoughts, tool executions, and step-by-step reasoning traces directly to the dashboard.
- 🔌 **Postgres MCP Server**: Automatically registers and exposes local relational schema tools (`postgres_list_tables`, database execution queries) to the agent swarm.
- ⚙️ **Zustand Verbosity Preferences**: A global preference toggle (**Brief**, **Default**, **Detailed**) persisted in the frontend store to adjust reasoning output length.
- 🔒 **Secure Memory Vault**: Supports drag-and-drop document uploads (`.pdf`, `.txt`, `.csv`, `.json`), parsing them using local extractors and storing them securely.
- 📱 **Capacitor Mobile Native**: Includes a Next.js 14 mobile-optimized web app packaged with CapacitorJS to run natively on Android/iOS.
- 🔥 **Firebase Hosting Deployment**: Ready-to-go hosting configurations and NPM scripts for rapid static deployment.

---

## 🏗️ System Architecture

```
                                  ┌────────────────────────────────────────┐
                                  │           Next.js Frontend             │
                                  │      (Web Dashboard & Mobile UI)       │
                                  └───────────┬────────────────┬───────────┘
                                              │                │
                                    HTTP APIs │                │ WebSockets
                                 (REST State) │                │ (Live Telemetry)
                                              ▼                ▼
                                  ┌────────────────────────────────────────┐
                                  │       FastAPI API Gateway Engine       │
                                  │         (Port 8000 Orchestration)      │
                                  └─────┬────────────────────────────┬─────┘
                                        │                            │
                                        │ Local Import               │ Tool Registry
                                        ▼                            ▼
                      ┌──────────────────────────────────┐  ┌──────────────────────────────────┐
                      │    SwarmOrchestrator Pipeline    │  │    PostgreSQL MCP Tool Server    │
                      │  Critic ➔ Consensus ➔ Playbook   │  │  (Schema, Tables, SQL Execution) │
                      └─────────────────┬────────────────┘  └─────────────────┬────────────────┘
                                        │                                     │
                                        │ Antigravity Generative Calls        │ Read / Write
                                        ▼                                     ▼
                      ┌──────────────────────────────────┐  ┌──────────────────────────────────┐
                      │      Google Cloud AI Suite       │  │        Relational Storage        │
                      │      (Antigravity & Gemini)      │  │        (PostgreSQL + Redis)      │
                      └──────────────────────────────────┘  └──────────────────────────────────┘
```

---

## 👥 The 18 Specialized Agents

Sentience Layer utilizes **distributed cognitive reasoning**. The agents are categorized into specialized quadrants:

| Quadrant | Agent Name | Core Responsibility |
|---|---|---|
| **🔍 Analysis & Causal AI** | `Causal Inference` | Identifies true cause-and-effect pathways, avoiding correlation bias. |
| | `Uncertainty` | Quantifies confidence boundaries and risks using sensitivity models. |
| | `Opportunity Analyst` | Discovers hidden synergies and anomaly potentials in incoming tables. |
| | `Action Category` | Classifies proposed strategic steps into standard organizational categories. |
| **🗣️ Swarm Deliberation** | `Critic` | Stress-audits claims, reviews constraints, and extracts unverified assumptions. |
| | `Consensus` | Synthesizes conflicting outputs and weights votes by confidence level. |
| | `Debate` | Argues multi-perspective viewpoints (Pro vs. Con) to expand insight breadth. |
| | `Ethics` | Audits proposed decisions against corporate and regulatory guidelines. |
| **🎯 Action Execution** | `Action Playbook` | Decomposes goals into concrete, assigned step-by-step task logs. |
| | `Action Priority` | Scores and ranks actions by feasibility, impact, and deadline urgency. |
| | `Action Ranking` | Benchmarks and filters competing action plans against target budgets. |
| **🔮 Foresight & Creation** | `Premonition` | Forecasts short-term and long-term indicators to project upcoming events. |
| | `Dream` | Relaxes operational constraints to brainstorm high-novelty answers. |
| | `Memory-Enabled` | Stores and recalls historical chat outcomes in episodic repositories. |
| | `Personalization` | Adapts outputs to match unique viewer roles and preferred styles. |
| | `Deterministic` | Processes explicit rule-based mappings to guarantee explainable traces. |
| | `Adversarial Test` | Assesses worst-case disaster scenarios to pressure-test action robustly. |

---

## ✉️ Swarm Agent Handoff Protocol

The `SwarmOrchestrator` runs a structured 3-agent chain where outputs are packed into formal **AgentMessageEnvelopes** and passed down the pipeline:

```json
{
  "protocol_version": "1.0.0",
  "message_id": "8b7e2832-5c91-4cf1-83da-8e99a8cb40ff",
  "session_id": "sess_1716035671_a7bf28",
  "sender": "ConsensusAgent",
  "recipient": "ActionPlaybookAgent",
  "payload": {
    "key_finding": "Onboarding SMS validation failure accounts for 68% of churn.",
    "insight": "Causal analysis demonstrates high temporal precedence between validation delay and drop-off...",
    "confidence": 0.92,
    "severity": "HIGH",
    "evidence": ["Verification delay > 40s in 84% of cases", "Conversion falls from 92% to 14%"]
  },
  "timestamp": 1716035678.924,
  "signature": "antigravity-swarm-signed-sha256"
}
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Redis 7+**
- **Firebase CLI** (for hosting deployment)

### 1. Repository Setup
Clone the repository and copy the environment template:
```bash
git clone https://github.com/MuhammadJohnRaza/sentience-layer.git
cd sentience-layer
cp .env.example .env
```
*Configure `.env` with your `GOOGLE_ANTIGRAVITY_API_KEY`, `GOOGLE_GEMINI_API_KEY`, and database URLs.*

### 2. Automated Installation
Run our comprehensive shell installer to set up all directory modules:
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Run Backend Engine
Initialize the FastAPI Python backend on port 8000:
```bash
cd backend/python
uvicorn main:app --reload --port 8000
```

### 4. Run Frontend Dashboard
Start the Next.js development server:
```bash
cd frontend
npm run dev
```
*Access the interactive dashboard at [http://localhost:3000](http://localhost:3000).*

---

## 📱 Mobile Native & Firebase Guide

Sentience Layer includes a native-ready mobile dashboard (in [mobile/](file:///c:/Users/catac\OneDrive\Desktop\sentience-layer\mobile)).

### Running Locally
```bash
cd mobile
npm install
npm run dev
```

### Capacitor Native Wrappers
Generate native Android Studio and iOS Xcode packages:
```bash
# Build the production static web export
npm run build

# Sync compiled web code with Capacitor native bridges
npx cap sync

# Open code inside native IDEs
npx cap open android
npx cap open ios
```

### Deploying to Firebase Hosting
Deploy the static dashboard globally to Firebase using our automated scripts:
```bash
# Login and select your active project
npx firebase login

# Compile, optimize, and deploy to Firebase
npm run firebase:deploy
```

---

## 🧪 Comprehensive Test Suite

Verify all framework components across backends and frontends:

```bash
# Test Python Agent logic and FastAPI routing
pytest tests/ -v --cov

# Test backend Node services
cd backend/node && npm test

# Test Next.js UI component logic
cd frontend && npm test
```

---

## 🎨 Code Demonstrations

### 1. Causal Inference
```python
# Distinguish correlations from causal treaters
result = await causal_inference_agent.analyze(
    data=sales_data,
    outcome="revenue",
    treatment="marketing_spend"
)
print(f"Outcome: {result.data['effect_strength']} (p < 0.05)")
```

### 2. Multi-Agent Debate
```python
# Generate balanced Pro vs Con deliberations
debate = await debate_agent.discuss(
    question="Should we migrate servers to the edge?",
    agents=["economic", "ethics", "uncertainty"]
)
print(f"Consensus: {debate.consensus.recommendation}")
```

### 3. Signed Swarm Handoff
```python
from backend.python.swarm_orchestrator import SwarmOrchestrator

orchestrator = SwarmOrchestrator()
result = await orchestrator.run(
    query="Why did Q1 operations experience latency spikes?",
    output_verbosity="detailed"
)
print(f"Key Finding: {result.key_finding}")
print(f"Actions: {result.actions}")
```

---

## 📁 Workspace Project Structure

```
sentience-layer/
├── backend/
│   ├── python/              # FastAPI core services
│   │   ├── agents/          # Implementations for the 18 AI agents
│   │   ├── api/             # API Router endpoints
│   │   ├── mcp_servers/     # Local Postgres MCP Server registration
│   │   ├── models/          # Database relational mapping
│   │   └── main.py          # Port 8000 Server Gateway
│   └── node/                # Node.js WebSocket helper backend
├── frontend/                # Next.js 14 Web Dashboard
├── mobile/                  # Next.js 14 Mobile App with Capacitor & Firebase
├── database/                # Relational SQL schema scripts
├── docs/                    # Complete architectural & API guides
│   ├── AGENTS.md            # Agent architectures & quadrants
│   ├── API.md               # REST & WebSocket API specification
│   ├── ARCHITECTURE.md      # Microservice dataflow guide
│   └── MOBILE.md            # Mobile build & Firebase Hosting guide
└── docker-compose.yml       # Standard container deployment blueprint
```

---

> **Built with ❤️ for the Google Antigravity Swarm Hackathon 2024**
