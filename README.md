# Customer Churn Full-Stack AI Platform

A production-oriented reference application demonstrating the lifecycle of an ML feature inside a software product.

## System

React dashboard → FastAPI → validation/auth → ML inference or AI agent → persistence → monitoring/CI.

The included model is trained on synthetic data. Replace it with governed business data for real use.

## Components

- **Frontend:** React + Vite dashboard
- **Backend:** FastAPI REST API
- **ML:** scikit-learn Random Forest, probability/risk scoring
- **Agent:** deterministic tool-calling style agent (no external LLM key required)
- **Database:** SQLAlchemy with SQLite demo configuration; PostgreSQL-compatible URL
- **Packaging:** Docker + Compose
- **CI:** GitHub Actions
- **Security baseline:** environment-based API key, input validation, CORS allow-list
- **MLOps direction:** model version returned by API; add MLflow/model registry and drift tooling in a governed production environment

## Run

```bash
docker compose up --build
```

The backend container needs a model artifact. Generate it first:

```bash
cd backend
python -m venv .venv
# activate it
pip install -r requirements.txt
python scripts/train.py
cd ..
docker compose up --build
```

Frontend: `http://localhost:3000`
API docs: `http://localhost:8000/docs`

## API flow

```text
POST /api/v1/predict
    ↓
Pydantic validation
    ↓
ML pipeline
    ↓
probability + threshold
    ↓
risk
    ↓
database
```

Agent flow:

```text
POST /api/v1/chat
    ↓
Agent intent/tool selection
    ↓
predict_churn / explain_risk
    ↓
ML model
    ↓
natural-language response
```

## Production hardening

Before a real deployment: use company IAM/OIDC instead of a shared API key; HTTPS and gateway/rate limiting; secret manager; PostgreSQL + migrations; structured logging/metrics/tracing; model registry; data/model validation; drift/performance monitoring; approval gates; canary/blue-green deployment; rollback; dependency and container scanning; privacy/retention controls; load testing; and a real LLM gateway with tool allow-lists if generative AI is introduced.

## AI tool transcript note

`AI_TOOL_TRANSCRIPTS.md` contains clearly labeled simulated examples for documentation. They must not be represented as genuine exported logs. For a submission requiring actual logs, export your real ChatGPT/Claude/Cursor sessions.
