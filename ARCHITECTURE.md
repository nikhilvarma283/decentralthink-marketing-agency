# Architecture Documentation

## System Overview

DecentralThink is a two-track platform serving dental practices and high school students with a shared technical foundation.

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Client Layer                              │
│  ┌──────────────────┐          ┌──────────────────────────┐ │
│  │  Dental UI       │          │  HS SaaS UI              │ │
│  │  (React)         │          │  (React)                 │ │
│  └──────────────────┘          └──────────────────────────┘ │
└────────────────┬──────────────────────────────────────────────┘
                 │ HTTPS (REST API)
┌────────────────▼──────────────────────────────────────────────┐
│                   API Gateway Layer                           │
│              (FastAPI + CORS + Auth)                          │
├────────────────────────────────────────────────────────────────┤
│                  API Routes (/api/v1/*)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  /auth   │  │  /chat   │  │ /strategy│  │  /execution  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
├────────────────────────────────────────────────────────────────┤
│              Business Logic Layer (Services)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ AuthService  │  │ ChatService  │  │ StrategyService      │ │
│  └──────────────┘  └──────────────┘  │ AgentService         │ │
│  ┌──────────────┐  ┌──────────────┐  │ ExecutionService     │ │
│  │ EmailService │  │ LLMService   │  └──────────────────────┘ │
│  └──────────────┘  └──────────────┘                            │
├────────────────────────────────────────────────────────────────┤
│                  Data Access Layer (ORM)                      │
│             (SQLAlchemy Models)                               │
├────────────────────────────────────────────────────────────────┤
│              Persistence Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ PostgreSQL   │  │ Redis Cache  │  │ File Storage (S3)    │ │
│  │ (Primary DB) │  │ (Sessions)   │  │ (Uploads)            │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼──────┐
│ Claude API   │ │ Stripe    │ │ SendGrid   │
│ (LLM)        │ │ (Payments)│ │ (Email)    │
└──────────────┘ └───────────┘ └────────────┘
        │              │              │
┌───────▼────────────────────────────▼──────────┐
│        External Services & Integrations       │
│  Twitter API │ LinkedIn API │ etc.            │
└────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Components

```
App
├── Router (React Router v6)
│   ├── Public Routes
│   │   ├── HomePage
│   │   ├── LoginPage
│   │   └── SignUpPage
│   └── Protected Routes
│       ├── DentalDashboard
│       │   ├── StrategyView
│       │   ├── AgentsList
│       │   ├── ExecutionPanel
│       │   └── AnalyticsDashboard
│       ├── StudentDashboard
│       │   ├── DiscoveryChat
│       │   ├── CollegeRecommendations
│       │   ├── PremiumContent
│       │   └── ActivityTracker
│       └── AdminDashboard
│           └── AnalyticsSummary
├── Header/Navigation
├── Context Providers
│   └── AuthContext
└── Global State (Zustand)
    ├── authStore
    ├── chatStore
    └── dashboardStore
```

### Backend Components

```
FastAPI App
├── Middleware
│   ├── CORS Middleware
│   ├── Authentication (JWT)
│   ├── Error Handling
│   └── Request Logging
├── Routes
│   ├── auth.py (signup, login, logout)
│   ├── users.py (profile, preferences)
│   ├── chat.py (messages, uploads)
│   ├── strategy.py (generate, view, edit)
│   ├── agents.py (list, create, configure)
│   ├── execution.py (pending tasks, approve, log)
│   ├── colleges.py (database, search, recommendations)
│   ├── stripe.py (payments, subscriptions)
│   └── analytics.py (metrics, summaries)
├── Services
│   ├── auth_service.py (password hashing, JWT)
│   ├── chat_service.py (message persistence, files)
│   ├── llm_service.py (Claude API integration)
│   ├── strategy_service.py (synthesis, storage)
│   ├── agent_service.py (agent management)
│   ├── execution_service.py (task management)
│   ├── email_service.py (SendGrid integration)
│   ├── stripe_service.py (payment processing)
│   └── college_service.py (college matching)
├── Models (ORM)
│   ├── User
│   ├── Practice (Dental)
│   ├── Student (HS)
│   ├── ChatMessage
│   ├── Plan
│   ├── Agent
│   ├── Execution
│   ├── College
│   ├── StudentRecommendation
│   └── UserPreferences
├── Schemas (Validation)
│   └── Pydantic request/response schemas
└── Database
    ├── SQLAlchemy ORM
    └── PostgreSQL
```

## Data Flow

### Dental Discovery & Strategy Flow

```
1. Practice Owner Signs Up
   └─> POST /auth/signup
       └─> User created in DB
           └─> Stripe customer created
               └─> Redirect to onboarding

2. Dental Onboarding
   └─> POST /onboarding/dental
       └─> Practice record created
           └─> Redirect to discovery chat

3. Multi-Session Discovery
   └─> POST /discovery/session/{n}
       └─> Save conversation
           └─> Extract context
               └─> AI provides follow-up questions

4. Strategy Synthesis
   └─> POST /strategy/generate
       └─> Call Claude API
           └─> Parse 90-day plan
               └─> Store in DB
                   └─> Display for review

5. Strategy Approval
   └─> POST /strategy/{id}/approve
       └─> Create agents from action items
           └─> Set status to "active"
               └─> Trigger onboarding email

6. Agent Execution
   └─> GET /execution/pending
       └─> Manager reviews
           └─> POST /execution/{id}/approve
               └─> Generate content
                   └─> Call external APIs (Twitter, SendGrid, etc.)
                       └─> Log result
```

### High School College Matching Flow

```
1. Student Signs Up
   └─> POST /auth/signup (role=high_schooler)
       └─> Student profile created
           └─> Redirect to discovery

2. Discovery Chat
   └─> POST /discovery/highschool
       └─> Conversational chat
           └─> Extract interests, goals, academics
               └─> Store in student profile

3. College Matching
   └─> POST /recommendations/{student_id}
       └─> Query college database
           └─> Apply matching algorithm
               └─> Score by relevance
                   └─> Categorize (reach/target/safety)
                       └─> Return top 30

4. Results Display
   └─> Free users: See 5 colleges (basic)
       Premium users: See all 30 (detailed)

5. Premium Upgrade
   └─> POST /stripe/subscription-hs
       └─> Process payment
           └─> Stripe webhook updates subscription
               └─> Unlock premium content
```

## Database Design

### Entity Relationship Diagram (Simplified)

```
Users (1) ─── (many) Practices
   ├─ email
   ├─ password_hash
   ├─ role
   └─ stripe_customer_id

Users (1) ─── (many) Students
   ├─ grade
   ├─ interests
   └─ goal

Users (1) ─── (many) ChatMessages
   ├─ session_id
   ├─ sender
   └─ content

Users (1) ─── (many) Plans

Practices (1) ─── (many) Agents
   ├─ name
   ├─ description
   ├─ cadence
   └─ prompt

Agents (1) ─── (many) Executions
   ├─ action_type
   ├─ content
   ├─ status
   └─ result

Students (1) ─── (many) StudentRecommendations

Colleges (1) ─── (many) StudentRecommendations
   ├─ name
   ├─ location
   ├─ programs
   └─ acceptance_rate

Users (1) ─── (1) UserPreferences
   ├─ email_frequency
   ├─ notifications_enabled
   └─ analytics_opted_in
```

## Authentication & Authorization

### JWT Flow

```
1. User signs up/logs in
   └─> Credentials validated
       └─> JWT token generated (exp: 30 days)
           └─> Stored in httpOnly cookie

2. Subsequent requests
   └─> Token included in Authorization header
       └─> Middleware validates token
           └─> Extract user_id, role
               └─> Inject into request context

3. Protected endpoints
   └─> Check auth token
       └─> Check user role (dentist/admin/etc.)
           └─> Grant access to resource
```

### Role-Based Access Control (RBAC)

```
Admin
├─ View all users
├─ Access analytics dashboard
└─ Manage platform settings

Dentist
├─ View own practice
├─ Manage own agents
├─ Execute own tasks
└─ View own analytics

HighSchooler
├─ View own student profile
├─ Access discovery
├─ View recommendations
└─ Manage preferences
```

## External Integration Points

### Third-Party APIs

| Service | Purpose | Direction | Frequency |
|---------|---------|-----------|-----------|
| **Claude API** | LLM for chat, synthesis | Outbound | On-demand |
| **Stripe** | Payment processing | Outbound | On signup, renewal |
| **SendGrid** | Email delivery | Outbound | Scheduled (weekly) |
| **Twitter API** | Social posting | Outbound | On execution approval |
| **LinkedIn API** | Social posting | Outbound | On execution approval |

### Error Handling & Retries

- Claude API timeouts → Retry up to 3x with exponential backoff
- Stripe failures → Log, alert admin, manual retry
- Email failures → Queue for retry (up to 24 hours)
- Social posting → Manual fallback (alert user)

## Caching Strategy

### Redis Cache Layers

```
Cache Key                  | TTL    | Purpose
─────────────────────────────────────────────────────
user:{user_id}:profile    | 1 hour | User profile data
practice:{id}:agents      | 30 min | Agent list
college:database          | 24 hrs | College data
college:recommendations:{student_id} | 12 hrs | Matching results
analytics:{type}          | 1 hour | Metrics data
```

### Cache Invalidation

- On create/update: Invalidate related keys
- Time-based: TTL expiration
- Manual: Admin endpoint to clear caches

## Scalability Considerations

### Horizontal Scaling

```
Load Balancer (nginx)
    ├─ Backend Server 1 (FastAPI)
    ├─ Backend Server 2 (FastAPI)
    └─ Backend Server N
    
    ├─ PostgreSQL (Primary)
    ├─ PostgreSQL (Replica)
    
    ├─ Redis Cluster
    
    └─ CDN (for static frontend)
```

### Database Optimization

- Indexes on foreign keys and frequently queried columns
- Read replicas for analytics queries
- Connection pooling (SQLAlchemy)
- Query optimization (avoid N+1 queries)

### API Rate Limiting

- Auth endpoints: 5 requests per minute per IP
- Chat endpoints: 60 requests per hour per user
- General endpoints: 1000 requests per hour per user
- Admin endpoints: 100 requests per minute

## Security Architecture

### Layers

1. **Transport**: HTTPS/TLS (enforced in production)
2. **Authentication**: JWT tokens with secure signing
3. **Authorization**: RBAC middleware validation
4. **Input Validation**: Pydantic schemas
5. **SQL Injection**: SQLAlchemy ORM (parameterized queries)
6. **CORS**: Strict origin checking
7. **Secrets**: Environment variables (never hardcoded)
8. **Encryption**: Passwords (bcrypt), sensitive data (AES-256 in future)

## Monitoring & Observability

### Logging

```
Format: JSON structured logs
Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
Output: Console (dev) + CloudWatch (prod)
```

### Metrics

```
Application Metrics:
- API response times
- Error rates by endpoint
- LLM token usage & costs
- Database query performance

Business Metrics:
- User signups by day
- Practice activations
- Freemium conversions
- Plan approvals
```

### Alerting

```
Critical: Database down, API errors > 5%, LLM API errors
Warning: Response time > 2s, Queue depth > 100
Info: Daily summary email
```

## Deployment Architecture

### Development

```
docker-compose.yml
├─ postgres:15 (local)
├─ redis:7 (local)
├─ backend (FastAPI dev server)
└─ frontend (Vite dev server)
```

### Staging/Production

```
AWS Infrastructure
├─ RDS PostgreSQL (primary + replica)
├─ ElastiCache Redis
├─ ECS Fargate (backend containers)
├─ CloudFront (CDN for frontend)
├─ S3 (file storage)
├─ CloudWatch (logging)
├─ Route 53 (DNS)
└─ WAF (DDoS protection)
```

## Testing Strategy

### Unit Tests

```
Backend: Pytest
├─ Models tests (ORM validation)
├─ Service tests (business logic)
├─ Schema tests (validation)
└─ Utility tests (helpers)

Frontend: Vitest/Jest
├─ Component tests (React components)
├─ Hook tests (custom hooks)
└─ Service tests (API client)
```

### Integration Tests

```
Backend: Pytest with test database
├─ API endpoint tests
├─ Database transaction tests
├─ External API mocks (Claude, Stripe, etc.)
└─ Error handling tests
```

### End-to-End Tests

```
Selenium/Cypress
├─ Sign up → Discovery → Strategy flow
├─ College search → Upgrade flow
└─ Agent execution workflow
```

## Roadmap (Phase 2+)

See [ROADMAP.md](./ROADMAP.md) for detailed Phase 2 and beyond plans.

---

**Last Updated**: 2026-06-22  
**Maintained By**: Nikhil Varma
