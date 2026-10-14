#!/usr/bin/env python3
"""Pack 11 — Expedition Attrition Monte Carlo."""
from __future__ import annotations

import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from gameplay_loop_chassis import (  # noqa: E402
    SOURCE_HASH,
    POLICIES,
    MAPPING_NORM,
    parse_levels,
    parse_ints,
    parse_pipe,
    simulate_expedition,
    summarize,
    write_result,
    mirror_suite,
)

PACK = "11-expedition-attrition-monte-carlo"
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SEED0 = 81100


def mappings_for(cell: str) -> list[str]:
    parts = parse_pipe(cell)
    out = []
    for p in parts:
        if p.lower() == "all":
            return ["Secured", "Mapped", "Sketched", "Unknown"]
        out.append(MAPPING_NORM.get(p.lower(), p.capitalize()))
    return out


def main() -> None:
    matrix = list(csv.DictReader((ROOT / "SCENARIO_MATRIX.csv").open(encoding="utf-8")))
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_halts = []
    findings = []

    for row in matrix:
        sid = row["scenario_id"]
        runs_n = int(row["runs"])
        levels = parse_levels(row["levels"])
        parties = parse_ints(row["party_size_or_scope"]) or [6]
        maps = mappings_for(row["difficulty_or_state"])
        objective = row["objective"]
        cells = []
        for level in levels:
            for party in parties:
                for mapping in maps:
                    for policy in POLICIES:
                        runs = []
                        for i in range(runs_n):
                            seed = SEED0 + hash((sid, level, party, mapping, policy, i)) % 10_000_000
                            rng = random.Random(seed)
                            kwargs = dict(
                                level=level,
                                party=party,
                                mapping=mapping,
                                policy_name=policy,
                                sustenance=2 if policy != "aggressive" else 1,
                                objective=objective,
                                casualty_start=1 if sid == "EXP-CASUALTY" else 0,
                                forced_rest_interrupt=(sid == "EXP-REST-DEBT"),
                                max_watches=40 if sid == "EXP-DEEP" else 32,
                            )
                            runs.append(simulate_expedition(rng, **kwargs))
                        metrics = summarize(runs)
                        metrics.update({
                            "level": level, "party": party, "mapping": mapping, "policy": policy,
                            "objective": objective, "requestedRuns": runs_n,
                        })
                        # sample ledger from first successful-ish run
                        sample = next((r for r in runs if r.haven), runs[0])
                        seed_s = SEED0 + hash((sid, level, party, mapping, policy, 0)) % 10_000_000
                        cell_halts = []
                        for r in runs:
                            cell_halts.extend(r.rules_halts)
                        # unique
                        seen = set()
                        uniq = []
                        for h in cell_halts:
                            if h["code"] not in seen:
                                seen.add(h["code"])
                                uniq.append(h)
                        all_halts.extend(uniq)

                        cell_findings = []
                        if metrics["wipeRate"] > 0.25:
                            cell_findings.append({
                                "severity": "high",
                                "claim": f"{sid}/{policy}/{mapping}/L{level}/P{party}: wipeRate {metrics['wipeRate']} exceeds 25%",
                                "evidence": "A",
                            })
                        if metrics["havenRate"] < 0.4 and sid != "EXP-ABORT":
                            cell_findings.append({
                                "severity": "high",
                                "claim": f"{sid}/{policy}/{mapping}: havenRate {metrics['havenRate']} below 40%",
                                "evidence": "A",
                            })
                        if metrics["profitLossRate"] > 0.7 and metrics["havenRate"] > 0.5:
                            cell_findings.append({
                                "severity": "medium",
                                "claim": f"{sid}/{policy}: haven arrivals still lose money {metrics['profitLossRate']} of the time (true profit after wages/shares)",
                                "evidence": "A",
                            })
                        if mapping == "Unknown" and metrics["objectiveRate"] < 0.15:
                            cell_findings.append({
                                "severity": "medium",
                                "claim": f"{sid}/Unknown: objectiveRate {metrics['objectiveRate']} — progressPerWatch=0 without Map Route success",
                                "evidence": "A",
                            })
                        if policy == "cautious" and policy != "aggressive":
                            pass
                        findings.extend(cell_findings)

                        # Short names — Windows path length under deep lab nest
                        pol = {"cautious": "cau", "balanced": "bal", "aggressive": "agg"}[policy]
                        mp = {"Secured": "sec", "Mapped": "map", "Sketched": "sk", "Unknown": "unk"}[mapping]
                        run_id = f"{pol}-L{level}-P{party}-{mp}"
                        payload = {
                            "pack": PACK,
                            "scenarioId": sid,
                            "runId": f"{sid}-{run_id}",
                            "seed": seed_s,
                            "sourceHash": SOURCE_HASH,
                            "fixtureHash": None,
                            "evidenceLevel": "A",
                            "outcome": "aggregated_monte_carlo",
                            "metrics": metrics,
                            "rulesHalts": uniq,
                            "findings": cell_findings,
                            "rawEvidencePath": f"results/{sid}/{run_id}.json",
                            "sampleLedger": sample.ledger[:12] if hasattr(sample, "ledger") else [],
                        }
                        # re-sim one with ledger
                        rng2 = random.Random(seed_s)
                        sample2 = simulate_expedition(rng2, record_ledger=True, **{
                            "level": level, "party": party, "mapping": mapping, "policy_name": policy,
                            "sustenance": 2 if policy != "aggressive" else 1, "objective": objective,
                            "casualty_start": 1 if sid == "EXP-CASUALTY" else 0,
                            "forced_rest_interrupt": sid == "EXP-REST-DEBT",
                            "max_watches": 40 if sid == "EXP-DEEP" else 32,
                        })
                        payload["sampleLedger"] = sample2.ledger
                        write_result(RESULTS / sid / f"{run_id}.json", payload)
                        cells.append(metrics)

        # scenario rollup
        if cells:
            rollup = {
                "pack": PACK,
                "scenarioId": sid,
                "runId": f"{sid}-ROLLUP",
                "seed": SEED0,
                "sourceHash": SOURCE_HASH,
                "fixtureHash": None,
                "evidenceLevel": "A",
                "outcome": "scenario_rollup",
                "metrics": {
                    "cells": len(cells),
                    "meanHavenRate": round(sum(c["havenRate"] for c in cells) / len(cells), 4),
                    "meanWipeRate": round(sum(c["wipeRate"] for c in cells) / len(cells), 4),
                    "meanObjectiveRate": round(sum(c["objectiveRate"] for c in cells) / len(cells), 4),
                    "meanTrueProfit": round(sum(c["meanTrueProfit"] for c in cells) / len(cells), 2),
                    "meanProfitLossRate": round(sum(c["profitLossRate"] for c in cells) / len(cells), 4),
                    "totalRuns": sum(c["n"] for c in cells),
                },
                "rulesHalts": [],
                "findings": [{
                    "severity": "info",
                    "claim": f"{sid} rollup across {len(cells)} policy/mapping/level cells",
                    "evidence": "A",
                }],
                "rawEvidencePath": f"results/{sid}/ROLLUP.json",
            }
            write_result(RESULTS / sid / "ROLLUP.json", rollup)

    # policy comparison finding
    findings.append({
        "severity": "info",
        "claim": "Cautious vs aggressive policies diverge on wipe vs profit — see cell JSONs; attrition systems create meaningful long-form tradeoffs under Mapped/Sketched but Unknown is near-dead without Map Route.",
        "evidence": "A",
    })

    # suite rules-halts append
    halt_path = ROOT.parents[1] / "results" / "rules-halts.csv"
    halt_path.parent.mkdir(parents=True, exist_ok=True)
    with halt_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if halt_path.stat().st_size == 0:
            w.writerow(["pack", "code", "note"])
        seen = set()
        for h in all_halts:
            key = h["code"]
            if key in seen:
                continue
            seen.add(key)
            w.writerow([PACK, h["code"], h["note"]])

    mirror_suite(PACK, RESULTS)
    print(json.dumps({"pack": PACK, "scenarios": len(matrix), "findings": len(findings)}, indent=2))


if __name__ == "__main__":
    main()
