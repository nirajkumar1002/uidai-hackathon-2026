"""
UIDAI Data Hackathon - Dashboard Package

This package contains utilities for the Streamlit dashboard.
Preprocessing is done separately using preprocess.py.
The dashboard only loads processed data.
"""

__version__ = "1.0.0"
__author__ = "Dhurandhar Team"

from .visualization_utils import VisualizationTools

__all__ = ['VisualizationTools']
