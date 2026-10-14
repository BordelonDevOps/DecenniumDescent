#!/usr/bin/env python3
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LAB = HERE.parent.parent
sys.path.insert(0, str(LAB / "tools"))
from compile_pack_helpers import gather, write_report

EXTRA = [
    "Static inventory: 335 feats, 848 spells parsed; 2000 pairwise + 500 triple scored.",
    "Top risks: extra_action / actor / reset / unbounded / control stacking tags.",
    "Level A static scan; agent confirmation still required for mandatory-choice claims.",
]
records, errors = gather([
    LAB / "results" / "p09",
    LAB / "results" / "09-feat-spell-ability-interactions",
    HERE / "results",
])
write_report(HERE, LAB, "Feat, Spell, and Ability Interaction Scan — Compiled Report", "09-feat-spell-ability-interactions", records, errors, EXTRA)
