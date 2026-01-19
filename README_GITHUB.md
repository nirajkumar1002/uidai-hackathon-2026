# 🏆 UIDAI Aadhaar Data Hackathon 2026
## Two-Tiered Aadhaar: How Regional Gaps Create Digital Inequality

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📊 Project Overview

**Analysis of 3.4 Million Aadhaar Records** revealing three interconnected crises in India's digital identity system:

1. **🔴 Biometric Compliance Crisis** - 38.6x variance across states (0.48x → 39.07x)
2. **🔴 Geographic Digital Divide** - Top 5 states control 55.3% of enrollments
3. **🔴 Urban-Rural Coverage Gap** - 205.5x per-capita disparity

**Key Insight:** Universal enrollment ≠ Universal access. WHERE you live determines WHETHER you can access government benefits.

---

## 🚀 Live Dashboard

**[→ View Interactive Dashboard](https://share.streamlit.io/)** *(Update with your deployed URL)*

---

## 📈 Key Findings

### Problem #1: Biometric Compliance Crisis
- **Best State:** Andaman & Nicobar Islands (39.07x compliance)
- **Worst State:** Meghalaya (0.48x compliance)
- **Gap:** 38.59x difference
- **Impact:** 15-20M children can't authenticate for benefits

### Problem #2: Geographic Concentration
- **Top 5 States:** 55.3% of all enrollments
- **Top 10 States:** Control 70%+ of resources
- **Disparity:** 205.5x between highest and lowest states per capita

### Problem #3: Urban-Rural Divide
- **Urban Districts (Top 50):** 26.3% of coverage
- **Rural Districts (900+):** 73.7% with minimal resources
- **Impact:** 600M+ rural residents underserved

---

## 🔧 Technology Stack

- **Data Processing:** Pandas, NumPy, Polars
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Dashboard:** Streamlit
- **Analysis:** Jupyter Notebooks, SciPy, Scikit-learn
- **Data Volume:** 3.4M records (deduplicated from 4.9M raw)

---

## 📁 Project Structure

```
uidai-hackathon-2026/
├── dashboard/
│   └── app.py                    # Streamlit dashboard (main entry point)
├── notebooks/
│   ├── 01_initial_exploration.ipynb
│   └── 02_deep_dive_three_problems.ipynb  # Complete analysis
├── data/
│   └── raw/                      # 12 CSV files (3 datasets)
├── src/
│   ├── data_loader.py            # Data loading & deduplication
│   ├── visualization_utils.py    # Chart generation
│   └── automated_eda.py          # EDA automation
├── outputs/
│   ├── figures/                  # 15 interactive HTML charts
│   └── reports/                  # Analysis reports & narrative
└── requirements.txt              # Python dependencies
```

---

## 🎯 Installation & Usage

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/uidai-hackathon-2026.git
cd uidai-hackathon-2026
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Dashboard
```bash
streamlit run dashboard/app.py
```

### 4. Explore Notebooks
```bash
jupyter notebook notebooks/02_deep_dive_three_problems.ipynb
```

---

## 📊 Visualizations

| Chart | Description | Key Insight |
|-------|-------------|-------------|
| State Compliance Heatmap | Biometric update rates by state | 38x variance |
| Geographic Concentration | Top 5 vs Rest of India | 55.3% concentration |
| Urban-Rural Split | Metro vs Village enrollment | 205x disparity |
| Per-Capita Analysis | Fairness across states | Massive inequality |
| District Rankings | Best/worst performers | Clear outliers |

---

## 🎓 Methodology

### Data Cleaning
- **Deduplication:** 31.18% duplicates removed (batch artifacts)
- **State Standardization:** Fixed case/spacing inconsistencies (e.g., "West Bangal" → "West Bengal")
- **Invalid Removal:** Filtered non-alphabetic state names

### Analysis Approach
1. **State-Level Aggregation:** Compliance ratios, enrollment volumes
2. **District-Level Analysis:** Urban/rural classification, outlier detection
3. **Per-Capita Normalization:** Fair comparison across states
4. **Cross-Dataset Correlation:** Enrollment vs biometric updates

---

## 💡 Policy Recommendations

### Immediate Actions (6 months)
- **Biometric Compliance Drives** in bottom 10% states (Meghalaya, Nagaland, Assam)
- **Mobile Enrollment Units** for underserved districts
- **Awareness Campaigns** in vernacular languages

### Medium-Term Goals (18 months)
- **Per-Capita Equity Targets:** Reduce disparity from 205x → 2x
- **Rural Infrastructure:** 500+ new enrollment centers
- **Compliance Tracking:** Real-time monitoring dashboard

### Success Metrics
- Compliance gap: 0.48x → 1.1x (all states)
- Geographic disparity: 205x → 1.5x
- Urban-rural gap: Close to 1.2x

---

## 📝 Citation

If you use this analysis, please cite:

```
UIDAI Aadhaar Hackathon 2026 - Two-Tiered Digital Identity Analysis
Author: [Your Name]
Repository: https://github.com/YOUR_USERNAME/uidai-hackathon-2026
Date: January 2026
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👤 Author

**[Your Name]**
- Email: yesiamniraj@gmail.com
- Hackathon: UIDAI Data Challenge 2026

---

## 🙏 Acknowledgments

- UIDAI for providing comprehensive Aadhaar datasets
- Hackathon organizers for the opportunity
- Open-source community for amazing tools (Streamlit, Plotly, Pandas)

---

## 📫 Contact

For questions or collaboration opportunities:
- **Email:** yesiamniraj@gmail.com
- **Dashboard:** [Live Demo Link]
- **Presentation:** [Google Slides/PDF Link]

---

**⭐ Star this repo if you find it useful!**
