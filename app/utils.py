import torch
import joblib
import json
import numpy as np
from pathlib import Path
from transformers import BertModel, BertTokenizer

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Base path to your saved model
BASE_PATH = Path("full_log_anomaly_model")

# Load fine-tuned BERT (LogBERT feature extractor)
bert_model = BertModel.from_pretrained(BASE_PATH / "bert_feature_extractor")
bert_model.to(device)
bert_model.eval()

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained(BASE_PATH / "tokenizer")

# Load XGBoost classifier
xgb_classifier = joblib.load(BASE_PATH / "xgb_classifier.joblib")

# Load id2label mapping
with open(BASE_PATH / "id2label.json", "r") as f:
    id2label = json.load(f)
id2label = {int(k): v for k, v in id2label.items()}  # ensure keys are ints


def prepare_embedding(log_sequence: list[str]):
    """
    Convert raw log sequence -> BERT embedding
    """
    text = " ".join(log_sequence)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = bert_model(**inputs)

    # Take [CLS] token embedding
    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
    return embedding


def predict_anomaly_type(log_sequence: list[str]) -> str:
    """
    Full LogBERT + XGBoost pipeline
    """
    embedding = prepare_embedding(log_sequence)
    prediction_id = int(xgb_classifier.predict(embedding)[0])
    return id2label[prediction_id]
