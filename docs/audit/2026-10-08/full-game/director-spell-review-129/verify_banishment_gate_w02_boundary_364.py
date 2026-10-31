from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import zipfile
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness364"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W02_Boundary_364_TESTONLY.zip"
CASE_PATH = PACK / "W02_BOUNDARY_CASE_364.json"
GATE_ID = "BG-W02-TESTONLY-GATE-364"
W07_ARCHIVE = BASE / "banishment_gate_witness363_repack01/DD_Rank9_BanishmentGate_W07_GustCorpse_363_Repack01_TESTONLY.zip"
W07_SEAL = BASE / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json"
ENC = "utf-8"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def pointer_parts(path):
    if not path:
        return []
    assert path.startswith("/")
    return [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]


def get_at(state, path):
    value = state
    for part in pointer_parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(state, path):
    parts = pointer_parts(path)
    assert parts, "Root-path mutation is forbidden"
    parent = state
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def apply_patch(state, operations):
    current = copy.deepcopy(state)
    for operation in operations:
        path, kind = operation["path"], operation["op"]
        assert path, "Root-path operation is forbidden"
        if kind == "test":
            assert get_at(current, path) == operation["value"], f"Precondition failed at {path}"
        elif kind == "replace":
            parent, key = parent_at(current, path)
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                assert key in parent
                parent[key] = copy.deepcopy(operation["value"])
        elif kind == "add":
            parent, key = parent_at(current, path)
            assert isinstance(parent, dict) and key not in parent
            parent[key] = copy.deepcopy(operation["value"])
        elif kind == "remove":
            parent, key = parent_at(current, path)
            assert isinstance(parent, dict) and key in parent
            del parent[key]
        else:
            raise AssertionError(f"Unsupported operation {kind}")
    return current


def changed_paths(before, after, path=""):
    if type(before) is dict and type(after) is dict:
        result = []
        for key in sorted(before.keys() | after.keys()):
            child = path + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                result.append(child)
            else:
                result.extend(changed_paths(before[key], after[key], child))
        return result
    if type(before) is type(after) and before == after:
        return []
    assert path
    return [path]


