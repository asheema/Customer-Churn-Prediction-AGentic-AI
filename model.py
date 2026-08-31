from pathlib import Path
import joblib
from .config import settings

class ModelService:
    def __init__(self):
        cfg = settings()
        path = Path(cfg.model_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Model not found: {path}. Run `python scripts/train.py` first."
            )
        bundle = joblib.load(path)
        self.pipeline = bundle["pipeline"]
        self.version = bundle.get("version", cfg.model_version)

    def predict(self, features: dict):
        cfg = settings()
        # The model pipeline was trained on the six feature columns.
        model_features = {
            k: features[k] for k in [
                "age", "monthly_spend", "login_frequency",
                "support_tickets", "payment_failures", "subscription_days"
            ]
        }
        probability = float(self.pipeline.predict_proba([model_features])[0][1])
        prediction = int(probability >= cfg.prediction_threshold)
        risk = "high" if probability >= 0.70 else (
            "medium" if probability >= 0.40 else "low"
        )
        return probability, prediction, risk
