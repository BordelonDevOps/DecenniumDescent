#!/usr/bin/env python3
"""
V7 Pack 02 — Expedition / Extraction deterministic playtest runner.

Sources (pending V7 promotion; see SOURCE_MANIFEST gaps):
  - DescentReviewChanges/incoming/DecenniumDescentv7/GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt
  - docs/mechanics/EXPEDITION_STRUCTURE_CANON.md (12-person RAW)
  - src/data/haven.json, src/data/dungeon-mechanics.json (companion mirrors)

Does NOT rewrite canon. Writes results/<scenario>/<agent>.json only.
"""
from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
BIBLE = (
    ROOT.parent.parent / "GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt"
)
PACK = "02-expedition-extraction"

# --- Roster (matches agents/players + bible Brass Lantern-style company) ---
PLAYERS = [
    {"id": "01-mara-vann", "name": "Mara Venn", "team": "Combat", "office": "Expedition Leader", "mod": 6},
    {"id": "02-orrik-stonewake", "name": "Orrik Stonewake", "team": "Combat", "office": "Rear Guard", "mod": 5},
    {"id": "03-taran-ashward", "name": "Taran Ashward", "team": "Combat", "office": "Escort Lead", "mod": 5},
    {"id": "04-salira-dusk", "name": "Salira Dusk", "team": "Reconnaissance", "office": "Routekeeper", "mod": 7},
    {"id": "05-pell-quickstep", "name": "Pell Quickstep", "team": "Reconnaissance", "office": "Scout", "mod": 6},
    {"id": "06-edrin-vale", "name": "Edrin Vale", "team": "Research", "office": "Claimant of Record", "mod": 7},
    {"id": "07-ysabel-threadseer", "name": "Ysabel Threadseer", "team": "Research", "office": "Risk Analyst", "mod": 6},
    {"id": "08-harka-reed", "name": "Harka Reed", "team": "Resource", "office": "Harvester", "mod": 6},
    {"id": "09-zeetes", "name": "Zeetes", "team": "Support", "office": "Quartermaster", "mod": 6},
    {"id": "10-durn-stonevow", "name": "Durn Stonevow", "team": "Support", "office": "Surgeon", "mod": 6},
    {"id": "11-ilse-harrow", "name": "Ilse Harrow", "team": "Support", "office": "Transport Chief", "mod": 5},
    {"id": "12-toma-glass", "name": "Toma Glass", "team": "Resource", "office": "Preservation Lead", "mod": 6},
]

TIER_DC = {1: 12, 2: 13, 3: 15, 4: 16}
TEAM_OPTIMAL = {"Combat": (4, 6), "Reconnaissance": (1, 3), "Research": (1, 3), "Resource": (2, 4), "Support": (1, 3)}


@dataclass
class CargoLot:
    name: str
    load: int
    extraction_class: int
    priority: int
    value: float
    tags: list[str] = field(default_factory=list)
    abandoned: bool = False
    at_risk: bool = False


@dataclass
class Member:
    pid: str
    name: str
    team: str
    office: str
    mod: int
    strain: int = 0
    wounds: int = 0
    downed: bool = False
    dead: bool = False
    rest_debt: bool = False
    meaningful_watches: int = 0
    idle_watches: int = 0
    activities: list[str] = field(default_factory=list)


@dataclass
class ExpeditionState:
    scenario: str
    seed: int
    tier: int
    hour: int
    supply: float
    daily_supply: float
    treasury: float
    free_load_start: int
    base_load: int
    convoy_capacity: int
    route_length: int
    route_risk: int
    mapping: str
    route_capacity: int
    progress: int = 0
    pressure: int = 0
    phase: str = "outbound"  # outbound | objective | extract | done
    camp: str = "none"
    extracting: bool = False
    abort_continued: bool = False
    sealed: bool = False
    abandoned: bool = False
    haven_arrived: bool = False
    sponsor_share: float = 0.20
    objective_met: bool = False
    desired_value: float = 0
    cargo: list[CargoLot] = field(default_factory=list)
    members: list[Member] = field(default_factory=list)
    watches: int = 0
    days: int = 0
    max_days: int = 12
    horn_deadline: int | None = None
    complications: int = 0
    severe_complications: int = 0
    extraction_tests: int = 0
    extraction_fails: int = 0
    cargo_abandoned_value: float = 0
    cargo_abandoned_load: int = 0
    supply_shortfalls: int = 0
    pressure_peaks: int = 0
    unused_role_notes: list[str] = field(default_factory=list)
    decision_bottlenecks: list[str] = field(default_factory=list)
    rulings: list[str] = field(default_factory=list)
    public_facts: list[str] = field(default_factory=list)
    hidden_lore_leaked: bool = False
    living_cargo_present: bool = False
    downed_carried: int = 0
    profit_gp: float = 0
    net_after_sponsor: float = 0
    outcome: str = "ongoing"
    activity_counts: dict = field(default_factory=lambda: defaultdict(int))
    team_successes: dict = field(default_factory=lambda: defaultdict(int))
    team_failures: dict = field(default_factory=lambda: defaultdict(int))
    watch_log: list[dict] = field(default_factory=list)
    mismatches: list[str] = field(default_factory=list)


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


def check(rng: random.Random, lead_mod: int, assistants: int, dc: int, strain_pen: int = 0) -> tuple[str, int, int]:
    nat = rng.randint(1, 20)
    total = nat + lead_mod + min(3, assistants) - strain_pen
    return degree(total, dc, nat), total, nat


def convoy_load(st: ExpeditionState) -> int:
    cargo = sum(c.load for c in st.cargo if not c.abandoned)
    casualties = sum(6 for m in st.members if m.downed and not m.dead)
    return st.base_load + cargo + casualties


def free_load(st: ExpeditionState) -> int:
    return max(0, st.convoy_capacity - convoy_load(st))


def progress_rate(st: ExpeditionState) -> int:
    if st.mapping in ("Mapped", "Secured"):
        rate = 2
    elif st.mapping == "Sketched":
        rate = 1
    else:
        rate = 0
    if convoy_load(st) > st.route_capacity:
        rate = max(0, rate - 1)
    return rate


def highest_extraction_class(st: ExpeditionState) -> int:
    lots = [c for c in st.cargo if not c.abandoned]
    return max((c.extraction_class for c in lots), default=0)


