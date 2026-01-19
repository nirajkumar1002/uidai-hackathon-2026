# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "UIDAI Hackathon - Three-Problem Analysis Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/uidai-hackathon-2026.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your GitHub repository
4. Set:
   - **Main file path:** `dashboard/app.py`
   - **Python version:** 3.12
5. Click "Deploy"

### 3. Share Your Dashboard

Your dashboard will be live at:
`https://share.streamlit.io/YOUR_USERNAME/uidai-hackathon-2026/main/dashboard/app.py`

---

## Alternative: Manual Deployment Commands

If you prefer command line:

```bash
# Install Streamlit Cloud CLI
pip install streamlit

# Login to Streamlit Cloud
streamlit config show

# Deploy
streamlit run dashboard/app.py --server.port 8501
```

---

## What Judges Will See

✅ Interactive dashboard with 4 pages:
- Overview with key findings
- Problem #1: Biometric Compliance Analysis
- Problem #3: Geographic Digital Divide
- Problem #4: Urban-Rural Coverage Disparity

✅ Live data exploration with:
- State selector
- Interactive charts
- Real-time metrics
- Policy recommendations

---

## Troubleshooting

**If deployment fails:**
1. Check requirements.txt has all dependencies
2. Ensure data files are included in repo
3. Verify app.py runs locally first
4. Check Streamlit Cloud logs for errors

**Data too large?**
If data/ folder exceeds GitHub limits:
- Use Git LFS for large files
- Or host data separately (Google Drive, S3)
- Update data_loader.py to fetch from URL
