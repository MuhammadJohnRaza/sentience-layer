# 🚀 Sentience Layer - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Redis 7+** - [Download](https://redis.io/download/)

### Optional
- **Docker & Docker Compose** - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads/)

### API Keys (Required)
- **Google Antigravity API Key** - [Get Key](https://cloud.google.com/antigravity)
- **Google Gemini API Key** - [Get Key](https://ai.google.dev/)

## Installation Methods

### Method 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/sentience-layer.git
cd sentience-layer

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env file with your API keys
nano .env  # or use your preferred editor

# Start with Docker
docker-compose up -d
```

### Method 2: Manual Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/sentience-layer.git
cd sentience-layer
```

#### Step 2: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required:
# - GOOGLE_ANTIGRAVITY_API_KEY
# - GOOGLE_GEMINI_API_KEY
# - DATABASE_URL
# - REDIS_URL
```

#### Step 3: Python Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if available)
# alembic upgrade head
```

#### Step 4: Node.js Backend Setup
```bash
cd backend/node
npm install
cd ../..
```

#### Step 5: Frontend Setup
```bash
cd frontend
npm install
cd ..
```

#### Step 6: Database Setup

**PostgreSQL**
```bash
# Create database
createdb sentience_db

# Or using psql
psql -U postgres
CREATE DATABASE sentience_db;
CREATE USER sentience WITH PASSWORD 'sentience123';
GRANT ALL PRIVILEGES ON DATABASE sentience_db TO sentience;
\q
```

**Redis**
```bash
# Start Redis server
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis:7-alpine
```

#### Step 7: Start Services

**Terminal 1: Python Backend**
```bash
cd backend/python
uvicorn main:app --reload --port 8000
```

**Terminal 2: Node.js Backend**
```bash
cd backend/node
npm run dev
```

**Terminal 3: Frontend**
```bash
cd frontend
npm run dev
```

**Terminal 4: Celery Worker**
```bash
cd backend/python
celery -A celery_app worker --loglevel=info
```

## Verification

### Check Services

1. **Frontend**: http://localhost:3000
2. **Python API**: http://localhost:8000
3. **API Docs**: http://localhost:8000/docs
4. **Node API**: http://localhost:3001

### Test API
```bash
# Health check
curl http://localhost:8000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "components": {
#     "kernel": "online",
#     "world_model": "online",
#     "agents": 18
#   }
# }
```

### Test Frontend
1. Open http://localhost:3000
2. You should see the Sentience Layer landing page
3. Click "Enter Mission Control"
4. Dashboard should load

## Docker Setup (Alternative)

### Quick Start
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Individual Services
```bash
# Start only database services
docker-compose up -d postgres redis chromadb

# Start backend services
docker-compose up -d backend-python backend-node

# Start frontend
docker-compose up -d frontend
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Kill process
kill -9 <PID>  # On Linux/Mac
taskkill /PID <PID> /F  # On Windows
```

#### 2. Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string in .env
DATABASE_URL=postgresql://sentience:sentience123@localhost:5432/sentience_db
```

#### 3. Redis Connection Error
```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Check Redis URL in .env
REDIS_URL=redis://localhost:6379/0
```

#### 4. Python Dependencies Error
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install <package-name>
```

#### 5. Node.js Dependencies Error
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 6. API Key Issues
```bash
# Verify .env file exists
ls -la .env

# Check API keys are set
cat .env | grep GOOGLE_ANTIGRAVITY_API_KEY

# Ensure no extra spaces or quotes
GOOGLE_ANTIGRAVITY_API_KEY=your_key_here  # ✓ Correct
GOOGLE_ANTIGRAVITY_API_KEY="your_key_here"  # ✗ Wrong (remove quotes)
```

## Development Setup

### Hot Reload
All services support hot reload during development:
- Python: `--reload` flag in uvicorn
- Node.js: `nodemon` watches for changes
- Frontend: Next.js dev server auto-reloads

### Code Formatting
```bash
# Python
black backend/python
isort backend/python

# TypeScript/JavaScript
npm run format
```

### Linting
```bash
# Python
flake8 backend/python
mypy backend/python

# TypeScript/JavaScript
npm run lint
```

### Testing
```bash
# Python tests
pytest tests/ -v --cov

# Node.js tests
cd backend/node && npm test

# Frontend tests
cd frontend && npm test

# E2E tests
npm run test:e2e
```

## Production Deployment

### Environment Variables
```bash
# Set production values
APP_ENV=production
APP_DEBUG=false

# Use strong secrets
JWT_SECRET_KEY=<generate-strong-random-key>
ENCRYPTION_KEY=<generate-32-byte-key>

# Use production database
DATABASE_URL=postgresql://user:pass@prod-db:5432/sentience_db

# Enable HTTPS
CORS_ORIGINS=https://yourdomain.com
```

### Build for Production
```bash
# Python: No build needed, but install production dependencies
pip install -r requirements.txt --no-dev

# Node.js backend
cd backend/node
npm run build

# Frontend
cd frontend
npm run build
npm start
```

### Docker Production
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or build custom images
docker build -t sentience-backend:latest ./backend/python
docker build -t sentience-frontend:latest ./frontend
```

## Next Steps

1. **Configure Agents**: Edit `backend/python/agents/agent_definitions.py`
2. **Add Data Sources**: Configure data ingestion in `backend/python/ingestion.py`
3. **Customize UI**: Modify frontend components in `frontend/src/components/`
4. **Set Up Monitoring**: Configure Prometheus and logging
5. **Read Documentation**: Check `docs/` folder for detailed guides

## Support

- **Documentation**: [docs/](../docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sentience-layer/issues)
- **Email**: support@sentiencelayer.ai

---

**Setup complete! 🎉 Start building with Sentience Layer!**
