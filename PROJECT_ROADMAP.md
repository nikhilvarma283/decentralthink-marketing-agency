# Project Roadmap: Weeks 1-8 (Parallel Execution)

## Overview

Three parallel tracks running simultaneously to get to revenue and investor-ready metrics by Week 8.

```
TRACK 1: Sprint 1-2 Development       TRACK 2: Dental Acquisition       TRACK 3: DevOps & Ops
(Backend + Frontend Implementation)    (Customer Acquisition)            (Infrastructure)
├─ Week 1-2: Core Features            ├─ Week 1: Pitch & Materials      ├─ Week 1: GitHub Actions
├─ Week 3-4: Polish & Testing         ├─ Week 2-3: Research & Outreach  ├─ Week 2-3: AWS Setup
├─ Week 5-6: Dental Onboarding        ├─ Week 4: Close First Practice    ├─ Week 4: Monitoring & Alerts
├─ Week 7-8: Execution & Payment      └─ Week 5-8: Onboard & Support    └─ Week 5-8: Prod Hardening
└─ Outcome: Auth, Chat, Strategy      └─ Outcome: 1-2 Practices Paying   └─ Outcome: Enterprise-Ready
```

---

## TRACK 1: Sprint 1-2 Development (Weeks 1-4)

### Week 1-2: Shared Foundation (9 Stories, 54 points)

**Goal**: Core infrastructure for both verticals

| Story | Task | Est. | Owner |
|-------|------|------|-------|
| 1.1-1.2 | Auth: Signup/Login/JWT | 1 day | Claude |
| 1.3-1.4 | Chat Interface + Multi-turn | 1.5 days | Claude |
| 1.5 | File Upload (PDF, DOCX, images) | 1 day | Claude |
| 1.6 | Strategy Storage (DB models, CRUD) | 0.5 day | Claude |
| 1.7 | Stripe Customer Setup (no charging yet) | 0.5 day | Claude |
| 1.9 | Analytics Dashboard (basic metrics) | 1 day | Claude |
| **Testing & Polish** | Unit tests, documentation | 1.5 days | Claude |
| **Definition of Done** | `docker-compose up` → signup → login → chat works | EOW2 | You |

**Deliverable**: 
- Backend: `/api/v1/auth/*`, `/api/v1/chat/*`, `/api/v1/users/*` endpoints working
- Frontend: Login page, Chat page, basic dashboard
- Database: All migrations auto-run, users/messages persisted

**Verification**: 
```bash
docker-compose up
# Navigate to localhost:3000
# Sign up → Login → Send message in chat → Message appears
```

---

### Week 3-4: Dental Discovery Phase (5 Stories, 31 points)

**Goal**: Dental-specific onboarding → 90-day plan generation

| Story | Task | Est. | Owner |
|-------|------|------|-------|
| 3.1 | Dental Onboarding Flow (form) | 1 day | Claude |
| 3.2 | Multi-Session Discovery Chat (5 guided sessions) | 1.5 days | Claude |
| 3.3 | Strategy Synthesizer (Claude API → 90-day plan) | 1.5 days | Claude |
| 3.4 | Strategy Viewer & Editor (markdown display, edit, approve) | 1 day | Claude |
| 3.5 | Agent Framework Skeleton (list agents, configure stubs) | 0.5 day | Claude |
| **Testing & Iteration** | E2E test: onboarding → strategy generation | 1.5 days | Claude |

**Deliverable**:
- Backend: `/api/v1/onboarding/dental`, `/api/v1/discovery/session/*`, `/api/v1/strategy/*` endpoints
- Frontend: Onboarding form → 5-session chat → Strategy review/edit page
- Integration: Claude API calls working, strategies stored in DB

**Verification**:
```bash
docker-compose up
# Sign up as dentist → Onboarding form → Start discovery chat
# Complete 5 sessions → System generates 90-day plan → Review & approve
```

---

## TRACK 2: Dental Customer Acquisition (Weeks 1-8)

### Week 1: Create Materials (3-4 hours of work for you)

