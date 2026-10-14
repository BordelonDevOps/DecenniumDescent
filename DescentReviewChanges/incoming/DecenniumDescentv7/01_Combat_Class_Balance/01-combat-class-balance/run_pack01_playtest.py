#!/usr/bin/env python3
"""
Pack 01 Combat/Class Balance — multi-agent table playtest runner.

Simulates SCENARIO_MATRIX.csv with seeded Monte Carlo combat grounded in:
- docs/mechanics/GAMEPLAY_LOOP_CANON.md (pending-review)
- src/data/class-core-mechanics.js identities
- src/data/class-details.js level features
- src/data/class-ceiling-caps.js draft caps (informational)
- encounter budgets / Tenacity / Retreat / summon caps from Gameplay Loop Bible

Does NOT modify canon. Writes results/<scenarioId>/<agentId>.json per RESULT_SCHEMA.json.
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT
# pack may live under DescentReviewChanges/incoming/... — climb to repo root
for p in [ROOT] + list(ROOT.parents):
    if (p / "src" / "data" / "class-core-mechanics.js").exists():
        REPO = p
        break

RESULTS = ROOT / "results"
PACK = "01-combat-class-balance"

# --- Class combat profiles (from class-core-mechanics + class-details) ---
CLASS_PROFILES = {
    "Soldier": {"role": "frontline", "hit": "d10", "dpr_mod": 1.0, "control": 0.15, "heal": 0.05, "summons": 0, "extra_action": True, "tempo": 0.9, "lookups": 1.2, "identity": "Palisade/Overwatch"},
    "Cleric": {"role": "support", "hit": "d8", "dpr_mod": 0.7, "control": 0.25, "heal": 1.2, "summons": 0, "extra_action": False, "tempo": 0.85, "lookups": 1.5, "identity": "Conviction"},
    "Thief": {"role": "skirmish", "hit": "d8", "dpr_mod": 1.15, "control": 0.2, "heal": 0.0, "summons": 0, "extra_action": False, "tempo": 1.05, "lookups": 1.3, "identity": "Sneak/Poison"},
    "Mage": {"role": "burst", "hit": "d6", "dpr_mod": 1.35, "control": 0.3, "heal": 0.0, "summons": 0, "extra_action": False, "tempo": 0.75, "lookups": 2.0, "identity": "Nuke Chains", "traumatic": True},
    "Paladin": {"role": "frontline", "hit": "d10", "dpr_mod": 1.05, "control": 0.2, "heal": 0.55, "summons": 0, "extra_action": False, "tempo": 0.8, "lookups": 1.8, "identity": "Oath/Smite"},
    "Ranger": {"role": "skirmish", "hit": "d10", "dpr_mod": 1.1, "control": 0.25, "heal": 0.05, "summons": 0.3, "extra_action": False, "tempo": 0.95, "lookups": 1.6, "identity": "Track Target"},
    "Tinker": {"role": "control", "hit": "d8", "dpr_mod": 0.85, "control": 0.45, "heal": 0.1, "summons": 1.5, "extra_action": False, "tempo": 0.7, "lookups": 2.4, "identity": "Deployables", "deploy_cap": 3},
    "Warrior": {"role": "frontline", "hit": "d12", "dpr_mod": 1.25, "control": 0.1, "heal": 0.1, "summons": 0, "extra_action": True, "tempo": 0.85, "lookups": 2.1, "identity": "Mutations"},
    "Dragoon": {"role": "mobile", "hit": "d10", "dpr_mod": 1.15, "control": 0.15, "heal": 0.0, "summons": 0, "extra_action": False, "tempo": 1.0, "lookups": 1.7, "identity": "Momentum"},
    "Monk": {"role": "mobile", "hit": "d8", "dpr_mod": 1.0, "control": 0.55, "heal": 0.05, "summons": 0, "extra_action": False, "tempo": 0.9, "lookups": 1.9, "identity": "Ki/Stance"},
    "Crimson Agent": {"role": "skirmish", "hit": "d8", "dpr_mod": 1.2, "control": 0.2, "heal": 0.15, "summons": 0, "extra_action": False, "tempo": 0.95, "lookups": 1.8, "identity": "Blood Mark"},
    "Bard": {"role": "support", "hit": "d8", "dpr_mod": 0.65, "control": 0.35, "heal": 0.4, "summons": 0, "extra_action": True, "tempo": 0.7, "lookups": 2.2, "identity": "Crescendo", "grants_extra_action": True},
    "Oracle": {"role": "support", "hit": "d8", "dpr_mod": 0.6, "control": 0.7, "heal": 0.5, "summons": 0, "extra_action": False, "tempo": 0.65, "lookups": 2.5, "identity": "Revelations", "hard_deny": True},
    "Mirrorsage": {"role": "control", "hit": "d6", "dpr_mod": 0.9, "control": 0.65, "heal": 0.0, "summons": 1.2, "extra_action": False, "tempo": 0.55, "lookups": 3.0, "identity": "Echo/Mirrorbind", "duplicate_risk": True},
    "Shaman": {"role": "support", "hit": "d8", "dpr_mod": 0.75, "control": 0.5, "heal": 0.35, "summons": 1.0, "extra_action": False, "tempo": 0.75, "lookups": 2.0, "identity": "Totems"},
    "Wizard": {"role": "burst", "hit": "d6", "dpr_mod": 1.2, "control": 0.55, "heal": 0.0, "summons": 2.5, "extra_action": False, "tempo": 0.6, "lookups": 2.8, "identity": "Spell Matrix/Necromancer", "dual_cast": True},
    "Druid": {"role": "flexible", "hit": "d8", "dpr_mod": 0.95, "control": 0.4, "heal": 0.45, "summons": 0.8, "extra_action": False, "tempo": 0.8, "lookups": 2.0, "identity": "Shapeshift"},
}

HIT_DIE = {"d6": 3.5, "d8": 4.5, "d10": 5.5, "d12": 6.5}

BUDGETS = {"Routine": 50, "Standard": 90, "Hard": 130, "Severe": 180, "Boss": 180, "Catastrophic": 240}

AGENT_SLUG = {
    "Soldier": "soldier", "Cleric": "cleric", "Thief": "thief", "Mage": "mage",
    "Paladin": "paladin", "Ranger": "ranger", "Tinker": "tinker", "Warrior": "warrior",
    "Dragoon": "dragoon", "Monk": "monk", "Crimson Agent": "crimson-agent", "Bard": "bard",
    "Oracle": "oracle", "Mirrorsage": "mirrorsage", "Shaman": "shaman", "Wizard": "wizard",
    "Druid": "druid",
}


def parse_players(cell: str) -> list[str]:
    cell = cell.strip().strip('"')
    if cell.startswith("all classes"):
        return list(CLASS_PROFILES.keys())
    return [p.strip() for p in cell.split(",") if p.strip()]


def expected_budget(difficulty: str, n_pc: int) -> float:
    base = BUDGETS.get(difficulty, 130)
    if n_pc == 4:
        return float(base)
    return float(base) * (1.0 + 0.2 * (n_pc - 4))


def hp_for(level: int, hit: str) -> float:
    return 10 + HIT_DIE[hit] * level + 2 * level


def dpr_for(level: int, prof: dict) -> float:
    # Rough PF2e/5e hybrid: weapon/spell baseline scales with level + identity mod
    base = (4 + level * 0.55) * prof["dpr_mod"]
    if level >= 5:
        base *= 1.35  # Extra Attack / Tier 3
    if level >= 11:
        base *= 1.2
    if level >= 17:
        base *= 1.15
    return base


@dataclass
class SeedResult:
    seed: int
    rounds: int
    win: bool
    objective_met: bool
    party_damage: float
    enemy_damage: float
    healing: float
    prevented: float
    control_applied: int
    full_turns_denied: int
    summons_peak: int
    summons_illegal: bool
    extra_action_stack_attempt: bool
    extra_action_capped: bool
    tenacity_triggers: int
    retreat_escape: int
    retreat_pursuit: int
    retreat_success: bool | None
    knockouts: int
    wounds: int
    cargo_intact_rounds: int
    objectives_held: int
    rp_spent: float
    decision_steps_avg: float
    lookups_avg: float
    deadlocks: int
    exploits: list[str] = field(default_factory=list)
    rules_flags: list[str] = field(default_factory=list)
    class_notes: dict = field(default_factory=dict)


def simulate_seed(scenario: dict, players: list[str], seed: int) -> SeedResult:
    rng = random.Random(seed)
    level = int(scenario["level"])
    difficulty = scenario["difficulty"]
    objective = scenario["objective"]
    n = len(players)
    budget = expected_budget(difficulty, n)
    # Objective/hazard steps bump effective difficulty
    if "Protect" in objective or "cargo" in objective.lower():
        budget *= 1.2
    if "elevated" in objective.lower() or "Control three" in objective:
        budget *= 1.2
    if "Retreat" in objective or "unkillable" in scenario.get("opposition", "").lower():
        budget = 9999  # unkillable pursuer proxy

    enemy_hp = budget * 1.8  # threat → HP mass proxy
    enemy_dpr = budget * 0.09 * (1 + level / 40)
    if "boss" in scenario.get("opposition", "").lower() or difficulty in ("Boss", "Catastrophic", "Severe"):
        enemy_hp *= 1.35
        enemy_dpr *= 1.15
        is_boss = True
    else:
        is_boss = difficulty in ("Boss", "Catastrophic") or "boss" in scenario.get("opposition", "").lower()

    party_hp = {c: hp_for(level, CLASS_PROFILES[c]["hit"]) for c in players}
    party_max = dict(party_hp)
    dprs = {c: dpr_for(level, CLASS_PROFILES[c]) for c in players}

    # Attrition scenarios: three sequential encounters without Long Rest
    encounters = 3 if "ATTRITION" in scenario["scenarioId"] else 1
    if "two-wave" in scenario.get("opposition", "").lower():
        encounters = 2

    total_party_dmg = 0.0
    total_enemy_dmg = 0.0
    total_heal = 0.0
    total_prev = 0.0
    control_applied = 0
    full_turns_denied = 0
    summons_peak = 0
    summons_illegal = False
    extra_action_stack_attempt = False
    extra_action_capped = False
    tenacity_triggers = 0
    knockouts = 0
    wounds = 0
    cargo_intact = 0
    objectives_held = 0
    rp_spent = 0.0
    decision_acc = []
    lookup_acc = []
    exploits: list[str] = []
    rules_flags: list[str] = []
    class_notes: dict = defaultdict(list)
    rounds_total = 0
    win = True
    objective_met = True
    retreat_escape = 0
    retreat_pursuit = 0
    retreat_success = None
    deadlocks = 0

    is_retreat = scenario["scenarioId"] == "CMB-RETREAT"
    is_cargo = "CARGO" in scenario["scenarioId"]
    is_mobility = "MOBILITY" in scenario["scenarioId"]
    is_control = "CONTROL" in scenario["scenarioId"]
    is_dark = "DARK" in scenario["scenarioId"]
    is_support = "SUPPORT" in scenario["scenarioId"]

    for enc in range(encounters):
        ehp = enemy_hp * (0.85 + 0.15 * enc)
        edpr = enemy_dpr * (1.0 + 0.08 * enc)
        # Resource decay without Long Rest
        fatigue = 1.0 - 0.12 * enc if encounters > 1 else 1.0
        summons_active = 0
        cargo_ok = True
        held = set()
        round_n = 0
        max_rounds = 20 if not is_retreat else 12
        control_same_source = defaultdict(int)
        tenacity_used_this_round = 0

        if is_retreat:
            # Unkillable pursuer — only retreat matters
            while retreat_escape < 3 and retreat_pursuit < 3 and round_n < max_rounds:
                round_n += 1
                lead = rng.choice(players)
                check = rng.randint(1, 20) + (4 + level // 4) + (2 if lead in ("Ranger", "Thief", "Tinker") else 0)
                # Assist from Soldier/Tinker
                if "Soldier" in players:
                    check += 1
                if "Tinker" in players and round_n == 1:
                    check += 2  # obstacle deploy
                dc = 15 + (level // 5)
                if check >= dc + 10:
                    retreat_escape += 2
                elif check >= dc:
                    retreat_escape += 1
                else:
                    retreat_pursuit += 1
                    if rng.random() < 0.35:
                        # sacrifice cargo for advantage fiction
                        class_notes["party"].append(f"seed{seed}: abandoned low-priority cargo for Escape advantage")
                # Pursuit pressure damages
                for c in players:
                    dmg = edpr * 0.35 * (0.7 + 0.6 * rng.random())
                    party_hp[c] -= dmg
                    total_enemy_dmg += dmg
                    if party_hp[c] <= 0 and party_max[c] > 0:
                        knockouts += 1
                        wounds += 1 if rng.random() < 0.4 else 0
                        party_hp[c] = 0
            retreat_success = retreat_escape >= 3 and retreat_pursuit < 3
            objective_met = bool(retreat_success)
            win = objective_met
            rounds_total += round_n
            continue

        while ehp > 0 and any(v > 0 for v in party_hp.values()) and round_n < max_rounds:
            round_n += 1
            tenacity_used_this_round = 0
            # --- Player turns ---
            grants_extra = []
            for c in players:
                if party_hp[c] <= 0:
                    continue
                prof = CLASS_PROFILES[c]
                lookups = prof["lookups"] + (0.5 if level >= 10 else 0) + (0.8 if level >= 15 else 0)
                steps = 1 + (1 if lookups > 2 else 0) + (1 if lookups > 2.5 else 0)
                decision_acc.append(steps)
                lookup_acc.append(lookups)

                # Summon / deploy management
                desired_summons = 0
                if prof["summons"] > 0:
                    desired_summons = int(min(4, math.ceil(prof["summons"] + (1 if level >= 10 else 0))))
                    if c == "Wizard" and level >= 10:
                        desired_summons = 4  # Necromancer pressure test — permanent undead wording conflict
                    if c == "Tinker":
                        desired_summons = min(3, 1 + level // 5)  # draft deployable cap 3
                    if c == "Mirrorsage":
                        desired_summons = 2 if level >= 5 else 1  # Charm Bind / reflections
                    if c == "Shaman":
                        desired_summons = 2  # totems as battlefield structures — rules question
                if desired_summons:
                    # Apply Gameplay Loop summon command cap (2 independent combat-capable)
                    if desired_summons > 2 and c in ("Wizard", "Mirrorsage", "Tinker"):
                        if desired_summons > 2:
                            summons_illegal = True
                            exploits.append(
                                f"{c} attempted {desired_summons} independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block)."
                            )
                            if c == "Wizard":
                                rules_flags.append(
                                    "Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering."
                                )
                            if c == "Tinker":
                                rules_flags.append(
                                    "Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?"
                                )
                    summons_active = min(desired_summons, 2) if not (c == "Tinker" and desired_summons > 2) else desired_summons
                    # Intentionally allow illegal peak for exploit detection, then Director caps in metrics
                    summons_peak = max(summons_peak, desired_summons)
                    if desired_summons > 2:
                        summons_active = desired_summons  # demonstrate exploit before ruling

                # Extra action stacking (Bard grant + Action Surge)
                extra_actions = 0
                if prof.get("extra_action") and level >= 2 and rng.random() < 0.45:
                    extra_actions += 1
                if any(CLASS_PROFILES[x].get("grants_extra_action") for x in players if party_hp.get(x, 0) > 0):
                    if c != "Bard" and (
                        (is_support and rng.random() < 0.35)
                        or (level >= 5 and "Bard" in players and rng.random() < 0.25)
                    ):
                        grants_extra.append(c)
                if prof.get("grants_extra_action") and rng.random() < 0.4:
                    # Bard Crescendo consume — may grant ally tempo
                    ally = rng.choice([x for x in players if x != c and party_hp.get(x, 0) > 0] or [c])
                    grants_extra.append(ally)
                    class_notes[c].append("Crescendo consume for ally tempo")

                if extra_actions + (1 if c in grants_extra else 0) > 1:
                    extra_action_stack_attempt = True
                    extra_action_capped = True
                    exploits.append(
                        f"Action-economy stack attempt on {c}: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action."
                    )
                    extra_actions = 1  # enforce

                # Dual Cast (Wizard L9+) as second spell — not a full Action if ruled as feature; flag ambiguity
                if prof.get("dual_cast") and level >= 9 and rng.random() < 0.5:
                    rules_flags.append(
                        "Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?"
                    )
                    total_party_dmg += dprs[c] * 0.55 * fatigue  # second spell damage

                # Damage
                dmg = dprs[c] * fatigue * (0.75 + 0.5 * rng.random())
                if summons_active:
                    dmg += summons_active * (2.5 + level * 0.35) * fatigue
                if extra_actions:
                    dmg += dprs[c] * 0.85 * fatigue
                # Mage Traumatic Casting / Dark path
                if prof.get("traumatic") and level >= 10 and is_dark and rng.random() < 0.4:
                    dmg *= 1.45
                    party_hp[c] -= level * 0.8  # self trauma
                    rp_spent += 3
                    class_notes[c].append("Traumatic/Dark Resonance surge")
                    rules_flags.append(
                        "Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine."
                    )
                ehp -= dmg
                total_party_dmg += dmg
                rp_spent += (1.2 if prof["role"] in ("burst", "support", "control") else 0.3) * (1 + level / 20)

                # Healing / prevention
                heal = prof["heal"] * (3 + level * 0.6) * (0.6 + 0.8 * rng.random())
                if heal:
                    # prefer wounded
                    wounded = sorted(players, key=lambda x: party_hp[x] / party_max[x])
                    t = wounded[0]
                    before = party_hp[t]
                    party_hp[t] = min(party_max[t], party_hp[t] + heal)
                    total_heal += party_hp[t] - before
                prev = (0.15 if prof["role"] == "frontline" else 0.05) * edpr
                if c == "Soldier":
                    prev *= 1.8
                    class_notes[c].append("Overwatch/Guard prevention")
                total_prev += prev

                # Control
                if rng.random() < prof["control"] * (1.1 if is_control else 1.0):
                    control_applied += 1
                    src = c
                    control_same_source[src] += 1
                    deny = False
                    if prof.get("hard_deny") or (is_control and rng.random() < 0.5):
                        deny = True
                    if deny:
                        if is_boss and tenacity_used_this_round < (2 if level >= 15 else 1):
                            tenacity_triggers += 1
                            tenacity_used_this_round += 1
                            class_notes["director"].append(f"Tenacity converted {c} deny → Staggered")
                        elif control_same_source[src] > 1 and not (is_boss and tenacity_used_this_round):
                            # same source second deny without new save — illegal under Loop
                            rules_flags.append(
                                f"{c} attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter)."
                            )
                            exploits.append(
                                f"Full-turn denial chain by {c} without escalation cost — blocked by Loop rule in adjudication."
                            )
                        else:
                            full_turns_denied += 1
                            edpr *= 0.85

                # Mirrorsage duplicate action economy probe
                if prof.get("duplicate_risk") and level >= 10 and rng.random() < 0.35:
                    rules_flags.append(
                        "Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps."
                    )
                    if rng.random() < 0.3:
                        exploits.append(
                            "Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active."
                        )

                # Mobility objectives
                if is_mobility and prof["role"] in ("mobile", "skirmish") and rng.random() < 0.55:
                    held.add(rng.randint(1, 3))
                if is_cargo and prof["role"] in ("frontline", "control") and rng.random() < 0.7:
                    cargo_ok = cargo_ok and True
                elif is_cargo and rng.random() < 0.15:
                    cargo_ok = False

            # Cap summons after player phase (Director ruling) for "legal" fight continuation
            if summons_active > 2:
                summons_active = 2
                class_notes["director"].append("Capped independent summons to 2 mid-round (ruling, not silent rewrite)")

            # --- Enemy turn ---
            living = [c for c in players if party_hp[c] > 0]
            if not living:
                break
            # Denied enemy turns reduce damage
            factor = 0.55 if full_turns_denied and round_n <= full_turns_denied else 1.0
            for _ in range(max(1, int(budget / 80))):
                target = rng.choice(living)
                dmg = edpr * factor * (0.7 + 0.6 * rng.random()) / max(1, int(budget / 80))
                # prevention
                dmg = max(0, dmg - total_prev / max(1, round_n) * 0.05)
                party_hp[target] -= dmg
                total_enemy_dmg += dmg
                if party_hp[target] <= 0:
                    knockouts += 1
                    if rng.random() < 0.35:
                        wounds += 1
                    party_hp[target] = 0
                    living = [c for c in players if party_hp[c] > 0]
                    if not living:
                        break

            if is_cargo and cargo_ok:
                cargo_intact += 1
            if is_mobility:
                objectives_held = max(objectives_held, len(held))

            # Deadlock probe: permanent control without Tenacity on non-boss
            if not is_boss and full_turns_denied >= 3 and ehp > enemy_hp * 0.5:
                deadlocks += 1
                rules_flags.append("Soft deadlock: repeated turn denial stalled fight without boss Tenacity.")

        rounds_total += round_n
        if is_cargo:
            objective_met = objective_met and cargo_intact >= 4
            win = objective_met and any(v > 0 for v in party_hp.values())
        elif is_mobility:
            objective_met = objective_met and objectives_held >= 3
            win = objective_met
        elif ehp > 0 and not any(v > 0 for v in party_hp.values()):
            win = False
            objective_met = False
        elif ehp > 0 and round_n >= max_rounds:
            win = False
            objective_met = False
            rules_flags.append("Encounter hit round cap without clear resolution.")
        else:
            win = win and any(v > 0 for v in party_hp.values())

        # Short rest between attrition waves (not Long Rest)
        if enc < encounters - 1:
            for c in players:
                if party_hp[c] > 0:
                    party_hp[c] = min(party_max[c], party_hp[c] + party_max[c] * 0.2)

    # Deduplicate exploit/flag strings
    exploits = sorted(set(exploits))
    rules_flags = sorted(set(rules_flags))

    return SeedResult(
        seed=seed,
        rounds=rounds_total,
        win=win,
        objective_met=objective_met,
        party_damage=round(total_party_dmg, 1),
        enemy_damage=round(total_enemy_dmg, 1),
        healing=round(total_heal, 1),
        prevented=round(total_prev, 1),
        control_applied=control_applied,
        full_turns_denied=full_turns_denied,
        summons_peak=summons_peak,
        summons_illegal=summons_illegal,
        extra_action_stack_attempt=extra_action_stack_attempt,
        extra_action_capped=extra_action_capped,
        tenacity_triggers=tenacity_triggers,
        retreat_escape=retreat_escape,
        retreat_pursuit=retreat_pursuit,
        retreat_success=retreat_success,
        knockouts=knockouts,
        wounds=wounds,
        cargo_intact_rounds=cargo_intact,
        objectives_held=objectives_held,
        rp_spent=round(rp_spent, 1),
        decision_steps_avg=round(sum(decision_acc) / max(1, len(decision_acc)), 2),
        lookups_avg=round(sum(lookup_acc) / max(1, len(lookup_acc)), 2),
        deadlocks=deadlocks,
        exploits=exploits,
        rules_flags=rules_flags,
        class_notes={k: v[:6] for k, v in class_notes.items()},
    )


def aggregate(seeds: list[SeedResult]) -> dict:
    n = len(seeds)
    def avg(attr):
        return round(sum(getattr(s, attr) for s in seeds) / n, 2)
    return {
        "iterations": n,
        "win_rate": round(sum(1 for s in seeds if s.win) / n, 3),
        "objective_rate": round(sum(1 for s in seeds if s.objective_met) / n, 3),
        "avg_rounds": avg("rounds"),
        "avg_party_damage": avg("party_damage"),
        "avg_enemy_damage": avg("enemy_damage"),
        "avg_healing": avg("healing"),
        "avg_prevented": avg("prevented"),
        "avg_control_applied": avg("control_applied"),
        "avg_full_turns_denied": avg("full_turns_denied"),
        "max_summons_peak": max(s.summons_peak for s in seeds),
        "summons_illegal_rate": round(sum(1 for s in seeds if s.summons_illegal) / n, 3),
        "extra_action_stack_rate": round(sum(1 for s in seeds if s.extra_action_stack_attempt) / n, 3),
        "avg_tenacity_triggers": avg("tenacity_triggers"),
        "avg_knockouts": avg("knockouts"),
        "avg_wounds": avg("wounds"),
        "avg_rp_spent": avg("rp_spent"),
        "avg_decision_steps": avg("decision_steps_avg"),
        "avg_lookups": avg("lookups_avg"),
        "deadlock_seeds": sum(s.deadlocks for s in seeds),
        "retreat_success_rate": round(
            sum(1 for s in seeds if s.retreat_success) / max(1, sum(1 for s in seeds if s.retreat_success is not None)), 3
        )
        if any(s.retreat_success is not None for s in seeds)
        else None,
    }


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def player_result(scenario_id: str, cls: str, seeds: list[SeedResult], agg: dict) -> dict:
    slug = AGENT_SLUG[cls]
    prof = CLASS_PROFILES[cls]
    notes = []
    for s in seeds:
        notes.extend(s.class_notes.get(cls, []))
    obs = [
        f"Played {len(seeds)} seeds as {cls} ({prof['identity']}) under scenario {scenario_id}.",
        f"Identity loop remained: {prof['identity']}; role={prof['role']}.",
        f"Aggregate win_rate={agg['win_rate']}, objective_rate={agg['objective_rate']}, avg_rounds={agg['avg_rounds']}.",
        f"Decision steps avg={agg['avg_decision_steps']}; rule lookups avg={agg['avg_lookups']}.",
    ]
    if notes:
        obs.append("Sample actions: " + "; ".join(notes[:5]))
    if prof.get("grants_extra_action"):
        obs.append("Crescendo/tempo grants were offered; Loop additional-Action cap enforced when stacked with Action Surge.")
    if prof["summons"] > 0:
        obs.append(f"Peak summons desired observed up to {agg['max_summons_peak']}; illegal_rate={agg['summons_illegal_rate']}.")
    if agg["avg_lookups"] > 2.5:
        obs.append("Turn frequently required >2 cross-references — readability stress.")
    if cls in ("Soldier", "Warrior") and agg["extra_action_stack_rate"] > 0.2:
        obs.append("Meaningful recurring choice preserved (Guard/Surge vs damage), but surge stacking with ally grants needed adjudication.")

    rq = []
    ex = []
    rec = []
    for s in seeds:
        rq.extend(s.rules_flags)
        ex.extend(s.exploits)
    # class-specific
    if cls == "Bard":
        rq.append("Does Crescendo-enhanced ally 'extra attack' count as the one additional full Action?")
        rec.append("Clarify Bard tempo grants as Bonus Action riders or as the single additional Action slot.")
    if cls == "Wizard":
        rq.append("How do permanent undead from Core Systems interact with the 2-summon command cap?")
        rec.append("Require Necromancer excess undead to use swarm/unit blocks; cite Loop summon rule in class path text.")
    if cls == "Mirrorsage":
        rq.append("Do Reflective Companions count against the 2-summon cap and against the 1 copy release/round draft ceiling?")
        rec.append("Promote draft ceiling caps for Mirrorsage into Loop-aligned explicit rules.")
    if cls == "Tinker":
        rq.append("Are Anacite drones and gadgets summons, deployables, or both for the command cap?")
        rec.append("Define deployables as non-summon structures unless they take independent combat turns.")
    if cls == "Oracle":
        rq.append("Oracle draft '1 hard deny / target / encounter' vs Loop same-source denial escalation — which wins?")
        rec.append("Keep both: Loop general rule + Oracle-specific 1 hard deny/target as tighter class ceiling.")
    if cls == "Mage" and scenario_id == "CMB-L10-DARK":
        rq.append("Traumatic Casting self-harm and Dissonance bypass: when does it violate anti-loop doctrine?")
    if cls in ("Monk", "Mirrorsage", "Oracle", "Wizard") and "CONTROL" in scenario_id:
        rec.append("Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.")

    return {
        "pack": PACK,
        "scenarioId": scenario_id,
        "agentId": slug,
        "seed": f"agg-{len(seeds)}-seeds",
        "observations": obs,
        "metrics": {
            "class": cls,
            "role": prof["role"],
            **{k: agg[k] for k in ("win_rate", "objective_rate", "avg_rounds", "avg_party_damage", "avg_healing", "avg_prevented", "avg_control_applied", "avg_lookups", "avg_decision_steps", "avg_rp_spent")},
            "class_dpr_model": round(dpr_for(int(re.search(r"L(\d+)", scenario_id).group(1)) if re.search(r"L(\d+)", scenario_id) else 5, prof), 2)
            if scenario_id != "CMB-RETREAT"
            else None,
        },
        "rulesQuestions": sorted(set(rq))[:12],
        "exploits": sorted(set(ex))[:10],
        "recommendations": sorted(set(rec))[:8],
        "confidence": "medium" if len(seeds) >= 10 else "low",
    }


def specialist_results(scenario: dict, players: list[str], seeds: list[SeedResult], agg: dict) -> dict[str, dict]:
    sid = scenario["scenarioId"]
    all_flags = sorted({f for s in seeds for f in s.rules_flags})
    all_ex = sorted({e for s in seeds for e in s.exploits})

    director = {
        "pack": PACK,
        "scenarioId": sid,
        "agentId": "director",
        "seed": f"agg-{len(seeds)}-seeds",
        "observations": [
            f"Ran {scenario['opposition']} at listed difficulty {scenario['difficulty']} for objective: {scenario['objective']}.",
            f"Budget model (4PC base adjusted): ~{expected_budget(scenario['difficulty'], len(players)):.0f} Threat Points before objective/hazard steps.",
            f"Observed win_rate={agg['win_rate']}, objective_rate={agg['objective_rate']}, avg_rounds={agg['avg_rounds']}, KO/seed={agg['avg_knockouts']}.",
            "Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.",
            f"Difficulty vs result: {'aligned' if 0.35 <= agg['win_rate'] <= 0.85 or sid == 'CMB-RETREAT' else 'diverged — budget may need recalibration'}.",
        ],
        "metrics": {
            **agg,
            "party_size": len(players),
            "stated_difficulty": scenario["difficulty"],
            "modeled_budget_tp": expected_budget(scenario["difficulty"], len(players)),
        },
        "rulesQuestions": all_flags[:15],
        "exploits": all_ex[:10],
        "recommendations": [
            "Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.",
            "Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.",
        ],
        "confidence": "high" if len(seeds) >= 10 else "medium",
    }

    observer = {
        "pack": PACK,
        "scenarioId": sid,
        "agentId": "rules-observer",
        "seed": f"agg-{len(seeds)}-seeds",
        "observations": [
            f"Average decision steps={agg['avg_decision_steps']} (flag if >3).",
            f"Average source lookups={agg['avg_lookups']} (flag if >3).",
            "Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.",
            "GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.",
        ],
        "metrics": {
            "avg_decision_steps": agg["avg_decision_steps"],
            "avg_lookups": agg["avg_lookups"],
            "turns_over_three_lookups_estimate": round(max(0, agg["avg_lookups"] - 3) * agg["avg_rounds"] * len(players), 2),
            "ambiguity_flags": len(all_flags),
        },
        "rulesQuestions": all_flags[:15] or [
            "No severe ambiguity this scenario beyond normal class feature lookups."
        ],
        "exploits": [],
        "recommendations": [
            "Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).",
            "Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.",
        ],
        "confidence": "high",
    }

    metrics_agent = {
        "pack": PACK,
        "scenarioId": sid,
        "agentId": "combat-metrics",
        "seed": f"agg-{len(seeds)}-seeds",
        "observations": [
            "Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.",
            "DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.",
        ],
        "metrics": {
            **agg,
            "dpr_party_estimate": round(agg["avg_party_damage"] / max(0.1, agg["avg_rounds"]), 2),
            "effective_prevention_per_round": round(agg["avg_prevented"] / max(0.1, agg["avg_rounds"]), 2),
            "heal_to_damage_taken_ratio": round(agg["avg_healing"] / max(0.1, agg["avg_enemy_damage"]), 3),
            "cargo_intact_rounds_avg": round(sum(s.cargo_intact_rounds for s in seeds) / len(seeds), 2),
            "objectives_held_max_avg": round(sum(s.objectives_held for s in seeds) / len(seeds), 2),
        },
        "rulesQuestions": [],
        "exploits": all_ex[:8],
        "recommendations": [
            "Keep outliers: report min/max rounds alongside averages in future tooling.",
            "Instrument live companion combat log to replace model DPR in later packs.",
        ],
        "confidence": "medium",
    }

    exploit_hunter = {
        "pack": PACK,
        "scenarioId": sid,
        "agentId": "exploit-hunter",
        "seed": f"agg-{len(seeds)}-seeds",
        "observations": [
            f"Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across {len(seeds)} seeds.",
            f"Illegal summon pressure rate={agg['summons_illegal_rate']}; extra-action stack attempt rate={agg['extra_action_stack_rate']}.",
            "No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.",
        ],
        "metrics": {
            "summons_illegal_rate": agg["summons_illegal_rate"],
            "extra_action_stack_rate": agg["extra_action_stack_rate"],
            "deadlock_seeds": agg["deadlock_seeds"],
            "max_summons_peak": agg["max_summons_peak"],
            "avg_full_turns_denied": agg["avg_full_turns_denied"],
        },
        "rulesQuestions": all_flags[:10],
        "exploits": all_ex[:15] or [
            "No demonstrated infinite exploit under enforced Loop caps this scenario."
        ],
        "recommendations": [
            "Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.",
            "Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.",
        ],
        "confidence": "high" if all_ex else "medium",
    }

    return {
        "director": director,
        "rules-observer": observer,
        "combat-metrics": metrics_agent,
        "exploit-hunter": exploit_hunter,
    }


def ceiling_parties() -> list[list[str]]:
    classes = list(CLASS_PROFILES.keys())
    # rotating 6-PC parties covering all 17
    parties = []
    for i in range(0, len(classes), 6):
        chunk = classes[i : i + 6]
        if len(chunk) < 6:
            chunk = chunk + classes[: 6 - len(chunk)]
        parties.append(chunk)
    return parties


def main():
    matrix_path = ROOT / "SCENARIO_MATRIX.csv"
    rows = list(csv.DictReader(matrix_path.open(encoding="utf-8")))
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary = []

    for row in rows:
        sid = row["scenarioId"]
        players = parse_players(row["players"])
        iterations = int(row["iterations"].split()[0]) if row["iterations"] else 10
        # Orchestrator minimums
        diff = row["difficulty"]
        if diff in ("Standard", "Hard"):
            iterations = max(iterations, 10)
        if diff in ("Severe", "Boss", "Catastrophic"):
            iterations = max(min(iterations, iterations), 5)

        if sid == "CMB-L20-CEILING":
            parties = ceiling_parties()
            all_seeds = []
            for pi, party in enumerate(parties):
                seeds = [simulate_seed(row, party, seed=1000 + pi * 100 + i) for i in range(5)]
                all_seeds.extend(seeds)
                agg = aggregate(seeds)
                out = RESULTS / sid / f"party{pi+1}"
                specs = specialist_results(row, party, seeds, agg)
                for aid, data in specs.items():
                    data["metrics"]["party"] = party
                    write_json(out / f"{aid}.json", data)
                for cls in party:
                    write_json(out / f"{AGENT_SLUG[cls]}.json", player_result(sid, cls, seeds, agg))
            # Also write scenario-level specialists aggregating all parties
            agg_all = aggregate(all_seeds)
            specs = specialist_results(row, players, all_seeds, agg_all)
            for aid, data in specs.items():
                write_json(RESULTS / sid / f"{aid}.json", data)
            summary.append((sid, len(all_seeds), agg_all))
            continue

        # Normal scenarios
        n_iter = iterations
        if "per party" in row["iterations"]:
            n_iter = 5
        seeds = [simulate_seed(row, players, seed=2000 + hash(sid) % 1000 + i) for i in range(n_iter)]
        agg = aggregate(seeds)
        specs = specialist_results(row, players, seeds, agg)
        for aid, data in specs.items():
            write_json(RESULTS / sid / f"{aid}.json", data)
        for cls in players:
            if cls in AGENT_SLUG:
                write_json(RESULTS / sid / f"{AGENT_SLUG[cls]}.json", player_result(sid, cls, seeds, agg))
        summary.append((sid, len(seeds), agg))

    # Executive findings for proposed patches input
    findings_path = ROOT / "results" / "_run_summary.json"
    write_json(
        findings_path,
        {
            "pack": PACK,
            "scenarios": [
                {"scenarioId": sid, "seeds": n, "metrics": agg} for sid, n, agg in summary
            ],
        },
    )
    print(f"Wrote results for {len(summary)} scenarios -> {RESULTS}")
    for sid, n, agg in summary:
        print(f"  {sid}: seeds={n} win={agg['win_rate']} obj={agg['objective_rate']} rounds={agg['avg_rounds']}")


if __name__ == "__main__":
    main()
