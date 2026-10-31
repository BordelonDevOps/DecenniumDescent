from __future__ import annotations

import copy
import hashlib
import json
import math
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness365_w01_faction_champion_verified03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack03_TESTONLY.zip"
CASE_PATH = PACK / "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03.json"
ENC = "utf-8"


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canon(value)).hexdigest()


def fsha(value):
    return hashlib.sha256(value).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def parent(obj, path):
    parts = [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]
    cur = obj
    for part in parts[:-1]:
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur, parts[-1]


def apply(obj, ops):
    cur = copy.deepcopy(obj)
    for op in ops:
        p, key = parent(cur, op["path"])
        if isinstance(p, list):
            index = int(key)
            if op["op"] == "replace":
                p[index] = copy.deepcopy(op["value"])
            elif op["op"] == "remove":
                p.pop(index)
            else:
                p.insert(index, copy.deepcopy(op["value"]))
        elif op["op"] == "add":
            assert key not in p
            p[key] = copy.deepcopy(op["value"])
        elif op["op"] == "remove":
            del p[key]
        else:
            p[key] = copy.deepcopy(op["value"])
    return cur


case = load(CASE_PATH)
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
plan = load(PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
bindings = load(PACK / "W01_SOURCE_BINDINGS_365.json")
manifest = load(PACK / "ARCHIVE_MANIFEST.json")
model_bytes = (PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").read_bytes()
model = json.loads(model_bytes)
acceptance = load(PACK / "authority/AC5_ACCEPTANCE/ACCEPTANCE.json")
receipt = load(PACK / "authority/AC5_ACCEPTANCE/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json")
accepted_archive = PACK / "authority/AC5_ACCEPTANCE/DD_AC5_Local_Final_05.zip"
source_a = load(PACK / "prior/CASE_A_ORIGINAL.json")
source_a_bytes = (PACK / "prior/CASE_A_ORIGINAL.json").read_bytes()
unknown = load(PACK / "prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json")
spellbook_profile_bytes = (PACK / "sources/WIZARD9_PROFILE_365_TESTONLY.json").read_bytes()
spellbook_profile = json.loads(spellbook_profile_bytes)
wizard20_profiles_bytes = (PACK / "sources/WIZARD20_ACTOR_PROFILES.json").read_bytes()
wizard20_profiles = json.loads(wizard20_profiles_bytes)
wizard20 = wizard20_profiles["Wizard20"]
counterspell_card = next(c for c in wizard20["automaticCards"] if c["id"] == "wizard.base.counterspell")

assert case["id"] == "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK03"
assert case["witnessId"] == "W01" and case["status"].endswith("NOT_ACCEPTED; NOT_APPLIED")
assert case["identityDecision"] == "HOLD"
assert queue["currentAuthority"]["reviewedApplied"] == 828
assert queue["currentAuthority"]["pending"] == 20 and queue["currentAuthority"]["acceptedUnapplied"] == 0
assert plan["status"] == "DIRECTOR_REQUIREMENTS_TRANSCRIBED; WITNESSES_NOT_YET_ESTABLISHED"
assert case["fixturePremises"]["campaignEventsAsserted"] is False
assert case["fixturePremises"]["identityAcceptanceOrApplication"] is False
assert case["sourceFork"]["sourceStateIsCopiedWithoutAlteration"] is True
assert case["sourceFork"]["sourceFileSha256"] == fsha(source_a_bytes)
assert source_a["final"] == case["initial"]
assert case["initialSHA256"] == case["sourceFork"]["forkStateSHA256"] == sha(case["initial"])

# Byte-exact accepted source and usable source pointers.
assert acceptance["verdict"] == "ACCEPT_FOR_AUTHORED_CAMPAIGN_PLAYTEST_INTEGRATION"
assert receipt["status"] == "exact-authored-acceptance-applied" and "faction-champion" in receipt["acceptedSpellIds"]
assert fsha(model_bytes) == "d782569ed8ef558f4edf54634e0d8c19926e24e2437528f1769b5ef3ce594898"
with zipfile.ZipFile(accepted_archive) as ac5z:
    assert ac5z.read("candidate/SPELLS_MODEL.json") == model_bytes
spell = model["spells"][14]
assert spell["id"] == "faction-champion"
assert spell["completeSourceAndAccess"]["classAccess"]["Wizard"] == {
    "rank": 5, "minimumClassLevel": 9, "school": "Conjuration", "baseRpCost": 10
}
assert spell["completeSourceAndAccess"]["source"]["coreEntries"][0]["original"]["components"] == "V, S, F"
assert spell["completeSourceAndAccess"]["source"]["coreEntries"][0]["original"]["duration"] == "Concentration, up to 1 minute"
assert bindings["ac5"]["modelSha256"] == fsha(model_bytes)

# The source-bound Wizard 9 is internally consistent and its complete acquisition/preparation is included.
assert fsha(spellbook_profile_bytes) == bindings["wizard9FixtureProfile"]["sha256"] == case["sourceBindings"]["wizard9FixtureProfile"]["sha256"]
assert spellbook_profile["PB"] == 4 and spellbook_profile["S"] == 2
assert spellbook_profile["RP"] == spellbook_profile["maxRP"] == 32
assert spellbook_profile["HP"] == spellbook_profile["maxHP"] == 56
assert spellbook_profile["AC"] == 12 and spellbook_profile["schoolSpecialization"] == "Conjuration"
assert len(spellbook_profile["wizardSpellbookAcquisitions"]) == 29
assert len(spellbook_profile["preparedMatrices"]) == 12 and "faction-champion" in spellbook_profile["preparedMatrices"]
assert spellbook_profile["preparation"]["completedBeforeFixtureEncounter"] is True
assert spellbook_profile["automaticClassCards"][0]["id"] == "wizard.base.counterspell"
actor = case["final"]["actors"]["E-W01-TESTONLY"]
assert actor["profileSHA256"] == fsha(spellbook_profile_bytes) and actor["profileArtifactPath"] == "sources/WIZARD9_PROFILE_365_TESTONLY.json"
assert (actor["PB"], actor["S"], actor["RP"], actor["maxRP"], actor["HP"], actor["maxHP"], actor["baseAC"], actor["AC"], actor["speed"]) == (4, 2, 22, 32, 56, 56, 12, 13, 25)
assert actor["spellEfficiency"] is None and actor["preparedSpells"].count("faction-champion") == 1

# The physical focus, custody, hand state, and all three spell components are recorded.
focus = case["final"]["items"]["focus-E-W01"]
assert focus["exists"] and focus["heldBy"] == actor["id"] and focus["hand"] == "left" and not focus["consumed"]
assert actor["heldItems"] == ["focus-E-W01"] and actor["freeHands"] == ["right"] and actor["voice"] is True
assert actor["carriedWeightLb"] == 1 and actor["carriedLoad"] == 0.1
commit_event = next(e for e in case["events"] if e["kind"] == "CAST_COMMIT")
assert commit_event["evidence"]["acceptedSourcePointer"] == "/spells/14/completeSourceAndAccess/source/coreEntries/0/original"
assert commit_event["evidence"]["wizardAccessPointer"] == "/spells/14/completeSourceAndAccess/classAccess/Wizard"
assert commit_event["evidence"]["preCastRP"] == 32 and commit_event["evidence"]["postCastRP"] == 22
cast_history = actor["spellHistory"][-1]
assert cast_history["components"] == ["V", "S", "F"]
assert cast_history["componentProof"] == {"V": "voice available; not silenced", "S": "right hand free", "F": "ordinary Wizard wand held in left hand"}
assert cast_history["concentrationEndsAt"] == 71.2

# Counterspell interruption window is after commitment and before resolution, with every resident evaluated.
counter_events = [e for e in case["events"] if e["kind"] == "COUNTERSPELL_WINDOW"]
assert len(counter_events) == 1
counter_event = counter_events[0]
commit_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "CAST_COMMIT")
counter_i = case["events"].index(counter_event)
resolve_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "SPELL_RESOLUTION")
assert commit_i < counter_i < resolve_i
window = counter_event["after"]["counterspellWindows"][-1]
assert counterspell_card["id"] == "wizard.base.counterspell" and counterspell_card["activation"] == "Reaction"
assert counterspell_card["cost"] == "3 RP" and "60 feet" in counterspell_card["rangeAndTarget"] and "2 rounds" in counterspell_card["frequency"]
assert {e["actorId"] for e in window["eligibleReactions"]} == {"A", "B", "D"}
for candidate in window["eligibleReactions"]:
    assert candidate["automaticCardId"] == "wizard.base.counterspell"
    assert candidate["perceivesCast"] and candidate["lineOfEffect"] and candidate["reactionAvailable"]
    assert candidate["currentRP"] >= candidate["costRP"] and candidate["distanceFeet"] <= candidate["rangeFeet"]
    assert candidate["rechargeReady"] and candidate["decision"] == "EXPLICIT_TEST_ONLY_DECLINE"
    assert candidate["reactionSpent"] is False and candidate["rpSpent"] == 0 and candidate["rechargeSpent"] is False
