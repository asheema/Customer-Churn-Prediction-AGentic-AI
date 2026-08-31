from pydantic import BaseModel, Field

class CustomerFeatures(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=120)
    monthly_spend: float = Field(ge=0)
    login_frequency: float = Field(ge=0)
    support_tickets: int = Field(ge=0)
    payment_failures: int = Field(ge=0)
    subscription_days: int = Field(ge=1)

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    prediction: int
    risk: str
    model_version: str

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    customer: CustomerFeatures | None = None

class ChatResponse(BaseModel):
    answer: str
    tool_used: str | None = None
    prediction: PredictionResponse | None = None