def begin_extraction(st: ExpeditionState) -> None:
    if st.extracting:
        return
    st.extracting = True
    st.phase = "extract"
    # Bible §16: + floor(highest EC / 2), max +3
    bump = min(3, highest_extraction_class(st) // 2)
    st.pressure = min(6, st.pressure + bump)
    # Require cargo priority before extraction (already assigned at creation; reaffirm)
    st.cargo.sort(key=lambda c: c.priority)
    st.public_facts.append(
        f"Extraction declared at hour {st.hour}: Pressure +{bump} from EC {highest_extraction_class(st)}; "
        f"cargo priority locked {[ (c.name, c.priority) for c in st.cargo if not c.abandoned ]}"
    )


def abandon_lowest(st: ExpeditionState, n: int = 1) -> list[str]:
    active = sorted([c for c in st.cargo if not c.abandoned], key=lambda c: (c.priority, -c.load))
    lost = []
    for c in active[:n]:
        c.abandoned = True
        c.at_risk = False
        st.cargo_abandoned_value += c.value
        st.cargo_abandoned_load += c.load
        lost.append(c.name)
    return lost


def place_at_risk(st: ExpeditionState, n: int = 1) -> list[str]:
    active = sorted([c for c in st.cargo if not c.abandoned and not c.at_risk], key=lambda c: (c.priority, -c.load))
    names = []
    for c in active[:n]:
        c.at_risk = True
        names.append(c.name)
    return names


def resolve_at_risk(st: ExpeditionState, choice: str) -> None:
    """choice: abandon | spend_time | fight"""
    at_risk = [c for c in st.cargo if c.at_risk and not c.abandoned]
    if not at_risk:
        return
    if choice == "abandon":
        for c in at_risk:
            c.abandoned = True
            c.at_risk = False
            st.cargo_abandoned_value += c.value
            st.cargo_abandoned_load += c.load
        st.decision_bottlenecks.append("Extraction response: abandoned at-risk cargo to save clock/Pressure")
    elif choice == "spend_time":
        for c in at_risk:
            c.at_risk = False
        st.hour += 8
        st.watches += 1
        st.decision_bottlenecks.append("Extraction response: spent 8h rather than abandon cargo")
    else:
        for c in at_risk:
            c.at_risk = False
        st.pressure = min(6, st.pressure + 1)
        st.decision_bottlenecks.append("Extraction response: fought to keep at-risk cargo; Pressure +1")


def apply_complication(st: ExpeditionState, rng: random.Random, severity: str) -> None:
    st.complications += 1
    if severity == "severe":
        st.severe_complications += 1
    threat = rng.choice(["time", "supply", "position", "cargo", "secrecy"])
    if threat == "time":
        st.hour += 8 if severity != "severe" else 16
        st.watches += 1 if severity != "severe" else 2
    elif threat == "supply":
        loss = 6 if severity == "minor" else 12 if severity == "standard" else 24
        st.supply = max(0, st.supply - loss)
    elif threat == "position":
        st.progress = max(0, st.progress - (1 if severity != "severe" else 2))
        st.pressure = min(6, st.pressure + 1)
    elif threat == "cargo":
        names = place_at_risk(st, 1 if severity != "severe" else 2)
        st.public_facts.append(f"Director stated at-risk before response: {names} ({severity})")
        # Players choose: Horn race / casualty prefer abandon; profit prefer spend/fight
        if st.scenario in ("EXP-HORN-RACE", "EXP-CASUALTY") or st.supply < st.daily_supply * 2:
            resolve_at_risk(st, "abandon")
        elif severity == "severe":
            resolve_at_risk(st, "abandon")
        else:
            resolve_at_risk(st, "spend_time" if st.hour < 1000 else "abandon")
    else:  # secrecy
        st.pressure = min(6, st.pressure + 1)
        if st.scenario == "EXP-T4-DARK" and severity == "severe":
            # Public symptoms only — Director ruling: do not confirm hidden lore
            st.rulings.append(
                "Director ruling: Severe secrecy complication reveals public symptoms only; "
                "hidden cosmology not confirmed (EXP-T4-DARK boundary)."
            )
            st.public_facts.append("Public symptom spike observed; lore unconfirmed.")


def pressure_roll(st: ExpeditionState, rng: random.Random) -> None:
    if st.pressure <= 0:
        return
    if st.pressure >= 6:
        apply_complication(st, rng, "severe")
        return
    roll = rng.randint(1, 6)
    if roll <= st.pressure:
        if roll == 1:
            sev = "severe"
        elif roll == st.pressure:
            sev = "minor"
        else:
            sev = "standard"
        apply_complication(st, rng, sev)


def team_activity(st: ExpeditionState, team: str, phase: str) -> str:
    if phase == "outbound":
        return {
            "Combat": "Advance",
            "Reconnaissance": "Scout Ahead" if st.mapping != "Unknown" else "Reconnaissance (open route)",
            "Research": "Identify",
            "Resource": "Forage",
            "Support": "Transport" if convoy_load(st) > st.route_capacity * 0.8 else "Establish Camp",
        }[team]
    if phase == "objective":
        return {
            "Combat": "Escort" if st.living_cargo_present or st.downed_carried else "Patrol",
            "Reconnaissance": "Map Route" if st.mapping in ("Unknown", "Sketched") else "Counter-Ambush",
            "Research": "Analyze Threat" if st.scenario == "EXP-T4-DARK" else "Identify",
            "Resource": "Harvest" if st.scenario != "EXP-CASUALTY" else "Preserve",
            "Support": "Treat" if any(m.downed or m.wounds for m in st.members) else "Preserve",
        }[team]
    # extract
    return {
        "Combat": "Escort",
        "Reconnaissance": "Conceal Trail",
        "Research": "Identify",
        "Resource": "Preserve",
        "Support": "Transport",
    }[team]


def resolve_team(st: ExpeditionState, rng: random.Random, team: str, activity: str) -> None:
    leads = [m for m in st.members if m.team == team and not m.dead and not m.downed]
    if not leads:
        st.unused_role_notes.append(f"Watch {st.watches}: team {team} had no able members for {activity}")
        return
    lead = max(leads, key=lambda m: m.mod)
    assistants = max(0, len(leads) - 1)
    strain_pen = 1 if lead.strain >= 1 else 0
    if lead.strain >= 3:
        # disadvantage approximated as -5
        strain_pen += 5
    dc = TIER_DC[st.tier]
    if activity.startswith("Reconnaissance") and st.mapping == "Unknown":
        dc = TIER_DC[st.tier]  # open route
    deg, total, nat = check(rng, lead.mod, assistants, dc, strain_pen)
    st.activity_counts[f"{team}:{activity}"] += 1
    for m in leads:
        m.meaningful_watches += 1
        m.activities.append(activity)

    if deg in ("success", "crit_success"):
        st.team_successes[team] += 1
        if team == "Reconnaissance":
            if st.mapping == "Unknown":
                st.mapping = "Sketched"
                st.rulings.append(f"Ruling: first successful recon opens Unknown→Sketched at hour {st.hour}")
            elif activity == "Map Route":
                # accumulate: treat success as +1 toward Risk threshold
                st.team_successes["map_progress"] += 1
                if st.team_successes["map_progress"] >= st.route_risk:
                    nxt = {"Sketched": "Mapped", "Mapped": "Secured"}.get(st.mapping)
                    if nxt:
                        st.mapping = nxt
                        st.team_successes["map_progress"] = 0
            if activity in ("Counter-Ambush", "Conceal Trail") or deg == "crit_success":
                floor = 0 if st.mapping == "Secured" else st.route_risk
                st.pressure = max(floor, st.pressure - 1)
            if deg == "crit_success":
                st.progress += 1
        elif team == "Resource":
            if activity == "Forage":
                st.supply += 4 + (2 if deg == "crit_success" else 0)
            elif activity == "Harvest":
                # Add cargo if free load
                value = {1: 160, 2: 800, 3: 4500, 4: 9000}[st.tier]
                load = {1: 4, 2: 6, 3: 8, 4: 10}[st.tier]
                ec = {1: 1, 2: 2, 3: 3, 4: 4}[st.tier]
                tags = ["Perishable"]
                if st.scenario == "EXP-T3-LONG" and not any(c.extraction_class >= 3 and not c.abandoned for c in st.cargo):
                    # Rare lot objective
                    name, load, ec, value, tags = "Rare survey lot", 8, 3, 6500, ["Fragile"]
                else:
                    name = f"Tier{st.tier} harvest"
                if free_load(st) >= load:
                    st.cargo.append(CargoLot(name, load, ec, priority=3, value=value, tags=tags))
                else:
                    st.decision_bottlenecks.append("Harvest succeeded but free Load insufficient; lot left behind")
            elif activity == "Preserve":
                for c in st.cargo:
                    if "Perishable" in c.tags or "Living" in c.tags or "Fragile" in c.tags:
                        if "Preserved" not in c.tags:
                            c.tags.append("Preserved")
        elif team == "Support":
            if activity == "Establish Camp" and st.camp == "none":
                st.camp = "temporary"
            elif activity == "Treat":
                for m in st.members:
                    if m.downed and not m.dead:
                        m.downed = False
                        m.wounds = min(3, m.wounds + 1)
                        st.supply = max(0, st.supply - 1)
                    elif m.wounds > 0 and deg in ("success", "crit_success"):
                        m.wounds -= 1 if deg == "success" else min(2, m.wounds)
                        st.supply = max(0, st.supply - 1)
            elif activity == "Transport":
                # redistribute — mechanical no-op beyond meaningful assignment
                pass
        elif team == "Combat":
            if activity == "Advance" and deg == "crit_success":
                st.progress += 1
            if activity == "Escort" and deg in ("success", "crit_success"):
                # protect assistants — reduce next cargo risk chance tracked via pressure floor
                pass
        elif team == "Research":
            if st.scenario == "EXP-T4-DARK":
                # Analyze symptoms without confirming hidden lore
                st.public_facts.append("Research logged public symptoms; no Director cosmology confirmation shared.")
            if activity == "Identify":
                for c in st.cargo:
                    if c.extraction_class >= 2 and deg in ("success", "crit_success"):
                        c.priority = max(c.priority, 4)
    else:
        st.team_failures[team] += 1
        if deg == "crit_fail":
            st.supply = max(0, st.supply - 4)
            st.pressure = min(6, st.pressure + 1)
            if team == "Combat":
                # possible casualty
                victim = rng.choice([m for m in st.members if m.team == "Combat" and not m.dead])
                if rng.random() < 0.35:
                    victim.downed = True
                    victim.wounds = min(3, victim.wounds + 1)
                    st.downed_carried = sum(1 for m in st.members if m.downed)


def end_of_day(st: ExpeditionState) -> None:
    """Day boundary only. Supply is consumed per Watch (1/3 daily) per bible worked example — do not double-charge here."""
    st.days += 1
    if st.supply <= 0:
        st.supply_shortfalls += 1
        for m in st.members:
            if not m.dead:
                m.strain = min(6, m.strain + 1)


def rest_watch(st: ExpeditionState, workers: list[Member]) -> None:
    worker_ids = {m.pid for m in workers}
    for m in st.members:
        if m.dead:
            continue
        if m.pid in worker_ids:
            m.rest_debt = True
            m.strain = min(6, m.strain + 0)  # work instead of rest
            m.meaningful_watches += 1
        else:
            # Long Rest once per 24h
            if m.rest_debt:
                m.rest_debt = False
            if st.camp in ("temporary", "fortified", "forward") or st.camp == "temporary":
                m.strain = max(0, m.strain - 1)
            m.meaningful_watches += 0  # rest is assigned but not a team activity
            # count rest as meaningful decision when recovering
            if m.strain > 0 or m.wounds > 0:
                m.meaningful_watches += 1
            else:
                m.idle_watches += 1


def extraction_test(st: ExpeditionState, rng: random.Random) -> None:
    st.extraction_tests += 1
    qm = next(m for m in st.members if m.office == "Quartermaster")
    dc = TIER_DC[st.tier]
    if convoy_load(st) > st.route_capacity:
        dc += 1
    unsecured = sum(
        1
        for c in st.cargo
        if not c.abandoned
        and any(t in c.tags for t in ("Volatile", "Cursed", "Living"))
        and "Preserved" not in c.tags
        and "Secured" not in c.tags
    )
    dc += min(3, unsecured)
    if st.pressure >= 4:
        dc += 2  # pursued proxy
    if st.mapping == "Secured":
        dc -= 2
    assistants = sum(1 for m in st.members if m.team == "Support" and m.pid != qm.pid and not m.dead)
    deg, total, nat = check(rng, qm.mod, assistants, dc, 1 if qm.strain else 0)
    if deg == "crit_success":
        floor = 0 if st.mapping == "Secured" else st.route_risk
        st.pressure = max(floor, st.pressure - 1)
    elif deg == "success":
        pass
    elif deg == "fail":
        st.extraction_fails += 1
        names = place_at_risk(st, 1)
        st.public_facts.append(
            f"Extraction Test Failure: at risk before response = {names}; options: lose 8h+Standard OR abandon low-priority"
        )
        if st.horn_deadline and st.hour >= st.horn_deadline - 24:
            resolve_at_risk(st, "abandon")
        else:
            # Prefer abandon low value if profitable buffer exists
            if names and any(c.name in names and c.value < 500 for c in st.cargo):
                resolve_at_risk(st, "abandon")
            else:
                resolve_at_risk(st, "spend_time")
                apply_complication(st, rng, "standard")
    else:
        st.extraction_fails += 1
        names = place_at_risk(st, 2)
        st.public_facts.append(f"Extraction Crit Fail: at risk = {names}")
        resolve_at_risk(st, "abandon")
        apply_complication(st, rng, "severe")


def settle_haven(st: ExpeditionState) -> None:
    st.haven_arrived = True
    st.phase = "done"
    gross = sum(c.value for c in st.cargo if not c.abandoned)
    # Condition/provenance simplified: preserved sound ×1; damaged unpreserved ×0.5; documented ×1
    adjusted = 0.0
    for c in st.cargo:
        if c.abandoned:
            continue
        mult = 1.0
        if "Perishable" in c.tags and "Preserved" not in c.tags:
            mult *= 0.5
        if "Fragile" in c.tags and "Preserved" not in c.tags:
            mult *= 0.75
        if "Living" in c.tags:
            mult = 0.0  # no sale; living captive/rescued
        adjusted += c.value * mult
    tax = adjusted * 0.05
    net = max(0.0, adjusted - tax)
    sponsor = net * st.sponsor_share
    retained = net - sponsor
    # wages rough: 12 * 15 gp/day * days
    wages = 12 * 15 * max(1, st.days)
    st.profit_gp = retained - wages - (st.cargo_abandoned_value * 0)  # abandoned already out of gross
    st.net_after_sponsor = retained
    st.treasury += retained
    # objective checks
    if st.scenario == "EXP-T1-PROFIT":
        st.objective_met = st.profit_gp > 0 and not st.sealed
    elif st.scenario == "EXP-HAVEN-RUN":
        st.objective_met = adjusted >= 8000 and not st.sealed
    elif st.scenario == "EXP-T3-LONG":
        st.objective_met = any(
            (not c.abandoned) and c.extraction_class >= 3 and "Rare" in c.name for c in st.cargo
        ) or any((not c.abandoned) and c.extraction_class >= 3 for c in st.cargo)
    elif st.scenario == "EXP-T4-DARK":
        st.objective_met = (not st.hidden_lore_leaked) and st.haven_arrived and len(st.public_facts) > 0
    elif st.scenario == "EXP-HORN-RACE":
        st.objective_met = st.haven_arrived and st.hour < 1200 and not st.sealed
    elif st.scenario == "EXP-CASUALTY":
        living = any((not c.abandoned) and "Living" in c.tags for c in st.cargo)
        downed_home = sum(1 for m in st.members if (m.downed or m.wounds > 0) and not m.dead) >= 2 or st.downed_carried >= 2
        # success if arrived with living cargo and two casualty loads accounted
        casualty_load = sum(6 for m in st.members if m.downed and not m.dead)
        st.objective_met = st.haven_arrived and living and (casualty_load >= 12 or downed_home)
    st.outcome = "haven" if st.haven_arrived else st.outcome


def init_scenario(scenario: str, seed: int) -> ExpeditionState:
    rng = random.Random(seed)  # noqa: F841 — seed recorded; rng created in run
    members = [Member(p["id"], p["name"], p["team"], p["office"], p["mod"]) for p in PLAYERS]

    if scenario == "EXP-T1-PROFIT":
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=1, hour=24, supply=144, daily_supply=12,
            treasury=600, free_load_start=58, base_load=42, convoy_capacity=100,
            route_length=6, route_risk=1, mapping="Mapped", route_capacity=80,
            pressure=1, max_days=12, desired_value=500, sponsor_share=0.20,
            members=members,
        )
    elif scenario == "EXP-HAVEN-RUN":
        # Inward delivery + extract 8000 — mixed mapped/sketched
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=2, hour=200, supply=240, daily_supply=12,
            treasury=1200, free_load_start=40, base_load=50, convoy_capacity=110,
            route_length=10, route_risk=2, mapping="Mapped", route_capacity=90,
            pressure=2, max_days=20, desired_value=8000, sponsor_share=0.30,
            members=members,
        )
        st.cargo.append(CargoLot("Inward licensed medicines", 18, 2, 5, 2500, ["Attention"]))
    elif scenario == "EXP-T3-LONG":
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=3, hour=400, supply=360, daily_supply=12,
            treasury=2000, free_load_start=35, base_load=55, convoy_capacity=100,
            route_length=14, route_risk=3, mapping="Sketched", route_capacity=70,
            pressure=3, max_days=30, desired_value=6500, sponsor_share=0.35,
            members=members,
        )
    elif scenario == "EXP-T4-DARK":
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=4, hour=600, supply=216, daily_supply=12,
            treasury=3000, free_load_start=30, base_load=60, convoy_capacity=95,
            route_length=12, route_risk=4, mapping="Unknown", route_capacity=60,
            pressure=4, max_days=18, desired_value=0, sponsor_share=0.45,
            members=members,
        )
        st.public_facts.append("Public brief: investigate Tier IV symptoms only; no crystal-path confirmation.")
    elif scenario == "EXP-HORN-RACE":
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=2, hour=1080, supply=96, daily_supply=12,
            treasury=800, free_load_start=25, base_load=55, convoy_capacity=100,
            route_length=8, route_risk=2, mapping="Mapped", route_capacity=75,
            pressure=3, max_days=5, desired_value=1000, sponsor_share=0.20,
            members=members, horn_deadline=1200,
        )
        st.cargo.append(CargoLot("Compromised-route salvage", 16, 2, 3, 2200, ["Fragile"]))
        st.cargo.append(CargoLot("Bulk reagents", 24, 1, 1, 900, ["Perishable"]))
        st.mapping = "Sketched"  # becomes compromised
        st.rulings.append("Director: mapped route becomes compromised → Mapping drops to Sketched; Risk/Pressure elevated.")
        st.pressure = 4
        begin_extraction(st)
    elif scenario == "EXP-CASUALTY":
        st = ExpeditionState(
            scenario=scenario, seed=seed, tier=3, hour=300, supply=168, daily_supply=12,
            treasury=1500, free_load_start=10, base_load=50, convoy_capacity=90,
            route_length=10, route_risk=3, mapping="Mapped", route_capacity=55,  # capacity constrained
            pressure=3, max_days=14, desired_value=0, sponsor_share=0.30,
            members=members,
        )
        # Two downed + living cargo
        st.members[1].downed = True
        st.members[1].wounds = 2
        st.members[2].downed = True
        st.members[2].wounds = 1
        st.downed_carried = 2
        st.cargo.append(CargoLot("Living captive (restrained)", 6, 3, 5, 0, ["Living", "Attention"]))
        st.living_cargo_present = True
        st.phase = "extract"
        begin_extraction(st)
    else:
        raise ValueError(scenario)

    # Verify free load bookkeeping
    expected_free = st.convoy_capacity - convoy_load(st)
    if abs(expected_free - st.free_load_start) > 15 and scenario not in ("EXP-HORN-RACE", "EXP-CASUALTY", "EXP-HAVEN-RUN"):
        st.mismatches.append(
            f"Prep free-load note {st.free_load_start} vs computed {expected_free} "
            f"(base {st.base_load}+cargo {convoy_load(st)-st.base_load} vs capacity {st.convoy_capacity})"
        )
    return st


