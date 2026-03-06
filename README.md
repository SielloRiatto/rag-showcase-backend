# RAG Demo

FastAPI application with PostgreSQL, SQLAlchemy (async) and Alembic.

## Requirements

- Python 3.11+
- PostgreSQL 14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start

```bash
# Clone and install
git clone <repo-url>
cd rag-showcase
uv sync

# Configure
cp .env.example .env

# Start PostgreSQL
docker run -d --name rag-postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rag_demo postgres:16

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload
```

Application: http://localhost:8000 | [Swagger UI](http://localhost:8000/docs) | [ReDoc](http://localhost:8000/redoc)

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | RAG Demo |
| `DEBUG` | Debug mode | false |
| `DATABASE_URL` | PostgreSQL connection URL | postgresql+asyncpg://...localhost:5432/rag_demo |
| `TEST_DATABASE_URL` | Test database URL | postgresql+asyncpg://...localhost:5432/rag_demo_test |

## Project Structure

```
src/
├── main.py          # FastAPI application
├── config.py        # Settings (pydantic-settings)
├── database.py      # Async engine and session factory
├── models/          # SQLAlchemy models
│   └── base.py      # DeclarativeBase
├── api/
│   ├── deps.py      # Dependencies (DbSession)
│   └── routes/      # Routers
└── services/        # Business logic
```

## Database Migrations

```bash
alembic revision --autogenerate -m "Description"  # Create
alembic upgrade head                               # Apply
alembic downgrade -1                               # Rollback
```

## Documentation

- [Development Guide](docs/development.md) — models, routes, services
- [Testing Guide](docs/testing.md) — writing and running tests
- [Contributing](CONTRIBUTING.md) — GitHub Flow, commit conventions
