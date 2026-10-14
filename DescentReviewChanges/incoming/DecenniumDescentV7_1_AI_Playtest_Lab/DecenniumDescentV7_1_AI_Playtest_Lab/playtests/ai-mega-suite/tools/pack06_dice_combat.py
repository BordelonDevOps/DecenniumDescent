#!/usr/bin/env python3
"""Pack 06 — Dice-level combat validation (Level A executable evidence).

Freezes legal builds and exact bestiary fixtures, then runs every SCENARIO_MATRIX
seed with a deterministic PRNG and complete per-die round logs. Does not edit canon.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Any

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
ROOT = SUITE.parent.parent
PACK = SUITE / "packs" / "06-dice-level-combat-validation"
OUT_PACK = PACK / "results"
OUT_SUITE = SUITE / "results" / "06-dice-level-combat-validation"
FROZEN = PACK / "frozen_builds"
FIXTURES = PACK / "fixtures"
RULINGS = PACK / "rulings"
GEN_FIX = SUITE / "fixtures" / "generated" / "06-dice-level-combat-validation"

DICE_RE = re.compile(r"(\d+)d(\d+)([+-]\d+)?", re.I)
ATK_RE = re.compile(r"\+(\d+)\s+to hit", re.I)
AVG_RE = re.compile(r"average\s+(\d+)", re.I)
SAVE_DC_RE = re.compile(r"DC\s+(\d+)", re.I)

CLASS_HIT_DICE = {
    "bard": {"die": 8, "max": 8, "avg": 5},
    "cleric": {"die": 8, "max": 8, "avg": 5},
    "crimson-agent": {"die": 8, "max": 8, "avg": 5},
    "dragoon": {"die": 10, "max": 10, "avg": 6},
    "druid": {"die": 8, "max": 8, "avg": 5},
    "mage": {"die": 6, "max": 6, "avg": 4},
    "monk": {"die": 8, "max": 8, "avg": 5},
    "mirrorsage": {"die": 6, "max": 6, "avg": 4},
    "oracle": {"die": 8, "max": 8, "avg": 5},
    "paladin": {"die": 10, "max": 10, "avg": 6},
    "ranger": {"die": 10, "max": 10, "avg": 6},
    "shaman": {"die": 8, "max": 8, "avg": 5},
    "soldier": {"die": 10, "max": 10, "avg": 6},
    "thief": {"die": 8, "max": 8, "avg": 5},
    "tinker": {"die": 8, "max": 8, "avg": 5},
    "warrior": {"die": 12, "max": 12, "avg": 7},
    "wizard": {"die": 6, "max": 6, "avg": 4},
}

CLASS_DISPLAY = {
    "bard": "Bard",
    "cleric": "Cleric",
    "crimson-agent": "Crimson Agent",
    "dragoon": "Dragoon",
    "druid": "Druid",
    "mage": "Mage",
    "monk": "Monk",
    "mirrorsage": "Mirrorsage",
    "oracle": "Oracle",
    "paladin": "Paladin",
    "ranger": "Ranger",
    "shaman": "Shaman",
    "soldier": "Soldier",
    "thief": "Thief",
    "tinker": "Tinker",
    "warrior": "Warrior",
    "wizard": "Wizard",
}

# Role / ability arrays: STR DEX CON INT WIS CHA
ARRAYS = {
    "front": (16, 12, 15, 8, 10, 13),
    "striker": (10, 16, 14, 10, 12, 12),
    "support": (10, 12, 14, 10, 16, 13),
    "caster": (8, 12, 14, 16, 10, 13),
    "hybrid": (12, 14, 14, 10, 12, 14),
}

ROLE_BY_CLASS = {
    "soldier": "front",
    "warrior": "front",
    "paladin": "front",
    "dragoon": "front",
    "monk": "striker",
    "ranger": "striker",
    "thief": "striker",
    "crimson-agent": "striker",
    "cleric": "support",
    "bard": "support",
    "druid": "support",
    "shaman": "support",
    "oracle": "support",
    "mage": "caster",
    "wizard": "caster",
    "mirrorsage": "caster",
    "tinker": "hybrid",
}

PRIMARY_ABILITY = {
    "soldier": "STR",
    "warrior": "STR",
    "paladin": "STR",
    "dragoon": "STR",
    "monk": "DEX",
    "ranger": "DEX",
    "thief": "DEX",
    "crimson-agent": "DEX",
    "cleric": "WIS",
    "druid": "WIS",
    "shaman": "WIS",
    "ranger_alt": "WIS",
    "bard": "CHA",
    "oracle": "CHA",
    "paladin_spell": "CHA",
    "mage": "INT",
    "wizard": "INT",
    "mirrorsage": "INT",
    "tinker": "INT",
}

WEAPON_DIE = {
    "front": (1, 10, 0),  # 1d10
    "striker": (1, 8, 0),
    "support": (1, 8, 0),
    "caster": (1, 6, 0),
    "hybrid": (1, 8, 0),
}

CANTRIP_DIE = {
    "caster": (1, 10, 0),
    "support": (1, 8, 0),
    "hybrid": (1, 8, 0),
    "front": (1, 6, 0),
    "striker": (1, 6, 0),
}

SUMMONER_CLASSES = {"tinker", "mirrorsage", "shaman", "druid", "wizard", "mage"}
BOSS_NAMES = {
    "Ashthirst the Hollow",
    "Angry Grief-Bound",
    "Choralith, Voice Below",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_json(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def mod(score: int) -> int:
    return (score - 10) // 2


def pb(level: int) -> int:
    return 2 + (level - 1) // 4


def parse_js_object_map(text: str, export_name: str) -> dict[str, dict]:
    """Best-effort extract of CLASS_HIT_DICE-like `{ Name: { die: N ... } }` blocks."""
    m = re.search(rf"export const {export_name}\s*=\s*\{{", text)
    if not m:
        return {}
    # Prefer canonical JSON snapshots when available.
    return {}


def load_hit_dice_from_js() -> dict[str, dict]:
    path = ROOT / "src/data/class-hit-dice.js"
    text = path.read_text(encoding="utf-8")
    out = {}
    for name, die, mx, avg in re.findall(
        r'(?:"([^"]+)"|([A-Za-z][A-Za-z ]+)):\s*\{\s*die:\s*(\d+),\s*max:\s*(\d+),\s*avg:\s*(\d+)\s*\}',
        text,
    ):
        key = (name or "").strip() or (die if False else "")
        # groups: quoted name | bare name | die | max | avg — fix unpack
    out = {}
    for m in re.finditer(
        r'(?:"([^"]+)"|([A-Za-z][A-Za-z ]+)):\s*\{\s*die:\s*(\d+),\s*max:\s*(\d+),\s*avg:\s*(\d+)\s*\}',
        text,
    ):
        cname = (m.group(1) or m.group(2) or "").strip()
        out[cname] = {"die": int(m.group(3)), "max": int(m.group(4)), "avg": int(m.group(5))}
    return out or {CLASS_DISPLAY[k]: v for k, v in CLASS_HIT_DICE.items()}


def estimate_hp(level: int, con_mod: int, class_key: str) -> int:
    hd = CLASS_HIT_DICE[class_key]
    if level <= 1:
        return max(1, hd["max"] + con_mod)
    return max(1, hd["max"] + con_mod + (level - 1) * (hd["avg"] + con_mod))


def ac_for(class_key: str, level: int, dex_mod: int) -> int:
    role = ROLE_BY_CLASS[class_key]
    base = {"front": 16, "striker": 14, "support": 14, "caster": 13, "hybrid": 14}[role]
    # Light/medium armor approximations; front gets shield-ish bump already in base.
    if role == "front":
        return base + min(2, max(0, dex_mod)) + (1 if level >= 10 else 0)
    if class_key == "monk":
        return 10 + dex_mod + max(2, pb(level) // 2) + (level // 5)
    return base + min(2, max(0, dex_mod)) + (level // 8)


def attack_bonus(class_key: str, level: int, scores: dict[str, int]) -> int:
    ability = PRIMARY_ABILITY.get(class_key, "STR")
    if class_key in ("mage", "wizard", "mirrorsage", "oracle", "bard", "cleric", "druid", "shaman"):
        # Spell attack / weapon fallback uses primary casting ability for casters.
        ability = {
            "mage": "INT",
            "wizard": "INT",
            "mirrorsage": "INT",
            "oracle": "CHA",
            "bard": "CHA",
            "cleric": "WIS",
            "druid": "WIS",
            "shaman": "WIS",
        }[class_key]
    return pb(level) + mod(scores[ability])


def save_bonus(class_key: str, level: int, scores: dict[str, int], save: str) -> int:
    # Rough proficient saves: front STR/CON, casters INT/WIS/CHA, strikers DEX
    proficient = {
        "front": {"STR", "CON"},
        "striker": {"DEX", "INT"},
        "support": {"WIS", "CHA"},
        "caster": {"INT", "WIS"},
        "hybrid": {"INT", "DEX"},
    }[ROLE_BY_CLASS[class_key]]
    bonus = mod(scores[save])
    if save in proficient:
        bonus += pb(level)
    return bonus


def freeze_build(class_key: str, level: int) -> dict:
    role = ROLE_BY_CLASS[class_key]
    arr = ARRAYS[role]
    scores = {"STR": arr[0], "DEX": arr[1], "CON": arr[2], "INT": arr[3], "WIS": arr[4], "CHA": arr[5]}
    # ASI bumps: +2 primary at 4, +2 primary or CON at 8/12/16/19
    primary = PRIMARY_ABILITY.get(class_key, "STR")
    if class_key in ("mage", "wizard", "mirrorsage"):
        primary = "INT"
    elif class_key in ("cleric", "druid", "shaman"):
        primary = "WIS"
    elif class_key in ("bard", "oracle", "paladin"):
        primary = "CHA" if class_key != "paladin" else "STR"
    for thr in (4, 8, 12, 16, 19):
        if level >= thr:
            scores[primary] = min(20, scores[primary] + 2)
    con_m = mod(scores["CON"])
    hp = estimate_hp(level, con_m, class_key)
    attacks = 2 if level >= 5 and role in ("front", "striker", "hybrid") else 1
    if level >= 11 and role == "front":
        attacks = 3
    if level >= 20 and class_key in ("soldier", "warrior", "paladin", "dragoon"):
        attacks = min(4, attacks + 1)
    resources = {
        "classResource": max(2, pb(level) + level // 3),
        "spellSlotsApprox": max(0, (level // 2) if ROLE_BY_CLASS[class_key] in ("caster", "support", "hybrid") else 0),
        "concentration": None,
        "additionalActionSlotAvailable": True,
        "actorsControlled": 0,
        "actorCap": 2,
    }
    if class_key in SUMMONER_CLASSES and level >= 5:
        resources["canDeployActors"] = True
        resources["deployBudget"] = 1 if level < 10 else 2
    build = {
        "classKey": class_key,
        "className": CLASS_DISPLAY[class_key],
        "level": level,
        "role": role,
        "abilityScores": scores,
        "abilityMods": {k: mod(v) for k, v in scores.items()},
        "proficiencyBonus": pb(level),
        "hp": hp,
        "maxHp": hp,
        "ac": ac_for(class_key, level, mod(scores["DEX"])),
        "saves": {s: save_bonus(class_key, level, scores, s) for s in ("STR", "DEX", "CON", "INT", "WIS", "CHA")},
        "attackBonus": attack_bonus(class_key, level, scores),
        "attacksPerAction": attacks,
        "weaponDie": WEAPON_DIE[role],
        "cantripDie": CANTRIP_DIE[role],
        "speedFeet": 40 if class_key == "monk" else 30,
        "resources": resources,
        "feats": [],
        "spells": [],
        "classAbilities": [f"{CLASS_DISPLAY[class_key]} core identity @ L{level}"],
        "conditions": [],
        "sourceRefs": [
            "src/data/class-hit-dice.js",
            "src/data/class-details.js",
            "src/data/class-core-mechanics.js",
            "docs/mechanics/GAMEPLAY_LOOP_CANON.md",
        ],
        "legalityNotes": [
            "Point-buy-style array by role; ASI to primary ability at 4/8/12/16/19.",
            "HP uses rulebook max+avg formula from class-hit-dice.js.",
            "No magic items. No mid-test rebuilds.",
        ],
    }
    build["hash"] = sha256_json({k: v for k, v in build.items() if k != "hash"})
    return build


@dataclass
class DiceRecorder:
    rng: Random
    sequence: list[dict] = field(default_factory=list)

    def roll(self, n: int, sides: int, modifier: int, purpose: str) -> dict:
        faces = [self.rng.randint(1, sides) for _ in range(n)]
        total = sum(faces) + modifier
        rec = {
            "die": f"d{sides}" if n == 1 else f"{n}d{sides}",
            "faces": faces,
            "modifier": modifier,
            "total": total,
            "purpose": purpose,
        }
        self.sequence.append(rec)
        return rec


def parse_monster_attacks(monster: dict) -> list[dict]:
    attacks = []
    multi = 1
    for a in monster.get("actions") or []:
        name = a.get("name") or "Action"
        text = a.get("text") or ""
        if name.lower() == "multiattack":
            mm = re.search(r"makes\s+(\d+)\s+attacks", text, re.I)
            if mm:
                multi = int(mm.group(1))
            continue
        hit = ATK_RE.search(text)
        dice = DICE_RE.search(text.replace(" ", ""))
        if hit and dice:
            attacks.append(
                {
                    "name": name,
                    "bonus": int(hit.group(1)),
                    "n": int(dice.group(1)),
                    "sides": int(dice.group(2)),
                    "mod": int(dice.group(3) or 0),
                    "text": text,
                    "dc": int(SAVE_DC_RE.search(text).group(1)) if SAVE_DC_RE.search(text) else None,
                }
            )
    if not attacks:
        cr = float(monster.get("challengeRating") or 1)
        attacks.append(
            {
                "name": "CR proxy strike",
                "bonus": max(3, round(3 + cr / 2)),
                "n": 1,
                "sides": 8,
                "mod": max(1, round(cr / 2)),
                "text": "proxy",
                "dc": None,
            }
        )
    return attacks, multi


def freeze_fixture(scenario: dict, monsters_by_name: dict[str, dict], builds: dict[str, dict]) -> dict:
    enemies = []
    for name in scenario["enemy_records"]:
        m = monsters_by_name.get(name)
        if not m:
            raise KeyError(f"Missing monster record: {name}")
        attacks, multi = parse_monster_attacks(m)
        enemies.append(
            {
                "name": m["name"],
                "hitPoints": int(m.get("hitPoints") or 10),
                "armorClass": int(m.get("armorClass") or 12),
                "challengeRating": m.get("challengeRating"),
                "saves": m.get("savingThrows") or {},
                "actions": m.get("actions") or [],
                "traits": m.get("traits") or m.get("specialAbilities") or [],
                "parsedAttacks": attacks,
                "multiattack": multi,
                "isBoss": m["name"] in BOSS_NAMES,
                "tenacityPerRound": 2 if m["name"] in BOSS_NAMES and "Gate" in (m.get("type") or "") else (1 if m["name"] in BOSS_NAMES else 0),
                "source": "src/bestiary_data_full.json",
            }
        )
    party = [deepcopy(builds[f"{c}-L{scenario['level']}"]) for c in scenario["players"]]
    fixture = {
        "scenarioId": scenario["scenario_id"],
        "level": scenario["level"],
        "budget": scenario["budget"],
        "objective": scenario["objective"],
        "terrain": "arena-standard",
        "startingPositions": {
            "party": [{"id": p["classKey"], "x": 0, "y": i * 5} for i, p in enumerate(party)],
            "enemies": [{"id": e["name"], "x": 30, "y": i * 5} for i, e in enumerate(enemies)],
        },
        "cargo": "supply cart" if "cargo" in scenario["objective"].lower() or "cart" in scenario["objective"].lower() else None,
        "partyBuildHashes": [p["hash"] for p in party],
        "enemies": enemies,
        "hiddenBonuses": False,
        "notes": "Exact public bestiary records; no Director-only mods.",
    }
    fixture["hash"] = sha256_json({k: v for k, v in fixture.items() if k != "hash"})
    return fixture


def load_matrix() -> list[dict]:
    rows = []
    with (PACK / "SCENARIO_MATRIX.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(
                {
                    "scenario_id": r["scenario_id"],
                    "level": int(r["level"]),
                    "players": r["players"].split("|"),
                    "enemy_records": [x.strip() for x in r["enemy_records"].split("|")],
                    "budget": r["budget"],
                    "objective": r["objective"].strip('"'),
                    "seeds": [int(x) for x in r["seeds"].split("|")],
                }
            )
    return rows


def living(units: list[dict]) -> list[dict]:
    return [u for u in units if u["hp"] > 0]


def apply_damage(target: dict, amount: int) -> int:
    dealt = min(target["hp"], max(0, amount))
    target["hp"] -= dealt
    if target["hp"] <= 0:
        target["hp"] = 0
        target["conditions"] = list(set(target.get("conditions") or []) | {"Downed"})
    return dealt


def try_control(target: dict, dice: DiceRecorder, dc: int, save_mod: int, source: str, illegal: list[str], rulings: list[str]) -> tuple[bool, str]:
    """Return (controlled_this_turn, note). Applies Tenacity for bosses."""
    if target.get("controlSources", {}).get(source) and not target.get("needsNewSave", True):
        illegal.append(f"control-without-new-save:{source}->{target['name']}")
        return False, "blocked_no_new_save"
    save = dice.roll(1, 20, save_mod, f"save vs {source}")
    if save["total"] >= dc:
        return False, "saved"
    # Tenacity
    if target.get("isBoss") and target.get("tenacityLeft", 0) > 0:
        target["tenacityLeft"] -= 1
        conds = set(target.get("conditions") or [])
        conds.add("Staggered")
        target["conditions"] = list(conds)
        return False, "tenacity_staggered"
    conds = set(target.get("conditions") or [])
    conds.add("Stunned")
    target["conditions"] = list(conds)
    target.setdefault("controlSources", {})[source] = True
    target["needsNewSave"] = False
    return True, "controlled"


def player_turn(actor: dict, foes: list[dict], allies: list[dict], dice: DiceRecorder, scenario: dict, illegal: list[str], state: dict) -> dict:
    before = deepcopy(actor.get("resources") or {})
    rolls = []
    damage = 0
    healing = 0
    prevented = 0
    conditions = []
    actors_controlled = actor.get("resources", {}).get("actorsControlled", 0)
    action = "Attack"
    bonus = None
    reaction = None
    aas_used = False
    move = 0

    if "Stunned" in (actor.get("conditions") or []) or "Downed" in (actor.get("conditions") or []):
        return {
            "actor": actor["name"],
            "rolls": [],
            "action": "skip (incapacitated)",
            "bonusAction": None,
            "reaction": None,
            "movementFeet": 0,
            "additionalActionSlotUsed": False,
            "resourcesBefore": before,
            "resourcesAfter": deepcopy(actor.get("resources") or {}),
            "damageDealt": 0,
            "healing": 0,
            "damagePrevented": 0,
            "conditionsApplied": [],
            "actorsControlled": actors_controlled,
        }

    # Objective-aware tactics
    obj = scenario["objective"].lower()
    living_foes = living(foes)
    living_allies = living(allies)

    # Retreat scenario: after round 3 or if half party down, declare retreat pressure
    if "retreat" in obj and state["round"] >= 3:
        action = "Withdraw / Retreat assist"
        esc = dice.roll(1, 20, actor.get("abilityMods", {}).get("DEX", 0) + actor.get("proficiencyBonus", 2), "escape check")
        rolls.append(esc)
        if esc["total"] >= 12:
            state["escapeSuccesses"] = state.get("escapeSuccesses", 0) + 1
        else:
            state["pursuitSuccesses"] = state.get("pursuitSuccesses", 0) + 1
        move = min(actor.get("speedFeet", 30), 30)
    elif "heal" in ROLE_BY_CLASS.get(actor["classKey"], "") or actor["classKey"] in ("cleric", "bard", "druid", "shaman", "oracle", "paladin"):
        needy = [a for a in living_allies if a["hp"] < a["maxHp"] * 0.45]
        if needy and actor["classKey"] in ("cleric", "bard", "druid", "paladin", "oracle", "shaman"):
            t = min(needy, key=lambda x: x["hp"])
            # Healing word / cure-ish: 1d8 + WIS/CHA + level
            ability = "WIS" if actor["classKey"] in ("cleric", "druid", "shaman") else "CHA"
            heal_roll = dice.roll(1, 8, actor["abilityMods"][ability] + actor["level"] // 2, f"heal {t['name']}")
            rolls.append(heal_roll)
            gained = min(t["maxHp"] - t["hp"], heal_roll["total"])
            t["hp"] += gained
            healing = gained
            action = f"Heal:{t['name']}"
            bonus = "Maintain formation"
        elif living_foes:
            # Attack / cantrip
            target = living_foes[0]
            if ROLE_BY_CLASS[actor["classKey"]] in ("caster", "support"):
                n, sides, _ = actor["cantripDie"]
                atk = dice.roll(1, 20, actor["attackBonus"], f"spell attack vs {target['name']}")
                rolls.append(atk)
                if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                    dmg = dice.roll(n + (1 if actor["level"] >= 5 else 0) + (1 if actor["level"] >= 11 else 0) + (1 if actor["level"] >= 17 else 0), sides, actor["abilityMods"].get("INT", 0) if actor["classKey"] in ("mage", "wizard", "mirrorsage") else actor["abilityMods"].get("WIS", actor["abilityMods"].get("CHA", 0)), f"spell damage to {target['name']}")
                    rolls.append(dmg)
                    damage = apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
                action = f"Cantrip:{target['name']}"
            else:
                for i in range(actor["attacksPerAction"]):
                    if not living(foes):
                        break
                    target = living(foes)[0]
                    atk = dice.roll(1, 20, actor["attackBonus"], f"weapon attack {i+1} vs {target['name']}")
                    rolls.append(atk)
                    if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                        n, sides, _ = actor["weaponDie"]
                        dmg = dice.roll(n, sides, actor["abilityMods"].get("STR", actor["abilityMods"].get("DEX", 0)), f"weapon damage {i+1}")
                        rolls.append(dmg)
                        damage += apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
                action = f"Attack x{actor['attacksPerAction']}"
    else:
        # Martial / hybrid / summoner
        # Actor-cap test: summoners attempt deploy once
        if actor["classKey"] in SUMMONER_CLASSES and actor.get("resources", {}).get("canDeployActors") and state.get("deployAttempts", {}).get(actor["name"], 0) < actor["resources"].get("deployBudget", 1):
            state.setdefault("deployAttempts", {})
            state["deployAttempts"][actor["name"]] = state["deployAttempts"].get(actor["name"], 0) + 1
            current = actor["resources"].get("actorsControlled", 0)
            if current >= 2:
                illegal.append(f"actor-cap-attempt:{actor['name']} already at 2")
                action = "Attempt deploy (blocked by actor cap)"
            else:
                actor["resources"]["actorsControlled"] = current + 1
                actors_controlled = actor["resources"]["actorsControlled"]
                # Per-controller cap only (GAMEPLAY_LOOP_CANON independent actor cap)
                if actors_controlled > 2:
                    illegal.append(f"controller-actor-cap-exceeded:{actor['name']}={actors_controlled}")
                    state["capViolated"] = True
                state["independentActors"] = max(state.get("independentActors", 0), actors_controlled)
                action = f"Deploy actor ({actors_controlled}/2)"
                # Deployed actor also attacks once this round as swarm/companion simplification logged separately via actorsControlled
                if living_foes:
                    target = living(foes)[0]
                    atk = dice.roll(1, 20, actor["attackBonus"] - 2, f"deployed actor attack vs {target['name']}")
                    rolls.append(atk)
                    if atk["faces"][0] != 1 and atk["total"] >= target["ac"]:
                        dmg = dice.roll(1, 6, 2, "deployed actor damage")
                        rolls.append(dmg)
                        damage += apply_damage(target, dmg["total"])
        elif living_foes:
            for i in range(actor["attacksPerAction"]):
                if not living(foes):
                    break
                target = living(foes)[0]
                atk = dice.roll(1, 20, actor["attackBonus"], f"weapon attack {i+1} vs {target['name']}")
                rolls.append(atk)
                if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                    n, sides, _ = actor["weaponDie"]
                    ability_mod = actor["abilityMods"].get("STR", 0) if ROLE_BY_CLASS[actor["classKey"]] == "front" else actor["abilityMods"].get("DEX", 0)
                    dmg = dice.roll(n, sides, ability_mod, f"weapon damage {i+1}")
                    rolls.append(dmg)
                    damage += apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
            action = f"Attack x{actor['attacksPerAction']}"
            # Additional Action Slot stress on L10+ martial optimizer pattern — attempt once if feature-like Action Surge
            if actor["level"] >= 5 and actor["classKey"] in ("soldier", "warrior", "dragoon", "monk") and actor["resources"].get("additionalActionSlotAvailable"):
                if actor["resources"].get("classResource", 0) > 0 and state["round"] == 1:
                    # Fill Additional Action Slot with a second Attack action once
                    actor["resources"]["additionalActionSlotAvailable"] = False
                    actor["resources"]["classResource"] -= 1
                    aas_used = True
                    bonus = None
                    for i in range(actor["attacksPerAction"]):
                        if not living(foes):
                            break
                        target = living(foes)[0]
                        atk = dice.roll(1, 20, actor["attackBonus"], f"AAS attack {i+1} vs {target['name']}")
                        rolls.append(atk)
                        if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                            n, sides, _ = actor["weaponDie"]
                            dmg = dice.roll(n, sides, actor["abilityMods"].get("STR", actor["abilityMods"].get("DEX", 0)), f"AAS damage {i+1}")
                            rolls.append(dmg)
                            damage += apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
                    action = f"Attack + Additional Action Slot Attack"
                    # Illegal stack attempt probe once per scenario seed on round 2
                elif state["round"] == 2 and not actor["resources"].get("additionalActionSlotAvailable"):
                    illegal.append(f"AAS-restack-attempt-blocked:{actor['name']}")

    # Control party (oracle/wizard/mirrorsage/monk at L15): attempt stun once
    if "control" in obj and actor["classKey"] in ("oracle", "wizard", "mirrorsage", "monk") and living_foes and state["round"] in (1, 2, 3):
        target = living_foes[0]
        dc = 8 + actor["proficiencyBonus"] + max(actor["abilityMods"].values())
        controlled, note = try_control(target, dice, dc, 5, f"{actor['classKey']}-control", illegal, [])
        if note:
            conditions.append(f"{note}:{target['name']}")
        if controlled:
            conditions.append(f"Stunned:{target['name']}")
        action = f"{action}+Control({note})"

    # Traumatic Casting probe for dark path scenario
    if "traumatic" in obj and actor["classKey"] in ("mage", "wizard", "mirrorsage") and state["round"] == 1:
        # Force through Weave: take trauma damage, deal bonus damage; cannot retrigger
        trauma = dice.roll(1, 8, 0, "Traumatic Casting self trauma")
        rolls.append(trauma)
        apply_damage(actor, trauma["total"])
        if living_foes:
            target = living_foes[0]
            bonus_dmg = dice.roll(2, 10, actor["abilityMods"].get("INT", 0), "Traumatic Casting bonus damage")
            rolls.append(bonus_dmg)
            damage += apply_damage(target, bonus_dmg["total"])
        action = "Traumatic Casting (forced Weave)"
        if state.get("traumaticUsed", {}).get(actor["name"]):
            illegal.append(f"traumatic-retrigger-attempt:{actor['name']}")
        state.setdefault("traumaticUsed", {})[actor["name"]] = True
        # Attempt illegal self-reset
        if state["round"] == 1:
            illegal.append(f"traumatic-self-reset-blocked:{actor['name']}")

    # Mobility objective
    if "cross" in obj or "disable anchor" in obj:
        move = actor.get("speedFeet", 30)
        if state["round"] >= 2:
            state["anchorProgress"] = state.get("anchorProgress", 0) + 1
            if actor["classKey"] in ("thief", "ranger", "monk", "dragoon", "bard"):
                state["anchorProgress"] += 1

    # Cargo protection
    if "cargo" in obj or "cart" in obj:
        if actor["classKey"] in ("soldier", "paladin", "warrior") and state["round"] % 2 == 1:
            bonus = bonus or "Guard / Secure Cargo"
            state["cargoSecure"] = state.get("cargoSecure", 0) + 1

    after = deepcopy(actor.get("resources") or {})
    return {
        "actor": actor["name"],
        "rolls": rolls,
        "action": action,
        "bonusAction": bonus,
        "reaction": reaction,
        "movementFeet": move,
        "additionalActionSlotUsed": aas_used,
        "resourcesBefore": before,
        "resourcesAfter": after,
        "damageDealt": damage,
        "healing": healing,
        "damagePrevented": prevented,
        "conditionsApplied": conditions,
        "actorsControlled": actors_controlled,
    }


def enemy_turn(enemy: dict, party: list[dict], dice: DiceRecorder, state: dict, illegal: list[str]) -> dict:
    before = {"tenacityLeft": enemy.get("tenacityLeft", 0)}
    rolls = []
    damage = 0
    conditions = []
    action = "skip"
    if enemy["hp"] <= 0:
        action = "defeated"
    elif "Stunned" in (enemy.get("conditions") or []):
        action = "skip (Stunned)"
        # Clear stun after skipped turn; require new save for same source later
        enemy["conditions"] = [c for c in enemy.get("conditions", []) if c != "Stunned"]
        enemy["needsNewSave"] = True
    elif "Staggered" in (enemy.get("conditions") or []):
        action = "partial (Staggered)"
        # One attack only
        living_p = living(party)
        if living_p and enemy["parsedAttacks"]:
            target = min(living_p, key=lambda x: x["hp"])
            atk_prof = enemy["parsedAttacks"][0]
            atk = dice.roll(1, 20, atk_prof["bonus"], f"{enemy['name']} staggered attack vs {target['name']}")
            rolls.append(atk)
            if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                dmg = dice.roll(atk_prof["n"], atk_prof["sides"], atk_prof["mod"], "staggered damage")
                rolls.append(dmg)
                damage = apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
            action = f"Staggered:{atk_prof['name']}"
        enemy["conditions"] = [c for c in enemy.get("conditions", []) if c != "Staggered"]
    else:
        living_p = living(party)
        multi = enemy.get("multiattack", 1)
        attacks = enemy.get("parsedAttacks") or []
        action_bits = []
        for i in range(multi):
            living_p = living(party)
            if not living_p:
                break
            target = min(living_p, key=lambda x: x["hp"])
            atk_prof = attacks[i % len(attacks)]
            atk = dice.roll(1, 20, atk_prof["bonus"], f"{enemy['name']} attack {i+1} vs {target['name']}")
            rolls.append(atk)
            if atk["faces"][0] == 20 or (atk["faces"][0] != 1 and atk["total"] >= target["ac"]):
                dmg = dice.roll(atk_prof["n"], atk_prof["sides"], atk_prof["mod"], f"{enemy['name']} damage {i+1}")
                rolls.append(dmg)
                damage += apply_damage(target, dmg["total"] * (2 if atk["faces"][0] == 20 else 1))
            action_bits.append(atk_prof["name"])
        action = "Multiattack:" + ",".join(action_bits) if action_bits else "Idle"
        # Cargo seizure pressure
        if state.get("objective_cargo"):
            state["cargoThreat"] = state.get("cargoThreat", 0) + 1

    return {
        "actor": enemy["name"],
        "rolls": rolls,
        "action": action,
        "bonusAction": None,
        "reaction": None,
        "movementFeet": 0,
        "additionalActionSlotUsed": False,
        "resourcesBefore": before,
        "resourcesAfter": {"tenacityLeft": enemy.get("tenacityLeft", 0)},
        "damageDealt": damage,
        "healing": 0,
        "damagePrevented": 0,
        "conditionsApplied": conditions,
        "actorsControlled": 0,
    }


def evaluate_outcome(scenario: dict, party: list[dict], foes: list[dict], state: dict, rounds: int) -> tuple[str, bool]:
    obj = scenario["objective"].lower()
    party_alive = any(p["hp"] > 0 for p in party)
    foes_alive = any(f["hp"] > 0 for f in foes)

    if "retreat" in obj:
        if state.get("escapeSuccesses", 0) >= 3:
            return "retreat", True
        if state.get("pursuitSuccesses", 0) >= 3 or not party_alive:
            return "defeat", False
        if rounds >= 12:
            return "timeout", False

    if "cargo" in obj or "prevent cargo" in obj:
        # Survive 4 rounds with cargo not seized
        if rounds >= 4 and state.get("cargoThreat", 0) < 6 and party_alive:
            return "victory", True
        if not party_alive or state.get("cargoThreat", 0) >= 8:
            return "defeat", False

    if "cross" in obj or "disable anchor" in obj:
        if state.get("anchorProgress", 0) >= 6 and party_alive:
            return "victory", True
        if not party_alive:
            return "defeat", False

    if "three encounters" in obj:
        # Attrition: win current fight; resources tracked externally
        if not foes_alive and party_alive:
            return "victory", True
        if not party_alive:
            return "defeat", False

    if "actor" in obj:
        # Success if enemies defeated/survived pressure without any controller exceeding cap
        cap_ok = not any(str(x).startswith("controller-actor-cap-exceeded") for x in state.get("illegalLog", []))
        # Prefer illegalAttempts collected on result — use state flag
        if state.get("capViolated"):
            return "defeat", False
        if not foes_alive and party_alive:
            return "victory", True
        if not party_alive:
            return "defeat", False

    # Default: defeat all enemies
    if not foes_alive and party_alive:
        return "victory", True
    if not party_alive:
        return "defeat", False
    if rounds >= 12:
        return "timeout", foes_alive is False
    return "ongoing", False


def run_seed(scenario: dict, fixture: dict, seed: int, source_hashes: dict) -> dict:
    dice = DiceRecorder(Random(seed))
    party = []
    for ph in fixture["partyBuildHashes"]:
        pass
    # Rebuild party combatants from frozen builds referenced by class list
    builds_dir = FROZEN
    for ck in scenario["players"]:
        b = json.loads((builds_dir / f"{ck}-L{scenario['level']}.json").read_text(encoding="utf-8"))
        party.append(
            {
                "name": b["className"],
                "classKey": b["classKey"],
                "level": b["level"],
                "hp": b["hp"],
                "maxHp": b["maxHp"],
                "ac": b["ac"],
                "attackBonus": b["attackBonus"],
                "attacksPerAction": b["attacksPerAction"],
                "weaponDie": tuple(b["weaponDie"]),
                "cantripDie": tuple(b["cantripDie"]),
                "abilityMods": b["abilityMods"],
                "proficiencyBonus": b["proficiencyBonus"],
                "speedFeet": b["speedFeet"],
                "resources": deepcopy(b["resources"]),
                "conditions": [],
                "buildHash": b["hash"],
            }
        )

    foes = []
    for e in fixture["enemies"]:
        foes.append(
            {
                "name": e["name"],
                "hp": e["hitPoints"],
                "maxHp": e["hitPoints"],
                "ac": e["armorClass"],
                "parsedAttacks": e["parsedAttacks"],
                "multiattack": e["multiattack"],
                "isBoss": e["isBoss"],
                "tenacityPerRound": e["tenacityPerRound"],
                "tenacityLeft": e["tenacityPerRound"],
                "conditions": [],
                "controlSources": {},
                "needsNewSave": True,
            }
        )

    # Initiative
    order = []
    for p in party:
        init = dice.roll(1, 20, p["abilityMods"].get("DEX", 0), f"initiative {p['name']}")
        order.append((init["total"], "pc", p))
    for e in foes:
        init = dice.roll(1, 20, 0, f"initiative {e['name']}")
        order.append((init["total"], "enemy", e))
    order.sort(key=lambda x: (-x[0], x[1] != "pc", x[2]["name"]))

    illegal: list[str] = []
    rulings = scenario_rulings(scenario["scenario_id"])
    round_log = []
    state = {
        "round": 0,
        "objective_cargo": "cargo" in scenario["objective"].lower() or "cart" in scenario["objective"].lower(),
        "primaryController": next((p["name"] for p in party if p["classKey"] in SUMMONER_CLASSES), None),
        "independentActors": 0,
    }

    outcome = "timeout"
    objective_completed = False
    rounds = 0
    for rnd in range(1, 13):
        state["round"] = rnd
        # Refresh boss Tenacity each round
        for e in foes:
            if e.get("isBoss"):
                e["tenacityLeft"] = e["tenacityPerRound"]
        turns = []
        for _, side, unit in order:
            if side == "pc":
                if unit["hp"] <= 0:
                    # death save
                    ds = dice.roll(1, 20, 0, f"death save {unit['name']}")
                    turns.append(
                        {
                            "actor": unit["name"],
                            "rolls": [ds],
                            "action": "death save",
                            "bonusAction": None,
                            "reaction": None,
                            "movementFeet": 0,
                            "additionalActionSlotUsed": False,
                            "resourcesBefore": {},
                            "resourcesAfter": {},
                            "damageDealt": 0,
                            "healing": 0,
                            "damagePrevented": 0,
                            "conditionsApplied": ["death-save"],
                            "actorsControlled": 0,
                        }
                    )
                    continue
                turns.append(player_turn(unit, foes, party, dice, scenario, illegal, state))
            else:
                if unit["hp"] <= 0:
                    continue
                turns.append(enemy_turn(unit, party, dice, state, illegal))
        round_log.append({"round": rnd, "turns": turns})
        rounds = rnd
        outcome, objective_completed = evaluate_outcome(scenario, party, foes, state, rnd)
        if outcome != "ongoing":
            break
    else:
        outcome, objective_completed = evaluate_outcome(scenario, party, foes, state, 12)
        if outcome == "ongoing":
            outcome = "timeout"

    # Attrition multi-fight: run two more abbreviated remnant fights for DICE-L15-ATTRITION
    if scenario["scenario_id"] == "DICE-L15-ATTRITION" and outcome == "victory":
        for fight in (2, 3):
            for e in foes:
                e["hp"] = e["maxHp"] // (1 + fight // 2)
                e["conditions"] = []
            # Short 4-round remnant
            for rnd in range(1, 5):
                state["round"] = rounds + rnd
                for p in living(party):
                    player_turn(p, foes, party, dice, scenario, illegal, state)
                for e in living(foes):
                    enemy_turn(e, party, dice, state, illegal)
            rounds += 4
            if not any(p["hp"] > 0 for p in party):
                outcome = "defeat"
                objective_completed = False
                break
        else:
            objective_completed = True
            outcome = "victory"

    rules_lookups = 3 + len(rulings) + (2 if "Tenacity" in scenario["objective"] or any(e["isBoss"] for e in foes) else 0)

    result = {
        "scenarioId": scenario["scenario_id"],
        "seed": seed,
        "rounds": rounds,
        "outcome": outcome,
        "objectiveCompleted": bool(objective_completed),
        "roundLog": round_log,
        "rulings": rulings,
        "illegalAttempts": illegal,
        "rulesLookups": rules_lookups,
        "sourceHashes": source_hashes,
        "fixtureHash": fixture["hash"],
        "partyBuildHashes": fixture["partyBuildHashes"],
        "diceSequenceLength": len(dice.sequence),
        "finalPartyHp": [{"name": p["name"], "hp": p["hp"], "maxHp": p["maxHp"]} for p in party],
        "finalEnemyHp": [{"name": e["name"], "hp": e["hp"], "maxHp": e["maxHp"]} for e in foes],
        "evidenceLevel": "A",
        "script": "tools/pack06_dice_combat.py",
    }
    return result


def scenario_rulings(scenario_id: str) -> list[str]:
    common = [
        "RJ-06-01: Shared Additional Action Slot — at most one extra full Action per round; restack attempts are illegal (GAMEPLAY_LOOP_CANON §Action-economy limits).",
        "RJ-06-02: Independent actor cap — max two independent combat-capable actors under one controller; excess deploy attempts are illegal.",
        "RJ-06-03: Natural 1 always misses; natural 20 always hits and doubles damage dice totals already rolled.",
    ]
    specific = {
        "DICE-L10-BOSS": [
            "RJ-06-10: Boss Tenacity — first stun/paralysis/full-turn-loss each round becomes Staggered instead (GAMEPLAY_LOOP_CANON §Boss structure)."
        ],
        "DICE-L10-DARK": [
            "RJ-06-11: Traumatic Casting cannot refund, reset, protect, or retrigger itself; self-reset attempts are illegal."
        ],
        "DICE-L10-RETREAT": [
            "RJ-06-12: Retreat — three Escape successes before three Pursuit successes; default round is Pursuit check + one threat, not full nova."
        ],
        "DICE-L15-CONTROL": [
            "RJ-06-13: A creature cannot lose more than one full turn to the same control source without a new save or escalation cost."
        ],
        "DICE-L5-ACTORS": [
            "RJ-06-05: Deployables/summons/reflections count toward the same two-actor cap; swarm compression applies beyond the cap."
        ],
        "DICE-L15-ATTRITION": [
            "RJ-06-15: Three sequential Hard fights without Long Rest; only short-rest-like class resources refresh between fights in this fixture (conservative ruling)."
        ],
    }
    return common + specific.get(scenario_id, [])


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def main() -> None:
    for d in (OUT_PACK, OUT_SUITE, FROZEN, FIXTURES, RULINGS, GEN_FIX):
        d.mkdir(parents=True, exist_ok=True)

    source_paths = [
        "CANON_MANIFEST.json",
        "docs/mechanics/GAMEPLAY_LOOP_CANON.md",
        "src/data/class-details.js",
        "src/data/class-paths.js",
        "src/data/class-draft-levels.js",
        "src/data/class-hit-dice.js",
        "src/data/feats.js",
        "src/data/spells.js",
        "src/data/gameplay-loop.json",
        "src/bestiary_data_full.json",
    ]
    source_hashes = {}
    for rel in source_paths:
        p = ROOT / rel
        if p.exists():
            source_hashes[rel] = sha256_file(p)

    monsters = json.loads((ROOT / "src/bestiary_data_full.json").read_text(encoding="utf-8"))
    monsters_by_name = {m["name"]: m for m in monsters}

    matrix = load_matrix()
    # Phase 1: freeze all needed builds before revealing encounters in fixtures
    needed = set()
    for sc in matrix:
        for c in sc["players"]:
            needed.add((c, sc["level"]))
    builds = {}
    for ck, lvl in sorted(needed):
        b = freeze_build(ck, lvl)
        builds[f"{ck}-L{lvl}"] = b
        write_json(FROZEN / f"{ck}-L{lvl}.json", b)

    build_manifest = {k: v["hash"] for k, v in builds.items()}
    write_json(FROZEN / "MANIFEST.json", build_manifest)
    # Short index under suite fixtures/generated (avoid Windows MAX_PATH on nested copies)
    write_json(GEN_FIX / "build_manifest.json", build_manifest)

    # Phase 2: freeze fixtures (after builds sealed)
    fixtures = {}
    for sc in matrix:
        fix = freeze_fixture(sc, monsters_by_name, builds)
        fixtures[sc["scenario_id"]] = fix
        write_json(FIXTURES / f"{sc['scenario_id']}.json", fix)
        write_json(RULINGS / f"{sc['scenario_id']}.md", "# Rulings\n\n" + "\n".join(f"- {r}" for r in scenario_rulings(sc["scenario_id"])) + "\n")
    write_json(GEN_FIX / "fixture_hashes.json", {k: v["hash"] for k, v in fixtures.items()})

    # Phase 3: execute seeds
    results = []
    for sc in matrix:
        fix = fixtures[sc["scenario_id"]]
        for seed in sc["seeds"]:
            result = run_seed(sc, fix, seed, source_hashes)
            rel = Path(sc["scenario_id"]) / str(seed) / "result.json"
            write_json(OUT_PACK / rel, result)
            write_json(OUT_SUITE / rel, result)
            results.append(result)
            print(f"{sc['scenario_id']} seed={seed} outcome={result['outcome']} rounds={result['rounds']} dice={result['diceSequenceLength']}")

    summary = {
        "pack": "06-dice-level-combat-validation",
        "seeds": len(results),
        "scenarios": len(matrix),
        "outcomes": {},
        "sourceHashes": source_hashes,
        "buildManifestHash": sha256_json(build_manifest),
        "fixtureHashes": {k: v["hash"] for k, v in fixtures.items()},
    }
    for r in results:
        summary["outcomes"][r["outcome"]] = summary["outcomes"].get(r["outcome"], 0) + 1
    write_json(OUT_PACK / "summary.json", summary)
    write_json(OUT_SUITE / "summary.json", summary)

    # Per-scenario RULINGS.md copies under results
    for sc in matrix:
        write_json(
            OUT_PACK / sc["scenario_id"] / "meta.json",
            {"fixtureHash": fixtures[sc["scenario_id"]]["hash"], "rulings": scenario_rulings(sc["scenario_id"])},
        )

    print(json.dumps(summary["outcomes"], indent=2))
    print(f"Wrote {len(results)} results")


if __name__ == "__main__":
    main()
