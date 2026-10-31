from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness365_w01_faction_champion_verified03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack03_TESTONLY.zip"
ENC = "utf-8"


def canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(v):
    return hashlib.sha256(canon(v)).hexdigest()


def fsha(b):
    return hashlib.sha256(b).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding=ENC)


def changed_ops(a, b, path=""):
    if type(a) is dict and type(b) is dict:
        out = []
        for key in sorted(a.keys() | b.keys()):
            p = path + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in a:
                out.append({"op": "add", "path": p, "value": b[key]})
            elif key not in b:
                out.append({"op": "remove", "path": p})
            else:
                out.extend(changed_ops(a[key], b[key], p))
        return out
    if type(a) is type(b) and a == b:
        return []
    assert path
    return [{"op": "replace", "path": path, "value": b}]


def pointer_get(obj, path):
    cur = obj
    for part in path[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def pointer_parent(obj, path):
    parts = [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]
    cur = obj
    for p in parts[:-1]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    return cur, parts[-1]


def apply_ops(state, ops):
    cur = copy.deepcopy(state)
    for op in ops:
        parent, key = pointer_parent(cur, op["path"])
        if isinstance(parent, list):
            idx = int(key)
            if op["op"] == "replace":
                parent[idx] = copy.deepcopy(op["value"])
            elif op["op"] == "remove":
                parent.pop(idx)
            else:
                parent.insert(idx, copy.deepcopy(op["value"]))
        elif op["op"] == "add":
            assert key not in parent
            parent[key] = copy.deepcopy(op["value"])
        elif op["op"] == "remove":
            del parent[key]
        else:
            parent[key] = copy.deepcopy(op["value"])
    return cur


def add_event(case, state, event_id, time, kind, mutate, evidence, outcome):
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    mutate(after)
    after["time"] = time
    clock_delta = time - case["initial"]["time"]
    after["clock"]["elapsedSeconds"] = case["initial"]["clock"]["elapsedSeconds"] + clock_delta
    for key in ("OpeningRemaining", "HornRemaining"):
        after["clock"][key] = case["initial"]["clock"][key] - clock_delta
    event = {
        "id": event_id, "time": time, "kind": kind, "evidence": evidence,
        "outcome": outcome, "before": before, "beforeSHA256": sha(before),
        "forward": changed_ops(before, after), "after": after,
        "afterSHA256": sha(after), "inverse": changed_ops(after, before),
    }
    assert apply_ops(before, event["forward"]) == after
    assert apply_ops(after, event["inverse"]) == before
    case["events"].append(event)
    return after


if ARCHIVE.exists():
    raise SystemExit(f"Refusing to overwrite an existing archive: {ARCHIVE}")
PACK.mkdir(parents=True, exist_ok=True)

case_path = BASE / "banishment_gate_return327_received/evidence/packet327/prior/cases/RANK9PLANARGATES5129-BANISHMENT-GATE-A.json"
unknown_path = case_path.with_name("RANK9PLANARGATES5129-BANISHMENT-GATE-A__unknown-type.json")
ac5_archive = ROOT / "docs/audit/2026-10-08/full-game/DD_AC5_Local_Final_05.zip"
with zipfile.ZipFile(ac5_archive) as az:
    ac5_model_bytes = az.read("candidate/SPELLS_MODEL.json")
    ac5_chapter_bytes = az.read("candidate/PLAYER_CHAPTER.md")
ac5_model = json.loads(ac5_model_bytes)
assert fsha(ac5_model_bytes) == "d782569ed8ef558f4edf54634e0d8c19926e24e2437528f1769b5ef3ce594898"
spell_source_path = "src/data/spells.js"
spell_source_bytes = subprocess.check_output(["git", "show", f"HEAD:{spell_source_path}"], cwd=ROOT)
assert fsha(spell_source_bytes) == "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078"
spell_source_text = spell_source_bytes.decode(ENC)
spell_object_start = spell_source_text.index("export const SPELLS = {") + len("export const SPELLS = ")
spell_object_end = spell_source_text.index("\n};", spell_object_start) + 2
spell_catalog = json.loads(spell_source_text[spell_object_start:spell_object_end])
wizard_rules_path = "DescentReviewChanges/ReviewBible/docs/mechanics/classes/wizard.md"
combat_rules_path = "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"
spell_rules_path = "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md"
equipment_rules_path = "DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_SOURCE_BINDINGS.md"
wizard_rules_bytes = subprocess.check_output(["git", "show", f"HEAD:{wizard_rules_path}"], cwd=ROOT)
combat_rules_bytes = subprocess.check_output(["git", "show", f"HEAD:{combat_rules_path}"], cwd=ROOT)
spell_rules_bytes = subprocess.check_output(["git", "show", f"HEAD:{spell_rules_path}"], cwd=ROOT)
equipment_rules_bytes = subprocess.check_output(["git", "show", f"HEAD:{equipment_rules_path}"], cwd=ROOT)
w06_archive_path = BASE / "banishment_gate_witness365_w06_planes_shift_repack06_verified04/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack06_TESTONLY.zip"
with zipfile.ZipFile(w06_archive_path) as w06z:
    wizard20_profiles_bytes = w06z.read("sources/WIZARD20_ACTOR_PROFILES.json")
wizard20_profiles = json.loads(wizard20_profiles_bytes)
wizard20_profile = wizard20_profiles["Wizard20"]
wizard20_counterspell = next(c for c in wizard20_profile["automaticCards"] if c["id"] == "wizard.base.counterspell")

wizard_spellbook = []
book_ids = set()
legal_rank_at_level = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5}
new_entries_at_level = {1: 6, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4}
for level in range(1, 10):
    candidates = []
    for spell_id, spell in spell_catalog.items():
        rank = spell.get("classRanks", {}).get("Wizard")
        learn = spell.get("classLearnLevels", {}).get("Wizard")
        if spell_id in book_ids or not isinstance(rank, int) or not isinstance(learn, int):
            continue
        if learn <= level and 1 <= rank <= legal_rank_at_level[level]:
            candidates.append((rank, learn, spell_id, spell))
    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    if level == 9:
        champion = next(item for item in candidates if item[2] == "faction-champion")
        selected = [champion] + [item for item in candidates if item[2] != "faction-champion"][:3]
    else:
        selected = candidates[:new_entries_at_level[level]]
    assert len(selected) == new_entries_at_level[level]
    for rank, learn, spell_id, spell in selected:
        wizard_spellbook.append({"spellId": spell_id, "acquiredAtWizardLevel": level, "rank": rank,
                                 "minimumClassLevel": learn, "school": spell.get("classSchools", {}).get("Wizard"),
                                 "sourcePath": spell_source_path})
        book_ids.add(spell_id)
