# 🚀 QUICK START GUIDE - UIDAI Hackathon

## ⚡ Get Started in 3 Steps:

### Step 1: Setup Environment (First Time Only)
```bash
cd c:\Users\Niraj\Desktop\code\data_hackathon_26
python src/setup.py
```

### Step 2: Place Your CSV Files
```
data/raw/enrolment/         ← Put 3 enrollment CSV files here
data/raw/demographic_update/ ← Put 6 demographic CSV files here  
data/raw/biometric_update/   ← Put 4 biometric CSV files here
```

### Step 3: Run Analysis
```bash
# Option A: Automated EDA (recommended first)
python src/automated_eda.py

# Option B: Interactive Jupyter Notebook
jupyter notebook notebooks/01_initial_exploration.ipynb
```

---

## 📚 What Each Tool Does:

### `src/data_loader.py`
- Automatically loads all 13 CSV files
- Combines them into 3 dataframes
- Shows summary statistics

### `src/eda_utils.py`
- Automated exploratory data analysis
- Missing data detection
- Outlier identification
- Correlation analysis
- Geographic coverage analysis

### `src/visualization_utils.py`
- Time series plots
- State/district comparisons
- Heatmaps
- Age distribution charts
- Interactive Plotly visualizations

### `src/automated_eda.py`
- Runs complete analysis pipeline
- Generates all visualizations
- Creates summary reports
- Saves everything to outputs/

---

## 🎯 Analysis Workflow:

```
1. Run automated_eda.py
   ↓
2. Review generated charts in outputs/figures/
   ↓
3. Identify 5-6 interesting patterns
   ↓
4. Open Jupyter notebook for deep dive
   ↓
5. Formulate specific problem statements
   ↓
6. Build focused analysis + dashboard
```

---

## 💡 Pro Tips:

1. **Start Broad**: Let automated_eda.py run first - it shows you everything
2. **Look for Anomalies**: Spikes, drops, outliers = interesting stories
3. **Compare Datasets**: Enrollment vs Updates = policy compliance insights
4. **Geographic Patterns**: Urban vs rural, state disparities
5. **Temporal Patterns**: Seasonality, trends, before/after events

---

## 🔥 Winning Features We Built:

✅ **Automated EDA** - Saves hours of manual exploration  
✅ **Interactive Visualizations** - Plotly charts judges can interact with  
✅ **Reusable Functions** - Easy to try different analyses  
✅ **Professional Structure** - Shows software engineering skills  
✅ **Comprehensive Documentation** - Easy for judges to understand  

---

## 📊 Expected Outputs:

After running `automated_eda.py`:
- `outputs/figures/*.html` - Interactive charts
- `outputs/reports/eda_report_*.txt` - Text summary

After Jupyter analysis:
- Custom visualizations
- Statistical test results
- Model outputs

---

## 🆘 Troubleshooting:

**Issue:** "No data loaded"  
**Fix:** Make sure CSV files are in correct data/raw/ folders

**Issue:** Package import errors  
**Fix:** Run `python src/setup.py` again

**Issue:** Charts not displaying in Jupyter  
**Fix:** Restart kernel and run all cells

---

## 🎓 Remember:

- **Exploration first, then focus**
- **Let data tell the story**
- **2-3 deep insights > 10 shallow ones**
- **Actionable recommendations = win**

---

Ready to discover insights! 🔍
