"""Make the exploratory-data-analysis scripts importable as the driver imports them."""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "fieldwork" / "exploratory-data-analysis" / "scripts"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
