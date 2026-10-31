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
OUT = BASE / "rank9_castingcost5_return271_prepared"
CASE_SOURCE = OLD
TARGET = "unholy-ascendance"


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
        "catalog.json#/spells/630/operational",
        "spell_form_profiles.json#/profiles/spellform.humanoid",
    ]
    return base + list(extra)


def event(state: dict, case_id: str, index: int, kind: str, at: float, detail: dict,
          refs: list[str], mutate) -> tuple[dict, dict]:
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    mutate(after)
    after["time"] = at
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
        for spell in ["polymorph", "vampiric-touch", "dispel-magic", "power-word-kill"]:
            if spell not in actor["prepared"]:
                actor["prepared"].append(spell)
            if not any(x.get("spellId") == spell for x in actor["everKnown"]):
                actor["everKnown"].append({"kind": "conditional-Wizard20-level-learning",
                    "source": "current catalog classAccess + ACTOR_PROFILES.json#/Wizard20/ordinaryLearning",
                    "spellId": spell})
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
        c.update({"id": "C", "profile": "CC194-C20-CULTIST-CONDITIONAL", "class": "Cleric", "level": 20,
                  "rp": 58, "maxRP": 58, "conviction": 7, "maxConviction": 7,
                  "position": [5, 0, 0], "prepared": ["healing-rite", "ritual-of-undeath"],
                  "reviewStats": {"S": 4, "M": 5, "PB": 6, "WIS": 20, "spellAttack": 11,
                                  "profileSource": "Cleric20 stats, conditional level-16 Cultist selection"},
                  "everKnown": [{"kind": "conditional-selection", "source": "cleric.json#/cards/12", "spellId": "healing-rite"},
                                {"kind": "conditional-level-16-Cultist-selection", "source": "cleric.json#/cards/57", "spellId": "ritual-of-undeath"}],
                  "resourceHistory": [], "effects": {}, "conditions": {}, "deathSaves": {"failures": 0, "successes": 0}})
        state["actors"]["C"] = c
        state["objects"]["C-conditional-profile"] = {"class": "Cleric", "classLevel": 20, "heroPath": "Cultist",
            "stats": {"S": 4, "M": 5, "PB": 6, "WIS": 20, "spellAttack": 11, "rpMaximum": 58, "convictionMaximum": 7},
            "selectedAtLevel16": {"id": "cleric.hero.cultist.ritual-of-undeath", "source": "cleric.json#/cards/57"},
            "qualification": "A conditional authored fixture; not a claim about a campaign character."}
    return state


def activate_ua(s: dict, at: float) -> None:
    a = s["actors"]["A"]
    a["rp"] -= 26
    a["action"] = max(0, a["action"] - 1)
    a["effects"]["unholy-ascendance"] = {"root": "UA271-A-cast", "start": at, "expires": at + 60.0,
                                           "suppressed": False, "concentration": False, "rank": 9, "pricePaid": 26}
    a["body"]["type"] = "Undead"
    a["form"] = {"id": "UA270-LIFE", "bodyIdentity": "A-original-character-body", "sameHPTrack": True}
    a["lifecycle"]["operativeTargetingType"] = "Undead"
    a["resourceHistory"].append({"spellId": "unholy-ascendance", "rank": 9, "rpPaid": 26, "actionPaid": True, "at": at})


def case_record(case_id: str, premise: str, state: dict, events: list[dict], assertions: list[str],
                status: str = "DEMONSTRATED_STATIC_TRACE", holds: list[str] | None = None) -> dict:
    final = copy.deepcopy(events[-1]["after"] if events else state)
    return {"id": case_id, "mainCaseId": case_id, "kind": "spell-review", "spellId": TARGET,
            "premise": premise, "questionIds": ["CC194-B04"], "holdIds": holds or [],
            "status": status, "runtimeExecuted": False, "assertions": assertions,
            "initialState": copy.deepcopy(state), "events": events, "finalState": final,
            "finalSHA256": sha(final)}


