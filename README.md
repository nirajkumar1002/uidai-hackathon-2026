# UIDAI Data Hackathon 2026 - Analysis Project

## 🎯 Objective
Analyze Aadhaar enrollment and update datasets to derive meaningful insights and policy recommendations.

## 📁 Project Structure
```
data_hackathon_26/
├── data/
│   ├── raw/                    # Original CSV files
│   │   ├── enrolment/         # 3 enrollment CSV files
│   │   ├── demographic_update/ # 6 demographic update CSV files
│   │   └── biometric_update/   # 4 biometric update CSV files
│   └── processed/              # Cleaned and merged datasets
├── notebooks/                  # Jupyter notebooks for analysis
├── src/                        # Python scripts and utilities
├── outputs/
│   ├── figures/               # Generated visualizations
│   └── reports/               # Analysis reports
└── dashboard/                  # Streamlit dashboard files
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your CSV files:**
   - Enrolment CSVs → `data/raw/enrolment/`
   - Demographic update CSVs → `data/raw/demographic_update/`
   - Biometric update CSVs → `data/raw/biometric_update/`

3. **Run initial exploration:**
   ```bash
   jupyter notebook notebooks/01_initial_exploration.ipynb
   ```

4. **Generate automated EDA:**
   ```bash
   python src/automated_eda.py
   ```

## 📊 Datasets

### 1. Aadhaar Enrolment (3 files)
**Columns:** date, state, district, pincode, age_0_5, age_5_17, age_18_greater

### 2. Demographic Update (6 files)
**Columns:** date, state, district, pincode, demo_age_5_17, demo_age_17_

### 3. Biometric Update (4 files)
**Columns:** date, state, district, pincode, bio_age_5_17, bio_age_17_

## 🔍 Analysis Approach
1. Exploration-first approach to discover patterns
2. Formulate problem statements based on findings
3. Deep dive analysis on selected problems
4. Build interactive dashboard for insights

## 📈 Key Analysis Areas
- Temporal trends and seasonality
- Geographic disparities
- Age group patterns
- Cross-dataset correlations
- Anomaly detection
- Predictive modeling
