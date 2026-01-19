"""
EDA (Exploratory Data Analysis) Utilities
Functions to quickly analyze and summarize datasets
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class EDAAnalyzer:
    """Automated EDA tools for quick insights"""
    
    def __init__(self, df, dataset_name="Dataset"):
        self.df = df
        self.name = dataset_name
        self.insights = []
        
    def basic_info(self):
        """Print basic dataset information"""
        print(f"\n{'='*60}")
        print(f"📊 BASIC INFO - {self.name}")
        print(f"{'='*60}")
        print(f"Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        print(f"Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"\nColumns: {list(self.df.columns)}")
        print(f"\nData types:\n{self.df.dtypes}")
        
    def missing_data_analysis(self):
        """Analyze missing data"""
        print(f"\n{'='*60}")
        print(f"❓ MISSING DATA ANALYSIS - {self.name}")
        print(f"{'='*60}")
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_pct.values
        })
        
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        
        if len(missing_df) == 0:
            print("✅ No missing values found!")
        else:
            print(missing_df.to_string(index=False))
            self.insights.append(f"Missing data in {len(missing_df)} columns")
        
        return missing_df
    
    def numeric_summary(self):
        """Summary statistics for numeric columns"""
        print(f"\n{'='*60}")
        print(f"🔢 NUMERIC SUMMARY - {self.name}")
        print(f"{'='*60}")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("No numeric columns found.")
            return
        
        print(self.df[numeric_cols].describe())
        
        # Check for zeros
        for col in numeric_cols:
            zero_count = (self.df[col] == 0).sum()
            zero_pct = (zero_count / len(self.df)) * 100
            if zero_pct > 50:
                print(f"\n⚠️ {col}: {zero_pct:.1f}% zeros!")
                self.insights.append(f"{col} has {zero_pct:.1f}% zeros")
    
    def categorical_summary(self):
        """Summary for categorical columns"""
        print(f"\n{'='*60}")
        print(f"📋 CATEGORICAL SUMMARY - {self.name}")
        print(f"{'='*60}")
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col != 'date':  # Skip date column
                print(f"\n{col.upper()}:")
                print(f"  Unique values: {self.df[col].nunique()}")
                print(f"  Most common:")
                print(self.df[col].value_counts().head().to_string())
    
    def temporal_analysis(self, date_col='date'):
        """Analyze temporal patterns"""
        if date_col not in self.df.columns:
            return
        
        print(f"\n{'='*60}")
        print(f"📅 TEMPORAL ANALYSIS - {self.name}")
        print(f"{'='*60}")
        
        self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')
        
        print(f"Date range: {self.df[date_col].min()} to {self.df[date_col].max()}")
        print(f"Total days: {(self.df[date_col].max() - self.df[date_col].min()).days}")
        
        # Check for gaps
        date_counts = self.df[date_col].value_counts().sort_index()
        date_range = pd.date_range(start=self.df[date_col].min(), 
                                   end=self.df[date_col].max(), 
                                   freq='D')
        missing_dates = set(date_range) - set(date_counts.index)
        
        if missing_dates:
            print(f"\n⚠️ Missing dates: {len(missing_dates)} days")
            self.insights.append(f"Missing {len(missing_dates)} dates in time series")
    
    def detect_outliers(self, numeric_cols=None):
        """Detect outliers using IQR method"""
        print(f"\n{'='*60}")
        print(f"🎯 OUTLIER DETECTION - {self.name}")
        print(f"{'='*60}")
        
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outlier_pct = (len(outliers) / len(self.df)) * 100
            
            if outlier_pct > 0:
                print(f"{col}: {len(outliers):,} outliers ({outlier_pct:.2f}%)")
                print(f"  Range: [{self.df[col].min()}, {self.df[col].max()}]")
                print(f"  Outlier bounds: < {lower_bound:.2f} or > {upper_bound:.2f}")
    
    def geographic_coverage(self):
        """Analyze geographic coverage"""
        print(f"\n{'='*60}")
        print(f"🗺️ GEOGRAPHIC COVERAGE - {self.name}")
        print(f"{'='*60}")
        
        if 'state' in self.df.columns:
            print(f"States: {self.df['state'].nunique()}")
            print(f"\nTop 10 states by record count:")
            print(self.df['state'].value_counts().head(10).to_string())
        
        if 'district' in self.df.columns:
            print(f"\nDistricts: {self.df['district'].nunique()}")
            
        if 'pincode' in self.df.columns:
            print(f"Pincodes: {self.df['pincode'].nunique()}")
            
            # Check for invalid pincodes
            invalid_pins = self.df[self.df['pincode'].astype(str).str.len() != 6]
            if len(invalid_pins) > 0:
                print(f"\n⚠️ Invalid pincodes: {len(invalid_pins):,} records")
    
    def age_distribution_analysis(self):
        """Analyze age group distributions"""
        age_cols = [col for col in self.df.columns if 'age' in col.lower()]
        
        if not age_cols:
            return
        
        print(f"\n{'='*60}")
        print(f"👥 AGE DISTRIBUTION - {self.name}")
        print(f"{'='*60}")
        
        for col in age_cols:
            total = self.df[col].sum()
            print(f"{col}: {total:,} ({(total / self.df[age_cols].sum().sum() * 100):.1f}% of total)")
    
    def correlation_analysis(self):
        """Analyze correlations between numeric columns"""
        print(f"\n{'='*60}")
        print(f"🔗 CORRELATION ANALYSIS - {self.name}")
        print(f"{'='*60}")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("Not enough numeric columns for correlation.")
            return
        
        corr_matrix = self.df[numeric_cols].corr()
        
        # Find high correlations (excluding self-correlation)
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.7:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_matrix.iloc[i, j]
                    ))
        
        if high_corr:
            print("High correlations found (|r| > 0.7):")
            for col1, col2, corr_val in high_corr:
                print(f"  {col1} ↔ {col2}: {corr_val:.3f}")
        else:
            print("No high correlations found.")
    
    def generate_insights_report(self):
        """Generate a summary of key insights"""
        print(f"\n{'='*60}")
        print(f"💡 KEY INSIGHTS - {self.name}")
        print(f"{'='*60}")
        
        if self.insights:
            for i, insight in enumerate(self.insights, 1):
                print(f"{i}. {insight}")
        else:
            print("Run analysis methods first to generate insights.")
    
    def run_full_eda(self):
        """Run all EDA methods"""
        self.basic_info()
        self.missing_data_analysis()
        self.numeric_summary()
        self.categorical_summary()
        self.temporal_analysis()
        self.geographic_coverage()
        self.age_distribution_analysis()
        self.detect_outliers()
        self.correlation_analysis()
        self.generate_insights_report()


def quick_eda(df, name="Dataset"):
    """Quick function to run full EDA"""
    analyzer = EDAAnalyzer(df, name)
    analyzer.run_full_eda()
    return analyzer


if __name__ == "__main__":
    print("✅ EDA utilities loaded successfully!")