def create_cases() -> list[dict]:
    refs = source_refs("inflict-wounds:Wizard rank1, Action, 2RP, V/S/F, 3d10 necrotic, melee spell attack",
                      "CH07:NULL-FIELD-QUIET-WELL-1", "CORE:WIS save DC15/hourly field exposure")
    cases: list[dict] = []

    # Matched ordinary and Null positive-to-zero forks use the same complete A/T profile.
    for case_no, null in [(12, False), (13, True)]:
        cid = f"RANK9CASTINGCOST5-271-UA-{'NULL' if null else 'ORDINARY'}-NEWZERO"
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
            s["results"].append({"kind": "damage-root", "id": f"{cid}/root1", "dealer": "T", "nullNonlethal": bool(null),
                "dealerSnapshot": {"nullVeilUnsuppressed": bool(null), "fieldId": "NULL-FIELD-QUIET-WELL-1" if null else None},
                "recipientSnapshot": {"identity": "A-original-character-body", "type": "Undead", "life": "Living", "hp": 7,
                    "maxHP": 122, "tempHP": 5, "wounds": 1, "deathSaveFailures": 0, "recoveryDeadline": None}})
            s["time"] = cast_at+0.1
        ev, cur = event(cur, cid, len(evs)+1, "damage-root-created", cast_at+0.1,
            {"dealer": "T", "spellId": "inflict-wounds", "rank": 1, "rootFlag": bool(null),
             "rootFlagSnapshot": "same actual damaging character T; controller-independent"}, refs, root)
        evs.append(ev)
        def damage(s):
            a, t = s["actors"]["A"], s["actors"]["T"]
            t["rp"] -= 2
            t["action"] = 0
            t["resourceHistory"].append({"spellId": "inflict-wounds", "rank": 1, "rpPaid": 2, "at": cast_at+0.12})
            before = {"hp": 7, "tempHP": 5, "wounds": 1, "deathSaveFailures": 0, "life": "Living", "type": "Undead"}
            after_damage = {"attack": "d20=3 + 11 = 14 vs AC12", "damageRoll": "3d10=24 necrotic", "allResistance": "floor(24/2)=12",
                            "tempAbsorbed": 5, "postTempDamage": 7, "actualHPLoss": 7, "resultingHP": 0,
                            "instantDeath": "7-7=0 < effective maximum 122", "woundSaveTrigger": "positive-to-zero", "woundSave": "CON14: d20=10 +2=12 vs DC10; success",
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
            {"preEvent": {"identity": "A-original-character-body", "operativeType": "Undead", "hp": 7, "maxHP": 122, "tempHP": 5,
             "wounds": 1, "conditions": [], "deathSaveFailures": 0, "recoveryDeadline": None},
             "damage": "3d10=24; all-resistance=12; tempHP absorbs5; actual HP loss7; HP7->0",
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
                t["rp"]-=2;t["action"]=0;t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"actionPaid":True,"at":3602.1})
                a["lifecycle"]["stableRecoveryDeadline"] = cast_at+0.22+7200
                s["results"].append({"kind":"later-null-hit-already-Stable0","rootDealer":"T","nullNonlethal":True,
                    "damageRoot":{"newIndependentRoot":True,"sourceSpell":"inflict-wounds","rank":1,"rootNullNonlethal":True},
                    "ordinaryDamage":"6d10=34; UA resistance gives17; HP already0; no damage failure; exact recovery deadline preserved",
                    "priorRecoveryDeadlinePreserved":a["lifecycle"]["stableRecoveryDeadline"],"deathCounters":{"failures":0,"successes":0}})
                s["time"] = 3602.1
            ev, cur = event(cur,cid,len(evs)+1,"already-stable0-null-hit",3602.1,
                {"newIndependentRoot":True,"dealer":"T","rank1InflictWoundsCost":2,"result":"same stable recovery deadline and counters; no reroll/restart"},refs,stable_again)
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
        cid = f"RANK9CASTINGCOST5-271-UA-{'NULL' if null else 'ORDINARY'}-WOULD-DIE"
        s0 = base_state(0, a_rp=54, t_rp=80, a_pos=(9,0,0), t_pos=(8,0,0), add_cleric=True)
        a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
        s0["time"] = 3614.0
        a["body"]["type"]="Undead"; a["effects"]["unholy-ascendance"]={"start":3600.1,"expires":3660.1,"suppressed":False,"concentration":False,"pricePaid":26}
        a["resourceHistory"].append({"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":3600.1})
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","sameHPTrack":True}
        a["lifecycle"]={"identity":"A-original-character-body","state":"Dying0","operativeTargetingType":"Undead",
                         "deathSaveFailures":2,"deathSaveSuccesses":0,"nextDeathSaveAt":3618.0,"stableRecoveryDeadline":None,
                         "history":[{"kind":"ordinary-positive-to-zero-damage","at":3601.0},{"kind":"failed-regular-death-save","at":3606.0},{"kind":"failed-regular-death-save","at":3612.0}]}
        a["deathSaves"]={"failures":2,"successes":0}; a["conditions"]={"Unconscious":True,"Dying":True}
        c["conviction"]=4; c["rp"]=52; c["action"]=0
        c["effects"]["ritual-of-undeath-death-ward"]={"target":"A","start":3600.0,"expires":3660.0,"mode":"Death Ward","usesRemaining":1,"source":"cleric.json#/cards/57","triggered":False}
        c["resourceHistory"].append({"source":"cleric.json#/cards/57","mode":"Death Ward","rpPaid":6,"convictionPaid":3,"at":3600.0})
        t["nullVeil"]={"source":"CH07 failed hourly WIS save","fieldId":"NULL-FIELD-QUIET-WELL-1","acquired":3600.0,"suppressed":False} if null else None
        t["effects"]["null-veil"]={"start":3600.0,"suppressed":False,"sourceField":"NULL-FIELD-QUIET-WELL-1"} if null else t["effects"].pop("null-veil",None)
        t["nullFieldExposure"]={"fieldId":"NULL-FIELD-QUIET-WELL-1","elapsedSeconds":3600,"hourlyWISSave":{"roll":2,"modifier":3,"total":5,"dc":15,"success":False}} if null else None
        s0["objects"]["preHitFork"]={"sharedSnapshotForCases14and15":True,"hp":0,"state":"Dying0","failures":2,"nextDeathSaveAt":3618.0,"wardUntriggered":True}
        u=copy.deepcopy(t);u["id"]="U";u["profile"]="CC194-W20";u["position"]=[8,0,0];u["rp"]=78;u["nullVeil"]=None;u["effects"].pop("null-veil",None)
        u["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"at":3601.0,"rootNullNonlethal":False})
        s0["actors"]["U"]=u
        s0["results"].append({"kind":"prior-ordinary-positive-to-zero-history","at":3601.0,"dealer":"U","nullNonlethal":False,
            "recipient":"A-original-character-body","subsequentFailedDeathSaves":[3606.0,3612.0]})
        refs2=source_refs("cleric.json#/cards/57","CH07/currentModule/chambers/6/nullField","CORE_RESOLUTION_PLAYTEST.md#death-saves-and-critical-damage")
        evs=[]
        def resolve(s):
            a=s["actors"]["A"]; c=s["actors"]["C"]
            if null:
                a["lifecycle"]["nextDeathSaveAt"]=3618.0
                a["deathSaves"]={"failures":2,"successes":0}
                c["effects"]["ritual-of-undeath-death-ward"]["triggered"]=False
                c["effects"]["ritual-of-undeath-death-ward"]["usesRemaining"]=1
                outcome="Qualifying Null suppresses damage-caused death failures; A remains Dying0 with failure2 and the same next-save marker; would-die Ward is not triggered or spent."
            else:
                a["hp"]=1; a["lifecycle"]["state"]="Living1-WardReplacement"; a["conditions"]={"Unconscious":False}
                a["targetingTypeTags"]=["Humanoid","Undead"]
                c["effects"]["ritual-of-undeath-death-ward"]["triggered"]=True
                c["effects"]["ritual-of-undeath-death-ward"]["usesRemaining"]=0
                c["effects"]["ritual-of-undeath-death-ward"]["triggerAt"]=3614.1
                outcome="Critical melee hit has a two-failure event. The first failure reaches the third-failure death branch; the acquired Ward replaces death at1HP and no later branch is replayed."
                t=s["actors"]["T"];t["rp"]-=2;t["action"]=0;t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"criticalMeleeAttack":True,"at":3614.1})
            s["results"].append({"kind":"zero-damage-outcome","nullNonlethal":bool(null),"damageRoot":{"dealer":"T","nullNonlethal":bool(null),"createdAt":3614.1},"targetBefore":{"hp":0,"failures":2,"nextDeathSaveAt":3618.0},
                "dealer":"T","attack":"melee Inflict Wounds; Unconscious target within5ft; critical","outcome":outcome})
            if null:
                t=s["actors"]["T"];t["rp"]-=2;t["action"]=0;t["resourceHistory"].append({"spellId":"inflict-wounds","rank":1,"rpPaid":2,"criticalMeleeAttack":True,"at":3614.1})
            s["time"]=3614.1
        ev, s1=event(s0,cid,1,"already-dying0-damage-resolution",3614.1,
            {"nullNonlethal":bool(null),"preEvent":{"hp":0,"life":"Living","state":"Dying0","deathSaveFailures":2,"nextDeathSaveAt":3618.0,
             "UA":"operative","ward":"active, untriggered, one use"},"outcome":"Null keeps markers and skips Ward" if null else "ordinary death trigger is replaced by Ritual of Undeath Death Ward"},refs2,resolve)
        evs.append(ev)
        cases.append(case_record(cid,
            "Conditional same pre-hit snapshot for paired Null/ordinary forks. Cleric Cultist level20 selected card57 at level16 and actually paid 6RP+3 Conviction for Death Ward mode; A was Living before the zero-state history and remains the same character.",
            s0,evs,["Null branch preserves existing Dying0 counters/schedule and leaves would-die Ward untriggered/unspent." if null else
                    "Ordinary critical damage creates the third-failure death branch; the acquired, eligible Ward replaces death at1HP."],
            holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Healing eligibility and UA270-HEAL.
    cid="RANK9CASTINGCOST5-271-UA-HEAL-OPERATIVE"
    s0=base_state(50,a_rp=54,add_cleric=True,a_pos=(9,0,0),t_pos=(10,0,0)); a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    a["body"]["type"]="Undead"; a["effects"]["unholy-ascendance"]={"start":0.1,"expires":60.1,"suppressed":False,"concentration":False,"pricePaid":26}; a["rp"]=54
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","sameHPTrack":True}; a["lifecycle"]["operativeTargetingType"]="Undead"
    a["resourceHistory"].append({"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":0.1})
    a["action"]=1; a["lastRegularStart"]=6.0; a["nextRegularStart"]=12.0
    c["action"]=1; c["rp"]=58;s0["time"]=6.0
    refs3=source_refs("catalog.json#/spells/630/operational","cleric.json#/cards/12","UA270-HEAL authorized by Return270")
    evs=[]
    def reject_heal(s):
        c=s["actors"]["C"]; c["results"] if "results" in c else None
        s["results"].append({"kind":"preflight-rejection","ability":"Healing Rite","target":"A","reason":"operative targeting type Undead fails living-only eligibility",
                              "rpPaid":0,"actionSpent":False,"beforeCommit":True}); s["time"]=6.1
    ev,s1=event(s0,cid,1,"healing-rite-rejected-before-commit",6.1,{"targetType":"Undead","livingOnly":True,"RP":58,"costPaid":0,"actionSpent":False},refs3,reject_heal);evs.append(ev)
    def vt(s):
        a=s["actors"]["A"]; t=s["actors"]["T"]; a["action"]=0
        a["resourceHistory"].append({"spellId":"vampiric-touch","rank":3,"ordinaryQuote":5,"UA270-HEAL":True,"rpPaid":0,"at":6.1})
        a["rp"]=54; a["hp"]=56
        s["results"].append({"kind":"vampiric-touch-self-heal","cast":{"actor":"A","rank":3,"action":True,"components":"V/S/F","operativeUA":True,"castingRPWaived":5},
            "attack":"d20=11 +11 =22 vs AC12","damage":"3d6=12 necrotic; actualDamageDealt12","healing":"floor(12/2)=6 to same caster A","hpBefore":50,"hpAfter":56,
            "RPbefore":54,"RPafter":54,"modifiersCapsAndProhibitions":"unchanged"});s["time"]=6.2
    ev,s2=event(s1,cid,2,"vampiric-touch-self-heal",6.2,{"rank":3,"priceWaiver":"UA270-HEAL only, no damage/healing increase","damage":12,"selfHeal":6,"sameIdentity":"A"},refs3,vt);evs.append(ev)
    cases.append(case_record(cid,"Unholy operative; conditional Wizard20 and Cleric20-Cultist fixtures. Shows living-only Healing Rite rejected before commitment and the director-authorized Vampiric Touch self-heal adapter.",s0,evs,
        ["Known Healing Rite illegality consumes neither action nor RP.","Vampiric Touch remains Action/Touch/V/S/F/rank3/base5RP, one attack and floor(actualDamageDealt/2); UA waives only its casting RP."],holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    cid="RANK9CASTINGCOST5-271-UA-HEAL-SUPPRESSED"
    s0=base_state(50,a_rp=47,add_cleric=True); a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    a["body"]["type"]="Undead";a["effects"]["unholy-ascendance"]={"start":6.1,"expires":66.1,"suppressed":True,"concentration":False,"pricePaid":26}
    a["concentration"]={"spellId":"polymorph","root":"POLY271-S","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","root":"POLY271-S","expires":60.1}}
    a["form"]["suppressed"]=True
    a["effects"]["polymorph"]={"root":"POLY271-S","start":0.1,"expires":60.1,"suppressed":True,"concentration":True}
    a["effects"]["antimagic-field"]={"root":"AMF271-S","start":8.1,"active":True,"suppressedTransforms":["unholy-ascendance","polymorph"]}
    a["body"]["type"]="Humanoid";a["lifecycle"]["operativeTargetingType"]="Humanoid"
    a["resourceHistory"].extend([{"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1},
                                 {"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":6.1}])
    t["rp"]=59;t["resourceHistory"].append({"spellId":"antimagic-field","rank":8,"rpPaid":21,"actionPaid":True,"at":8.1})
    t["concentration"]={"spellId":"antimagic-field","root":"AMF271-S","start":8.1,"expires":3608.1,"concentration":True}
    a["action"]=0;a["lastRegularStart"]=6.0;a["nextRegularStart"]=12.0
    c["rp"]=58;c["action"]=1;s0["time"]=8.5
    refs7=source_refs("cleric.json#/cards/12","Antimagic Field suppresses all transformations; source-grounded accepted interface")
    evs=[]
    def heal_under_suppression(s):
        a=s["actors"]["A"];c=s["actors"]["C"];c["rp"]-=2;c["action"]=0
        a["hp"]=72
        c["resourceHistory"].append({"ability":"healing-rite","rpPaid":2,"target":"A","at":9.0,"dice":"4d8=17","M":5})
        s["results"].append({"kind":"healing-rite-success","target":"A","targetTypeAtCommit":"Humanoid","basis":"AMF suppresses both transformations; base body legally expressed",
            "roll":"S=4d8(17)+M5=22","hpBefore":50,"hpAfter":72,"woundsBefore":1,"woundsAfter":1,"rpPaid":2,"actionPaid":True});s["time"]=9.0
    ev,state=event(s0,cid,1,"healing-rite-legal-under-antimagic-suppression",9.0,{"eligibility":"legal while UA and Polymorph are both suppressed","cost":2,"healing":22,"noWoundRemoval":True},refs7,heal_under_suppression);evs.append(ev)
    def resume_after_field(s):
        a=s["actors"]["A"];a["effects"]["antimagic-field"]["active"]=False;a["effects"]["antimagic-field"]["endedAt"]=14.2
        s["actors"]["T"]["concentration"]=None
        a["effects"]["unholy-ascendance"]["suppressed"]=False;a["effects"]["polymorph"]["suppressed"]=False
        a["form"].pop("suppressed",None);a["body"]["type"]="Undead";a["lifecycle"]["operativeTargetingType"]="Undead"
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
        s["results"].append({"kind":"field-exit-resume","UAdeadline":66.1,"PolymorphDeadline":60.1,"clockChange":None,"UAoperative":True,"originalGearMelded":True});s["time"]=14.2
    def refresh_and_vampiric(s):
        a=s["actors"]["A"];t=s["actors"]["T"]
        a["action"]=0;a["lastRegularStart"]=12.0;a["nextRegularStart"]=18.0;a["rp"]-=5;a["hp"]=78
        a["resourceHistory"].append({"spellId":"vampiric-touch","rank":3,"ordinaryQuote":5,"UA270-HEAL":False,"rpPaid":5,"at":12.1})
        s["results"].append({"kind":"vampiric-touch-under-suppression","actor":"A","rank":3,"quote":5,"rpPaid":5,"actionPaid":True,
            "UA":"suppressed, therefore no UA payment waiver","body":"base Humanoid with original accessible focus/hands/speech","attack":"d20=11+11=22 vs AC12",
            "damage":"3d6=12 necrotic","actualDamageDealt":12,"selfHeal":"floor(12/2)=6","HPbefore":72,"HPafter":78,
            "sameOutputAsOperativeUA":True});s["time"]=12.1
    def refresh_a(s):
        a=s["actors"]["A"];a["action"]=1;a["lastRegularStart"]=12.0;a["nextRegularStart"]=18.0;s["time"]=12.0
    ev,state=event(state,cid,2,"regular-start-A",12.0,{"actor":"A","actionRefresh":True},refs7,refresh_a);evs.append(ev)
    ev,state=event(state,cid,3,"vampiric-touch-ordinary-quote-under-suppression",12.1,{"rank":3,"RPpaid":5,"sameDamageAndHealing":True,"UAisSuppressed":True},refs7,refresh_and_vampiric);evs.append(ev)
    ev,state=event(state,cid,4,"field-end-and-resume",14.2,{"originalDeadlinesPreserved":True,"recasting":False},refs7,resume_after_field);evs.append(ev)
    cases.append(case_record(cid,"Living-only Healing Rite can legally target the same character while actual Antimagic Field suppresses both UA and the prior Polymorph; ending the field restores the original active records.",s0,evs,
        ["Healing Rite pays 2RP and heals S4d8+M5=22; it removes no Wound.","Eligibility is based on the legally expressed Humanoid type while both transformations are suppressed.","Exit resumes only surviving records at their original absolute deadlines."],holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    cid="RANK9CASTINGCOST5-271-UA-HEAL-COMMIT-RACE"
    s0=base_state(50,a_rp=54,add_cleric=True);a,t,c=s0["actors"]["A"],s0["actors"]["T"],s0["actors"]["C"]
    a["body"]["type"]="Humanoid";a["effects"]["unholy-ascendance"]={"start":0.1,"expires":60.1,"suppressed":True,"concentration":False,"pricePaid":26}
    a["effects"]["antimagic-field"]={"root":"AMF271-RACE","start":2.0,"active":True,"suppressedTransforms":["unholy-ascendance"]}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suppressed":True}
    a["lifecycle"]["operativeTargetingType"]="Humanoid";a["resourceHistory"].append({"spellId":"unholy-ascendance","rank":9,"rpPaid":26,"actionPaid":True,"at":0.1})
    t["rp"]=59;t["resourceHistory"].append({"spellId":"antimagic-field","rank":8,"rpPaid":21,"actionPaid":True,"at":2.0})
    t["concentration"]={"spellId":"antimagic-field","root":"AMF271-RACE","start":2.0,"expires":3602.0,"concentration":True}
    c["rp"]=58;c["action"]=1;s0["time"]=2.9
    refs8=source_refs("cleric.json#/cards/12","GPT Return270 authorized later eligibility change after lawful commitment")
    evs=[]
    def commit_rite(s):
        c=s["actors"]["C"];c["rp"]-=2;c["action"]=0
        c["pendingAbility"]={"id":"healing-rite-commit","target":"A","costPaid":2,"targetEligibleAtCommit":True,"resolveAt":3.2}
        c["resourceHistory"].append({"ability":"healing-rite","rpPaid":2,"at":3.0,"committedWhileTargetHumanoid":True})
        s["results"].append({"kind":"lawful-ability-commit","cost":2,"target":"A","preflight":"legal; AMF suppresses UA","effectNotYetResolved":True});s["time"]=3.0
    ev,state=event(s0,cid,1,"healing-rite-commit",3.0,{"eligibilityAtCommit":"Humanoid","RPpaid":2,"ActionSpent":True,"resolve":3.2},refs8,commit_rite);evs.append(ev)
    def field_ends(s):
        a=s["actors"]["A"];a["effects"]["antimagic-field"]["active"]=False;a["effects"]["unholy-ascendance"]["suppressed"]=False;a["body"]["type"]="Undead"
        s["actors"]["T"]["concentration"]=None
        s["time"]=3.1
    ev,state=event(state,cid,2,"eligibility-changes-after-commit",3.1,{"UAresumesBeforeFinalEligibilityCheck":True,"targetTypeNow":"Undead"},refs8,field_ends);evs.append(ev)
    def reject_effect(s):
        a=s["actors"]["A"];c=s["actors"]["C"];c.pop("pendingAbility",None)
        s["results"].append({"kind":"effect-blocked-after-lawful-commit","reason":"living-only target is now Undead","healing":0,"RPpaid":2,"RPrefunded":0,
            "actionSpent":True,"AHP":a["hp"]});s["time"]=3.2
    ev,state=event(state,cid,3,"healing-blocked-no-refund",3.2,{"eligibilityRecheck":"Undead fails living-only target","expenditureRetained":True,"healing":0},refs8,reject_effect);evs.append(ev)
    cases.append(case_record(cid,"Separate conditional commitment-race fork: the acquired Cleric's Healing Rite is legal when committed under UA suppression; UA resumes before the later eligibility check.",s0,evs,
        ["Known illegality would reject before commitment; this different event becomes ineligible only after lawful commitment.","Later blocked effect grants no healing and refunds neither the 2RP nor Action."],holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Prior form, focus custody, real Antimagic suppression, resumption, rejected rank-3 Dispel, original expiry.
    cid="RANK9CASTINGCOST5-271-UA-FORM-LIFECYCLE"
    s0=base_state(50,a_pos=(0,0,0),t_pos=(5,0,0),add_cleric=True); a,b=s0["actors"]["A"],s0["actors"]["T"]
    a["prepared"] += [x for x in ["polymorph","unholy-ascendance"] if x not in a["prepared"]]
    c=s0["actors"]["C"]
    a["rp"]=80; s0["time"]=0.0; evs=[]
    refs4=source_refs("catalog.json#/spells/630/operational","Transformation Polymorph R4 spellform.humanoid; 60-second concentration","Antimagic Field rank8/base21RP","UA270-LIFE spell-local suspension")
    def polymorph_cast(s):
        a=s["actors"]["A"];a["rp"]-=7;a["action"]=0
        a["concentration"]={"spellId":"polymorph","root":"POLY271-A","start":0.1,"expires":60.1,"concentration":True,"rank":4,"pricePaid":7}
        a["form"]={"id":"polymorph","profile":"spellform.humanoid","start":0.1,"expires":60.1,"physicalExpression":"Humanoid-form","underlyingBody":"A-original-character-body","gearMelded":["A-focus","A-robe","A-book"],"concentrationRoot":"POLY271-A"}
        a["body"].update({"type":"Humanoid","hands":2,"speech":True})
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":False,"melded":True})
        a["resourceHistory"].append({"spellId":"polymorph","rank":4,"rpPaid":7,"actionPaid":True,"at":0.1});s["time"]=0.1
    ev,cur=event(s0,cid,1,"cast-polymorph-r4-humanoid",0.1,{"rank":4,"price":7,"action":"Action","concentrationDeadline":60.1,"profile":"spellform.humanoid","handsSpeech":True},refs4,polymorph_cast);evs.append(ev)
    def transfer_focus(s):
        s["objects"]["T-focus"]["custody"]="A";s["objects"]["T-focus"]["transferHistory"]=[{"from":"T","to":"A","at":5.9,"lawfulExternalTransfer":True}]
        s["actors"]["A"]["equipment"]["externalFocus"]={"id":"T-focus","owner":"T","custody":"A","accessible":True,"held":True}
        s["time"]=5.9
    ev,cur=event(cur,cid,2,"external-focus-transfer",5.9,{"item":"T-focus","owner":"T","custody":"T->A","meldedOriginalItemsRemainUnavailable":True},refs4,transfer_focus);evs.append(ev)
    def start_a(s):
        a=s["actors"]["A"];a["action"]=1;a["bonusAction"]=1;a["lastRegularStart"]=6.0;a["nextRegularStart"]=12.0;s["time"]=6.0
    ev,cur=event(cur,cid,3,"regular-start-A",6.0,{"actor":"A","actionRefresh":True,"normalRegularSlot":True},refs4,start_a);evs.append(ev)
    def ua_cast(s):
        activate_ua(s,6.1);s["actors"]["A"]["equipment"]["focus"]={"id":"A-focus","custody":"A","accessible":False,"melded":True}
        s["actors"]["A"]["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","root":"POLY271-A","expires":60.1,"concentration":True,"gearMelded":["A-focus","A-robe","A-book"]},"externalFocusHeld":"T-focus"}
        s["time"]=6.1
    ev,s1=event(cur,cid,4,"cast-unholy-over-existing-form",6.1,{"price":26,"rank":9,"components":"V/S/F","externalFocus":"T-focus, custody T->A at5.9",
        "sameBodyIdentity":True,"priorPolymorphConcentration":"preserved; deadline60.1","UAexpires":66.1,"meldedAItems":"still unavailable"},refs4,ua_cast);evs.append(ev)
    def amf(s):
        a=s["actors"]["A"]; a["effects"]["antimagic-field"]={"root":"AMF271-T","start":8.1,"expires":3608.1,"suppressedTransforms":["unholy-ascendance","polymorph"]}
        a["effects"]["unholy-ascendance"]["suppressed"]=True; a["form"]["suppressed"]=True
        a["body"]["type"]="Humanoid";a["body"]["hands"]=2;a["life"]="Living"
        s["actors"]["T"]["concentration"]={"spellId":"antimagic-field","root":"AMF271-T","start":8.1,"expires":3608.1,"concentration":True}
        s["actors"]["T"]["resourceHistory"].append({"spellId":"antimagic-field","rank":8,"rpPaid":21,"actionPaid":True,"at":8.1})
        for key in ["focus","robe","spellbook"]: a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["actors"]["T"]["rp"]-=21;s["actors"]["T"]["action"]=0
        s["results"].append({"kind":"antimagic-field-suppression","actor":"T","rank":8,"pricePaid":21,"scope":"all actual transformations",
            "A":{"body":"original Humanoid","UA":"suppressed","Polymorph":"suppressed","clocks":{"poly":60.1,"UA":66.1},"originalGearCustody":"A; accessible only in base expression"}})
        s["time"]=8.1
    ev,s2=event(s1,cid,5,"antimagic-field-suppression",8.1,{"caster":"T","spellId":"antimagic-field","rank":8,"RP":21,"bothTransformationsSuppressed":True},refs4,amf);evs.append(ev)
    def amf_end(s):
        a=s["actors"]["A"];a["effects"]["antimagic-field"]["endedAt"]=14.2;a["effects"]["antimagic-field"]["active"]=False
        s["actors"]["T"]["concentration"]=None
        a["effects"]["unholy-ascendance"]["suppressed"]=False;a["form"].pop("suppressed",None);a["body"]["type"]="Undead"
        for key in ["focus","robe","spellbook"]: a["equipment"][key].update({"accessible":False,"melded":True,"custody":"A"})
        s["results"].append({"kind":"resume-original-records","A":{"UAstart":6.1,"UAexpires":66.1,"PolymorphStart":0.1,"PolymorphExpires":60.1},"noClockRestart":True,"noGearDuplication":True});s["time"]=14.2
    ev,s3=event(s2,cid,6,"antimagic-field-end-resume",14.2,{"resume":"same UA and Polymorph records; exact original deadlines"},refs4,amf_end);evs.append(ev)
    def refresh_t(s):
        b=s["actors"]["T"];b["action"]=1;b["lastRegularStart"]=20.0;b["nextRegularStart"]=26.0;s["time"]=20.0
    ev,s3a=event(s3,cid,7,"regular-start-T",20.0,{"actor":"T","actionRefresh":True,"normalRegularSlot":True},refs4,refresh_t);evs.append(ev)
    def rejected_dispensal(s):
        a=s["actors"]["A"];b=s["actors"]["T"]
        s["results"].append({"kind":"known-illegal-dispel-rejected-before-commit","caster":"T","spell":"dispel-magic","actualSpellRank":3,"costQuote":5,
            "target":"A/unholy-ascendance","targetGeneratingRank":9,"sourceCeiling":"Dispel Magic accepts only rank0-3; no automatic upcast",
            "rpPaid":0,"actionSpent":False,"UAremainsActive":True,"PolymorphStillSuspended":True})
        s["time"]=20.2
    ev,s4=event(s3a,cid,8,"rank3-dispel-known-ineligible",20.2,{"targetRank":9,"dispelRank":3,"attemptRejectedBeforeCommit":True,"noRPOrActionSpent":True},
        source_refs("catalog.json#/spells/dispel-magic/operational","catalog.json#/spells/greater-dispel/source (no operational row; not assumed)"),rejected_dispensal);evs.append(ev)
    def prior_expire_ua_remains(s):
        a=s["actors"]["A"];a["concentration"]=None
        a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","priorForm":"Polymorph expired at its own original endpoint"}
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"prior-form-expired-while-UA-operative","at":60.1,"UAexpires":66.1,"UAstillOperative":True,
            "formRefresh":False,"gearRestoredOnlyOnce":["A-focus","A-robe","A-book"],"externalFocusCustody":"A"});s["time"]=60.1
    ev,s5=event(s4,cid,9,"prior-form-original-expiry-UA-remains",60.1,{"PolymorphDeadline":60.1,"UAremainsUntil":66.1,"noRecast":True},refs4,prior_expire_ua_remains);evs.append(ev)
    def ua_natural_expire(s):
        a=s["actors"]["A"];a["effects"].pop("unholy-ascendance",None);a["form"]=None;a["body"]["type"]="Humanoid"
        s["results"].append({"kind":"UA-natural-expiry","at":66.1,"UAexpiredAtOriginalDeadline":True,"baseBodyExpressed":"Humanoid","sameIdentity":"A-original-character-body",
            "noHealingFromExpiry":True,"gearCustody":"A","noDuplicateOrRecoveredLostGear":True});s["time"]=66.1
    ev,s6=event(s5,cid,10,"UA-natural-expiry-after-prior-form",66.1,{"UADeadline":66.1,"noClockRestart":True},refs4,ua_natural_expire);evs.append(ev)
    def legal_heal_after_natural_reversion(s):
        a=s["actors"]["A"];c=s["actors"]["C"];c["rp"]-=2;c["action"]=0;a["hp"]=72
        c["resourceHistory"].append({"ability":"healing-rite","target":"A","rpPaid":2,"at":67.0,"roll":"4d8=17 + M5"})
        s["results"].append({"kind":"healing-rite-after-natural-UA-reversion","targetType":"Humanoid","eligibleLivingAlly":True,"healing":"S4d8(17)+M5=22",
            "hpBefore":50,"hpAfter":72,"woundsBefore":1,"woundsAfter":1,"RPpaid":2,"woundsRemoved":0});s["time"]=67.0
    ev,s7=event(s6,cid,11,"healing-rite-after-natural-reversion",67.0,{"source":"cleric.json#/cards/12","targetType":"Humanoid","cost":2,"healing":22},refs4,legal_heal_after_natural_reversion);evs.append(ev)
    cases.append(case_record(cid,"Actual acquired and paid Polymorph R4 Humanoid is already operative before Unholy Ascendance. The original gear is melded; T transfers a real focus into A's custody before the UA cast.",s0,evs,
        ["UA activation does not reset or replace Polymorph concentration/deadline.","Actual Antimagic Field suppresses both transformations; exit resumes only surviving records with unchanged clocks.","Current Dispel Magic is rank3, can end only rank0-3 effects, and has no automatic upcast; the attempted early removal is rejected before cost/action.","Polymorph expires at its own deadline while UA remains; the original body/gear return without refreshing UA, which later expires at its own deadline.","Living-only Healing Rite is legal on the same character after natural reversion; no early-UA-dismissal witness is claimed because no eligible source remover is currently bounded."],
        holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    # Prior form expiry while UA continues, and actual non-damage death are separate forks.
    cid="RANK9CASTINGCOST5-271-UA-PRIOR-EXPIRY"
    s0=base_state(90,a_pos=(0,0,0),t_pos=(5,0,0));a=s0["actors"]["A"]
    a["rp"]=47;a["concentration"]={"spellId":"polymorph","root":"POLY271-B","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","root":"POLY271-B","expires":60.1,"gearMelded":["A-focus","A-robe","A-book"]}}
    a["body"]["type"]="Undead";a["effects"]["unholy-ascendance"]={"start":6.1,"expires":66.1,"suppressed":False,"concentration":False,"pricePaid":26}
    a["equipment"]["focus"]={"id":"A-focus","custody":"A","accessible":False,"melded":True}
    refs5=source_refs("Transformation Polymorph R4 concentration 60s","UA270-LIFE spell-local prior-form suspension")
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
        s["results"].append({"kind":"UA-original-expiry","at":66.1,"sameBodyIdentity":True,"HP":90,"wounds":1,"gearCustody":"A","newLifeOrSoul":False});s["time"]=66.1
    ev,state=event(state,cid,2,"UA-original-expiry",66.1,{"UAExpires":66.1,"noClockReset":True},refs5,expire_ua);evs.append(ev)
    cases.append(case_record(cid,"Polymorph begins at0.1 and expires at60.1; UA begins at6.1 and expires at66.1. The prior form ends first while UA remains operative.",s0,evs,
        ["The expired prior form is not recreated or refreshed; Unholy continues only to its own original end.","Original A gear is restored once with custody preserved."] ,holds=["CC194-H01","CC194-H02","CC194-H07","CC194-H08"]))

    cid="RANK9CASTINGCOST5-271-UA-ACTUAL-DEATH"
    s0=base_state(90,a_rp=47,a_pos=(0,0,0),t_pos=(5,0,0));a,b=s0["actors"]["A"],s0["actors"]["T"]
    a["body"]["type"]="Undead";a["effects"]["unholy-ascendance"]={"start":6.1,"expires":66.1,"suppressed":False,"concentration":False,"pricePaid":26}
    a["concentration"]={"spellId":"polymorph","root":"POLY271-DEAD","start":0.1,"expires":60.1,"concentration":True,"pricePaid":7}
    a["form"]={"id":"UA270-LIFE","bodyIdentity":"A-original-character-body","suspendedPriorForm":{"id":"polymorph","expires":60.1}}
    a["equipment"]["focus"]={"id":"A-focus","custody":"A","accessible":False,"melded":True}
    refs6=source_refs("catalog.json#/spells/power-word-kill","UA270-LIFE actual-death endpoint","Transformation Polymorph death ends form/concentration")
    s0["time"]=8.0
    def pwk(s):
        a=s["actors"]["A"];t=s["actors"]["T"];t["rp"]-=26;t["action"]=0
        a["life"]="Dead";a["lifecycle"]["state"]="Dead";a["lifecycle"]["deathCause"]="non-damage Power Word Kill";a["lifecycle"]["deathAt"]=8.1
        a["concentration"]=None;a["form"]=None;a["effects"].pop("unholy-ascendance",None);a["body"]["type"]="Humanoid"
        for key in ["focus","robe","spellbook"]:a["equipment"][key].update({"accessible":True,"melded":False,"custody":"A"})
        s["results"].append({"kind":"actual-nondamage-death","spell":"power-word-kill","rank":9,"pricePaid":26,"targetHP":90,"threshold":100,"damage":0,
            "A":{"life":"Dead","HP":90,"bodyIdentity":"A-original-character-body","UA":"ended","PolymorphConcentration":"ended","revived":False,"soulOrHuntRule":"not inferred"},
            "gear":{"restoredOnly":["A-focus","A-robe","A-book"],"custody":"A","duplicated":False,"lostGearRecovered":False}});s["time"]=8.1
    ev,state=event(s0,cid,1,"power-word-kill-actual-death",8.1,{"caster":"T","spellId":"power-word-kill","rank":9,"RP":26,"targetHP":90,"nonDamage":True,"UAandpriorFormEnd":True},refs6,pwk)
    cases.append(case_record(cid,"Independent non-damage death fork with A at90HP; no qualifying Null damage is involved and no protection is stipulated. It closes only UA/form lifecycle; no soul, Hunt, or revival conclusion is imported.",s0,[ev],
        ["Actual death ends UA and the live prior-form concentration record.","Character/body identity stays A; HP is not reassigned by form expiry; original surviving items restore exactly once with unchanged custody."],
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
    procedure["reviewVersion"]="Return271 / UA270-LIFE + UA270-HEAL witness supplement"
    procedure["procedure"] += ("\n\nNEW spell-local UA270-LIFE (explicitly authorized by GPT in Return270; proposal only, not source-recovered): preserve one original character/body identity and all HP/maxHP/Wounds/injuries/death counters/resources/equipment. Operative targeting type is Undead, so living-only targets fail. Ordinary damage follows that character's Core/Healing damage, Wound and death-save procedures through this adapter. No automatic destruction, immunity, separate HP or special zero-HP action. For this recipient only, a qualifying same-dealer Null root suppresses damage-caused Instant Death, Wound/Maiming saves and damage-caused death failures. New positive-to-zero becomes Stable0 with cleared counters and one stipulated d4-hour recovery deadline; already-Dying0/Stable0 preserves current counters/schedule/deadline. Zero HP causes ordinary unconsciousness; it does not end the nonconcentration UA overlay. Actual death ends UA; original expiry and independent removal remain. Suppression returns the legally expressed underlying type/body while all original clocks continue. Each later event snapshots then-current state; reversion never resurrects. Scope is Unholy Ascendance only.\n\nNEW spell-local UA270-HEAL (explicitly authorized by GPT in Return270; proposal only): while UA is operative, the continuing caster may receive its own already-accepted Vampiric Touch self-heal. Preserve Action/Touch/V/S/F, one attack, actual damage and floor(actualDamageDealt/2). The UA waiver changes only eligible casting payment; suppressed/reverted casts use ordinary quote. No new spell, unconscious casting or generic Undead healing. Preserve all existing CC194-H qualifications and downstream gates.")

    cases=create_cases()
    for c in cases: dump_json(OUT/f"cases/{c['id']}.json",c)
    dump_json(OUT/"procedures/unholy-ascendance.json",procedure)
    # Include the exact prior held packet, current-source bindings and relevant current source rows.
    previous = {"path":"evidence/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",**file_binding(OLD)}
    dump_json(OUT/"evidence/CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json",source_candidate)
    dump_json(OUT/"evidence/DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json",delivery)
    dump_json(OUT/"evidence/PRIOR_RETURN240_BINDING.json",previous)
    source_paths=[
      "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_194/ACTOR_PROFILES.json",
      "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
      "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
      "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
      "DescentReviewChanges/ReviewBible/data/playtest/spell_form_profiles.json",
      "DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_relic_null_reviewed_01.json",
      "DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md",
    ]
    excerpt={"status":"SOURCE_BOUND_CONDITIONAL_WITNESSES","sourceSnapshot":source_candidate["sourceSnapshot"],
             "currentAuthority":source_candidate["currentAuthority"],"current117SourceBindings":source_candidate["sourceBindings"],
             "sourceFiles":[file_binding(ROOT/p) for p in source_paths],
             "notes":["Full Return270 current-source ZIP remains attached in the GPT conversation.","Source file hashes bind this packet to the current working tree.","No canonical procedure/index/catalog/queue file is changed here."]}
    dump_json(OUT/"evidence/SOURCE_AND_AUTHORITY_BINDINGS.json",excerpt)
    authorization=("# GPT Return270 authorization\n\n"
      "GPT explicitly authorized the new spell-local proposal UA270-LIFE and UA270-HEAL for witness construction only. It did not accept or apply Unholy Ascendance.\n\n"
      "UA270-LIFE: preserve one original character/body identity, HP/maxHP/Wounds/injuries/death counters/resources/equipment; operative targeting type Undead; ordinary damage uses the character's Core/Healing lifecycle; no automatic destruction, immortality, separate HP or special zero-HP action; same-dealer qualifying Null suppresses this recipient's damage-caused instant death/Wound/death failures; new positive-to-zero becomes Stable0 with cleared counters and one stipulated d4-hour deadline; already-Dying0/Stable0 preserves applicable counters/schedule/deadline; zero HP unconsciousness does not end nonconcentration UA; actual death ends UA; suppression restores legally expressed underlying form with original clocks; no resurrection; spell-local scope only.\n\n"
      "UA270-HEAL: the continuing caster may receive its own already-accepted Vampiric Touch self-heal while UA operates; retain one attack and floor(actualDamageDealt/2); UA changes eligible payment only. Suppressed/reverted cast uses ordinary quote. No unconscious casting or generic Undead healing.\n")
    (OUT/"evidence/GPT_RETURN270_AUTHORIZATION.md").write_text(authorization,encoding="utf-8",newline="\n")
    blocker=("# Return271 open source blocker — early UA removal\n\n"
      "Status: unresolved; no witness or rule is claimed. GPT Return270 required an independent legal removal route that reveals an otherwise-valid prior form.\n\n"
      "The bound operational Dispel Magic permits ending only an individually perceptible ongoing spell effect generated by actual rank 0–3, has no scaling, and uses the original generating rank. Unholy Ascendance is actual rank 9. Therefore the attempted rank-3 Dispel is rejected before payment/action. Greater Dispel is rank 5 in its class-access row but has `operational: null` and is marked not selectable until operational review, so this packet does not invent its acquisition, target eligibility, or rank-9 resolution. The bound Unholy Ascendance record supplies its one-minute duration but no independent-dismissal clause.\n\n"
      "Director decision requested: either (a) authorize a narrow Unholy Ascendance-local dismissal procedure, including actor, timing, cost/action, and prior-form resumption semantics, solely for a new reversible witness; (b) identify an already-bound, actually acquired source rule that supplies a legal remover; or (c) confirm early removal remains an acceptance blocker. No option is assumed by Return271. Natural expiry, Antimagic suppression/resumption, prior-form expiry, and actual-death branches are separately witnessed.\n")
    (OUT/"evidence/OPEN_SOURCE_BLOCKER_EARLY_UA_REMOVAL.md").write_text(blocker,encoding="utf-8",newline="\n")
    readme=("# Return271 — Unholy Ascendance integrated lifecycle witnesses\n\n"
      "Target: unholy-ascendance / CC194-B04 only. Authority at source packet 270: 815 applied / 33 pending / 0 accepted-unapplied; 539 complete procedures / 173 scoped interfaces.\n\n"
      "The new cases are conditional static traces, not runtime/playtest claims. They are built under GPT's explicit spell-local UA270-LIFE and UA270-HEAL authorship. Existing Return240 cases and source qualifications are preserved in the bound historical archive. No acceptance/application is recorded.\n\n"
      "One source blocker remains explicit: no currently bound, selectable procedure supports early removal of this rank-9 effect. Rank-3 Dispel Magic is correctly rejected; Greater Dispel has no operational procedure. See evidence/OPEN_SOURCE_BLOCKER_EARLY_UA_REMOVAL.md. The packet asks GPT to authorize a narrow UA-local dismissal, identify a bound legal source route, or confirm the blocker. Natural expiry and suppression/resumption are witnessed.\n\n"
      "Review request: independently verify the complete current source binding and the integrated new cases, then issue explicit ACCEPT or HOLD for Unholy Ascendance only. If held, identify exact remaining defects. If accepted, leave unapplied and report counts plus next priority (GPT previously named mind-collapse / MD196-B01). Do not decide another identity.\n")
    (OUT/"README.md").write_text(readme,encoding="utf-8",newline="\n")
    request=("Return271 is attached with the current-source 270 binding, the preserved Return240 history, and ten new reversible static witness traces. Please act as director for unholy-ascendance / CC194-B04 only. Independently verify source integrity, the authorized UA270-LIFE/UA270-HEAL boundaries, and the traces.\n\n"
      "The cases cover: matched ordinary versus same-dealer CH07 Null positive-to-zero; actual field exposure, failed save, dealer-at-root binding; defenses/tempHP/post-temp damage/HP/Wound/death/recovery snapshots; already-Dying0 and already-Stable0 clocks; an acquired and actually paid Cleric Cultist Ritual of Undeath would-die protection that stays untriggered under Null but works on an ordinary death branch; living-only Healing Rite rejection before commitment, legal and blocked healing across operative/suppressed/reverted states, and the continuing caster's UA270-HEAL Vampiric Touch; a paid Polymorph R4 Humanoid form with an externally transferred focus, original melded gear custody, actual Antimagic suppression/resumption with unchanged deadlines, prior-form expiry while UA remains, and independent non-damage actual death. The required early-UA-removal branch is not claimed: the trace rejects rank-3 Dispel Magic against rank-9 UA before commitment. Greater Dispel is not selectable because its bound operational procedure is null. The exact source gap and decision requested are in evidence/OPEN_SOURCE_BLOCKER_EARLY_UA_REMOVAL.md.\n\n"
      "Please return an explicit final ACCEPT or HOLD for unholy-ascendance only and resolve the early-removal blocker: authorize a narrow spell-local dismissal for a new witness, identify a bound legal removal source, or confirm the blocker remains. If held, name any other exact semantic/source defect and minimum correction. If accepted, confirm accepted=true but applied=false, current authority counts, and next identity priority. Preserve CC194-H01-H08, all distinctions and downstream gates. Do not accept/apply another identity.")
    (OUT/"REQUEST_271.txt").write_text(request,encoding="utf-8",newline="\n")
    # Deterministic allowlist and member hashes.
    members=[]
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name not in {"DELIVERY_271.json","INDEPENDENT_AUDIT_271.json"}:
            members.append({"name":p.relative_to(OUT).as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    archive=BASE/"DD_Rank9_UnholyAscendance_Director_Return271.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for m in members: z.write(OUT/m["name"],m["name"])
    archive_binding=file_binding(archive,archive.relative_to(ROOT).as_posix())
    delivery271={"id":"DD_Rank9_UnholyAscendance_Director_Return271_DELIVERY","status":"PREPARED_FOR_DIRECTOR_REVIEW",
        "archive":archive_binding,"memberCount":len(members),"payloadMemberCount":len(members)-1,"members":members,
        "currentSourceDelivery":file_binding(SRC270/"DD_Rank9_CastingCost5_CurrentSource_270_DELIVERY.json"),
        "currentAuthority":source_candidate["currentAuthority"],"spellId":TARGET,"blockerIds":["CC194-B04"],"accepted":False,"applied":False}
    dump_json(BASE/"DD_Rank9_UnholyAscendance_Director_Return271_DELIVERY.json",delivery271)

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
      "Cleric would-die ward untriggered Null":any("not triggered or spent" in str(c) for c in cases),
      "healing preflight and UA270-HEAL":any("vampiric-touch" in str(c) and "preflight-rejection" in str(c) for c in cases),
      "antimagic suppression resumption and unchanged deadlines":any("antimagic-field-suppression" in str(c) and "noClockRestart" in str(c) for c in cases),
      "exact equipment custody and no duplication":any("noGearDuplication" in str(c) or "duplicated" in str(c) for c in cases),
      "prior form expires while UA continues":any("prior-form-expired-while-UA-operative" in str(c) for c in cases),
      "distinct non-damage actual death":any("actual-nondamage-death" in str(c) for c in cases),
      "rank-9 early removal source gap accurately disclosed":("no witness or rule is claimed" in blocker and "Greater Dispel" in blocker and any("known-illegal-dispel-rejected-before-commit" in str(c) for c in cases)),
    }
    for k,v in semantics.items():check("semantic coverage: "+k,v)
    with zipfile.ZipFile(archive) as z:
        zin=sorted(z.namelist()); expected=sorted(m["name"] for m in members)
        check("archive exact member allowlist",zin==expected)
        for m in members:
            data=z.read(m["name"])
            check("member hash: "+m["name"],hashlib.sha256(data).hexdigest()==m["sha256"])
    failures=[x for x in checks if not x["passed"]]
    audit={"id":"RANK9_CASTINGCOST5_RETURN271_INDEPENDENT_AUDIT","status":"PASS_PACKAGE_BINDING_AND_REPLAY" if not failures else "FAIL",
        "checkCount":len(checks),"checksPassed":len(checks)-len(failures),"checksFailed":len(failures),"checks":checks,"failures":failures,
        "archive":archive_binding,"caseCount":len(cases),"eventCount":sum(len(c["events"]) for c in cases),
        "forwardInverseOperationCount":2*sum(len(c["events"]) for c in cases),"sourceBindingCount":len(source_candidate["sourceBindings"]),
        "authority":source_candidate["currentAuthority"],"acceptedIds":[],"appliedIds":[],"heldIds":[TARGET]}
    dump_json(BASE/"RANK9_CASTINGCOST5_RETURN271_INDEPENDENT_AUDIT.json",audit)
    assert not failures, json.dumps(failures,indent=2)
    print(json.dumps({"status":audit["status"],"checkCount":audit["checkCount"],"caseCount":audit["caseCount"],"eventCount":audit["eventCount"],
                      "archive":archive_binding,"delivery":file_binding(BASE/"DD_Rank9_UnholyAscendance_Director_Return271_DELIVERY.json")},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
