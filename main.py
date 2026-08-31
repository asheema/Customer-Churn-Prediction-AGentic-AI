from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .agent import ChurnAgent
from .config import settings
from .db import ChatLog, Prediction, SessionLocal, init_db
from .model import ModelService
from .schemas import (
    ChatRequest, ChatResponse, CustomerFeatures, PredictionResponse
)
from .security import require_api_key

model_service: ModelService | None = None
agent: ChurnAgent | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_service, agent
    init_db()
    model_service = ModelService()
    agent = ChurnAgent(model_service)
    yield

cfg = settings()
app = FastAPI(title=cfg.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in cfg.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_service is not None}

@app.get("/ready")
def ready():
    return {
        "ready": model_service is not None,
        "model_version": model_service.version if model_service else None
    }

@app.post("/api/v1/predict", response_model=PredictionResponse,
          dependencies=[Depends(require_api_key)])
def predict(data: CustomerFeatures):
    probability, prediction, risk = model_service.predict(data.model_dump())
    db = SessionLocal()
    try:
        db.add(Prediction(
            customer_id=data.customer_id,
            churn_probability=probability,
            prediction=prediction,
            risk=risk,
            model_version=model_service.version,
        ))
        db.commit()
    finally:
        db.close()

    return PredictionResponse(
        customer_id=data.customer_id,
        churn_probability=round(probability, 6),
        prediction=prediction,
        risk=risk,
        model_version=model_service.version,
    )

@app.post("/api/v1/chat", response_model=ChatResponse,
          dependencies=[Depends(require_api_key)])
def chat(req: ChatRequest):
    customer = req.customer.model_dump() if req.customer else None
    answer, tool, result = agent.answer(req.message, customer)

    prediction_response = None
    if result and customer:
        probability, prediction, risk = result
        prediction_response = PredictionResponse(
            customer_id=customer["customer_id"],
            churn_probability=round(probability, 6),
            prediction=prediction,
            risk=risk,
            model_version=model_service.version,
        )

    db = SessionLocal()
    try:
        db.add(ChatLog(message=req.message, answer=answer, tool_used=tool))
        db.commit()
    finally:
        db.close()

    return ChatResponse(answer=answer, tool_used=tool, prediction=prediction_response)
