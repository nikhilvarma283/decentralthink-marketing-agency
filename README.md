# DecentralThink Marketing Agency Platform

A customizable AI-powered marketing agency platform for dental practices and high school students.

## Overview

DecentralThink is a **Phase 1** implementation of a dual-track marketing platform:

1. **Dental Managed Service** (US): AI agents help dental practices with patient acquisition, retention, and marketing automation
2. **High School SaaS** (Global): Free/freemium platform helping high schoolers with college exploration and career guidance

## Project Structure

```
decentralthink-marketing-agency/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── utils/        # Helper functions
│   │   ├── main.py       # FastAPI app
│   │   ├── config.py     # Configuration
│   │   └── database.py   # Database setup
│   ├── tests/            # Pytest test suite
│   ├── migrations/       # Alembic database migrations
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Docker image definition
├── frontend/             # React + TypeScript application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API client
│   │   ├── types/        # TypeScript types
│   │   ├── App.tsx       # Root app component
│   │   └── main.tsx      # Entry point
│   ├── package.json      # Node dependencies
│   ├── tsconfig.json     # TypeScript configuration
│   ├── vite.config.ts    # Vite configuration
│   └── Dockerfile        # Docker image definition
├── docker-compose.yml    # Multi-container orchestration
├── .gitignore            # Git ignore rules
└── README.md             # This file

```

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0
- **API Documentation**: Swagger UI (automatic)
- **Testing**: Pytest

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Database Migrations**: Alembic

## Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- Node.js 18+ (for local frontend development, optional)
- Python 3.11+ (for local backend development, optional)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/nikhilvarma283/decentralthink-marketing-agency.git
cd decentralthink-marketing-agency
```

2. Create environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Start all services:
```bash
docker-compose up
```

4. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

### Local Development (Without Docker)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

## Architecture

### System Layers

```
┌─────────────────────────────────────────────┐
│         User Interfaces (React)             │
│  Dental UI │ HS SaaS UI                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      FastAPI REST API (/api/v1/*)          │
│  Auth │ Chat │ Strategy │ Agents │ ...    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Core Orchestration Engine                │
│  LLM Integration │ Agent Framework │ ...   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       Data Layer (PostgreSQL + Redis)       │
└─────────────────────────────────────────────┘
```

## API Endpoints

All endpoints are prefixed with `/api/v1/`. Full documentation available at `/docs` when server is running.

### Authentication
- `POST /auth/signup` — Register new user
- `POST /auth/login` — Login user
- `POST /auth/logout` — Logout user

### User Management
- `GET /users/profile` — Get user profile
- `PATCH /users/profile` — Update user profile
- `GET /users/preferences` — Get user preferences
- `PATCH /users/preferences` — Update preferences

### Chat & Discovery
- `POST /chat/message` — Send chat message
- `POST /chat/upload` — Upload file to chat
- `GET /discovery/sessions` — Get discovery sessions
- `POST /discovery/session/{n}` — Create/get session

### Strategies & Plans
- `POST /strategy/generate` — Generate strategy
- `GET /strategy/{id}` — Get strategy
- `PATCH /strategy/{id}` — Update strategy
- `POST /strategy/{id}/approve` — Approve strategy

### Dental-Specific
- `GET /agents` — List agents
- `POST /agents` — Create agent
- `GET /execution/pending` — Get pending tasks
- `POST /execution/{id}/approve` — Approve & execute

### Colleges (HS)
- `GET /colleges` — List colleges
- `GET /recommendations/{student_id}` — Get college recommendations

### Analytics
- `GET /analytics/summary` — Get platform metrics
- `GET /analytics/hs-summary` — Get HS-specific metrics

## Database Schema

See `backend/alembic/versions/` for schema definitions. Key tables:

- `users` — User accounts (dentists, high schoolers, admins)
- `practices` — Dental practices
- `students` — High school student profiles
- `chat_messages` — Chat conversation history
- `plans` — Marketing/strategy plans
- `agents` — Automated agents (dental)
- `executions` — Agent execution logs
- `colleges` — College database (HS)
- `student_recommendations` — College matches

## Testing

### Backend Tests
```bash
cd backend
pytest                    # Run all tests
pytest --cov            # Run with coverage
pytest -v               # Verbose output
```

### Frontend Tests
```bash
cd frontend
npm test                 # Run tests
npm test -- --coverage  # With coverage
```

## Deployment

### Docker Deployment
```bash
docker-compose up -d    # Run in background
docker-compose logs -f  # View logs
docker-compose down     # Stop all services
```

### Database Backups
```bash
./scripts/backup_db.sh      # Backup PostgreSQL
./scripts/restore_db.sh     # Restore from backup
```

## Environment Variables

### Backend (`.env`)
```
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key
CLAUDE_API_KEY=sk-ant-xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
SENDGRID_API_KEY=SG.xxxxx
```

### Frontend (`.env`)
```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request

## Development Workflow

### Code Style
- **Backend**: PEP 8 (enforced by black/pylint)
- **Frontend**: ESLint + Prettier

### Pre-commit Checks
```bash
# Backend
black app/
pylint app/

# Frontend
npm run lint
npm run format
```

## Known Limitations (Phase 1)

- [ ] Autonomous agent execution (manual approval required)
- [ ] Video/multimedia support in chat
- [ ] CRM integration for dental
- [ ] School B2B partnerships for HS
- [ ] College essay coaching
- [ ] SAT proctoring integration

See [ROADMAP.md](./ROADMAP.md) for Phase 2+ plans.

## Troubleshooting

### "Connection refused" on localhost:8000
- Ensure `docker-compose up` is running
- Check: `docker ps` to see running containers
- View logs: `docker-compose logs backend`

### Database migration errors
- Restart containers: `docker-compose restart postgres`
- Rebuild images: `docker-compose build --no-cache`

### Frontend won't connect to backend
- Check REACT_APP_API_URL in `.env`
- Verify backend is running: `curl http://localhost:8000`
- Check browser console for CORS errors

## Support

- **Issues**: Create an issue on GitHub
- **Email**: support@decentralthink.com
- **Slack**: [Join our community](link-to-slack)

## License

MIT License — see LICENSE.md

## Authors

- **Nikhil Varma** — Founder & Architect

---

**Current Phase**: Phase 1 (MVP)  
**Last Updated**: 2026-06-22  
**Next Milestone**: Phase 1 Alpha Launch (Week 8 for dental, Week 12 for HS)
