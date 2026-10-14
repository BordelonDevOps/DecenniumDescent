#!/usr/bin/env python3
"""Pack 07 — Statistical Combat Calibration (seeded Monte Carlo)."""
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
PACK = LAB / "packs" / "07-statistical-combat-calibration"
# Short suite-side paths avoid Windows MAX_PATH on deep pack folders.
PACK_OUT = LAB / "results" / "p07"
SUITE_OUT = LAB / "results" / "07-statistical-combat-calibration"
SEED0 = int(os.getenv("DD_PACK07_SEED", "70700"))

GAME = json.loads((ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_2.json").read_text(encoding="utf-8"))
BUDGETS = GAME["encounterMath"]["fourCharacterBudgets"]
RTP = {int(k): v for k, v in GAME["encounterMath"]["relativeThreatPoints"].items()}


def _win_long(path: Path) -> str:
    p = os.path.abspath(str(path))
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


def write_text(path: Path, text: str) -> None:
    os.makedirs(_win_long(Path(path).parent), exist_ok=True)
    with open(_win_long(path), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def write_json(path: Path, obj) -> None:
    write_text(path, json.dumps(obj, indent=2))


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


SOURCE_HASH = sha_file(ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_2.json")


def party_budget(difficulty: str, party_size: int) -> float:
    base = BUDGETS[difficulty]
    return base * (1.0 + 0.2 * (party_size - 4))


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
    # Resource proxy: short-rest burst points (RP-like)
    rp = 2 + level // 3
    return {
        "role": role,
        "ac": ac,
        "hp": hp,
        "maxhp": hp,
        "attack": attack,
        "attacks": attacks,
        "dmg": dmg,
        "heal": heal,
        "rp": rp,
        "maxrp": rp,
    }


def synthesize_foes(level: int, budget: float) -> list[dict]:
    """Greedy pack using relativeThreatPoints against party level."""
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
                # Prefer spending down; at low remaining allow -4 fillers
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
                    }
                )
                remaining -= cost
                placed = True
                break
        if not placed:
            # Force cheapest unit if any budget left
            off = min(offsets, key=lambda o: RTP[o])
            cost = RTP[off]
            if cost > remaining:
                break
            flvl = max(1, level + off)
            foes.append(
                {
                    "offset": off,
                    "cost": cost,
                    "ac": 12 + flvl // 2,
                    "hp": int(flvl * 8 + 18),
                    "attack": 3 + flvl // 2,
                    "dmg": 5.5 + flvl * 0.75,
                    "multi": 1,
                }
            )
            remaining -= cost
    if not foes:
        # RULES_HALT fallback: budget too small for any published RTP unit
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
                "syntheticFallback": True,
            }
        )
    return foes


def d20(rng: random.Random) -> int:
    return rng.randint(1, 20)


def hit(roll: int, bonus: int, ac: int) -> bool:
    return roll == 20 or (roll != 1 and roll + bonus >= ac)


