# Sentience Layer - Autonomous Content-to-Action Agent

**Google AI Sekho Hackathon Submission**  
**Challenge 1: Autonomous Content-to-Action Agent (Insight → Action System)**

---

## 🏆 Competition Overview

This project demonstrates a complete **Agentic AI System** that transforms unstructured content into actionable outcomes using **Google Antigravity** as the core orchestration platform.

### System Flow
```
📄 Content Input → 🧠 Understanding → 💡 Insights → 🎯 Actions → 🎲 Simulation → ✅ Execution
```

---

## ✨ Key Features

### 1. **Multi-Modal Content Understanding** (25% - Antigravity Integration)
- **Text, PDF, Images, Audio** processing
- Google Antigravity NLP for semantic understanding
- Entity extraction and topic modeling
- Sentiment and urgency analysis
- **Antigravity APIs Used:**
  - `/embeddings` - Multi-modal embeddings
  - `/nlp/expand` - Query expansion
  - `/vision/ocr` - Image text extraction
  - `/audio/transcribe` - Speech-to-text

### 2. **Agentic Reasoning & Workflow** (20%)
- **ReAct Pattern** implementation (Reason → Act → Observe)
- Multi-step reasoning chain with 4+ steps
- 18 specialized agents orchestrated via Antigravity
- Autonomous decision-making with confidence scoring
- **Agent Types:**
  - Causal Inference Agent
  - Premonition Agent
  - Economic Agent
  - Ethics Agent
  - Uncertainty Agent
  - Adversarial Test Agent
  - And 12 more...

### 3. **Insight Extraction** (20%)
- **Pattern Detection** - Identifies recurring patterns
- **Anomaly Detection** - Flags unusual behavior
- **Causal Inference** - Discovers cause-effect relationships
- **Prediction** - Forecasts future outcomes
- **Risk Analysis** - Evaluates potential risks
- Cross-referenced with Antigravity knowledge graph

### 4. **Action Simulation** (15%)
- **Monte Carlo Simulation** with 100+ runs
- Before/After state visualization
- Step-by-step outcome analysis
- **Downstream Effects** (3-hop propagation)
- Success probability calculation
- Best/Worst case scenario generation
- Rollback state capture

### 5. **Technical Implementation** (10%)
- Clean architecture with separation of concerns
- FastAPI backend + React Native mobile app
- WebSocket for real-time updates
- Offline-first with sync capabilities
- Error handling and retry logic
- Comprehensive logging

### 6. **Innovation & UX** (10%)
- **LLM-Powered Routing** - Intelligent navigation
- **Swarm Orchestration** - Dynamic agent selection
- **Cognitive OS** - Self-aware system architecture
- **Immersive UI** - Cyberpunk-inspired design
- **Real-time Telemetry** - Live agent monitoring

---

## 🎯 Example Use Cases

### Business Scenario
**Input:**
```
Sales report shows 25% decline in Lahore region this quarter.
Customer complaints increased by 40%.
```

**Output:**
- **Insight:** Revenue decline pattern detected (confidence: 92%)
- **Impact:** Projected revenue loss of $250K
- **Recommended Action:** Launch regional discount campaign
- **Simulation:** 87% success rate, expected ROI: 2.3x
- **Execution:** Campaign created, 5,000 users targeted

### Policy/News Scenario
**Input:**
```
Breaking: Fuel prices increased by 15% effective immediately.
```

**Output:**
- **Insight:** Cost increase will affect delivery operations
- **Impact:** 12% increase in operational costs
- **Recommended Action:** Update delivery pricing model
- **Simulation:** 91% success rate, customer retention: 94%
- **Execution:** Pricing updated, notifications sent

---

## 🏗️ Architecture

### Backend (Python FastAPI)
```
backend/python/
├── api/
│   ├── main.py                    # Main API orchestrator
│   └── routes/                    # API endpoints
├── services/
│   ├── content_understanding.py   # Multi-modal parsing
│   ├── insight_extraction.py      # Pattern & anomaly detection
│   ├── action_generation.py       # Action recommendation
│   ├── action_simulation.py       # Monte Carlo simulation
│   └── antigravity_orchestrator.py # Antigravity integration
├── agents/
│   ├── causal_inference_agent.py
│   ├── premonition_agent.py
│   └── [16 more agents]
└── antigravity_client.py          # Antigravity API client
```

### Mobile App (React Native + Expo)
```
mobile/
├── src/
│   ├── screens/
│   │   ├── ContentInputScreen.js  # Multi-modal input
│   │   ├── ResultsScreen.js       # Analysis results
│   │   └── SimulationScreen.js    # Simulation visualization
│   ├── services/
│   │   ├── api.js                 # Backend API client
│   │   └── routing.js             # LLM-powered routing
│   └── components/
│       ├── ChatBubble.js
│       ├── ActionCard.js
│       └── [20+ components]
└── App.js                          # Main app entry
```

---

## 🚀 Setup & Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- Expo CLI
- Google Antigravity API Key (or OpenRouter API Key as fallback)

### Backend Setup
```bash
cd backend/python
pip install -r requirements.txt

# Set environment variables
export ANTIGRAVITY_API_KEY="your_key_here"
export OPENROUTER_API_KEY="your_fallback_key"

# Run server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Mobile App Setup
```bash
cd mobile
npm install

# Run on Android
npm run android

# Run on iOS
npm run ios

