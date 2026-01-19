"""
Data Loading Utilities for UIDAI Hackathon
Automatically loads and combines all CSV files from the three datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Load and preprocess UIDAI datasets"""
    
    def __init__(self, data_dir='../data/raw'):
        self.data_dir = Path(data_dir)
        self.enrolment_dir = self.data_dir / 'enrolment'
        self.demographic_dir = self.data_dir / 'demographic_update'
        self.biometric_dir = self.data_dir / 'biometric_update'
        
    def load_enrolment_data(self):
        """Load all enrolment CSV files and combine them"""
        print("Loading Enrolment Data...")
        
        csv_files = list(self.enrolment_dir.glob('*.csv'))
        print(f"   Found {len(csv_files)} CSV files")
        
        if not csv_files:
            print("   ⚠️ No CSV files found in enrolment folder!")
            return None
        
        dfs = []
        for file in csv_files:
            print(f"   Loading {file.name}...")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        records_before_dedup = len(combined)
        
        # Convert date column to datetime
        combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
        
        # Basic cleaning - track duplicates
        duplicates_found = combined.duplicated().sum()
        combined = combined.drop_duplicates()
        records_after_dedup = len(combined)
        
        print(f"   Records before dedup: {records_before_dedup:,}")
        print(f"   Duplicates found: {duplicates_found:,}")
        print(f"   Records after dedup: {records_after_dedup:,}")
        print(f"   Dedup loss: {(duplicates_found/records_before_dedup)*100:.2f}%")
        print(f"Loaded {len(combined):,} records")
        print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")
        
        return combined
    
    def load_demographic_update_data(self):
        """Load all demographic update CSV files and combine them"""
        print("\n Loading Demographic Update Data...")
        
        csv_files = list(self.demographic_dir.glob('*.csv'))
        print(f"   Found {len(csv_files)} CSV files")
        
        if not csv_files:
            print("   ⚠️ No CSV files found in demographic_update folder!")
            return None
        
        dfs = []
        for file in csv_files:
            print(f"   Loading {file.name}...")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        records_before_dedup = len(combined)
        
        # Convert date column to datetime
        combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
        
        # Basic cleaning - track duplicates
        duplicates_found = combined.duplicated().sum()
        combined = combined.drop_duplicates()
        records_after_dedup = len(combined)
        
        print(f"   Records before dedup: {records_before_dedup:,}")
        print(f"   Duplicates found: {duplicates_found:,}")
        print(f"   Records after dedup: {records_after_dedup:,}")
        print(f"   Dedup loss: {(duplicates_found/records_before_dedup)*100:.2f}%")
        print(f"   Loaded {len(combined):,} records")
        print(f"   Date range: {combined['date'].min()} to {combined['date'].max()}")
        
        return combined
    
    def load_biometric_update_data(self):
        """Load all biometric update CSV files and combine them"""
        print("\n Loading Biometric Update Data...")
        
        csv_files = list(self.biometric_dir.glob('*.csv'))
        print(f"   Found {len(csv_files)} CSV files")
        
        if not csv_files:
            print("   ⚠️ No CSV files found in biometric_update folder!")
            return None
        
        dfs = []
        for file in csv_files:
            print(f"   Loading {file.name}...")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        records_before_dedup = len(combined)
        
        # Convert date column to datetime
        combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
        
        # Basic cleaning - track duplicates
        duplicates_found = combined.duplicated().sum()
        combined = combined.drop_duplicates()
        records_after_dedup = len(combined)
        
        print(f"   Records before dedup: {records_before_dedup:,}")
        print(f"   Duplicates found: {duplicates_found:,}")
        print(f"   Records after dedup: {records_after_dedup:,}")
        print(f"   Dedup loss: {(duplicates_found/records_before_dedup)*100:.2f}%")
        print(f"   Loaded {len(combined):,} records")
        print(f"   Date range: {combined['date'].min()} to {combined['date'].max()}")
        
        return combined
    
    def load_all_data(self):
        """Load all three datasets"""
        print("=" * 60)
        print("UIDAI Data Loader - Loading All Datasets")
        print("=" * 60)
        
        enrolment = self.load_enrolment_data()
        demographic = self.load_demographic_update_data()
        biometric = self.load_biometric_update_data()
        
        print("\n" + "=" * 60)
        print("All Data Loaded Successfully!")
        print("=" * 60)
        
        return {
            'enrolment': enrolment,
            'demographic': demographic,
            'biometric': biometric
        }
    
    def get_summary_stats(self, datasets):
        """Generate quick summary statistics for all datasets"""
        print("\n DATASET SUMMARY")
        print("=" * 60)
        
        for name, df in datasets.items():
            if df is not None:
                print(f"\n{name.upper()}:")
                print(f"  Rows: {len(df):,}")
                print(f"  Columns: {len(df.columns)}")
                print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                print(f"  Null values: {df.isnull().sum().sum():,}")
                print(f"  Unique states: {df['state'].nunique() if 'state' in df.columns else 'N/A'}")
                print(f"  Unique districts: {df['district'].nunique() if 'district' in df.columns else 'N/A'}")
                print(f"  Unique pincodes: {df['pincode'].nunique() if 'pincode' in df.columns else 'N/A'}")


def quick_load():
    """Quick function to load all data with one call"""
    loader = DataLoader()
    datasets = loader.load_all_data()
    loader.get_summary_stats(datasets)
    return datasets


if __name__ == "__main__":
    # Test the loader
    datasets = quick_load()
