#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve();ROOT=HERE.parent.parent.parent.parent
scripts=['preflight.py','run_budget_autotune.py','run_objective_calibration.py','run_coupled_expedition.py','run_haven_formulas.py','run_one_opening_cycle.py','run_fail_closed_fuzz.py','compile_all_results.py']
for s in scripts:
 print(f'\n=== {s} ===',flush=True);r=subprocess.run([sys.executable,str(HERE.parent/s)],cwd=ROOT)
 if r.returncode:raise SystemExit(r.returncode)
