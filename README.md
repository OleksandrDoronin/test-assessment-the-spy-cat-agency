# Spy Cats API

A FastAPI-based REST API for managing spy cats, their missions, and mission targets.

## Features

- **Spy Cat Management**: Create, read, update, and delete spy cats with breed validation via TheCatAPI
- **Mission Management**: Create missions with 1-3 targets, assign cats to missions
- **Target Tracking**: Update mission targets with notes and completion status
- **Pagination**: List endpoints support limit/offset pagination
- **Database**: SQLite with SQLAlchemy ORM and Alembic migrations

## Requirements

- Python 3.13+
- UV package manager

## Installation

```bash
# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head
```

## Running the Application

```bash
# Development server
uv run python src/main.py

# Or using uvicorn directly
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Spy Cats

- `POST /cats` - Create a new spy cat (breed validated with TheCatAPI)
- `GET /cats` - List all spy cats (paginated)
- `GET /cats/{cat_id}` - Get spy cat details
- `PATCH /cats/{cat_id}` - Update spy cat salary
- `DELETE /cats/{cat_id}` - Delete spy cat

### Missions

- `POST /missions` - Create a mission with 1-3 targets
- `GET /missions` - List all missions (paginated)
- `GET /missions/{mission_id}` - Get mission details
- `PATCH /missions/{mission_id}/assign` - Assign a cat to a mission
- `DELETE /missions/{mission_id}` - Delete mission (only if not assigned)

### Targets

- `PATCH /missions/{mission_id}/targets/{target_id}` - Update target notes or mark as completed

## Project Structure

```
src/
├── main.py              # Application entry point
├── router.py            # API routes
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # Business logic
├── repositories/        # Database access layer
├── dependencies/        # FastAPI dependencies
├── errors/              # Custom exceptions
└── utils/               # Helper functions
```

## Development

```bash
# Install dev dependencies
uv sync --all-groups

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

## Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```
