#!/usr/bin/env python3
from pathlib import Path
import subprocess, json, sys

HERE=Path(__file__).resolve()
LAB=HERE.parent.parent
ROOT=LAB.parent.parent
commands=[
    ["python","tools/validate_magic_system.py"],
    ["node","--no-warnings","tools/validate_class_abilities.mjs"],
    ["python","tools/validate_public_canon.py"],
    ["python","tools/validate_gameplay_loop.py"],
]
results=[]
for cmd in commands:
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    results.append({"command":" ".join(cmd),"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr})
out=LAB/"results"/"00-static-validators"
out.mkdir(parents=True,exist_ok=True)
(out/"results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
for r in results:
    print(f"{r['command']}: {'PASS' if r['returncode']==0 else 'FAIL'}")
    if r["stdout"]: print(r["stdout"])
    if r["stderr"]: print(r["stderr"],file=sys.stderr)
sys.exit(1 if any(r["returncode"] for r in results) else 0)
