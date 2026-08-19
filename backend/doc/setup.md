# Aegis AI-Agent Setup & Deployment Guide

This guide walks through setting up the Aegis AI-Agent backend locally, running with Docker, configuring environment variables, and running the test suite.

---

## 1. Prerequisites

- Python 3.10+ (recommended Python 3.12)
- Docker & Docker Compose (or Podman)
- Ollama (running locally on port 11434 with model `llama3` or `mistral`)
- PostgreSQL database (optional if running standalone SQLite mock)

---

## 2. Environment Configuration (`.env`)

Copy `.env.example` to `.env` in the `backend/` directory or export the following variables:

```bash
# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3
LLM_TIMEOUT=60

# Database Configuration
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/aegis
MARIADB_URL=mysql+pymysql://root:password@localhost:3306/aegis
MSSQL_URL=mssql+pyodbc://sa:Password123@localhost:1433/aegis?driver=ODBC+Driver+18+for+SQL+Server

# Execution Settings
EXECUTION_TIMEOUT=30
WORKSPACE_ROOT=/app/workspace
```

---

## 3. Running with Docker

Build and start the backend service:

```bash
cd backend
docker build -t aegis-backend .
docker run -p 8000:8000 --env-file .env aegis-backend
```

Or using Docker Compose:

```bash
docker-compose up --build
```

The FastAPI application will be accessible at:
- **API root**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

---

## 4. Local Development Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server with live reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 5. Running the Test Suite

Run the full test suite with `pytest`:

```bash
pytest backend/tests -v
```

Or execute individual test suites:

```bash
python3 -m unittest discover -s backend/tests
```