case = load(CASE_PATH)
bindings = load(PACK / "W02_SOURCE_BINDINGS_364.json")
reuse = load(PACK / "W07_SOURCE_REUSE_364.json")
owner_auth = load(PACK / "W02_OWNER_TESTONLY_AUTHORIZATION_364.json")
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
plan = load(PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
source_audit = load(PACK / "authority/PG327_W03_W06_W07_SOURCE_AUDIT_362.json")

assert case["id"] == "W02_BOUNDARY_CASE_364" and case["witnessId"] == "W02"
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert case["initialSHA256"] == sha(case["initial"]) and case["finalSHA256"] == sha(case["final"])
assert len(case["events"]) == 9
assert case["fixturePremises"] == owner_auth

# Every transition must patch precisely the changed fields and reverse exactly.
state = copy.deepcopy(case["initial"])
for event in case["events"]:
    assert event["before"] == state and event["beforeSHA256"] == sha(state)
    forward = event["forward"]
    inverse = event["inverse"]
    assert all(op["path"] for op in forward + inverse)
    assert all(op["op"] in {"test", "add", "remove", "replace"} for op in forward + inverse)
    assert sorted(op["path"] for op in forward if op["op"] != "test") == sorted(changed_paths(event["before"], event["after"]))
    state = apply_patch(state, forward)
    assert state == event["after"] and event["afterSHA256"] == sha(state)
assert state == case["final"]
for event in reversed(case["events"]):
    assert event["after"] == state
    state = apply_patch(state, event["inverse"])
    assert state == event["before"]
assert state == case["initial"]
assert case["inverseRestorationOrder"] == [e["id"] for e in reversed(case["events"])]
assert [e["time"] for e in case["events"]] == sorted(e["time"] for e in case["events"])

# Reconfirm W07 Repack01 was sealed and is preserved byte-for-byte.
assert file_sha(W07_ARCHIVE.read_bytes()) == reuse["w07ArchiveSha256"] == case["priorSealedWitness"]["archiveSha256"]
assert file_sha(W07_SEAL.read_bytes()) == file_sha((PACK / "prior/PG327_W07_DIRECTOR_SEAL_363_REPACK01.json").read_bytes())
seal = load(W07_SEAL)
assert seal["rulingId"] == reuse["w07DirectorRulingId"] and seal["decision"].startswith("W07 PASSES")
with zipfile.ZipFile(W07_ARCHIVE) as w07:
    assert file_sha(w07.read("MANIFEST.json")) == reuse["w07ManifestSha256"]
    assert file_sha(w07.read("SOURCE_BINDINGS_363.json")) == reuse["w07SourceBindingsSha256"]
    w07_bindings = json.loads(w07.read("SOURCE_BINDINGS_363.json"))
    assert w07_bindings["sourceCommit"] == bindings["sourceCommit"]
    for prior_binding in reuse["reusedBindings"]:
        member = prior_binding["packetMember"]
        assert file_sha(w07.read(member)) == file_sha((PACK / member).read_bytes())

# Verify the exact copied members against Git and the W07 source-binding record.
included = {}
for binding in bindings["bindings"]:
    member_data = (PACK / binding["packetMember"]).read_bytes()
    assert len(member_data) == binding["bytes"] if "bytes" in binding else True
    if binding.get("sourceCommit") == bindings["sourceCommit"]:
        git_bytes = subprocess.check_output(
            ["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'],
            cwd=ROOT,
        )
        assert member_data == git_bytes
        assert file_sha(member_data) == binding["gitSha256"]
        included[binding["repositoryPath"]] = binding
assert len(included) == 11
assert len(bindings["bindings"]) == 17

sources = PACK / "sources"
catalog = json.loads((sources / "catalog.json").read_bytes())
w20_source = json.loads((sources / "WIZARD20_ACTOR_PROFILES.json").read_bytes())["Wizard20"]
w17_source = json.loads((sources / "W17_ACTOR_PROFILES.json").read_bytes())["profiles"][0]
guard_source = json.loads((sources / "bestiary_data_full.json").read_bytes())[326]
procedure = json.loads((sources / "RETURN327_banishment-gate.json").read_bytes())
gate = next(x for x in catalog["spells"] if x.get("id") == "banishment-gate")
counterspell = next(x for x in catalog["spells"] if x.get("id") == "counterspell")["operational"]
historical_gate_range = procedure["nativeCardUnchanged"]["source"]["coreEntries"][0]["original"]["range"]
assert historical_gate_range == "120 feet"
assert "within120ft" in procedure["procedure"]
assert gate["classAccess"]["Wizard"]["baseRpCost"] == 26
assert case["sourceBindings"]["Wizard20"]["gitSha256"] == included["DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json"]["gitSha256"]
assert "banishment-gate" in w20_source["spellbook"] and "banishment-gate" in w20_source["prepared"]
assert w20_source["hpMaximum"] == 122 and w20_source["rpMaximum"] == 80
assert w17_source["maximumHP"] == 104 and w17_source["PB"] == 6
assert guard_source["name"] == "Guard" and guard_source["type"] == "Humanoid" and guard_source["size"] == "Medium"
assert guard_source["hitPoints"] == 112 and guard_source["speed"] == "40 ft."
assert counterspell["rangeFeet"] == 60 and counterspell["components"] == ["V", "S", "F"]
assert w20_source["automaticCards"][1]["id"] == "wizard.base.counterspell"
assert w17_source["automaticCards"][1]["id"] == "wizard.base.counterspell"
assert case["sourceBindings"]["Guard"]["gitSha256"] == included["src/bestiary_data_full.json"]["gitSha256"]

# Gate cast and counterspell decision are complete; no cost or cooldown is charged for a decline.
initial = case["initial"]
actors = initial["actors"]
assert (actors["W20"]["HP"], actors["W20"]["maxHP"], actors["W20"]["RP"], actors["W20"]["maxRP"]) == (122, 122, 80, 80)
assert (actors["W17"]["HP"], actors["W17"]["maxHP"], actors["W17"]["RP"], actors["W17"]["maxRP"]) == (104, 104, 64, 64)
for actor_id, focus_id in (("W20", "focus-W20"), ("W17", "focus-W17")):
    actor = actors[actor_id]
    focus = initial["items"][focus_id]
    assert focus["heldBy"] == actor_id and focus["hand"] == "left"
    assert actor["heldItems"] == [focus_id] and actor["freeHands"] == ["right"]
assert actors["W17"]["counterspellReady"] is True
assert actors["W17"]["recharge"]["wizard.base.counterspell"]["roundsUntilReady"] == 0
gate_cast = next(e for e in case["events"] if e["kind"] == "CAST_COMMIT")
pending = gate_cast["after"]["pendingCast"]
assert pending["spellId"] == "banishment-gate" and pending["actionPaid"] and pending["rpPaid"] == 26
assert pending["componentsProvided"] == ["V", "S", "F"] and pending["focusId"] == "focus-W20"
window = pending["counterspellWindow"]
assert len(window["eligibleReactors"]) == 1
reactor = window["eligibleReactors"][0]
assert reactor["actorId"] == "W17" and reactor["distanceFeet"] == 24 <= reactor["rangeFeet"] == 60
assert reactor["perceivesCast"] and reactor["lineOfEffect"] and reactor["reactionAvailable"] and reactor["rechargeReady"]
assert reactor["currentRP"] == 64 and reactor["costRP"] == 3
assert reactor["componentsAvailable"] == ["V", "S", "F"] and reactor["focusId"] == "focus-W17"
assert reactor["decision"] == "declines" and not reactor["attempted"]
assert not reactor["reactionSpent"] and reactor["RPSpent"] == 0 and not reactor["cooldownChanged"]
assert "TEST_ONLY" in reactor["decisionPremise"]
gate_inputs = gate_cast["authoredInputs"]
assert gate_inputs["rangeFeet"] == 120
assert gate_inputs["casterBasePositionFeet"] == actors["W20"]["position"]
assert math.isclose(gate_inputs["distanceFeet"], math.dist(gate_inputs["casterBasePositionFeet"], gate_inputs["gatePoint"]), abs_tol=1e-10)
assert gate_inputs["distanceFeet"] <= gate_inputs["rangeFeet"]

# Actual lawful movement stops with the leading face at x=0.
guard_id = "Guard-W02-TESTONLY"
opening_guard = actors[guard_id]
assert opening_guard["HP"] == opening_guard["maxHP"] == 112
assert opening_guard["conditions"] == [] and opening_guard["movementPreventingConditions"] == []
assert opening_guard["speedFeet"] == 40
assert opening_guard["bodyBoxWorld"] == {"x": [-10, -5], "y": [-2.5, 2.5], "z": [0, 6]}
assert opening_guard["position"] == [-7.5, 0, 0]
start_event = next(e for e in case["events"] if e["kind"] == "REGULAR_START" and e["authoredInputs"].get("sourceSpeedFeet") == 40)
started_guard = start_event["after"]["actors"][guard_id]
assert started_guard["regularSchedule"]["starts"] == [2.0]
assert started_guard["regularSchedule"]["budgetHistory"] == [{"time": 2.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 40}]
movement = next(e for e in case["events"] if e["kind"] == "LAWFUL_MOVEMENT_TO_BOUNDARY_WITHOUT_CROSSING")
input_data = movement["authoredInputs"]
move_after = movement["after"]
move_guard = move_after["actors"][guard_id]
assert input_data["movementSpentFeet"] == 5 and input_data["wallet"] == [40, 35]
assert move_guard["movement"] == 35
assert move_guard["movementHistory"][-1]["walletBefore"] == 40 and move_guard["movementHistory"][-1]["walletAfter"] == 35
assert move_guard["position"] == [-2.5, 0, 0]
assert move_guard["bodyBoxWorld"] == {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]}
assert move_guard["plane"] == "fixture:origin"
assert input_data["toBodyBox"]["x"][1] == 0 and input_data["positiveInteriorOverlapBeyondPlane"] is False
receipt = move_after["movementReceipts"][-1]
assert receipt["movementWallet"] == {"before": 40, "after": 35}
assert receipt["leadingFaceOnlyTouchesPlane"] if "leadingFaceOnlyTouchesPlane" in receipt else receipt["interiorBeyondPlane"] is False
assert receipt["triggeredGate"] is False and not receipt["admission"] and not receipt["cell"] and not receipt["claim"]
assert move_after["crossingReceipts"] == {} and move_after["admissions"] == [] and move_after["hardDenialClaims"] == []
assert move_after["effects"][GATE_ID]["cells"] == [] and move_after["effects"][GATE_ID]["admissions"] == []

terminal_event = next(e for e in case["events"] if e["kind"] == "CONCENTRATION_END_NO_CELL")
terminal = terminal_event["after"]
terminal_guard = terminal["actors"][guard_id]
assert terminal_guard["plane"] == "fixture:origin" and terminal_guard["position"] == [-2.5, 0, 0]
assert terminal_guard["bodyBoxWorld"] == {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]}
assert terminal_guard["HP"] == 112 and terminal_guard["death"]["status"] == "alive"
assert terminal["crossingReceipts"] == {} and terminal["admissions"] == [] and terminal["hardDenialClaims"] == []
assert terminal["effects"][GATE_ID]["status"] == "ended"
assert terminal["effects"][GATE_ID]["closeCount"] == 1
assert terminal["effects"][GATE_ID]["cells"] == [] and terminal["effects"][GATE_ID]["admissions"] == []
assert terminal["actors"]["W20"]["concentration"] is None
assert terminal_event["authoredInputs"]["scheduledMarkersProcessedThroughEnd"] == [0.0, 0.9, 1.0, 1.9, 2.0]

