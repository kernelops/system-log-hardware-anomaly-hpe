Download the output file named full_log_anomaly_model from the notebook
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
Its file structure will be as mentioned above
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
This should be the project directory
logbert-restapi
│── app/
│   ├── main.py
│   ├── utils.py
│   ├── schemas.py
│── full_log_anomaly_model/
|    ├── bert_feature_extractor/
|    │   ├── config.json
|    │   └── model.safetensors
|    │
|    ├── tokenizers/
|    │   ├── special_tokens_map.json
|    │   ├── tokenizer_config.json
|    │   └── vocab.txt
|    │
|    ├── id2label.json
|    └── xgb_classifier.joblib
│── requirements.txt