assert {x["actorId"] for x in window["ineligible"]} == {"E-W01-TESTONLY", "C", "B-pet", "D-pet"}
for who in ("A", "B", "D"):
    start_actor = case["initial"]["actors"][who]
    end_actor = counter_event["after"]["actors"][who]
    assert (start_actor["RP"], start_actor["reaction"], start_actor["recharge"]) == (end_actor["RP"], end_actor["reaction"], end_actor["recharge"])

# Stance and command/attached-phase order follow the cited regular-turn lifecycle.
assert actor["stance"]["id"] == "Guarded" and actor["stance"]["selectedAt"] == 11.0
assert case["events"][1]["kind"] == "REGULAR_START_AND_STANCE_SELECTION"
command_event = next(e for e in case["events"] if e["kind"] == "COMPANION_COMMAND")
regular_end_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "REGULAR_END")
phase_start_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "ATTACHED_PHASE_START")
cross_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "COMMANDED_MOVEMENT_THROUGH_APERTURE")
phase_end_i = next(i for i, e in enumerate(case["events"]) if e["kind"] == "ATTACHED_PHASE_END")
assert case["events"].index(command_event) < regular_end_i < phase_start_i < cross_i < phase_end_i
champ = case["final"]["actors"]["Champion-W01-TESTONLY"]
assert (champ["HP"], champ["maxHP"], champ["baseHP"], champ["conjurationSpecializationHPBonus"]) == (79, 79, 70, 9)
assert champ["deadline"] == case["final"]["effects"][champ["source"]]["deadline"] == cast_history["concentrationEndsAt"] == 71.2
assert champ["phaseState"] == "ATTACHED_PHASE_CLOSED" and champ["command"]["executed"] is True
assert champ["movementHistory"][0]["spentFt"] == 20 and champ["movementHistory"][0]["phaseState"] == "ATTACHED_PHASE_ACTIVE"
assert champ["position"] == [10, -5, 0] and champ["action"] == champ["movement"] == champ["commandAllowance"] == 0