# Validate source/authority references and honest unchanged queue.
assert plan["requirements"]["witnesses"][1]["id"] == "W02"
assert source_audit["witnessSources"]["W03"]["status"] == "SOURCE_HOLD_NO_QUALIFYING_ACCEPTED_SOURCE_FOUND"
assert source_audit["witnessSources"]["W06"]["status"] == "SOURCE_ROUTE_APPROVED_WITNESS_OUTSTANDING"
assert queue["currentAuthority"]["reviewedApplied"] == 828
assert queue["currentAuthority"]["pending"] == 20
assert queue["currentAuthority"]["acceptedUnapplied"] == 0
assert case["coverage"]["W03"].startswith("open source gap")
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert case["assertions"]["applicationAuthorized"] is False
assert "all nine events" in (PACK / "README.md").read_text(encoding=ENC).lower()

with zipfile.ZipFile(ARCHIVE) as zf:
    assert zf.testzip() is None
    names = zf.namelist()
    assert len(names) == len(set(names))
    manifest = json.loads(zf.read("MANIFEST.json"))
    assert len(names) == len(manifest["members"]) + 2
    checked = 0
    for member in manifest["members"]:
        data = zf.read(member["path"])
        assert len(data) == member["bytes"] and file_sha(data) == member["sha256"]
        assert f"{zlib.crc32(data) & 0xffffffff:08x}" == member["crc32"]
        checked += 1
    assert checked == len(manifest["members"])
    archived_case = json.loads(zf.read("W02_BOUNDARY_CASE_364.json"))
    assert archived_case == case
    assert file_sha(zf.read("prior/W07_Repack01_TESTONLY.zip")) == seal["archiveSha256"]