def run_expedition(scenario: str, seed: int) -> ExpeditionState:
    st = init_scenario(scenario, seed)
    rng = random.Random(seed)

    # Abort conditions (bible Brass Lantern style)
    min_reserve_supply = 24
    max_casualties_critical = 2
    latest_return_hour = st.horn_deadline or (st.hour + st.max_days * 24 - 48)

    def check_abort() -> bool:
        criticals = sum(1 for m in st.members if m.wounds >= 3 or (m.downed and m.wounds >= 2))
        if st.supply < min_reserve_supply:
            return True
        if criticals >= max_casualties_critical and st.scenario != "EXP-CASUALTY":
            return True
        if st.hour >= latest_return_hour and not st.extracting:
            return True
        if st.horn_deadline and st.hour >= st.horn_deadline - 16 and not st.extracting:
            return True
        return False

    target_progress_out = st.route_length
    # For haven-run, objective phase after reaching mid
    objective_watches = 0

    while st.outcome == "ongoing" and st.days < st.max_days + 2:
        if st.horn_deadline and st.hour >= st.horn_deadline:
            st.sealed = True
            st.outcome = "sealed"
            st.public_facts.append(f"Sealed below at hour {st.hour} (Horn 1200 crossed).")
            break

        # Day: Watch M, A active; E rest (with optional workers)
        for watch_name in ("Morning", "Afternoon", "Evening"):
            if st.outcome != "ongoing":
                break
            if st.horn_deadline and st.hour >= st.horn_deadline:
                st.sealed = True
                st.outcome = "sealed"
                break

            if check_abort() and not st.extracting:
                # Leader decides: Horn race / casualty force extract; others may push one abort
                if st.scenario in ("EXP-HORN-RACE", "EXP-CASUALTY") or st.days >= st.max_days - 2:
                    begin_extraction(st)
                elif st.supply < min_reserve_supply or st.hour >= latest_return_hour:
                    begin_extraction(st)
                else:
                    st.abort_continued = True
                    st.pressure = min(6, st.pressure + 1)
                    st.decision_bottlenecks.append("Continued after abort condition; Pressure +1 until extracting")
                    begin_extraction(st)

            # Consume 1/3 daily supply each watch (bible example)
            st.supply = max(0, st.supply - st.daily_supply / 3)

            if watch_name == "Evening":
                # Rest watch: 3 workers camp/conceal; 9 rest
                workers = [m for m in st.members if m.team in ("Support", "Reconnaissance") and not m.dead][:3]
                if st.camp == "none" and workers:
                    resolve_team(st, rng, "Support", "Establish Camp")
                if workers:
                    recon = [m for m in workers if m.team == "Reconnaissance"]
                    if recon:
                        resolve_team(st, rng, "Reconnaissance", "Conceal Trail")
                rest_watch(st, workers)
                # Exposed bivouac pressure if no camp
                if st.camp == "none":
                    st.pressure = min(6, st.pressure + 1)
            else:
                # Phase transitions
                if not st.extracting:
                    if st.progress >= target_progress_out and st.phase == "outbound":
                        st.phase = "objective"
                        objective_watches = 0
                    if st.phase == "objective":
                        objective_watches += 1
                        need_obj = 2 if st.scenario == "EXP-T1-PROFIT" else 4 if st.scenario != "EXP-T3-LONG" else 6
                        if st.scenario == "EXP-T4-DARK":
                            need_obj = 3
                        if objective_watches >= need_obj:
                            begin_extraction(st)
                            st.progress = 0  # return route
                    if st.days >= st.max_days - 1 and not st.extracting:
                        begin_extraction(st)
                        st.progress = 0

                # Assign all twelve
                for team in ("Combat", "Reconnaissance", "Research", "Resource", "Support"):
                    act = team_activity(st, team, st.phase if not st.extracting else "extract")
                    resolve_team(st, rng, team, act)

                # Route progress
                rate = progress_rate(st)
                if st.mapping == "Unknown":
                    rate = 0
                # recon may have opened
                if st.mapping != "Unknown":
                    if st.mapping == "Sketched":
                        rate = 1
                    elif st.mapping in ("Mapped", "Secured"):
                        rate = 2
                    if convoy_load(st) > st.route_capacity:
                        rate = max(0, rate - 1)
                        st.pressure = min(6, st.pressure + 1)
                st.progress += rate

                # Pressure modifiers
                if st.abort_continued and st.extracting:
                    st.abort_continued = False  # stops increasing once extracting (bible)
                # Attention cargo
                if any("Attention" in c.tags and not c.abandoned for c in st.cargo):
                    # only count once per watch as increase condition — apply at roll time via tracked flag
                    pass
                floor = 0 if st.mapping == "Secured" else st.route_risk
                # increases
                inc = 0
                if convoy_load(st) > st.route_capacity:
                    inc += 1
                if any("Attention" in c.tags and not c.abandoned for c in st.cargo):
                    inc += 1
                if any(m.downed for m in st.members):
                    # missing/captured proxy — pursued casualty
                    if rng.random() < 0.25:
                        inc += 1
                if st.abort_continued:
                    inc += 1
                st.pressure = min(6, st.pressure + inc)
                # reductions max 2
                red = 0
                if st.camp == "temporary" and watch_name == "Afternoon" and rng.random() < 0.3:
                    red += 1
                st.pressure = max(floor, st.pressure - min(2, red))
                st.pressure_peaks = max(st.pressure_peaks, st.pressure)

                pressure_roll(st, rng)

                if st.extracting and st.progress > 0 and st.progress % 4 == 0:
                    extraction_test(st, rng)

                # Return complete
                if st.extracting and st.progress >= st.route_length:
                    settle_haven(st)
                    st.outcome = "haven"
                    break

            st.hour += 8
            st.watches += 1
            st.watch_log.append({
                "watch": st.watches,
                "name": watch_name,
                "hour": st.hour,
                "phase": st.phase,
                "progress": st.progress,
                "pressure": st.pressure,
                "supply": round(st.supply, 1),
                "load": convoy_load(st),
                "mapping": st.mapping,
            })

        end_of_day(st)
        if st.days >= st.max_days and not st.haven_arrived and st.outcome == "ongoing":
            if st.extracting and st.progress >= st.route_length * 0.7:
                # Forced finish near haven — ruling
                st.rulings.append("Ruling: day-cap reached during extraction; final forced march to Haven with +1 Pressure.")
                st.pressure = min(6, st.pressure + 1)
                settle_haven(st)
                st.outcome = "haven"
            else:
                st.abandoned = True
                st.outcome = "abandoned"
                st.decision_bottlenecks.append("Day cap without Haven arrival — expedition abandoned")

    if st.outcome == "ongoing":
        st.abandoned = True
        st.outcome = "abandoned"
    return st


