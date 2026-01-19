"""
Quick Start Script - Sets up Python environment and installs dependencies
Run this first before any analysis
"""

import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_requirements():
    """Install all required packages"""
    print("\n📦 Installing required packages...")
    print("This may take a few minutes...\n")
    
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            str(requirements_file),
            "--upgrade"
        ])
        print("\n✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing packages: {e}")
        return False

def verify_installation():
    """Verify key packages are installed"""
    print("\n🔍 Verifying installation...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'scipy', 'sklearn', 'streamlit', 'jupyter'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT FOUND")
            all_installed = False
    
    return all_installed

def create_data_structure_guide():
    """Create a guide for where to place CSV files"""
    guide_file = Path(__file__).parent.parent / "DATA_PLACEMENT_GUIDE.txt"
    
    content = """
╔════════════════════════════════════════════════════════════════╗
║          UIDAI HACKATHON - DATA PLACEMENT GUIDE                ║
╚════════════════════════════════════════════════════════════════╝

📁 PLACE YOUR CSV FILES IN THE FOLLOWING FOLDERS:

1. ENROLLMENT DATA (3 CSV files)
   → data/raw/enrolment/
   
2. DEMOGRAPHIC UPDATE DATA (6 CSV files)
   → data/raw/demographic_update/
   
3. BIOMETRIC UPDATE DATA (4 CSV files)
   → data/raw/biometric_update/

═══════════════════════════════════════════════════════════════

📋 AFTER PLACING FILES, RUN:

Option 1 - Automated Analysis:
   python src/automated_eda.py

Option 2 - Interactive Jupyter Notebook:
   jupyter notebook notebooks/01_initial_exploration.ipynb

═══════════════════════════════════════════════════════════════

✨ QUICK COMMANDS:

- Install dependencies:
  python src/setup.py

- Run automated EDA:
  python src/automated_eda.py

- Launch Jupyter:
  jupyter notebook

- Launch Dashboard (after analysis):
  streamlit run dashboard/app.py

═══════════════════════════════════════════════════════════════
"""
    
    with open(guide_file, 'w') as f:
        f.write(content)
    
    print(f"\n📄 Created: {guide_file}")
    print(content)

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("🚀 UIDAI HACKATHON - PROJECT SETUP")
    print("="*70 + "\n")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install packages
    if not install_requirements():
        print("\n⚠️ Some packages failed to install. Please check the errors above.")
        return
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️ Some packages are missing. Try running again.")
        return
    
    # Create guide
    create_data_structure_guide()
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    
    print("\n📌 NEXT STEPS:")
    print("1. Place your CSV files in the appropriate data/raw/ folders")
    print("2. Run: python src/automated_eda.py")
    print("3. Or launch Jupyter: jupyter notebook")
    print("\n")

if __name__ == "__main__":
    main()
