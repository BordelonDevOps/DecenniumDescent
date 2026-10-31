from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness365_w01_faction_champion_verified02"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack02_TESTONLY.zip"
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
    "id": "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02",
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
    a.update({"id": spell_actor_id, "profile": "TESTONLY-WIZARD9-W01", "profileSHA256": None,
              "class": "Wizard", "level": 9, "HP": 55, "maxHP": 55, "RP": 50, "maxRP": 50,
              "plane": "fixture:origin", "position": [10, 20, 0], "AC": 14, "speed": 30,
              "equipment": ["focus-E-W01", "pack-E-W01"], "carriedLoad": 0.2, "carriedWeightLb": 2,
              "action": 0, "bonusAction": 0, "reaction": 1, "movement": 0,
              "lastSpell": None, "preparedFamiliesUsed": [], "spellHistory": [], "resourceHistory": [],
              "concentration": None, "conditions": [], "magicThisTurn": False,
              "regularSchedule": {"firstStart": 11.0, "period": 6, "endOffset": 0.9, "nextStart": 11.0,
                                  "nextEnd": 11.9, "starts": [], "ends": [], "budgetHistory": []},
              "knownSpells": ["faction-champion"], "preparedSpells": ["faction-champion"],
              "factionEligibility": copy.deepcopy(fixture["championFactionEligibility"])})
    a["profileSHA256"] = sha({k: v for k, v in a.items() if k != "profileSHA256"})
    s["actors"][spell_actor_id] = a

state = add_event(case, state, "W01-E01-TESTONLY-ACQUIRE-PREPARE", 10.95, "TESTONLY_ACQUISITION_AND_PREPARATION", acquire,
                  {"acceptedSpellId": "faction-champion", "acceptanceAuthority": "AC5 exact acceptance 05", "actorId": spell_actor_id},
                  "A hypothetical Wizard 9 has acquired and prepared the accepted spell; no campaign acquisition is claimed.")

def start(s):
    a = s["actors"][spell_actor_id]
    a.update({"action": 1, "bonusAction": 1, "reaction": 1, "movement": 30, "magicThisTurn": False})
    sch = a["regularSchedule"]
    sch["starts"].append(11.0)
    sch["nextEnd"] = 11.9
    sch["nextStart"] = 17.0
    sch["budgetHistory"].append({"time": 11.0, "action": 1, "BA": 1, "Reaction": 1, "Move": 30, "recharge": {}})

state = add_event(case, state, "W01-E02-TESTONLY-REGULAR-START", 11.0, "REGULAR_START", start,
                  {"actorId": spell_actor_id, "fixtureTurn": True}, "Wizard 9 turn budgets are opened for the bounded test fixture.")

def commit(s):
    a = s["actors"][spell_actor_id]
    assert a["action"] == 1 and a["RP"] >= 10 and a["factionEligibility"] == fixture["championFactionEligibility"]
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
                              "explicitAidProhibition": False, "concentrationEndsAt": 71.1})
    a["resourceHistory"].append({"event": cast_id, "RP": -10, "poolAfter": a["RP"], "discount": False})

state = add_event(case, state, "W01-E03-TESTONLY-CAST-COMMIT", 11.1, "CAST_COMMIT", commit,
                  {"spellId": "faction-champion", "acceptedSourcePointer": "/spells/faction-champion/completeSourceAndAccess/coreEntries/0/original",
                   "action": True, "components": ["V", "S", "F"], "costRP": 10, "rangeFt": 60,
                   "concentrationSeconds": 60, "factionEligibility": copy.deepcopy(fixture["championFactionEligibility"])},
                  "Action, V/S/F and 10 RP are paid; concentration is independently scheduled for 60 seconds.")

