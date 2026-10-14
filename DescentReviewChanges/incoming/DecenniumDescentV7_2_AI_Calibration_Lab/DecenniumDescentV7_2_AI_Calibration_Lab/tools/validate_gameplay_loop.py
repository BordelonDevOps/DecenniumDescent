#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_2.json"
RUNTIME = ROOT / "src/data/gameplay-loop.json"
DOC = ROOT / "docs/mechanics/GAMEPLAY_LOOP_CANON.md"
DOCTRINE = ROOT / "docs/mechanics/DESIGN_DOCTRINE.md"
COMPONENT = ROOT / "src/components/ExpeditionTracker.tsx"
QUICKSTART_MD = ROOT / "docs/mechanics/QUICKSTART_LEVEL_1.md"
QUICKSTART_DOCX = ROOT / "books/player/Decennium_Descent_Quickstart_Reference_v1.docx"

REQUIRED_TEAMS = {"combat", "recon", "research", "resource", "support", "rest"}
DESIGN_RULE = "Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems."

errors: list[str] = []
for path in [PUBLIC, RUNTIME, DOC, DOCTRINE, COMPONENT, QUICKSTART_MD, QUICKSTART_DOCX]:
    if not path.exists():
        errors.append(f"Missing required gameplay artifact: {path.relative_to(ROOT)}")

if not errors:
    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    if public != runtime:
        errors.append("Public and runtime gameplay-loop JSON differ")
    if public.get("meta", {}).get("designRule") != DESIGN_RULE:
        errors.append("Canonical design rule is missing or changed")
    if public.get("meta", {}).get("version") != "1.2":
        errors.append("Gameplay loop must be version 1.2")
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
    limits = public.get("combat", {}).get("actionLimits", {})
    if limits.get("extraFullActionsPerRound") != 1:
        errors.append("Additional full Actions must be capped at one per round")
    if limits.get("independentSummons") != 2:
        errors.append("Independent combat-capable actors must be capped at two")
    retreat = public.get("combat", {}).get("retreat", {})
    if retreat.get("escapeSourceCapPerRound") != 1:
        errors.append("Retreat must cap ordinary Escape sources at one per round")
    debt = public.get("restAndAttrition", {}).get("restDebt", {})
    if debt.get("countdownWatches") != 2:
        errors.append("Rest Debt must use a two-Watch countdown")
    if len(public.get("havenResolution", [])) != 10:
        errors.append("Full Haven resolution must contain ten ordered steps")
    if len(public.get("havenShortPath", {}).get("steps", [])) != 5:
        errors.append("Tier I Haven fast path must contain five steps")
    if len(public.get("seasonal", {}).get("changeCategories", [])) != 5:
        errors.append("Seasonal loop must include five change categories")
    if public.get("seasonal", {}).get("openingsPerCycle") != 1:
        errors.append("There must be exactly one Opening per ten-year Cycle")
    if public.get("seasonal", {}).get("cycleLengthYears") != 10:
        errors.append("Cycle length must be ten years")
    if "sustenance" not in public.get("route", {}).get("ratings", []):
        errors.append("Routes must include Sustenance")
    if public.get("route", {}).get("forcedMarchUnknown", {}).get("progress") != 1:
        errors.append("Unknown-route Forced March procedure is missing")
    if public.get("advancement", {}).get("default") != "milestone":
        errors.append("Milestone advancement must be the default")
    if not public.get("extraction", {}).get("testCadence"):
        errors.append("Extraction test cadence is missing")
    ec_mods = public.get("extraction", {}).get("cargoDcModifierByHighestClass", {})
    if ec_mods != {str(i): i for i in range(7)}:
        errors.append("Extraction Class DC modifier table must be +0 through +6")
    if public.get("extraction", {}).get("cargoModifierCap") != 7:
        errors.append("Cargo-and-handling Extraction modifier must cap at +7")
    encounter = public.get("encounterMath", {})
    if encounter.get("partySizeMultipliers") != {"3": 0.8, "4": 1.0, "5": 1.2, "6": 1.4}:
        errors.append("Encounter party-size multipliers mismatch")
    if not encounter.get("difficultyAccounting") or not encounter.get("objectiveProfiles"):
        errors.append("Objective difficulty accounting is missing")
    if not public.get("havenEconomy", {}).get("taxSchedule"):
        errors.append("Haven tax schedule is missing")
    if not public.get("havenEconomy", {}).get("insurance"):
        errors.append("Haven cargo insurance formula is missing")
    if not public.get("reputation", {}).get("accessGates"):
        errors.append("Reputation access gates are missing")
    if public.get("seasonal", {}).get("havenDistrictStates") != ["Intact", "Strained", "Damaged", "Captured", "Recovering"]:
        errors.append("Haven district condition track mismatch")
    component_text = COMPONENT.read_text(encoding="utf-8")
    if "Rest debt {member.watchesWithoutRest}/3" in component_text:
        errors.append("ExpeditionTracker still uses obsolete /3 Rest Debt counter")
    if "restDebtDueIn" not in component_text:
        errors.append("ExpeditionTracker lacks explicit Rest Debt countdown")
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

print("Gameplay loop validation: PASS - preparation -> descent -> extraction -> Haven -> one decennial Opening")
