#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

HERE=Path(__file__).resolve().parent
steps=[
    ["python",str(HERE/"preflight.py")],
    ["python",str(HERE/"run_static_validators.py")],
    ["python",str(HERE/"run_baseline_simulations.py")],
    ["python",str(HERE/"run_property_fuzz.py")],
    ["python",str(HERE/"compile_all_results.py")],
]
for cmd in steps:
    print("\n>>>"," ".join(cmd))
    rc=subprocess.call(cmd)
    if rc:
        print("FAILED:",cmd)
        sys.exit(rc)
print("\nBaseline preparation complete. Continue with Cursor agent packs.")
