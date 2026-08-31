from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42
FEATURES = [
    "age", "monthly_spend", "login_frequency",
    "support_tickets", "payment_failures", "subscription_days"
]

def make_demo_data(n=10000):
    rng = np.random.default_rng(RANDOM_STATE)
    age = rng.integers(18, 70, n)
    spend = np.clip(rng.normal(900, 300, n), 50, None)
    login = np.clip(rng.normal(2.5, 1.5, n), 0, None)
    tickets = rng.poisson(3, n)
    failures = rng.poisson(0.7, n)
    days = rng.integers(30, 1000, n)
    score = (
        -0.9 * login + 0.28 * tickets + 0.65 * failures
        - 0.0007 * days + 0.0002 * spend + rng.normal(0, 0.8, n)
    )
    p = 1 / (1 + np.exp(-score))
    churn = rng.binomial(1, p)
    return pd.DataFrame({
        "age": age, "monthly_spend": spend, "login_frequency": login,
        "support_tickets": tickets, "payment_failures": failures,
        "subscription_days": days, "churned": churn
    })

def main():
    df = make_demo_data()
    X, y = df[FEATURES], df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    pipeline = Pipeline([
        ("classifier", RandomForestClassifier(
            n_estimators=250, max_depth=12,
            class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
        ))
    ])
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    prob = pipeline.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, pred))
    print("F1:", round(f1_score(y_test, pred), 4))
    print("ROC-AUC:", round(roc_auc_score(y_test, prob), 4))

    Path("models").mkdir(exist_ok=True)
    joblib.dump(
        {"pipeline": pipeline, "version": "1.0.0-demo"},
        "models/churn_model.joblib"
    )

if __name__ == "__main__":
    main()
