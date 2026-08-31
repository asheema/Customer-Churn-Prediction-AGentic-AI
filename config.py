from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Churn Intelligence Platform"
    environment: str = "development"
    api_key: str = "change-me"
    database_url: str = "sqlite:///./data/churn.db"
    model_path: str = "models/churn_model.joblib"
    prediction_threshold: float = 0.50
    cors_origins: str = "http://localhost:3000"
    model_version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def settings():
    return Settings()
