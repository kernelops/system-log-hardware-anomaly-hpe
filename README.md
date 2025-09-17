# HPE CPP-2: Hardware Anomaly Detection from System Logs

Professional implementation of multi-dataset log- and telemetry-driven anomaly detection for hardware reliability. Built as part of the HPE CPP-2 Program.

## Overview

We explored multiple modeling approaches across complementary datasets to detect and forecast hardware anomalies/failures:

- Windows Logs (Loghub): LogBERT embeddings + XGBoost classifier (supervised)
- BGL Supercomputer Logs (Loghub): LogBERT + XGBoost with a FastAPI inference service
- PSM (Pooled Server Metrics): LSTM sequence model (outperformed LSTM+XGBoost ensemble)
- Backblaze Drive Stats: DeepAR time-series forecasting on failure rates (Q1 2025 focus)

## Repository Structure

```
Backblaze-DeepAR-Harddrive/
  backblaze-2025-q1-deepar.ipynb
  Backblaze-DeepAR-Technical-Report.md
  SMART_Attributes_CheatSheet.md

logBERT_XGBoost-BGL-loghub/
  bgl-full-logbert-xgboost.ipynb
  fast-api/
    app/
      main.py
      schemas.py
      utils.py
    requirements.txt

logBERT-windows_logs-loghub/
  LogBERT-windows-logs-anomaly-rate.ipynb
  logbert-model.pth
  vocab_unified.pkl

PSM-LSTM/
  psm-lstm-xgboost.ipynb

loghub/  # sample subsets from Loghub for reference/testing
```

## Approaches and Datasets

- Windows logs: Supervised training with LogBERT embeddings and XGBoost on the Windows subset from Loghub. See `logBERT-windows_logs-loghub/LogBERT-windows-logs-anomaly-rate.ipynb`.

- BGL log anomalies (with API): LogBERT + XGBoost trained via the Kaggle notebook; a FastAPI wrapper serves predictions from the fine-tuned feature extractor and classifier.
  - Training notebook and weights: Kaggle link `https://www.kaggle.com/code/nishanthegde2315/bgl-full-logbert-xgboost`
  - Code: `logBERT_XGBoost-BGL-loghub/` (see FastAPI setup below)

- PSM telemetry anomalies: LSTM and LSTM+XGBoost were evaluated; the pure LSTM performed better.
  - Dataset: `https://www.kaggle.com/datasets/ljolm08/pooled-server-metrics-psm`
  - Notebook: `PSM-LSTM/psm-lstm-xgboost.ipynb`

- Backblaze HDD failure forecasting: DeepAR on per-model daily failure rates, trained primarily on Q1 2025.
  - Dataset: `https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data`
  - Notebook: `Backblaze-DeepAR-Harddrive/backblaze-2025-q1-deepar.ipynb`
  - Technical report: `Backblaze-DeepAR-Harddrive/Backblaze-DeepAR-Technical-Report.md`

## FastAPI Inference Service (BGL - LogBERT + XGBoost)

The API wraps a fine-tuned LogBERT (feature extractor) and an XGBoost classifier to predict anomaly types from sequences of log lines.

### Model artifacts

- Download the model folder produced by the Kaggle training (feature extractor, tokenizer, `xgb_classifier.joblib`, `id2label.json`), and place it at:
  - `logBERT_XGBoost-BGL-loghub/fast-api/app/full_log_anomaly_model/`

Kaggle training reference: `https://www.kaggle.com/code/nishanthegde2315/bgl-full-logbert-xgboost`

### Local setup

```bash
cd logBERT_XGBoost-BGL-loghub/fast-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Usage

POST `http://localhost:8000/predict`

```json
{
  "log_sequence": [
    "2025-05-17 10:24:00 ERROR MPI_FAIL rank=8 node=compute-2",
    "2025-05-17 10:24:01 WARNING retrying communication channel",
    "2025-05-17 10:24:02 FATAL link timeout exceeded"
  ]
}
```

Response:

```json
{
  "prediction": "network_timeout",
  "cleaned_logs": ["ERROR MPI_FAIL rank=8 node=compute-2", "WARNING retrying communication channel", "FATAL link timeout exceeded"]
}
```

## Project-wide Python Environment

Install the consolidated dependencies at repo root:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Contributors

- Nishant V H
- Sridula O S

## Acknowledgements & Data Sources

- Loghub datasets (Windows, BGL, etc.)
- PSM: `https://www.kaggle.com/datasets/ljolm08/pooled-server-metrics-psm`
- Backblaze Drive Stats and quarterly AFR snapshots: see `https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data`

If you use Backblaze data, please cite Backblaze as the source per their dataset terms.

## Citation (Loghub)

```
@inproceedings{zhu2023loghub,
  title={Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics},
  author={Zhu, Jieming and He, Shilin and He, Pinjia and Liu, Jinyang and Lyu, Michael R},
  booktitle={IEEE International Symposium on Software Reliability Engineering (ISSRE)},
  year={2023}
}
```

## License

Research/educational use. Respect licenses and terms of the underlying datasets and models.