def simulate(level: int, difficulty: str, party_size: int, rng: random.Random, max_rounds: int = 20) -> dict:
    roles = ["front", "support", "striker", "caster", "front", "striker"][:party_size]
    party = [party_member(level, r) for r in roles]
    budget = party_budget(difficulty, party_size)
    foes = synthesize_foes(level, budget)
    for f in foes:
        f["curhp"] = f["hp"]
    rounds = 0
    down = 0
    damage_dealt = 0
    damage_taken = 0
    healing = 0
    hits = 0
    attacks = 0
    rp_spent = 0
    rules = []
    if any(f.get("syntheticFallback") for f in foes):
        rules.append(
            {
                "code": "RULES_HALT",
                "topic": "encounterMath.relativeThreatPoints",
                "detail": f"Budget {budget} could not place published RTP units; used synthetic filler.",
            }
        )

    while rounds < max_rounds and any(f["curhp"] > 0 for f in foes) and any(p["hp"] > 0 for p in party):
        rounds += 1
        # Party turn
        for p in party:
            if p["hp"] <= 0:
                continue
            if p["role"] == "support":
                candidates = [x for x in party if 0 < x["hp"] < x["maxhp"] * 0.5]
                if candidates and p["rp"] > 0:
                    t = min(candidates, key=lambda x: x["hp"] / x["maxhp"])
                    h = max(1, round(p["heal"] + rng.randint(1, 6)))
                    t["hp"] = min(t["maxhp"], t["hp"] + h)
                    healing += h
                    p["rp"] -= 1
                    rp_spent += 1
                    continue
            for _ in range(p["attacks"]):
                living = [f for f in foes if f["curhp"] > 0]
                if not living:
                    break
                target = max(living, key=lambda f: f["curhp"])
                attacks += 1
                roll = d20(rng)
                bonus = p["attack"]
                # Optional RP spend for +2 to hit (burst)
                if p["rp"] > 0 and roll + bonus < target["ac"] and roll + bonus + 2 >= target["ac"] and rng.random() < 0.35:
                    p["rp"] -= 1
                    rp_spent += 1
                    bonus += 2
                if hit(roll, bonus, target["ac"]):
                    hits += 1
                    dmg = max(1, round(p["dmg"] + rng.uniform(-2, 2)))
                    target["curhp"] -= dmg
                    damage_dealt += dmg
        if not any(f["curhp"] > 0 for f in foes):
            break
        # Foe turn
        living_p = [p for p in party if p["hp"] > 0]
        for f in foes:
            if f["curhp"] <= 0 or not living_p:
                continue
            for _ in range(f["multi"]):
                if not living_p:
                    break
                t = rng.choice(living_p)
                attacks += 1
                if hit(d20(rng), f["attack"], t["ac"]):
                    hits += 1
                    dmg = max(1, round(f["dmg"] + rng.uniform(-1.5, 1.5)))
                    t["hp"] -= dmg
                    damage_taken += dmg
                    if t["hp"] <= 0:
                        down += 1
                        living_p = [p for p in party if p["hp"] > 0]

    won = any(f["curhp"] > 0 for f in foes) is False and any(p["hp"] > 0 for p in party)
    wiped = not any(p["hp"] > 0 for p in party)
    alive = sum(1 for p in party if p["hp"] > 0)
    hp_left = sum(max(0, p["hp"]) for p in party)
    hp_total = sum(p["maxhp"] for p in party)
    return {
        "won": won,
        "wiped": wiped,
        "rounds": rounds,
        "downed": down,
        "alive": alive,
        "hpPct": hp_left / hp_total if hp_total else 0,
        "damageDealt": damage_dealt,
        "damageTaken": damage_taken,
        "healing": healing,
        "hitRate": hits / attacks if attacks else 0,
        "rpSpent": rp_spent,
        "foeCount": len(foes),
        "budget": budget,
        "budgetSpent": sum(f["cost"] for f in foes),
        "rulesHalts": rules,
    }


def mean_ci(xs: list[float], z: float = 1.96) -> tuple[float, float, float]:
    m = statistics.mean(xs)
    if len(xs) < 2:
        return m, m, m
    sd = statistics.stdev(xs)
    half = z * sd / math.sqrt(len(xs))
    return m, m - half, m + half