# Run on Web
npm run web
```

---

## 📱 Demo Flow

### Step 1: Content Input
- Open app → Navigate to "Content Input"
- Choose input method:
  - **Text:** Paste report/article
  - **Document:** Upload PDF
  - **Image:** Capture/select photo
  - **Example:** Use pre-loaded scenarios

### Step 2: Analysis
- System processes content through Antigravity
- Real-time progress updates via WebSocket
- Multi-agent reasoning chain displayed

### Step 3: Results
- **Understanding:** Intent, urgency, topics
- **Insights:** Patterns, anomalies, predictions
- **Reasoning Chain:** 4-step ReAct process
- **Actions:** Top 3 recommended actions

### Step 4: Simulation
- Select action to simulate
- Monte Carlo runs (100 iterations)
- View success probability, expected value
- Before/After state comparison
- Downstream effects (3 hops)

### Step 5: Execution
- Review simulation results
- Confirm execution
- System executes action
- Results logged to vault

---

## 🎥 Demo Video Script

**[0:00-0:30] Introduction**
- "Welcome to Sentience Layer - an autonomous content-to-action agent"
- "Built with Google Antigravity for the AI Sekho Hackathon"

**[0:30-1:00] Content Input**
- Show text input with business scenario
- Demonstrate document upload
- Show camera capture for image input

**[1:00-2:00] Analysis Pipeline**
- Real-time processing visualization
- Agent swarm orchestration
- Reasoning chain display

**[2:00-3:00] Insights & Actions**
- Show extracted insights with confidence scores
- Display recommended actions
- Explain impact analysis

**[3:00-4:00] Simulation**
- Run Monte Carlo simulation
- Show before/after state
- Display downstream effects
- Explain success probability

**[4:00-4:30] Execution**
- Confirm action execution
- Show execution logs
- Display final outcome

**[4:30-5:00] Closing**
- Recap key features
- Highlight Antigravity integration
- Thank you message

---

## 📊 Evaluation Criteria Coverage

| Criterion | Score | Evidence |
|-----------|-------|----------|
| **Antigravity Use** | 25% | Central to all operations - NLP, embeddings, causal discovery, knowledge graph |
| **Agentic Reasoning** | 20% | ReAct pattern, 18 agents, multi-step reasoning, autonomous decisions |
| **Insight Quality** | 20% | Meaningful patterns, causal links, predictions, cross-validated |
| **Action Simulation** | 15% | Monte Carlo (100 runs), state diff, downstream effects, rollback |
| **Technical** | 10% | Clean architecture, error handling, WebSocket, offline-first |
| **Innovation** | 10% | LLM routing, swarm orchestration, cognitive OS, immersive UX |

---

## 🔧 Technical Highlights

### Antigravity Integration Points
1. **Content Understanding** - Multi-modal embeddings
2. **Entity Extraction** - NLP entity recognition
3. **Causal Discovery** - Causal graph generation
4. **Predictive Analytics** - Time series forecasting
5. **Knowledge Graph** - Entity validation
6. **Vector Search** - Semantic similarity
7. **Anomaly Detection** - Unsupervised learning
8. **Reasoning APIs** - ReAct pattern execution

### Innovation Features
- **LLM-Powered Routing:** Intelligent screen navigation based on user intent
- **Swarm Orchestration:** Dynamic agent selection and parallel execution
- **Cognitive Memory:** Persistent belief store with learning
- **Dream Mode:** Offline causal exploration
- **Doubt Theater:** Multi-agent debate visualization

---

## 📝 Documentation

- **Architecture:** `docs/ARCHITECTURE.md`
- **Agents:** `docs/AGENTS.md`
- **API:** `docs/API.md`
- **Setup:** `docs/SETUP.md`
- **Demo Script:** `docs/DEMO_SCRIPT.md`

---

## 🎯 Competition Requirements Checklist

- ✅ **Working Prototype:** Mobile app + Backend API
- ✅ **Demo Video:** 3-5 minutes showing full pipeline
- ✅ **Agent Trace:** Antigravity workplan, tasks, reasoning steps
- ✅ **Documentation:** README with architecture, tools, assumptions
- ✅ **Antigravity Central:** Used in core orchestration, not superficial
- ✅ **Agentic Workflow:** Multi-step reasoning with clear flow
- ✅ **Insight Quality:** Meaningful, non-trivial insights
- ✅ **Action Simulation:** Realistic Monte Carlo simulation
- ✅ **Outcome Visualization:** Before/after state, execution logs

---

## 🏅 Why This Project Wins

1. **Genuine Antigravity Integration:** Not a wrapper - deeply integrated across 8+ API endpoints
2. **Complete Pipeline:** End-to-end from content → insight → action → simulation → execution
3. **Production-Ready:** Clean architecture, error handling, offline support
4. **Innovation:** LLM routing, swarm orchestration, cognitive OS
5. **User Experience:** Immersive UI, real-time updates, intuitive flow
6. **Scalability:** Modular design, 18 specialized agents, extensible
7. **Documentation:** Comprehensive docs, clear architecture, reproducible

---

## 👥 Team

**Solo Developer:** kasa-maker  
**GitHub:** https://github.com/kasa-maker/sentience-layer

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Google AI Sekho Team for organizing the hackathon
- Antigravity team for the powerful platform
- Open source community for amazing tools

---

**Built with ❤️ for Google AI Sekho Hackathon 2026**
