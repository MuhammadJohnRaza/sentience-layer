# 🔐 Security Policy

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability in Sentience Layer, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email: **security@sentiencelayer.ai** (or your contact email)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Features

### 1. Authentication & Authorization

**JWT-based Authentication**
```python
# All API endpoints require valid JWT tokens
@app.get("/api/insights")
async def get_insights(token: str = Depends(verify_token)):
    # Token verified before processing
    pass
```

**Role-Based Access Control (RBAC)**
- Admin: Full access to all features
- Analyst: Read/write insights, simulations
- Viewer: Read-only access
- API: Programmatic access with scoped permissions

### 2. Data Encryption

**At Rest**
- Database: AES-256 encryption for sensitive fields
- Files: Encrypted storage for uploaded data
- Secrets: Stored in environment variables, never in code

**In Transit**
- TLS 1.3 for all API communications
- WebSocket connections use WSS (secure)
- Internal service communication encrypted

### 3. Input Validation

**Pydantic Schemas**
```python
class InsightRequest(BaseModel):
    query: str = Field(..., max_length=1000)
    context: Optional[Dict] = Field(default={})
    
    @validator('query')
    def validate_query(cls, v):
        # Prevent SQL injection, XSS
        if any(char in v for char in ['<', '>', ';', '--']):
            raise ValueError("Invalid characters in query")
        return v
```

**SQL Injection Prevention**
- All database queries use parameterized statements
- ORM (SQLAlchemy) for safe query construction
- No raw SQL execution from user input

**XSS Prevention**
- All user input sanitized before rendering
- Content Security Policy headers
- React's built-in XSS protection

### 4. Rate Limiting

```python
# Prevent abuse and DoS attacks
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    
    # 100 requests per minute per IP
    if await rate_limiter.is_exceeded(client_ip, limit=100, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return await call_next(request)
```

### 5. API Key Security

**Google Antigravity API Keys**
- Stored in environment variables only
- Never logged or exposed in responses
- Rotated regularly (recommended: every 90 days)
- Scoped to minimum required permissions

**Best Practices**
```bash
# ✅ Good: Environment variable
export GOOGLE_ANTIGRAVITY_API_KEY="your_key"

# ❌ Bad: Hardcoded in code
api_key = "AIzaSyC..."  # NEVER DO THIS
```

### 6. Audit Logging

All sensitive operations are logged:
```python
@dataclass
class AuditLog:
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    ip_address: str
    success: bool
    details: Dict

# Example
audit_log.record(
    user_id="user_123",
    action="simulate_action",
    resource="marketing_budget",
    ip_address=request.client.host,
    success=True
)
```

### 7. Secure Configuration

**Environment Variables**
- All secrets in `.env` file (never committed)
- Different configs for dev/staging/prod
- Secrets rotation policy

**CORS Configuration**
```python
# Restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Security Checklist

### For Developers

- [ ] Never commit `.env` files
- [ ] Use parameterized queries for database
- [ ] Validate all user input
- [ ] Sanitize output before rendering
- [ ] Use HTTPS in production
- [ ] Rotate API keys regularly
- [ ] Keep dependencies updated
- [ ] Run security scans (`npm audit`, `safety check`)
- [ ] Review code for security issues
- [ ] Test authentication/authorization

### For Deployment

- [ ] Enable TLS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Restrict database access
- [ ] Use secrets management (AWS Secrets Manager, etc.)
- [ ] Set up monitoring and alerts
- [ ] Regular security updates
- [ ] Backup encryption keys
- [ ] Implement DDoS protection

## Known Security Considerations

### 1. AI Model Security

**Prompt Injection**
- User queries are sanitized before sending to AI models
- System prompts are protected from user manipulation
- Output validation to prevent malicious responses

**Data Privacy**
- User data is not used to train models
- Sensitive data masked before processing
- Compliance with GDPR, CCPA

### 2. Third-Party Dependencies

We regularly scan dependencies for vulnerabilities:
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
npm audit fix
```

### 3. Database Security

**PostgreSQL**
- Strong passwords (min 16 characters)
- Network isolation (not exposed to internet)
- Regular backups (encrypted)
- Principle of least privilege for DB users

**Redis**
- Password protected
- Bind to localhost only
- Disable dangerous commands (FLUSHALL, CONFIG)

## Compliance

### GDPR Compliance
- User data deletion on request
- Data export functionality
- Consent management
- Privacy by design

### SOC 2 (Planned)
- Access controls
- Encryption standards
- Audit logging
- Incident response

## Security Updates

We follow semantic versioning for security patches:
- **Critical**: Immediate patch release
- **High**: Patch within 7 days
- **Medium**: Patch in next minor release
- **Low**: Patch in next major release

## Contact

For security concerns: **security@sentiencelayer.ai**

For general questions: **support@sentiencelayer.ai**

---

**Last Updated**: 2024-11-15  
**Version**: 4.0
