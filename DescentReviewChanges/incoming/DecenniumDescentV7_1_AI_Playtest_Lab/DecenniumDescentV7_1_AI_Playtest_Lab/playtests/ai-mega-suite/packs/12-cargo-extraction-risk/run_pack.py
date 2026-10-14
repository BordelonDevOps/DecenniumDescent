#!/usr/bin/env python3
"""Pack 12 — Cargo and Extraction Risk Calibration."""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from gameplay_loop_chassis import (  # noqa: E402
    SOURCE_HASH,
    POLICIES,
    parse_levels,
    parse_ints,
    parse_pipe,
    simulate_expedition,
    write_result,
    mirror_suite,
)

PACK = "12-cargo-extraction-risk"
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SEED0 = 82100


def main() -> None:
    matrix = list(csv.DictReader((ROOT / "SCENARIO_MATRIX.csv").open(encoding="utf-8")))
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_halts = []

    for row in matrix:
        sid = row["scenario_id"]
        runs_n = int(row["runs"])
        levels = parse_levels(row["levels"])
        parties = parse_ints(row["party_size_or_scope"]) or [6]
        ecs = parse_ints(row["difficulty_or_state"])
        objective = row["objective"]
        mapping = "Unknown" if sid == "CARGO-UNKNOWN" else ("Sketched" if "ATTENTION" in sid else "Mapped")
        casualty = 1 if sid == "CARGO-CASUALTY" else 0

        for level in levels:
            for party in parties:
                for ec in ecs:
                    for policy in ("cautious", "balanced", "aggressive"):
                        retained_frac = []
                        profits = []
                        loss_events = []
                        delays = []
                        casualties = []
                        haven_n = 0
                        rules = []
                        for i in range(runs_n):
                            seed = SEED0 + hash((sid, level, party, ec, policy, i)) % 10_000_000
                            rng = random.Random(seed)
                            r = simulate_expedition(
                                rng,
                                level=level,
                                party=party,
                                mapping=mapping,
                                policy_name=policy,
                                objective=objective,
                                attention_ec=ec,
                                casualty_start=casualty,
                                max_watches=28,
                            )
                            rules.extend(r.rules_halts)
                            if r.haven:
                                haven_n += 1
                            out_load = max(1, r.cargo_load_out)
                            retained_frac.append(r.cargo_load_haven / out_load)
                            profits.append(r.true_profit)
                            loss_events.append(1 if r.cargo_load_haven < r.cargo_load_out else 0)
                            delays.append(r.extraction_fails)
                            casualties.append(r.casualties + r.deaths)

                        # unique halts
                        seen = set()
                        uniq = []
                        for h in rules:
                            if h["code"] not in seen:
                                seen.add(h["code"])
                                uniq.append(h)
                        all_halts.extend(uniq)

                        metrics = {
                            "n": runs_n,
                            "level": level,
                            "party": party,
                            "extractionClass": ec,
                            "policy": policy,
                            "mapping": mapping,
                            "havenRate": round(haven_n / runs_n, 4),
                            "meanRetainedLoadFrac": round(statistics.mean(retained_frac), 4),
                            "medianRetainedLoadFrac": round(statistics.median(retained_frac), 4),
                            "cargoLossRate": round(statistics.mean(loss_events), 4),
                            "meanExtractionFailCount": round(statistics.mean(delays), 3),
                            "meanCasualties": round(statistics.mean(casualties), 3),
                            "meanTrueProfit": round(statistics.mean(profits), 2),
                            "medianTrueProfit": round(statistics.median(profits), 2),
                            "profitP10": round(sorted(profits)[max(0, runs_n // 10)], 2),
                            "profitP90": round(sorted(profits)[min(runs_n - 1, 9 * runs_n // 10)], 2),
                        }
                        findings = []
                        # Rational tradeoff checks
                        if ec >= 4 and metrics["meanRetainedLoadFrac"] > 0.95 and metrics["havenRate"] > 0.85:
                            findings.append({
                                "severity": "high",
                                "claim": f"EC{ec} Attention/strategic cargo retains {metrics['meanRetainedLoadFrac']} with haven {metrics['havenRate']} — risk may be underweighted vs ordinary salvage",
                                "evidence": "A",
                            })
                        if ec <= 1 and metrics["cargoLossRate"] > 0.5:
                            findings.append({
                                "severity": "medium",
                                "claim": f"Light EC{ec} cargo loss rate {metrics['cargoLossRate']} unexpectedly high under {mapping}/{policy}",
                                "evidence": "A",
                            })
                        if sid == "CARGO-CASUALTY" and metrics["meanRetainedLoadFrac"] < 0.3:
                            findings.append({
                                "severity": "medium",
                                "claim": "Casualty+cargo runs abandon most load — Living priority-5 still lost when extraction crit-fails dump two lots",
                                "evidence": "A",
                            })
                        if metrics["profitP90"] - metrics["profitP10"] < 50 and ec >= 4:
                            findings.append({
                                "severity": "medium",
                                "claim": f"EC{ec} profit spread P90-P10={metrics['profitP90']-metrics['profitP10']:.0f} looks compressed — outcomes may be too arbitrary or too flat",
                                "evidence": "A",
                            })

                        pol = {"cautious": "cau", "balanced": "bal", "aggressive": "agg"}[policy]
                        run_id = f"{pol}-L{level}-P{party}-E{ec}"
                        write_result(RESULTS / sid / f"{run_id}.json", {
                            "pack": PACK,
                            "scenarioId": sid,
                            "runId": f"{sid}-{run_id}",
                            "seed": SEED0 + hash((sid, level, party, ec, policy)) % 10_000_000,
                            "sourceHash": SOURCE_HASH,
                            "fixtureHash": None,
                            "evidenceLevel": "A",
                            "outcome": "aggregated_monte_carlo",
                            "metrics": metrics,
                            "rulesHalts": uniq,
                            "findings": findings,
                            "rawEvidencePath": f"results/{sid}/{run_id}.json",
                        })

    halt_path = ROOT.parents[1] / "results" / "rules-halts.csv"
    halt_path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not halt_path.exists() or halt_path.stat().st_size == 0
    with halt_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["pack", "code", "note"])
        seen = set()
        for h in all_halts:
            if h["code"] in seen:
                continue
            seen.add(h["code"])
            w.writerow([PACK, h["code"], h["note"]])

    mirror_suite(PACK, RESULTS)
    print(json.dumps({"pack": PACK, "scenarios": len(matrix)}, indent=2))


if __name__ == "__main__":
    main()