school_candidates = sorted(
    (spell.get("classRanks", {}).get("Wizard"), spell.get("classLearnLevels", {}).get("Wizard"), spell_id, spell)
    for spell_id, spell in spell_catalog.items()
    if spell_id not in book_ids and spell.get("classRanks", {}).get("Wizard") == 1
    and spell.get("classLearnLevels", {}).get("Wizard", 99) <= 1 and "Conjuration" in spell.get("schools", [])
)
spec_rank, spec_learn, spec_spell_id, spec_spell = school_candidates[0]
wizard_spellbook.append({"spellId": spec_spell_id, "acquiredAtWizardLevel": 1, "rank": spec_rank,
                         "minimumClassLevel": spec_learn, "school": "Conjuration", "sourcePath": spell_source_path,
                         "acquisitionKind": "Arcane School specialization bonus"})
prepared_ids = ["faction-champion"] + [entry["spellId"] for entry in wizard_spellbook if entry["spellId"] != "faction-champion"][:11]
assert len(wizard_spellbook) == 29 and len(set(e["spellId"] for e in wizard_spellbook)) == 29
assert len(prepared_ids) == 12 and len(set(prepared_ids)) == 12
wizard9_profile = {
    "id": "WIZARD9-TESTONLY-PG327-W01-365",
    "fixtureOnly": True,
    "campaignCharacterAsserted": False,
    "class": "Wizard", "classLevel": 9, "totalCharacterLevel": 9, "multiclass": False,
    "PB": 4, "S": 2, "M": 3,
    "abilityScores": {"STR": 8, "DEX": 14, "CON": 14, "INT": 16, "WIS": 12, "CHA": 10},
    "abilityModifiers": {"STR": -1, "DEX": 2, "CON": 2, "INT": 3, "WIS": 1, "CHA": 0},
    "HP": 56, "maxHP": 56,
    "hpDerivation": {"level1Base": 6, "level1Constitution": 2, "level1Subtotal": 8,
                      "levels2To9DieFaces": [4, 4, 4, 4, 4, 4, 4, 4],
                      "levels2To9ConstitutionEach": 2, "total": 56, "rollsAreTestOnly": True},
    "AC": 12, "acDerivation": {"formula": "10 + DEX modifier", "DEXModifier": 2,
                                "armorWorn": None, "sourceActorProfileCrossCheck": "Wizard20 AC 12 at DEX 14"},
    "RP": 32, "maxRP": 32,
    "schoolSpecialization": "Conjuration",
    "schoolSpecializationEffect": "Wizard-summoned creatures gain +1 maximum HP per Wizard level",
    "wizardSpellbookAcquisitions": wizard_spellbook,
    "preparedMatrices": prepared_ids,
    "preparation": {"completedAfterLongRest": True, "studyMinutes": 60, "completedBeforeFixtureEncounter": True,
                    "fixtureTimeIsNotCampaignHistory": True, "matrixCountFormula": "Wizard level + Intelligence modifier",
                    "matrixCount": 12, "factionChampionPrepared": True},
    "automaticClassCards": [{"id": "wizard.base.counterspell", "gainedAtWizardLevel": 2,
                              "activation": "Reaction", "costRP": 3, "rangeFt": 60, "rechargeRounds": 2}],
    "sourceBindings": {
        "wizardRulesPath": wizard_rules_path, "wizardRulesSha256": fsha(wizard_rules_bytes),
        "spellCatalogPath": spell_source_path, "spellCatalogSha256": fsha(spell_source_bytes),
        "acceptedChampionModelSha256": fsha(ac5_model_bytes),
    },
}
wizard9_profile_bytes = canon(wizard9_profile)
wizard9_profile_sha = fsha(wizard9_profile_bytes)
case_a = json.loads(case_path.read_text(encoding=ENC))
initial = copy.deepcopy(case_a["final"])
assert initial["time"] == 10.9
gate_id = "RANK9PLANARGATES5129-BANISHMENT-GATE-A/cast1"
assert initial["effects"][gate_id]["selectedType"] == "Elemental"
assert set(k for k in initial["effects"] if "/cell/" in k) == {
    f"{gate_id}/cell/B-pet", f"{gate_id}/cell/D-pet"
}

fixture = {
    "fixtureId": "OWNER-TESTONLY-PG327-W01-365",
    "authorizedByOwnerForHypotheticalTestState": True,
    "campaignEventsAsserted": False,
    "runtimeExecutionAsserted": False,
    "identityAcceptanceOrApplication": False,
    "factionId": "fixture:allied-faction-365",
    "factionRecordsAreTestPremises": True,
    "roles": {
        "B-pet": {"relation": "ALLY_TEST_ONLY", "type": "Elemental", "sourceAdmissionPreserved": True},
        "D-pet": {"relation": "ENEMY_TEST_ONLY", "type": "Elemental", "sourceAdmissionPreserved": True},
    },
    "geometry": {
        "plane": "fixture:origin", "planeEquation": "y=0", "gateCenter": [10, 0, 0],
        "apertureWidthFt": 10, "apertureHeightFt": 15,
        "horizontalSpanFt": [5, 15], "verticalSpanFt": [0, 15],
        "coordinateAndBodyBoxConvention": "TEST_ONLY; x-y ground plane, z is height; bodyBox is width/depth/height",
    },
    "championFactionEligibility": {
        "factionId": "fixture:allied-faction-365", "alliedStatus": True,
        "standing": 1, "invocationPermission": True, "explicitAidProhibition": False,
        "membership": "not asserted or inferred",
    },
    "hypotheticalWizardAcquisitionAndPreparation": {
        "actorId": "E-W01-TESTONLY", "class": "Wizard", "classLevel": 9,
        "spellId": "faction-champion", "acquired": True, "prepared": True,
        "fixtureOnly": True,
    },
}

