"""
Automated EDA Script - Run this to get comprehensive analysis of all datasets
Generates reports and visualizations automatically

Usage: python automated_eda.py
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent))

from data_loader import DataLoader
from eda_utils import EDAAnalyzer
from visualization_utils import VisualizationTools, save_figure

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print(" UIDAI HACKATHON - AUTOMATED EDA")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Load all data
    print("STEP 1: Loading Data...")
    print("-"*80)
    loader = DataLoader()
    datasets = loader.load_all_data()
    
    if all(df is None for df in datasets.values()):
        print("\n No data loaded! Please place CSV files in the data/raw folders.")
        print("\nExpected structure:")
        print("  data/raw/enrolment/       - 3 CSV files")
        print("  data/raw/demographic_update/ - 6 CSV files")
        print("  data/raw/biometric_update/   - 4 CSV files")
        return
    
    loader.get_summary_stats(datasets)
    
    # Step 2: Run EDA on each dataset
    print("\n\nSTEP 2: Running Exploratory Data Analysis...")
    print("-"*80)
    
    analyzers = {}
    
    for name, df in datasets.items():
        if df is not None:
            print(f"\n{'='*80}")
            print(f"Analyzing: {name.upper()}")
            print(f"{'='*80}")
            analyzer = EDAAnalyzer(df, name)
            analyzer.run_full_eda()
            analyzers[name] = analyzer
    
    # Step 3: Generate visualizations
    print("\n\nSTEP 3: Generating Visualizations...")
    print("-"*80)
    
    viz = VisualizationTools()
    
    for name, df in datasets.items():
        if df is not None and 'date' in df.columns:
            print(f"\nGenerating charts for {name}...")
            
            # Calculate total enrollments/updates per day
            numeric_cols = [col for col in df.columns if col not in ['date', 'state', 'district', 'pincode']]
            df['total'] = df[numeric_cols].sum(axis=1)
            
            # Time series plot
            daily_totals = df.groupby('date')['total'].sum().reset_index()
            fig = viz.plot_time_series(daily_totals, 'date', ['total'], 
                                       title=f'{name.title()} - Daily Trend')
            save_figure(fig, f'{name}_daily_trend')
            print(f"   Daily trend chart saved")
            
            # State comparison
            if 'state' in df.columns:
                fig = viz.plot_state_comparison(df, 'state', 'total')
                save_figure(fig, f'{name}_state_comparison')
                print(f"   State comparison chart saved")
            
            # Age distribution
            age_cols = [col for col in df.columns if 'age' in col.lower()]
            if age_cols:
                fig = viz.plot_age_distribution(df, age_cols, 
                                               title=f'{name.title()} - Age Distribution')
                save_figure(fig, f'{name}_age_distribution')
                print(f"   Age distribution chart saved")
    
    # Step 4: Generate summary report
    print("\n\nSTEP 4: Generating Summary Report...")
    print("-"*80)
    
    report_path = Path('../outputs/reports')
    report_path.mkdir(parents=True, exist_ok=True)
    
    report_file = report_path / f'eda_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("UIDAI DATA HACKATHON - AUTOMATED EDA REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for name, df in datasets.items():
            if df is not None:
                f.write(f"\n{'='*80}\n")
                f.write(f"{name.upper()} DATASET\n")
                f.write(f"{'='*80}\n")
                f.write(f"Total Records: {len(df):,}\n")
                f.write(f"Date Range: {df['date'].min()} to {df['date'].max()}\n")
                f.write(f"Unique States: {df['state'].nunique()}\n")
                f.write(f"Unique Districts: {df['district'].nunique()}\n")
                f.write(f"Unique Pincodes: {df['pincode'].nunique()}\n")
                
                if name in analyzers:
                    f.write(f"\nKey Insights:\n")
                    for i, insight in enumerate(analyzers[name].insights, 1):
                        f.write(f"  {i}. {insight}\n")
    
    print(f"\n Report saved: {report_file}")
    
    # Step 5: Next steps recommendations
    print("\n\n" + "="*80)
    print(" AUTOMATED EDA COMPLETE!")
    print("="*80)
    
    print("\n Generated Files:")
    print(f"   Visualizations: outputs/figures/")
    print(f"   Report: {report_file}")
    
    print("\n RECOMMENDED NEXT STEPS:")
    print("\n1. REVIEW VISUALIZATIONS")
    print("   - Open the HTML files in outputs/figures/")
    print("   - Look for unusual patterns, spikes, or anomalies")
    
    print("\n2. IDENTIFY INTERESTING PATTERNS")
    print("   - Which states show unusual trends?")
    print("   - Are there seasonal patterns?")
    print("   - Do age groups behave differently?")
    
    print("\n3. FORMULATE PROBLEM STATEMENTS")
    print("   - Based on patterns found, define 2-3 specific questions")
    print("   - Focus on policy-relevant, actionable insights")
    
    print("\n4. DEEP DIVE ANALYSIS")
    print("   - Open notebooks/01_initial_exploration.ipynb")
    print("   - Conduct statistical tests on your hypotheses")
    print("   - Build predictive models if applicable")
    
    print("\n5. BUILD DASHBOARD")
    print("   - Create interactive Streamlit app")
    print("   - Present findings in a compelling way")
    
    print("\n" + "="*80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