def parse_matrix():
    rows = []
    with (PACK / "SCENARIO_MATRIX.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def expand(field: str) -> list:
    parts = [p.strip() for p in field.split("|")]
    out = []
    for p in parts:
        out.append(int(p) if p.isdigit() else p)
    return out


def main():
    os.makedirs(_win_long(PACK_OUT), exist_ok=True)
    os.makedirs(_win_long(SUITE_OUT), exist_ok=True)
    matrix = parse_matrix()
    all_findings = []
    rules_halts_global = []
    summary_rows = []

    for row in matrix:
        sid = row["scenario_id"]
        levels = expand(row["levels"])
        parties = expand(row["party_size_or_scope"])
        diffs = expand(row["difficulty_or_state"])
        runs = int(row["runs"])
        scenario_dir = PACK_OUT / sid
        os.makedirs(_win_long(scenario_dir), exist_ok=True)
        suite_scenario = SUITE_OUT / sid
        os.makedirs(_win_long(suite_scenario), exist_ok=True)

        cell_metrics = []
        scenario_halts = []
        for level in levels:
            for party_size in parties:
                for difficulty in diffs:
                    outcomes = []
                    for i in range(runs):
                        rng = random.Random(SEED0 + hash((sid, level, party_size, difficulty, i)) % 10_000_000)
                        outcomes.append(simulate(int(level), str(difficulty), int(party_size), rng))
                    wins = [1.0 if o["won"] else 0.0 for o in outcomes]
                    hp = [o["hpPct"] for o in outcomes]
                    downs = [float(o["downed"]) for o in outcomes]
                    rounds = [float(o["rounds"]) for o in outcomes]
                    hit_rates = [o["hitRate"] for o in outcomes]
                    heal = [float(o["healing"]) for o in outcomes]
                    dmg = [float(o["damageDealt"]) for o in outcomes]
                    rp = [float(o["rpSpent"]) for o in outcomes]
                    wipes = [1.0 if o["wiped"] else 0.0 for o in outcomes]
                    for o in outcomes:
                        scenario_halts.extend(o["rulesHalts"])

                    wr, wr_lo, wr_hi = mean_ci(wins)
                    cell = {
                        "level": int(level),
                        "partySize": int(party_size),
                        "difficulty": difficulty,
                        "runs": runs,
                        "winRate": round(wr, 4),
                        "winRateCI95": [round(wr_lo, 4), round(wr_hi, 4)],
                        "meanHpPct": round(mean_ci(hp)[0], 4),
                        "meanDowned": round(mean_ci(downs)[0], 3),
                        "meanRounds": round(mean_ci(rounds)[0], 3),
                        "meanHitRate": round(mean_ci(hit_rates)[0], 4),
                        "meanHealing": round(mean_ci(heal)[0], 2),
                        "meanDamageDealt": round(mean_ci(dmg)[0], 2),
                        "meanRpSpent": round(mean_ci(rp)[0], 2),
                        "wipeRate": round(mean_ci(wipes)[0], 4),
                        "budget": party_budget(str(difficulty), int(party_size)),
                    }
                    cell_metrics.append(cell)
                    summary_rows.append({"scenarioId": sid, **cell})

        # Band separation check within each (level, party)
        findings = []
        by_lp = {}
        for c in cell_metrics:
            by_lp.setdefault((c["level"], c["partySize"]), []).append(c)
        order = ["routine", "standard", "hard", "severe", "catastrophic"]
        for key, cells in by_lp.items():
            cells_sorted = sorted(cells, key=lambda c: order.index(c["difficulty"]) if c["difficulty"] in order else 99)
            for a, b in zip(cells_sorted, cells_sorted[1:]):
                # Expected: harder => lower winRate. Flag overlap of 95% CIs when winRate not decreasing.
                if a["winRate"] + 0.02 < b["winRate"]:
                    findings.append(
                        {
                            "severity": "confirmed",
                            "type": "difficulty_inversion",
                            "level": key[0],
                            "partySize": key[1],
                            "easier": a["difficulty"],
                            "harder": b["difficulty"],
                            "winRates": [a["winRate"], b["winRate"]],
                            "detail": "Harder budget band produced higher win rate than easier band.",
                        }
                    )
                elif a["winRateCI95"][0] <= b["winRateCI95"][1] and abs(a["winRate"] - b["winRate"]) < 0.05:
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "band_collapse",
                            "level": key[0],
                            "partySize": key[1],
                            "pair": [a["difficulty"], b["difficulty"]],
                            "winRates": [a["winRate"], b["winRate"]],
                            "detail": "Adjacent difficulty bands have overlapping outcomes (<5pp separation).",
                        }
                    )
            # Absolute calibration anchors (chassis expectations)
            for c in cells_sorted:
                if c["difficulty"] == "routine" and c["winRate"] < 0.85:
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "routine_too_deadly",
                            "cell": c,
                            "detail": "Routine win rate below 85% on chassis proxy.",
                        }
                    )
                if c["difficulty"] == "catastrophic" and c["winRate"] > 0.55:
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "catastrophic_too_easy",
                            "cell": c,
                            "detail": "Catastrophic win rate above 55% on chassis proxy.",
                        }
                    )
                if c["difficulty"] == "standard" and not (0.55 <= c["winRate"] <= 0.92):
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "standard_off_band",
                            "cell": c,
                            "detail": "Standard win rate outside 55–92% chassis expectation window.",
                        }
                    )

        # Deduplicate halts
        halt_keys = set()
        uniq_halts = []
        for h in scenario_halts:
            k = (h.get("topic"), h.get("detail"))
            if k not in halt_keys:
                halt_keys.add(k)
                uniq_halts.append(h)

        # Survival / resource curve finding across levels (same difficulty)
        for difficulty in diffs:
            series = [c for c in cell_metrics if c["difficulty"] == difficulty and c["partySize"] == parties[0]]
            series = sorted(series, key=lambda c: c["level"])
            if len(series) >= 3:
                wrs = [c["winRate"] for c in series]
                if max(wrs) - min(wrs) > 0.35:
                    findings.append(
                        {
                            "severity": "suspected",
                            "type": "level_curve_instability",
                            "difficulty": difficulty,
                            "levels": [c["level"] for c in series],
                            "winRates": wrs,
                            "detail": "Win rate swings >35pp across levels at fixed difficulty (chassis may need level-scaled budget review).",
                        }
                    )

        outcome = "PASS"
        if any(f["severity"] == "confirmed" for f in findings):
            outcome = "FAIL"
        elif findings:
            outcome = "WARN"

        record = {
            "pack": "07-statistical-combat-calibration",
            "scenarioId": sid,
            "runId": f"{sid}-{SEED0}",
            "seed": SEED0,
            "sourceHash": SOURCE_HASH,
            "fixtureHash": hashlib.sha256(json.dumps(cell_metrics, sort_keys=True).encode()).hexdigest(),
            "evidenceLevel": "A",
            "outcome": outcome,
            "metrics": {
                "cells": cell_metrics,
                "cellCount": len(cell_metrics),
                "runsPerCell": runs,
                "objective": row["objective"],
            },
            "rulesHalts": uniq_halts,
            "findings": findings,
            "rawEvidencePath": f"results/07-statistical-combat-calibration/{sid}/",
        }
        out_path = scenario_dir / "summary.json"
        write_json(out_path, record)
        write_json(suite_scenario / "summary.json", record)
        # Compact per-cell CSV
        with open(_win_long(scenario_dir / "cells.csv"), "w", newline="", encoding="utf-8") as f:
            if cell_metrics:
                w = csv.DictWriter(f, fieldnames=list(cell_metrics[0].keys()))
                w.writeheader()
                w.writerows(cell_metrics)
        all_findings.extend(findings)
        rules_halts_global.extend(uniq_halts)

    # Suite rollup
    rollup = {
        "pack": "07-statistical-combat-calibration",
        "scenarioId": "PACK07-ROLLUP",
        "runId": f"PACK07-{SEED0}",
        "seed": SEED0,
        "sourceHash": SOURCE_HASH,
        "fixtureHash": None,
        "evidenceLevel": "A",
        "outcome": "FAIL" if any(f.get("severity") == "confirmed" for f in all_findings) else ("WARN" if all_findings else "PASS"),
        "metrics": {"scenarioCount": len(matrix), "summaryRows": len(summary_rows), "findingCount": len(all_findings)},
        "rulesHalts": rules_halts_global,
        "findings": all_findings[:200],
        "rawEvidencePath": "results/07-statistical-combat-calibration/",
    }
    write_json(SUITE_OUT / "rollup.json", rollup)
    write_json(PACK_OUT / "rollup.json", rollup)
    with open(_win_long(SUITE_OUT / "all_cells.csv"), "w", newline="", encoding="utf-8") as f:
        if summary_rows:
            w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
            w.writeheader()
            w.writerows(summary_rows)
    print(json.dumps({"pack": "07", "scenarios": len(matrix), "cells": len(summary_rows), "findings": len(all_findings), "halts": len(rules_halts_global)}, indent=2))


if __name__ == "__main__":
    main()
