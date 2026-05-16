# Contributing to Sentience Layer

Thank you for your interest in contributing to Sentience Layer! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide system information (OS, Python version, etc.)
- Include error messages and logs

### 2. Suggest Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain why it would be valuable

### 3. Submit Code
- Fork the repository
- Create a feature branch
- Write clean, documented code
- Add tests for new functionality
- Submit a pull request

### 4. Improve Documentation
- Fix typos and clarify explanations
- Add examples and tutorials
- Improve API documentation

## 🔧 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker (optional)

### Setup Steps

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/sentience-layer.git
cd sentience-layer
```

2. **Run setup script**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Start development servers**
```bash
# Terminal 1: Python backend
cd backend/python
uvicorn main:app --reload

# Terminal 2: Node backend
cd backend/node
npm run dev

# Terminal 3: Frontend
cd frontend
npm run dev
```

## 📝 Code Style

### Python
- Follow PEP 8
- Use Black for formatting: `black backend/python`
- Use type hints
- Maximum line length: 100 characters

```python
# Good
async def process_query(query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
    """
    Process a user query through the agent system.
    
    Args:
        query: The user's question
        context: Optional context dictionary
        
    Returns:
        AgentResult with findings and confidence
    """
    pass

# Bad
def process(q, c=None):
    pass
```

### TypeScript/JavaScript
- Follow Airbnb style guide
- Use Prettier for formatting
- Use TypeScript for type safety
- Prefer functional components in React

```typescript
// Good
interface InsightProps {
  query: string;
  onResult: (result: InsightResult) => void;
}

export const InsightPanel: React.FC<InsightProps> = ({ query, onResult }) => {
  // Component logic
};

// Bad
export default function InsightPanel(props) {
  // Component logic
}
```

## 🧪 Testing

### Python Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend/python --cov-report=html

# Run specific test
pytest tests/test_agents.py::test_causal_inference -v
```

### JavaScript Tests
```bash
# Backend tests
cd backend/node
npm test

# Frontend tests
cd frontend
npm test
```

### Writing Tests

**Python Example**
```python
import pytest
from backend.python.agents.causal_inference_agent import CausalInferenceAgent

@pytest.mark.asyncio
async def test_causal_inference():
    agent = CausalInferenceAgent()
    await agent.initialize()
    
    data = [
        {"marketing": 100, "revenue": 1000},
        {"marketing": 150, "revenue": 1200},
    ]
    
    result = await agent._infer_causality(data, ["marketing", "revenue"])
    
    assert result.success
    assert len(result.data["hypotheses_generated"]) > 0
```

## 📋 Pull Request Process

### Before Submitting

1. **Update your branch**
```bash
git checkout main
git pull upstream main
git checkout your-feature-branch
git rebase main
```

2. **Run tests**
```bash
pytest tests/ -v
npm test
```

3. **Format code**
```bash
black backend/python
npm run format
```

4. **Update documentation**
- Add docstrings to new functions
- Update README if needed
- Add examples for new features

### PR Guidelines

**Title Format**
```
[Type] Brief description

Examples:
[Feature] Add economic impact agent
[Fix] Resolve causal inference edge case
[Docs] Update API documentation
[Refactor] Simplify consensus algorithm
```

**Description Template**
```markdown
## What does this PR do?
Brief description of changes

## Why is this needed?
Explain the motivation

## How was it tested?
Describe testing approach

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted
- [ ] No breaking changes (or documented)
```

### Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer approval required
3. Address review comments
4. Squash commits before merge (if requested)

## 🏗️ Architecture Guidelines

### Adding a New Agent

1. **Create agent file**
```python
# backend/python/agents/your_agent.py
from .base_agent import BaseAgent, AgentMessage, AgentResult

class YourAgent(BaseAgent):
    def __init__(self, agent_id: str = "your_agent", config: Optional[Dict] = None):
        super().__init__(agent_id, config)
        
    async def initialize(self):
        self.register_skill("your_skill", self.your_skill)
        
    async def process(self, message: AgentMessage) -> AgentResult:
        return await self.your_skill(message)
        
    async def your_skill(self, message: AgentMessage) -> AgentResult:
        # Implementation
        return AgentResult(success=True, data={})
```

2. **Register in agent_definitions.py**
```python
AGENT_REGISTRY = [
    # ... existing agents
    "your_agent"
]
```

3. **Add tests**
```python
# tests/test_your_agent.py
import pytest
from backend.python.agents.your_agent import YourAgent

@pytest.mark.asyncio
async def test_your_agent():
    agent = YourAgent()
    await agent.initialize()
    # Test logic
```

4. **Update documentation**
- Add to docs/AGENTS.md
- Describe capabilities and use cases

## 🐛 Debugging Tips

### Python Backend
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()

# Logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend
```typescript
// React DevTools
// Chrome extension for debugging React components

// Console logging
console.log('Debug:', { query, result });

// Debugger
debugger;
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Google Antigravity Docs](https://cloud.google.com/antigravity)
- [Project Architecture](docs/ARCHITECTURE.md)
- [Agent System](docs/AGENTS.md)

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: support@sentiencelayer.ai

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Sentience Layer! 🚀
