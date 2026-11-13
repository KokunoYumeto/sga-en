"""Run the included rebuild driver from the records project root."""
import runpy
import sys
from pathlib import Path
driver=Path("work/contributions/packaging_audit/rebuild.py")
sys.path.insert(0,str(driver.parent))
runpy.run_path(str(driver),run_name="__main__")