spell_actor_id = "E-W01-TESTONLY"
champ_id = "Champion-W01-TESTONLY"
cast_id = "BG-W01-TESTONLY-FACTION-CHAMPION-365/cast1"
champ_effect_id = cast_id
faction_id = fixture["factionId"]

case = {
    "id": "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03",
    "witnessId": "W01",
    "status": "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED",
    "scope": "PG327-B03; accepted AC5 Faction Champion Humanoid crossing an Elemental-selected Gate",
    "identityDecision": "HOLD",
    "fixturePremises": fixture,
    "sourceFork": {
        "caseId": case_a["id"], "sourcePath": case_path.relative_to(ROOT).as_posix(),
        "sourceFileSha256": fsha(case_path.read_bytes()),
        "forkedAtTime": initial["time"], "forkStateSHA256": sha(initial),
        "historicalSourceStatus": case_a["status"],
        "sourceStateIsCopiedWithoutAlteration": True,
    },
    "sourceBindings": {
        "gateId": gate_id,
        "gateSelection": {"selectedType": "Elemental", "active": True, "deadline": initial["effects"][gate_id]["deadline"]},
        "acceptedSpellId": "faction-champion", "acceptedProfileId": "AC5-PROFILE-FACTION-CHAMPION-01",
        "acceptedEligibilityRuleId": "AC5-CHAMPION-ALLY-01",
        "wizard9FixtureProfile": {"packetMember": "sources/WIZARD9_PROFILE_365_TESTONLY.json", "sha256": wizard9_profile_sha},
        "counterspellSourceProfile": {"packetMember": "sources/WIZARD20_ACTOR_PROFILES.json", "pointer": "/Wizard20/automaticCards",
                                       "sha256": fsha(wizard20_profiles_bytes),
                                       "automaticCard": wizard20_counterspell},
    },
    "initial": initial,
    "initialSHA256": sha(initial),
    "events": [],
    "assertions": {
        "matchingElementalAdmissionsRetained": ["B-pet", "D-pet"],
        "matchingElementalRoleLabelsAreTestOnly": True,
        "humanoidCrossingHasNoExile": True,
        "humanoidCrossingHasNoSave": True,
        "noNewHardDenialClaim": True,
        "noSecondCellOrGateMutation": True,
        "unknownTypeControlRemainsSeparateAndNondiagnostic": True,
    },
}

state = copy.deepcopy(initial)

def acquire(s):
    a = copy.deepcopy(s["actors"]["A"])
    a.update({"id": spell_actor_id, "profile": wizard9_profile["id"], "profileSHA256": wizard9_profile_sha,
              "profileArtifactPath": "sources/WIZARD9_PROFILE_365_TESTONLY.json",
              "class": "Wizard", "level": 9, "PB": 4, "S": 2, "M": 3,
              "abilityScores": copy.deepcopy(wizard9_profile["abilityScores"]),
              "abilityModifiers": copy.deepcopy(wizard9_profile["abilityModifiers"]),
              "HP": 56, "maxHP": 56, "RP": 32, "maxRP": 32,
              "plane": "fixture:origin", "position": [10, 20, 0], "AC": 12, "baseAC": 12,
              "speed": 30, "baseSpeed": 30,
              "equipment": ["focus-E-W01"], "carriedItemIds": ["focus-E-W01"],
              "carriedLoad": 0.1, "carriedWeightLb": 1,
              "action": 0, "bonusAction": 0, "reaction": 1, "movement": 0,
              "lastSpell": None, "preparedFamiliesUsed": [], "spellHistory": [], "resourceHistory": [],
              "concentration": None, "conditions": [], "magicThisTurn": False,
              "regularSchedule": {"firstStart": 11.0, "period": 6, "endOffset": 0.9, "nextStart": 11.0,
                                  "nextEnd": 11.9, "starts": [], "ends": [], "budgetHistory": []},
              "knownSpells": [x["spellId"] for x in wizard_spellbook],
              "preparedSpells": list(prepared_ids), "spellbookAcquisitions": copy.deepcopy(wizard_spellbook),
              "schoolSpecialization": "Conjuration", "spellEfficiency": None,
              "hands": 2, "heldItems": ["focus-E-W01"], "freeHands": ["right"],
              "focusId": "focus-E-W01", "focusAccessible": True, "voice": True,
              "visible": True, "lineOfEffect": True, "stance": None, "stanceHistory": [],
              "counterspellAutomaticId": "wizard.base.counterspell",
              "counterspellReady": True, "counterspellRechargeRounds": 2,
              "recharge": {"wizard.base.counterspell": {"ready": True, "roundsUntilReady": 0,
                            "rechargeRounds": 2, "lastUsed": None}},
              "factionEligibility": copy.deepcopy(fixture["championFactionEligibility"])})
    s["actors"][spell_actor_id] = a
    s["items"]["focus-E-W01"] = {
        "id": "focus-E-W01", "kind": "ordinaryWizardFocus", "itemType": "wand", "massLb": 1,
        "load": 0.1, "owner": spell_actor_id, "custodian": spell_actor_id, "heldBy": spell_actor_id,
        "hand": "left", "plane": "fixture:origin", "position": None, "exists": True,
        "quantity": 1, "provenance": "explicit TEST_ONLY carried fixture; not created by spell",
        "consumed": False, "sizeFeet": [0.5, 0.5, 0.5],
        "sourceBinding": {"packetMember": "sources/EQUIPMENT_SOURCE_BINDINGS.md", "description": "ordinary Wizard wand focus"},
    }

