from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness363"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W07_GustCorpse_363_TESTONLY.zip"
CASE_PATH = PACK / "W07_GUST_CORPSE_CASE_363.json"
ENC = "utf-8"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def root_patch(state, patch):
    current = copy.deepcopy(state)
    assert len(patch) == 2
    assert patch[0]["op"] == "test" and patch[0]["path"] == ""
    assert patch[1]["op"] == "replace" and patch[1]["path"] == ""
    assert current == patch[0]["value"]
    return copy.deepcopy(patch[1]["value"])


case = load(CASE_PATH)
bindings = load(PACK / "SOURCE_BINDINGS_363.json")
extracts = load(PACK / "SOURCE_EXTRACTS_363.json")
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
source_audit = load(PACK / "authority/PG327_W03_W06_W07_SOURCE_AUDIT_362.json")

assert case["spellId"] == "banishment-gate" and case["witnessId"] == "W07"
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert case["initialSHA256"] == sha(case["initial"])
assert case["finalSHA256"] == sha(case["final"])

state = copy.deepcopy(case["initial"])
for event in case["events"]:
    assert event["before"] == state
    assert event["beforeSHA256"] == sha(state)
    state = root_patch(state, event["forward"])
    assert state == event["after"]
    assert event["afterSHA256"] == sha(state)
assert state == case["final"]

for event in reversed(case["events"]):
    assert event["after"] == state
    state = root_patch(state, event["inverse"])
    assert state == event["before"]
assert state == case["initial"]
assert case["inverseRestorationOrder"] == [event["id"] for event in reversed(case["events"])]
assert [event["time"] for event in case["events"]] == sorted(event["time"] for event in case["events"])

start = case["initial"]["actors"]["Guard-W07-TESTONLY"]
crossing = next(e for e in case["events"] if e["kind"] == "FORCED_MOVEMENT_AND_ADMISSION")
crossed = crossing["after"]
guard = crossed["actors"]["Guard-W07-TESTONLY"]
death_event = next(e for e in case["events"] if e["kind"] == "SCHEDULED_DEATH_SAVE")
dead = death_event["after"]["actors"]["Guard-W07-TESTONLY"]
closure = next(e for e in case["events"] if e["kind"] == "GATE_CONCENTRATION_END_AND_CELL_CLOSURE")
final_guard = closure["after"]["actors"]["Guard-W07-TESTONLY"]
assert start["HP"] == 0 and start["death"]["status"] == "dying" and start["death"]["failures"] == 2
assert start["conditions"] == ["Unconscious", "Prone"]
assert start["noAbilityScoresProvided"] is True
assert start["bodyBoxWorld"] == {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 1]}
assert crossed["crossingReceipts"][guard["crossingReceiptId"]]["completeBodyCrossing"] is True
assert guard["originPlaneAdmissionBox"] == {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}
assert guard["cellLocalBodyBox"] == {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 1]}
assert guard["saveOutcome"]["result"] == "automaticFailure" and guard["saveOutcome"]["die"] is None
assert dead["death"]["status"] == "dead" and dead["death"]["failures"] == 3
assert dead["death"]["saveInputs"][-1]["d20"] == 5
assert dead["death"]["saveInputs"][-1]["woundSave"].startswith("not triggered")
assert dead["corpseIdentity"] == "Guard-W07-TESTONLY" and dead["heldItems"] == []
assert dead["carriedItemIds"] == ["G01-paper-token"]
assert final_guard["id"] == guard["id"] and final_guard["corpseIdentity"] == dead["corpseIdentity"]
assert final_guard["plane"] == "fixture:origin" and final_guard["position"] == [2.5, 0, 0]
assert closure["after"]["effects"]["BG-W07-TESTONLY-CELL-363"]["closeCount"] == 1
assert closure["after"]["effects"]["BG-W07-TESTONLY-GATE-363"]["closeCount"] == 1
assert closure["after"]["items"]["G01-paper-token"]["location"]["carrierId"] == final_guard["id"]
assert closure["after"]["closureReceipts"][0]["duplicateBodyCreated"] is False
assert closure["after"]["closureReceipts"][0]["refund"] == 0

assert queue["currentAuthority"]["reviewedApplied"] == 828
assert queue["currentAuthority"]["pending"] == 20
assert queue["currentAuthority"]["acceptedUnapplied"] == 0
assert source_audit["directorRuling"]["decision"] == "HOLD"
assert source_audit["witnessSources"]["W03"]["status"] == "SOURCE_HOLD_NO_QUALIFYING_ACCEPTED_SOURCE_FOUND"
assert source_audit["witnessSources"]["W07"]["status"] == "SOURCE_ROUTE_APPROVED_WITNESS_OUTSTANDING"
assert case["coverage"]["W03"] == "source gap remains open"

with zipfile.ZipFile(ARCHIVE, "r") as zf:
    assert zf.testzip() is None
    names = zf.namelist()
    assert len(names) == len(set(names))
    packet_manifest = json.loads(zf.read("MANIFEST.json"))
    assert len(names) == len(packet_manifest["members"]) + 2
    checked = 0
    for member in packet_manifest["members"]:
        data = zf.read(member["path"])
        assert len(data) == member["bytes"]
        assert file_sha(data) == member["sha256"]
        checked += 1
    assert checked == len(packet_manifest["members"])
    catalog = json.loads(zf.read("sources/catalog.json"))
    gate_entry = next(item for item in catalog["spells"] if item["id"] == "banishment-gate")
    gust_entry = next(item for item in catalog["spells"] if item["id"] == "gust")["operational"]
    bestiary = json.loads(zf.read("sources/bestiary_data_full.json"))
    assert gate_entry == extracts["gate"]["catalogEntry"]
    assert gust_entry == extracts["gust"]["card"]
    assert bestiary[326] == extracts["guard"]["profile"]
    included = {b["repositoryPath"]: b for b in bindings["bindings"] if b.get("sourceCommit") == bindings["sourceCommit"]}
    for binding in included.values():
        data = zf.read(binding["packetMember"])
        assert len(data) == binding["gitBytes"]
        assert file_sha(data) == binding["gitSha256"]
        original = subprocess.check_output(["git", "show", f"{binding['sourceCommit']}:{binding['repositoryPath']}"], cwd=ROOT)
        assert file_sha(original) == binding["gitSha256"]

report = {
    "id": "PG327-W07-INDEPENDENT-AUDIT-363",
    "status": "PASS_PACKET_INTEGRITY_AND_W07_REPLAY; DIRECTOR_SEAL_REQUIRED",
    "archive": ARCHIVE.name,
    "archiveBytes": ARCHIVE.stat().st_size,
    "archiveSha256": file_sha(ARCHIVE.read_bytes()),
    "archiveZipCrc": "PASS",
    "memberHashesVerified": checked,
    "gitSourceBindingsVerified": len(included),
    "eventCount": len(case["events"]),
    "forwardReplay": "PASS",
    "inverseReplay": "PASS exact reverse-order restoration",
    "sameCorpseAndTokenReturn": "PASS",
    "spellAccepted": False,
    "spellApplied": False,
    "applicationAuthorized": False,
    "w03": "OPEN SOURCE GAP",
    "queueAuthority": "Queue361: 828 applied / 20 pending / 0 accepted-unapplied",
}
out = OUT / "INDEPENDENT_AUDIT_363.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(report, ensure_ascii=False, indent=2))
