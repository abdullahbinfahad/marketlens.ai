"""Compatibility entry point for Streamlit Cloud configurations targeting app.py/streamlit_app.py."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from streamlit_app import main

if __name__ == "__main__":
    main()
