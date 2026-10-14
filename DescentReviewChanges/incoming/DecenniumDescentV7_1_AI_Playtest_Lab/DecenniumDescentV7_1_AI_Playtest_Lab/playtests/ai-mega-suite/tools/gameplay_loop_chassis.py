#!/usr/bin/env python3
"""Executable Gameplay Loop v1.1 chassis for Packs 11–14. Not canon; playtest harness only."""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
LAB = HERE.parent.parent
ROOT = LAB.parent.parent
GAME_PATH = ROOT / "data/public/Decennium_Descent_Gameplay_Loop_v1_1.json"
GAME = json.loads(GAME_PATH.read_text(encoding="utf-8"))
SOURCE_HASH = hashlib.sha256(GAME_PATH.read_bytes()).hexdigest()

PROGRESS = GAME["route"]["progressPerWatch"]
TIER_DC = {int(k.replace("tier", "")) if k.startswith("tier") else 0: v for k, v in GAME["resolution"]["tierDcs"].items() if k.startswith("tier")}
TIER_DC[0] = GAME["resolution"]["tierDcs"]["routine"]
SPONSOR = GAME["sponsorShares"]
SALE = GAME["saleValue"]
TAX = GAME["havenEconomy"]["taxSchedule"]
HEAT = GAME["havenEconomy"]["underwaysHeat"]
COIN = GAME["havenEconomy"]["coinAssay"]
LABOR = GAME["havenEconomy"]["labor"]
COMMODITY = GAME["havenEconomy"]["commodityIndex"]
SEASONAL = GAME["seasonal"]
REP_MIN, REP_MAX = GAME["reputation"]["minimum"], GAME["reputation"]["maximum"]

MAPPING_NORM = {
    "mapped": "Mapped",
    "sketched": "Sketched",
    "unknown": "Unknown",
    "secured": "Secured",
    "all": None,
}


def parse_pipe(s: str) -> list[str]:
    return [x.strip() for x in str(s).split("|") if x.strip()]


def parse_levels(s: str) -> list[int]:
    if str(s).lower() == "all":
        return [1, 3, 5, 10, 15]
    return [int(x) for x in parse_pipe(s)]


def parse_ints(s: str) -> list[int]:
    if str(s).lower() in ("n/a", "all", ""):
        return []
    return [int(x) for x in parse_pipe(s)]


def degree(total: int, dc: int, nat: int) -> str:
    if total >= dc + 10:
        deg = "crit_success"
    elif total >= dc:
        deg = "success"
    elif total <= dc - 10:
        deg = "crit_fail"
    else:
        deg = "fail"
    if nat == 20:
        deg = {"crit_fail": "fail", "fail": "success", "success": "crit_success", "crit_success": "crit_success"}[deg]
    elif nat == 1:
        deg = {"crit_success": "success", "success": "fail", "fail": "crit_fail", "crit_fail": "crit_fail"}[deg]
    return deg


def check(rng: random.Random, mod: int, assistants: int, dc: int, strain_pen: int = 0) -> str:
    nat = rng.randint(1, 20)
    total = nat + mod + min(3, assistants) - strain_pen
    return degree(total, dc, nat)


def tier_for_level(level: int) -> int:
    if level <= 4:
        return 1
    if level <= 8:
        return 2
    if level <= 12:
        return 3
    if level <= 16:
        return 4
    return 5


def commodity_median(level: int) -> float:
    t = tier_for_level(level)
    key = f"Tier {['I','II','III','IV','V'][t-1]}"
    return float(COMMODITY[key]["medianGp"])


@dataclass
class Lot:
    name: str
    load: int
    ec: int
    priority: int
    base_value: float
    tags: list[str] = field(default_factory=list)
    abandoned: bool = False
    lost: bool = False


@dataclass
class ExpeditionResult:
    outcome: str
    haven: bool
    objective: bool
    wiped: bool
    aborted: bool
    sealed: bool
    watches: int
    hours: int
    peak_pressure: int
    end_pressure: int
    end_strain: float
    end_supply: float
    rest_debt_events: int
    casualties: int
    deaths: int
    cargo_load_out: int
    cargo_load_haven: int
    cargo_value_gross: float
    cargo_value_retained: float
    net_after_sponsor: float
    true_profit: float
    extraction_tests: int
    extraction_fails: int
    over_capacity_watches: int
    forage_gains: float
    mapping: str
    policy: str
    level: int
    party: int
    sustenance: int
    rules_halts: list[dict]
    ledger: list[dict] = field(default_factory=list)


