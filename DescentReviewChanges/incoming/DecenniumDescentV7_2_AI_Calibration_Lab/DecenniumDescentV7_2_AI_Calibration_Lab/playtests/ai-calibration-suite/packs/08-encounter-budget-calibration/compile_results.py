#!/usr/bin/env python3
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LAB = HERE.parent.parent
sys.path.insert(0, str(LAB / "tools"))
from compile_pack_helpers import gather, write_report

EXTRA = [
    "Objective-conditioned budgets (kill/cargo/escort/hazard/ambush/retreat).",
    "Ambush / escort / objective stacking produce RULES_HALT and soft-band findings.",
    "No silent rulebook edits.",
]
records, errors = gather([
    LAB / "results" / "p08",
    LAB / "results" / "08-encounter-budget-calibration",
    HERE / "results",
])
write_report(HERE, LAB, "Encounter Budget Calibration — Compiled Report", "08-encounter-budget-calibration", records, errors, EXTRA)
