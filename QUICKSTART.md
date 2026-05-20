# Quick Start Guide - Sentience Layer

Get the competition-winning content-to-action agent running in 10 minutes!

---

## 🚀 Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://www.python.org/))
- **Expo CLI** (`npm install -g expo-cli`)
- **Git** ([Download](https://git-scm.com/))
- **API Key** (Google Antigravity or OpenRouter)

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/kasa-maker/sentience-layer.git
cd sentience-layer
```

### 2. Backend Setup (Python FastAPI)

```bash
# Navigate to backend
cd backend/python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic aiohttp python-dotenv

# Create .env file
echo "ANTIGRAVITY_API_KEY=your_key_here" > .env
echo "OPENROUTER_API_KEY=your_fallback_key" >> .env

# Run server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend should now be running at:** `http://localhost:8000`

### 3. Mobile App Setup (React Native + Expo)

Open a **new terminal** window:

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Start Expo development server
npm start
```

### 4. Run the App

Choose your platform:

**Android:**
```bash
npm run android
```

**iOS:**
```bash
npm run ios
```

**Web:**
```bash
npm run web
```

---

## ✅ Verify Installation

### Test Backend

Open browser and visit:
- Health Check: `http://localhost:8000/api/health`
- System Info: `http://localhost:8000/api/info`

You should see JSON responses indicating the system is healthy.

### Test Mobile App

1. App should load with home screen
2. Tap "CONTENT → ACTION" button
3. Enter sample text: "Sales declined by 25%"
4. Tap "ANALYZE TEXT"
5. Should see processing animation

---

## 🎯 Quick Demo Flow

### Scenario 1: Business Report Analysis

1. **Open App** → Tap "CONTENT → ACTION"
2. **Select Example** → "Business Report Analysis"
3. **Analyze** → Tap "ANALYZE TEXT"
4. **View Results** → See insights, reasoning chain, actions
5. **Simulate** → Tap "SIMULATE" on top action
6. **Execute** → Review simulation, tap "EXECUTE ACTION"

### Scenario 2: News Impact Analysis

1. **Open App** → Tap "CONTENT → ACTION"
2. **Select Example** → "News Article Impact"
3. **Analyze** → Tap "ANALYZE TEXT"
4. **View Results** → See policy impact analysis
5. **Simulate** → Run Monte Carlo simulation
6. **Execute** → Confirm action execution

---

## 🔧 Configuration

### API Keys

Edit `backend/python/.env`:

```env
# Google Antigravity (primary)
ANTIGRAVITY_API_KEY=your_antigravity_key

# OpenRouter (fallback)
OPENROUTER_API_KEY=your_openrouter_key

# Optional
DEBUG=True
LOG_LEVEL=INFO
```

### Mobile App API Endpoint

Edit `mobile/src/services/api.js`:

```javascript
const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'  // Development
  : 'https://your-production-url.com/api/v1';  // Production
```

---

## 📱 Features to Test

### ✅ Content Understanding
- Text input
- Document upload (PDF)
- Image capture
- Example scenarios

### ✅ Insight Extraction
- Pattern detection
- Anomaly detection
- Causal inference
- Predictions

### ✅ Action Generation
- Recommended actions
- Confidence scores
- Step-by-step plans

### ✅ Simulation
- Monte Carlo (100 runs)
- Success probability
- Before/After state
- Downstream effects

### ✅ Execution
- Action confirmation
- Execution logs
- Result tracking

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in command
python -m uvicorn api.main:app --reload --port 8001
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**API key errors:**
- Check `.env` file exists
- Verify key format
- Try fallback OpenRouter key

### Mobile App Issues

**Metro bundler errors:**
```bash
# Clear cache
expo start -c
```

**Dependencies not found:**
```bash
# Reinstall
rm -rf node_modules
npm install
```

**Can't connect to backend:**
- Check backend is running
- Verify API_BASE_URL in `api.js`
- Try `http://10.0.2.2:8000` for Android emulator

---

## 📚 Next Steps

### Explore Features
- Try different input types
- Test all example scenarios
- Review agent traces
- Check simulation results

### Customize
- Add your own agents
- Modify action templates
- Adjust simulation parameters
- Customize UI theme

### Deploy
- Deploy backend to cloud (Render, Railway, etc.)
- Build mobile app for production
- Configure production API keys
- Set up monitoring

---

## 🎥 Record Demo Video

### Preparation
1. Clear all test data
2. Restart backend and app
3. Test full flow once
4. Prepare screen recording tool

### Recording
1. Start with home screen
2. Show content input
3. Demonstrate analysis
4. Display simulation
5. Execute action
6. Show results

### Export
- Format: MP4
- Resolution: 1080p
- Duration: 3-5 minutes
- Upload to YouTube/Drive

---

## 📞 Support

**Issues?** Check:
- Backend logs: Terminal running uvicorn
- Mobile logs: Expo console
- Browser console: For web version

**Documentation:**
- Architecture: `docs/ARCHITECTURE.md`
- API Reference: `docs/API.md`
- Agent Details: `docs/AGENTS.md`

---

## 🏆 Competition Submission

### Required Files
- ✅ Working prototype (backend + mobile)
- ✅ Demo video (3-5 minutes)
- ✅ README with documentation
- ✅ Agent trace logs
- ✅ Source code

### Submission Checklist
- [ ] Code pushed to GitHub
- [ ] Demo video uploaded
- [ ] README completed
- [ ] All features working
- [ ] Documentation clear

---

**You're ready to win! 🚀**

For questions or issues, open an issue on GitHub or contact the team.