def resolve(s):
    a = s["actors"][spell_actor_id]
    assert a["concentration"] == cast_id and a["factionEligibility"] == fixture["championFactionEligibility"]
    champ = {
        "id": champ_id, "finiteSummon": True, "exists": True, "type": "Humanoid", "creatureType": "Humanoid",
        "profileId": "AC5-PROFILE-FACTION-CHAMPION-01", "profileSHA256": None,
        "source": cast_id, "owner": spell_actor_id, "factionId": faction_id,
        "plane": "fixture:origin", "position": [10, 15, 0], "lastPlane": None, "lastPosition": None,
        "HP": 70, "maxHP": 70, "AC": 18, "size": "Medium", "bodyBox": [5, 5, 6], "bodyMassLb": 180,
        "speed": 30, "movement": 30, "action": 1, "bonusAction": 0, "reaction": 1,
        "abilities": {"STR": 18, "DEX": 12, "CON": 16, "INT": 10, "WIS": 12, "CHA": 12},
        "saves": "owner-current-PB-as-total", "checks": "printed ability modifier; no proficiency",
        "senses": "ordinary sight/hearing", "defenses": [], "conditions": [], "equipment": [],
        "intrinsicGear": "AC/attack manifestation only; not inventory", "command": None,
        "deadline": 71.2, "concentration": cast_id, "testOnlyBody": True,
    }
    profile = ac5_model["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    champ["profileSHA256"] = sha(profile)
    s["actors"][champ_id] = champ
    s["effects"][champ_effect_id] = {"id": champ_effect_id, "spellId": "faction-champion", "owner": spell_actor_id,
                                     "active": True, "concentration": True, "createdAt": 11.2, "deadline": 71.2,
                                     "body": champ_id, "factionId": faction_id, "testOnly": True}
    a["spellHistory"][-1]["resolutionTime"] = 11.2
    a["spellHistory"][-1]["standingAtResolution"] = 1

state = add_event(case, state, "W01-E04-TESTONLY-CHAMPION-FORMATION", 11.2, "SPELL_RESOLUTION", resolve,
                  {"spellId": "faction-champion", "profileId": "AC5-PROFILE-FACTION-CHAMPION-01",
                   "alliedStatus": True, "standingAtResolution": 1, "invocationPermission": True,
                   "explicitAidProhibition": False, "placement": [10, 15, 0], "distanceFromCasterFt": 5},
                  "One finite Humanoid representative forms within 60 feet; no named NPC or campaign faction event is asserted.")

def command(s):
    owner = s["actors"][spell_actor_id]
    champ = s["actors"][champ_id]
    assert owner["bonusAction"] == 1 and champ["exists"]
    owner["bonusAction"] = 0
    owner["companionCommandRound"] = 11.0
    champ["command"] = {"at": 11.3, "ownerId": spell_actor_id, "cost": "owner Bonus Action",
                        "instruction": "move straight through the Gate aperture", "testOnly": True}
    champ["phaseHistory"] = [{"time": 11.3, "command": "move straight through the Gate aperture", "offenseSpent": False}]

state = add_event(case, state, "W01-E05-TESTONLY-COMMAND", 11.3, "COMPANION_COMMAND", command,
                  {"ownerId": spell_actor_id, "targetId": champ_id, "cost": "Bonus Action", "instruction": "move through aperture"},
                  "The owner pays the real Bonus Action command token before companion movement.")

def cross(s):
    champ = s["actors"][champ_id]
    gate = s["effects"][gate_id]
    assert champ["type"] == "Humanoid" and gate["selectedType"] == "Elemental" and champ["movement"] >= 20
    before = list(champ["position"])
    champ["movement"] -= 20
    champ["lastPlane"], champ["lastPosition"] = champ["plane"], before
    champ["position"] = [10, -5, 0]
    champ["movementHistory"] = [{"from": before, "to": [10, -5, 0], "spentFt": 20,
                                 "portalPlaneCrossed": "y=0", "fitsAperture": True}]
    s["observations"].append({"eventId": "W01-E06-TESTONLY-CROSSING", "actorId": champ_id,
                              "selectedType": gate["selectedType"], "actualType": champ["type"],
                              "result": "NONMATCHING_HUMANOID_PASSES; NO_GATE_EXILE_RESOLUTION",
                              "saveRolled": False, "newHardDenialClaim": False, "newCell": False,
                              "factionRelationshipLabel": "TEST_ONLY_ONLY"})

state = add_event(case, state, "W01-E06-TESTONLY-CROSSING", 11.4, "COMMANDED_MOVEMENT_THROUGH_APERTURE", cross,
                  {"actorId": champ_id, "from": [10, 15, 0], "to": [10, -5, 0], "movementFt": 20,
                   "portalPlane": "y=0", "xWithinAperture": True, "bodyFits10x15": True,
                   "actualCreatureType": "Humanoid", "selectedCreatureType": "Elemental"},
                  "The entire finite Humanoid crosses the 10-by-15-foot aperture; no Gate cell, save, exile, or new hard-denial claim results.")

def end_turn(s):
    a = s["actors"][spell_actor_id]
    a["action"] = a["bonusAction"] = a["movement"] = 0
    a["regularSchedule"]["ends"].append(11.9)
    a["regularSchedule"]["nextEnd"] = 17.9

state = add_event(case, state, "W01-E07-TESTONLY-REGULAR-END", 11.9, "REGULAR_END", end_turn,
                  {"actorId": spell_actor_id, "fixtureTurn": True}, "The fixture owner turn closes with the spent action and command recorded.")
case["final"] = state
case["finalSHA256"] = sha(state)
case["inverseRestorationOrder"] = [e["id"] for e in reversed(case["events"])]
case["coverageMap"] = [
    {"predicate": "accepted AC5 Faction Champion source/access/profile/eligibility", "members": ["authority/AC5_ACCEPTANCE/ACCEPTANCE.json", "authority/AC5_ACCEPTANCE/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json", "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02.json"]},
    {"predicate": "matching allied/enemy Elemental admissions retained", "members": ["prior/CASE_A_ORIGINAL.json", "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02.json"]},
    {"predicate": "Humanoid commanded crossing with no Gate exile/save/hard denial", "members": ["W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02.json", "sources/RETURN327_banishment-gate.json"]},
    {"predicate": "unknown type remains nondiagnostic separate control", "members": ["prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json"]},
]
dump(PACK / "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02.json", case)

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
}
for dest, src in copy_map.items():
    target = PACK / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(src.read_bytes())

(PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").write_bytes(ac5_model_bytes)
(PACK / "authority/AC5_ACCEPTANCE/ACCEPTED_SPELLS_MODEL_SNAPSHOT.json").write_bytes(ac5_model_bytes)
(PACK / "authority/AC5_ACCEPTANCE/AC5_PLAYER_CHAPTER_SNAPSHOT.md").write_bytes(ac5_chapter_bytes)
prior_archive_bytes = (PACK / "prior/W01_REPACK01_UNSUBMITTED.zip").read_bytes()
prior_delivery = json.loads((PACK / "prior/W01_REPACK01_UNSUBMITTED_DELIVERY.json").read_text(encoding=ENC))
assert fsha(prior_archive_bytes) == prior_delivery["sha256"]
dump(PACK / "prior/W01_REPACK01_SUPERSESSION.json", {
    "supersededArchive": "W01_REPACK01_UNSUBMITTED.zip", "supersededArchiveSha256": fsha(prior_archive_bytes),
    "reason": "Repack01 bound a later working AC5 model rather than the byte-exact model accepted in DD_AC5_Local_Final_05.zip.",
    "externalSubmission": False, "directorReviewRequested": False,
    "correction": "Repack02 binds the accepted archive member and the receipt's d782569e... hash.",
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
    "fixtureOnly": True,
}
dump(PACK / "W01_SOURCE_BINDINGS_365.json", bindings)
readme = """# W01 Faction Champion Gate Witness — TEST_ONLY\n\nThis packet submits only PG327-B03/W01 evidence. The case forks the preserved Return327 case A final state with both previously admitted matching Elementals intact. It adds a separately labeled hypothetical Wizard 9 and accepted AC5 Faction Champion, then records a paid Bonus Action command and 20-foot movement of a finite Humanoid body through the existing 10-by-15-foot aperture of an Elemental-selected Gate. No Gate exile, save, new cell, or new hard-denial claim occurs for the nonmatching Humanoid.\n\nFaction identity, allied status, standing, permission, acquisition/preparation, coordinates and party role labels are explicitly TEST_ONLY premises, not campaign facts. The unknown-type control is included unchanged and remains nondiagnostic. The exact AC5 model is extracted from the accepted archive, not taken from a later working copy. Repack01 was corrected before submission and is preserved as an unsubmitted superseded build. This packet is not accepted or applied; Gate identity remains HOLD and queue counts are unchanged.\n"""
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
dump(OUT / "ARCHIVE_DELIVERY_365_W01_REPACK02.json", delivery)
print(json.dumps({"archive": str(ARCHIVE), "bytes": ARCHIVE.stat().st_size, "sha256": archive_sha,
                  "events": len(case["events"]), "members": len(manifest["members"]), "out": str(OUT)}, indent=2))
