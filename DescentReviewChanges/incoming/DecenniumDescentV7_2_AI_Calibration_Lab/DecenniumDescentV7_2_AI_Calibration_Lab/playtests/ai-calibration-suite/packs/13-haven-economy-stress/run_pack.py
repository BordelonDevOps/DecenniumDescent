#!/usr/bin/env python3
"""Pack 13 — Haven Economy Stress Test (executable settlement formulas)."""
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
    GAME,
    SPONSOR,
    SALE,
    TAX,
    HEAT,
    COIN,
    LABOR,
    COMMODITY,
    REP_MIN,
    REP_MAX,
    parse_ints,
    parse_pipe,
    write_result,
    mirror_suite,
)

PACK = "13-haven-economy-stress"
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SEED0 = 83100

SPONSOR_MAP = {
    "self": "self",
    "guild": "guild",
    "bank": "merchantOrBank",
    "noble": "nobleOrTemple",
    "sovereign": "sovereign",
}


def settle_sale(rng: random.Random, *, base: float, sponsor_key: str, demand_key: str,
                provenance="documented", condition="sound", urgency="normal",
                tax_key="routineRegisteredGoods", wages=0.0, replacement=0.0,
                debt_service=0.0) -> dict:
    gross = base * SALE["provenance"][provenance] * SALE["demand"][demand_key] * SALE["condition"][condition] * SALE["urgency"][urgency]
    share = SPONSOR[sponsor_key]
    taxes = gross * TAX[tax_key]
    net = gross * (1 - share) - taxes
    true = net - wages - replacement - debt_service
    return {
        "gross": round(gross, 2),
        "taxes": round(taxes, 2),
        "sponsorShare": share,
        "netAfterSponsor": round(net, 2),
        "trueProfit": round(true, 2),
    }


def assay_coin(rng: random.Random, quality: str, amount: float) -> dict:
    """quality: clean|shaved|counterfeit"""
    fee = max(COIN["minimumFeeGp"], amount * COIN["assayFee"])
    remint = 0.0
    detected = False
    loss = 0.0
    rules = []
    if quality == "clean":
        return {"fee": round(fee, 2), "remint": 0, "detected": False, "loss": 0, "net": round(amount - fee, 2), "rulesHalts": rules}
    # Assayer check vs DC
    dc = {"shaved": COIN["dcs"]["obviousShaving"], "counterfeit": COIN["dcs"]["platedOrSophisticatedCounterfeit"]}[quality]
    roll = rng.randint(1, 20) + 5  # trained assayer
    detected = roll >= dc
    if detected:
        if quality == "shaved":
            loss = amount * 0.08
            remint = amount * COIN["remintFee"]
        else:
            loss = amount * 0.5  # seized / worthless — seizure fraction underspecified
            rules.append({
                "code": "COUNTERFEIT-SEIZURE-FRACTION",
                "note": "coinAssay defines DCs and fees but not seizure/forfeiture fraction on detected counterfeit; sim uses 50% value loss proxy.",
            })
            remint = 0
    else:
        # undetected bad coin circulates — later Heat/reputation risk externalized
        loss = 0
    return {
        "fee": round(fee, 2),
        "remint": round(remint, 2),
        "detected": detected,
        "loss": round(loss, 2),
        "net": round(amount - fee - remint - loss, 2),
        "dc": dc,
        "roll": roll,
        "rulesHalts": rules,
    }


def heat_tick(rng: random.Random, heat: int, bribe: str | None = None) -> dict:
    h = heat
    if bribe == "tenPercent":
        h = max(HEAT["bribes"]["floorWhileActive"], h + HEAT["bribes"]["tenPercent"])
    elif bribe == "twentyFivePercent":
        h = max(HEAT["bribes"]["floorWhileActive"], h + HEAT["bribes"]["twentyFivePercent"])
    h = max(HEAT["minimum"], min(HEAT["maximum"], h))
    complication = False
    if h > 0:
        complication = (h >= 6) or (rng.randint(1, 6) <= h)
    return {"heat": h, "complication": complication}