**Deliverables** (I'll help draft, you refine):

1. **1-Page Practice Pitch** (PDF)
   - Problem: Low patient acquisition
   - Solution: AI-powered marketing agents
   - ROI: "20+ new patient inquiries/month"
   - Price: $500/month (first 2 weeks free to test)
   - CTA: "Schedule 20-min demo"

2. **Email Template** (cold outreach)
   ```
   Subject: AI Marketing for [Practice Name]
   
   Hi [Owner],
   
   Most dental practices spend 30+ hours/month on marketing with minimal results.
   
   We built DecentralThink to automate that. AI agents:
   - Post engaging content (Twitter, LinkedIn, email)
   - Generate reviews from happy patients
   - Run referral campaigns
   - All while you focus on patients
   
   Result: Our beta dentists got 20+ new inquiries in month 1.
   
   Curious? Let's chat for 20 minutes.
   
   [Calendar link]
   
   —Nikhil
   ```

3. **LinkedIn Pitch** (connection message)
   ```
   Hi [Name], 
   
   I noticed you're running [practice name]. 
   I'm building an AI agent that handles patient acquisition for dental practices.
   
   Takes 15 minutes to set up, no upfront cost (test it free for 2 weeks).
   
   Worth 20 minutes to explore?
   
   [Calendar link]
   ```

4. **Target Practice Profile**
   - 2-4 dentists
   - 500-1000 patient base
   - Located in US
   - Spending < $2.5K/month on marketing (open to growth)
   - Active on social media or willing to be

**Your Action**: 
- Refine 1-pager and email
- Create a list of 15 target practices (LinkedIn, Google Maps search by city)
- Send 5 test emails this week to get feedback

---

### Week 2-3: Research & Warm Outreach

**Your Action**:
1. Build a list of 20-30 target practices with owner names (LinkedIn research)
2. Personalize and send emails (batch of 10 per day)
3. Make cold calls to practices who don't respond to email (get number from practice websites)
4. Track: # sent, # responses, # interested, # meetings

**Success Metrics**:
- 20-30 emails sent
- 3-5 responses (15% response rate is good)
- 1-2 meetings scheduled

---

### Week 4: Close First Practice

**Timeline**:
- Mon-Wed: Schedule demos with interested practices (30-45 min each)
- During demo:
  - Show them the platform (even if auth not perfect yet)
  - Manually run a strategy synthesis for their practice
  - Show what agents will do for them
  - Get commitment: "Try free for 2 weeks, then $500/month"

**Success Metric**: 
- 1 signed customer (email + Stripe setup, even if charging is manual)

**What you'll tell them**:
> "We're launching this week. You're in the first cohort. Free for 2 weeks to test, then $500/month if you love it. I'll personally oversee your strategy and onboarding."

---

### Week 5-8: Onboarding & Support

**Your Action**:
1. Onboard first practice into the platform (they complete discovery chat)
2. You manually synthesize their strategy (use Claude API through platform)
3. Start generating content (manually until agents are ready)
4. Weekly check-ins: "How many leads? What's working?"
5. Iterate based on feedback

**Success Metric**:
- First practice active and generating leads
- Monthly revenue: $500-1000 MRR

---

## TRACK 3: DevOps & Operations (Weeks 1-8)

### Week 1: GitHub Actions Setup

**Goal**: Auto-run tests on every PR, ensure code quality

**Deliverables**:

1. **Backend Tests Workflow** (`.github/workflows/backend-tests.yml`)
   - Run on: `git push` to any branch
   - Steps:
     - Install dependencies
     - Run `pytest` (all backend tests)
     - Upload coverage report
   - Fail if: Tests fail OR coverage < 80%

2. **Frontend Tests Workflow** (`.github/workflows/frontend-tests.yml`)
   - Run on: `git push` to any branch
   - Steps:
     - Install dependencies
     - Run `npm test` (all frontend tests)
     - Lint check: `npm run lint`
   - Fail if: Tests fail OR linting errors

3. **Docker Build Workflow** (`.github/workflows/docker-build.yml`)
   - Test that Docker images build successfully
   - Run on: PRs to main, pushes to main

**Your Action**: 
- Review workflows (I'll provide)
- Commit to repo
- Verify workflows run on next commit

---

### Week 2-3: AWS Deployment Preparation

**Goal**: Ready to deploy to production when needed

**Deliverables**:

1. **Terraform Infrastructure Code** (IaC)
   ```
   aws/
   ├── rds.tf          (PostgreSQL RDS setup)
   ├── elasticache.tf  (Redis cluster)
   ├── ecs.tf          (Fargate containers for backend)
   ├── s3.tf           (File storage for uploads)
   ├── cloudfront.tf   (CDN for frontend)
   ├── iam.tf          (Roles & permissions)
   └── variables.tf    (Configuration)
   ```

2. **Deployment Guide** (README)
   - Prerequisites: AWS account, Terraform, AWS CLI
   - Commands: `terraform apply` → Deploy entire stack
   - Cost estimate: ~$200-500/month

3. **Environment Secrets Management**
   - AWS Secrets Manager for API keys
   - Environment-specific `.env` files (dev, staging, prod)

**Your Action**:
- Create AWS account (free tier covers this)
- Install Terraform & AWS CLI
- Review infrastructure code
- Deploy to staging environment (test it works)

---

### Week 4: Monitoring & Alerts

**Deliverables**:

1. **CloudWatch Dashboards**
   - API response times
   - Error rates by endpoint
   - Database connection pool
   - Redis cache hit rate
   - LLM API costs

2. **Alerts** (email/SMS if something breaks)
   - Database down → Email within 1 min
   - API error rate > 5% → Email
   - SSL certificate expires in 7 days → Email

3. **Log Aggregation** (CloudWatch Logs)
   - All application logs → CloudWatch
   - Searchable by request ID, user, error type

**Your Action**:
- Set up CloudWatch dashboard (I'll provide template)
- Configure email alerts
- Test: Trigger an alert manually to verify it works

---

### Week 5-8: Production Hardening

**Deliverables**:

1. **Security Hardening**
   - HTTPS enforced (AWS Certificate Manager)
   - WAF (Web Application Firewall) enabled
   - Rate limiting on all endpoints
   - SQL injection prevention review
   - CORS properly configured

2. **Database Backups** (automated daily)
   - AWS RDS automated backups (30-day retention)
   - Restore tested monthly

3. **Performance Optimization**
   - Database query indexing reviewed
   - Frontend bundle size optimized
   - CDN caching configured for static assets

4. **Documentation**
   - Deployment runbook (how to deploy)
   - Incident response guide (what to do if prod is down)
   - On-call rotation setup

**Your Action**:
- Review security checklist
- Test backup & restore procedure
- Run performance tests
- Document runbooks

---

## Milestones & Checkpoints

### End of Week 2
- ✅ Auth, chat, strategy storage working locally
- ✅ GitHub Actions running tests automatically
- ✅ 5+ practice emails sent, initial responses coming in

### End of Week 4
- ✅ Dental onboarding → strategy synthesis → execution flow complete
- ✅ AWS infrastructure deployed to staging
- ✅ 1 practice signed (or very close)

### End of Week 6
- ✅ HS SaaS foundation running locally
- ✅ First practice actively generating plans
- ✅ Production monitoring live

### End of Week 8 (Phase 1 Complete)
- ✅ 1-2 dental practices paying ($500-1000 MRR)
- ✅ 20-50 HS users active
- ✅ Platform running on AWS (production-ready)
- ✅ GitHub Actions CI/CD working
- ✅ Ready to pitch to investors Q1 2027

---

## Weekly Check-in Template

Every Friday, update:

```
WEEK X SUMMARY
==============

TRACK 1 (Development):
- Completed: [Stories X, Y, Z]
- Blockers: [Any issues?]
- Next: [What's coming]

TRACK 2 (Acquisition):
- Emails sent: [N]
- Responses: [N] 
- Meetings: [Names]
- Next: [Follow-ups]

TRACK 3 (DevOps):
- Completed: [Infrastructure X, Y]
- Blockers: [Any issues?]
- Next: [What's coming]

METRICS:
- Development velocity: [story points/week]
- Customer pipeline: [N interested, M committed]
- System uptime: [% if in production]
```

---

## Success Criteria (Week 8)

| Metric | Target | Status |
|--------|--------|--------|
| Backend Stories Complete | All Sprint 1-2 + 3-4 | — |
| Frontend Stories Complete | All Sprint 1-2 + 3-4 | — |
| Tests Passing | 100% | — |
| Dental Practices | 1-2 paying | — |
| MRR (Monthly Recurring Revenue) | $500-1000 | — |
| HS Users | 20-50 active | — |
| Production Deployment | Live on AWS | — |
| GitHub Actions | All passing | — |
| Monitoring Alerts | Working | — |

---

## Decision Points

**If blocked on development**: Skip non-critical features, extend timeline

**If customer acquisition stalls**: Adjust messaging, try different channels (calls vs. email), offer longer free trial

**If AWS deployment is complex**: Stay on Docker-compose for longer, deploy later

---

**Next Step**: Confirm you're ready to start, then I'll:
1. Create detailed Sprint 1-2 code specs (ready by EOD)
2. Draft customer acquisition materials (ready by EOD)
3. Commit GitHub Actions & Terraform code (ready by EOD)

Sound good?
