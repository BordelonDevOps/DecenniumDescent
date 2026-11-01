#!/usr/bin/env python3
"""Independent package and reversible-state audit for Fortress W02 Repack420."""

from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "fortress_w02_scribing_witness_420_repack02"
PACKET = OUT / "DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_420_Repack02_TESTONLY.zip"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha(canonical(value))


def load_json(raw: bytes) -> Any:
    return json.loads(raw)


def parts(pointer: str) -> list[str]:
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def apply_operations(state: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for operation in operations:
        path = parts(operation["path"])
        if not path:
            raise ValueError("Root operations are not permitted")
        parent = result
        for part in path[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = path[-1]
        if operation["op"] == "add":
            if isinstance(parent, list):
                parent.insert(int(key), copy.deepcopy(operation["value"]))
            else:
                if key in parent:
                    raise ValueError(f"Cannot add existing key {operation['path']}")
                parent[key] = copy.deepcopy(operation["value"])
        elif operation["op"] == "remove":
            if isinstance(parent, list):
                del parent[int(key)]
            else:
                del parent[key]
        elif operation["op"] == "replace":
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                parent[key] = copy.deepcopy(operation["value"])
        else:
            raise ValueError(f"Unexpected operation {operation['op']}")
    return result


def audit_replay(branch: dict[str, Any], parent_state: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    if branch["status"] != "DIRECTOR_REVIEW_PENDING":
        raise ValueError("A branch is not pending director review")
    if branch["scope"]["branchId"] != "PG366-W02-R1" or branch["scope"]["witnessId"] != "PG328-W02":
        raise ValueError("Branch scope escaped PG328-W02 / PG366-W02-R1")
    if branch["ownerAdoptedPremises"]["proposalSha256"] != "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930":
        raise ValueError("Branch no longer binds exact owner-adopted Proposal 415")
    if branch["lineage"]["parentFinalStateSha256"] != digest(parent_state):
        raise ValueError("Branch parent state hash differs from immutable Return284 state")
    initial = branch["initial"]
    if digest(initial) != branch["initialSHA256"]:
        raise ValueError("Initial full-state hash mismatch")
    initial_parent = {key: value for key, value in initial.items() if key != "w02TestOnlyScenario"}
    if initial_parent != parent_state:
        raise ValueError("TEST_ONLY scenario seed changed the preserved parent fork state")
    overlay = initial["w02TestOnlyScenario"]
    if overlay["ownerAdoptionSha256"] != branch["ownerAdoptedPremises"]["adoptionSha256"]:
        raise ValueError("Initial scenario overlay has a different owner-adoption binding")
    book = overlay["worksite"]["spellbook"]
    if book["existingContentsIds"] != profile["spellbook"] or "flame-armor" in book["existingContentsIds"]:
        raise ValueError("Initial book contents differ from the bound profile or already include Flame Armor")
    if book["existingContentsDigest"] != digest(profile["spellbook"]):
        raise ValueError("Initial spellbook contents digest is incorrect")

    events = branch["events"]
    if len(events) != 6:
        raise ValueError("Each W02 branch must contain exactly six replayable events")
    expected_kinds = [
        "TEST_ONLY_INITIATIVE_EXIT",
        "TEST_ONLY_BOOK_UNPACK_AND_SETUP_COMPLETE",
        "SETTLE_INHERITED_SPELL_EFFICIENCY_DEADLINE_ONCE",
        "TEST_ONLY_SCRIBING_START_AND_INPUT_COMMITMENT",
        "TEST_ONLY_SCRIBING_COMPLETION" if branch["scope"]["branchKind"] == "completion" else "TEST_ONLY_SCRIBING_ABANDONMENT",
        "TEST_ONLY_BOOK_REPACK_AFTER_TERMINAL",
    ]
    timing = branch["ownerAdoptedPremises"]["exactProposedOwnerPremises"]["timingAndOutcomes"]
    expected_times = [
        timing["preservedEndThenInitiativeExitAtSeconds"],
        timing["setupCompleteBySeconds"],
        timing["settleInheritedSpellEfficiencyDeadlineOnceAtSeconds"],
        timing["workStartsAtSeconds"],
        branch["terminalOutcome"]["eventTimeSeconds"],
        branch["terminalOutcome"]["eventTimeSeconds"],
    ]
    if [event["time"] for event in events] != expected_times:
        raise ValueError("W02 event times differ from the exact adopted initiative/setup/deadline/work sequence")
    expected_duration = 3600 if branch["scope"]["branchKind"] == "completion" else 1800
    if branch["terminalOutcome"]["productiveDurationSeconds"] != expected_duration:
        raise ValueError("Branch productive duration differs from the adopted outcome")
    state = copy.deepcopy(initial)
    for index, event in enumerate(events):
        if event["kind"] != expected_kinds[index]:
            raise ValueError(f"Unexpected W02 event order or kind at {event['id']}")
        if digest(event["before"]) != event["beforeSHA256"] or event["before"] != state:
            raise ValueError(f"Before-state continuity/hash failure at {event['id']}")
        state = apply_operations(state, event["forward"])
        if state != event["after"] or digest(state) != event["afterSHA256"]:
            raise ValueError(f"Forward operation replay/hash failure at {event['id']}")
        if state["time"] != event["time"]:
            raise ValueError(f"Event time does not match full-state time at {event['id']}")
        if index == 0 and (state["mode"] != "outside-initiative" or state["w02TestOnlyScenario"]["initiativeDispatchEnabled"] is not False):
            raise ValueError("The inherited 0.9 end did not explicitly exit initiative and suspend future dispatch")
        if index == 1 and (state["items"]["cargo-A"]["massLb"] != 7 or state["items"]["cargo-A"]["load"] != 0.7 or state["actors"]["A"]["carriedWeightLb"] != 9 or state["actors"]["A"]["carriedLoad"] != 0.9 or state["w02TestOnlyScenario"]["worksite"]["spellbook"]["location"] != "FORTRESS-TABLE-W02-01"):
            raise ValueError("The book unpack/setup event does not reconcile the adopted interim cargo/carried weights")
        if index == 3:
            supplies = state["w02TestOnlyScenario"]["worksite"]["supplies"]
            if any(row["contentsStatus"] != "COMMITTED_TO_THIS_ATTEMPT" for row in supplies["inkBottles"]) or supplies["paperSheets"]["status"] != "COMMITTED_TO_THIS_ATTEMPT":
                raise ValueError("The 7.0 event did not commit all adopted materials to this attempt")
        if index == 4 and (state["actors"]["A"]["carriedWeightLb"] != 9 or state["w02TestOnlyScenario"]["worksite"]["spellbook"]["location"] != "FORTRESS-TABLE-W02-01"):
            raise ValueError("The terminal outcome is not recorded before the separate book repack")
        if index == 5 and (state["items"]["cargo-A"]["massLb"] != 10 or state["items"]["cargo-A"]["load"] != 1 or state["actors"]["A"]["carriedWeightLb"] != 12 or state["actors"]["A"]["carriedLoad"] != 1.2 or state["w02TestOnlyScenario"]["worksite"]["spellbook"]["location"] != "cargo-A"):
            raise ValueError("The separate book-repack event does not restore the adopted 10/12 lb load")
        if apply_operations(event["after"], event["inverse"]) != event["before"]:
            raise ValueError(f"Event inverse operations do not restore before-state at {event['id']}")

    if state != branch["final"] or digest(state) != branch["finalSHA256"]:
        raise ValueError("Forward replay does not reach the bound terminal full state")
    restoration = branch["inverseRestorationOrder"]
    if restoration != [event["id"] for event in reversed(events)]:
        raise ValueError("Declared inverse restoration order is not reverse chronological")
    reverse_state = copy.deepcopy(state)
    for event in reversed(events):
        reverse_state = apply_operations(reverse_state, event["inverse"])
        if digest(reverse_state) != event["beforeSHA256"]:
            raise ValueError(f"Full reverse traversal hash mismatch at {event['id']}")
    if reverse_state != initial:
        raise ValueError("Full reverse traversal does not restore exact scenario initial state")

    is_completion = branch["scope"]["branchKind"] == "completion"
    final = branch["final"]
    scenario = final["w02TestOnlyScenario"]
    outcome = branch["terminalOutcome"]
    if final["time"] != outcome["eventTimeSeconds"]:
        raise ValueError("Terminal time differs from branch assertion")
    if final["clock"]["elapsedSeconds"] != outcome["elapsedClockSeconds"]:
        raise ValueError("Terminal elapsed clock differs from branch assertion")
    for clock_name in ("OpeningRemaining", "HornRemaining", "Hunt"):
        if final["clock"][clock_name] != outcome["worldClocks"][clock_name]:
            raise ValueError(f"Terminal world clock differs from assertion: {clock_name}")
    if final["clock"]["Hunt"] is not None or outcome["actorA"]["RP"] != 54:
        raise ValueError("A new Hunt clock or RP/resource change was introduced")
    expected_status = "COMPLETED" if is_completion else "ABANDONED"
    if scenario["status"] != expected_status or final["work"] is not None:
        raise ValueError("Terminal work state is not complete/abandoned with no active work")
    if len(scenario["worksite"]["spellbook"]["copiedEntries"]) != int(is_completion):
        raise ValueError("Branch has an incorrect count of copied entries")
    if is_completion:
        entry = scenario["worksite"]["spellbook"]["copiedEntries"][0]
        if entry != outcome["spellbookEntryAdded"] or entry["spellId"] != "flame-armor":
            raise ValueError("Completion output does not match the provenance-linked Flame Armor assertion")
        if entry["copySourceManuscriptId"] != overlay["worksite"]["manuscript"]["id"]:
            raise ValueError("Completion entry does not identify the adopted finite source manuscript")
    elif outcome["spellbookEntryAdded"] is not None:
        raise ValueError("Abandonment branch asserts a spellbook entry")
    if outcome["materials"]["refund"] or outcome["materials"]["allCommittedInputsLostAtTerminalOutcome"] is not True:
        raise ValueError("Committed materials were refunded or not expended")
    if not is_completion and outcome["materials"]["abandonedWorkCreditGranted"] is not False:
        raise ValueError("Abandonment branch grants work credit")

    expected_actor = copy.deepcopy(parent_state["actors"]["A"])
    expected_actor["spellEfficiency"] = None
    if final["actors"]["A"] != expected_actor:
        raise ValueError("Actor A changed outside the adopted deadline expiry")
    for actor_id, parent_actor in parent_state["actors"].items():
        if actor_id != "A" and final["actors"][actor_id] != parent_actor:
            raise ValueError(f"Unrelated actor changed: {actor_id}")
    for field in ("items", "effects", "spaces", "pendingCast", "pendingCastStack", "transitReceipts", "effectReceipts", "hardDenialClaims", "observations"):
        if final[field] != parent_state[field]:
            raise ValueError(f"Parent state field unexpectedly changed: {field}")
    if final["mode"] != "outside-initiative" or final["w02TestOnlyScenario"]["initiativeExitApplied"] is not True or final["w02TestOnlyScenario"]["initiativeDispatchEnabled"] is not False:
        raise ValueError("Scenario enabled future initiative dispatch")
    if final["w02TestOnlyScenario"]["regularScheduleMarkersPreserved"] is not True:
        raise ValueError("Scenario failed to preserve regular schedule markers")
    book = final["w02TestOnlyScenario"]["worksite"]["spellbook"]
    if book["location"] != "cargo-A" or book["unpackedForCopy"] is not True or book["repackedAfterTerminal"] is not True:
        raise ValueError("The book was not separately unpacked and repacked")
    repack = branch["postTerminalRepack"]
    if not repack["separateSubsequentEvent"] or repack["eventTimeSeconds"] != outcome["eventTimeSeconds"] or repack["elapsedClockAdvancedSeconds"] != 0:
        raise ValueError("Separate post-terminal repack timing/order is inconsistent")
    if outcome["actorA"]["carriedWeightLb"] != 9 or outcome["bookInCargo"] is not False or repack["actorCarriedWeightLb"] != 12:
        raise ValueError("Terminal-before-repack and repacked load states do not reconcile")
    if any(branch["testOnlyLimits"][key] for key in ("campaignOccurrence", "canonicalRuleChanged", "liveFixtureMutated", "parentBytesChanged", "fortressAcceptedOrApplied", "queueChanged")):
        raise ValueError("A branch claims a forbidden mutation or acceptance/application")
    return {
        "branch": branch["scope"]["branchKind"],
        "events": len(events),
        "forwardOperations": sum(len(event["forward"]) for event in events),
        "inverseOperations": sum(len(event["inverse"]) for event in events),
        "forwardHashesMatched": True,
        "inverseHashesMatched": True,
        "exactInitialRestored": True,
        "terminalStateReconciles": True,
    }


def main() -> None:
    delivery = json.loads((OUT / "DELIVERY_420.json").read_text(encoding="utf-8"))
    packet_raw = PACKET.read_bytes()
    if len(packet_raw) != delivery["packetBytes"] or sha(packet_raw) != delivery["packetSha256"]:
        raise ValueError("Delivery packet bytes/hash mismatch")
    with zipfile.ZipFile(PACKET) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"ZIP CRC failure: {bad_member}")
        payload = {name.removeprefix("payload/"): archive.read(name)
                   for name in archive.namelist() if name.startswith("payload/") and not name.endswith("/")}
    manifest_raw = payload["MANIFEST.json"]
    if sha(manifest_raw) != delivery["manifestSha256"]:
        raise ValueError("Manifest hash differs from delivery")
    manifest = load_json(manifest_raw)
    listed = {row["path"]: row for row in manifest["files"]}
    if set(listed) != (set(payload) - {"MANIFEST.json"}):
        raise ValueError("Manifest does not enumerate the exact payload file set")
    for path, row in listed.items():
        if len(payload[path]) != row["bytes"] or sha(payload[path]) != row["sha256"]:
            raise ValueError(f"Payload member binding failed: {path}")

    proposal_raw = payload["authority/OWNER_PG328_W02_SCRIBING_PREMISE_PROPOSAL_415_TESTONLY.json"]
    adoption_raw = payload["authority/OWNER_PG328_W02_SCRIBING_PREMISE_ADOPTION_419_TESTONLY.json"]
    proposal = load_json(proposal_raw)
    adoption = load_json(adoption_raw)
    expected_proposal_sha = "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930"
    if sha(proposal_raw) != expected_proposal_sha or adoption["scope"]["proposalSha256"] != expected_proposal_sha:
        raise ValueError("Exact adopted Proposal 415 binding failed")
    if adoption["ownerAuthorization"]["verbatim"] != "Adopt Proposal 415 exactly":
        raise ValueError("Owner adoption instruction changed")
    if adoption["scope"]["branchId"] != "PG366-W02-R1" or adoption["scope"]["witnessId"] != "PG328-W02":
        raise ValueError("Owner adoption scope changed")

    queue = load_json(payload["authority/CURRENT_SPELL_QUEUE_404.json"])
    live_queue_path = BASE / "CURRENT_SPELL_QUEUE_404.json"
    live_queue = json.loads(live_queue_path.read_text(encoding="utf-8"))
    if sha(payload["authority/CURRENT_SPELL_QUEUE_404.json"]) != sha(live_queue_path.read_bytes()):
        raise ValueError("Packet queue binding differs from current main checkout")
    if (queue["currentAuthority"]["reviewedApplied"], queue["currentAuthority"]["pending"], queue["currentAuthority"]["acceptedUnapplied"]) != (829, 19, 0):
        raise ValueError("Queue404 is no longer 829/19/0")
    if queue["nextIdentity"] != "conjure-demiplane-fortress" or queue != live_queue:
        raise ValueError("Packet does not preserve live Queue404 priority and full contents")

    parent_zip_raw = payload["parent/Return284_HELD.zip"]
    with zipfile.ZipFile(BytesIO(parent_zip_raw)) as parent_zip:
        parent_member = proposal["sourceBindings"]["parentArchive"]["member"]
        parent_raw = parent_zip.read(parent_member)
    parent = load_json(parent_raw)
    if sha(parent_raw) != proposal["sourceBindings"]["parentArchive"]["memberSha256"]:
        raise ValueError("Parent case member bytes differ from Proposal415 binding")
    parent_state = parent["events"][8]["after"]
    if digest(parent_state) != parent["finalSHA256"]:
        raise ValueError("Parent fork state does not match immutable terminal hash")
    profile_raw = payload["sources/RETURN284_WIZARD20_PROFILE.json"]
    profile = load_json(profile_raw)
    profile_sha = sha(profile_raw)
    if profile_sha != load_json(payload["case/PG328_W02_SCRIBING_COMPLETION_BRANCH_420_TESTONLY.json"])["sourceBindings"]["heldArchiveSource"]["wizardProfileMemberSha256"]:
        raise ValueError("Wizard profile bytes differ from Proposal415 source binding")

    completion = load_json(payload["case/PG328_W02_SCRIBING_COMPLETION_BRANCH_420_TESTONLY.json"])
    abandonment = load_json(payload["case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_420_TESTONLY.json"])
    completion_result = audit_replay(completion, parent_state, profile)
    abandonment_result = audit_replay(abandonment, parent_state, profile)
    prior = load_json(payload["authority/PRIOR_PACKET_419_BINDING.json"])
    prior_packet = (BASE / "fortress_w02_scribing_witness_419/DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_419_TESTONLY.zip").read_bytes()
    if sha(prior_packet) != prior["sha256"] or delivery["priorPacket419Sha256"] != prior["sha256"]:
        raise ValueError("Superseded Repack419 packet binding failed")

    checks = {
        "deliveryPacketLengthAndHash": True,
        "zipCrcAndManifestExactFileSet": True,
        "allPayloadMembersMatchLengthAndSha256": True,
        "exactProposal415AndAdoption419Scope": True,
        "liveQueue404BindingAnd829_19_0Priority": True,
        "immutableParentArchiveMemberAndForkState": True,
        "sourceProfileAndBaselineSpellbookExact": True,
        "completionSixEventsIncludingExitUnpackAndRepack": True,
        "completionForwardOperationsAndEveryStateHash": True,
        "completionAllInverseOperationsAndExactRestoration": True,
        "abandonmentSixEventsIncludingExitUnpackAndRepack": True,
        "abandonmentForwardOperationsAndEveryStateHash": True,
        "abandonmentAllInverseOperationsAndExactRestoration": True,
        "completionOnlyOneFlameArmorEntryWithProvenance": True,
        "abandonmentNoEntryRefundOrWorkCredit": True,
        "actorResourcesPositionHistoryAndSchedulePreserved": True,
        "parentActorsItemsEffectsAndSpacesPreserved": True,
        "inheritedClockOffsetAndRunningClocksReconcile": True,
        "initiativeExitAndDispatchSuspensionReconcile": True,
        "bookUnpackAndSeparateRepackLoadArithmetic": True,
        "allNonW02HoldsAndAcceptanceApplicationPreserved": True,
        "supersededRepack419BoundByExactPacketHash": True,
    }
    audit = {
        "recordId": "PG328-W02-REPACK420-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "classification": "INDEPENDENT_PACKET_SOURCE_AND_REVERSIBLE_REPLAY_AUDIT_TEST_ONLY",
        "status": "PASS_PENDING_DIRECTOR_REVIEW",
        "packetPath": PACKET.name,
        "packetBytes": len(packet_raw),
        "packetSha256": sha(packet_raw),
        "manifestSha256": sha(manifest_raw),
        "checkCount": len(checks),
        "checks": checks,
        "replay": {"completion": completion_result, "abandonment": abandonment_result},
        "queue": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
        "parentBytesMutated": False,
        "fixtureMutated": False,
        "canonicalRulesChanged": False,
        "runtimeExecuted": False,
        "fortressAcceptedOrApplied": False,
    }
    (OUT / "INDEPENDENT_AUDIT_420.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit["status"], "checks": len(checks), "packetSha256": audit["packetSha256"],
                      "completion": completion_result, "abandonment": abandonment_result,
                      "auditPath": str(OUT / "INDEPENDENT_AUDIT_420.json")}, indent=2))


if __name__ == "__main__":
    main()