POLICIES = {
    "cautious": {"abort_pressure": 3, "rest_at_strain": 2, "cargo_factor": 0.7, "forage": True, "map_when_unknown": True},
    "balanced": {"abort_pressure": 4, "rest_at_strain": 3, "cargo_factor": 1.0, "forage": True, "map_when_unknown": True},
    "aggressive": {"abort_pressure": 5, "rest_at_strain": 4, "cargo_factor": 1.3, "forage": False, "map_when_unknown": False},
}


def simulate_expedition(
    rng: random.Random,
    *,
    level: int,
    party: int,
    mapping: str,
    policy_name: str = "balanced",
    sustenance: int = 2,
    objective: str = "profit",
    casualty_start: int = 0,
    attention_ec: int | None = None,
    forced_rest_interrupt: bool = False,
    max_watches: int = 36,
    target_progress: int | None = None,
    record_ledger: bool = False,
) -> ExpeditionResult:
    pol = POLICIES[policy_name]
    tier = tier_for_level(level)
    dc = TIER_DC.get(tier, 15)
    mapping = MAPPING_NORM.get(mapping.lower(), mapping) if mapping else "Mapped"
    if mapping is None:
        mapping = "Mapped"

    # Capacity: party Strength proxy — 14 STR each → 14 Load, convoy uses 60% of sum as route capacity baseline
    carry_each = 14
    convoy_capacity = int(party * carry_each * 0.55)
    route_capacity = max(20, int(convoy_capacity * (1.1 if mapping in ("Mapped", "Secured") else 0.85)))
    base_load = max(4, party)  # kit
    supply = float(party * 3)  # ~3 Medium-days reserve
    strain = [0] * party
    downed = [False] * party
    dead = [False] * party
    rest_debt = [False] * party
    for i in range(min(casualty_start, party)):
        downed[i] = True

    cargo: list[Lot] = []
    pressure = 0
    progress = 0
    watches = 0
    hours = 0
    peak_p = 0
    rest_debt_events = 0
    forage_gains = 0.0
    over_cap = 0
    extraction_tests = 0
    extraction_fails = 0
    extracting = False
    aborted = False
    sealed = False
    haven = False
    objective_met = False
    wiped = False
    attention_applied = False
    rules_halts: list[dict] = []
    ledger: list[dict] = []

    # Target progress by scenario objective
    if target_progress is None:
        if objective.startswith("two-day"):
            target_progress = 6
        elif "Haven" in objective or "reach Haven" in objective:
            target_progress = 10
        elif "Tier IV" in objective or "frontier" in objective:
            target_progress = 14
        elif "abort" in objective:
            target_progress = 10
        else:
            target_progress = 8

    def alive_count() -> int:
        return sum(1 for i in range(party) if not dead[i])

    def walking() -> int:
        return sum(1 for i in range(party) if not dead[i] and not downed[i])

    def cargo_load() -> int:
        cas = sum(6 for i in range(party) if downed[i] and not dead[i])
        return base_load + sum(c.load for c in cargo if not c.abandoned and not c.lost) + cas

    def mean_strain() -> float:
        living = [strain[i] for i in range(party) if not dead[i]]
        return statistics.mean(living) if living else 6.0

    def add_cargo(ec: int, load: int, value: float, tags: list[str], name: str, priority: int):
        nonlocal attention_applied, pressure
        cargo.append(Lot(name, load, ec, priority, value, tags))
        if "Attention" in tags and not attention_applied:
            pressure = min(6, pressure + 1)
            attention_applied = True

    # Seed cargo by objective class
    if attention_ec is not None:
        med = commodity_median(level) * (2 + attention_ec)
        tags = ["Attention"] if attention_ec >= 4 else ([] if attention_ec < 3 else ["Fragile"])
        if attention_ec >= 3:
            tags = list(set(tags + (["Volatile"] if attention_ec == 3 else ["Attention", "Cursed"][: attention_ec - 2])))
        add_cargo(attention_ec, 4 + attention_ec * 2, med * pol["cargo_factor"], tags or ([] if attention_ec < 2 else ["Fragile"]), f"lot-ec{attention_ec}", max(1, 6 - attention_ec))
    elif "casualty" in objective.lower():
        add_cargo(2, 6, commodity_median(level) * 8 * pol["cargo_factor"], ["Living"], "living-specimen", 5)
    else:
        # progressive salvage during run
        pass

    qm_mod = 4 + tier  # Quartermaster Survival proxy
    assistants = min(3, max(0, walking() // 3))

    while watches < max_watches and alive_count() > 0 and not haven and not sealed:
        watches += 1
        hours += 8
        # Horn at Opening hour 1200 of 2400 — mid-expedition soft fail if still outbound late
        if hours >= 1200 and objective.startswith("two-day"):
            # past Horn on short descent — force extract attempt
            extracting = True

        # Rest debt failure at day boundary every 3 watches
        if watches % 3 == 0:
            for i in range(party):
                if rest_debt[i] and not dead[i]:
                    strain[i] = min(6, strain[i] + 1)
                    rest_debt[i] = False
                    rest_debt_events += 1
                    if strain[i] >= 6:
                        dead[i] = True
                    elif strain[i] >= 5:
                        downed[i] = True

        # Supply burn: one Medium character-day per walking member per day (~3 watches)
        if watches % 3 == 1:
            need = walking() + sum(1 for i in range(party) if downed[i] and not dead[i]) * 0.5
            supply -= need
            if supply < 0:
                supply = 0
                for i in range(party):
                    if not dead[i]:
                        strain[i] = min(6, strain[i] + 1)
                        if strain[i] >= 6:
                            dead[i] = True
                        elif strain[i] >= 5:
                            downed[i] = True

        # Rest interrupt scenario
        if forced_rest_interrupt and watches in (4, 5) and mean_strain() >= 1:
            # interrupted long rest → Rest Debt
            for i in range(party):
                if not dead[i] and not downed[i]:
                    rest_debt[i] = True
            rules_halts.append({
                "code": "REST-DEBT-INTERRUPT-TIMING",
                "note": "Rest Debt deadline 'next two Watches and before next day boundary' — applied as day-boundary failure; interrupt mid-rest timing vs Evening camp workers remains underspecified in JSON.",
            })

        # Policy rest
        if mean_strain() >= pol["rest_at_strain"] and walking() > 0 and not extracting:
            hours += 8
            watches += 1
            for i in range(party):
                if not dead[i]:
                    strain[i] = max(0, strain[i] - 1)
                    rest_debt[i] = False
            pressure = max(0, pressure - 1)
            continue

        # Map Route when Unknown
        if mapping == "Unknown" and pol["map_when_unknown"] and walking() >= 1:
            deg = check(rng, qm_mod, assistants, dc, int(mean_strain()))
            if deg in ("success", "crit_success"):
                mapping = "Sketched" if deg == "success" else "Mapped"
            else:
                pressure = min(6, pressure + 1)

        # Forage / sustenance
        if pol["forage"] and sustenance > 0 and walking() > 0:
            deg = check(rng, qm_mod - 1, min(2, assistants), dc, int(mean_strain()))
            if deg == "crit_success":
                gain = sustenance + math.ceil(sustenance / 2)
                supply += gain
                forage_gains += gain
            elif deg == "success":
                supply += sustenance
                forage_gains += sustenance
            elif deg == "crit_fail":
                pressure = min(6, pressure + 1)

        # Progress
        rate = int(PROGRESS.get(mapping, 0))
        load_now = cargo_load()
        if load_now > route_capacity:
            rate = max(0, rate - 1)
            pressure = min(6, pressure + 1)
            over_cap += 1
        # Unknown with rate 0: only incidental progress via lucky scout
        if rate == 0 and mapping == "Unknown":
            if rng.random() < 0.15:
                rate = 1
            elif not any(h.get("code") == "UNKNOWN-PROGRESS-ZERO" for h in rules_halts):
                rules_halts.append({
                    "code": "UNKNOWN-PROGRESS-ZERO",
                    "note": "progressPerWatch.Unknown=0; without Map Route success, expedition cannot meet Progress targets — intentional deadlock risk.",
                })
        progress += rate

        # Salvage pickup (not casualty/attention-fixed runs)
        if attention_ec is None and "casualty" not in objective.lower() and rng.random() < 0.35 * pol["cargo_factor"]:
            ec = min(6, max(0, tier - 1 + rng.randint(0, 2)))
            load = max(2, int(3 * pol["cargo_factor"] + ec))
            val = commodity_median(level) * (1 + ec) * (0.8 + rng.random() * 0.6)
            tags = []
            if ec >= 4:
                tags.append("Attention")
            if ec == 3:
                tags.append("Volatile")
            add_cargo(ec, load, val, tags, f"salvage-{watches}", max(1, 5 - ec // 2))

        # Pressure check end of Watch: 1d6 <= Pressure
        if pressure >= 6 or (pressure > 0 and rng.randint(1, 6) <= pressure):
            severe = pressure >= 6 or rng.random() < 0.35
            if severe:
                # casualty or cargo risk
                walkers = [i for i in range(party) if not dead[i] and not downed[i]]
                if walkers and rng.random() < 0.4:
                    i = rng.choice(walkers)
                    downed[i] = True
                    strain[i] = min(6, strain[i] + 2)
                elif cargo:
                    # low priority at risk
                    lot = min((c for c in cargo if not c.abandoned and not c.lost), key=lambda c: c.priority, default=None)
                    if lot and rng.random() < 0.5:
                        lot.lost = True
                pressure = min(6, pressure + 1)
            else:
                for i in range(party):
                    if not dead[i]:
                        strain[i] = min(6, strain[i] + 1)
                pressure = min(6, pressure + 1)

        peak_p = max(peak_p, pressure)

        # Abort policy
        if pressure >= pol["abort_pressure"] and not extracting:
            aborted = True
            extracting = True
            if "abort" in objective.lower():
                objective_met = True  # timely abort is the objective

        if progress >= target_progress and not extracting:
            objective_met = objective_met or ("abort" not in objective.lower())
            extracting = True
            # Extraction Class pressure bump
            highest = max((c.ec for c in cargo if not c.abandoned and not c.lost), default=0)
            pressure = min(6, pressure + min(3, highest // 2))

        # Extraction tests by mapping cadence
        if extracting:
            cadence_every = {"Secured": 99, "Mapped": 6, "Sketched": 3, "Unknown": 2}.get(mapping, 3)
            if extraction_tests == 0 or progress % cadence_every == 0 or pressure >= 5:
                extraction_tests += 1
                highest = max((c.ec for c in cargo if not c.abandoned and not c.lost), default=0)
                cargo_mod = highest  # underspecified numeric cargo DC mods → treat EC as DC bump
                if highest > 0 and not any(h.get("code") == "EXTRACTION-CARGO-DC-MODS" for h in rules_halts):
                    rules_halts.append({
                        "code": "EXTRACTION-CARGO-DC-MODS",
                        "note": "extraction.test cites 'cargo modifiers' without numeric schedule in Gameplay Loop JSON; sim uses +EC to DC as chassis proxy.",
                    })
                deg = check(rng, qm_mod, assistants, dc + cargo_mod, int(mean_strain()))
                if deg == "crit_success":
                    pressure = max(0, pressure - 1)
                elif deg == "success":
                    pass
                elif deg == "fail":
                    extraction_fails += 1
                    hours += 8
                    lots = sorted([c for c in cargo if not c.abandoned and not c.lost], key=lambda c: c.priority)
                    if lots and rng.random() < 0.6:
                        lots[0].lost = True
                else:
                    extraction_fails += 1
                    hours += 8
                    lots = sorted([c for c in cargo if not c.abandoned and not c.lost], key=lambda c: c.priority)
                    for lot in lots[:2]:
                        lot.lost = True
                    walkers = [i for i in range(party) if not dead[i] and not downed[i]]
                    if walkers and rng.random() < 0.5:
                        downed[rng.choice(walkers)] = True

            # Finish extraction after enough progress home or tests
            if extraction_tests >= 1 and (progress >= target_progress or aborted or hours >= 200):
                if alive_count() > 0:
                    haven = True
                break

        if alive_count() == 0:
            wiped = True
            break
        if hours >= 2400:
            sealed = True
            break

        if record_ledger and watches <= 40:
            ledger.append({
                "watch": watches, "hour": hours, "progress": progress, "pressure": pressure,
                "supply": round(supply, 2), "load": cargo_load(), "mapping": mapping,
                "alive": alive_count(), "extracting": extracting,
            })

    # Settlement
    retained = [c for c in cargo if not c.abandoned and not c.lost]
    gross = 0.0
    for c in retained:
        prov = SALE["provenance"]["documented"]
        demand = SALE["demand"]["normal"]
        cond = SALE["condition"]["sound"]
        urg = SALE["urgency"]["normal"]
        gross += c.base_value * prov * demand * cond * urg
    tax_rate = TAX["routineRegisteredGoods"]
    if any("Attention" in c.tags or c.ec >= 4 for c in retained):
        tax_rate = TAX["strategicOrRegulatedCargo"]
    if any("Contraband" in c.tags for c in retained):
        tax_rate = TAX["authorizedContrabandAmnesty"]
    taxes = gross * tax_rate
    sponsor = SPONSOR["guild"]
    net = gross * (1 - sponsor) - taxes
    wages = LABOR["dailyWagesGp"]["skilled"] * party * max(1, hours // 24) * (
        LABOR["dangerousExpeditionMultiplier"] if tier >= 3 else 1
    )
    replacement = sum(200 for i in range(party) if dead[i]) + sum(50 for i in range(party) if downed[i] and not dead[i])
    true_profit = net - wages - replacement

    # Deduplicate rules halts by code
    seen = set()
    uniq = []
    for h in rules_halts:
        if h["code"] not in seen:
            seen.add(h["code"])
            uniq.append(h)

    outcome = "wipe" if wiped else ("sealed" if sealed else ("haven_abort" if aborted and haven else ("haven" if haven else "lost")))
    return ExpeditionResult(
        outcome=outcome,
        haven=haven,
        objective=objective_met and haven,
        wiped=wiped,
        aborted=aborted,
        sealed=sealed,
        watches=watches,
        hours=hours,
        peak_pressure=peak_p,
        end_pressure=pressure,
        end_strain=round(mean_strain(), 3),
        end_supply=round(supply, 2),
        rest_debt_events=rest_debt_events,
        casualties=sum(1 for i in range(party) if downed[i] and not dead[i]),
        deaths=sum(1 for i in range(party) if dead[i]),
        cargo_load_out=sum(c.load for c in cargo),
        cargo_load_haven=sum(c.load for c in retained),
        cargo_value_gross=round(gross, 2),
        cargo_value_retained=round(sum(c.base_value for c in retained), 2),
        net_after_sponsor=round(net, 2),
        true_profit=round(true_profit, 2),
        extraction_tests=extraction_tests,
        extraction_fails=extraction_fails,
        over_capacity_watches=over_cap,
        forage_gains=round(forage_gains, 2),
        mapping=mapping,
        policy=policy_name,
        level=level,
        party=party,
        sustenance=sustenance,
        rules_halts=uniq,
        ledger=ledger,
    )


def summarize(runs: list[ExpeditionResult]) -> dict[str, Any]:
    n = len(runs)
    if not n:
        return {}
    def rate(pred):
        return round(sum(1 for r in runs if pred(r)) / n, 4)
    profits = [r.true_profit for r in runs]
    return {
        "n": n,
        "havenRate": rate(lambda r: r.haven),
        "objectiveRate": rate(lambda r: r.objective),
        "wipeRate": rate(lambda r: r.wiped),
        "abortRate": rate(lambda r: r.aborted),
        "sealedRate": rate(lambda r: r.sealed),
        "meanPeakPressure": round(statistics.mean(r.peak_pressure for r in runs), 3),
        "meanWatches": round(statistics.mean(r.watches for r in runs), 3),
        "meanHours": round(statistics.mean(r.hours for r in runs), 2),
        "meanTrueProfit": round(statistics.mean(profits), 2),
        "medianTrueProfit": round(statistics.median(profits), 2),
        "profitLossRate": rate(lambda r: r.true_profit < 0),
        "meanCargoRetainedLoad": round(statistics.mean(r.cargo_load_haven for r in runs), 3),
        "meanExtractionFailRate": round(statistics.mean((r.extraction_fails / r.extraction_tests) if r.extraction_tests else 0 for r in runs), 4),
        "meanRestDebtEvents": round(statistics.mean(r.rest_debt_events for r in runs), 3),
        "meanDeaths": round(statistics.mean(r.deaths for r in runs), 3),
    }


def write_result(path: Path, payload: dict) -> None:
    """Write JSON; on Windows use extended-length paths to survive deep lab nests."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2)
    try:
        path.write_text(data, encoding="utf-8")
        return
    except OSError:
        pass
    # Extended path (\\?\) for Win32 MAX_PATH
    resolved = path if path.is_absolute() else path.resolve()
    ext = r"\\?\\" + str(resolved)
    Path(ext).parent.mkdir(parents=True, exist_ok=True)
    with open(ext, "w", encoding="utf-8") as f:
        f.write(data)


def mirror_suite(pack_id: str, src_dir: Path) -> None:
    dest = LAB / "results" / pack_id
    dest.mkdir(parents=True, exist_ok=True)
    for p in src_dir.glob("**/*"):
        if p.is_file():
            rel = p.relative_to(src_dir)
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(p.read_bytes())
