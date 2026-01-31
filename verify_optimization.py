"""
VERIFICATION SCRIPT - Check if optimization is complete

Run: python verify_optimization.py
"""

import os
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent

def check_files():
    """Verify all required files exist"""
    required_files = [
        'preprocess.py',
        'app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'DEPLOYMENT.md',
        'OPTIMIZATION_SUMMARY.md',
        'src/__init__.py',
        'data/processed/state_compliance.csv',
        'data/processed/state_geography.csv',
        'data/processed/district_volumes.csv',
        'data/processed/state_urban_rural.csv',
        'data/processed/state_metrics_full.csv',
        'data/processed/metadata.json',
    ]
    
    print("\n" + "="*70)
    print("📋 FILE VERIFICATION")
    print("="*70)
    
    all_exist = True
    for file in required_files:
        path = PROJECT_ROOT / file
        exists = path.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file:50s}", end="")
        if exists:
            size = path.stat().st_size
            print(f" ({size:,} bytes)")
        else:
            print()
            all_exist = False
    
    return all_exist

def check_processed_size():
    """Check total size of processed data"""
    print("\n" + "="*70)
    print("📊 PROCESSED DATA SIZE")
    print("="*70)
    
    processed_dir = PROJECT_ROOT / 'data' / 'processed'
    total_size = 0
    
    if processed_dir.exists():
        for file in processed_dir.glob('*.csv'):
            size = file.stat().st_size
            total_size += size
            print(f"  {file.name:30s}: {size:>7,} bytes")
    
    metadata_file = processed_dir / 'metadata.json'
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        print(f"\n  Raw size: {metadata.get('raw_size_mb', 'N/A')} MB")
        print(f"  Processed size: {metadata.get('processed_size_mb', 'N/A')} MB")
        print(f"  Compression ratio: {metadata.get('compression_ratio', 'N/A')}x")
    
    print(f"\n  📊 Total CSV size: {total_size:,} bytes (~{total_size/1024:.1f} KB)")
    print(f"  🎯 Target: < 1MB ✅" if total_size < 1024*1024 else f"  🎯 Target: < 1MB ❌")
    
    return total_size

def check_requirements():
    """Check requirements.txt contains needed packages"""
    print("\n" + "="*70)
    print("📦 DEPENDENCIES CHECK")
    print("="*70)
    
    req_file = PROJECT_ROOT / 'requirements.txt'
    required_packages = [
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn',
        'streamlit',
    ]
    
    if req_file.exists():
        with open(req_file, 'r') as f:
            content = f.read().lower()
        
        for pkg in required_packages:
            found = pkg.lower() in content
            status = "✅" if found else "❌"
            print(f"{status} {pkg}")
    else:
        print("❌ requirements.txt not found")

def main():
    print("\n🔍 OPTIMIZATION VERIFICATION SCRIPT")
    
    # Run checks
    files_ok = check_files()
    size = check_processed_size()
    check_requirements()
    
    # Final summary
    print("\n" + "="*70)
    print("✅ VERIFICATION SUMMARY")
    print("="*70)
    
    checks = {
        "Files in place": files_ok,
        "Processed data size < 1MB": size < 1024*1024,
        "Ready for deployment": files_ok and size < 1024*1024
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    # Deployment instructions
    if all(checks.values()):
        print("\n" + "="*70)
        print("🚀 READY FOR DEPLOYMENT!")
        print("="*70)
        print("""
Next steps:
1. Push to GitHub:
   git add .
   git commit -m "Optimization: 19,600x compression for Streamlit Cloud"
   git push

2. Deploy to Streamlit Cloud:
   - Go to https://share.streamlit.io
   - Create new app from GitHub
   - Select repository and set main file to: app.py
   - Deploy!

3. Test deployment:
   - Visit your public URL
   - Check all dashboard pages
   - Monitor memory usage

Documentation:
- See DEPLOYMENT.md for detailed guide
- See OPTIMIZATION_SUMMARY.md for changes made
        """)
    else:
        print("\n⚠️ Some checks failed. Please review above.")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
