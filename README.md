# UIDAI Aadhaar Data Analysis: Digital Identity Inequality

**Three-Problem Analysis of 3.4M+ Aadhaar Records**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Project Overview

This analysis reveals **three interconnected crises** in India's universal Aadhaar enrollment system that create a two-tiered digital identity access system:

### The Three Problems

1. **Biometric Compliance Crisis**
   - Mandatory updates at ages 5 & 15 show 38.6x variance across states
   - Range: 0.48x to 39.07x compliance ratio
   - 15-20 million children unable to authenticate for benefits

2. **Geographic Digital Divide**
   - Top 5 states control 55.3% of all enrollments
   - Per-capita disparity: 205.5x between highest and lowest states
   - Northeastern regions severely underserved

3. **Urban-Rural Coverage Gap**
   - Top 50 urban districts: 26.3% of infrastructure
   - 900+ rural districts: 73.7% with minimal resources
   - 600+ million rural residents underserved

### Key Insight
Universal enrollment (96.4% children) masks systematic inequality. **WHERE you live determines WHETHER you access government benefits.**

---

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd data_hackathon_26
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data placement:**
   ```
   data/raw/
   ├── enrolment/              (3 CSV files)
   ├── demographic_update/     (6 CSV files)
   └── biometric_update/       (4 CSV files)
   ```

### Running the Analysis

**Step 1: Interactive Dashboard (Recommended)**
```bash
streamlit run dashboard/app.py
```
Opens at `http://localhost:8501` with 6 interactive analysis pages

**Step 2: Jupyter Notebooks**
```bash
jupyter notebook notebooks/02_deep_dive_three_problems.ipynb
```
Complete analysis with code, visualizations, and detailed findings

**Step 3: Automated EDA (Optional)**
```bash
python src/automated_eda.py
```
Generates exploratory data analysis report

---

## Interactive Dashboard

**[→ View Dashboard](#)** *(Deploy URL to be added)*

### Dashboard Pages:
1. **Overview** - Problem narrative & key statistics
2. **Problem #1** - Biometric compliance analysis by state
3. **Problem #2** - Geographic concentration patterns  
4. **Problem #3** - Urban-rural coverage disparities
5. **Advanced Analytics** - Statistical validation, clustering, regression
6. **Synthesis** - Policy recommendations & implementation roadmap

---

## Project Structure

```
data_hackathon_26/
├── dashboard/
│   └── app.py                          # Streamlit app (main entry point)
├── notebooks/
│   ├── 01_initial_exploration.ipynb    # Basic EDA
│   ├── 02_deep_dive_three_problems.ipynb  # Main analysis
│   └── 03_advanced_analytics.ipynb     # Statistical validation
├── data/raw/
│   ├── enrolment/                      # 3 enrollment CSV files
│   ├── demographic_update/             # 6 demographic CSV files
│   └── biometric_update/               # 4 biometric CSV files
├── src/
│   ├── data_loader.py                  # Data loading & cleaning
│   ├── visualization_utils.py          # Chart generation
│   ├── eda_utils.py                    # EDA utilities
│   └── automated_eda.py                # Automated analysis
├── outputs/
│   ├── figures/                        # Generated visualizations (15 charts)
│   └── reports/                        # Analysis reports & findings
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── METHODOLOGY.md                      # Detailed methodology & approach
```

---

## Citation

If you use this analysis in your work, please cite:

```bibtex
@project{uidai2026,
  title={UIDAI Aadhaar Data Analysis: Digital Identity Inequality},
  author={Niraj kumar},
  year={2026},
  url={https://github.com/nirajkumar1002/data_hackathon_26}
}
```

---

## License

MIT License - See LICENSE file for details
