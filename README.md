# Real-time Network Intrusion Detection System (IDS) using Machine Learning

This project implements a high-performance, scalable Machine Learning-based Network Intrusion Detection System (IDS) using the **CIC-IDS2017** dataset. It is optimized to handle large-scale datasets (~2.5 million rows) on standard consumer hardware (approx. 32GB RAM, no GPU required).

## ✨ Key Features
- **Scalability**: Designed for 2.5M+ rows without memory crashes.
- **Robust Preprocessing**: Encoding-aware label cleaning (handles corrupted `\ufffd` characters and standardizes complex labels like "Web Attack").
- **Resource Optimized**: Numerical downcasting to `float32` and single-threaded tuning to prevent CPU overheating and RAM explosion.
- **Production-Lite Simulation**: Generates Suricata-style logs and structured JSON outputs for easy integration with SIEM tools.

## 📁 Project Structure

```text
├── datasets/                   # Raw CSV files and cleaned Parquet data
├── models/                     # Trained pipelines (.pkl), scalers, and encoders
├── result/                     # JSON outputs from simulation tests
├── notebooks/                  # Main Pipeline Notebooks
│   ├── 01_Data_Prep_and_EDA.ipynb
│   ├── 02_Feature_Engineering_and_Modeling.ipynb
│   └── 03_Simulation_and_Deployment.ipynb
├── requirements.txt            # Required Python libraries
├── alerts.log                  # Raw text logs (ANSI/UTF-8)
└── README.md                   # Project documentation
```

## 🚀 Setup Instructions

### 1. Prerequisites
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

### 2. Dataset Setup
Download the **CIC-IDS2017** dataset and place the 8 raw `.csv` files into the `datasets/` folder. The notebooks strictly enforce UTF-8/Latin1 handling to ensure cross-platform compatibility.

## 🛠️ Usage Pipeline

### Step 1: Data Preparation & Memory Optimization
Run `01_Data_Prep_and_EDA.ipynb` to:
- Merge raw CSVs and optimize memory (float64 -> float32).
- **Sanitize Labels**: Strip non-ASCII characters and standardize "Web Attack" naming conventions.
- Export to **Parquet** for 10x faster loading in subsequent steps.

### Step 2: Scalable Feature Engineering & Modeling
Run `02_Feature_Engineering_and_Modeling.ipynb` to:
- **Tuning Strategy**: Perform `RandomizedSearchCV` on a stratified sample (150k rows) to find optimal hyperparameters efficiently.
- **Final Training**: Automatically retrain the best model (Random Forest, Logistic Regression, or Naive Bayes) on the **FULL** training set (2M+ rows).
- **Pipeline Preservation**: Save the entire preprocessing + model stack as a single artifact.

### Step 3: Real-time Simulation & SIEM-Ready Output
Run `03_Simulation_and_Deployment.ipynb` to:
- Simulate network traffic with 50/50 Benign/Attack samples.
- **Suricata-Style Logs**: Generate readable alerts including Destination Port information.
- **JSON Output**: Save structured `simulation_output.json` including True Label, Log Message, and Match Status (`success`/`FAILURE`).

## 📊 Resource Management
| Resource | Optimization |
| :--- | :--- |
| **RAM** | Optimized to fit ~2.5M rows in < 32GB RAM via downcasting. |
| **CPU** | Hyperparameter tuning restricted to `n_jobs=1` to prevent overheating. |
| **Encoding** | Strictly enforced `UTF-8` for all file I/O to prevent `charmap` codec crashes. |

## ⚖️ License
This project is for educational purposes.
