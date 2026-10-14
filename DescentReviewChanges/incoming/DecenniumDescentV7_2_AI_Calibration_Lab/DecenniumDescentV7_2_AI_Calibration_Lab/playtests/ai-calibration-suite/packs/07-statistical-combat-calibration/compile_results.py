#!/usr/bin/env python3
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LAB = HERE.parent.parent
sys.path.insert(0, str(LAB / "tools"))
from compile_pack_helpers import gather, write_report

EXTRA = [
    "Proxy chassis Monte Carlo across L1–L20 / party 4–6 / difficulty bands.",
    "Difficulty order generally holds; level-curve instability flags mid-tier softness vs L1 lethality.",
    "Canon untouched; candidate budget retunes only via proposed-patches.",
]
records, errors = gather([
    LAB / "results" / "p07",
    LAB / "results" / "07-statistical-combat-calibration",
    HERE / "results",
])
write_report(HERE, LAB, "Statistical Combat Calibration — Compiled Report", "07-statistical-combat-calibration", records, errors, EXTRA)