def debt_cycle(rng: random.Random, principal: float, term: str, opening_rate: float | None = None) -> dict:
    # Interest cap per Opening 0.1
    cap = LABOR["debtInterestCapPerOpening"]
    rate = opening_rate if opening_rate is not None else {"short": 0.05, "medium": 0.08, "long": 0.1}[term]
    if rate > cap:
        rules = [{
            "code": "DEBT-INTEREST-OVER-CAP",
            "note": f"Requested rate {rate} exceeds debtInterestCapPerOpening {cap}; clamped.",
        }]
        rate = cap
    else:
        rules = []
    openings = {"short": 1, "medium": 3, "long": 6}[term]
    interest = 0.0
    bal = principal
    defaulted = False
    for _ in range(openings):
        interest += bal * rate
        bal += bal * rate
        # payment ability shock
        if rng.random() < (0.08 if term == "long" else 0.04):
            defaulted = True
            break
    collateral_seized = defaulted and term != "short"
    rep_hit = -2 if defaulted else (0 if interest < principal * 0.15 else -1)
    return {
        "rate": rate,
        "openings": openings,
        "interestAccrued": round(interest, 2),
        "balance": round(bal, 2),
        "defaulted": defaulted,
        "collateralSeized": collateral_seized,
        "reputationDelta": rep_hit,
        "rulesHalts": rules,
    }


def faction_access(rep: int) -> dict:
    labels = GAME["reputation"]["labels"]
    key = str(rep)
    # Thresholds inferred — exact shop/license gates not fully numeric in JSON
    access = {
        "marketDesk": rep >= -1,
        "licensedMaterials": rep >= 0,
        "strategicAuctions": rep >= 2,
        "sovereignContracts": rep >= 4,
        "proscribed": rep <= -4,
    }
    halt = {
        "code": "FACTION-ACCESS-THRESHOLDS",
        "note": "reputation labels exist (-5..+5) but numeric access gates for desks/licenses are not fully tabulated in Gameplay Loop JSON; sim uses inferred thresholds.",
    }
    return {"rep": rep, "label": labels.get(key, "?"), "access": access, "rulesHalts": [halt]}


