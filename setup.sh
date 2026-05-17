#!/bin/bash

# Sentience Layer v4.0 - Setup Script
# Google Antigravity Hackathon Entry

set -e  # Exit on error

echo "🧠 Sentience Layer Setup Script"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Windows (Git Bash/WSL)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo -e "${YELLOW}⚠️  Detected Windows environment${NC}"
    IS_WINDOWS=true
else
    IS_WINDOWS=false
fi

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION installed"
else
    print_error "Python 3.11+ is required but not installed"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION installed"
else
    print_error "Node.js 18+ is required but not installed"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    print_success "Docker $DOCKER_VERSION installed"
    HAS_DOCKER=true
else
    print_info "Docker not found - will skip containerized setup"
    HAS_DOCKER=false
fi

echo ""
echo "🔧 Setting up environment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_info "Creating .env file from .env.example"
    cp .env.example .env
    print_success ".env file created"
    print_info "⚠️  Please edit .env and add your API keys!"
else
    print_info ".env file already exists"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data/faiss_index
mkdir -p ml-models
mkdir -p database/backups
print_success "Directories created"

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
if [ -f requirements.txt ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found"
fi

# Install Node.js dependencies for backend
echo ""
echo "📦 Installing Node.js backend dependencies..."
if [ -d backend/node ]; then
    cd backend/node
    npm install
    cd ../..
    print_success "Node.js backend dependencies installed"
fi

# Install Node.js dependencies for frontend
echo ""
echo "🎨 Installing frontend dependencies..."
if [ -d frontend ]; then
    cd frontend
    npm install
    cd ..
    print_success "Frontend dependencies installed"
fi

# Setup database (if Docker is available)
if [ "$HAS_DOCKER" = true ]; then
    echo ""
    echo "🐳 Setting up Docker containers..."
    print_info "Starting PostgreSQL, Redis, and ChromaDB..."

    docker-compose up -d postgres redis chromadb

    # Wait for PostgreSQL to be ready
    print_info "Waiting for PostgreSQL to be ready..."
    sleep 5

    print_success "Database containers started"

    # Run database migrations
    echo ""
    echo "🗄️  Running database migrations..."
    # Uncomment when migrations are ready
    # python3 -m alembic upgrade head
    print_info "Database migrations skipped (not implemented yet)"
fi

# Generate agent definitions
echo ""
echo "🤖 Generating agent definitions..."
if [ -f generate_agents.py ]; then
    python3 generate_agents.py
    print_success "Agent definitions generated"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
if [ -d tests ]; then
    python3 -m pytest tests/ -v --tb=short || print_info "Some tests failed (this is okay for initial setup)"
else
    print_info "No tests directory found"
fi

# Final instructions
echo ""
echo "================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "================================"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit .env file and add your API keys:"
echo "   - GOOGLE_ANTIGRAVITY_API_KEY"
echo "   - GOOGLE_GEMINI_API_KEY"
echo ""
echo "2. Start the services:"
if [ "$HAS_DOCKER" = true ]; then
    echo "   Docker: docker-compose up"
    echo "   OR"
fi
echo "   Manual:"
echo "   - Terminal 1: cd backend/python && uvicorn main:app --reload"
echo "   - Terminal 2: cd backend/node && npm run dev"
echo "   - Terminal 3: cd frontend && npm run dev"
echo "   - Terminal 4: celery -A celery_app worker --loglevel=info"
echo ""
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Python API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Node API: http://localhost:3001"
echo ""
echo "4. For development:"
echo "   - Run tests: pytest tests/ -v"
echo "   - Format code: black backend/python"
echo "   - Lint: flake8 backend/python"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