delivery = load(OUT / "ARCHIVE_DELIVERY_364.json")
archive_bytes = ARCHIVE.read_bytes()
assert delivery["bytes"] == len(archive_bytes)
assert delivery["sha256"] == file_sha(archive_bytes)
assert delivery["memberCount"] == len(names)
assert delivery["zipTest"] == "PASS"

report = {
    "id": "PG327-W02-INDEPENDENT-AUDIT-364",
    "status": "PASS_W02_MOVEMENT_TO_TOUCH; DIRECTOR_REVIEW_REQUIRED",
    "archive": ARCHIVE.name,
    "archiveBytes": len(archive_bytes),
    "archiveSha256": file_sha(archive_bytes),
    "archiveCrc": "PASS",
    "memberCount": len(names),
    "payloadHashesAndCrcsVerified": checked,
    "reusedGitSourceBindingsVerified": len(included),
    "sourceBindings": len(bindings["bindings"]),
    "eventCount": len(case["events"]),
    "forwardReplay": "PASS; field-scoped changed-path operations and preconditions",
    "inverseReplay": "PASS; exact initial state restored; unchanged fields preserved",
    "movement": "PASS; legal 5-foot movement, wallet 40 to 35, body stops touching x=0",
    "admissions": 0,
    "cells": 0,
    "hardDenialClaims": 0,
    "guardRemainsLivingAndOnOriginPlane": True,
    "w07": "Preserved separately; Director-sealed TEST_ONLY witness PASS",
    "w03": "OPEN SOURCE GAP",
    "spellAccepted": False,
    "spellApplied": False,
    "applicationAuthorized": False,
    "queueAuthority": "Queue361: 828 applied / 20 pending / 0 accepted-unapplied",
}
(OUT / "INDEPENDENT_AUDIT_364.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(report, ensure_ascii=False, indent=2))
