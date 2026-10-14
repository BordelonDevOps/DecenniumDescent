#!/usr/bin/env python3
"""Pack 08 — Encounter Budget Calibration (seeded scenario matrix)."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve()
LAB = HERE.parent.parent
ROOT = LAB.parent.parent
PACK = LAB / "packs" / "08-encounter-budget-calibration"
PACK_OUT = PACK / "results"
SUITE_OUT = LAB / "results" / "08-encounter-budget-calibration"
SEED0 = int(os.getenv("DD_PACK08_SEED", "80800"))

GAME = json.loads((ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_1.json").read_text(encoding="utf-8"))
BUDGETS = GAME["encounterMath"]["fourCharacterBudgets"]
RTP = {int(k): v for k, v in GAME["encounterMath"]["relativeThreatPoints"].items()}
DIFF_ORDER = ["routine", "standard", "hard", "severe", "catastrophic"]


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


SOURCE_HASH = sha_file(ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_1.json")


def party_budget(difficulty: str, party_size: int) -> float:
    return BUDGETS[difficulty] * (1.0 + 0.2 * (party_size - 4))


def step_up(diff: str) -> str:
    i = DIFF_ORDER.index(diff)
    return DIFF_ORDER[min(len(DIFF_ORDER) - 1, i + 1)]


def party_member(level: int, role: str) -> dict:
    pb = 2 + (level - 1) // 4
    ac = {"front": 15, "support": 14, "striker": 14, "caster": 13}[role] + (level // 8)
    con = {"front": 3, "support": 2, "striker": 2, "caster": 1}[role]
    die = {"front": 10, "support": 8, "striker": 8, "caster": 6}[role]
    avg = die // 2 + 1
    hp = die + con + (level - 1) * (avg + con)
    attack = pb + 3 + (1 if level >= 8 else 0)
    attacks = 2 if level >= 5 and role in ("front", "striker") else 1
    dmg = {"front": 8.5, "support": 5.5, "striker": 9.5, "caster": 8.0}[role] + level * 0.45
    heal = (5 + level * 1.2) if role == "support" else 0
    return {"role": role, "ac": ac, "hp": hp, "maxhp": hp, "attack": attack, "attacks": attacks, "dmg": dmg, "heal": heal}


def synthesize_foes(level: int, budget: float) -> list[dict]:
    offsets = sorted(RTP.keys(), reverse=True)
    remaining = budget
    foes = []
    guard = 0
    while remaining >= min(RTP.values()) and guard < 12:
        guard += 1
        placed = False
        for off in offsets:
            cost = RTP[off]
            if cost <= remaining + 1e-9:
                if remaining - cost > budget * 0.55 and off >= 0:
                    continue
                flvl = max(1, level + off)
                foes.append(
                    {
                        "offset": off,
                        "cost": cost,
                        "ac": 12 + flvl // 2 + max(0, off),
                        "hp": int((flvl * 8 + 18) * (1 + max(0, off) * 0.12)),
                        "attack": 3 + flvl // 2 + max(-1, off),
                        "dmg": 5.5 + flvl * 0.75 + max(0, off) * 2.0,
                        "multi": 2 if off >= 1 else 1,
                        "curhp": 0,
                    }
                )
                foes[-1]["curhp"] = foes[-1]["hp"]
                remaining -= cost
                placed = True
                break
        if not placed:
            break
    if not foes:
        flvl = max(1, level - 4)
        foes.append(
            {
                "offset": -4,
                "cost": 0,
                "ac": 11 + flvl // 2,
                "hp": int(flvl * 6 + 10),
                "attack": 2 + flvl // 2,
                "dmg": 4 + flvl * 0.5,
                "multi": 1,
                "curhp": int(flvl * 6 + 10),
                "syntheticFallback": True,
            }
        )
    return foes


def d20(rng):
    return rng.randint(1, 20)


def hit(roll, bonus, ac):
    return roll == 20 or (roll != 1 and roll + bonus >= ac)


def simulate_objective(scenario: str, level: int, difficulty: str, party_size: int, rng: random.Random) -> dict:
    """Return outcome dict with success flag for the scenario objective."""
    roles = ["front", "support", "striker", "caster", "front", "striker"][:party_size]
    party = [party_member(level, r) for r in roles]
    rules = []

    # Canon: objectives / hazard / surprise each increase effective difficulty one step
    # unless already baked into creature levels. For labeled matrices we apply mechanical
    # extras AND note whether creature budget was also stepped.
    creature_diff = difficulty
    apply_step = scenario in ("BUDGET-CARGO", "BUDGET-ESCORT", "BUDGET-HAZARD", "BUDGET-AMBUSH", "BUDGET-RETREAT")
    # Ambiguity: does the matrix label already include the step? Record RULES_HALT for clarification.
    if apply_step:
        rules.append(
            {
                "code": "RULES_HALT",
                "topic": "encounterMath.objectiveStep",
                "detail": (
                    "GAMEPLAY_LOOP_CANON: objectives/terrain/surprise/hazards each increase effective "
                    "difficulty by one step unless already included in creature levels. Scenario matrix "
                    f"labels {difficulty} for {scenario}; sim uses creature budget at labeled band and "
                    "adds objective mechanics separately (risk of double-count or under-count)."
                ),
            }
        )

    budget = party_budget(creature_diff, party_size)
    foes = synthesize_foes(level, budget)
    cargo_hp = 40 + level * 5
    cargo_max = cargo_hp
    escort_progress = 0
    escort_needed = 6
    retreat_progress = 0
    retreat_needed = 5
    fixed_rounds = 8
    rounds = 0
    down = 0
    ambush_done = False

    def living():
        return [p for p in party if p["hp"] > 0]

    def foes_alive():
        return [f for f in foes if f["curhp"] > 0]

    def party_act():
        nonlocal escort_progress, retreat_progress
        for p in party:
            if p["hp"] <= 0:
                continue
            if scenario == "BUDGET-ESCORT" and rng.random() < 0.35:
                escort_progress += 1
                continue
            if scenario == "BUDGET-RETREAT":
                retreat_progress += 1
                if rng.random() < 0.4:
                    continue
            if p["role"] == "support":
                cands = [x for x in party if 0 < x["hp"] < x["maxhp"] * 0.5]
                if cands:
                    t = min(cands, key=lambda x: x["hp"] / x["maxhp"])
                    t["hp"] = min(t["maxhp"], t["hp"] + max(1, round(p["heal"] + rng.randint(1, 6))))
                    continue
            for _ in range(p["attacks"]):
                fa = foes_alive()
                if not fa or scenario == "BUDGET-RETREAT":
                    break
                target = max(fa, key=lambda f: f["curhp"])
                if hit(d20(rng), p["attack"], target["ac"]):
                    target["curhp"] -= max(1, round(p["dmg"] + rng.uniform(-2, 2)))

    def foe_act(disadv_party=False):
        nonlocal cargo_hp, down, escort_progress
        for f in foes:
            if f["curhp"] <= 0:
                continue
            for _ in range(f["multi"]):
                # Objective targeting
                if scenario == "BUDGET-CARGO" and rng.random() < 0.45 and cargo_hp > 0:
                    if hit(d20(rng), f["attack"], 12):
                        cargo_hp -= max(1, round(f["dmg"] * 0.8))
                    continue
                if scenario == "BUDGET-ESCORT" and rng.random() < 0.35:
                    escort_progress = max(0, escort_progress - (1 if rng.random() < 0.5 else 0))
                lp = living()
                if not lp:
                    return
                t = rng.choice(lp)
                roll = d20(rng)
                if disadv_party:
                    roll = min(roll, d20(rng))
                # Ambush: surprised party treated as AC-2
                ac = t["ac"] - (2 if disadv_party else 0)
                if hit(roll, f["attack"], ac):
                    t["hp"] -= max(1, round(f["dmg"] + rng.uniform(-1.5, 1.5)))
                    if t["hp"] <= 0:
                        down += 1

    # Ambush: free foe round
    if scenario == "BUDGET-AMBUSH":
        foe_act(disadv_party=True)
        ambush_done = True

    max_rounds = fixed_rounds if scenario in ("BUDGET-CARGO", "BUDGET-RETREAT") else 20
    while rounds < max_rounds and living():
        rounds += 1
        if scenario == "BUDGET-HAZARD":
            # Complex hazard damage each round
            for p in living():
                if rng.random() < 0.55:
                    p["hp"] -= max(1, round(3 + level * 0.6 + rng.uniform(0, 3)))
                    if p["hp"] <= 0:
                        down += 1
        party_act()
        if scenario == "BUDGET-CROSS" and not foes_alive():
            break
        if scenario == "BUDGET-ESCORT" and escort_progress >= escort_needed:
            break
        if scenario == "BUDGET-RETREAT" and retreat_progress >= retreat_needed:
            break
        if living() and (foes_alive() or scenario in ("BUDGET-CARGO", "BUDGET-HAZARD", "BUDGET-AMBUSH", "BUDGET-RETREAT", "BUDGET-ESCORT")):
            # Keep foes present for non-kill objectives even if somehow cleared early
            if not foes_alive() and scenario != "BUDGET-CROSS":
                # Respawn pressure: one filler to keep objective contested
                flvl = level
                foes.append(
                    {
                        "offset": -2,
                        "cost": 15,
                        "ac": 12 + flvl // 2,
                        "hp": int(flvl * 6 + 12),
                        "attack": 2 + flvl // 2,
                        "dmg": 4 + flvl * 0.6,
                        "multi": 1,
                        "curhp": int(flvl * 6 + 12),
                    }
                )
            foe_act(disadv_party=False)
        if scenario == "BUDGET-CARGO" and rounds >= fixed_rounds:
            break
        if scenario == "BUDGET-CROSS" and not foes_alive():
            break

    wiped = not living()
    if scenario == "BUDGET-CROSS":
        success = (not wiped) and (not foes_alive())
    elif scenario == "BUDGET-CARGO":
        success = (not wiped) and cargo_hp > 0 and rounds >= fixed_rounds
    elif scenario == "BUDGET-ESCORT":
        success = (not wiped) and escort_progress >= escort_needed
    elif scenario == "BUDGET-HAZARD":
        success = (not wiped) and (not foes_alive() or rounds >= 12)
        if not foes_alive():
            success = not wiped
    elif scenario == "BUDGET-AMBUSH":
        success = (not wiped) and (not foes_alive())
    elif scenario == "BUDGET-RETREAT":
        success = (not wiped) and retreat_progress >= retreat_needed
    else:
        success = False
        rules.append({"code": "RULES_HALT", "topic": "scenario", "detail": f"Unknown scenario {scenario}"})

    hp_left = sum(max(0, p["hp"]) for p in party)
    hp_total = sum(p["maxhp"] for p in party)
    return {
        "success": success,
        "wiped": wiped,
        "rounds": rounds,
        "downed": down,
        "hpPct": hp_left / hp_total if hp_total else 0,
        "cargoPct": cargo_hp / cargo_max if cargo_max else 0,
        "escortProgress": escort_progress,
        "retreatProgress": retreat_progress,
        "budget": budget,
        "rulesHalts": rules,
        "ambushApplied": ambush_done,
    }


def mean_ci(xs, z=1.96):
    m = statistics.mean(xs)
    if len(xs) < 2:
        return m, m, m
    sd = statistics.stdev(xs)
    half = z * sd / math.sqrt(len(xs))
    return m, m - half, m + half


def expand(field: str):
    return [int(p) if p.strip().isdigit() else p.strip() for p in field.split("|")]


def main():
    PACK_OUT.mkdir(parents=True, exist_ok=True)
    SUITE_OUT.mkdir(parents=True, exist_ok=True)
    matrix = list(csv.DictReader((PACK / "SCENARIO_MATRIX.csv").open(encoding="utf-8")))
    all_findings = []
    all_halts = []
    summary_rows = []

    for row in matrix:
        sid = row["scenario_id"]
        levels = expand(row["levels"])
        parties = expand(row["party_size_or_scope"])
        diffs = expand(row["difficulty_or_state"])
        runs = int(row["runs"])
        scenario_dir = PACK_OUT / sid
        suite_scenario = SUITE_OUT / sid
        scenario_dir.mkdir(parents=True, exist_ok=True)
        suite_scenario.mkdir(parents=True, exist_ok=True)

        cells = []
        scenario_halts = []
        for level in levels:
            for party_size in parties:
                for difficulty in diffs:
                    outs = []
                    for i in range(runs):
                        rng = random.Random(SEED0 + hash((sid, level, party_size, difficulty, i)) % 10_000_000)
                        outs.append(simulate_objective(sid, int(level), str(difficulty), int(party_size), rng))
                    for o in outs:
                        scenario_halts.extend(o["rulesHalts"])
                    succ = [1.0 if o["success"] else 0.0 for o in outs]
                    wipe = [1.0 if o["wiped"] else 0.0 for o in outs]
                    hp = [o["hpPct"] for o in outs]
                    sr, lo, hi = mean_ci(succ)
                    cell = {
                        "level": int(level),
                        "partySize": int(party_size),
                        "difficulty": difficulty,
                        "runs": runs,
                        "successRate": round(sr, 4),
                        "successCI95": [round(lo, 4), round(hi, 4)],
                        "wipeRate": round(mean_ci(wipe)[0], 4),
                        "meanHpPct": round(mean_ci(hp)[0], 4),
                        "meanRounds": round(mean_ci([float(o["rounds"]) for o in outs])[0], 3),
                        "budget": party_budget(str(difficulty), int(party_size)),
                    }
                    if sid == "BUDGET-CARGO":
                        cell["meanCargoPct"] = round(mean_ci([o["cargoPct"] for o in outs])[0], 4)
                    cells.append(cell)
                    summary_rows.append({"scenarioId": sid, **cell})

        findings = []
        # Distinctness of difficulty bands
        by_lp = {}
        for c in cells:
            by_lp.setdefault((c["level"], c["partySize"]), []).append(c)
        for key, group in by_lp.items():
            group = sorted(group, key=lambda c: DIFF_ORDER.index(c["difficulty"]) if c["difficulty"] in DIFF_ORDER else 99)
            rates = [c["successRate"] for c in group]
            # Monotonic non-increasing expected
            for a, b in zip(group, group[1:]):
                if b["successRate"] > a["successRate"] + 0.03:
                    findings.append(
                        {
                            "severity": "confirmed",
                            "type": "budget_band_inversion",
                            "scenario": sid,
                            "level": key[0],
                            "partySize": key[1],
                            "easier": a["difficulty"],
                            "harder": b["difficulty"],
                            "successRates": [a["successRate"], b["successRate"]],
                            "detail": "Harder labeled budget produced higher objective success than easier band.",
                        }
                    )
                elif abs(a["successRate"] - b["successRate"]) < 0.05:
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "budget_band_nondistinct",
                            "scenario": sid,
                            "level": key[0],
                            "partySize": key[1],
                            "pair": [a["difficulty"], b["difficulty"]],
                            "successRates": [a["successRate"], b["successRate"]],
                            "detail": "Adjacent budgets not distinct in outcome distribution (<5pp).",
                        }
                    )
            if len(rates) >= 3 and (max(rates) - min(rates)) < 0.12:
                findings.append(
                    {
                        "severity": "confirmed",
                        "type": "budget_collapse_across_band",
                        "scenario": sid,
                        "level": key[0],
                        "partySize": key[1],
                        "successRates": rates,
                        "detail": "All difficulty bands within 12pp — budgets do not produce predictable distinct bands.",
                    }
                )

        # Party-size adjustment check: at same level/diff, larger party should improve success if budget scales correctly
        for level in levels:
            for difficulty in diffs:
                subset = [c for c in cells if c["level"] == level and c["difficulty"] == difficulty]
                subset = sorted(subset, key=lambda c: c["partySize"])
                if len(subset) >= 2:
                    # Scaled budget should keep success roughly stable; large swings imply bad scaling
                    spread = max(c["successRate"] for c in subset) - min(c["successRate"] for c in subset)
                    if spread > 0.25:
                        findings.append(
                            {
                                "severity": "suspected",
                                "type": "party_size_scaling_unstable",
                                "scenario": sid,
                                "level": level,
                                "difficulty": difficulty,
                                "byParty": [(c["partySize"], c["successRate"], c["budget"]) for c in subset],
                                "detail": "±20% per PC budget scaling left >25pp success swing across party sizes.",
                            }
                        )

        halt_keys = set()
        uniq = []
        for h in scenario_halts:
            k = (h.get("topic"), h.get("detail"))
            if k not in halt_keys:
                halt_keys.add(k)
                uniq.append(h)

        outcome = "FAIL" if any(f["severity"] == "confirmed" for f in findings) else ("WARN" if findings else "PASS")
        record = {
            "pack": "08-encounter-budget-calibration",
            "scenarioId": sid,
            "runId": f"{sid}-{SEED0}",
            "seed": SEED0,
            "sourceHash": SOURCE_HASH,
            "fixtureHash": hashlib.sha256(json.dumps(cells, sort_keys=True).encode()).hexdigest(),
            "evidenceLevel": "A",
            "outcome": outcome,
            "metrics": {"cells": cells, "cellCount": len(cells), "runsPerCell": runs, "objective": row["objective"]},
            "rulesHalts": uniq,
            "findings": findings,
            "rawEvidencePath": f"results/08-encounter-budget-calibration/{sid}/",
        }
        (scenario_dir / "summary.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        (suite_scenario / "summary.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        with (scenario_dir / "cells.csv").open("w", newline="", encoding="utf-8") as f:
            if cells:
                # flatten CI
                flat = []
                for c in cells:
                    d = dict(c)
                    d["successCI95"] = str(d.get("successCI95"))
                    flat.append(d)
                w = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
                w.writeheader()
                w.writerows(flat)
        all_findings.extend(findings)
        all_halts.extend(uniq)

    rollup = {
        "pack": "08-encounter-budget-calibration",
        "scenarioId": "PACK08-ROLLUP",
        "runId": f"PACK08-{SEED0}",
        "seed": SEED0,
        "sourceHash": SOURCE_HASH,
        "fixtureHash": None,
        "evidenceLevel": "A",
        "outcome": "FAIL" if any(f.get("severity") == "confirmed" for f in all_findings) else ("WARN" if all_findings else "PASS"),
        "metrics": {"scenarioCount": len(matrix), "summaryRows": len(summary_rows), "findingCount": len(all_findings)},
        "rulesHalts": all_halts,
        "findings": all_findings[:250],
        "rawEvidencePath": "results/08-encounter-budget-calibration/",
    }
    (SUITE_OUT / "rollup.json").write_text(json.dumps(rollup, indent=2), encoding="utf-8")
    (PACK_OUT / "rollup.json").write_text(json.dumps(rollup, indent=2), encoding="utf-8")
    with (SUITE_OUT / "all_cells.csv").open("w", newline="", encoding="utf-8") as f:
        if summary_rows:
            flat = []
            fields = set()
            for c in summary_rows:
                d = dict(c)
                if "successCI95" in d:
                    d["successCI95"] = str(d["successCI95"])
                flat.append(d)
                fields.update(d.keys())
            w = csv.DictWriter(f, fieldnames=sorted(fields), extrasaction="ignore")
            w.writeheader()
            w.writerows(flat)
    print(json.dumps({"pack": "08", "scenarios": len(matrix), "cells": len(summary_rows), "findings": len(all_findings), "halts": len(all_halts)}, indent=2))


if __name__ == "__main__":
    main()
