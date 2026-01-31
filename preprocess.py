"""
PREPROCESSING SCRIPT - UIDAI Data Hackathon
============================================

This script:
1. Loads all raw CSV files from data/raw/ (~209MB)
2. Performs heavy pandas operations (cleaning, merging, aggregations)
3. Generates processed summary tables
4. Saves compressed files to data/processed/ (~15-20MB)

This preprocessing is done ONCE locally before deployment.
The app.py only loads these small processed files.

Usage:
    python preprocess.py

Output:
    data/processed/
    ├── state_compliance.csv          (Biometric compliance by state)
    ├── state_geography.csv           (Enrollment concentration by state)
    ├── state_urban_rural.csv         (Urban-rural split by state)
    ├── district_volumes.csv          (Enrollment by district)
    ├── state_metrics_full.csv        (Complete metrics for analytics)
    └── metadata.json                 (Processing metadata)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import warnings
import sys

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'

# Ensure processed directory exists
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_state_name(state):
    """Standardize state/UT names to handle variations in formatting"""
    if pd.isna(state):
        return state
    state = str(state).strip()
    state = state.lower().title()
    state = ' '.join(state.split())
    state = state.replace('&', 'And').replace(' & ', ' And ')
    
    replacements = {
        'Orissa': 'Odisha',
        'Pondicherry': 'Puducherry',
        'West  Bengal': 'West Bengal',
        'West Bangal': 'West Bengal',
        'Westbengal': 'West Bengal',
        'Andaman And Nicobar Islands': 'Andaman And Nicobar Islands',
        'Andaman & Nicobar Islands': 'Andaman And Nicobar Islands',
        'Dadra And Nagar Haveli': 'Dadra And Nagar Haveli And Daman And Diu',
        'Dadra And Nagar Haveli And Daman And Diu': 'Dadra And Nagar Haveli And Daman And Diu',
        'Dadra & Nagar Haveli': 'Dadra And Nagar Haveli And Daman And Diu',
        'Dadra & Nagar Haveli And Daman And Diu': 'Dadra And Nagar Haveli And Daman And Diu',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra And Nagar Haveli And Daman And Diu',
        'Daman And Diu': 'Dadra And Nagar Haveli And Daman And Diu',
        'Daman & Diu': 'Dadra And Nagar Haveli And Daman And Diu',
        'Jammu And Kashmir': 'Jammu And Kashmir',
        'Jammu & Kashmir': 'Jammu And Kashmir',
    }
    return replacements.get(state, state)

def load_dataset(folder_path, dataset_name):
    """Load and combine all CSV files from a folder"""
    print(f"\n📂 Loading {dataset_name}...")
    csv_files = list(folder_path.glob('*.csv'))
    
    if not csv_files:
        print(f"   ⚠️ No CSV files found!")
        return None
    
    print(f"   Found {len(csv_files)} files")
    dfs = []
    
    for file in csv_files:
        print(f"   → {file.name}", end="")
        df = pd.read_csv(file)
        print(f" ({len(df):,} rows)")
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    print(f"   Total: {len(combined):,} rows")
    
    # Convert date
    if 'date' in combined.columns:
        combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
    
    # Clean state names
    if 'state' in combined.columns:
        combined['state'] = combined['state'].apply(clean_state_name)
        combined = combined[~combined['state'].str.match(r'^\d+$', na=False)]
    
    # Remove duplicates
    before = len(combined)
    combined = combined.drop_duplicates()
    after = len(combined)
    print(f"   After dedup: {after:,} rows (removed {before-after:,} duplicates)")
    
    return combined

def optimize_dtypes(df):
    """Optimize data types to reduce memory usage"""
    for col in df.columns:
        if df[col].dtype == 'int64':
            # Check if can use int32
            if df[col].min() >= np.iinfo(np.int32).min and df[col].max() <= np.iinfo(np.int32).max:
                df[col] = df[col].astype('int32')
        elif df[col].dtype == 'float64':
            # Check if can use float32
            df[col] = df[col].astype('float32')
        elif df[col].dtype == 'object':
            # Convert to category if beneficial
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
    return df

# ============================================================================
# PREPROCESSING FUNCTIONS
# ============================================================================

def preprocess_all_data():
    """Main preprocessing function"""
    
    print("\n" + "="*70)
    print("🚀 UIDAI DATA PREPROCESSING - STARTED")
    print("="*70)
    
    # Load all raw datasets
    enrolment = load_dataset(RAW_DATA_DIR / 'enrolment', 'Enrolment Data')
    demographic = load_dataset(RAW_DATA_DIR / 'demographic_update', 'Demographic Data')
    biometric = load_dataset(RAW_DATA_DIR / 'biometric_update', 'Biometric Data')
    
    if enrolment is None or demographic is None or biometric is None:
        print("❌ ERROR: Could not load all datasets!")
        return False
    
    print("\n" + "-"*70)
    print("⚙️  PROCESSING DATA")
    print("-"*70)
    
    # ========== ENROLMENT PROCESSING ==========
    print("\n1️⃣ Processing Enrolment Data...")
    
    # Fill NaN values in age columns
    age_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
    for col in age_cols:
        if col in enrolment.columns:
            enrolment[col] = enrolment[col].fillna(0)
    
    # Create derived columns
    enrolment['total_enroll'] = enrolment[age_cols].sum(axis=1)
    enrolment['children_enroll'] = enrolment[['age_0_5', 'age_5_17']].sum(axis=1)
    
    # Optimize data types
    enrolment = optimize_dtypes(enrolment)
    
    print(f"   Enrolment shape: {enrolment.shape}")
    print(f"   Memory: {enrolment.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # ========== BIOMETRIC PROCESSING ==========
    print("\n2️⃣ Processing Biometric Data...")
    
    # Fill NaN values
    biometric = biometric.fillna(0)
    biometric['bio_child'] = biometric.get('bio_age_5_17', 0)
    
    # Optimize data types
    biometric = optimize_dtypes(biometric)
    
    print(f"   Biometric shape: {biometric.shape}")
    print(f"   Memory: {biometric.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # ========== DEMOGRAPHIC PROCESSING ==========
    print("\n3️⃣ Processing Demographic Data...")
    
    demographic = optimize_dtypes(demographic)
    
    print(f"   Demographic shape: {demographic.shape}")
    print(f"   Memory: {demographic.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # ========== AGGREGATED TABLES ==========
    print("\n4️⃣ Creating aggregated tables...")
    
    # TABLE 1: STATE COMPLIANCE (for Problem 1)
    print("   → state_compliance.csv")
    state_enroll = enrolment.groupby('state')[['age_0_5', 'age_5_17']].sum().reset_index()
    state_enroll['children_enroll'] = state_enroll['age_0_5'] + state_enroll['age_5_17']
    
    state_bio = biometric.groupby('state')['bio_child'].sum().reset_index()
    state_bio.columns = ['state', 'child_bio_updates']
    
    state_compliance = state_enroll.merge(state_bio, on='state', how='left')
    state_compliance['child_bio_updates'] = state_compliance['child_bio_updates'].fillna(0)
    state_compliance['compliance_ratio'] = (
        state_compliance['child_bio_updates'] / 
        (state_compliance['children_enroll'] + 1)  # Avoid division by zero
    )
    state_compliance = optimize_dtypes(state_compliance)
    
    # TABLE 2: STATE GEOGRAPHY (for Problem 2)
    print("   → state_geography.csv")
    state_volumes = enrolment.groupby('state').agg({
        'total_enroll': 'sum',
        'district': 'nunique'
    }).reset_index()
    state_volumes.columns = ['state', 'total_enroll', 'num_districts']
    state_volumes['per_capita_district'] = state_volumes['total_enroll'] / (state_volumes['num_districts'] + 1)
    state_volumes = state_volumes.sort_values('total_enroll', ascending=False)
    state_volumes = optimize_dtypes(state_volumes)
    
    # TABLE 3: DISTRICT VOLUMES (for Problem 3)
    print("   → district_volumes.csv")
    district_volumes = enrolment.groupby('district')['total_enroll'].sum().reset_index()
    district_volumes = district_volumes.sort_values('total_enroll', ascending=False)
    district_volumes = optimize_dtypes(district_volumes)
    
    # TABLE 4: STATE URBAN-RURAL SPLIT (for Problem 3)
    print("   → state_urban_rural.csv")
    urban_districts = set(district_volumes.head(50)['district'])
    enrolment['is_urban'] = enrolment['district'].isin(urban_districts).astype('int8')
    
    state_urban_rural = enrolment.groupby('state').agg({
        'total_enroll': 'sum',
        'is_urban': lambda x: (x == 1).sum()
    }).reset_index()
    state_urban_rural.columns = ['state', 'total_enroll', 'urban_districts']
    state_urban_rural['urban_pct'] = (
        state_urban_rural['urban_districts'] / (state_urban_rural['total_enroll'] + 1)
    )
    state_urban_rural = optimize_dtypes(state_urban_rural)
    
    # TABLE 5: FULL STATE METRICS (for Advanced Analytics)
    print("   → state_metrics_full.csv")
    state_metrics = enrolment.groupby('state').agg({
        'total_enroll': 'sum',
        'district': 'nunique',
        'is_urban': lambda x: (x == 1).sum()
    }).reset_index()
    state_metrics.columns = ['state', 'total_enroll', 'num_districts', 'urban_count']
    state_metrics['urban_pct'] = (
        state_metrics['urban_count'] / (state_metrics['num_districts'] + 1)
    )
    state_metrics = state_metrics.merge(
        state_compliance[['state', 'compliance_ratio']], 
        on='state', 
        how='left'
    ).dropna()
    state_metrics = optimize_dtypes(state_metrics)
    
    # ========== SAVE PROCESSED FILES ==========
    print("\n" + "-"*70)
    print("💾 SAVING PROCESSED FILES")
    print("-"*70)
    
    files_to_save = [
        ('state_compliance.csv', state_compliance),
        ('state_geography.csv', state_volumes),
        ('district_volumes.csv', district_volumes),
        ('state_urban_rural.csv', state_urban_rural),
        ('state_metrics_full.csv', state_metrics),
    ]
    
    total_size = 0
    for filename, df in files_to_save:
        filepath = PROCESSED_DATA_DIR / filename
        df.to_csv(filepath, index=False, compression='gzip')
        size_mb = filepath.stat().st_size / 1024**2
        total_size += size_mb
        print(f"   ✅ {filename:30s} → {size_mb:6.2f} MB ({len(df):,} rows)")
    
    print(f"\n   📊 Total processed size: {total_size:.2f} MB")
    print(f"   📉 Compression ratio: {(209 / total_size):.1f}x")
    
    # ========== SAVE METADATA ==========
    metadata = {
        'preprocessing_date': pd.Timestamp.now().isoformat(),
        'raw_size_mb': 209,
        'processed_size_mb': round(total_size, 2),
        'compression_ratio': round(209 / total_size, 2),
        'datasets': {
            'enrolment': {'rows': len(enrolment), 'columns': list(enrolment.columns)},
            'biometric': {'rows': len(biometric), 'columns': list(biometric.columns)},
            'demographic': {'rows': len(demographic), 'columns': list(demographic.columns)},
        },
        'processed_files': {name: len(df) for name, df in files_to_save}
    }
    
    metadata_path = PROCESSED_DATA_DIR / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n   📝 Metadata saved to metadata.json")
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "="*70)
    print("✅ PREPROCESSING COMPLETE!")
    print("="*70)
    print(f"\n📍 Processed files location: {PROCESSED_DATA_DIR}")
    print(f"\n🚀 Next step: Deploy app.py to Streamlit Cloud")
    print(f"   - Raw data (data/raw/) is NOT needed for deployment")
    print(f"   - Only data/processed/ files are needed")
    print("\n💡 To run the dashboard locally:")
    print(f"   streamlit run app.py")
    print("\n" + "="*70)
    
    return True

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        success = preprocess_all_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
