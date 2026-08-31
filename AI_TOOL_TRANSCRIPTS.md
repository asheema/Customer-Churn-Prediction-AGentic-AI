# AI-assisted development transcript examples

IMPORTANT: These are **simulated examples**, not genuine exported logs from a real Claude, Cursor, or ChatGPT account. Do not submit them as authentic logs. Use your actual exported conversations if authenticity is required.

## ChatGPT — Architecture prompt

User:
> I need a production-oriented customer churn platform with a React frontend, FastAPI backend, ML inference, an agent that can call approved business tools, a database, Docker and CI. Design the components and API contracts.

Assistant summary:
> Proposed a React dashboard calling FastAPI endpoints. FastAPI validates input, authenticates requests, routes prediction requests to a model service, and routes conversational requests to an allow-listed agent. Predictions and chat audit records are persisted. Docker Compose runs the services locally, and CI runs training smoke tests, compilation and unit tests.

## Claude — Production review prompt

User:
> Review this architecture for production risks. Focus on secrets, authentication, CORS, database sessions, model loading, AI tool permissions and rollback.

Assistant summary:
> Recommended environment/secret-manager configuration, company IAM, restrictive CORS, session cleanup, startup model validation, allow-listed tools, audit logging, model versioning and rollback. Recommended not exposing unrestricted arbitrary code execution through the agent.

## Cursor — Implementation prompt

User:
> Implement FastAPI Pydantic schemas for customer churn prediction and a /predict endpoint. Add a chat endpoint that invokes only approved prediction/explanation tools.

Assistant summary:
> Generated schemas, API endpoints, model service, deterministic agent routing, database persistence and tests. Added API-key authentication as a local demo baseline.

## Debugging prompt

User:
> The API says the model artifact is missing. Explain the cause and the correct startup sequence.

Assistant summary:
> The trained model file is intentionally not committed. Run the training script to create models/churn_model.joblib before starting the API, or provide a managed model artifact at deployment time.

## Real-log guidance

For a real portfolio or hiring assignment:
1. Ask the AI tool to design the architecture.
2. Ask it to generate one module.
3. Ask it to review that module.
4. Give it a real error and ask for diagnosis.
5. Ask for unit tests.
6. Ask for security/production review.
7. Export the actual conversations or screenshots.
8. Keep a human-authored note describing what you accepted, changed, and tested.
