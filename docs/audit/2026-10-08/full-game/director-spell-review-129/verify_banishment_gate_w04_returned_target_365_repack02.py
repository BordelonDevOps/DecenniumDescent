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
OUT = BASE / "banishment_gate_witness365_w04_returned_target_verified03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W04_ReturnedTarget_365_Repack02_TESTONLY.zip"
CASE = PACK / "W04_RETURNED_TARGET_CASE_365_REPACK02.json"
GATE_ID = "BG-W06-TESTONLY-GATE-365"
CELL_ID = "BG-W06-TESTONLY-CELL-GUARD-365"
TARGET_ID = "Guard-W06-TESTONLY"
CREATOR_ID = "W20"
ENCOUNTER_ID = "fixture:banishment-gate-w06-365"
ENC = "utf-8"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def parts(path):
    return [x.replace("~1", "/").replace("~0", "~") for x in path[1:].split("/")] if path else []


def get_at(obj, path):
    value = obj
    for part in parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(obj, path):
    ps = parts(path)
    parent = obj
    for part in ps[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, ps[-1]


def apply_ops(state, ops):
    current = copy.deepcopy(state)
    for op in ops:
        path, kind = op["path"], op["op"]
        if kind == "test":
            assert get_at(current, path) == op["value"], f"precondition {path}"
            continue
        parent, key = parent_at(current, path)
        if isinstance(parent, list):
            i = int(key)
            if kind == "replace":
                parent[i] = copy.deepcopy(op["value"])
            elif kind == "remove":
                parent.pop(i)
            elif kind == "add":
                parent.insert(i, copy.deepcopy(op["value"]))
            else:
                raise AssertionError(f"unsupported list op {kind}")
        elif kind == "add":
            assert key not in parent
            parent[key] = copy.deepcopy(op["value"])
        elif kind == "replace":
            assert key in parent
            parent[key] = copy.deepcopy(op["value"])
        elif kind == "remove":
            assert key in parent
            del parent[key]
        else:
            raise AssertionError(f"unsupported op {kind}")
    return current


case = load(CASE)
source_bindings = load(PACK / "W06_SOURCE_BINDINGS_365.json")
plan = load(PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
seal = load(PACK / "prior/PG327_W06_DIRECTOR_SEAL_365_REPACK06.json")
audit06 = load(PACK / "prior/INDEPENDENT_AUDIT_365_REPACK06.json")
w06_archive = PACK / "prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack06_TESTONLY.zip"
assert case["id"] == "W04_RETURNED_TARGET_CASE_365_REPACK02" and case["witnessId"] == "W04"
assert case["authorizedTestFixture"]["campaignEventsAsserted"] is False
assert case["authorizedTestFixture"]["identityAcceptanceOrApplication"] is False
assert case["supersedesSubmissions"]["supersedes"]["archive"] == "DD_Rank9_BanishmentGate_W04_ReturnedTarget_365_Repack01_TESTONLY.zip"
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert seal["witnessDecision"] == "SEALED_TEST_ONLY" and seal["identityDecision"] == "HOLD"
assert "W04" in seal["remainingWitnessIds"] and seal["nextWitness"] == "W04"
assert sha(queue) == sha(load(BASE / "CURRENT_SPELL_QUEUE_361.json"))
assert queue["currentAuthority"]["reviewedApplied"] == 828
assert queue["currentAuthority"]["pending"] == 20 and queue["currentAuthority"]["acceptedUnapplied"] == 0
w04_plan = next(x for x in plan["requirements"]["witnesses"] if x["id"] == "W04")
assert "existing creator/target/encounter claim" in w04_plan["requiredEvidence"]
assert seal["archiveSha256"] == file_sha(w06_archive.read_bytes()) == audit06["archiveSha256"]
with zipfile.ZipFile(w06_archive) as w06z:
    w06_case = json.loads(w06z.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK06.json"))
    w06_source_bindings = json.loads(w06z.read("W06_SOURCE_BINDINGS_365.json"))
    prior_event = w06_case["events"][7]
    assert prior_event["kind"] == "VOLUNTARY_COMPLETE_CROSSING_AND_ADMISSION"
    assert case["initial"] == prior_event["after"]
    assert case["priorAdmission"]["event"] == prior_event
    gate_binding = w06_source_bindings["fixtureSpecificBindings"]["Gate"]
    gate_bytes = w06z.read(gate_binding["packetMember"])
assert case["fixturePremises"]["sourceArchiveSha256"] == file_sha(w06_archive.read_bytes())
assert case["fixturePremises"]["forkEventId"] == prior_event["id"]
assert case["initialSHA256"] == sha(case["initial"]) == prior_event["afterSHA256"]

expected_gate_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json"
assert gate_binding["sourcePath"] == expected_gate_path
assert gate_binding["sourcePath"] == w06_source_bindings["bindings"][11]["repositoryPath"]
assert case["sourceBindings"]["Gate"]["sourcePath"] == expected_gate_path
assert case["sourceBindings"]["Gate"]["sha256"] == file_sha(gate_bytes)
assert subprocess.check_output(["git", "show", f'{gate_binding["repositorySourceCommit"]}:{expected_gate_path}'], cwd=ROOT) == gate_bytes
gate_source = json.loads(gate_bytes)
assert isinstance(get_at(gate_source, "/procedure"), str)
assert isinstance(get_at(gate_source, "/sharedContract/cellExtension"), dict)
for clause in ("PG9-Q14", "PG9-Q16", "PG9-Q29"):
    assert clause in gate_source["procedure"]

initial = case["initial"]
target = initial["actors"][TARGET_ID]
gate = initial["effects"][GATE_ID]
cell = initial["cells"][CELL_ID]
claim = {"creatorId": CREATOR_ID, "targetId": TARGET_ID, "encounterId": ENCOUNTER_ID,
         "claimId": "claim-Guard-365", "spentAt": 2.05}
assert target["lifeClassification"] == "ALIVE_LIVING_TEST_ONLY_FIXTURE"
assert gate["status"] == "active" and gate["creatorId"] == CREATOR_ID
assert gate["selectedCreatureType"] == "Humanoid" and gate["endsAt"] == 600.2
assert cell["status"] == "active" and cell["deadline"] == 62.05
assert cell["primaryTargetId"] == TARGET_ID and cell["originAnchor"]["plane"] == "fixture:origin"
assert claim in initial["hardDenialClaims"]
first_id = f"{GATE_ID}/crossing/1"
assert case["priorAdmission"]["crossingId"] == first_id
first_receipt = initial["crossingReceipts"][first_id]
assert first_receipt["claimSpent"] is True and first_receipt["admittedAt"] == 2.05
assert first_receipt["to"] == CELL_ID and first_receipt["targetId"] == TARGET_ID

events = case["events"]
assert events and events[0]["before"] == initial
current = copy.deepcopy(initial)
for event in events:
    assert event["before"] == current, event["id"]
    assert event["beforeSHA256"] == sha(current)
    assert event["afterSHA256"] == sha(event["after"])
    assert apply_ops(current, event["forward"]) == event["after"], event["id"]
    assert apply_ops(event["after"], event["inverse"]) == current, event["id"]
    current = copy.deepcopy(event["after"])
assert current == case["final"] and case["finalSHA256"] == sha(current)
restored = copy.deepcopy(current)
for event in reversed(events):
    restored = apply_ops(restored, event["inverse"])
assert restored == initial and sha(restored) == case["initialSHA256"]
assert case["inverseRestorationOrder"] == [e["id"] for e in reversed(events)]

start_events = [e for e in events if e["kind"] == "REGULAR_START"]
end_events = [e for e in events if e["kind"] == "REGULAR_END"]
assert len(start_events) == 40 and len(end_events) == 40
assert any(e["time"] == 62.0 and e["authoredInputs"]["actorId"] == TARGET_ID for e in start_events)
assert all(events[i]["time"] <= events[i+1]["time"] for i in range(len(events)-1))
for event in end_events:
    actor_id = event["authoredInputs"]["actorId"]
    before_actor = event["before"]["actors"][actor_id]
    after_actor = event["after"]["actors"][actor_id]
    assert after_actor["action"] == after_actor["bonusAction"] == after_actor["movement"] == 0
    assert after_actor.get("reaction") == before_actor.get("reaction")
    assert after_actor["regularSchedule"]["ends"][-1] == event["time"]
    assert after_actor["regularSchedule"]["nextEnd"] == event["time"] + after_actor["regularSchedule"]["period"]
for event in start_events:
    actor_id = event["authoredInputs"]["actorId"]
    after_actor = event["after"]["actors"][actor_id]
    assert event["authoredInputs"]["testOnlyStanceChoice"] == "Mobile"
    assert event["authoredInputs"]["stanceSelectedBeforeActivityOrIdleEnd"] is True
    assert after_actor["stance"]["id"] == "Mobile"
    assert after_actor["stance"]["selectedAt"] == event["time"]
    assert after_actor["stance"]["expiresAtNextRegularStart"] == event["time"] + after_actor["regularSchedule"]["period"]
    assert after_actor["stanceHistory"][-1] == after_actor["stance"]
    assert after_actor["mobileFirstFiveFeetAllowance"]["remainingFeet"] == 5
    assert after_actor["mobileFirstFiveFeetAllowance"]["expiresAtNextRegularStart"] == after_actor["stance"]["expiresAtNextRegularStart"]
    if actor_id in event["before"]["actors"]:
        old_actor = event["before"]["actors"][actor_id]
        old_stance = old_actor.get("stance") or {}
        if old_stance and old_stance.get("expiresAtNextRegularStart", float("inf")) <= event["time"]:
            assert event["after"]["actors"][actor_id]["stanceHistory"][-2]["expiredAt"] == event["time"]
    if actor_id == "W20" and event["time"] == 6.0:
        assert event["after"]["actors"][actor_id]["magicThisTurn"] is False
marker_events = [e for e in events if e["kind"] == "OBSERVATION_ONLY_DEADLINE_NOOP"]
assert len(marker_events) == 1
marker = marker_events[0]
assert marker["time"] == 20.0
assert marker["authoredInputs"]["classification"] == "TEST_ONLY observation-only marker; not a campaign or engine timer"
assert marker["authoredInputs"]["result"] == "NO_OP" and marker["authoredInputs"]["onceOnly"] is True
assert marker["authoredInputs"]["orderedAfter"] == "Guard regular start at 20.0"
assert marker["before"]["clocks"]["otherIndependentDeadlines"]["fixture-independence-marker-365"] == 20.0
assert "fixture-independence-marker-365" not in marker["after"]["clocks"]["otherIndependentDeadlines"]
assert marker["after"]["clockReceipts"]["fixture-independence-marker-365"]["result"] == "NO_OP"
assert marker["after"]["clockReceipts"]["fixture-independence-marker-365"]["inWorldConsequence"] is False
prior_guard_start = next(e for e in events if e["kind"] == "REGULAR_START" and e["time"] == 20.0 and e["authoredInputs"]["actorId"] == TARGET_ID)
assert marker["before"] == prior_guard_start["after"]
assert "fixture-independence-marker-365" not in case["final"]["clocks"]["otherIndependentDeadlines"]
assert case["final"]["clockReceipts"]["fixture-independence-marker-365"]["handledAt"] == 20.0

return_event = next(e for e in events if e["kind"] == "CELL_DEADLINE_AND_LAWFUL_RETURN")
returned = return_event["after"]
returned_actor = returned["actors"][TARGET_ID]
returned_cell = returned["cells"][CELL_ID]
returned_gate = returned["effects"][GATE_ID]
assert return_event["time"] == 62.05
assert returned_actor["plane"] == "fixture:origin" and returned_actor["position"] == cell["originAnchor"]["position"]
assert returned_actor["bodyBoxWorld"] == cell["originAnchor"]["bodyBox"]
assert returned_actor["lifeClassification"] == target["lifeClassification"] and returned_actor["HP"] == target["HP"]
assert returned_cell["status"] == "destroyed" and returned_cell["closeCount"] == 1 and returned_cell["closedAt"] == 62.05
assert returned_gate["status"] == "active" and returned_gate["concentration"] is True
assert returned_gate["cells"] == [] and returned_gate["admissions"] == [CELL_ID]
assert returned["hardDenialClaims"] == initial["hardDenialClaims"]
assert returned["settlements"][-1]["sameIdentityPreserved"] is True

cross_event = next(e for e in events if e["kind"] == "LATER_PAID_CROSSING_NO_SECOND_ADMISSION")
cross = cross_event["after"]
actor_after_cross = cross["actors"][TARGET_ID]
gate_after_cross = cross["effects"][GATE_ID]
new_id = f"{GATE_ID}/crossing/2"
new_receipt = cross["crossingReceipts"][new_id]
assert cross_event["time"] == 62.1 and cross_event["authoredInputs"]["actualTurnStartedAt"] == 62.0
assert cross_event["authoredInputs"]["movementSpentFeet"] == 5
assert actor_after_cross["movement"] == 35
assert actor_after_cross["movementHistory"][-1]["feetSpent"] == 5
assert cross_event["authoredInputs"]["mobileAllowanceUsedFeet"] == 5
assert actor_after_cross["stance"]["id"] == "Mobile" and actor_after_cross["stance"]["expiresAtNextRegularStart"] == 68.0
assert actor_after_cross["mobileFirstFiveFeetAllowance"]["usedFeet"] == 5
assert actor_after_cross["mobileFirstFiveFeetAllowance"]["remainingFeet"] == 0
assert actor_after_cross["mobileFirstFiveFeetAllowance"]["usedAt"] == 62.1
assert actor_after_cross["mobileFirstFiveFeetAllowance"]["grantsFreeMovement"] is False
assert actor_after_cross["movementHistory"][-1]["from"] == [2.5, -2.5, 0]
assert actor_after_cross["movementHistory"][-1]["to"] == [-2.5, -2.5, 0]
assert new_receipt["completeBodyCrossing"] is True and new_receipt["outcome"] == "NO_ADMISSION_EXISTING_HARD_DENIAL_CLAIM"
assert new_receipt["existingClaimId"] == "claim-Guard-365" and new_receipt["claimSpent"] is False
assert new_receipt["cellId"] is None and new_receipt["admittedAt"] is None
assert gate_after_cross["status"] == "active" and gate_after_cross["cells"] == []
assert gate_after_cross["admissions"] == [CELL_ID]
assert cross["hardDenialClaims"] == initial["hardDenialClaims"]
assert len(cross["cells"]) == 1 and cross["cells"][CELL_ID]["status"] == "destroyed"
assert actor_after_cross["plane"] == "fixture:origin"

for kind, expected_id in (("DUPLICATE_CROSSING_DELIVERY_RETURNS_EXISTING_RECEIPT", new_id),
                          ("DUPLICATE_ORIGINAL_DELIVERY_RETURNS_EXISTING_RECEIPT", first_id)):
    event = next(e for e in events if e["kind"] == kind)
    receipt = event["authoredInputs"]["returnedReceipt"]
    assert event["before"] == event["after"] and event["forward"] == event["inverse"] == []
    assert event["authoredInputs"]["crossingId"] == expected_id
    assert receipt["id"] == expected_id and receipt == event["before"]["crossingReceipts"][expected_id]
    assert event["authoredInputs"]["returnedReceiptSha256"] == sha(receipt)
assert events[-1]["after"]["effects"][GATE_ID]["admissions"] == [CELL_ID]
assert events[-1]["after"]["hardDenialClaims"] == initial["hardDenialClaims"]
assert case["assertions"]["laterCrossingCreatesNoSecondCellOrClaim"]
assert case["assertions"]["duplicateLaterCrossingReturnsExistingReceipt"]
assert case["assertions"]["duplicateOriginalCrossingReturnsExistingReceipt"]
assert case["assertions"]["identityAccepted"] is False and case["assertions"]["identityApplied"] is False

with zipfile.ZipFile(ARCHIVE) as zf:
    names = zf.namelist()
    assert len(names) == len(set(names)) and zf.testzip() is None
    manifest = json.loads(zf.read("MANIFEST.json"))
    assert len(names) == len(manifest["members"]) + 2
    checked = 0
    for member in manifest["members"]:
        data = zf.read(member["path"])
        assert len(data) == member["bytes"] and file_sha(data) == member["sha256"]
        assert f"{zlib.crc32(data) & 0xffffffff:08x}" == member["crc32"]
        checked += 1
    archived_case = json.loads(zf.read("W04_RETURNED_TARGET_CASE_365_REPACK02.json"))
    assert archived_case == case
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack06_TESTONLY.zip")) == seal["archiveSha256"]
    previous_archive = zf.read("prior/DD_Rank9_BanishmentGate_W04_ReturnedTarget_365_Repack01_TESTONLY.zip")
    assert file_sha(previous_archive) == case["supersedesSubmissions"]["supersedes"]["archiveSha256"]
    assert "prior/PG327_W04_DIRECTOR_HOLD_365_REPACK01.json" in names

archive_bytes = ARCHIVE.read_bytes()
delivery = load(OUT / "ARCHIVE_DELIVERY_365_W04_REPACK02.json")
assert delivery["bytes"] == len(archive_bytes) and delivery["sha256"] == file_sha(archive_bytes)
assert delivery["zipTest"] == "PASS" and delivery["memberCount"] == len(names)
report = {
    "id": "PG327-W04-INDEPENDENT-AUDIT-365-REPACK02",
    "status": "PASS_TESTONLY_W04_RETURNED_TARGET_CROSSING_AND_TIMELINE; DIRECTOR_REVIEW_REQUIRED",
    "archive": ARCHIVE.name, "archiveBytes": len(archive_bytes), "archiveSha256": file_sha(archive_bytes),
    "memberCount": len(names), "payloadHashesAndCrcsVerified": checked,
    "priorSealedWitness": "W06; exact archive hash and event-7 admission snapshot verified",
    "sourceBindings": 1, "eventCount": len(events), "forwardReplay": "PASS",
    "turnLifecycle": "40 regular starts and 40 regular ends; resources expire, Reaction persists, nextEnd advances, W20 magicThisTurn resets",
    "stanceLifecycle": "All 40 starts record fixture-only Mobile before activity/idle end; previous stances/allowances expire; later crossing pays movement and consumes 5-foot allowance",
    "observationMarker": "Single 20.0 no-op receipt ordered after Guard start; no in-world effect and no unresolved marker remains",
    "supersededW04Repack01": "Archive, independent audit, delivery record, and Director HOLD preserved in packet history",
    "inverseReplay": "PASS; exact post-admission fork state restored",
    "cellReturn": "Same living Guard returned at independent 62.05 deadline; Gate remains active to 600.2",
    "laterCrossing": "Five feet paid on actual Guard turn; no second cell or refreshed claim",
    "duplicateDelivery": "Both later crossing receipt and original successful receipt reused unchanged",
    "identityDecision": "HOLD", "spellAccepted": False, "spellApplied": False,
    "applicationAuthorized": False, "queueAuthority": "Queue361: 828 applied / 20 pending / 0 accepted-unapplied"
}
(OUT / "INDEPENDENT_AUDIT_365_W04_REPACK02.json").write_text(json.dumps(report, indent=2) + "\n", encoding=ENC)
print(json.dumps(report, indent=2))
