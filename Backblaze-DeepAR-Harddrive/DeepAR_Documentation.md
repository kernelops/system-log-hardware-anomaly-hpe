# Backblaze DeepAR Failure Forecasting - Technical Report

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Data Pipeline](#data-pipeline)
4. [Model Development](#model-development)
5. [Accuracy Results](#accuracy-results)
6. [Performance Metrics](#performance-metrics)
7. [Usage Instructions](#usage-instructions)
8. [Technical Implementation](#technical-implementation)
9. [Recommendations](#recommendations)
10. [Appendices](#appendices)

---

## 1. Project Overview

### Objective
Develop a time-series forecasting system using DeepAR to predict hard drive failures in Backblaze's fleet, enabling proactive maintenance and reducing data loss.

### Dataset
- **Source**: Backblaze Hard Drive Statistics (Drive Stats)
- **Period**: Focused training and analysis on Q1 2025
- **Access**: https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data
- **Target**: Daily failure rates per drive model

### Key Achievements
- ✅ Built end-to-end forecasting pipeline
- ✅ Implemented proper time-series validation with backtesting
- ✅ Created production-ready CLI tools
- ✅ Evaluated dynamic features (active drive counts)

---

## 2. System Architecture

### Components
```
Raw Data (Backblaze CSVs) → Data Preparation → Model Training → Prediction → Evaluation
```

### File Structure
```
<root>/Backblaze-DeepAR-Harddrive/
├── backblaze-2025-q1-deepar.ipynb
├── processed/             # Per-model time series
├── deepar_predictor*/     # Trained models
├── forecasts/             # Prediction outputs
├── prepare_blackbalze.py  # Data preparation
├── deepar_train.py        # Model training
├── deepar_predict.py      # Prediction generation
└── deepar_backtest.py     # Model validation
```

---

## 3. Data Pipeline

### 3.1 Data Preparation (`prepare_blackbalze.py`)

**Input**: Daily Backblaze CSV files with columns:
- `date`, `model`, `serial_number`, `failure`, `capacity_bytes`, `temperature`, `power_on_hours`

**Process**:
1. Load and harmonize columns across quarters
2. Group by model and date
3. Aggregate statistics:
   - `active_drives`: Count of unique drives per model per day
   - `failure`: Sum of failures per model per day
   - `failure_rate`: failures / active_drives
   - `temperature`, `power_on_hours`: Mean values

**Output**: Per-model CSV files in `processed/` folder

**Usage**:
```bash
python prepare_blackbalze.py --input-dirs data_Q1_2025 --out-dir processed
```

### 3.2 Data Statistics

- Target period: Q1 2025
- Rare event setting: most days have zero failures

---

## 4. Model Development

### 4.1 DeepAR Configuration

**Base Architecture**:
- **Framework**: GluonTS with PyTorch backend
- **Model**: DeepAR (Deep Autoregressive)
- **Frequency**: Daily ('D')
- **Prediction horizon**: 7 days
- **Context length**: 14–21 days

**Typical Hyperparameters**:
- Hidden size: 40–64
- RNN layers: 2–3
- Dropout: 0.1
- Batch size: 32
- Training epochs: 5–10

### 4.2 Features

- Static: model identifier (categorical encoding)
- Dynamic: `active_drives` (normalized), optionally temperature trends, device age, SMART summaries

---

## 5. Accuracy Results

### 5.1 Backtesting Methodology

- Time-series cross-validation: hold out last 7 days per series
- Forecast last 7 days; compute MAE, MAPE, sMAPE

### 5.2 Detailed Results (Illustrative)

- Models show conservative predictions under rare-event regimes; consider p90 for planning

---

## 6. Performance Metrics

- MAE: mean absolute error on failure_rate
- MAPE/sMAPE: percentage metrics; sMAPE more stable when near zero

---

## 7. Usage Instructions (Local)

### 7.1 Environment Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 7.2 Workflow

#### Step 1: Data Preparation
```bash
python prepare_blackbalze.py \
  --input-dirs data_Q1_2025 \
  --out-dir processed
```

#### Step 2: Model Training (Example Configuration)
```bash
python deepar_train.py \
  --processed-dir processed \
  --output-dir deepar_predictor_best \
  --use-dynamic-feat \
  --hidden-size 64 \
  --num-layers 3 \
  --max-epochs 10 \
  --prediction-length 7 \
  --context-length 21
```

#### Step 3: Generate Forecasts
```bash
python deepar_predict.py \
  --predictor-dir deepar_predictor_best \
  --processed-dir processed \
  --all \
  --out forecasts
```

#### Step 4: Model Validation
```bash
python deepar_backtest.py \
  --use-dynamic-feat \
  --hidden-size 64 \
  --num-layers 3 \
  --epochs 5 \
  --output backtest_results.csv
```

---

## 8. Technical Implementation

- DeepAR with probabilistic outputs; global model across items (drive models)
- Dataset creation via `ListDataset`; dynamic features normalization
- Early stopping, dropout, gradient clipping for stability

---

## 9. Recommendations

- Use p90 forecasts for conservative capacity and risk planning
- Retrain monthly with rolling 12-month window as data grows
- Add device age and SMART attribute trends as dynamic covariates
- Consider survival analysis or binary classification as complementary signals

---

## 10. Appendices

- CLI references: `prepare_blackbalze.py`, `deepar_train.py`, `deepar_predict.py`, `deepar_backtest.py`
- Example outputs: forecast CSVs and backtest metrics

---

**Document Version**: 1.0  
**Last Updated**: September 17, 2025  
**Contact**: HPE CPP-2 Project Team