def main() -> None:
    matrix = list(csv.DictReader((ROOT / "SCENARIO_MATRIX.csv").open(encoding="utf-8")))
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_halts = []

    for row in matrix:
        sid = row["scenario_id"]
        runs_n = int(row["runs"])
        states = parse_pipe(row["difficulty_or_state"])
        parties = parse_ints(row["party_size_or_scope"])

        if sid == "HAVEN-CHARTER":
            for party in parties or [6]:
                for st in states:
                    sk = SPONSOR_MAP[st]
                    profits = []
                    loss = 0
                    rules = []
                    for i in range(runs_n):
                        rng = random.Random(SEED0 + hash((sid, party, st, i)) % 10_000_000)
                        success = rng.random() < 0.55
                        base = rng.choice([100, 250, 500, 1000, 2500, 5000, 10000])
                        if not success:
                            base *= rng.uniform(0.1, 0.4)
                        wages = LABOR["dailyWagesGp"]["skilled"] * party * rng.randint(2, 10)
                        replacement = 0 if success else rng.randint(100, 800)
                        s = settle_sale(rng, base=base, sponsor_key=sk, demand_key=rng.choice(list(SALE["demand"])),
                                        tax_key=rng.choice(list(TAX)), wages=wages, replacement=replacement)
                        profits.append(s["trueProfit"])
                        if s["trueProfit"] < 0:
                            loss += 1
                    metrics = {
                        "n": runs_n, "party": party, "sponsor": st, "sponsorShare": SPONSOR[sk],
                        "meanTrueProfit": round(statistics.mean(profits), 2),
                        "medianTrueProfit": round(statistics.median(profits), 2),
                        "lossRate": round(loss / runs_n, 4),
                        "p10": round(sorted(profits)[runs_n // 10], 2),
                        "p90": round(sorted(profits)[9 * runs_n // 10], 2),
                    }
                    findings = []
                    if st == "sovereign" and metrics["lossRate"] < 0.3:
                        findings.append({"severity": "medium", "claim": "Sovereign 45% share still shows <30% loss rate — charter may remain viable or wage model understates cost", "evidence": "A"})
                    if st == "self" and metrics["lossRate"] > 0.5:
                        findings.append({"severity": "medium", "claim": "Self-sponsored expeditions lose money >50% once wages/replacements apply — gross≠true profit", "evidence": "A"})
                    write_result(RESULTS / sid / f"{sid}-{st}-P{party}.json", {
                        "pack": PACK, "scenarioId": sid, "runId": f"{sid}-{st}-P{party}",
                        "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                        "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                        "metrics": metrics, "rulesHalts": rules, "findings": findings,
                        "rawEvidencePath": f"results/{sid}/{sid}-{st}-P{party}.json",
                    })

        elif sid == "HAVEN-MARKET":
            for demand in states:
                vals = []
                for i in range(runs_n):
                    rng = random.Random(SEED0 + hash((sid, demand, i)) % 10_000_000)
                    base = COMMODITY["Tier III"]["medianGp"] * rng.randint(1, 20)
                    s = settle_sale(rng, base=base, sponsor_key="guild", demand_key=demand)
                    vals.append(s["gross"])
                # compare to normal
                write_result(RESULTS / sid / f"{sid}-{demand}.json", {
                    "pack": PACK, "scenarioId": sid, "runId": f"{sid}-{demand}",
                    "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                    "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                    "metrics": {
                        "n": runs_n, "demand": demand, "multiplier": SALE["demand"][demand],
                        "meanGross": round(statistics.mean(vals), 2),
                        "medianGross": round(statistics.median(vals), 2),
                    },
                    "rulesHalts": [],
                    "findings": [{
                        "severity": "info",
                        "claim": f"Demand '{demand}' multiplies sale value by {SALE['demand'][demand]} — glutted vs strategic spread is {SALE['demand']['strategic']/SALE['demand']['glutted']:.2f}x",
                        "evidence": "A",
                    }],
                    "rawEvidencePath": f"results/{sid}/{sid}-{demand}.json",
                })

        elif sid == "HAVEN-COIN":
            for quality in states:
                nets = []
                detect = 0
                rules_acc = []
                for i in range(runs_n):
                    rng = random.Random(SEED0 + hash((sid, quality, i)) % 10_000_000)
                    amount = rng.choice([50, 100, 250, 500, 1000, 5000])
                    a = assay_coin(rng, quality, amount)
                    nets.append(a["net"] / amount)
                    detect += int(a["detected"])
                    rules_acc.extend(a["rulesHalts"])
                seen = set()
                uniq = []
                for h in rules_acc:
                    if h["code"] not in seen:
                        seen.add(h["code"]); uniq.append(h)
                all_halts.extend(uniq)
                write_result(RESULTS / sid / f"{sid}-{quality}.json", {
                    "pack": PACK, "scenarioId": sid, "runId": f"{sid}-{quality}",
                    "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                    "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                    "metrics": {
                        "n": runs_n, "quality": quality,
                        "meanNetFrac": round(statistics.mean(nets), 4),
                        "detectRate": round(detect / runs_n, 4) if quality != "clean" else 0.0,
                    },
                    "rulesHalts": uniq,
                    "findings": [],
                    "rawEvidencePath": f"results/{sid}/{sid}-{quality}.json",
                })

        elif sid == "HAVEN-HEAT":
            for h0 in [int(x) for x in states]:
                comps = 0
                bribe_floor_hits = 0
                for i in range(runs_n):
                    rng = random.Random(SEED0 + hash((sid, h0, i)) % 10_000_000)
                    bribe = rng.choice([None, None, "tenPercent", "twentyFivePercent"])
                    t = heat_tick(rng, h0, bribe)
                    comps += int(t["complication"])
                    if bribe and t["heat"] <= HEAT["bribes"]["floorWhileActive"] and h0 > 1:
                        bribe_floor_hits += 1
                findings = []
                if h0 == 0:
                    # verify no auto complications
                    pass
                if h0 >= 4 and comps / runs_n < 0.3:
                    findings.append({"severity": "high", "claim": f"Heat {h0} complication rate {comps/runs_n:.2f} seems low for 'end of Haven Turn 1d6<=Heat'", "evidence": "A"})
                write_result(RESULTS / sid / f"{sid}-H{h0}.json", {
                    "pack": PACK, "scenarioId": sid, "runId": f"{sid}-H{h0}",
                    "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                    "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                    "metrics": {
                        "n": runs_n, "startHeat": h0,
                        "complicationRate": round(comps / runs_n, 4),
                        "expectedApprox": round(min(1.0, h0 / 6), 4),
                        "bribeFloorHits": bribe_floor_hits,
                    },
                    "rulesHalts": [],
                    "findings": findings,
                    "rawEvidencePath": f"results/{sid}/{sid}-H{h0}.json",
                })

        elif sid == "HAVEN-DEBT":
            for term in states:
                defaults = 0
                interests = []
                rules_acc = []
                for i in range(runs_n):
                    rng = random.Random(SEED0 + hash((sid, term, i)) % 10_000_000)
                    principal = rng.choice([100, 500, 1000, 5000, 20000])
                    # occasionally try over-cap rate
                    rate = None
                    if rng.random() < 0.1:
                        rate = 0.15
                    d = debt_cycle(rng, principal, term, rate)
                    defaults += int(d["defaulted"])
                    interests.append(d["interestAccrued"] / principal)
                    rules_acc.extend(d["rulesHalts"])
                seen = set(); uniq = []
                for h in rules_acc:
                    if h["code"] not in seen:
                        seen.add(h["code"]); uniq.append(h)
                all_halts.extend(uniq)
                write_result(RESULTS / sid / f"{sid}-{term}.json", {
                    "pack": PACK, "scenarioId": sid, "runId": f"{sid}-{term}",
                    "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                    "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                    "metrics": {
                        "n": runs_n, "term": term,
                        "defaultRate": round(defaults / runs_n, 4),
                        "meanInterestFrac": round(statistics.mean(interests), 4),
                        "interestCapPerOpening": LABOR["debtInterestCapPerOpening"],
                    },
                    "rulesHalts": uniq,
                    "findings": [{
                        "severity": "info",
                        "claim": f"{term} debt mean interest fraction {statistics.mean(interests):.3f}; default rate {defaults/runs_n:.3f}",
                        "evidence": "A",
                    }],
                    "rawEvidencePath": f"results/{sid}/{sid}-{term}.json",
                })

        elif sid == "HAVEN-FACTION":
            # states like "-5 through +5"
            reps = list(range(REP_MIN, REP_MAX + 1))
            for rep in reps:
                access = faction_access(rep)
                all_halts.extend(access["rulesHalts"])
                # Monte Carlo: random Haven actions gated by access
                blocked = 0
                for i in range(runs_n):
                    rng = random.Random(SEED0 + hash((sid, rep, i)) % 10_000_000)
                    action = rng.choice(["marketDesk", "licensedMaterials", "strategicAuctions", "sovereignContracts"])
                    if not access["access"][action]:
                        blocked += 1
                write_result(RESULTS / sid / f"{sid}-R{rep}.json", {
                    "pack": PACK, "scenarioId": sid, "runId": f"{sid}-R{rep}",
                    "seed": SEED0, "sourceHash": SOURCE_HASH, "fixtureHash": None,
                    "evidenceLevel": "A", "outcome": "aggregated_monte_carlo",
                    "metrics": {
                        "n": runs_n, "reputation": rep, "label": access["label"],
                        "access": access["access"],
                        "blockedActionRate": round(blocked / runs_n, 4),
                    },
                    "rulesHalts": access["rulesHalts"],
                    "findings": [],
                    "rawEvidencePath": f"results/{sid}/{sid}-R{rep}.json",
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
