from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import predict_anomaly_type
import re

app = FastAPI()

# --- Cleaning helpers ---
def clean_log_line(line: str) -> str:
    """
    Extract severity + message from raw log line
    """
    parts = line.split()
    severities = ["INFO", "ERROR", "SEVERE", "FATAL", "WARNING"]
    for i, token in enumerate(parts):
        if token in severities:
            return f"{token} " + " ".join(parts[i+1:])
    return line  # fallback if severity not found

def clean_logs(logs: list[str]) -> list[str]:
    return [clean_log_line(line) for line in logs]

class LogRequest(BaseModel):
    log_sequence: list[str]

@app.post("/predict")
def predict_log(request: LogRequest):
    # Step 1: clean incoming logs
    cleaned_logs = clean_logs(request.log_sequence)

    # Step 2: run model prediction
    prediction = predict_anomaly_type(cleaned_logs)

    return {
        "prediction": prediction,
        "cleaned_logs": cleaned_logs  # optional: lets you verify cleaning
    }