state = add_event(case, state, "W01-E01-TESTONLY-PROFILE-AND-ITEM-LOAD", 10.9, "TESTONLY_PROFILE_AND_ITEM_LOAD", acquire,
                  {"acceptedSpellId": "faction-champion", "acceptanceAuthority": "AC5 exact acceptance 05",
                   "actorId": spell_actor_id, "profileArtifact": "sources/WIZARD9_PROFILE_365_TESTONLY.json",
                   "profileSHA256": wizard9_profile_sha, "acquisitionLedger": wizard_spellbook,
                   "preparedMatrices": prepared_ids, "acquisitionAndPreparationCompletedBeforeFork": True,
                   "inventoryItem": "focus-E-W01"},
                  "The test fixture loads a source-bound Wizard 9 whose spellbook acquisition and one-hour preparation premise were completed before this historical fork; campaign acquisition is not claimed.")

def start(s):
    a = s["actors"][spell_actor_id]
    a.update({"action": 1, "bonusAction": 1, "reaction": 1, "movement": 30, "magicThisTurn": False})
    a["stance"] = {"id": "Guarded", "selectedAt": 11.0, "expiresAtNextRegularStart": 17.0,
                    "ACBonus": 1, "speedPenalty": 5, "fixtureSelection": True,
                    "source": "COMBAT_ACTION_PLAYTEST.md#stances"}
    a["AC"] = a["baseAC"] + a["stance"]["ACBonus"]
    a["speed"] = max(0, a["baseSpeed"] - a["stance"]["speedPenalty"])
    a["stanceHistory"].append(copy.deepcopy(a["stance"]))
    sch = a["regularSchedule"]
    sch["starts"].append(11.0)
    sch["nextEnd"] = 11.9
    sch["nextStart"] = 17.0
    sch["budgetHistory"].append({"time": 11.0, "action": 1, "BA": 1, "Reaction": 1, "Move": 30,
                                 "recharge": {"wizard.base.counterspell": "ready"}, "stanceSelectedBeforeActivity": True})

state = add_event(case, state, "W01-E02-TESTONLY-REGULAR-START-STANCE", 11.0, "REGULAR_START_AND_STANCE_SELECTION", start,
                  {"actorId": spell_actor_id, "fixtureTurn": True, "stance": "Guarded",
                   "selectedBeforeFirstStanceRelevantActivity": True}, "Wizard 9 turn budgets and Guarded stance are selected before any relevant activity.")

def commit(s):
    a = s["actors"][spell_actor_id]
    assert a["action"] == 1 and a["RP"] == 32 and a["preparedSpells"].count("faction-champion") == 1
    assert a["freeHands"] == ["right"] and a["heldItems"] == ["focus-E-W01"] and a["voice"] is True
    assert s["items"]["focus-E-W01"]["exists"] and not s["items"]["focus-E-W01"]["consumed"]
    assert a["factionEligibility"] == fixture["championFactionEligibility"]
    a["action"] = 0
    a["RP"] -= 10
    a["lastSpell"] = "faction-champion"
    a["preparedFamiliesUsed"] = ["faction-champion"]
    a["magicThisTurn"] = True
    a["concentration"] = cast_id
    a["spellHistory"].append({"castId": cast_id, "spellId": "faction-champion", "class": "Wizard", "rank": 5,
                              "school": "Conjuration", "time": 11.1, "costRP": 10, "components": ["V", "S", "F"],
                              "rangeFt": 60, "actionSpent": True, "factionId": faction_id,
                              "alliedStatus": True, "standingAtCommit": 1, "invocationPermission": True,
                              "explicitAidProhibition": False, "concentrationEndsAt": 71.2,
                              "spellSourcePointer": "/spells/14/completeSourceAndAccess/source/coreEntries/0/original",
                              "wizardAccessPointer": "/spells/14/completeSourceAndAccess/classAccess/Wizard",
                              "componentProof": {"V": "voice available; not silenced", "S": "right hand free",
                                                 "F": "ordinary Wizard wand held in left hand"}})
    a["resourceHistory"].append({"event": cast_id, "RP": -10, "poolAfter": a["RP"], "discount": False})
    s["pendingCast"] = {"castId": cast_id, "casterId": spell_actor_id, "spellId": "faction-champion",
                        "committedAt": 11.1, "counterspellWindow": "OPEN_TEST_ONLY", "resolved": False}

state = add_event(case, state, "W01-E03-TESTONLY-CAST-COMMIT", 11.1, "CAST_COMMIT", commit,
                  {"spellId": "faction-champion", "acceptedSourcePointer": "/spells/14/completeSourceAndAccess/source/coreEntries/0/original",
                   "wizardAccessPointer": "/spells/14/completeSourceAndAccess/classAccess/Wizard",
                   "action": True, "components": ["V", "S", "F"], "costRP": 10, "rangeFt": 60,
                   "concentrationSeconds": 60, "preCastRP": 32, "postCastRP": 22,
                   "focusItem": "focus-E-W01", "freeSomaticHand": "right", "voiceAvailable": True,
                   "factionEligibility": copy.deepcopy(fixture["championFactionEligibility"])},
                  "The prepared spell commits after Action, all V/S/F prerequisites and 10 RP are evidenced; the Counterspell window opens before effect resolution.")

