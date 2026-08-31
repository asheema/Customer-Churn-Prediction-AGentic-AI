# Interview story

I built a full-stack customer churn intelligence platform.

The frontend is a React dashboard where an operator enters customer attributes and can ask a conversational agent for churn analysis.

The React application calls a FastAPI backend. FastAPI validates the request with Pydantic, authenticates it, and sends features to a versioned scikit-learn model. The service returns churn probability, threshold-based prediction and risk level, and stores the prediction for audit/analysis.

The agent is implemented with an allow-listed tool pattern. It can call the churn prediction and risk-explanation tools; it cannot execute arbitrary code. This design can later be connected to an approved enterprise LLM gateway.

The application is containerized with Docker and has a GitHub Actions CI workflow. For production, I would add company IAM, secret management, PostgreSQL migrations, observability, model registry, drift monitoring, approval gates, canary deployment and rollback.

A key engineering decision was to keep the demo runnable without an external LLM API key, while keeping a clear boundary where a governed LLM/tool-calling layer can be introduced.
