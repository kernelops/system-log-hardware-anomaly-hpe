Download the output folder full_log_anomaly_model from the notebook. Its structure should look like this:
```
full_log_anomaly_model/
│
├── bert_feature_extractor/
│   ├── config.json
│   └── model.safetensors
│
├── tokenizers/
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.txt
│
├── id2label.json
└── xgb_classifier.joblib
```
I couldn't add it as it is too big

1. Install Python
2. Create a venv:
```
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the server:
```
uvicorn app.main:app --reload
```

5. Open Swagger docs at:
```
http://127.0.0.1:8000/docs
```


Project Structure
```
logbert-restapi/
│
├── app/
│   ├── main.py
│   ├── utils.py
│   └── schemas.py
│
├── full_log_anomaly_model/
│   ├── bert_feature_extractor/
│   │   ├── config.json
│   │   └── model.safetensors
│   │
│   ├── tokenizers/
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   └── vocab.txt
│   │
│   ├── id2label.json
│   └── xgb_classifier.joblib
│
└── requirements.txt
```
