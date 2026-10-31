from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SRC270 = BASE / "rank9_castingcost5_current_source_270_prepared"
OLD = BASE / "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip"
OUT = BASE / "rank9_castingcost5_return272_prepared"
CASE_SOURCE = OLD
TARGET = "unholy-ascendance"
WIZARD_PROFILE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_194/ACTOR_PROFILES.json"
WIZARD_CARD_FILE = ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json"
CLERIC_CARD_FILE = ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json"
CATALOG_FILE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
FORM_PROFILE_FILE = ROOT / "DescentReviewChanges/ReviewBible/data/playtest/spell_form_profiles.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_binding(path: Path, rel: str | None = None) -> dict:
    raw = path.read_bytes()
    import zlib
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def source_refs(*extra: str) -> list[str]:
    base = [
        "current-source:DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json",
        "current-source:CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json#/sourceBindings",
        "PROCEDURES.json#unholy-ascendance",
        "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
        "HEALING_DEATH_PLAYTEST.md#L37-L46",
        "CORE_RESOLUTION_PLAYTEST.md#L35-L60",
        "COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md#recipient-lifecycles-for-qualifying-Null-damage",
        "TRANSFORMATION_SPELL_PLAYTEST.md#Polymorph-and-Antimagic-suppression",
        "cleric.json#/cards/12",
        "cleric.json#/cards/57",
        "catalog.json#/spells/630/operational",  # vampiric-touch
        "catalog.json#/spells/735/operational",  # polymorph
        "spell_form_profiles.json#/profiles/spellform.humanoid",
        "wizard.json#/cards/19",  # acquired Arch Dispel
        "wizard.json#/cards/21",  # acquired Arcane Sight
        "ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/2/choices/1",
        "ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/8/choices/0",
        "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
        "SPELL_INTEGRATION_RULES.md#Resolve-a-cast-at-the-table",
    ]
    return base + list(extra)


def wizard_profile() -> dict:
    return read_json(WIZARD_PROFILE)["Wizard20"]


def configure_conditional_learning(actor: dict) -> None:
    """Build a fixed-count Wizard20 conditional selection ledger for these cases."""
    profile = wizard_profile()
    learning = copy.deepcopy(profile["ordinaryLearning"])
    replacements = [
        (5, "alignment-prediction", "vampiric-touch"),
        (5, "alignment-revelation", "dispel-magic"),
        (8, "alignment-lock", "polymorph"),
        (19, "bestow-curse", "power-word-kill"),
    ]
    by_level = {row["level"]: row for row in learning}
    catalog = read_json(CATALOG_FILE)["spells"]
    by_id = {spell["id"]: spell for spell in catalog}
    ledger = []
    for level, old_id, new_id in replacements:
        row = by_level[level]
        assert old_id in row["selected"], (level, old_id, row["selected"])
        access = by_id[new_id]["classAccess"]["Wizard"]
        assert access["minimumClassLevel"] <= level, (new_id, level, access)
        row["selected"][row["selected"].index(old_id)] = new_id
        ledger.append({"level": level, "spellId": new_id, "replaces": old_id,
                       "rank": access["rank"], "source": "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
                       "sameSelectionCount": True, "conditionalFixture": True})
        if old_id in actor["prepared"]:
            actor["prepared"].remove(old_id)
        if new_id not in actor["prepared"]:
            actor["prepared"].append(new_id)
        actor["everKnown"] = [x for x in actor["everKnown"] if x.get("spellId") != old_id]
        if not any(x.get("spellId") == new_id for x in actor["everKnown"]):
            actor["everKnown"].append({"kind": "conditional-fixed-count-level-learning", "spellId": new_id,
                "level": level, "replaces": old_id,
                "source": "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning"})
    actor["ordinaryLearning"] = learning
    actor["conditionalLearningLedger"] = ledger
    actor["acquiredWizardFeatures"] = [
        {"id": choice["id"], "level": row["level"], "source": f"ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/{row['level']-1}/choices"}
        for row in profile["acquisitionLedger"] for choice in row.get("choices", [])
        if choice.get("id") in {"wizard.arch.arcane-sight", "wizard.arch.dispel-magic", "wizard.arch.spell-efficiency"}
    ]
    actor["classFeatureState"] = {"spellEfficiency": {"selected": True, "usesAvailable": True,
        "source": "ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/18/choices/0"}}


def advance_calendar(state: dict, at: float) -> dict:
    """Advance every actor's six-second regular-turn calendar through an event time."""
    advanced = {}
    for actor_id, actor in state["actors"].items():
        interval = actor.get("regularTurnSeconds") or 6.0
        actor["regularTurnSeconds"] = interval
        nxt = actor.get("nextRegularStart")
        if nxt is None:
            continue
        nxt = float(nxt)
        first = None
        last = None
        count = 0
        while nxt <= at + 1e-9:
            if first is None:
                first = nxt
            last = nxt
            count += 1
            nxt = round(nxt + interval, 9)
        if not count:
            continue
        life_state = actor.get("lifecycle") or {}
        down = (actor.get("life") == "Dead" or life_state.get("state") in {"Dying0", "Stable0", "Dead"}
                or actor.get("conditions", {}).get("Unconscious", False))
        # A required save is never silently crossed by a compressed calendar run.
        marker = life_state.get("nextDeathSaveAt")
        if marker is not None and first is not None and marker <= last + 1e-9:
            history = life_state.get("history", [])
            represented = any(abs(float(x.get("at", -1)) - float(marker)) < 1e-9
                              and "death-save" in str(x.get("kind", "")) for x in history)
            if not represented:
                raise ValueError(f"{actor_id} required death save at {marker} crossed in calendar advancement to {at}")
        actor["lastRegularStart"] = last
        actor["nextRegularStart"] = nxt
        if down:
            actor["action"] = actor["bonusAction"] = actor["reaction"] = 0
        else:
            actor["action"] = actor["bonusAction"] = actor["reaction"] = 1
        cal = actor.setdefault("turnCalendar", {"intervalSeconds": interval, "runs": [], "regularStarts": 0})
        cal["intervalSeconds"] = interval
        cal["regularStarts"] += count
        run = {"firstStart": first, "lastStart": last, "lastEnd": round(last + interval, 9),
               "count": count, "intervalSeconds": interval}
        if cal["runs"] and abs(cal["runs"][-1]["lastStart"] + interval - first) < 1e-9:
            prev = cal["runs"][-1]
            prev["lastStart"] = last
            prev["lastEnd"] = run["lastEnd"]
            prev["count"] += count
        else:
            cal["runs"].append(run)
        cal["nextRegularStart"] = nxt
        cal["lastRegularStart"] = last
        cal["lastRegularEnd"] = run["lastEnd"]
        cal["budgetAtEndpoint"] = {"action": actor["action"], "bonusAction": actor["bonusAction"], "reaction": actor["reaction"]}
        efficiency=(actor.get("classFeatureState") or {}).get("spellEfficiency")
        if efficiency and efficiency.get("pendingMatrix") and efficiency.get("expiresAfterRegularTurnEnd") is not None \
                and float(efficiency["expiresAfterRegularTurnEnd"]) <= at + 1e-9:
            efficiency["expiredAt"] = float(efficiency["expiresAfterRegularTurnEnd"])
            efficiency["expiredBeforeEventAt"] = at
            efficiency["pendingMatrix"] = None
            efficiency["usesAvailable"] = True
        advanced[actor_id] = {"firstStart": first, "lastStart": last, "lastEnd": run["lastEnd"],
                              "count": count, "nextRegularStart": nxt, "incapacitated": down}
    return advanced


def rebuild_cast_histories(state: dict) -> None:
    """Reconcile committed spell casts, Wizard first-matrix protection, Refrain and actions."""
    for actor_id, actor in state["actors"].items():
        entries = [x for x in actor.get("resourceHistory", [])
                   if x.get("spellId") and isinstance(x.get("rank"), (int, float)) and x.get("at") is not None]
        entries.sort(key=lambda x: float(x["at"]))
        casts = []
        seen = set()
        last = None
        refrain = 0
        dissonance = 0
        class_name = actor.get("class")
        for row in entries:
            spell_id = row["spellId"]
            rank = int(row["rank"])
            repeated = spell_id in seen
            same_as_previous = spell_id == last
            refrain_delta = 1 if same_as_previous else 0
            if class_name == "Wizard" and not repeated:
                base = 0  # protected first cast of each prepared Wizard matrix
            else:
                base = 0 if rank == 0 else (1 if rank <= 5 else 2)
            refrain = min(3, refrain + refrain_delta) if same_as_previous else 0
            dissonance += base
            casts.append({"spellId": spell_id, "rank": rank, "at": row["at"],
                "rpPaid": row.get("rpPaid"), "ordinaryBaseDissonance": base,
                "protectedFirstMatrix": class_name == "Wizard" and not repeated,
                "refrainDelta": refrain_delta, "refrainAfter": refrain,
                "sameNameAsPrevious": same_as_previous,
                "spellEfficiencyApplied": bool(class_name == "Wizard" and row.get("spellEfficiencyApplied")),
                "sourceHistoryRef": row.get("source", row.get("spellId"))})
            seen.add(spell_id)
            last = spell_id
        actor["spellHistory"] = {"casts": casts, "lastMatrix": last, "refrain": refrain,
                                 "dissonance": dissonance, "distinctMatricesCast": len(seen)}
        actor["dissonance"] = dissonance
        actor["refrain"] = refrain
        actor.setdefault("interruptionHistory", [])


def event(state: dict, case_id: str, index: int, kind: str, at: float, detail: dict,
          refs: list[str], mutate) -> tuple[dict, dict]:
    rebuild_cast_histories(state)
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    calendar = advance_calendar(after, at)
    mutate(after)
    rebuild_cast_histories(after)
    after["time"] = at
    detail = copy.deepcopy(detail)
    detail["automaticTurnCalendarAdvancement"] = calendar
    ev = {"id": f"{case_id}:{index}", "kind": kind, "time": at, "detail": detail,
          "sourceRefs": refs, "before": before, "after": after,
          "beforeSHA256": sha(before), "afterSHA256": sha(after),
          "forward": [{"op": "test", "path": "", "value": before},
                      {"op": "replace", "path": "", "value": after}],
          "inverse": [{"op": "test", "path": "", "value": after},
                      {"op": "replace", "path": "", "value": before}]}
    return ev, after


def base_state(a_hp: int = 100, *, a_rp: int = 80, t_rp: int = 80,
               a_pos=(9, 0, 0), t_pos=(0, 0, 0), add_cleric: bool = False) -> dict:
    with zipfile.ZipFile(OLD) as z:
        source = json.loads(z.read("cases/01.json"))
        state = copy.deepcopy(source["initialState"])
    a, t = state["actors"]["A"], state["actors"]["T"]
    a.update({"hp": a_hp, "maxHP": 122, "tempHP": 0, "wounds": 1, "life": "Living",
              "position": list(a_pos), "rp": a_rp, "reviewStats": {"S": 4, "M": 5, "PB": 6,
              "INT": 20, "WIS": 16, "CON": 14, "spellAttack": 11, "profileSource": "ACTOR_PROFILES.json#/Wizard20"},
              "lifecycle": {"identity": "A-original-character-body", "state": "PositiveHP",
              "deathSaveFailures": 0, "deathSaveSuccesses": 0, "stableRecoveryDeadline": None}})
    t.update({"position": list(t_pos), "rp": t_rp, "reviewStats": {"S": 4, "M": 5, "PB": 6,
              "INT": 20, "WIS": 16, "CON": 14, "spellAttack": 11, "profileSource": "ACTOR_PROFILES.json#/Wizard20"},
              "nullVeil": None})
    for actor in (a, t):
        actor["regularTurnSeconds"] = 6.0
        actor["turnCalendar"] = {"intervalSeconds": 6.0, "runs": [], "regularStarts": 0}
        actor["interruptionHistory"] = []
        actor["spellHistory"] = {"casts": [], "lastMatrix": None, "refrain": 0, "dissonance": 0, "distinctMatricesCast": 0}
        configure_conditional_learning(actor)
    state["objects"].update({
        "T-focus": {"id": "T-focus", "kind": "spellcasting-focus", "owner": "T", "custody": "T", "accessible": True},
        "A-original-gear": {"owner": "A", "identity": ["A-focus", "A-robe", "A-book"], "custody": "A",
                            "gearHistory": [{"event": "initial", "holder": "A"}]},
        "NULL-FIELD-QUIET-WELL-1": {"fieldId": "NULL-FIELD-QUIET-WELL-1", "source": "CH07/currentModule/chambers/6/nullField",
                                     "boundary": "radius 7.5ft cylinder, z=0..10; main chamber only"},
    })
    state["constraints"]["currentSnapshot"] = "main; current source packet Return270"
    state["constraints"]["fixtureNature"] = "Conditional authored operands only; no campaign existence claim."
    if add_cleric:
        c = copy.deepcopy(t)
        for field in ["acquiredWizardFeatures","conditionalLearningLedger","ordinaryLearning","classFeatureState"]:
            c.pop(field,None)
        c.update({"id": "C", "profile": "CC194-C20-CULTIST-CONDITIONAL", "class": "Cleric", "level": 20,
                  "rp": 58, "maxRP": 58, "conviction": 7, "maxConviction": 7,
                  "position": [5, 0, 0], "prepared": ["healing-rite", "ritual-of-undeath"],
                   "reviewStats": {"S": 4, "M": 5, "PB": 6, "WIS": 20, "spellAttack": 11,
                                   "profileSource": "rank9planargates5_reviewed_200/ACTOR_PROFILES.json#/Cleric20; conditional level-16 Cultist selection"},
                  "everKnown": [{"kind": "conditional-selection", "source": "cleric.json#/cards/12", "spellId": "healing-rite"},
                                {"kind": "conditional-level-16-Cultist-selection", "source": "cleric.json#/cards/57", "spellId": "ritual-of-undeath"}],
                   "resourceHistory": [], "effects": {}, "conditions": {}, "deathSaves": {"failures": 0, "successes": 0},
                   "prepared": ["healing-rite", "ritual-of-undeath"],
                   "everKnown": [{"kind": "conditional-selection", "source": "cleric.json#/cards/12", "spellId": "healing-rite"},
                                 {"kind": "conditional-level-16-Cultist-selection", "source": "cleric.json#/cards/57", "spellId": "ritual-of-undeath"}],
                   "regularTurnSeconds": 6.0, "turnCalendar": {"intervalSeconds": 6.0, "runs": [], "regularStarts": 0},
                   "interruptionHistory": [], "spellHistory": {"casts": [], "lastMatrix": None, "refrain": 0, "dissonance": 0}})
        c["equipment"] = {"focus": {"id": "C-focus", "custody": "C", "accessible": True, "melded": False},
                          "robe": {"id": "C-robe", "custody": "C", "worn": True},
                          "spellbook": {"id": "C-book", "custody": "C", "accessible": True}}
        state["actors"]["C"] = c
        state["objects"]["C-focus"] = {"id": "C-focus", "kind": "spellcasting-focus", "owner": "C", "custody": "C", "accessible": True}
        state["objects"]["C-conditional-profile"] = {"class": "Cleric", "classLevel": 20, "heroPath": "Cultist",
            "stats": {"S": 4, "M": 5, "PB": 6, "WIS": 20, "spellAttack": 11, "rpMaximum": 58, "convictionMaximum": 7},
            "selectedAtLevel16": {"id": "cleric.hero.cultist.ritual-of-undeath", "source": "cleric.json#/cards/57"},
            "qualification": "A conditional authored fixture; not a claim about a campaign character."}
    return state