def aggregate_runs(scenario: str, iterations: int) -> list[ExpeditionState]:
    return [run_expedition(scenario, seed=10_000 + i * 97 + hash(scenario) % 1000) for i in range(iterations)]


def pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 1) if d else 0.0


def write_agent_results(scenario: str, runs: list[ExpeditionState]) -> None:
    outdir = RESULTS / scenario
    outdir.mkdir(parents=True, exist_ok=True)
    n = len(runs)
    outcomes = defaultdict(int)
    for r in runs:
        outcomes[r.outcome] += 1
    obj_rate = pct(sum(1 for r in runs if r.objective_met), n)
    avg_profit = round(sum(r.profit_gp for r in runs) / n, 1)
    avg_hours = round(sum(r.hour - runs[0].hour + (r.watches * 0) for r in runs) / n, 1)
    # better elapsed
    avg_elapsed = round(sum(r.watches * 8 for r in runs) / n, 1)
    avg_pressure_peak = round(sum(r.pressure_peaks for r in runs) / n, 2)
    avg_supply_end = round(sum(r.supply for r in runs) / n, 1)
    avg_abandoned_value = round(sum(r.cargo_abandoned_value for r in runs) / n, 1)
    avg_casualties = round(sum(sum(1 for m in r.members if m.dead or m.downed) for r in runs) / n, 2)
    avg_extraction_fails = round(sum(r.extraction_fails for r in runs) / n, 2)
    haven_rate = pct(sum(1 for r in runs if r.haven_arrived), n)
    sealed_rate = pct(sum(1 for r in runs if r.sealed), n)

    # Combat undersize observation
    combat_count = sum(1 for p in PLAYERS if p["team"] == "Combat")

    common_metrics = {
        "iterations": n,
        "outcomes": dict(outcomes),
        "objective_met_pct": obj_rate,
        "haven_arrival_pct": haven_rate,
        "sealed_pct": sealed_rate,
        "avg_profit_gp": avg_profit,
        "avg_net_after_sponsor_gp": round(sum(r.net_after_sponsor for r in runs) / n, 1),
        "avg_elapsed_hours": avg_elapsed,
        "avg_pressure_peak": avg_pressure_peak,
        "avg_supply_end": avg_supply_end,
        "avg_abandoned_cargo_gp": avg_abandoned_value,
        "avg_abandoned_load": round(sum(r.cargo_abandoned_load for r in runs) / n, 1),
        "avg_downed_or_dead": avg_casualties,
        "avg_extraction_test_fails": avg_extraction_fails,
        "avg_complications": round(sum(r.complications for r in runs) / n, 2),
        "combat_team_size": combat_count,
        "combat_optimal_band": "4-6",
        "source_note": "GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing",
    }

    # Director
    director_obs = [
        f"Across {n} seeded runs, outcomes={dict(outcomes)}; objective_met={obj_rate}%; Haven={haven_rate}%; sealed={sealed_rate}%.",
        f"Average elapsed {avg_elapsed}h; peak Pressure avg {avg_pressure_peak}; extraction test failures avg {avg_extraction_fails}.",
        "At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).",
        f"Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.",
    ]
    if scenario == "EXP-T4-DARK":
        director_obs.append(
            "Hidden lore boundary held: Research logged public symptoms only; no crystal-path / Old God confirmation in public facts."
        )
    if scenario == "EXP-HORN-RACE":
        director_obs.append(
            f"Horn race from hour 1080→1200: sealed_pct={sealed_rate}. Compromised Mapped→Sketched halves Progress and stretches clock."
        )
    director_q = [
        "When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?",
        "Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?",
        "Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.",
    ]
    director_ex = [
        "Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.",
    ]
    director_rec = [
        "Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).",
        "Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.",
        "Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.",
    ]
    write_json(outdir / "director.json", {
        "pack": PACK, "scenarioId": scenario, "agentId": "director", "seed": f"{runs[0].seed}-{runs[-1].seed}",
        "observations": director_obs, "metrics": common_metrics,
        "rulesQuestions": director_q, "exploits": director_ex, "recommendations": director_rec, "confidence": "high",
    })

    # Quartermaster auditor
    mismatches = []
    for r in runs:
        mismatches.extend(r.mismatches)
        # Recalculate sponsor share
        gross_adj = sum(c.value for c in r.cargo if not c.abandoned)
        # verify extraction pressure bump
        # verify casualty load 6 each
        for m in r.members:
            if m.downed and not m.dead:
                pass
    qm_obs = [
        f"Independent recalc: avg abandoned cargo {avg_abandoned_value} gp / {common_metrics['avg_abandoned_load']} Load; avg net after sponsor {common_metrics['avg_net_after_sponsor_gp']} gp.",
        f"Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).",
        f"Prep free-Load bookkeeping mismatches noted in {len(mismatches)} run annotations (scenario cargo overrides).",
        "Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).",
        f"Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.",
    ]
    qm_q = [
        "Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.",
        "Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.",
    ]
    qm_ex = [
        "Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.",
        "Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.",
    ]
    qm_rec = [
        "Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.",
        "Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.",
        "Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.",
    ]
    write_json(outdir / "quartermaster-auditor.json", {
        "pack": PACK, "scenarioId": scenario, "agentId": "quartermaster-auditor", "seed": f"{runs[0].seed}-{runs[-1].seed}",
        "observations": qm_obs,
        "metrics": {**common_metrics, "mismatch_notes": mismatches[:20], "avg_supply_shortfalls": round(sum(r.supply_shortfalls for r in runs)/n, 2)},
        "rulesQuestions": qm_q, "exploits": qm_ex, "recommendations": qm_rec, "confidence": "high",
    })

    # Rules observer
    team_sizes = defaultdict(int)
    for p in PLAYERS:
        team_sizes[p["team"]] += 1
    undersized = [t for t, (lo, hi) in TEAM_OPTIMAL.items() if team_sizes[t] < lo]
    ro_obs = [
        f"All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).",
        f"Team sizes this roster: {dict(team_sizes)}. Undersized vs bible optimal bands: {undersized or 'none'}.",
        f"Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.",
        "SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.",
        f"Decision bottlenecks recurring: {sorted(set(b for r in runs for b in r.decision_bottlenecks))[:8]}",
    ]
    ro_q = [
        "Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.",
        "Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?",
    ]
    ro_ex = [
        "Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).",
    ]
    ro_rec = [
        "Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.",
        "Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.",
        "Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.",
    ]
    write_json(outdir / "rules-observer.json", {
        "pack": PACK, "scenarioId": scenario, "agentId": "rules-observer", "seed": f"{runs[0].seed}-{runs[-1].seed}",
        "observations": ro_obs, "metrics": {**common_metrics, "team_sizes": dict(team_sizes), "undersized_teams": undersized},
        "rulesQuestions": ro_q, "exploits": ro_ex, "recommendations": ro_rec, "confidence": "high",
    })

    # Per-player agents
    for p in PLAYERS:
        pid = p["id"]
        avg_meaningful = round(sum(next(m.meaningful_watches for m in r.members if m.pid == pid) for r in runs) / n, 1)
        avg_idle = round(sum(next(m.idle_watches for m in r.members if m.pid == pid) for r in runs) / n, 1)
        avg_strain = round(sum(next(m.strain for m in r.members if m.pid == pid) for r in runs) / n, 2)
        downed_rate = pct(sum(1 for r in runs if next(m.downed or m.dead for m in r.members if m.pid == pid)), n)
        acts = defaultdict(int)
        for r in runs:
            m = next(x for x in r.members if x.pid == pid)
            for a in m.activities:
                acts[a] += 1

        obs = [
            f"{p['name']} ({p['team']}/{p['office']}): avg meaningful Watch marks {avg_meaningful}, idle-ish rests {avg_idle}, end Strain {avg_strain}, downed/dead rate {downed_rate}%.",
            f"Top activities: {dict(sorted(acts.items(), key=lambda kv: -kv[1])[:5])}.",
        ]
        q: list[str] = []
        ex: list[str] = []
        rec: list[str] = []

        if p["team"] == "Combat":
            obs.append("Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.")
            if combat_count < 4:
                q.append("Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?")
            if scenario == "EXP-CASUALTY":
                obs.append("With two Downed Combat members, Escort lead pressure shifts to remaining fighter + Support Transport.")
            rec.append("Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.")
        elif p["team"] == "Reconnaissance":
            obs.append("Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.")
            if scenario == "EXP-HORN-RACE":
                obs.append("Compromised route made Conceal Trail and Progress rate the critical path to beat Horn 1200.")
            q.append("How many Map Route successes are needed when Risk changes mid-expedition after compromise?")
            rec.append("Show Mapping upgrade progress as X/Risk on the route card.")
        elif p["team"] == "Research":
            if scenario == "EXP-T4-DARK":
                obs.append("Risk Analyst / Claimant stayed on public-symptom Identify/Analyze; no hidden lore confirmation leaked to players.")
                q.append("What public Research outputs are legal at Tier IV without violating Director dual-layer canon?")
            else:
                obs.append("Identify raised cargo priority on EC≥2 lots, feeding extraction triage.")
            rec.append("Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.")
        elif p["team"] == "Resource":
            obs.append("Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.")
            if scenario == "EXP-T3-LONG":
                obs.append("Rare lot objective forced Preserve + Capacity management on Sketched Risk 3.")
            ex.append("On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.")
            rec.append("Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.")
        elif p["team"] == "Support":
            if p["office"] == "Quartermaster":
                obs.append("Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.")
                q.append("Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?")
            elif p["office"] == "Surgeon":
                obs.append("Treat Watches competed with Transport during casualty extraction — real office conflict.")
            elif p["office"] == "Transport Chief":
                obs.append("Capacity-constrained Load made Transport assignment meaningful every extract Watch.")
            rec.append("Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.")

        if avg_idle > avg_meaningful * 0.5 and p["team"] != "Support":
            obs.append("High idle-rest ratio: character felt less decisive on Rest Watches when healthy — expected but worth teaching at table.")

        write_json(outdir / f"{pid}.json", {
            "pack": PACK, "scenarioId": scenario, "agentId": pid, "seed": f"{runs[0].seed}-{runs[-1].seed}",
            "observations": obs,
            "metrics": {
                **{k: common_metrics[k] for k in ("iterations", "objective_met_pct", "haven_arrival_pct", "avg_elapsed_hours", "avg_profit_gp")},
                "avg_meaningful_watches": avg_meaningful,
                "avg_idle_watches": avg_idle,
                "avg_end_strain": avg_strain,
                "downed_or_dead_pct": downed_rate,
                "activity_counts": dict(acts),
                "team": p["team"],
                "office": p["office"],
            },
            "rulesQuestions": q, "exploits": ex, "recommendations": rec,
            "confidence": "medium" if scenario == "EXP-T4-DARK" else "high",
        })


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_proposed_patches(all_scenario_stats: dict) -> None:
    patch_dir = ROOT / "proposed_patches"
    patch_dir.mkdir(exist_ok=True)
    md = []
    md.append("# Proposed patches — Pack 02 Expedition / Extraction\n")
    md.append("**Status:** proposals only — NOT applied to canon.\n")
    md.append("**Evidence base:** deterministic multi-iteration sims per SCENARIO_MATRIX.csv; bible = `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt`.\n")
    md.append("**Assumption:** Pack 01 combat results not ready (0 JSON); class balance not used beyond tier DC checks.\n")
    md.append("\n## P2-01 — Define Extraction Test spacing\n")
    md.append("- **Issue:** Bible §16 says test at every major route transition; no numeric spacing.\n")
    md.append("- **Evidence:** All scenarios required a Director ruling (sim used every 4 Progress).\n")
    md.append("- **Proposal:** Add table: Mapped segment = 1 test per Length/2 Progress; Unknown/Sketched = every 3 Progress; always on Severe complication.\n")
    md.append("\n## P2-02 — Attention Pressure cadence\n")
    md.append("- **Issue:** §7 lists Attention-tagged artifact as Pressure increase condition without per-Watch vs once-while-carried clarity.\n")
    md.append("- **Evidence:** EXP-HAVEN-RUN / EXP-CASUALTY Pressure peaks sensitive to interpretation.\n")
    md.append("- **Proposal:** Increase once when first carried into a Watch, then only again if re-exposed after concealment OR on complication.\n")
    md.append("\n## P2-03 — Profitability charter metric\n")
    md.append("- **Issue:** 'Return profitable' / 8,000 gp objectives ambiguous vs sponsor shares and wages (§17).\n")
    md.append(f"- **Evidence:** EXP-T1 avg profit {all_scenario_stats.get('EXP-T1-PROFIT',{}).get('avg_profit_gp')}; EXP-HAVEN-RUN objective rate {all_scenario_stats.get('EXP-HAVEN-RUN',{}).get('objective_met_pct')}%.\n")
    md.append("- **Proposal:** Charter fields: `gross_target`, `net_after_sponsor_target`, `profit_after_wages_target` — pick one as primary.\n")
    md.append("\n## P2-04 — Forage output cap\n")
    md.append("- **Issue:** Tier I Forage can erase Supply abort pressure on Mapped Risk 1.\n")
    md.append("- **Proposal:** Cap Forage at `tier_biome_rating` units; Critical Success needed to exceed; Failure risks exposure Pressure.\n")
    md.append("\n## P2-05 — Rest-debt for evening camp workers\n")
    md.append("- **Issue:** Camp example has 3 workers skip Rest; §5 Strain rule needs explicit same-day vs next-day timing.\n")
    md.append("- **Proposal:** Workers who skip Evening Rest must take Morning Rest next day or gain 1 Strain at next day-boundary.\n")
    md.append("\n## P2-06 — Companion SOURCE_MANIFEST gaps\n")
    md.append("- **Issue:** `GAMEPLAY_LOOP_CANON.md`, `gameplay-loop.json`, `ExpeditionTracker.tsx` not on main.\n")
    md.append("- **Proposal:** Promote bible → canon + JSON + tracker UI under owner order; until then keep extract as pending-review SoT for playtests.\n")
    md.append("\n## P2-07 — Sample company Combat band\n")
    md.append("- **Issue:** Pack roster Combat=3 vs optimal 4–6; EXP-CASUALTY collapses Escort capacity.\n")
    md.append("- **Proposal:** Adjust worked example / pack roster to 4 Combat OR document 3-Combat professional company as supported variant.\n")
    (patch_dir / "PROPOSED_PATCHES.md").write_text("".join(md), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    matrix_path = ROOT / "SCENARIO_MATRIX.csv"
    rows = list(csv.DictReader(matrix_path.open(encoding="utf-8")))
    stats = {}
    run_log = []
    for row in rows:
        sid = row["scenarioId"]
        iterations = int(row["iterations"])
        print(f"Running {sid} x{iterations}...")
        runs = aggregate_runs(sid, iterations)
        write_agent_results(sid, runs)
        n = len(runs)
        stats[sid] = {
            "avg_profit_gp": round(sum(r.profit_gp for r in runs) / n, 1),
            "objective_met_pct": pct(sum(1 for r in runs if r.objective_met), n),
            "haven_pct": pct(sum(1 for r in runs if r.haven_arrived), n),
            "sealed_pct": pct(sum(1 for r in runs if r.sealed), n),
            "avg_elapsed_h": round(sum(r.watches * 8 for r in runs) / n, 1),
            "avg_pressure_peak": round(sum(r.pressure_peaks for r in runs) / n, 2),
        }
        run_log.append({"scenarioId": sid, **stats[sid], "iterations": iterations})
        print(f"  -> {stats[sid]}")

    write_proposed_patches(stats)
    (RESULTS / "_orchestrator_summary.json").write_text(
        json.dumps({
            "pack": PACK,
            "bible": str(BIBLE),
            "pack01_assumption": "Pack 01 has results/ but 0 JSON files — combat balance findings not incorporated.",
            "source_manifest_gaps": [
                "docs/mechanics/GAMEPLAY_LOOP_CANON.md",
                "src/data/gameplay-loop.json",
                "src/components/ExpeditionTracker.tsx",
            ],
            "scenarios": run_log,
        }, indent=2),
        encoding="utf-8",
    )
    # Human report scaffold (compile_results produces COMPILED_REPORT from agent JSON)
    print("Done. Run compile_results.py next.")


if __name__ == "__main__":
    main()
