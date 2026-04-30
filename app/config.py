"""
Shared configuration for the Streamlit app.
Provides reliable PROJECT_ROOT that works regardless of how Streamlit
discovers and executes page scripts.
"""

import os
import sys

# This file lives at app/config.py, so go up one level to get the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Ensure project root is on the path so 'utils' is importable
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