def activate_ua(s: dict, at: float) -> None:
    a = s["actors"]["A"]
    a["rp"] -= 26
    a["action"] = max(0, a["action"] - 1)
    a["effects"]["unholy-ascendance"] = {"root": "UA272-A-cast", "start": at, "expires": at + 60.0,
                                           "suppressed": False, "concentration": False, "rank": 9, "pricePaid": 26}
    a["body"]["type"] = "Undead"
    a["form"] = {"id": "UA270-LIFE", "bodyIdentity": "A-original-character-body", "sameHPTrack": True}
    a["lifecycle"]["operativeTargetingType"] = "Undead"
    a["resourceHistory"].append({"spellId": "unholy-ascendance", "rank": 9, "rpPaid": 26, "actionPaid": True, "at": at})
    if not any(x.get("spellId")=="unholy-ascendance" and x.get("at")==at for x in a.get("interruptionHistory",[])):
        a.setdefault("interruptionHistory",[]).append({"spellId":"unholy-ascendance","at":at,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})


def case_record(case_id: str, premise: str, state: dict, events: list[dict], assertions: list[str],
                status: str = "DEMONSTRATED_STATIC_TRACE", holds: list[str] | None = None) -> dict:
    final = copy.deepcopy(events[-1]["after"] if events else state)
    initial = copy.deepcopy(state)
    rebuild_cast_histories(initial)
    return {"id": case_id, "mainCaseId": case_id, "kind": "spell-review", "spellId": TARGET,
            "premise": premise, "questionIds": ["CC194-B04"], "holdIds": holds or [],
            "status": status, "runtimeExecuted": False, "assertions": assertions,
            "initialState": initial, "events": events, "finalState": final,
            "finalSHA256": sha(final)}


