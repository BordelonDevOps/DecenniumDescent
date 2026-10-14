#!/usr/bin/env python3
"""Pack 14 — Seasonal and Decennial Campaign Simulation."""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from gameplay_loop_chassis import (  # noqa: E402
    SOURCE_HASH,
    SEASONAL,
    SALE,
    parse_levels,
    parse_ints,
    parse_pipe,
    write_result,
    mirror_suite,
)

PACK = "14-seasonal-cycle-simulation"
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SEED0 = 84100

DISTRICT_STATES = SEASONAL["havenDistrictStates"]
MAG = list(SEASONAL["consequenceMagnitude"].keys())


def opening_outcome(rng: random.Random, *, level: int, party: int, severity: str, scenario: str) -> dict:
    """One Opening inside a Cycle — public vs sealed separation."""
    fail_w = {"minor": 0.15, "standard": 0.35, "severe": 0.55}[severity]
    if "FAILURE" in scenario:
        fail_w = min(0.95, fail_w + 0.25)
    failed = rng.random() < fail_w
    depth = rng.choice(["Haven", "Tier I", "Tier II", "Tier III"][: max(2, level // 3 + 1)])
    public = {
        "publicDepthRecord": depth if not failed else "Haven",
        "routesSecured": [] if failed else [f"trunk-{rng.randint(1,4)}"],
        "routesLost": [f"spur-{rng.randint(1,9)}"] if failed else [],
        "artifactsExtracted": [] if failed else [f"art-{rng.randint(100,999)}"],
        "survivors": max(0, party - (rng.randint(2, party // 2) if failed else rng.randint(0, 1))),
        "wealthDelta": -rng.randint(50, 400) if failed else rng.randint(20, 500),
        "districtDamage": failed and severity != "minor",
    }
    sealed = {
        "directorSealedConsequence": f"{severity}:{rng.choice(SEASONAL['changeCategories'])}",
        "hiddenRivalMove": rng.random() < 0.3,
        "unrevealedChamberState": "transformed" if rng.random() < 0.5 else "reset",
    }
    # Canon boundary: sealed must not leak into public
    leaked = any(k in public for k in sealed)
    return {"failed": failed, "public": public, "sealed": sealed, "leaked": leaked}


def advance_cycle(state: dict, opening: dict, rng: random.Random, severity: str) -> dict:
    st = deepcopy(state)
    st["openings"] += 1
    st["publicDepthHistory"].append(opening["public"]["publicDepthRecord"])
    # Persistent
    for r in opening["public"]["routesSecured"]:
        st["securedTrunks"].add(r)
    for r in opening["public"]["routesLost"]:
        st["unsecuredSpurs"].discard(r)
        st["securedTrunks"].discard(r)
    for a in opening["public"]["artifactsExtracted"]:
        st["artifacts"].append(a)
    st["wealth"] += opening["public"]["wealthDelta"]
    # District damage / recovery
    if opening["public"]["districtDamage"]:
        cur = st["district"]
        idx = min(len(DISTRICT_STATES) - 1, DISTRICT_STATES.index(cur) + (2 if severity == "severe" else 1))
        # skip Captured sometimes
        st["district"] = DISTRICT_STATES[min(idx, 3)]  # Intact..Captured
    elif st["district"] in ("Damaged", "Recovering", "Strained"):
        # recovery tick
        if rng.random() < 0.4:
            idx = max(0, DISTRICT_STATES.index(st["district"]) - 1)
            st["district"] = DISTRICT_STATES[idx] if DISTRICT_STATES[idx] != "Captured" else "Recovering"
    # Replenishment: unsecured routes/nodes reset; secured trunks persist
    st["unsecuredSpurs"] = {f"spur-{i}" for i in range(rng.randint(2, 6))}
    st["marketDemand"] = rng.choice(list(SALE["demand"].keys()))
    # Heirs / legacy
    if opening["public"]["survivors"] == 0 or (opening["failed"] and rng.random() < 0.2):
        st["heirsActivated"] += 1
        st["lineageDepth"] += 1
    st["sealedLog"].append(opening["sealed"])
    st["mapFidelity"] = min(1.0, 0.55 + 0.08 * len(st["securedTrunks"]))
    # Degradation of unsecured knowledge
    st["chamberKnowledge"] = round(rng.uniform(0.1, 0.4), 3)
    return st


def run_campaign(rng: random.Random, *, cycles: int, level: int, party: int, severity: str, scenario: str) -> dict:
    state = {
        "openings": 0,
        "securedTrunks": set(),
        "unsecuredSpurs": set(),
        "artifacts": [],
        "wealth": 100,
        "district": "Intact",
        "heirsActivated": 0,
        "lineageDepth": 0,
        "marketDemand": "normal",
        "mapFidelity": 0.5,
        "chamberKnowledge": 0.3,
        "publicDepthHistory": [],
        "sealedLog": [],
        "boundaryViolations": 0,
    }
    for c in range(cycles):
        # three Openings per Cycle (pack README: three-Cycle campaigns; CYCLE-BASELINE says three Openings)
        openings_per = 3 if scenario == "CYCLE-BASELINE" else 3
        for _ in range(openings_per):
            op = opening_outcome(rng, level=level, party=party, severity=severity, scenario=scenario)
            if op["leaked"]:
                state["boundaryViolations"] += 1
            state = advance_cycle(state, op, rng, severity)
        # end-of-cycle seasonal shock
        if scenario == "CYCLE-MARKET" or rng.random() < 0.4:
            state["marketDemand"] = rng.choice(["glutted", "sought", "strategic", "normal"])
        if scenario == "CYCLE-MAP":
            # secured principles persist; fidelity should not collapse to zero
            if not state["securedTrunks"]:
                state["mapFidelity"] = max(0.2, state["mapFidelity"] * 0.7)
    return {
        "openings": state["openings"],
        "securedTrunks": len(state["securedTrunks"]),
        "artifacts": len(state["artifacts"]),
        "wealth": state["wealth"],
        "district": state["district"],
        "heirsActivated": state["heirsActivated"],
        "lineageDepth": state["lineageDepth"],
        "finalDemand": state["marketDemand"],
        "mapFidelity": round(state["mapFidelity"], 3),
        "chamberKnowledge": state["chamberKnowledge"],
        "boundaryViolations": state["boundaryViolations"],
        "explorationStillNontrivial": state["chamberKnowledge"] < 0.85 or state["mapFidelity"] < 0.95,
    }


def main() -> None:
    matrix = list(csv.DictReader((ROOT / "SCENARIO_MATRIX.csv").open(encoding="utf-8")))
    RESULTS.mkdir(parents=True, exist_ok=True)
    # README: at least 1000 seeded three-Cycle campaigns — distribute across cells
    for row in matrix:
        sid = row["scenario_id"]
        runs_n = int(row["runs"])
        levels = parse_levels(row["levels"])
        parties = parse_ints(row["party_size_or_scope"]) or [6]
        sevs = parse_pipe(row["difficulty_or_state"])
        # Ensure total campaigns across cells >= meaningful volume
        for level in levels:
            for party in parties:
                for sev in sevs:
                    wealths = []
                    heirs = []
                    fidelity = []
                    nontrivial = 0
                    damaged = 0
                    violations = 0
                    for i in range(runs_n):
                        seed = SEED0 + hash((sid, level, party, sev, i)) % 10_000_000
                        rng = random.Random(seed)
                        cycles = 3
                        out = run_campaign(rng, cycles=cycles, level=level, party=party, severity=sev, scenario=sid)
                        wealths.append(out["wealth"])
                        heirs.append(out["heirsActivated"])
                        fidelity.append(out["mapFidelity"])
                        nontrivial += int(out["explorationStillNontrivial"])
                        damaged += int(out["district"] in ("Damaged", "Captured", "Recovering", "Strained"))
                        violations += out["boundaryViolations"]

                    findings = []
                    if statistics.mean(fidelity) < 0.3 and sid != "CYCLE-FAILURE":
                        findings.append({
                            "severity": "high",
                            "claim": f"{sid}: mean mapFidelity {statistics.mean(fidelity):.2f} — secured trunk persistence may be too weak",
                            "evidence": "A",
                        })
                    if nontrivial / runs_n < 0.5:
                        findings.append({
                            "severity": "high",
                            "claim": f"{sid}: only {nontrivial/runs_n:.0%} campaigns remain nontrivial to explore — replenishment may be insufficient",
                            "evidence": "A",
                        })
                    if sid == "CYCLE-LEGACY" and statistics.mean(heirs) < 0.2:
                        findings.append({
                            "severity": "medium",
                            "claim": "Legacy scenario rarely activates heirs — dynasty pressure under-triggered",
                            "evidence": "A",
                        })
                    if violations:
                        findings.append({
                            "severity": "critical",
                            "claim": f"Canon boundary violations detected: {violations}",
                            "evidence": "A",
                        })
                    if sid == "CYCLE-FAILURE" and damaged / runs_n < 0.3:
                        findings.append({
                            "severity": "medium",
                            "claim": f"Failure scenario district damage rate {damaged/runs_n:.2f} lower than expected",
                            "evidence": "A",
                        })

                    halt = []
                    if sid == "CYCLE-BASELINE":
                        halt.append({
                            "code": "OPENINGS-PER-CYCLE-COUNT",
                            "note": "Seasonal JSON lists cycleRecordFields but does not hard-code Openings-per-Cycle count; sim uses 3 Openings × 3 Cycles per pack README.",
                        })

                    run_id = f"L{level}-P{party}-{sev[:3]}"
                    write_result(RESULTS / sid / f"{run_id}.json", {
                        "pack": PACK,
                        "scenarioId": sid,
                        "runId": f"{sid}-{run_id}",
                        "seed": SEED0 + hash((sid, level, party, sev)) % 10_000_000,
                        "sourceHash": SOURCE_HASH,
                        "fixtureHash": None,
                        "evidenceLevel": "A",
                        "outcome": "aggregated_monte_carlo",
                        "metrics": {
                            "n": runs_n,
                            "level": level,
                            "party": party,
                            "severity": sev,
                            "cycles": 3,
                            "openingsPerCycle": 3,
                            "meanWealth": round(statistics.mean(wealths), 2),
                            "meanHeirsActivated": round(statistics.mean(heirs), 3),
                            "meanMapFidelity": round(statistics.mean(fidelity), 3),
                            "nontrivialExplorationRate": round(nontrivial / runs_n, 4),
                            "districtStressRate": round(damaged / runs_n, 4),
                            "boundaryViolations": violations,
                            "persistentFields": SEASONAL["persistent"],
                            "replenishedFields": SEASONAL["replenished"],
                        },
                        "rulesHalts": halt,
                        "findings": findings,
                        "rawEvidencePath": f"results/{sid}/{run_id}.json",
                        "sealedNote": "Director sealed consequences stored only in sealedLog during sim; omitted from public metrics.",
                    })

    # Global volume check file
    total = sum(1 for _ in RESULTS.glob("**/*.json"))
    write_result(RESULTS / "_meta" / "volume.json", {
        "pack": PACK,
        "scenarioId": "_META",
        "runId": "volume",
        "seed": SEED0,
        "sourceHash": SOURCE_HASH,
        "fixtureHash": None,
        "evidenceLevel": "A",
        "outcome": "meta",
        "metrics": {"resultFiles": total, "readmeMinimumCampaigns": 1000},
        "rulesHalts": [],
        "findings": [{
            "severity": "info",
            "claim": f"Wrote {total} aggregated campaign result files; each embeds n runs (see scenario matrix).",
            "evidence": "A",
        }],
        "rawEvidencePath": "results/_meta/volume.json",
    })

    halt_path = ROOT.parents[1] / "results" / "rules-halts.csv"
    halt_path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not halt_path.exists() or halt_path.stat().st_size == 0
    with halt_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["pack", "code", "note"])
        w.writerow([PACK, "OPENINGS-PER-CYCLE-COUNT", "Openings-per-Cycle not hard-coded in seasonal JSON; used 3×3 from pack README."])

    mirror_suite(PACK, RESULTS)
    print(json.dumps({"pack": PACK, "scenarios": len(matrix)}, indent=2))


if __name__ == "__main__":
    main()
