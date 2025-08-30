from pydantic import BaseModel
from typing import List

class InputData(BaseModel):
    features: List[float]  # one embedding vector

class PredictionResponse(BaseModel):
    prediction: int
    label: str