# Every global clock progresses from the exact historical fork; cast concentration shares one deadline.
initial_time = case["initial"]["time"]
initial_clock = case["initial"]["clock"]
clock_offset = initial_clock["elapsedSeconds"] - initial_time
for event in case["events"]:
    state = event["after"]
    delta = event["time"] - initial_time
    assert math.isclose(state["clock"]["elapsedSeconds"], event["time"] + clock_offset, abs_tol=1e-8)
    for key in ("OpeningRemaining", "HornRemaining"):
        assert math.isclose(state["clock"][key], initial_clock[key] - delta, abs_tol=1e-7)
assert case["final"]["time"] == 11.92

# Full forward/inverse replay, preservation of source admissions, and unchanged Gate/cell state.
state = copy.deepcopy(case["initial"])
for event in case["events"]:
    assert event["before"] == state and event["beforeSHA256"] == sha(state)
    assert apply(state, event["forward"]) == event["after"] and event["afterSHA256"] == sha(event["after"])
    assert apply(event["after"], event["inverse"]) == state
    state = copy.deepcopy(event["after"])
assert state == case["final"] and case["finalSHA256"] == sha(state)
for event in reversed(case["events"]):
    state = apply(state, event["inverse"])
assert state == case["initial"] and case["inverseRestorationOrder"] == [e["id"] for e in reversed(case["events"])]
gate_id = case["sourceBindings"]["gateId"]
assert case["initial"]["effects"][gate_id]["selectedType"] == "Elemental"
assert case["final"]["effects"][gate_id] == case["initial"]["effects"][gate_id]
initial_cells = {k: v for k, v in case["initial"]["effects"].items() if "/cell/" in k}
final_cells = {k: v for k, v in case["final"]["effects"].items() if "/cell/" in k}
assert final_cells == initial_cells and len(final_cells) == 2
assert case["final"]["hardDenialClaims"] == case["initial"]["hardDenialClaims"]
cross_event = case["events"][cross_i]
assert cross_event["evidence"]["bodyFits10x15"] and cross_event["evidence"]["legalAttachedPhaseActive"]
assert cross_event["outcome"].find("no Gate exile, save, new cell") >= 0
obs = case["final"]["observations"][-1]
assert obs["result"] == "NONMATCHING_HUMANOID_PASSES; NO_GATE_EXILE_RESOLUTION"
assert obs["saveRolled"] is False and obs["newHardDenialClaim"] is False and obs["newCell"] is False
assert unknown["status"] == "HELD_NATIVE_TYPE_CONTROL"
assert not any(e.get("kind") == "AUTO_EXILE" for e in unknown["events"])
assert not unknown["final"].get("hardDenialClaims")