def counterspell_window(s):
    pending = s["pendingCast"]
    assert pending["castId"] == cast_id and pending["counterspellWindow"] == "OPEN_TEST_ONLY"
    caster = s["actors"][spell_actor_id]
    window = {"castId": cast_id, "opensAfterCommitBeforeEffect": True, "evaluatedAt": 11.15,
              "fixturePerceptionPremise": "TEST_ONLY; unobstructed ordinary perception and line of effect in this bounded scene",
              "eligibleReactions": [], "explicitDeclines": [], "ineligible": []}
    for actor_id in ("A", "B", "D"):
        actor = s["actors"][actor_id]
        distance = math.dist(actor["position"], caster["position"])
        readiness = actor.get("recharge", {}).get("wizard.base.counterspell", {}).get("ready", True)
        eligible = (actor.get("class") == "Wizard" and actor.get("level", 0) >= 2
                    and actor.get("reaction", 0) == 1 and actor.get("RP", 0) >= 3
                    and readiness and distance <= 60)
        assert eligible
        entry = {"actorId": actor_id, "profileSource": "sources/WIZARD20_ACTOR_PROFILES.json#/Wizard20",
                 "automaticCardId": "wizard.base.counterspell", "automaticAtWizardLevel": 2,
                 "distanceFeet": round(distance, 6), "rangeFeet": 60, "perceivesCast": True,
                 "lineOfEffect": True, "reactionAvailable": True, "currentRP": actor["RP"],
                 "costRP": 3, "rechargeReady": True, "rechargeRounds": 2,
                 "decision": "EXPLICIT_TEST_ONLY_DECLINE", "reactionSpent": False,
                 "rpSpent": 0, "rechargeSpent": False}
        window["eligibleReactions"].append(entry)
        window["explicitDeclines"].append(actor_id)
        actor.setdefault("counterspellHistory", []).append(copy.deepcopy(entry))
    for actor_id, reason in ((spell_actor_id, "The caster cannot Counterspell their own cast"),
                             ("C", "Cleric has no Wizard automatic Counterspell feature"),
                             ("B-pet", "No source-bound Counterspell card or spell access"),
                             ("D-pet", "No source-bound Counterspell card or spell access")):
        window["ineligible"].append({"actorId": actor_id, "reason": reason, "attempted": False,
                                      "reactionSpent": False, "rpSpent": 0})
    s["pendingCast"]["counterspellWindow"] = "CLOSED_ALL_DECLINED_TEST_ONLY"
    s.setdefault("counterspellWindows", []).append(window)

state = add_event(case, state, "W01-E04-TESTONLY-COUNTERSPELL-WINDOW", 11.15, "COUNTERSPELL_WINDOW", counterspell_window,
                  {"castId": cast_id, "sourceMember": "sources/WIZARD_CLASS_RULES.md",
                   "automaticFeatureId": "wizard.base.counterspell", "eligibleReactors": ["A", "B", "D"],
                   "declinesCostNothing": True, "allOtherActorsEvaluated": True},
                  "The post-commit, pre-effect window evaluates all actors; three eligible source-backed Wizards explicitly decline without spending Reaction, RP, or recharge.")

