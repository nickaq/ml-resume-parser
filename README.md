# ML Resume Parser — AI-Powered Job Recommendations

A full-stack web application that recommends vacancies to users based on resume text and vacancy descriptions, using NLP/ML for matching.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Docker Compose                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   PostgreSQL  │  │   FastAPI    │  │   Next.js     │  │
│  │   (asyncpg)   │◄─│   Backend    │◄─│   Frontend    │  │
│  │   :5432       │  │   :8000      │  │   :3000       │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Backend Architecture (Clean Architecture-inspired)

```
backend/app/
├── api/             # FastAPI route handlers & dependencies
│   ├── routes/      # Endpoint definitions (auth, resumes, vacancies, etc.)
│   ├── deps.py      # FastAPI Depends (auth, db session)
│   └── router.py    # Router registry
├── core/            # Configuration, security, database setup
│   ├── config.py    # Pydantic Settings (env-based)
│   ├── database.py  # Async SQLAlchemy engine & session
│   └── security.py  # JWT & password hashing
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic request/response schemas
├── services/        # Business logic layer
├── repositories/    # Data access layer (generic CRUD + custom queries)
├── ai/              # AI/NLP recommendation engine (placeholder)
└── utils/           # Shared helper functions
```

### Frontend Architecture

```
frontend/src/
├── app/             # Next.js App Router (pages & layouts)
├── components/      # Reusable UI components
├── lib/             # Utilities (API client)
├── services/        # API service modules (auth, resume, vacancy, etc.)
└── types/           # TypeScript type definitions
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **Async SQLAlchemy** | Non-blocking I/O for high-concurrency API endpoints |
| **Repository Pattern** | Clean separation of data access from business logic; easy to mock in tests |
| **Service Layer** | Business logic lives outside routes — testable and reusable |
| **Pydantic Settings** | Type-safe environment configuration with validation |
| **Separate sync URL for Alembic** | asyncpg doesn't support DDL migrations; sync psycopg2 URL used for migrations only |
| **Next.js App Router** | Modern React framework with server components and file-based routing |
| **Monorepo** | Backend and frontend versioned together; simplified Docker Compose orchestration |

### AI Integration Point

The `backend/app/ai/engine.py` module defines a `RecommendationEngine` class with a `match()` method interface. When the NLP/ML module is ready:

1. Implement the `match()` method with your model (cosine similarity, transformers, etc.)
2. Uncomment and implement `RecommendationService.generate_recommendations()`
3. Add a `/recommendations/generate` POST endpoint

The rest of the architecture is already wired to support it.

---

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone and enter the project
cd ml-resume-parser

# 2. Copy environment files
cp backend/.env.example backend/.env

# 3. Start all services (PostgreSQL, Backend, Frontend)
docker compose up --build

# 4. Run migrations (in a separate terminal)
docker compose exec backend alembic upgrade head
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

### Option 2: Local Development

#### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 14+

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local

# Start dev server
npm run dev
```

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | No | Health check |
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login and get JWT token |
| POST | `/api/v1/resumes` | Yes | Upload a resume |
| GET | `/api/v1/resumes` | Yes | List user's resumes |
| GET | `/api/v1/resumes/{id}` | Yes | Get a specific resume |
| DELETE | `/api/v1/resumes/{id}` | Yes | Delete a resume |
| POST | `/api/v1/vacancies` | Yes | Create a vacancy |
| GET | `/api/v1/vacancies` | No | List active vacancies |
| GET | `/api/v1/vacancies/{id}` | No | Get a vacancy |
| PATCH | `/api/v1/vacancies/{id}` | Yes | Update a vacancy |
| DELETE | `/api/v1/vacancies/{id}` | Yes | Delete a vacancy |
| GET | `/api/v1/recommendations` | Yes | Get recommendations |

---

## Project Structure

```
ml-resume-parser/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── health.py
│   │   │   │   ├── recommendations.py
│   │   │   │   ├── resumes.py
│   │   │   │   └── vacancies.py
│   │   │   ├── deps.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── vacancy.py
│   │   │   ├── recommendation.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── vacancy.py
│   │   │   ├── recommendation.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── resume_service.py
│   │   │   ├── vacancy_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── __init__.py
│   │   ├── repositories/
│   │   │   ├── base.py
│   │   │   ├── user_repository.py
│   │   │   ├── resume_repository.py
│   │   │   ├── vacancy_repository.py
│   │   │   ├── recommendation_repository.py
│   │   │   └── __init__.py
│   │   ├── ai/
│   │   │   ├── engine.py
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── helpers.py
│   │   │   └── __init__.py
│   │   └── main.py
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── Button.tsx
│   │   │   └── Card.tsx
│   │   ├── lib/
│   │   │   └── api-client.ts
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   ├── resume.service.ts
│   │   │   ├── vacancy.service.ts
│   │   │   └── recommendation.service.ts
│   │   └── types/
│   │       └── index.ts
│   ├── .env.example
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
└── .gitignore
```

---

## Next Steps

1. **Add AI/ML matching** — Implement `RecommendationEngine.match()` in `backend/app/ai/engine.py`
2. **Add tests** — pytest for backend, Jest/Playwright for frontend
3. **Add resume parser** — Extract skills, experience, education from raw text
4. **Add vacancy ingestion** — Scrape or import vacancy data from job boards
5. **Add user profile page** — Dashboard with resume management and recommendations
6. **Add CI/CD** — GitHub Actions for linting, testing, and deployment
