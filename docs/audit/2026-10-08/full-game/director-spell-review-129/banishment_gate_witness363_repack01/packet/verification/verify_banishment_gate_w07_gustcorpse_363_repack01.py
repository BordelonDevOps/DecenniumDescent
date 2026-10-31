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
OUT = BASE / "banishment_gate_witness363_repack01"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W07_GustCorpse_363_Repack01_TESTONLY.zip"
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


def parts(pointer):
    if not pointer:
        return []
    if not pointer.startswith("/"):
        raise AssertionError(f"Invalid JSON pointer: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def get_at(value, pointer):
    for part in parts(pointer):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(value, pointer):
    path_parts = parts(pointer)
    assert path_parts, "Root-path mutation is forbidden"
    parent = value
    for part in path_parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, path_parts[-1]


def apply_patch(state, operations):
    current = copy.deepcopy(state)
    for operation in operations:
        pointer = operation["path"]
        assert pointer, "Root-path patch is forbidden"
        kind = operation["op"]
        if kind == "test":
            assert get_at(current, pointer) == operation["value"], f"Precondition failed at {pointer}"
        elif kind == "replace":
            parent, key = parent_at(current, pointer)
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                assert key in parent, f"Replace target missing at {pointer}"
                parent[key] = copy.deepcopy(operation["value"])
        elif kind == "add":
            parent, key = parent_at(current, pointer)
            assert isinstance(parent, dict) and key not in parent, f"Add target is not an absent object field at {pointer}"
            parent[key] = copy.deepcopy(operation["value"])
        elif kind == "remove":
            parent, key = parent_at(current, pointer)
            assert isinstance(parent, dict) and key in parent, f"Remove target missing at {pointer}"
            del parent[key]
        else:
            raise AssertionError(f"Unsupported JSON Patch operation: {kind}")
    return current


def changed_paths(before, after, pointer=""):
    if type(before) is dict and type(after) is dict:
        result = []
        for key in sorted(before.keys() | after.keys()):
            child = pointer + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                result.append(child)
            else:
                result.extend(changed_paths(before[key], after[key], child))
        return result
    if type(before) is type(after) and before == after:
        return []
    assert pointer, "Top-level state schema unexpectedly changed"
    return [pointer]


case = load(CASE_PATH)
bindings = load(PACK / "SOURCE_BINDINGS_363.json")
extracts = load(PACK / "SOURCE_EXTRACTS_363.json")
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
source_audit = load(PACK / "authority/PG327_W03_W06_W07_SOURCE_AUDIT_362.json")

assert case["id"] == "W07_GUST_CORPSE_CASE_363_REPACK01"
assert case["spellId"] == "banishment-gate" and case["witnessId"] == "W07"
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert case["initialSHA256"] == sha(case["initial"])
assert case["finalSHA256"] == sha(case["final"])
assert len(case["events"]) == 10

state = copy.deepcopy(case["initial"])
for event in case["events"]:
    assert event["before"] == state
    assert event["beforeSHA256"] == sha(state)
    mutations = [op for op in event["forward"] if op["op"] != "test"]
    assert all(op["path"] for op in event["forward"] + event["inverse"])
    assert all(op["op"] in {"test", "add", "remove", "replace"} for op in event["forward"] + event["inverse"])
    assert sorted(op["path"] for op in mutations) == sorted(changed_paths(event["before"], event["after"]))
    state = apply_patch(state, event["forward"])
    assert state == event["after"]
    assert event["afterSHA256"] == sha(state)
assert state == case["final"]

for event in reversed(case["events"]):
    assert event["after"] == state
    state = apply_patch(state, event["inverse"])
    assert state == event["before"]
assert state == case["initial"], "Inverse patch replay did not restore every field"
assert case["inverseRestorationOrder"] == [event["id"] for event in reversed(case["events"])]
assert [event["time"] for event in case["events"]] == sorted(event["time"] for event in case["events"])
assert "all ten transitions" in (PACK / "README.md").read_text(encoding=ENC)

# Both actual interruption windows now include the one eligible opposite Wizard.
windows = []
for event in case["events"]:
    pending = event["after"].get("pendingCast")
    if pending:
        window = pending.get("counterspellWindow")
        if window:
            windows.append((pending, window, event["after"]))
assert len(windows) == 2
for pending, window, snapshot in windows:
    caster_id = pending["casterId"]
    reactor_id = "W17" if caster_id == "W20" else "W20"
    reactor = snapshot["actors"][reactor_id]
    assert len(window["eligibleReactors"]) == 1
    eligible = window["eligibleReactors"][0]
    assert eligible["actorId"] == reactor_id
    assert eligible["automaticCardId"] == "wizard.base.counterspell"
    assert eligible["distanceFeet"] == 24 and eligible["distanceFeet"] <= eligible["rangeFeet"] == 60
    assert eligible["perceivesCast"] and eligible["lineOfEffect"] and eligible["reactionAvailable"]
    assert eligible["rechargeReady"] and eligible["currentRP"] == reactor["RP"] >= eligible["costRP"] == 3
    assert eligible["componentsAvailable"] == ["V", "S", "F"]
    assert eligible["freeSomaticHand"] in reactor["freeHands"]
    focus = snapshot["items"][eligible["focusId"]]
    assert focus["heldBy"] == reactor_id and focus["hand"] != eligible["freeSomaticHand"]
    assert reactor["reaction"] == 1
    assert reactor["recharge"]["wizard.base.counterspell"]["ready"] is True
    assert eligible["decision"] == "declines" and not eligible["attempted"]
    assert not eligible["reactionSpent"] and eligible["RPSpent"] == 0 and not eligible["cooldownChanged"]
    assert "TEST_ONLY" in eligible["decisionPremise"]
    assert all(item["actorId"] != reactor_id for item in window["ineligible"])

initial_actors = case["initial"]["actors"]
assert (initial_actors["W20"]["HP"], initial_actors["W20"]["maxHP"]) == (122, 122)
assert (initial_actors["W17"]["HP"], initial_actors["W17"]["maxHP"]) == (104, 104)
for actor_id, focus_id in (("W20", "focus-W20"), ("W17", "focus-W17")):
    actor = initial_actors[actor_id]
    item = case["initial"]["items"][focus_id]
    assert actor["focusId"] == focus_id and actor["focusAccessible"]
    assert actor["heldItems"] == [focus_id] and actor["freeHands"] == ["right"]
    assert item["heldBy"] == actor_id and item["hand"] == "left"
assert extracts["counterspell"]["operationalCard"]["rangeFeet"] == 60
assert extracts["counterspell"]["operationalCard"]["components"] == ["V", "S", "F"]
assert extracts["counterspell"]["Wizard20"]["automaticCard"]["id"] == "wizard.base.counterspell"
assert extracts["counterspell"]["Wizard17"]["automaticCard"]["id"] == "wizard.base.counterspell"
assert extracts["counterspell"]["Wizard17"]["alwaysPreparedId"] == "wizard.base.counterspell"
assert "always-prepared" in extracts["counterspell"]["Wizard17"]["alwaysPreparedRule"]
assert "always-prepared class matrices" in extracts["counterspell"]["wizardClassRuleLine44"]
assert "Counterspell" in extracts["counterspell"]["wizardClassRuleLine72"]
assert "automatically gains Counterspell" in extracts["counterspell"]["wizardClassRuleLine72"]
assert all("recharge 2 rounds" in extracts["counterspell"][actor]["automaticCard"]["frequency"] for actor in ("Wizard20", "Wizard17"))

# The case field must use the exact included Git version; local working bytes remain provenance.
guard_binding = next(item for item in bindings["bindings"] if item["repositoryPath"] == "src/bestiary_data_full.json")
guard_actor = initial_actors["Guard-W07-TESTONLY"]
assert guard_actor["profileSHA256"] == guard_binding["gitSha256"]
assert guard_actor["profileWorkingTreeSHA256"] == guard_binding["workingTreeSha256"]
assert extracts["guard"]["gitSourceSha256"] == guard_binding["gitSha256"]
assert extracts["guard"]["workingTreeSha256"] == guard_binding["workingTreeSha256"]
assert case["sourceBindings"]["Guard"]["gitSha256"] == guard_binding["gitSha256"]
assert case["sourceBindings"]["Guard"]["sha256WorkingTree"] == guard_binding["workingTreeSha256"]

# Check the turn markers and the 120-foot placement range corrected in Repack01.
for actor_id, turn_end, next_end in (("W20", 0.9, 6.9), ("W17", 1.9, 7.9)):
    expected_start = 0.0 if actor_id == "W20" else 1.0
    start_event = next(e for e in case["events"] if e["kind"] == "REGULAR_START" and e["after"]["actors"][actor_id]["regularSchedule"]["starts"] == [expected_start])
    end_event = next(e for e in case["events"] if e["kind"] == "TURN_END" and e["after"]["actors"][actor_id]["regularSchedule"]["ends"] == [turn_end])
    started = start_event["after"]["actors"][actor_id]["regularSchedule"]
    ended = end_event["after"]["actors"][actor_id]["regularSchedule"]
    assert started["starts"] == [expected_start]
    assert len(started["budgetHistory"]) == 1
    assert ended["ends"] == [turn_end] and ended["nextEnd"] == next_end
gate_event = next(e for e in case["events"] if e["kind"] == "CAST_COMMIT" and e["after"].get("pendingCast", {}).get("spellId") == "banishment-gate")
gate_inputs = gate_event["authoredInputs"]
assert gate_inputs["rangeFeet"] == gate_inputs["rangeSourceFeet"] == extracts["gate"]["pointPlacementRangeFeet"] == 120
assert gate_inputs["casterBasePositionFeet"] == initial_actors["W20"]["position"] == [-50, 0, 0]
assert gate_inputs["point"] == [0, 0, 7.5]
assert gate_inputs["distanceModel"].startswith("3D Euclidean")
assert math.isclose(gate_inputs["distanceFeet"], math.dist(gate_inputs["casterBasePositionFeet"], gate_inputs["point"]), rel_tol=0, abs_tol=1e-10)
assert gate_inputs["distanceFeet"] <= gate_inputs["rangeFeet"]

# Existing lifecycle and scope assertions remain intact.
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
assert case["supersedesArchiveSha256"] == "16b2d61a6f2d252bea543802be00aa7dd687ec0a757345f52139c676862938cf"
original_archive = BASE / "banishment_gate_witness363/DD_Rank9_BanishmentGate_W07_GustCorpse_363_TESTONLY.zip"
assert file_sha(original_archive.read_bytes()) == case["supersedesArchiveSha256"]

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
    manifest = json.loads(zf.read("MANIFEST.json"))
    assert len(names) == len(manifest["members"]) + 2
    checked = 0
    for member in manifest["members"]:
        data = zf.read(member["path"])
        assert len(data) == member["bytes"]
        assert file_sha(data) == member["sha256"]
        assert f"{zlib.crc32(data) & 0xffffffff:08x}" == member["crc32"]
        checked += 1
    assert checked == len(manifest["members"])
    archived_case = json.loads(zf.read("W07_GUST_CORPSE_CASE_363.json"))
    assert archived_case == case
    source_catalog = json.loads(zf.read("sources/catalog.json"))
    bestiary = json.loads(zf.read("sources/bestiary_data_full.json"))
    assert bestiary[326] == extracts["guard"]["profile"]
    included = {binding["repositoryPath"]: binding for binding in bindings["bindings"] if binding.get("sourceCommit") == bindings["sourceCommit"]}
    for binding in included.values():
        data = zf.read(binding["packetMember"])
        assert len(data) == binding["gitBytes"]
        assert file_sha(data) == binding["gitSha256"]
        original = subprocess.check_output(["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'], cwd=ROOT)
        assert file_sha(original) == binding["gitSha256"]
    source_counterspell = next(item for item in source_catalog["spells"] if item.get("id") == "counterspell")["operational"]
    assert source_counterspell == extracts["counterspell"]["operationalCard"]
    source_gate = next(item for item in source_catalog["spells"] if item.get("id") == "banishment-gate")
    assert source_gate == extracts["gate"]["catalogEntry"]
    source_gust = next(item for item in source_catalog["spells"] if item.get("id") == "gust")["operational"]
    assert source_gust == extracts["gust"]["card"]

delivery = load(OUT / "ARCHIVE_DELIVERY_363_REPACK01.json")
archive_bytes = ARCHIVE.read_bytes()
assert delivery["bytes"] == len(archive_bytes)
assert delivery["sha256"] == file_sha(archive_bytes)
assert delivery["memberCount"] == len(names)
assert delivery["allMemberHashesAndCrcsVerified"] is True and delivery["zipTest"] == "PASS"

report = {
    "id": "PG327-W07-INDEPENDENT-AUDIT-363-REPACK01",
    "status": "PASS_PACKET_INTEGRITY_AND_W07_REPLAY; DIRECTOR_SEAL_REQUIRED",
    "archive": ARCHIVE.name,
    "archiveBytes": len(archive_bytes),
    "archiveSha256": file_sha(archive_bytes),
    "archiveZipCrc": "PASS",
    "memberHashesAndCrcsVerified": checked,
    "gitSourceBindingsVerified": len(included),
    "eventCount": len(case["events"]),
    "forwardReplay": "PASS with field-scoped mutations and preconditions",
    "inverseReplay": "PASS exact reverse-order restoration; unchanged fields preserved",
    "counterspellWindows": "PASS: both opposite Wizards eligible; both cost-free TEST_ONLY declines recorded",
    "casterHPAndFocusCustody": "PASS",
    "guardGitBoundProfileHash": "PASS; working-tree hash retained separately",
    "turnCalendar": "PASS: single start refresh; W20 next end 6.9; W17 next end 7.9",
    "gatePlacementRange": "PASS: sourced 120 feet",
    "sameCorpseAndTokenReturn": "PASS",
    "spellAccepted": False,
    "spellApplied": False,
    "applicationAuthorized": False,
    "w03": "OPEN SOURCE GAP",
    "queueAuthority": "Queue361: 828 applied / 20 pending / 0 accepted-unapplied",
}
out = OUT / "INDEPENDENT_AUDIT_363_REPACK01.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(report, ensure_ascii=False, indent=2))