def create_cases() -> list[dict]:
    refs = source_refs("inflict-wounds:Wizard rank1, Action, 2RP, V/S/F, 3d10 necrotic, melee spell attack",
                      "CH07:NULL-FIELD-QUIET-WELL-1", "CORE:WIS save DC15/hourly field exposure")
    cases: list[dict] = []

    # Matched ordinary and Null positive-to-zero forks use the same complete A/T profile.
    for case_no, null in [(12, False), (13, True)]:
        cid = f"RANK9CASTINGCOST5-272-UA-{'NULL' if null else 'ORDINARY'}-NEWZERO"
        s0 = base_state(7, a_pos=(9, 0, 0), t_pos=((0, 0, 0) if null else (8, 0, 0)))
        s0["time"] = 0.0
        evs: list[dict] = []
        cur = s0
        if null:
            def enter(s):
                s["actors"]["T"]["nullFieldExposure"] = {"fieldId": "NULL-FIELD-QUIET-WELL-1", "entered": 0.0, "elapsedSeconds": 3600,
                    "hourlyWISSave": {"at": 3600.0, "roll": 2, "modifier": 3, "total": 5, "dc": 15, "success": False}}
                s["actors"]["T"]["nullVeil"] = {"source": "failed hourly WIS DC15 while exposed to CH07 field", "fieldId": "NULL-FIELD-QUIET-WELL-1",
                    "acquired": 3600.0, "suppressed": False}
                s["actors"]["T"]["effects"]["null-veil"] = {"start": 3600.0, "suppressed": False, "sourceField": "NULL-FIELD-QUIET-WELL-1"}
                s["time"] = 3600.0
            ev, cur = event(cur, cid, 1, "null-veil-acquired", 3600.0,
                {"dealer": "T", "fieldId": "NULL-FIELD-QUIET-WELL-1", "exposureSeconds": 3600, "failedSave": "2+3=5 < DC15"}, refs, enter)
            evs.append(ev)
            def leave(s):
                s["actors"]["T"]["position"] = [8, 0, 0]
                s["actors"]["T"]["nullFieldExposure"]["exited"] = 3600.05
                s["time"] = 3600.05
            ev, cur = event(cur, cid, 2, "field-exit-and-move", 3600.05,
                {"dealer": "T", "position": [8, 0, 0], "outsideCylinder": True, "distanceToA": 1}, refs, leave)
            evs.append(ev)
            cast_at = 3600.1
        else:
            cast_at = 0.1
        def ua(s):
            s["time"] = cast_at
            activate_ua(s, cast_at)
        ev, cur = event(cur, cid, len(evs)+1, "cast-resolution", cast_at,
            {"actor": "A", "spellId": "unholy-ascendance", "rank": 9, "price": 26, "action": "Action", "components": "V/S/F",
             "bodyIdentityPreserved": True, "operativeTargetingType": "Undead", "expires": cast_at+60}, refs, ua)
        evs.append(ev)
        def root(s):
            s["time"] = cast_at + 0.1
            t=s["actors"]["T"]
            t["rp"]-=2;t["action"]=0
            t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"actionPaid":True,"at":cast_at+0.1})
            t["interruptionHistory"].append({"spellId":"inflict-wounds","at":cast_at+0.1,"windowOpened":True,
                "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
            t["classFeatureState"]["spellEfficiency"].update({"usesAvailable":True,"pendingMatrix":"inflict-wounds",
                "triggeredByCastAt":cast_at+0.1,"expiresAfterRegularTurnEnd":3608.0})
            s["results"].append({"kind": "damage-root", "id": f"{cid}/root1", "dealer": "T", "nullNonlethal": bool(null),
                "dealerSnapshot": {"nullVeilUnsuppressed": bool(null), "fieldId": "NULL-FIELD-QUIET-WELL-1" if null else None},
                "castCommit":{"spellId":"inflict-wounds","rank":1,"RPpaid":2,"ActionSpent":True,"at":cast_at+0.1,
                    "interruptionWindow":{"opened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"outcome":"no interruption attempt"}},
                "recipientSnapshot": {"identity": "A-original-character-body", "type": "Undead", "life": "Living", "hp": 7,
                    "maxHP": 122, "tempHP": 0, "wounds": 1, "deathSaveFailures": 0, "recoveryDeadline": None}})
            s["time"] = cast_at+0.1
        ev, cur = event(cur, cid, len(evs)+1, "damage-root-created", cast_at+0.1,
            {"dealer": "T", "spellId": "inflict-wounds", "rank": 1, "rootFlag": bool(null),
             "rootFlagSnapshot": "same actual damaging character T; controller-independent"}, refs, root)
        evs.append(ev)
        def damage(s):
            a = s["actors"]["A"]
            before = {"hp": 7, "tempHP": 0, "wounds": 1, "deathSaveFailures": 0, "life": "Living", "type": "Undead"}
            after_damage = {"attack": "d20=3 + 11 = 14 vs AC12", "damageRoll": "3d10=24 necrotic", "allResistance": "floor(24/2)=12",
                            "tempAbsorbed": 0, "postTempDamage": 12, "actualHPLoss": 7, "overkill": 5, "resultingHP": 0,
                            "instantDeath": "actual HP loss7; 7-7=0 < effective maximum 122", "woundSaveTrigger": "positive-to-zero",
                            "woundSave": "CON14: d20=10 +2 - Wound1 =11 vs DC10; success",
                            "woundsAfter": 1}
            if null:
                after_damage["woundSave"]="suppressed entirely by UA270-LIFE because this is a qualifying same-dealer Null root"
                after_damage["instantDeath"]="suppressed by UA270-LIFE Null branch after normal damage quantities are computed"
            a["lifecycle"]["lastDamageSnapshot"] = before
            a["lifecycle"]["lastDamageCalculation"] = after_damage
            a["hp"] = 0; a["tempHP"] = 0; a["conditions"]["Unconscious"] = True
            if null:
                a["lifecycle"].update({"state": "Stable0", "deathSaveFailures": 0, "deathSaveSuccesses": 0,
                    "stableRecoveryDeadline": cast_at+0.22+7200, "recoveryDie": 2, "recoveryUnitSeconds": 3600})
                a["deathSaves"] = {"failures": 0, "successes": 0}
                a["conditions"].pop("Dying", None)
                a["conditions"]["Stable"] = True
            else:
                a["lifecycle"].update({"state": "Dying0", "deathSaveFailures": 0, "deathSaveSuccesses": 0,
                    "stableRecoveryDeadline": None, "nextDeathSaveAt": 6.0})
                a["deathSaves"] = {"failures": 0, "successes": 0}
                a["conditions"]["Dying"] = True
            s["results"].append({"kind": "damage-resolution", "dealer": "T", "nullNonlethal": bool(null),
                "preEvent": before, "calculation": after_damage, "postEventLifecycle": copy.deepcopy(a["lifecycle"])})
            s["time"] = cast_at+0.22
        ev, cur = event(cur, cid, len(evs)+1, "damage-resolution", cast_at+0.22,
            {"preEvent": {"identity": "A-original-character-body", "operativeType": "Undead", "hp": 7, "maxHP": 122, "tempHP": 0,
             "wounds": 1, "conditions": [], "deathSaveFailures": 0, "recoveryDeadline": None},
              "damage": "3d10=24; all-resistance=12; tempHP absorbs0; post-temp damage12; actual HP loss7; overkill5; HP7->0",
             "nullNonlethal": bool(null), "outcome": "Stable0 with one 2-hour deadline" if null else "ordinary Dying0, counters0, next death-save marker6"}, refs, damage)
        evs.append(ev)
        if null:
            cid_state=cur
            def stable_turn(s):
                t=s["actors"]["T"];t["action"]=1;t["lastRegularStart"]=3602.0;t["nextRegularStart"]=3608.0;s["time"]=3602.0
            ev,cur=event(cur,cid,len(evs)+1,"regular-start-T",3602.0,{"actor":"T","normalActionRefresh":True,"NullVeilStillUnsuppressed":True},refs,stable_turn)
            evs.append(ev)
            def stable_again(s):
                a=s["actors"]["A"];t=s["actors"]["T"]
                t["rp"]-=1;t["action"]=0;t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":1,"actionPaid":True,
                    "spellEfficiencyApplied":True,"at":3602.1})
                t["classFeatureState"]["spellEfficiency"].update({"usesAvailable":False,"appliedAt":3602.1,
                    "triggeredByCastAt":cast_at+0.1,"expiresAfterRegularTurnEnd":3608.0,"pendingMatrix":None,
                    "consumedByCastAt":3602.1})
                a["lifecycle"]["stableRecoveryDeadline"] = cast_at+0.22+7200
                s["results"].append({"kind":"later-null-hit-already-Stable0","rootDealer":"T","nullNonlethal":True,
                    "damageRoot":{"newIndependentRoot":True,"sourceSpell":"inflict-wounds","rank":1,"rootNullNonlethal":True,
                        "attack":"d20=5 + 11 =16 vs AC12; hit","rawDamage":"3d10=18 necrotic","allResistance":"floor(18/2)=9",
                        "tempAbsorbed":0,"postTempDamage":9,"actualHPLoss":0,"overkill":9},
                    "ordinaryDamage":"HP already0; qualifying same-dealer Null root causes no additional death failure; exact recovery deadline preserved",
                    "spellMatrixHistory":{"priorInflictWoundsAt":cast_at+0.1,"currentAt":3602.1,"repeatedMatrix":True,
                        "refrainDelta":1,"WizardProtectedFirstMatrix":False,"SpellEfficiencyReduction":1,"actualRPpaid":1},
                    "priorRecoveryDeadlinePreserved":a["lifecycle"]["stableRecoveryDeadline"],"deathCounters":{"failures":0,"successes":0}})
                s["time"] = 3602.1
            ev, cur = event(cur,cid,len(evs)+1,"already-stable0-null-hit",3602.1,
                {"newIndependentRoot":True,"dealer":"T","rank1InflictWoundsCost":1,"spellEfficiencyApplied":True,
                 "sameMatrixRepeat":True,"refrainDelta":1,"result":"same stable recovery deadline and counters; no reroll/restart"},refs,stable_again)
            evs.append(ev)
        cases.append(case_record(cid,
            "Matched conditional Wizard20 caster profile. Ordinary fork and same-dealer Null fork differ only in T's source-bound Null Veil at root creation.",
            s0, evs, ["Same A original identity/body, UA duration, HP/maxHP/tempHP/Wounds and damage packet in both forks.",
                     "Null root is created by the actual damaging character T while its CH07-derived Null Veil is unsuppressed.",
                     "Null positive-to-zero establishes Stable0 with one absolute d4-hour deadline; later Null damage preserves it." if null else
                     "Ordinary positive-to-zero uses the same character's normal Core damage/Wound/death procedure."],
            holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Untriggered would-die protection: Null at already-Dying0 versus ordinary lethal hit.
    for case_no, null in [(14, True), (15, False)]:
        cid = f"RANK9CASTINGCOST5-272-UA-{'NULL' if null else 'ORDINARY'}-WOULD-DIE"
        s0 = base_state(0, a_rp=54, t_rp=80, a_pos=(9,0,0), t_pos=(8,0,0), add_cleric=True)
        a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
        s0["time"] = 3614.0
        a["body"]["type"]="Undead"; a["effects"]["unholy-ascendance"]={"start":3600.1,"expires":3660.1,"suppressed":False,"concentration":False,"pricePaid":26}
        a["resourceHistory"].append({"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":3600.1})
        a["interruptionHistory"].append({"spellId":"unholy-ascendance","at":3600.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","sameHPTrack":True}
        a["lifecycle"]={"identity":"A-original-character-body","state":"Dying0","operativeTargetingType":"Undead",
                         "deathSaveFailures":2,"deathSaveSuccesses":0,"nextDeathSaveAt":3618.0,"stableRecoveryDeadline":None,
                         "history":[{"kind":"ordinary-positive-to-zero-damage","at":3601.0},{"kind":"failed-regular-death-save","at":3606.0},{"kind":"failed-regular-death-save","at":3612.0}]}
        a["deathSaves"]={"failures":2,"successes":0}; a["conditions"]={"Unconscious":True,"Dying":True}
        c["profile"]="CC194-C20-CULTIST-CONDITIONAL"; c["heroPath"]="Cultist"
        c["reviewStats"]={"S":4,"M":5,"PB":6,"WIS":20,"spellAttack":11,
            "profileSource":"ACTOR_PROFILES.json#/Cleric20; conditional level-16 Cultist choice from cleric.json#/cards/57"}
        c["conditionalHeroPathSelection"]={"heroPath":"Cultist","level":16,"card":"cleric.json#/cards/57",
            "sourceProfile":"ACTOR_PROFILES.json#/Cleric20","selectionCountPreserved":True}
        c["conviction"]=4; c["rp"]=52; c["action"]=1
        c["finiteUses"]={"cleric.hero.cultist.ritual-of-undeath":{"frequency":"1/long rest","usesBefore":1,
            "usesRemaining":0,"committedAt":3600.0,"source":"cleric.json#/cards/57"}}
        c["effects"]["ritual-of-undeath-death-ward"]={"target":"A","start":3600.0,"expires":3660.0,
            "mode":"Death Ward","activationUseSpent":True,"wardTriggerAvailable":True,"source":"cleric.json#/cards/57","triggered":False}
        c["resourceHistory"].append({"ability":"ritual-of-undeath","source":"cleric.json#/cards/57","mode":"Death Ward",
            "rpPaid":6,"convictionPaid":3,"actionPaid":True,"longRestUseBefore":1,"longRestUseAfter":0,"at":3600.0})
        t["nullVeil"]={"source":"CH07 failed hourly WIS save","fieldId":"NULL-FIELD-QUIET-WELL-1","acquired":3600.0,"suppressed":False} if null else None
        t["effects"]["null-veil"]={"start":3600.0,"suppressed":False,"sourceField":"NULL-FIELD-QUIET-WELL-1"} if null else t["effects"].pop("null-veil",None)
        t["nullFieldExposure"]={"fieldId":"NULL-FIELD-QUIET-WELL-1","elapsedSeconds":3600,"hourlyWISSave":{"roll":2,"modifier":3,"total":5,"dc":15,"success":False}} if null else None
        s0["objects"]["preHitFork"]={"sharedSnapshotForCases14and15":True,"hp":0,"state":"Dying0","failures":2,
            "nextDeathSaveAt":3618.0,"wardUntriggered":True,"wardActivationUseAlreadySpent":True,"wardTriggerAvailable":True}
        u=copy.deepcopy(t);u["id"]="U";u["profile"]="CC194-W20";u["position"]=[8,0,0];u["rp"]=78;u["nullVeil"]=None;u["effects"].pop("null-veil",None)
        u["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"at":3601.0,"rootNullNonlethal":False})
        u["interruptionHistory"].append({"spellId":"inflict-wounds","at":3601.0,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        s0["actors"]["U"]=u
        advance_calendar(s0,3614.0);rebuild_cast_histories(s0)
        s0["results"].extend([
            {"kind":"prior-ordinary-positive-to-zero-history","at":3601.0,"dealer":"U","nullNonlethal":False,
             "recipient":"A-original-character-body","attack":"d20=8 + 11 =19 vs AC12; hit",
             "damage":{"spell":"inflict-wounds","rank":1,"raw":"3d10=14 necrotic","allResistance":"floor(14/2)=7",
                 "tempAbsorbed":0,"postTempDamage":7,"actualHPLoss":7,"startingHP":7,"endingHP":0,"overkill":0,
                 "woundSave":"CON14: d20=10 +2 - Wound1 =11 vs DC10; success","deathTransition":"ordinary Dying0","rootNullNonlethal":False},
             "committedCast":{"rpPaid":2,"actionPaid":True,"at":3601.0},"subsequentFailedDeathSaves":[3606.0,3612.0]},
            {"kind":"regular-death-save","at":3606.0,"roll":"d20=5","result":"failure","failuresAfter":1},
            {"kind":"regular-death-save","at":3612.0,"roll":"d20=4","result":"failure","failuresAfter":2}
        ])
        refs2=source_refs("cleric.json#/cards/57","ACTOR_PROFILES.json#/Cleric20/convictionMaximum",
            "CH07/currentModule/chambers/6/nullField","CORE_RESOLUTION_PLAYTEST.md#death-saves-and-critical-damage",
            "SPELL_INTEGRATION_RULES.md#Resolve-a-cast-at-the-table","wizard.json#/cards/15")
        evs=[]
        def resolve(s):
            a=s["actors"]["A"]; c=s["actors"]["C"]
            if null:
                a["lifecycle"]["nextDeathSaveAt"]=3618.0
                a["deathSaves"]={"failures":2,"successes":0}
                c["effects"]["ritual-of-undeath-death-ward"]["triggered"]=False
                c["effects"]["ritual-of-undeath-death-ward"]["wardTriggerAvailable"]=True
                outcome="Qualifying same-dealer Null suppresses damage-caused death failures; A remains Dying0 with failure2 and the same next-save marker; ward activation was paid, but its trigger is not consumed."
            else:
                a["hp"]=1; a["life"]="Living"; a["lifecycle"]["state"]="Living1-WardReplacement"
                a["lifecycle"]["deathSaveFailures"]=0; a["lifecycle"]["deathSaveSuccesses"]=0
                a["lifecycle"].pop("nextDeathSaveAt",None); a["deathSaves"]={"failures":0,"successes":0}
                a["conditions"].pop("Dying",None); a["conditions"].pop("Unconscious",None)
                a["targetingTypeTags"]=["Humanoid","Undead"]
                a["effects"]["ritual-of-undeath-dual-type"]={"source":"cleric.json#/cards/57","start":3614.1,
                    "expires":3624.0,"expiryBasis":"A's actual next regular turn starts3618 and ends3624",
                    "types":["Humanoid","Undead"],"triggeredByDeathWard":True}
                c["effects"]["ritual-of-undeath-death-ward"]["triggered"]=True
                c["effects"]["ritual-of-undeath-death-ward"]["triggerAt"]=3614.1
                outcome="Critical melee hit at zero HP supplies two death failures; starting from2 reaches the would-die transition. The previously activated Ward replaces death at1HP, clears death state, and sets dual-type expiry to A's actual next turn END at3624."
            t=s["actors"]["T"];t["rp"]-=2;t["action"]=0
            t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"actionPaid":True,"criticalMeleeAttack":True,"at":3614.1})
            t["interruptionHistory"].append({"spellId":"inflict-wounds","at":3614.1,"windowOpened":True,
                "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
            s["results"].append({"kind":"zero-damage-outcome","nullNonlethal":bool(null),
                "damageRoot":{"dealer":"T","nullNonlethal":bool(null),"createdAt":3614.1,"newIndependentRoot":True,
                    "castCommit":{"spellId":"inflict-wounds","rank":1,"rpPaid":2,"actionPaid":True},
                    "attack":"d20=4/14 with advantage; 14+11=25 vs AC12; hit; critical vs Unconscious target within5ft",
                    "damage":{"roll":"6d10=30 necrotic","allResistance":"floor(30/2)=15","tempAbsorbed":0,
                        "postTempDamage":15,"actualHPLoss":0,"targetHPbefore":0,"overkill":15}},
                "targetBefore":{"hp":0,"failures":2,"successes":0,"nextDeathSaveAt":3618.0},
                "dealer":"T","outcome":outcome})
            s["time"]=3614.1
        ev, s1=event(s0,cid,1,"already-dying0-damage-resolution",3614.1,
             {"nullNonlethal":bool(null),"preEvent":{"hp":0,"life":"Living","state":"Dying0","deathSaveFailures":2,"nextDeathSaveAt":3618.0,
              "UA":"operative","ward":"active and trigger-available; its1/long-rest activation was already paid"},
              "outcome":"Null keeps markers and ward trigger availability" if null else "ordinary death trigger is replaced by Ritual of Undeath Death Ward; death counters and pending marker clear"},refs2,resolve)
        evs.append(ev)
        cases.append(case_record(cid,
             "Conditional same pre-hit snapshot for paired Null/ordinary forks. Cleric20 base profile supplies S4/M5/PB6/WIS20, RP maximum58 and Conviction maximum7; a conditional level-16 Cultist selection of card57 spends 6RP+3 Conviction and its one long-rest activation at3600. A was Living before zero-state history and remains the same character.",
             s0,evs,["Null branch preserves existing Dying0 counters/schedule; ward activation is spent but its trigger remains available." if null else
                     "Ordinary critical damage triggers the acquired Ward, recovers A to1HP, clears counters/next-save marker, and records dual-type expiry at A's next turn END."],
            holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Healing eligibility, accepted Antimagic boundaries and UA270-HEAL.
    cid="RANK9CASTINGCOST5-272-UA-HEAL-OPERATIVE"
    s0=base_state(50,a_rp=80,add_cleric=True,a_pos=(9,0,0),t_pos=(10,0,0));a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    a["hp"]=50;activate_ua(s0,0.1);s0["time"]=0.0
    advance_calendar(s0,6.0);rebuild_cast_histories(s0);s0["time"]=6.0
    refs3=source_refs("catalog.json#/spells/630/operational","cleric.json#/cards/12","UA270-HEAL authorized by Return270",
        "SPELL_INTEGRATION_RULES.md#Resolve-a-cast-at-the-table","wizard.json#/cards/15")
    evs=[]
    def reject_heal(s):
        s["results"].append({"kind":"preflight-rejection","ability":"Healing Rite","target":"A",
            "reason":"operative targeting type Undead fails the card's living-only eligibility",
            "rpPaid":0,"actionSpent":False,"beforeCommit":True,"spellOrAbilityHistoryChanged":False});s["time"]=6.1
    ev,s1=event(s0,cid,1,"healing-rite-rejected-before-commit",6.1,
        {"targetType":"Undead","livingOnly":True,"RPbefore":58,"costPaid":0,"actionSpent":False},refs3,reject_heal);evs.append(ev)
    def vt(s):
        a=s["actors"]["A"];t=s["actors"]["T"]
        before={"T":{"hp":100,"tempHP":0,"wounds":1,"life":"Living"},"A":{"hp":50,"tempHP":0,"wounds":1}}
        a["action"]=0;a["hp"]=56
        a["resourceHistory"].append({"spellId":"vampiric-touch","rank":3,"ordinaryQuote":5,"UA270-HEAL":True,
            "rpPaid":0,"actionPaid":True,"spellEfficiencyApplied":False,"at":6.2})
        a["interruptionHistory"].append({"spellId":"vampiric-touch","at":6.2,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        t["hp"]=88
        t["lifecycle"]={"lastDamageSettlement":{"root":"UA272-HEAL-OPERATIVE/VT1","rawDamage":12,
            "damageType":"necrotic","resistance":0,"tempHPBefore":0,"tempAbsorbed":0,"postTempDamage":12,
            "actualHPLoss":12,"overkill":0,"hpBefore":100,"hpAfter":88,"woundsBefore":1,"woundsAfter":1,
            "deathSaveFailures":0,"conditionsChanged":False}}
        s["results"].append({"kind":"vampiric-touch-self-heal","cast":{"actor":"A","rank":3,"action":True,
            "components":"V/S/F","operativeUA":True,"ordinaryQuote":5,"castingRPWaived":5,"rpPaid":0,"at":6.2,
            "interruptionWindow":{"opened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"}},
            "attack":"d20=11 + 11 =22 vs AC12; hit","targetDamageSettlement":{"target":"T","hpBefore":100,
                "rawNecrotic":12,"resistance":0,"tempAbsorbed":0,"actualDamageDealt":12,"hpAfter":88,"wounds":1},
            "healing":{"recipient":"same caster A","formula":"floor(actualDamageDealt/2)","actualDamageDealt":12,
                "healing":6,"hpBefore":50,"hpAfter":56},"priorTargetSnapshot":before,
            "RPbefore":54,"RPafter":54,"modifiersCapsAndProhibitions":"unchanged"});s["time"]=6.2
    ev,s2=event(s1,cid,2,"vampiric-touch-self-heal",6.2,
        {"rank":3,"priceWaiver":"UA270-HEAL only; no damage/healing increase","damage":12,"selfHeal":6,"targetHP":"100->88"},refs3,vt);evs.append(ev)
    cases.append(case_record(cid,"Unholy Ascendance operative; conditional Wizard20/Cleric20 fixtures. Healing Rite is preflight-rejected against the Undead target; the continuing caster uses the authorized Vampiric Touch adapter against T.",s0,evs,
        ["Known Healing Rite illegality consumes neither Action nor RP.","Vampiric Touch remains Action/Touch/V/S/F/rank3/base5RP, one attack and floor(actualDamageDealt/2); UA waives only its casting RP.",
         "T's target damage is fully settled before A receives the 6HP self-heal."],holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    cid="RANK9CASTINGCOST5-272-UA-HEAL-SUPPRESSED"
    s0=base_state(50,a_rp=80,add_cleric=True,a_pos=(0,0,0),t_pos=(5,0,0));a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    a["hp"]=50;a["rp"]=47
    a["concentration"]={"spellId":"polymorph","root":"POLY272-S","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7,"rank":4}
    a["effects"]["polymorph"]={"root":"POLY272-S","start":0.1,"expires":60.1,"suppressed":True,"concentration":True}
    a["effects"]["unholy-ascendance"]={"root":"UA272-S","start":6.1,"expires":66.1,"suppressed":True,"concentration":False,"pricePaid":26}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suppressed":True,
        "suspendedPriorForm":{"id":"polymorph","root":"POLY272-S","expires":60.1,"gearMelded":["A-focus","A-robe","A-book"]}}
    a["body"]["type"]="Humanoid";a["lifecycle"]["operativeTargetingType"]="Humanoid"
    for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
    s0["objects"]["T-focus"]["custody"]="A";s0["objects"]["T-focus"]["transferHistory"]=[{"from":"T","to":"A","at":5.9}]
    a["equipment"]["externalFocus"]={"id":"T-focus","owner":"T","custody":"A","accessible":True,"held":True}
    t["equipment"]["focus"]={"id":"C-focus","owner":"C","custody":"T","accessible":True,"held":True}
    s0["objects"]["T-focus"]["owner"]="T"
    s0["objects"]["C-focus"]["custody"]="T";s0["objects"]["C-focus"]["transferHistory"]=[{"from":"C","to":"T","at":7.9}]
    c["equipment"].pop("focus",None)
    a["resourceHistory"].extend([{"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1},
        {"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":6.1}])
    t["rp"]=59;t["resourceHistory"].append({"spellId":"antimagic-field","rank":8,"rpPaid":21,"actionPaid":True,"at":8.1})
    a["interruptionHistory"].extend([
        {"spellId":"polymorph","at":0.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
        {"spellId":"unholy-ascendance","at":6.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
    ])
    t["interruptionHistory"].append({"spellId":"antimagic-field","at":8.1,"windowOpened":True,
        "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
    t["concentration"]={"spellId":"antimagic-field","root":"AMF272-S","start":8.1,"expires":68.1,"concentration":True}
    a["effects"]["antimagic-field"]={"root":"AMF272-S","start":8.1,"expires":68.1,"active":True,
        "school":"Abjuration","center":[5,0,0],"radius":20,"suppressionRule":"RW149-F: actual spells and explicitly magical nonspell/item expressions"}
    advance_calendar(s0,8.5)
    a["action"]=0;t["action"]=0;c["action"]=1;s0["time"]=8.5;rebuild_cast_histories(s0)
    refs7=source_refs("cleric.json#/cards/12","rank8ward5_reviewed_149/DIRECTOR_RETURN/PROCEDURES/antimagic-field.json#/procedure",
        "rank8ward5_reviewed_149/DIRECTOR_RETURN/DIRECTOR_DECISION.json#/acceptedIds",
        "RW149-F AC5-ANTIMAGIC-IO-04: legal cast inside; originating-inside spell payload suppressed with no queued release",
        "wizard.json#/cards/15","TRANSFORMATION_SPELL_PLAYTEST.md#Polymorph-and-Antimagic-suppression")
    evs=[]
    def heal_under_field(s):
        a=s["actors"]["A"];c=s["actors"]["C"];c["rp"]-=2;c["action"]=0;a["hp"]=72
        c["resourceHistory"].append({"ability":"healing-rite","source":"cleric.json#/cards/12","rpPaid":2,"actionPaid":True,
            "target":"A","at":9.0,"dice":"4d8=17","M":5})
        s["results"].append({"kind":"healing-rite-success","target":"A","targetTypeAtCommit":"Humanoid",
            "fieldClassification":{"rule":"RW149-F suppresses actual spells and explicitly magical nonspell/item expressions",
                "card":"active Cleric ability; spellRank null; tags rite, healing; no explicit magical tag",
                "disposition":"not in the field suppression predicate"},
            "roll":"S=4d8(17)+M5=22","hpBefore":50,"hpAfter":72,"woundsBefore":1,"woundsAfter":1,
            "rpPaid":2,"actionPaid":True,"noWoundRemoval":True});s["time"]=9.0
    ev,state=event(s0,cid,1,"healing-rite-under-field-source-classified",9.0,
        {"eligibility":"living Humanoid within30ft","suppression":"not suppressed; card is a nonspell and not expressly magical",
         "cost":2,"healing":22,"noWoundRemoval":True},refs7,heal_under_field);evs.append(ev)
    def start_a(s):
        a=s["actors"]["A"];a["action"]=1;a["lastRegularStart"]=12.0;a["nextRegularStart"]=18.0;s["time"]=12.0
    ev,state=event(state,cid,2,"regular-start-A",12.0,{"actor":"A","actionRefresh":True},refs7,start_a);evs.append(ev)
    def blocked_vt(s):
        a=s["actors"]["A"]
        a["rp"]-=5;a["action"]=0
        a["resourceHistory"].append({"spellId":"vampiric-touch","rank":3,"ordinaryQuote":5,"rpPaid":5,"actionPaid":True,
            "payload":"suppressed at origin by AMF","spellEfficiencyApplied":False,"at":12.1})
        a["classFeatureState"]["spellEfficiency"].update({"usesAvailable":True,"pendingMatrix":"vampiric-touch",
            "triggeredByCastAt":12.1,"expiresAfterRegularTurnEnd":18.0})
        s["results"].append({"kind":"vampiric-touch-blocked-at-origin","actor":"A","target":"T","rank":3,
            "quote":5,"rpPaid":5,"actionPaid":True,"components":"V/S/F; accessible external T-focus",
            "targetEligibilityAtCommit":True,"attackRoll":"none; payload suppressed before attack","damage":0,"actualDamageDealt":0,
            "healing":0,"queuedFutureRelease":False,"refund":0,"HP":{"A":72,"T":100},
            "fieldRule":"RW149-F AC5-ANTIMAGIC-IO-04: originating-inside ordinary magical payload is suppressed after legal commitment"})
        a["interruptionHistory"].append({"spellId":"vampiric-touch","at":12.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt before field suppression"})
        s["time"]=12.1
    ev,state=event(state,cid,3,"vampiric-touch-paid-payload-suppressed",12.1,
        {"spellRank":3,"ordinaryRP":5,"ActionSpent":True,"effect":"no attack, damage, healing or queued release","targetHP":"T remains100"},refs7,blocked_vt);evs.append(ev)
    def poly_expire(s):
        a=s["actors"]["A"];a["effects"].pop("polymorph",None);a["concentration"]=None
        a["form"]["suspendedPriorForm"]={"id":"polymorph","root":"POLY272-S","expiredAt":60.1,"resumed":False}
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"polymorph-original-expiry-under-AMF","at":60.1,"sameRootEnded":True,
            "UAstillActiveButSuppressed":True,"UAdeadline":66.1,"gearRestoredByGenuinePolymorphClosure":True,
            "externalFocus":{"id":"T-focus","custody":"A","accessible":True},"noDuplication":True});s["time"]=60.1
    ev,state=event(state,cid,4,"polymorph-expires-under-field",60.1,
        {"originalDeadline":60.1,"concentrationEnds":True,"originalGearRestoredOnce":True},refs7,poly_expire);evs.append(ev)
    def ua_expire(s):
        a=s["actors"]["A"];a["effects"].pop("unholy-ascendance",None);a["form"]=None
        a["body"]["type"]="Humanoid";a["lifecycle"]["operativeTargetingType"]="Humanoid"
        s["results"].append({"kind":"UA-original-expiry-under-AMF","at":66.1,"sameRootEnded":True,
            "AMFstillActiveUntil":68.1,"body":"original Humanoid","HP":72,"resourceRefresh":False,
            "gearAlreadyRestoredAtPolyClosure":True,"externalFocusCustody":"A"});s["time"]=66.1
    ev,state=event(state,cid,5,"ua-expires-under-field",66.1,{"originalDeadline":66.1,"noClockRestart":True},refs7,ua_expire);evs.append(ev)
    def field_expire(s):
        s["actors"]["A"]["effects"]["antimagic-field"]["active"]=False
        s["actors"]["A"]["effects"]["antimagic-field"]["endedAt"]=68.1
        s["actors"]["T"]["concentration"]=None
        s["results"].append({"kind":"AMF-original-expiry","at":68.1,"durationSeconds":60,
            "allTransformationRecordsAlreadyExpired":True,"resumption":"none; no surviving suppressed record",
            "resourceRefresh":False,"gearCustody":{"A-focus":"A","A-robe":"A","A-book":"A","T-focus":"A","C-focus":"T"}});s["time"]=68.1
    ev,state=event(state,cid,6,"amf-expires-at-sixty-seconds",68.1,
        {"castAt":8.1,"durationSeconds":60,"expiresAt":68.1,"concentrationEnds":True},refs7,field_expire);evs.append(ev)
    def start_a72(s):
        s["time"]=72.0
    ev,state=event(state,cid,7,"regular-start-A-after-reversion",72.0,{"actor":"A","actionRefresh":True},refs7,start_a72);evs.append(ev)
    def vt_after_reversion(s):
        a=s["actors"]["A"];t=s["actors"]["T"]
        a["rp"]-=5;a["action"]=0;a["hp"]=78;t["hp"]=88
        a["resourceHistory"].append({"spellId":"vampiric-touch","rank":3,"ordinaryQuote":5,"rpPaid":5,"actionPaid":True,
            "spellEfficiencyApplied":False,"at":72.1})
        a["interruptionHistory"].append({"spellId":"vampiric-touch","at":72.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        a["classFeatureState"]["spellEfficiency"].update({"usesAvailable":True,"expiredPriorWindowAt":18.0,
            "lastCastAt":72.1,"pendingMatrix":"vampiric-touch","triggeredByCastAt":72.1,
            "expiresAfterRegularTurnEnd":84.0,"reason":"same matrix cast occurs after the prior window; this cast opens a new window"})
        t["lifecycle"]={"lastDamageSettlement":{"root":"UA272-HEAL-SUPPRESSED/VT-AFTER","rawDamage":12,
            "damageType":"necrotic","resistance":0,"tempHPBefore":0,"tempAbsorbed":0,"postTempDamage":12,
            "actualHPLoss":12,"overkill":0,"hpBefore":100,"hpAfter":88,"woundsBefore":1,"woundsAfter":1,
            "deathSaveFailures":0,"conditionsChanged":False}}
        s["results"].append({"kind":"vampiric-touch-ordinary-after-lawful-reversion","at":72.1,"actor":"A","target":"T",
            "body":"original Humanoid; UA and Polymorph ended at their original deadlines; AMF ended at68.1",
            "focus":{"id":"T-focus","custody":"A","accessible":True},"attack":"d20=11 +11 =22 vs AC12; hit",
            "damage":{"raw":"3d6=12 necrotic","resistance":0,"tempAbsorbed":0,"actualDamageDealt":12,"T":{"hpBefore":100,"hpAfter":88}},
            "healing":{"formula":"floor(actualDamageDealt/2)","actualDamageDealt":12,"amount":6,"A":{"hpBefore":72,"hpAfter":78}},
            "ordinaryQuote":5,"RPpaid":5,"ActionPaid":True,"refrain":{"sameMatrixAsCommittedSuppressedCast":True,
                "refrainDelta":1,"WizardBaseDissonance":1,"spellEfficiencyApplied":False}});s["time"]=72.1
    ev,state=event(state,cid,8,"vampiric-touch-ordinary-after-reversion",72.1,
        {"rank":3,"ordinaryRP":5,"sameCastFamilyRepeat":True,"payload":"resolved normally after all suppression ended"},refs7,vt_after_reversion);evs.append(ev)
    cases.append(case_record(cid,"The accepted Antimagic Field source is applied to two real suppressed spells. Healing Rite remains outside the field scope because its exact Cleric card is a nonspell ability without an explicitly magical tag. A valid Vampiric Touch cast inside commits its ordinary price but has no queued payload; the positive ordinary-price spell witness occurs only after natural reversion and field expiry.",s0,evs,
        ["Healing Rite pays2RP and heals S4d8+M5=22 under the exact RW149-F class-feature predicate; it removes no Wound.",
         "Vampiric Touch inside the field commits5RP and Action; it produces no attack, damage, healing or later release.",
         "The field expires68.1; Polymorph expires60.1 and UA66.1 while suppressed, so neither record resumes and no deadline/resource is refreshed.",
         "After lawful reversion, ordinary Vampiric Touch pays5RP, settles T100->88, then heals A72->78 by floor(actualDamageDealt/2)."],
        holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Prior form, focus custody, real Antimagic suppression, resumption, rejected rank-3 Dispel, original expiry.
    cid="RANK9CASTINGCOST5-272-UA-FORM-LIFECYCLE"
    s0=base_state(50,a_pos=(0,0,0),t_pos=(5,0,0),add_cleric=True); a,b=s0["actors"]["A"],s0["actors"]["T"]
    c=s0["actors"]["C"]
    a["rp"]=80; s0["time"]=0.0; evs=[]
    refs4=source_refs("catalog.json#/spells/735/operational","spell_form_profiles.json#/profiles/spellform.humanoid",
        "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning","rank8ward5_reviewed_149/DIRECTOR_RETURN/PROCEDURES/antimagic-field.json#/procedure",
        "rank8ward5_reviewed_149/DIRECTOR_RETURN/DIRECTOR_DECISION.json#/acceptedIds",
        "wizard.json#/cards/19","wizard.json#/cards/21","UA270-LIFE spell-local suspension")
    def polymorph_cast(s):
        a=s["actors"]["A"];a["rp"]-=7;a["action"]=0
        a["concentration"]={"spellId":"polymorph","root":"POLY272-A","start":0.1,"expires":60.1,"concentration":True,"rank":4,"pricePaid":7}
        a["form"]={"id":"polymorph","profile":"spellform.humanoid","start":0.1,"expires":60.1,"physicalExpression":"Humanoid-form","underlyingBody":"A-original-character-body","gearMelded":["A-focus","A-robe","A-book"],"concentrationRoot":"POLY272-A"}
        a["body"].update({"type":"Humanoid","hands":2,"speech":True})
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True})
        a["resourceHistory"].append({"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1})
        a["interruptionHistory"].append({"spellId":"polymorph","at":0.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"});s["time"]=0.1
    ev,cur=event(s0,cid,1,"cast-polymorph-r4-humanoid",0.1,{"rank":4,"price":7,"action":"Action","concentrationDeadline":60.1,"profile":"spellform.humanoid","handsSpeech":True},refs4,polymorph_cast);evs.append(ev)
    def transfer_focus(s):
        s["objects"]["T-focus"]["custody"]="A";s["objects"]["T-focus"]["transferHistory"]=[{"from":"T","to":"A","at":5.9,"lawfulExternalTransfer":True}]
        s["actors"]["A"]["equipment"]["externalFocus"]={"id":"T-focus","owner":"T","custody":"A","accessible":True,"held":True}
        s["actors"]["T"]["equipment"]["focus"]={"id":None,"custody":"T","accessible":False,"melded":False}
        s["time"]=5.9
    ev,cur=event(cur,cid,2,"external-focus-transfer",5.9,{"item":"T-focus","owner":"T","custody":"T->A","meldedOriginalItemsRemainUnavailable":True},refs4,transfer_focus);evs.append(ev)
    def transfer_c_focus(s):
        s["objects"]["C-focus"]["custody"]="T";s["objects"]["C-focus"]["transferHistory"]=[{"from":"C","to":"T","at":5.95,"lawfulExternalTransfer":True}]
        s["actors"]["C"]["equipment"].pop("focus",None)
        s["actors"]["T"]["equipment"]["focus"]={"id":"C-focus","owner":"C","custody":"T","accessible":True,"held":True}
        s["time"]=5.95
    ev,cur=event(cur,cid,3,"alternate-focus-transfer-before-antimagic",5.95,{"item":"C-focus","owner":"C","custody":"C->T",
        "T-focusAlreadyWithA":True,"THasAccessibleFocusForAMF":True},refs4,transfer_c_focus);evs.append(ev)
    def start_a(s):
        a=s["actors"]["A"];a["action"]=1;a["bonusAction"]=1;a["lastRegularStart"]=6.0;a["nextRegularStart"]=12.0;s["time"]=6.0
    ev,cur=event(cur,cid,4,"regular-start-A",6.0,{"actor":"A","actionRefresh":True,"normalRegularSlot":True},refs4,start_a);evs.append(ev)
    def ua_cast(s):
        activate_ua(s,6.1);s["actors"]["A"]["equipment"]["focus"]={"id":"A-focus","custody":"A","accessible":False,"melded":True}
        s["actors"]["A"]["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","root":"POLY272-A","expires":60.1,"concentration":True,"gearMelded":["A-focus","A-robe","A-book"]},"externalFocusHeld":"T-focus"}
        s["time"]=6.1
    ev,s1=event(cur,cid,5,"cast-unholy-over-existing-form",6.1,{"price":26,"rank":9,"components":"V/S/F","externalFocus":"T-focus, custody T->A at5.9",
        "sameBodyIdentity":True,"priorPolymorphConcentration":"preserved; deadline60.1","UAexpires":66.1,"meldedAItems":"still unavailable"},refs4,ua_cast);evs.append(ev)
    def amf(s):
        a=s["actors"]["A"]; a["effects"]["antimagic-field"]={"root":"AMF272-T","start":8.1,"expires":68.1,"active":True,
            "center":[5,0,0],"radius":20,"suppressedTransforms":["unholy-ascendance","polymorph"]}
        a["effects"]["unholy-ascendance"]["suppressed"]=True; a["form"]["suppressed"]=True
        a["body"]["type"]="Humanoid";a["body"]["hands"]=2;a["life"]="Living"
        s["actors"]["T"]["concentration"]={"spellId":"antimagic-field","root":"AMF272-T","start":8.1,"expires":68.1,"concentration":True}
        s["actors"]["T"]["resourceHistory"].append({"spellId":"antimagic-field","rank":8,"rpPaid":21,"actionPaid":True,"at":8.1})
        s["actors"]["T"]["interruptionHistory"].append({"spellId":"antimagic-field","at":8.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        # Suppression keeps A's original Polymorph-melded gear inaccessible until that record genuinely ends.
        s["actors"]["T"]["rp"]-=21;s["actors"]["T"]["action"]=0
        s["results"].append({"kind":"antimagic-field-suppression","actor":"T","rank":8,"pricePaid":21,"scope":"all actual transformations",
            "A":{"body":"Humanoid expression","UA":"suppressed","Polymorph":"suppressed","clocks":{"poly":60.1,"UA":66.1},
                "originalGear":{"custody":"A","accessible":False,"melded":True},"externalFocus":{"id":"T-focus","custody":"A","accessible":True}},
            "T":{"focus":{"id":"C-focus","custody":"T","accessible":True}}})
        s["time"]=8.1
    ev,s2=event(s1,cid,6,"antimagic-field-suppression",8.1,{"caster":"T","spellId":"antimagic-field","rank":8,"RP":21,
        "durationSeconds":60,"expiresAt":68.1,"bothTransformationsSuppressed":True},refs4,amf);evs.append(ev)
    def amf_checkpoint(s):
        a=s["actors"]["A"]
        s["results"].append({"kind":"ongoing-field-suppression-checkpoint","at":14.2,"AMFactive":True,"expiresAt":68.1,
            "UA":{"suppressed":True,"expiresAt":66.1},"Polymorph":{"suppressed":True,"expiresAt":60.1},
            "originalGear":{"custody":"A","accessible":False,"melded":True},"noClockRestart":True})
        s["time"]=14.2
    ev,s3=event(s2,cid,7,"suppression-checkpoint",14.2,{"fieldStillActive":True,"originalGearStillMeldedAndUnavailable":True,
        "deadlinesUnchanged":{"Polymorph":60.1,"UA":66.1}},refs4,amf_checkpoint);evs.append(ev)
    def refresh_t(s):
        b=s["actors"]["T"];b["action"]=1;b["lastRegularStart"]=20.0;b["nextRegularStart"]=26.0;s["time"]=20.0
    ev,s3a=event(s3,cid,8,"regular-start-T",20.0,{"actor":"T","actionRefresh":True,"normalRegularSlot":True},refs4,refresh_t);evs.append(ev)
    def rejected_dispensal(s):
        a=s["actors"]["A"];b=s["actors"]["T"]
        s["results"].append({"kind":"known-illegal-dispel-rejected-before-commit","caster":"T","spell":"dispel-magic","actualSpellRank":3,"costQuote":5,
            "target":"A/unholy-ascendance","targetGeneratingRank":9,"sourceCeiling":"Dispel Magic accepts only rank0-3; no automatic upcast",
            "rpPaid":0,"actionSpent":False,"preflightRejectedBeforeAMFOrCastCommit":True,"UAremainsActive":True,"PolymorphStillSuspended":True})
        s["time"]=20.2
    ev,s4=event(s3a,cid,9,"rank3-dispel-known-ineligible",20.2,{"targetRank":9,"dispelRank":3,"attemptRejectedBeforeCommit":True,"noRPOrActionSpent":True},
        source_refs("catalog.json#/spells/dispel-magic/operational","SPELL_INTEGRATION_RULES.md#rank-limited-dispels-inspect-original-generating-rank"),rejected_dispensal);evs.append(ev)
    def prior_expire_ua_remains(s):
        a=s["actors"]["A"];a["concentration"]=None;a["effects"].pop("polymorph",None)
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","priorForm":"Polymorph expired at its own original endpoint",
            "suppressed":True,"UAexpires":66.1}
        a["body"]["type"]="Humanoid"
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"prior-form-expired-while-UA-operative","at":60.1,"UAexpires":66.1,"UAstillOperative":True,
            "formRefresh":False,"gearRestoredOnlyOnce":["A-focus","A-robe","A-book"],"externalFocusCustody":"A"});s["time"]=60.1
    ev,s5=event(s4,cid,10,"prior-form-original-expiry-UA-remains",60.1,{"PolymorphDeadline":60.1,"UAremainsUntil":66.1,"noRecast":True},refs4,prior_expire_ua_remains);evs.append(ev)
    def ua_natural_expire(s):
        a=s["actors"]["A"];a["effects"].pop("unholy-ascendance",None);a["form"]=None;a["body"]["type"]="Humanoid"
        a["lifecycle"]["operativeTargetingType"]="Humanoid"
        s["results"].append({"kind":"UA-natural-expiry","at":66.1,"UAexpiredAtOriginalDeadline":True,"baseBodyExpressed":"Humanoid","sameIdentity":"A-original-character-body",
            "noHealingFromExpiry":True,"gearCustody":"A","noDuplicateOrRecoveredLostGear":True});s["time"]=66.1
    ev,s6=event(s5,cid,11,"UA-natural-expiry-after-prior-form",66.1,{"UADeadline":66.1,"noClockRestart":True},refs4,ua_natural_expire);evs.append(ev)
    def legal_heal_after_natural_reversion(s):
        a=s["actors"]["A"];c=s["actors"]["C"];c["rp"]-=2;c["action"]=0;a["hp"]=72
        c["resourceHistory"].append({"ability":"healing-rite","target":"A","rpPaid":2,"actionPaid":True,"at":67.0,"roll":"4d8=17 + M5"})
        s["results"].append({"kind":"healing-rite-after-natural-UA-reversion","targetType":"Humanoid","eligibleLivingAlly":True,"healing":"S4d8(17)+M5=22",
            "hpBefore":50,"hpAfter":72,"woundsBefore":1,"woundsAfter":1,"RPpaid":2,"woundsRemoved":0});s["time"]=67.0
    ev,s7=event(s6,cid,12,"healing-rite-after-natural-reversion",67.0,{"source":"cleric.json#/cards/12","targetType":"Humanoid","cost":2,"healing":22},refs4,legal_heal_after_natural_reversion);evs.append(ev)
    def field_final_expiry(s):
        a=s["actors"]["A"];a["effects"]["antimagic-field"]["active"]=False;a["effects"]["antimagic-field"]["endedAt"]=68.1
        s["actors"]["T"]["concentration"]=None
        s["results"].append({"kind":"AMF-original-expiry","at":68.1,"durationSeconds":60,
            "allTransformationRecordsAlreadyExpired":True,"resumption":"none","noResourceRefresh":True,
            "custody":{"T-focus":"A","C-focus":"T"}});s["time"]=68.1
    ev,s8=event(s7,cid,13,"antimagic-field-original-expiry",68.1,{"expiresAt":68.1,"durationSeconds":60,
        "noSurvivingTransformationToResume":True},refs4,field_final_expiry);evs.append(ev)
    cases.append(case_record(cid,"Actual acquired and paid Polymorph R4 Humanoid is already operative before Unholy Ascendance. The original gear is melded; T transfers a real focus into A's custody before the UA cast.",s0,evs,
        ["UA activation does not reset or replace Polymorph concentration/deadline.","The accepted Antimagic field is paid/cast by a Wizard with an accessible C-focus; T-focus is in A's custody and mirrors are reconciled.",
         "During active suppression both transformations remain in their records, and A's original Polymorph-melded gear remains inaccessible until Polymorph genuinely expires.",
         "Rank3 Dispel Magic is rejected before commitment against rank9 UA; acquired Arch Dispel is handled in the separate early-removal case.",
         "Polymorph expires at60.1, UA at66.1, and the sixty-second field at68.1; no surviving record resumes and no clock/resource refresh occurs.",
         "Living-only Healing Rite is legal on the same character after natural UA reversion."],
        holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Prior form expiry while UA continues, and actual non-damage death are separate forks.
    cid="RANK9CASTINGCOST5-272-UA-PRIOR-EXPIRY"
    s0=base_state(50,a_pos=(0,0,0),t_pos=(5,0,0),add_cleric=True);a=s0["actors"]["A"]
    a["rp"]=47;a["concentration"]={"spellId":"polymorph","root":"POLY272-B","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","root":"POLY272-B","expires":60.1,"gearMelded":["A-focus","A-robe","A-book"]}}
    a["body"]["type"]="Undead";a["effects"]["unholy-ascendance"]={"start":6.1,"expires":66.1,"suppressed":False,"concentration":False,"pricePaid":26}
    a["effects"]["polymorph"]={"root":"POLY272-B","start":0.1,"expires":60.1,"suppressed":False,"suspendedByOverlay":True,"concentration":True}
    a["lifecycle"]["operativeTargetingType"]="Undead"
    for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
    a["resourceHistory"].extend([
        {"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1},
        {"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":6.1},
    ])
    a["interruptionHistory"].extend([
        {"spellId":"polymorph","at":0.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
        {"spellId":"unholy-ascendance","at":6.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
    ])
    s0["time"]=8.0;advance_calendar(s0,8.0);rebuild_cast_histories(s0)
    refs5=source_refs("catalog.json#/spells/735/operational","spell_form_profiles.json#/profiles/spellform.humanoid",
        "TRANSFORMATION_SPELL_PLAYTEST.md#Polymorph-and-Antimagic-suppression","UA270-LIFE spell-local prior-form suspension")
    evs=[];state=s0
    def expire_poly(s):
        a=s["actors"]["A"];a["concentration"]=None;a["effects"].pop("polymorph",None)
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","priorForm":"ended at its original endpoint"}
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"prior-form-expired-while-UA-operative","at":60.1,"UAexpires":66.1,"UAstillOperative":True,
            "formRefresh":False,"restoredOnlyOriginalGear":True,"custody":"A","duplicateOrRecoveredLostGear":False});s["time"]=60.1
    ev,state=event(state,cid,1,"prior-form-expires-UA-remains",60.1,{"PolymorphExpires":60.1,"UAExpires":66.1,"UAremains":True,"noRefresh":True},refs5,expire_poly);evs.append(ev)
    def expire_ua(s):
        a=s["actors"]["A"];a["effects"].pop("unholy-ascendance");a["form"]=None;a["body"]["type"]="Humanoid"
        s["results"].append({"kind":"UA-original-expiry","at":66.1,"sameBodyIdentity":True,"HP":50,"wounds":1,"gearCustody":"A","newLifeOrSoul":False});s["time"]=66.1
    ev,state=event(state,cid,2,"UA-original-expiry",66.1,{"UAExpires":66.1,"noClockReset":True},refs5,expire_ua);evs.append(ev)
    cases.append(case_record(cid,"Polymorph begins at0.1 and expires at60.1; UA begins at6.1 and expires at66.1. The prior form ends first while UA remains operative. Cleric C is a conditional level-20 Cultist fixture for the post-reversion Healing Rite.",s0,evs,
        ["The expired prior form is not recreated or refreshed; Unholy continues only to its own original end.","Original A gear is restored once with custody preserved."] ,holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    cid="RANK9CASTINGCOST5-272-UA-ACTUAL-DEATH"
    s0=base_state(90,a_rp=47,a_pos=(0,0,0),t_pos=(5,0,0));a,b=s0["actors"]["A"],s0["actors"]["T"]
    a["body"]["type"]="Undead";a["effects"]["unholy-ascendance"]={"start":6.1,"expires":66.1,"suppressed":False,"concentration":False,"pricePaid":26}
    a["concentration"]={"spellId":"polymorph","root":"POLY272-DEAD","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","expires":60.1}}
    a["equipment"]["focus"]={"id":"A-focus","custody":"A","accessible":False,"melded":True}
    refs6=source_refs("rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/PROCEDURES.json#/spells[id=power-word-kill]",
        "rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/DIRECTOR_DECISION.json#/acceptedIds/power-word-kill",
        "rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/CASE_INDEX.json#/power-word-kill",
        "ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
        "Transformation Polymorph death ends form/concentration")
    s0["time"]=8.0
    advance_calendar(s0,8.0); rebuild_cast_histories(s0)
    a["resourceHistory"].extend([
        {"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1},
        {"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":6.1},
    ])
    a["interruptionHistory"].extend([
        {"spellId":"polymorph","at":0.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
        {"spellId":"unholy-ascendance","at":6.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"},
    ])
    for key in ["focus","robe","spellbook"]:
        a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
    a["effects"]["polymorph"]={"root":"POLY272-DEAD","start":0.1,"expires":60.1,"suppressed":False,"suspendedByOverlay":True,"concentration":True}
    a["lifecycle"]["operativeTargetingType"]="Undead"
    t=s0["actors"]["T"]
    t["rp"]=80
    t["ordinaryLearningSource"]="ACTOR_PROFILES.json#/Wizard20/ordinaryLearning; conditional level-19 Power Word Kill replaces Bestow Curse at fixed selection count"
    def pwk(s):
        a=s["actors"]["A"];t=s["actors"]["T"];t["rp"]-=26;t["action"]=0
        t["resourceHistory"].append({"spellId":"power-word-kill","rank":9,"rpPaid":26,"actionPaid":True,
            "at":8.1,"prepared":True,"knownAtLevel":19,"source":"rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/PROCEDURES.json#/spells[id=power-word-kill]"})
        t["interruptionHistory"].append({"spellId":"power-word-kill","at":8.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        a["life"]="Dead";a["lifecycle"]["state"]="Dead";a["lifecycle"]["deathCause"]="non-damage Power Word Kill";a["lifecycle"]["deathAt"]=8.1
        a["concentration"]=None;a["form"]=None;a["effects"].pop("unholy-ascendance",None);a["effects"].pop("polymorph",None);a["body"]["type"]="Humanoid"
        a["lifecycle"].pop("nextDeathSaveAt",None);a["deathSaves"]={"failures":0,"successes":0}
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"actual-nondamage-death","spell":"power-word-kill","rank":9,"pricePaid":26,"actionPaid":True,
            "sourceProcedureAccepted":True,"sourceProcedureApplied":False,"target":"A-original-character-body","targetTypeAtResolution":"Living",
            "targetHP":90,"threshold":100,"perceived":True,"withinNative120Feet":True,"lineOfEffect":True,"damage":0,
            "A":{"life":"Dead","HP":90,"bodyIdentity":"A-original-character-body","UA":"ended","PolymorphConcentration":"ended","revived":False,"soulOrHuntRule":"not inferred"},
            "gear":{"restoredOnly":["A-focus","A-robe","A-book"],"custody":"A","duplicated":False,"lostGearRecovered":False}});s["time"]=8.1
    ev,state=event(s0,cid,1,"power-word-kill-actual-death",8.1,{"caster":"T","spellId":"power-word-kill","rank":9,"RP":26,
        "sourceAcceptedUnapplied":True,"TLevel20WizardKnownPreparedAt19":True,"targetType":"Living","targetHP":90,"threshold":100,
        "within120Feet":True,"perceived":True,"nonDamage":True,"UAandpriorFormEnd":True},refs6,pwk)
    cases.append(case_record(cid,"Independent non-damage death fork with A at90HP; no qualifying Null damage is involved and no protection is stipulated. It closes only UA/form lifecycle; no soul, Hunt, or revival conclusion is imported.",s0,[ev],
        ["Actual death ends UA and the live prior-form concentration record.","Character/body identity stays A; HP is not reassigned by form expiry; original surviving items restore exactly once with unchanged custody."],
        holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Source-grounded early removal: acquired Arcane Sight supports perception; acquired Wizard Arch Dispel ends only UA.
    cid="RANK9CASTINGCOST5-272-UA-EARLY-ARCH-DISPEL"
    s0=base_state(50,a_rp=80,t_rp=80,a_pos=(0,0,0),t_pos=(5,0,0),add_cleric=True);a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    s0["time"]=0.0
    refs8=source_refs("ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
        "wizard.json#/cards/19","wizard.json#/cards/21",
        "ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/2/choices/1",
        "ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/8/choices/0",
        "catalog.json#/spells/735/operational","rank8ward5_reviewed_149/DIRECTOR_RETURN/PROCEDURES/antimagic-field.json#/procedure")
    evs=[]
    def cast_poly(s):
        a=s["actors"]["A"];a["rp"]-=7;a["action"]=0
        a["concentration"]={"spellId":"polymorph","root":"POLY272-EARLY","start":0.1,"expires":60.1,"concentration":True,"rank":4,"pricePaid":7}
        a["effects"]["polymorph"]={"root":"POLY272-EARLY","start":0.1,"expires":60.1,"suppressed":False,"concentration":True}
        a["form"]={"id":"polymorph","profile":"spellform.humanoid","root":"POLY272-EARLY","bodyIdentity":"A-original-character-body",
            "physicalExpression":"Humanoid-form","start":0.1,"expires":60.1,"gearMelded":["A-focus","A-robe","A-book"]}
        a["body"].update({"type":"Humanoid","hands":2,"speech":True})
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
        a["resourceHistory"].append({"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1})
        a["interruptionHistory"].append({"spellId":"polymorph","at":0.1,"windowOpened":True,"eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        s["time"]=0.1
    ev,state=event(s0,cid,1,"cast-polymorph-before-ua",0.1,{"spellId":"polymorph","rank":4,"RP":7,"Action":True,
        "profile":"spellform.humanoid","concentrationDeadline":60.1,"originalGearMelded":True},refs8,cast_poly);evs.append(ev)
    def cast_sight(s):
        t=s["actors"]["T"];t["rp"]-=2;t["action"]=0
        t["concentration"]={"ability":"arcane-sight","start":0.2,"expires":600.2,"concentration":True,"source":"wizard.json#/cards/21"}
        t["effects"]["arcane-sight"]={"start":0.2,"expires":600.2,"radius":60,"perceivesMagicalAuras":True}
        t["resourceHistory"].append({"ability":"arcane-sight","source":"wizard.json#/cards/21","rpPaid":2,"actionPaid":True,"at":0.2})
        t["interruptionHistory"].append({"ability":"arcane-sight","at":0.2,"windowOpened":False,"reason":"active Wizard feature; not a spell cast"})
        s["time"]=0.2
    ev,state=event(state,cid,2,"activate-acquired-arcane-sight",0.2,{"ability":"wizard.arch.arcane-sight","RP":2,"Action":True,
        "durationSeconds":600,"concentrationDeadline":600.2,"rangeFeet":60},refs8,cast_sight);evs.append(ev)
    def transfer_t_focus(s):
        s["objects"]["T-focus"]["custody"]="A"
        s["objects"]["T-focus"]["transferHistory"]=[{"from":"T","to":"A","at":5.9,"lawfulExternalTransfer":True}]
        s["actors"]["A"]["equipment"]["externalFocus"]={"id":"T-focus","owner":"T","custody":"A","accessible":True,"held":True}
        s["actors"]["T"]["equipment"]["focus"]={"id":None,"custody":"T","accessible":False,"melded":False}
        s["time"]=5.9
    ev,state=event(state,cid,3,"external-focus-transfer-to-A",5.9,{"item":"T-focus","custody":"T->A","AHasAccessibleFocusForUA":True},refs8,transfer_t_focus);evs.append(ev)
    def transfer_c_focus(s):
        s["objects"]["C-focus"]["custody"]="T"
        s["objects"]["C-focus"]["transferHistory"]=[{"from":"C","to":"T","at":5.95,"lawfulExternalTransfer":True}]
        s["actors"]["C"]["equipment"].pop("focus",None)
        s["actors"]["T"]["equipment"]["focus"]={"id":"C-focus","owner":"C","custody":"T","accessible":True,"held":True}
        s["time"]=5.95
    ev,state=event(state,cid,4,"alternate-focus-transfer-to-T",5.95,{"item":"C-focus","custody":"C->T","THasAccessibleFocusForArchDispel":True},refs8,transfer_c_focus);evs.append(ev)
    def ua_cast(s):
        a=s["actors"]["A"];activate_ua(s,6.1)
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph",
            "root":"POLY272-EARLY","expires":60.1,"concentration":True,"gearMelded":["A-focus","A-robe","A-book"]}}
        s["time"]=6.1
    ev,state=event(state,cid,5,"cast-ua-while-poly-operative",6.1,{"spellId":"unholy-ascendance","rank":9,"RP":26,"Action":True,
        "accessibleComponentFocus":"T-focus transferred into A custody at5.9","PolymorphConcentrationStillEndsAt":60.1,"UAExpires":66.1,
        "identity":"A-original-character-body"},refs8,ua_cast);evs.append(ev)
    def perceive_ua(s):
        t=s["actors"]["T"];t["action"]=0
        t["effects"]["arcane-sight"]["examinedAt"]=8.1
        t["perceptionHistory"]=[{"at":8.1,"source":"wizard.json#/cards/21","observedCastAt":6.1,
            "effectRoot":"UA272-A-cast","spellId":"unholy-ascendance","ongoing":True,"within60Feet":True,
            "lineOfSight":True,"casterIdentity":"A-original-character-body"}]
        t["resourceHistory"].append({"ability":"arcane-sight-examine","source":"wizard.json#/cards/21","actionPaid":True,"at":8.1})
        s["time"]=8.1
    ev,state=event(state,cid,6,"examine-perceived-ua-aura",8.1,{"actor":"T","Action":True,"arcaneSightActive":True,
        "UASeenCastAt":6.1,"ongoingEffectSelected":"UA272-A-cast","within60Feet":True,"lineOfSight":True},refs8,perceive_ua);evs.append(ev)
    def arch_dispel(s):
        a=s["actors"]["A"];t=s["actors"]["T"];t["rp"]-=3;t["action"]=0
        t["resourceHistory"].append({"spellId":"dispel-magic","rank":3,"feature":"wizard.arch.dispel-magic","source":"wizard.json#/cards/19",
            "rpPaid":3,"actionPaid":True,"at":14.1,"spellEfficiencyApplied":False})
        t["interruptionHistory"].append({"spellId":"dispel-magic","at":14.1,"windowOpened":True,
            "eligibleCounterspellers":[],"reactionsSpent":0,"result":"no interruption attempt"})
        a["effects"].pop("unholy-ascendance",None);a["body"]["type"]="Humanoid";a["lifecycle"]["operativeTargetingType"]="Humanoid"
        a["form"]={"id":"polymorph","profile":"spellform.humanoid","root":"POLY272-EARLY","bodyIdentity":"A-original-character-body",
            "physicalExpression":"resumed-original-prior-form","start":0.1,"expires":60.1,"concentrationRoot":"POLY272-EARLY",
            "sameConcentrationRecord":True,"gearMelded":["A-focus","A-robe","A-book"]}
        a["effects"]["polymorph"]={"root":"POLY272-EARLY","start":0.1,"expires":60.1,"suppressed":False,"concentration":True}
        a["concentration"]={"spellId":"polymorph","root":"POLY272-EARLY","start":0.1,"expires":60.1,"concentration":True,"rank":4,"pricePaid":7}
        s["results"].append({"kind":"early-removal-by-acquired-wizard-arch-dispel","caster":"T","target":"UA272-A-cast",
            "feature":"wizard.arch.dispel-magic","rank":3,"pricePaid":3,"actionPaid":True,"roll":"d20=13 + INT5 + PB6 =24 vs DC19",
            "success":True,"effectChosen":"one actually perceived ongoing spell: UA only","UAendedAt":14.1,
            "survivingPriorForm":{"spellId":"polymorph","root":"POLY272-EARLY","deadline":60.1,"sameConcentrationRecord":True},
            "A":{"bodyIdentity":"A-original-character-body","hp":50,"rp":47,"wounds":1,"concentrationUnchanged":True,
                "gear":{"custody":"A","accessible":False,"melded":True}},
            "noRefresh":{"HP":True,"resources":True,"concentration":True,"equipment":True,"clock":True}})
        s["time"]=14.1
    ev,state=event(state,cid,7,"arch-dispel-removes-only-ua-and-resumes-poly",14.1,{"caster":"T","acquiredFeature":"wizard.arch.dispel-magic",
        "action":True,"RP":3,"componentFocus":"C-focus transferred C->T at5.95","rangeFeet":60,"check":"d20=13 + INT5 + PB6 =24 vs DC19","targetRank":9,
        "targetActuallyPerceived":True,"effectEnded":"UA only","polymorphOriginalDeadline":60.1},refs8,arch_dispel);evs.append(ev)
    cases.append(case_record(cid,"T is a conditional Wizard20 fixture with source-acquired Arcane Sight and Wizard Arch Dispel. A casts Polymorph at0.1 and Unholy Ascendance at6.1 using a lawfully transferred focus; T receives a second real focus before dispelling. T observes the cast, uses Arcane Sight to perceive ongoing UA, and at T's14.1 turn successfully ends only UA. The same Polymorph concentration/root, deadline and melded gear resume without refresh.",s0,evs,
        ["The acquired Wizard Arch Dispel is Action/3RP/range60/recharge2; INT+PB24 beats DC19 for actual rank9 UA.",
         "Only the selected perceived UA root ends. The same Polymorph record resumes at its original deadline60.1.",
         "A's HP, RP, Wounds, concentration, original melded gear, equipment custody and all original clocks are unchanged by removal."],
        holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))
    return cases


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_candidate = read_json(SRC270 / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json")
    delivery = read_json(SRC270 / "DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json")
    assert source_candidate["currentAuthority"] == {"reviewedApplied":815,"pending":33,"acceptedUnapplied":0,
        "completeStandaloneProcedures":539,"scopedInterfaces":173}
    assert len(source_candidate["sourceBindings"]) == 117
    procedure_path=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_222_final/procedures/unholy-ascendance.json"
    procedure=read_json(procedure_path)
    assert procedure["accepted"] is False and procedure["applied"] is False and procedure["blockerIds"] == ["CC194-B04"]
    procedure=copy.deepcopy(procedure)
    procedure["reviewVersion"]="Return272 / UA270-LIFE + UA270-HEAL witness supplement"
    procedure["sourceAuthority"]=source_candidate["currentAuthority"]
    procedure["sourcePacket"]=file_binding(SRC270/"DD_Rank9_CastingCost5_CurrentSource_270.zip")
    procedure["commonProcedureScope"]="Only unholy-ascendance / CC194-B04 is reviewed here. Perfect Spell, other wrappers, and already-applied identities are dependency context and are outside this packet's decision scope."
    procedure["reviewScope"]={"target":"unholy-ascendance","questionId":"CC194-B04","decisionScope":"target only",
        "perfectSpell":"context only; not reviewed or reopened","otherIdentities":"not reviewed or decided"}
    procedure["sourceBinding"]="SOURCE_BINDING.json"
    procedure["caseIndex"]="case-index/CC194-B04-RETURN272.json"
    procedure["provenance"]["currentNativePointer"]="/spells/673"
    procedure["provenance"]["currentBackingHashes"]="SOURCE_BINDING.json"
    procedure["procedure"] += ("\n\nNEW spell-local UA270-LIFE (explicitly authorized by GPT in Return270; proposal only, not source-recovered): preserve one original character/body identity and all HP/maxHP/Wounds/injuries/death counters/resources/equipment. Operative targeting type is Undead, so living-only targets fail. Ordinary damage follows that character's Core/Healing damage, Wound and death-save procedures through this adapter. No automatic destruction, immunity, separate HP or special zero-HP action. For this recipient only, a qualifying same-dealer Null root suppresses damage-caused Instant Death, Wound/Maiming saves and damage-caused death failures. New positive-to-zero becomes Stable0 with cleared counters and one stipulated d4-hour recovery deadline; already-Dying0/Stable0 preserves current counters/schedule/deadline. Zero HP causes ordinary unconsciousness; it does not end the nonconcentration UA overlay. Actual death ends UA; original expiry and independent removal remain. Suppression returns the legally expressed underlying type/body while all original clocks continue. Each later event snapshots then-current state; reversion never resurrects. Scope is Unholy Ascendance only.\n\nNEW spell-local UA270-HEAL (explicitly authorized by GPT in Return270; proposal only): while UA is operative, the continuing caster may receive its own already-accepted Vampiric Touch self-heal. Preserve Action/Touch/V/S/F, one attack, actual damage and floor(actualDamageDealt/2). The UA waiver changes only eligible casting payment; suppressed/reverted casts use ordinary quote. No new spell, unconscious casting or generic Undead healing. Preserve all existing CC194-H qualifications and downstream gates.")

    cases=create_cases()
    for c in cases: dump_json(OUT/f"cases/{c['id']}.json",c)
    case_index={"id":"CC194-B04-RETURN272-CASE-INDEX","target":TARGET,"questionId":"CC194-B04",
        "status":"CONDITIONAL_STATIC_WITNESSES","caseCount":len(cases),
        "cases":[{"caseId":c["id"],"member":f"cases/{c['id']}.json","eventCount":len(c["events"]),
                  "finalSHA256":c["finalSHA256"],"status":c["status"]} for c in cases]}
    dump_json(OUT/"case-index/CC194-B04-RETURN272.json",case_index)
    procedure["caseIds"]=[c["id"] for c in cases]
    dump_json(OUT/"procedures/unholy-ascendance.json",procedure)
    # Include the exact prior held packet, current-source bindings and relevant current source rows.
    previous = {"path":"evidence/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",**file_binding(OLD)}
    dump_json(OUT/"evidence/CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json",source_candidate)
    dump_json(OUT/"evidence/DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json",delivery)
    dump_json(OUT/"evidence/PRIOR_RETURN240_BINDING.json",previous)
    source_paths=[
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_194/ACTOR_PROFILES.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
      "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
      "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json",
      "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
      "DescentReviewChanges/ReviewBible/data/playtest/spell_form_profiles.json",
      "DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_relic_null_reviewed_01.json",
      "DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8ward5_reviewed_149/DIRECTOR_RETURN/PROCEDURES/antimagic-field.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8ward5_reviewed_149/DIRECTOR_RETURN/DIRECTOR_DECISION.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8ward5_reviewed_149/DIRECTOR_RETURN/MODEL.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/PROCEDURES.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/DIRECTOR_DECISION.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery7_reviewed_184/DIRECTOR_RETURN/CASE_INDEX.json",
    ]
    direct_bindings=[]
    for source_no,rel in enumerate(source_paths,1):
        src=ROOT/rel
        assert src.is_file(), f"missing bound source: {src}"
        archive_member=f"evidence/src/{source_no:02d}-{src.name}"
        dest=OUT/archive_member
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(src.read_bytes())
        binding=file_binding(src,rel)
        binding["archiveMember"]=archive_member
        direct_bindings.append(binding)
    accepted_archives=[
      (BASE/"rank8ward5_return149_received/DD_Rank8_Ward5_Director_Return149.zip",["cases/RW149-X__antimagic-field.json"]),
      (BASE/"rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184.zip",[
        "cases/DR184-POWER-WORD-KILL-A-QUALIFYING-THRESHOLD.json",
        "cases/DR184-POWER-WORD-KILL-ACTUAL-ANTIMAGIC-RECIPIENT-SUPPRESSION.json"]),
    ]
    archive_case_bindings=[]
    for archive_path,names in accepted_archives:
        assert archive_path.is_file(), f"missing accepted source archive: {archive_path}"
        with zipfile.ZipFile(archive_path) as srczip:
            for member_name in names:
                raw=srczip.read(member_name)
                safe=member_name.replace("/","__")
                archive_member=f"evidence/accepted/{safe}"
                dest=OUT/archive_member;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
                import zlib
                archive_case_bindings.append({"sourceArchive":file_binding(archive_path),"sourceMember":member_name,
                    "archiveMember":archive_member,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                    "crc32":f"{zlib.crc32(raw)&0xffffffff:08x}"})
    source_binding={"id":"RETURN272-SOURCE-BINDING","target":TARGET,"questionId":"CC194-B04",
        "sourceAuthority":source_candidate["currentAuthority"],"current117Bindings":source_candidate["sourceBindings"],
        "currentSourceCandidate":file_binding(SRC270/"CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json"),
        "currentSourceDelivery":file_binding(SRC270/"DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json"),
        "priorReturn240":previous,"directSources":direct_bindings,"acceptedSourceArchiveCases":archive_case_bindings,
        "notes":["Direct source bytes are embedded under evidence/sources and mapped by archiveMember.",
            "Accepted AMF and Power Word Kill case members are extracted byte-for-byte from the named accepted source archives.",
            "AMF and PWK acceptance dispositions remain accepted/unapplied as stated in their attached director decisions.",
            "This packet does not change canonical procedure, index, catalog or queue files."]}
    dump_json(OUT/"SOURCE_BINDING.json",source_binding)
    procedure["sourceBinding"]="SOURCE_BINDING.json"
    procedure["caseIndex"]="case-index/CC194-B04-RETURN272.json"
    dump_json(OUT/"procedures/unholy-ascendance.json",procedure)
    excerpt={"status":"SOURCE_BOUND_CONDITIONAL_WITNESSES","sourceSnapshot":source_candidate["sourceSnapshot"],
             "currentAuthority":source_candidate["currentAuthority"],"current117SourceBindings":source_candidate["sourceBindings"],
             "sourceFiles":direct_bindings,"acceptedSourceArchiveCases":archive_case_bindings,
             "rootSourceBinding":"SOURCE_BINDING.json",
             "notes":["Exact source bytes are embedded under evidence/sources and indexed in SOURCE_BINDING.json.",
                 "The full Return270 current-source ZIP remains attached in the GPT conversation.",
                 "No canonical procedure/index/catalog/queue file is changed here."]}
    dump_json(OUT/"evidence/SOURCE_AND_AUTHORITY_BINDINGS.json",excerpt)
    authorization=("# GPT Return270 authorization\n\n"
      "GPT explicitly authorized the new spell-local proposal UA270-LIFE and UA270-HEAL for witness construction only. It did not accept or apply Unholy Ascendance.\n\n"
      "UA270-LIFE: preserve one original character/body identity, HP/maxHP/Wounds/injuries/death counters/resources/equipment; operative targeting type Undead; ordinary damage uses the character's Core/Healing lifecycle; no automatic destruction, immortality, separate HP or special zero-HP action; same-dealer qualifying Null suppresses this recipient's damage-caused instant death/Wound/death failures; new positive-to-zero becomes Stable0 with cleared counters and one stipulated d4-hour deadline; already-Dying0/Stable0 preserves applicable counters/schedule/deadline; zero HP unconsciousness does not end nonconcentration UA; actual death ends UA; suppression restores legally expressed underlying form with original clocks; no resurrection; spell-local scope only.\n\n"
      "UA270-HEAL: the continuing caster may receive its own already-accepted Vampiric Touch self-heal while UA operates; retain one attack and floor(actualDamageDealt/2); UA changes eligible payment only. Suppressed/reverted cast uses ordinary quote. No unconscious casting or generic Undead healing.\n")
    (OUT/"evidence/GPT_RETURN270_AUTHORIZATION.md").write_text(authorization,encoding="utf-8",newline="\n")
    blocker=("# Return272 early-UA-removal source route\n\n"
      "The early-removal source gap is resolved by an existing acquired route; no new UA-local dismissal is proposed. The conditional Wizard20 fixture acquires Wizard Arch Dispel from `ACTOR_PROFILES.json#/Wizard20/acquisitionLedger/8/choices/0` and Arcane Sight from `.../acquisitionLedger/2/choices/1`. The exact card bytes are embedded in `SOURCE_BINDING.json`.\n\n"
      "At14.1, T spends the card's Action and3RP, selects only the actually perceived ongoing rank9 UA root, and succeeds on INT+PB: d20 13 + 11 =24 vs DC19. The same Polymorph root, concentration and60.1 endpoint resume; A's HP, resources, melded gear, custody and clocks do not refresh. Rank3 ordinary Dispel remains correctly rejected before commitment; the successful route is the separate acquired Arch Dispel card.\n")
    (OUT/"evidence/EARLY_REMOVAL_ROUTE.md").write_text(blocker,encoding="utf-8",newline="\n")
    readme=("# Return272 — Unholy Ascendance integrated lifecycle witnesses\n\n"
      "Target: unholy-ascendance / CC194-B04 only. Authority at source packet 270: 815 applied / 33 pending / 0 accepted-unapplied; 539 complete procedures / 173 scoped interfaces.\n\n"
      "The new cases are conditional static traces, not runtime/playtest claims. They are built under GPT's explicit spell-local UA270-LIFE and UA270-HEAL authorship. Existing Return240 cases and source qualifications are preserved in the bound historical archive. No acceptance/application is recorded.\n\n"
      "The source-grounded early-removal route now uses the acquired Wizard Arch Dispel with Arcane Sight perception and resumes the unchanged prior Polymorph record. Exact accepted Antimagic and Power Word Kill procedures, decisions and representative accepted cases are bound byte-for-byte in SOURCE_BINDING.json. The packet includes ten new conditional static traces and makes no acceptance/application claim.\n\n"
      "Review request: independently verify the complete current source binding and the integrated new cases, then issue explicit ACCEPT or HOLD for Unholy Ascendance only. If held, identify exact remaining defects. If accepted, leave unapplied and report counts plus next priority (GPT previously named mind-collapse / MD196-B01). Do not decide another identity.\n")
    (OUT/"README.md").write_text(readme,encoding="utf-8",newline="\n")
    request=("Return272 is attached with the current-source 270 binding, the preserved Return240 history, and ten new reversible static witness traces. Please act as director for unholy-ascendance / CC194-B04 only. Independently verify source integrity, the authorized UA270-LIFE/UA270-HEAL boundaries, and the traces.\n\n"
      "The cases cover: matched ordinary versus same-dealer CH07 Null positive-to-zero; actual field exposure, failed save, dealer-at-root binding; defenses/tempHP/post-temp damage/HP/Wound/death/recovery snapshots; already-Dying0 and already-Stable0 clocks; acquired and paid Ritual of Undeath protection; living-only Healing Rite and Vampiric Touch outcomes across operative, suppressed and reverted states; paid Polymorph with equipment custody and Antimagic suppression; original deadlines, prior-form expiry, source-grounded early Arch Dispel removal/resumption, and independent Power Word Kill death. Exact actor/form profile bytes and accepted Antimagic/Power Word Kill procedures, decisions and case evidence are embedded and indexed by SOURCE_BINDING.json.\n\n"
      "Please independently verify Return272 and issue an explicit final ACCEPT or HOLD for unholy-ascendance / CC194-B04 only. If held, identify the exact remaining defects and minimum correction. If accepted, confirm accepted=true but applied=false, current authority counts, and next identity priority. Preserve CC194-H01-H08, all distinctions and downstream gates. Do not accept/apply another identity.")
    (OUT/"REQUEST_272.txt").write_text(request,encoding="utf-8",newline="\n")
    # Deterministic allowlist and member hashes.
    members=[]
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name not in {"DELIVERY_272.json","INDEPENDENT_AUDIT_272.json"}:
            members.append({"name":p.relative_to(OUT).as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    archive=BASE/"DD_Rank9_UnholyAscendance_Director_Return272.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for m in members: z.write(OUT/m["name"],m["name"])
    archive_binding=file_binding(archive,archive.relative_to(ROOT).as_posix())
    delivery272={"id":"DD_Rank9_UnholyAscendance_Director_Return272_DELIVERY","status":"PREPARED_FOR_DIRECTOR_REVIEW",
        "archive":archive_binding,"memberCount":len(members),"payloadMemberCount":len(members),"members":members,
        "currentSourceDelivery":file_binding(SRC270/"DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json"),
        "currentAuthority":source_candidate["currentAuthority"],"spellId":TARGET,"blockerIds":["CC194-B04"],"accepted":False,"applied":False}
    dump_json(BASE/"DD_Rank9_UnholyAscendance_Director_Return272_DELIVERY.json",delivery272)

    # Independent package/trace audit, including forward+inverse replay and semantic scope checks.
    checks=[]
    def check(name,ok,detail=""):
        checks.append({"check":name,"passed":bool(ok),"detail":detail})
    check("current authority 815/33/0; 539/173",source_candidate["currentAuthority"]=={"reviewedApplied":815,"pending":33,"acceptedUnapplied":0,"completeStandaloneProcedures":539,"scopedInterfaces":173})
    check("117 refreshed current source bindings",len(source_candidate["sourceBindings"])==117)
    check("target remains unapplied in proposal",procedure["accepted"] is False and procedure["applied"] is False and procedure["blockerIds"]==["CC194-B04"])
    check("new case count 10",len(cases)==10)
    check("case identities unique",len({c["id"] for c in cases})==len(cases))
    for c in cases:
        cur=copy.deepcopy(c["initialState"])
        for i,e in enumerate(c["events"]):
            ok=(sha(cur)==e["beforeSHA256"] and sha(e["after"])==e["afterSHA256"] and e["before"]==cur and
                e["forward"][0]=={"op":"test","path":"","value":cur} and e["forward"][1]=={"op":"replace","path":"","value":e["after"]} and
                e["inverse"][0]=={"op":"test","path":"","value":e["after"]} and e["inverse"][1]=={"op":"replace","path":"","value":cur})
            check(f"{c['id']} event {i+1} chained forward/inverse",ok)
            cur=copy.deepcopy(e["after"])
        check(f"{c['id']} final replay/hash",cur==c["finalState"] and sha(cur)==c["finalSHA256"])
    semantics={
      "UA same identity and life clock":any("A-original-character-body" in str(c) and "UA270-LIFE" in str(c) for c in cases),
      "same-dealer Null root":any("nullNonlethal" in str(c) and "dealerSnapshot" in str(c) for c in cases),
      "new zero stable recovery deadline":any("Stable0" in str(c) and "stableRecoveryDeadline" in str(c) for c in cases),
      "existing zero counters and schedule preserved":any("already-dying0" in c["id"].lower() or "WOULD-DIE" in c["id"] for c in cases),
      "Cleric would-die ward untriggered Null":any("NULL-WOULD-DIE" in c["id"] and "wardTriggerAvailable" in str(c) and "triggered': False" in str(c) for c in cases),
      "healing preflight and UA270-HEAL":any("vampiric-touch" in str(c) and "preflight-rejection" in str(c) for c in cases),
      "antimagic suppression resumption and unchanged deadlines":any("antimagic-field-suppression" in str(c) and "noClockRestart" in str(c) for c in cases),
      "exact equipment custody and no duplication":any("noGearDuplication" in str(c) or "duplicated" in str(c) for c in cases),
      "prior form expires while UA continues":any("prior-form-expired-while-UA-operative" in str(c) for c in cases),
      "distinct non-damage actual death":any("actual-nondamage-death" in str(c) for c in cases),
      "acquired Arch Dispel early-removal and prior-form resumption witnessed":any("EARLY-ARCH-DISPEL" in c["id"] and "POLY272-EARLY" in str(c) and "early-removal-by-acquired-wizard-arch-dispel" in str(c) for c in cases),
      "accepted suppression and direct-death sources bound":len(archive_case_bindings)==3 and any("antimagic-field.json" in x["path"] for x in direct_bindings) and any("PROCEDURES.json" in x["path"] and "deathrecovery7" in x["path"] for x in direct_bindings),
      "procedure authority, scope, source binding and case index reconciled":procedure["sourceAuthority"]==source_candidate["currentAuthority"] and procedure["commonProcedureScope"].startswith("Only unholy-ascendance") and procedure["sourceBinding"]=="SOURCE_BINDING.json" and procedure["caseIndex"]=="case-index/CC194-B04-RETURN272.json" and len(procedure["caseIds"])==len(cases),
      "delivery counts every listed payload member":delivery272["payloadMemberCount"]==len(delivery272["members"]) and delivery272["memberCount"]==len(delivery272["members"]),
    }
    for k,v in semantics.items():check("semantic coverage: "+k,v)
    with zipfile.ZipFile(archive) as z:
        zin=sorted(z.namelist()); expected=sorted(m["name"] for m in members)
        check("archive exact member allowlist",zin==expected)
        for m in members:
            data=z.read(m["name"])
            check("member hash: "+m["name"],hashlib.sha256(data).hexdigest()==m["sha256"])
    failures=[x for x in checks if not x["passed"]]
    audit={"id":"RANK9_CASTINGCOST5_RETURN272_INDEPENDENT_AUDIT","status":"PASS_PACKAGE_BINDING_AND_REPLAY" if not failures else "FAIL",
        "checkCount":len(checks),"checksPassed":len(checks)-len(failures),"checksFailed":len(failures),"checks":checks,"failures":failures,
        "archive":archive_binding,"caseCount":len(cases),"eventCount":sum(len(c["events"]) for c in cases),
        "forwardInverseOperationCount":2*sum(len(c["events"]) for c in cases),"sourceBindingCount":len(source_candidate["sourceBindings"]),
        "authority":source_candidate["currentAuthority"],"acceptedIds":[],"appliedIds":[],"heldIds":[TARGET]}
    dump_json(BASE/"RANK9_CASTINGCOST5_RETURN272_INDEPENDENT_AUDIT.json",audit)
    assert not failures, json.dumps(failures,indent=2)
    print(json.dumps({"status":audit["status"],"checkCount":audit["checkCount"],"caseCount":audit["caseCount"],"eventCount":audit["eventCount"],
                      "archive":archive_binding,"delivery":file_binding(BASE/"DD_Rank9_UnholyAscendance_Director_Return272_DELIVERY.json")},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