def resolve(s):
    a = s["actors"][spell_actor_id]
    assert a["concentration"] == cast_id and a["factionEligibility"] == fixture["championFactionEligibility"]
    champ = {
        "id": champ_id, "finiteSummon": True, "exists": True, "type": "Humanoid", "creatureType": "Humanoid",
        "profileId": "AC5-PROFILE-FACTION-CHAMPION-01", "profileSHA256": None,
        "source": cast_id, "owner": spell_actor_id, "factionId": faction_id,
        "plane": "fixture:origin", "position": [10, 15, 0], "lastPlane": None, "lastPosition": None,
        "HP": 79, "maxHP": 79, "baseHP": 70, "conjurationSpecializationHPBonus": 9,
        "AC": 18, "size": "Medium", "bodyBox": [5, 5, 6], "bodyMassLb": 180,
        "speed": 30, "movement": 30, "action": 1, "bonusAction": 0, "reaction": 1,
        "abilities": {"STR": 18, "DEX": 12, "CON": 16, "INT": 10, "WIS": 12, "CHA": 12},
        "saves": "owner-current-PB-as-total", "checks": "printed ability modifier; no proficiency",
        "senses": "ordinary sight/hearing", "defenses": [], "conditions": [], "equipment": [],
        "intrinsicGear": "AC/attack manifestation only; not inventory", "command": None,
        "deadline": 71.2, "concentration": cast_id, "testOnlyBody": True,
        "phaseState": "NOT_STARTED_UNTIL_OWNER_TURN_END", "phaseHistory": [], "movementHistory": [],
    }
    profile = ac5_model["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    champ["profileSHA256"] = sha(profile)
    s["actors"][champ_id] = champ
    s["effects"][champ_effect_id] = {"id": champ_effect_id, "spellId": "faction-champion", "owner": spell_actor_id,
                                     "active": True, "concentration": True, "createdAt": 11.2, "deadline": 71.2,
                                     "body": champ_id, "factionId": faction_id, "testOnly": True}
    a["spellHistory"][-1]["resolutionTime"] = 11.2
    a["spellHistory"][-1]["standingAtResolution"] = 1
    s["pendingCast"] = None

state = add_event(case, state, "W01-E05-TESTONLY-CHAMPION-FORMATION", 11.2, "SPELL_RESOLUTION", resolve,
                  {"spellId": "faction-champion", "profileId": "AC5-PROFILE-FACTION-CHAMPION-01",
                   "alliedStatus": True, "standingAtResolution": 1, "invocationPermission": True,
                   "explicitAidProhibition": False, "placement": [10, 15, 0], "distanceFromCasterFt": 5},
                  "One finite Humanoid forms with the Conjuration Wizard's +9 maximum-HP specialization; its attached phase is not opened before the owner's turn ends.")

def command(s):
    owner = s["actors"][spell_actor_id]
    champ = s["actors"][champ_id]
    assert owner["bonusAction"] == 1 and champ["exists"]
    owner["bonusAction"] = 0
    owner["companionCommandRound"] = 11.0
    champ["command"] = {"at": 11.3, "ownerId": spell_actor_id, "cost": "owner Bonus Action",
                        "instruction": "move straight through the Gate aperture", "testOnly": True}
    champ["phaseHistory"] = [{"time": 11.3, "command": "move straight through the Gate aperture", "offenseSpent": False}]

state = add_event(case, state, "W01-E06-TESTONLY-COMMAND", 11.3, "COMPANION_COMMAND", command,
                  {"ownerId": spell_actor_id, "targetId": champ_id, "cost": "Bonus Action", "instruction": "move through aperture"},
                  "The owner pays the real Bonus Action command token before companion movement.")

def end_turn(s):
    a = s["actors"][spell_actor_id]
    a["action"] = a["bonusAction"] = a["movement"] = 0
    a["regularSchedule"]["ends"].append(11.9)
    a["regularSchedule"]["nextEnd"] = 17.9

state = add_event(case, state, "W01-E07-TESTONLY-REGULAR-END", 11.9, "REGULAR_END", end_turn,
                  {"actorId": spell_actor_id, "fixtureTurn": True, "reactionPreserved": True,
                   "actionBonusActionAndMovementExpire": True}, "The fixture owner turn ends; spent Action/Bonus Action are retained in history, unused movement expires, and Reaction remains.")

def attached_phase_start(s):
    champ = s["actors"][champ_id]
    owner = s["actors"][spell_actor_id]
    assert owner["regularSchedule"]["ends"][-1] == 11.9 and champ["command"]["ownerId"] == spell_actor_id
    champ.update({"phaseState": "ATTACHED_PHASE_ACTIVE", "action": 1, "movement": 30,
                  "commandAllowance": 1, "movementAllowance": 30})
    champ["phaseHistory"].append({"time": 11.9, "kind": "ATTACHED_PHASE_START", "afterOwnerRegularEnd": True,
                                  "source": "wizard.md#SUMMON-COMMAND-LIMIT"})

state = add_event(case, state, "W01-E08-TESTONLY-ATTACHED-PHASE-START", 11.9, "ATTACHED_PHASE_START", attached_phase_start,
                  {"ownerId": spell_actor_id, "companionId": champ_id, "startsAfterWholeOwnerTurn": True},
                  "The Champion's attached phase begins only after the owner's full regular turn has ended.")

def cross(s):
    champ = s["actors"][champ_id]
    gate = s["effects"][gate_id]
    assert champ["phaseState"] == "ATTACHED_PHASE_ACTIVE" and champ["commandAllowance"] == 1
    assert champ["type"] == "Humanoid" and gate["selectedType"] == "Elemental" and champ["movement"] >= 20
    before = list(champ["position"])
    champ["movement"] -= 20
    champ["movementAllowance"] -= 20
    champ["lastPlane"], champ["lastPosition"] = champ["plane"], before
    champ["position"] = [10, -5, 0]
    champ["command"]["executed"] = True
    champ["command"]["spentMovementFt"] = 20
    champ["movementHistory"] = [{"from": before, "to": [10, -5, 0], "spentFt": 20,
                                 "portalPlaneCrossed": "y=0", "fitsAperture": True,
                                 "phaseState": champ["phaseState"], "commandedByOwner": True}]
    s["observations"].append({"eventId": "W01-E09-TESTONLY-CROSSING", "actorId": champ_id,
                              "selectedType": gate["selectedType"], "actualType": champ["type"],
                              "result": "NONMATCHING_HUMANOID_PASSES; NO_GATE_EXILE_RESOLUTION",
                              "saveRolled": False, "newHardDenialClaim": False, "newCell": False,
                              "factionRelationshipLabel": "TEST_ONLY_ONLY"})

state = add_event(case, state, "W01-E09-TESTONLY-CROSSING", 11.91, "COMMANDED_MOVEMENT_THROUGH_APERTURE", cross,
                  {"actorId": champ_id, "from": [10, 15, 0], "to": [10, -5, 0], "movementFt": 20,
                   "portalPlane": "y=0", "xWithinAperture": True, "bodyFits10x15": True,
                   "actualCreatureType": "Humanoid", "selectedCreatureType": "Elemental",
                   "legalAttachedPhaseActive": True, "ownerRegularEnd": 11.9},
                  "The commanded crossing occurs inside the legal attached phase after the owner's turn; the full Humanoid crosses the aperture with no Gate exile, save, new cell, or new hard-denial claim.")

def attached_phase_end(s):
    champ = s["actors"][champ_id]
    champ["action"] = champ["movement"] = champ["commandAllowance"] = champ["movementAllowance"] = 0
    champ["phaseState"] = "ATTACHED_PHASE_CLOSED"
    champ["phaseHistory"].append({"time": 11.92, "kind": "ATTACHED_PHASE_END", "unusedAllowancesExpired": True})

state = add_event(case, state, "W01-E10-TESTONLY-ATTACHED-PHASE-END", 11.92, "ATTACHED_PHASE_END", attached_phase_end,
                  {"companionId": champ_id, "movementRemaining": 10, "actionUnused": True,
                   "commandAndMovementAllowancesClosed": True},
                  "The attached phase closes with its Action and remaining movement/command allowances explicitly expired.")
case["final"] = state
case["finalSHA256"] = sha(state)
case["inverseRestorationOrder"] = [e["id"] for e in reversed(case["events"])]
case["coverageMap"] = [
    {"predicate": "accepted AC5 Faction Champion source/access/profile/eligibility", "members": ["authority/AC5_ACCEPTANCE/ACCEPTANCE.json", "authority/AC5_ACCEPTANCE/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json", "sources/WIZARD9_PROFILE_365_TESTONLY.json", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json"]},
    {"predicate": "Wizard 9 profile, spellbook, preparation, components and inventory", "members": ["sources/WIZARD9_PROFILE_365_TESTONLY.json", "sources/WIZARD_CLASS_RULES.md", "sources/SPELL_INTEGRATION_RULES.md", "sources/EQUIPMENT_SOURCE_BINDINGS.md", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json"]},
    {"predicate": "Counterspell window and each reactor's eligibility or decline", "members": ["sources/WIZARD20_ACTOR_PROFILES.json", "sources/WIZARD_CLASS_RULES.md", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json"]},
    {"predicate": "matching allied/enemy Elemental admissions retained", "members": ["prior/CASE_A_ORIGINAL.json", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json"]},
    {"predicate": "Humanoid commanded crossing with no Gate exile/save/hard denial", "members": ["W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json", "sources/RETURN327_banishment-gate.json"]},
    {"predicate": "unknown type remains nondiagnostic separate control", "members": ["prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json"]},
]
dump(PACK / "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json", case)

copy_map = {
    "authority/CURRENT_SPELL_QUEUE_361.json": BASE / "banishment_gate_current_authority_361/CURRENT_SPELL_QUEUE_361.json",
    "authority/PG327_W01_W08_WITNESS_PLAN_361.json": BASE / "PG327_W01_W08_WITNESS_PLAN_361.json",
    "authority/PG327_W03_W06_W07_SOURCE_AUDIT_362.json": BASE / "PG327_W03_W06_W07_SOURCE_AUDIT_362.json",
    "authority/AC5_ACCEPTANCE/ACCEPTANCE.json": ROOT / "docs/audit/2026-10-08/full-game/ac5-exact-acceptance-05/ACCEPTANCE.json",
    "authority/AC5_ACCEPTANCE/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json": ROOT / "docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json",
    "authority/AC5_ACCEPTANCE/DD_AC5_Local_Final_05.zip": ac5_archive,
    "authority/AC5_ACCEPTANCE/DD_AC5_Exact_Acceptance_05.zip": ROOT / "docs/audit/2026-10-08/full-game/DD_AC5_Exact_Acceptance_05.zip",
    "authority/PG327_W02_DIRECTOR_SEAL_364_REPACK03.json": BASE / "PG327_W02_DIRECTOR_SEAL_364_REPACK03.json",
    "authority/PG327_W04_DIRECTOR_SEAL_365_REPACK02.json": BASE / "PG327_W04_DIRECTOR_SEAL_365_REPACK02.json",
    "authority/PG327_W06_DIRECTOR_SEAL_365_REPACK06.json": BASE / "PG327_W06_DIRECTOR_SEAL_365_REPACK06.json",
    "authority/PG327_W07_DIRECTOR_SEAL_363_REPACK01.json": BASE / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json",
    "prior/CASE_A_ORIGINAL.json": case_path,
    "prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json": unknown_path,
    "prior/W01_REPACK01_UNSUBMITTED.zip": BASE / "banishment_gate_witness365_w01_faction_champion_verified01/DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack01_TESTONLY.zip",
    "prior/W01_REPACK01_UNSUBMITTED_DELIVERY.json": BASE / "banishment_gate_witness365_w01_faction_champion_verified01/ARCHIVE_DELIVERY_365_W01_REPACK01.json",
    "prior/W01_REPACK02_SUBMITTED.zip": BASE / "banishment_gate_witness365_w01_faction_champion_verified02/DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack02_TESTONLY.zip",
    "prior/W01_REPACK02_SUBMITTED_DELIVERY.json": BASE / "banishment_gate_witness365_w01_faction_champion_verified02/ARCHIVE_DELIVERY_365_W01_REPACK02.json",
    "prior/W01_REPACK02_SUBMITTED_AUDIT.json": BASE / "banishment_gate_witness365_w01_faction_champion_verified02/INDEPENDENT_AUDIT_365_W01_REPACK02.json",
    "prior/PG327_W01_DIRECTOR_HOLD_365_REPACK02.json": BASE / "PG327_W01_DIRECTOR_HOLD_365_REPACK02.json",
    "sources/WIZARD_CLASS_RULES.md": ROOT / wizard_rules_path,
    "sources/COMBAT_ACTION_PLAYTEST.md": ROOT / combat_rules_path,
    "sources/SPELL_INTEGRATION_RULES.md": ROOT / spell_rules_path,
    "sources/EQUIPMENT_SOURCE_BINDINGS.md": ROOT / equipment_rules_path,
}
for dest, src in copy_map.items():
    target = PACK / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(src.read_bytes())

(PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").write_bytes(ac5_model_bytes)
(PACK / "authority/AC5_ACCEPTANCE/ACCEPTED_SPELLS_MODEL_SNAPSHOT.json").write_bytes(ac5_model_bytes)
(PACK / "authority/AC5_ACCEPTANCE/AC5_PLAYER_CHAPTER_SNAPSHOT.md").write_bytes(ac5_chapter_bytes)
(PACK / "sources/SPELL_CATALOG_HEAD.js").write_bytes(spell_source_bytes)
(PACK / "sources/WIZARD20_ACTOR_PROFILES.json").write_bytes(wizard20_profiles_bytes)
(PACK / "sources/WIZARD9_PROFILE_365_TESTONLY.json").write_bytes(wizard9_profile_bytes)
prior_archive_bytes = (PACK / "prior/W01_REPACK01_UNSUBMITTED.zip").read_bytes()
prior_delivery = json.loads((PACK / "prior/W01_REPACK01_UNSUBMITTED_DELIVERY.json").read_text(encoding=ENC))
assert fsha(prior_archive_bytes) == prior_delivery["sha256"]
dump(PACK / "prior/W01_REPACK01_SUPERSESSION.json", {
    "supersededArchive": "W01_REPACK01_UNSUBMITTED.zip", "supersededArchiveSha256": fsha(prior_archive_bytes),
    "reason": "Repack01 bound a later working AC5 model rather than the byte-exact model accepted in DD_AC5_Local_Final_05.zip.",
    "externalSubmission": False, "directorReviewRequested": False,
    "correction": "Repack02 corrected the AC5 archive binding using the receipt's accepted d782569e... hash; Repack02 was submitted and received HOLD, which Repack03 addresses.",
})
repack02_bytes = (PACK / "prior/W01_REPACK02_SUBMITTED.zip").read_bytes()
repack02_delivery = json.loads((PACK / "prior/W01_REPACK02_SUBMITTED_DELIVERY.json").read_text(encoding=ENC))
repack02_ruling = json.loads((PACK / "prior/PG327_W01_DIRECTOR_HOLD_365_REPACK02.json").read_text(encoding=ENC))
assert fsha(repack02_bytes) == repack02_delivery["sha256"] == repack02_ruling["archiveSha256"]
dump(PACK / "prior/W01_REPACK02_SUPERSESSION.json", {
    "supersededArchive": "W01_REPACK02_SUBMITTED.zip", "supersededArchiveSha256": fsha(repack02_bytes),
    "directorRuling": "prior/PG327_W01_DIRECTOR_HOLD_365_REPACK02.json",
    "directorRulingId": repack02_ruling["rulingId"], "directorDecision": "HOLD",
    "reason": "Director identified six semantic residuals; Repack03 supplies corrected source-bound Wizard9 state, component custody, Counterspell window, stance/attached-phase timing, unified concentration and global clocks, and valid source pointers/audit counts.",
    "residualsAddressed": repack02_ruling["remainingResidualIds"], "acceptedOrApplied": False,
})

w06_archive = BASE / "banishment_gate_witness365_w06_planes_shift_repack06_verified04/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack06_TESTONLY.zip"
with zipfile.ZipFile(w06_archive) as zf:
    w06_bindings = json.loads(zf.read("W06_SOURCE_BINDINGS_365.json"))
    w06_bindings_bytes = zf.read("W06_SOURCE_BINDINGS_365.json")
    gate_binding = w06_bindings["fixtureSpecificBindings"]["Gate"]
    gate_bytes = zf.read(gate_binding["packetMember"])
(PACK / "sources").mkdir(exist_ok=True)
(PACK / "sources/RETURN327_banishment-gate.json").write_bytes(gate_bytes)
(PACK / "sources/W06_SOURCE_BINDINGS_365.json").write_bytes(w06_bindings_bytes)
(PACK / "prior/W06_REPACK06_DIRECTOR_SEAL.json").write_bytes((BASE / "PG327_W06_DIRECTOR_SEAL_365_REPACK06.json").read_bytes())

bindings = {
    "sourceCommit": w06_bindings["sourceCommit"],
    "gate": {"repositoryPath": gate_binding["sourcePath"], "packetMember": "sources/RETURN327_banishment-gate.json",
             "sourceCommit": gate_binding["repositorySourceCommit"], "sha256": fsha(gate_bytes),
             "procedurePointer": gate_binding["procedurePointer"], "cellExtensionPointer": gate_binding["cellExtensionPointer"]},
    "sourceCaseA": {"packetMember": "prior/CASE_A_ORIGINAL.json", "sha256": fsha(case_path.read_bytes()), "forkStateSHA256": sha(initial)},
    "unknownTypeControl": {"packetMember": "prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json", "sha256": fsha(unknown_path.read_bytes()), "use": "separate nondiagnostic control; original bytes preserved"},
    "ac5": {"spellId": "faction-champion", "profileId": "AC5-PROFILE-FACTION-CHAMPION-01", "eligibilityRuleId": "AC5-CHAMPION-ALLY-01",
            "acceptancePath": "authority/AC5_ACCEPTANCE/ACCEPTANCE.json", "modelPath": "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json",
            "modelSha256": fsha((PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").read_bytes()),
            "acceptedArchiveSha256": fsha(ac5_archive.read_bytes())},
    "wizard9FixtureProfile": {"packetMember": "sources/WIZARD9_PROFILE_365_TESTONLY.json", "sha256": fsha(wizard9_profile_bytes),
                              "sourceRules": {"packetMember": "sources/WIZARD_CLASS_RULES.md", "sha256": fsha(wizard_rules_bytes)},
                              "spellCatalog": {"packetMember": "sources/SPELL_CATALOG_HEAD.js", "sha256": fsha(spell_source_bytes)}},
    "wizard20CounterspellProfiles": {"packetMember": "sources/WIZARD20_ACTOR_PROFILES.json", "sha256": fsha(wizard20_profiles_bytes),
                                     "wizardPointer": "/Wizard20", "automaticCardId": "wizard.base.counterspell"},
    "combatRules": {"packetMember": "sources/COMBAT_ACTION_PLAYTEST.md", "sha256": fsha(combat_rules_bytes)},
    "spellRules": {"packetMember": "sources/SPELL_INTEGRATION_RULES.md", "sha256": fsha(spell_rules_bytes)},
    "equipmentRules": {"packetMember": "sources/EQUIPMENT_SOURCE_BINDINGS.md", "sha256": fsha(equipment_rules_bytes)},
    "fixtureOnly": True,
}
dump(PACK / "W01_SOURCE_BINDINGS_365.json", bindings)
readme = """# W01 Faction Champion Gate Witness — TEST_ONLY\n\nThis packet submits only PG327-B03/W01 evidence. It forks the preserved Return327 case A final state with both previously admitted matching Elementals intact. It adds a source-bound hypothetical Wizard 9 and accepted AC5 Faction Champion, records all Counterspell opportunities, and runs the paid-command crossing during the Champion's attached phase after the owner's turn ends. The finite Humanoid crosses 20 feet through the existing 10-by-15-foot aperture of an Elemental-selected Gate without Gate exile, save, new cell, or new hard-denial claim.\n\nFaction identity, allied status, standing, permission, Wizard profile/rolls, acquisition/preparation, coordinates, perception/line of effect and party role labels are explicitly TEST_ONLY premises, not campaign facts. The unknown-type control is included unchanged and remains nondiagnostic. The exact AC5 model is extracted from the accepted archive. Repack01 and submitted Repack02 are preserved with provenance; Repack02 received a Director HOLD listing six residuals, which this packet addresses. This packet is not accepted or applied; Gate identity remains HOLD and queue counts are unchanged.\n"""
(PACK / "README.md").write_text(readme, encoding=ENC)

members = sorted(p for p in PACK.rglob("*") if p.is_file())
manifest = {"schemaVersion": "1.0", "fixtureOnly": True, "members": [
    {"path": p.relative_to(PACK).as_posix(), "bytes": p.stat().st_size, "sha256": fsha(p.read_bytes())} for p in members
]}
dump(PACK / "ARCHIVE_MANIFEST.json", manifest)
with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for p in sorted(q for q in PACK.rglob("*") if q.is_file()):
        zf.write(p, p.relative_to(PACK).as_posix())
archive_sha = fsha(ARCHIVE.read_bytes())
delivery = {"archive": ARCHIVE.name, "bytes": ARCHIVE.stat().st_size, "sha256": archive_sha,
            "witnessId": "W01", "status": case["status"], "identityDecision": "HOLD",
            "queueCounts": {"reviewedApplied": 828, "pending": 20, "acceptedUnapplied": 0},
            "campaignEventsAsserted": False, "acceptedOrApplied": False}
dump(OUT / "ARCHIVE_DELIVERY_365_W01_REPACK03.json", delivery)
print(json.dumps({"archive": str(ARCHIVE), "bytes": ARCHIVE.stat().st_size, "sha256": archive_sha,
                  "events": len(case["events"]), "members": len(manifest["members"]), "out": str(OUT)}, indent=2))
