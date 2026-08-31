"""
Tool-calling style business agent.

This module deliberately keeps the agent deterministic and local so the demo
runs without an LLM API key. In a real deployment, an approved LLM gateway
can call the same tools with an allow-listed tool schema.
"""
from .model import ModelService

class ChurnAgent:
    def __init__(self, model: ModelService):
        self.model = model

    def answer(self, message: str, customer: dict | None = None):
        text = message.lower()

        if customer and any(word in text for word in ["churn", "risk", "leave", "cancel"]):
            probability, prediction, risk = self.model.predict(customer)
            answer = (
                f"Customer {customer['customer_id']} has a "
                f"{probability:.1%} estimated churn probability and is "
                f"classified as {risk} risk. "
                + (
                    "A retention workflow should be considered."
                    if prediction == 1 else
                    "No high-risk churn flag was triggered at the configured threshold."
                )
            )
            return answer, "predict_churn", (probability, prediction, risk)

        if "explain" in text or "why" in text:
            if customer:
                reasons = []
                if customer["login_frequency"] < 1:
                    reasons.append("low login frequency")
                if customer["support_tickets"] >= 5:
                    reasons.append("high support-ticket volume")
                if customer["payment_failures"] >= 2:
                    reasons.append("repeated payment failures")
                if reasons:
                    return "Potential risk signals include " + ", ".join(reasons) + ".", "explain_risk", None
            return "Provide a customer record and I can explain the configured risk signals.", None, None

        return (
            "I can help with churn risk, explain risk signals, and produce "
            "a prediction when customer features are provided."
        ), None, None
