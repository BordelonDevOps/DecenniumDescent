#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_1.json"
RUNTIME = ROOT / "src/data/gameplay-loop.json"
DOC = ROOT / "docs/mechanics/GAMEPLAY_LOOP_CANON.md"
DOCTRINE = ROOT / "docs/mechanics/DESIGN_DOCTRINE.md"
COMPONENT = ROOT / "src/components/ExpeditionTracker.tsx"

REQUIRED_TEAMS = {"combat", "recon", "research", "resource", "support", "rest"}
DESIGN_RULE = "Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems."

errors: list[str] = []
for path in [PUBLIC, RUNTIME, DOC, DOCTRINE, COMPONENT]:
    if not path.exists():
        errors.append(f"Missing required gameplay artifact: {path.relative_to(ROOT)}")

if not errors:
    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    if public != runtime:
        errors.append("Public and runtime gameplay-loop JSON differ")
    if public.get("meta", {}).get("designRule") != DESIGN_RULE:
        errors.append("Canonical design rule is missing or changed")
    if public.get("expedition", {}).get("maximumRoster") != 12:
        errors.append("Expedition maximum roster must be 12")
    modes = public.get("modes", {}).get("expedition", {})
    if modes.get("watchHours") != 8 or modes.get("watchesPerDay") != 3:
        errors.append("Expedition Mode must use three eight-hour Watches")
    opening = public.get("opening", {})
    if opening.get("hours") != 2400 or opening.get("hornHour") != 1200:
        errors.append("Opening/Horn clock must be 2400/1200 hours")
    teams = {entry.get("id") for entry in public.get("expedition", {}).get("teams", [])}
    if teams != REQUIRED_TEAMS:
        errors.append(f"Gameplay teams mismatch: {teams}")
    if public.get("pressure", {}).get("maximum") != 6:
        errors.append("Pressure must use 0-6")
    if public.get("cargo", {}).get("priorityRange") != [1, 5]:
        errors.append("Cargo priority must use 1-5")
    if public.get("combat", {}).get("actionLimits", {}).get("extraFullActionsPerRound") != 1:
        errors.append("Additional full Actions must be capped at one per round")
    if public.get("combat", {}).get("actionLimits", {}).get("independentSummons") != 2:
        errors.append("Independent combat-capable summons must be capped at two")
    if len(public.get("havenResolution", [])) != 10:
        errors.append("Haven resolution must contain ten ordered steps")
    if len(public.get("seasonal", {}).get("changeCategories", [])) != 5:
        errors.append("Seasonal loop must include five change categories")
    if public.get("meta", {}).get("version") != "1.1":
        errors.append("Gameplay loop must be version 1.1")
    if "sustenance" not in public.get("route", {}).get("ratings", []):
        errors.append("Routes must include Sustenance")
    if public.get("advancement", {}).get("default") != "milestone":
        errors.append("Milestone advancement must be the default")
    if not public.get("extraction", {}).get("testCadence"):
        errors.append("Extraction test cadence is missing")
    if not public.get("havenEconomy", {}).get("taxSchedule"):
        errors.append("Haven tax schedule is missing")
    if public.get("seasonal", {}).get("havenDistrictStates") != ["Intact", "Strained", "Damaged", "Captured", "Recovering"]:
        errors.append("Haven district condition track mismatch")
    public_text = json.dumps(public).lower()
    banned = ["marquis of silence", "claimant succession", "tier vii", "tier viii", "tier ix", "tier x"]
    for token in banned:
        if token in public_text:
            errors.append(f"Public gameplay data leaked Director term: {token}")

if errors:
    print("Gameplay loop validation: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Gameplay loop validation: PASS — complete preparation → descent → extraction → Haven → seasonal loop")