# Supersession chain retains the submitted archive and exact Director HOLD.
prior02 = (PACK / "prior/W01_REPACK02_SUBMITTED.zip").read_bytes()
prior02_delivery = load(PACK / "prior/W01_REPACK02_SUBMITTED_DELIVERY.json")
prior02_ruling = load(PACK / "prior/PG327_W01_DIRECTOR_HOLD_365_REPACK02.json")
prior02_supersession = load(PACK / "prior/W01_REPACK02_SUPERSESSION.json")
assert fsha(prior02) == prior02_delivery["sha256"] == prior02_ruling["archiveSha256"] == prior02_supersession["supersededArchiveSha256"]
assert prior02_ruling["witnessDecision"] == "HOLD" and prior02_ruling["acceptedIds"] == prior02_ruling["appliedIds"] == []
assert set(prior02_ruling["remainingResidualIds"]) == set(prior02_supersession["residualsAddressed"])

# Every payload and zipped member is hash-checked; archive count distinguishes manifest from payload.
payload_paths = {entry["path"] for entry in manifest["members"]}
assert "ARCHIVE_MANIFEST.json" not in payload_paths
for entry in manifest["members"]:
    raw = (PACK / entry["path"]).read_bytes()
    assert len(raw) == entry["bytes"] and fsha(raw) == entry["sha256"]
with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    assert archive.testzip() is None
    assert set(names) == payload_paths | {"ARCHIVE_MANIFEST.json"}
    for name in names:
        assert archive.read(name) == (PACK / name).read_bytes()
assert len(names) == len(manifest["members"]) + 1

checks = {
    "exactAC5AcceptedSourceAndAccess": True,
    "sourceBoundWizard9AcquisitionPreparationAndDerivedStats": True,
    "heldFocusFreeSomaticHandAndAudibleVoice": True,
    "allEligibleAndIneligibleCounterspellReactorsEvaluated": True,
    "sourceAExactForkAndExistingElementalAdmissions": True,
    "singleConcentrationDeadlineAndAdvancingGlobalClocks": True,
    "stanceSelectedBeforeActivity": True,
    "attachedPhaseBeginsAfterOwnerEndAndClosesBudgets": True,
    "lawfulPaidCommandAnd20FootCrossing": True,
    "noHumanoidExileSaveNewCellOrHardDenial": True,
    "unknownTypeSeparateNondiagnosticControl": True,
    "forwardInverseReplay": True,
    "archiveIntegrityAndManifest": True,
}
audit = {
    "id": "PG327-W01-365-REPACK03-INDEPENDENT-AUDIT",
    "status": "PASS_TEST_ONLY_WITNESS_PACKET",
    "archive": ARCHIVE.name,
    "archiveSha256": fsha(ARCHIVE.read_bytes()),
    "archiveBytes": ARCHIVE.stat().st_size,
    "caseId": case["id"],
    "eventCount": len(case["events"]),
    "manifestPayloadCount": len(manifest["members"]),
    "archiveMemberCountIncludingManifest": len(names),
    "checks": checks,
    "campaignEventsAsserted": False,
    "identityAcceptanceOrApplication": False,
    "identityDecision": "HOLD",
    "queueCounts": {"reviewedApplied": 828, "pending": 20, "acceptedUnapplied": 0},
}
audit_path = OUT / "INDEPENDENT_AUDIT_365_W01_REPACK03.json"
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(audit, indent=2))
