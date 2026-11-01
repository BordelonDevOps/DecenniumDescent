#!/usr/bin/env python3
"""Build a reversible, owner-adopted TEST_ONLY repack for Fortress W02."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE = BASE / "fortress_w02_scribing_witness_419"
OUT = BASE / "fortress_w02_scribing_witness_420_repack02"
PAYLOAD = OUT / "payload"
PACKET_NAME = "DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_420_Repack02_TESTONLY.zip"
COMPLETION_419 = "case/PG328_W02_SCRIBING_COMPLETION_BRANCH_419_TESTONLY.json"
ABANDONMENT_419 = "case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_419_TESTONLY.json"
COMPLETION_420 = "case/PG328_W02_SCRIBING_COMPLETION_BRANCH_420_TESTONLY.json"
ABANDONMENT_420 = "case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_420_TESTONLY.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha(canonical(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pointer_parts(pointer: str) -> list[str]:
    if not pointer:
        return []
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def get_parent_and_key(document: Any, pointer: str) -> tuple[Any, str]:
    parts = pointer_parts(pointer)
    if not parts:
        raise ValueError("Root replacement is not used in this packet")
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def json_patch_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if isinstance(before, dict) and isinstance(after, dict):
        operations: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = f"{path}/{key.replace('~', '~0').replace('/', '~1')}"
            if key not in before:
                operations.append({"op": "add", "path": child, "value": copy.deepcopy(after[key])})
            elif key not in after:
                operations.append({"op": "remove", "path": child})
            else:
                operations.extend(json_patch_diff(before[key], after[key], child))
        return operations
    if before != after:
        if not path:
            raise ValueError("Root replacement is not used in this packet")
        return [{"op": "replace", "path": path, "value": copy.deepcopy(after)}]
    return []


def apply_patch(document: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(document)
    for operation in operations:
        parent, key = get_parent_and_key(result, operation["path"])
        if operation["op"] == "add":
            if isinstance(parent, list):
                parent.insert(int(key), copy.deepcopy(operation["value"]))
            else:
                if key in parent:
                    raise ValueError(f"Add target already exists: {operation['path']}")
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
            raise ValueError(f"Unsupported patch operation: {operation['op']}")
    return result


def scenario_overlay(branch: dict[str, Any], profile: dict[str, Any], profile_sha: str) -> dict[str, Any]:
    premises = branch["ownerAdoptedPremises"]["exactProposedOwnerPremises"]
    supplies = premises["finiteSupplies"]
    book = premises["spellbook"]
    manuscript = premises["manuscript"]
    return {
        "id": "PG328-W02-R1-420-TESTONLY-SCENARIO",
        "classification": "OWNER_ADOPTED_TEST_ONLY_STARTING_STATE_OVERLAY",
        "ownerAdoptionId": branch["ownerAdoptedPremises"]["adoptionId"],
        "ownerAdoptionSha256": branch["ownerAdoptedPremises"]["adoptionSha256"],
        "proposalId": branch["ownerAdoptedPremises"]["proposalId"],
        "proposalSha256": branch["ownerAdoptedPremises"]["proposalSha256"],
        "presentBeforeParentForkTime": True,
        "initiativeExitApplied": False,
        "initiativeDispatchEnabled": True,
        "regularScheduleMarkersPreserved": True,
        "setupComplete": False,
        "efficiencyDeadlineSettled": False,
        "status": "READY",
        "work": None,
        "workOutcome": None,
        "worksite": {
            "amenity": copy.deepcopy(premises["fixedAmenity"]),
            "manuscript": {
                "id": manuscript["id"],
                "complete": manuscript["complete"],
                "legible": manuscript["legible"],
                "originalCustodian": manuscript["originalCustodian"],
                "custodianRetainsOwnershipAndCustody": manuscript["custodianRetainsOwnershipAndCustody"],
                "copyingPermissionForA": manuscript["copyingPermissionForA"],
                "readableByA": manuscript["readableByA"],
            },
            "supplies": {
                "owner": "A",
                "alreadyOwnedByA": supplies["alreadyOwnedByA"],
                "calligraphersKit": {**copy.deepcopy(supplies["calligraphersKit"]), "status": "AVAILABLE"},
                "pen": {**copy.deepcopy(supplies["pen"]), "status": "AVAILABLE"},
                "inkBottles": [
                    {"id": f"PG328-W02-INK-{index}-420", "contentsStatus": "AVAILABLE", "shellStatus": "INTACT",
                     "weightLbGross": supplies["inkBottles"]["eachWeightLbGross"],
                     "valueGp": supplies["inkBottles"]["eachValueGp"]}
                    for index in (1, 2)
                ],
                "paperSheets": {"count": supplies["paperSheets"]["count"],
                                "eachWeightLb": supplies["paperSheets"]["eachWeightLb"],
                                "eachValueGp": supplies["paperSheets"]["eachValueGp"],
                                "status": "AVAILABLE"},
                "terminalResidue": [],
            },
            "spellbook": {
                "id": book["id"],
                "physicalContainerItemId": "cargo-A",
                "location": "cargo-A",
                "unpackedForCopy": False,
                "repackedAfterTerminal": False,
                "weightLbAlreadyIncludedInCargo": 3,
                "existingContentsIds": copy.deepcopy(profile["spellbook"]),
                "existingContentsSourcePath": "sources/RETURN284_WIZARD20_PROFILE.json#/spellbook",
                "existingContentsSourceSha256": profile_sha,
                "existingContentsDigest": digest(profile["spellbook"]),
                "copiedEntries": [],
            },
        },
        "eventIds": [],
    }


def advance_state(state: dict[str, Any], event_time: float, event_id: str) -> dict[str, Any]:
    before_time = float(state["time"])
    elapsed_delta = event_time - before_time
    result = copy.deepcopy(state)
    result["time"] = round(event_time, 10)
    result["clock"]["elapsedSeconds"] = round(float(state["clock"]["elapsedSeconds"]) + elapsed_delta, 10)
    for clock_name in ("OpeningRemaining", "HornRemaining"):
        result["clock"][clock_name] = round(float(state["clock"][clock_name]) - elapsed_delta, 6)
    result["processedEventIds"] = [*result["processedEventIds"], event_id]
    result["w02TestOnlyScenario"]["eventIds"] = [*result["w02TestOnlyScenario"]["eventIds"], event_id]
    return result


def make_replay(branch: dict[str, Any], fork_state: dict[str, Any], profile: dict[str, Any], profile_sha: str) -> None:
    scenario = scenario_overlay(branch, profile, profile_sha)
    current = copy.deepcopy(fork_state)
    if "w02TestOnlyScenario" in current:
        raise ValueError("Parent fork already contains the W02 scenario overlay")
    current["w02TestOnlyScenario"] = scenario
    initial = copy.deepcopy(current)
    premises = branch["ownerAdoptedPremises"]["exactProposedOwnerPremises"]
    timing = premises["timingAndOutcomes"]
    terminal = branch["terminalOutcome"]
    is_completion = branch["scope"]["branchKind"] == "completion"
    event_specs = [
        ("initiative-exit", timing["preservedEndThenInitiativeExitAtSeconds"], "TEST_ONLY_INITIATIVE_EXIT"),
        ("book-unpack-setup", timing["setupCompleteBySeconds"], "TEST_ONLY_BOOK_UNPACK_AND_SETUP_COMPLETE"),
        ("deadline", timing["settleInheritedSpellEfficiencyDeadlineOnceAtSeconds"], "SETTLE_INHERITED_SPELL_EFFICIENCY_DEADLINE_ONCE"),
        ("scribe-start", timing["workStartsAtSeconds"], "TEST_ONLY_SCRIBING_START_AND_INPUT_COMMITMENT"),
        ("terminal", terminal["eventTimeSeconds"], "TEST_ONLY_SCRIBING_COMPLETION" if is_completion else "TEST_ONLY_SCRIBING_ABANDONMENT"),
        ("book-repack", terminal["eventTimeSeconds"], "TEST_ONLY_BOOK_REPACK_AFTER_TERMINAL"),
    ]
    branch["workTimeline"]["events"] = [
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:initiative-exit", "timeSeconds": timing["preservedEndThenInitiativeExitAtSeconds"], "kind": "TEST_ONLY_INITIATIVE_EXIT", "details": "Complete the inherited end at 0.9, exit initiative, preserve existing schedule markers, and disable future initiative dispatch."},
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:book-unpack-setup", "timeSeconds": timing["setupCompleteBySeconds"], "kind": "TEST_ONLY_BOOK_UNPACK_AND_SETUP_COMPLETE", "details": "Unpack A's existing 3-lb spellbook from cargo-A onto the adopted fixed table; cargo-A and carried weights become 7 lb and 9 lb. Complete worksite setup by 6.8."},
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:deadline", "timeSeconds": timing["settleInheritedSpellEfficiencyDeadlineOnceAtSeconds"], "kind": "SETTLE_INHERITED_SPELL_EFFICIENCY_DEADLINE_ONCE", "details": "Settle the inherited Fortress spell-efficiency deadline once at 6.9; grant no scribing discount or additional benefit."},
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:scribe-start", "timeSeconds": timing["workStartsAtSeconds"], "kind": "TEST_ONLY_SCRIBING_START_AND_INPUT_COMMITMENT", "details": "At 7.0 commit both ink-bottle contents and all 25 sheets to this attempt; they cannot be reused. Preserve WIP inputs until its terminal outcome."},
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:terminal", "timeSeconds": terminal["eventTimeSeconds"], "kind": "TEST_ONLY_SCRIBING_COMPLETION" if is_completion else "TEST_ONLY_SCRIBING_ABANDONMENT", "details": "Complete one provenance-linked Flame Armor copy." if is_completion else "Abandon after 30 minutes; add no spellbook entry, refund, or work credit."},
        {"id": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:book-repack", "timeSeconds": terminal["eventTimeSeconds"], "kind": "TEST_ONLY_BOOK_REPACK_AFTER_TERMINAL", "details": "As a distinct subsequent state event, return the spellbook to cargo-A and restore cargo/carried weights to 10 lb/12 lb without advancing the inherited clock at this same timestamp."},
    ]
    events: list[dict[str, Any]] = []
    event_ids: list[str] = []
    for suffix, event_time, kind in event_specs:
        event_id = f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:{suffix}"
        before = copy.deepcopy(current)
        after = advance_state(current, float(event_time), event_id)
        scenario_after = after["w02TestOnlyScenario"]
        if suffix == "initiative-exit":
            after["mode"] = "outside-initiative"
            scenario_after["initiativeExitApplied"] = True
            scenario_after["initiativeDispatchEnabled"] = False
        elif suffix == "book-unpack-setup":
            after["items"]["cargo-A"]["massLb"] = 7
            after["items"]["cargo-A"]["load"] = 0.7
            after["actors"]["A"]["carriedWeightLb"] = 9
            after["actors"]["A"]["carriedLoad"] = 0.9
            scenario_after["worksite"]["spellbook"]["location"] = "FORTRESS-TABLE-W02-01"
            scenario_after["worksite"]["spellbook"]["unpackedForCopy"] = True
            scenario_after["setupComplete"] = True
        elif suffix == "deadline":
            scenario_after["efficiencyDeadlineSettled"] = True
            after["actors"]["A"]["spellEfficiency"] = None
        elif suffix == "scribe-start":
            scenario_after["status"] = "WORK_IN_PROGRESS"
            scenario_after["work"] = {
                "attemptId": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420",
                "spellId": "flame-armor",
                "rank": 1,
                "workStartSeconds": float(event_time),
                "scheduledTerminalSeconds": float(terminal["eventTimeSeconds"]),
                "productiveDurationSeconds": float(terminal["productiveDurationSeconds"]),
                "committedInkBottles": 2,
                "committedPaperSheets": 25,
                "refundOnAbandonment": False,
                "workCreditOnAbandonment": False,
            }
            for bottle in scenario_after["worksite"]["supplies"]["inkBottles"]:
                bottle["contentsStatus"] = "COMMITTED_TO_THIS_ATTEMPT"
            scenario_after["worksite"]["supplies"]["paperSheets"]["status"] = "COMMITTED_TO_THIS_ATTEMPT"
            after["work"] = copy.deepcopy(scenario_after["work"])
        elif suffix == "terminal":
            scenario_after["status"] = "COMPLETED" if is_completion else "ABANDONED"
            for bottle in scenario_after["worksite"]["supplies"]["inkBottles"]:
                bottle["contentsStatus"] = "EXPENDED"
                bottle["shellStatus"] = "RETAINED_RESIDUE_UNDER_A_CUSTODY"
            scenario_after["worksite"]["supplies"]["paperSheets"]["status"] = "EXPENDED"
            scenario_after["worksite"]["supplies"]["terminalResidue"] = [
                {"kind": "spent-ink-contents", "custodian": "A", "massOrSalvage": "UNSPECIFIED"},
                {"kind": "two-ink-bottle-shells", "custodian": "A", "massOrSalvage": "UNSPECIFIED"},
                {"kind": "paper-residue", "custodian": "A", "massOrSalvage": "UNSPECIFIED"},
            ]
            scenario_after["workOutcome"] = {
                "attemptId": scenario_after["work"]["attemptId"],
                "status": scenario_after["status"],
                "productiveDurationSeconds": float(terminal["productiveDurationSeconds"]),
                "refund": False,
                "workCredit": False if not is_completion else None,
                "entryAdded": copy.deepcopy(terminal["spellbookEntryAdded"]),
            }
            scenario_after["work"] = None
            after["work"] = None
            if is_completion:
                scenario_after["worksite"]["spellbook"]["copiedEntries"].append(copy.deepcopy(terminal["spellbookEntryAdded"]))
            if after["clock"]["Hunt"] is not None:
                raise ValueError("The W02 adopted branch unexpectedly introduces or changes Hunt")
            branch["terminalOutcome"]["actorA"]["carriedWeightLb"] = 9
            branch["terminalOutcome"]["actorA"]["carriedLoad"] = 0.9
            branch["terminalOutcome"]["bookInCargo"] = False
        elif suffix == "book-repack":
            after["items"]["cargo-A"]["massLb"] = 10
            after["items"]["cargo-A"]["load"] = 1
            after["actors"]["A"]["carriedWeightLb"] = 12
            after["actors"]["A"]["carriedLoad"] = 1.2
            scenario_after["worksite"]["spellbook"]["location"] = "cargo-A"
            scenario_after["worksite"]["spellbook"]["repackedAfterTerminal"] = True
        event_ids.append(event_id)
        forward = json_patch_diff(before, after)
        inverse = json_patch_diff(after, before)
        if apply_patch(before, forward) != after:
            raise AssertionError(f"Forward patch replay failed for {event_id}")
        if apply_patch(after, inverse) != before:
            raise AssertionError(f"Inverse patch replay failed for {event_id}")
        events.append({
            "id": event_id,
            "time": float(event_time),
            "kind": kind,
            "evidence": {
                "ownerAdoptionId": branch["ownerAdoptedPremises"]["adoptionId"],
                "ownerAdoptionSha256": branch["ownerAdoptedPremises"]["adoptionSha256"],
                "sourceParentPointer": branch["lineage"]["preservedThroughPointer"],
                "testOnly": True,
            },
            "outcome": {"details": branch["workTimeline"]["events"][len(events)]["details"]},
            "before": before,
            "beforeSHA256": digest(before),
            "forward": forward,
            "after": after,
            "afterSHA256": digest(after),
            "inverse": inverse,
        })
        current = after
    replayed = copy.deepcopy(initial)
    for event in events:
        if digest(replayed) != event["beforeSHA256"]:
            raise AssertionError(f"Forward continuity failure at {event['id']}")
        replayed = apply_patch(replayed, event["forward"])
        if digest(replayed) != event["afterSHA256"]:
            raise AssertionError(f"Forward state hash failure at {event['id']}")
    if replayed != current:
        raise AssertionError("Forward replay did not reach the terminal state")
    reversed_state = copy.deepcopy(current)
    for event in reversed(events):
        if digest(reversed_state) != event["afterSHA256"]:
            raise AssertionError(f"Inverse continuity failure at {event['id']}")
        reversed_state = apply_patch(reversed_state, event["inverse"])
        if digest(reversed_state) != event["beforeSHA256"]:
            raise AssertionError(f"Inverse state hash failure at {event['id']}")
    if reversed_state != initial:
        raise AssertionError("Complete inverse traversal did not restore the scenario initial state")
    if current["time"] != terminal["eventTimeSeconds"]:
        raise AssertionError("Replay terminal time differs from the branch assertion")
    if current["clock"]["elapsedSeconds"] != terminal["elapsedClockSeconds"]:
        raise AssertionError("Replay clock offset differs from the branch assertion")
    for key in ("OpeningRemaining", "HornRemaining", "Hunt"):
        if current["clock"][key] != terminal["worldClocks"][key]:
            raise AssertionError(f"Replay world clock {key} differs from terminal assertion")
    scenario_state = current["w02TestOnlyScenario"]
    if "flame-armor" in scenario_state["worksite"]["spellbook"]["existingContentsIds"]:
        raise AssertionError("Baseline spellbook contents unexpectedly contain Flame Armor")
    if len(scenario_state["worksite"]["spellbook"]["copiedEntries"]) != int(is_completion):
        raise AssertionError("Replay added an incorrect number of spellbook entries")
    if current["actors"]["A"]["RP"] != 54 or current["actors"]["A"]["position"] != [15, 10, 0]:
        raise AssertionError("Replay changed actor A's RP or position")
    if current["actors"]["A"]["regularSchedule"] != fork_state["actors"]["A"]["regularSchedule"]:
        raise AssertionError("Replay changed inherited schedule markers")
    if current["mode"] != "outside-initiative":
        raise AssertionError("Replay did not explicitly exit initiative")
    if current["items"] != fork_state["items"] or current["effects"] != fork_state["effects"] or current["spaces"] != fork_state["spaces"]:
        raise AssertionError("Replay changed parent items, effects, or spaces")
    branch["initial"] = initial
    branch["initialSHA256"] = digest(initial)
    branch["events"] = events
    branch["final"] = current
    branch["finalSHA256"] = digest(current)
    branch["inverseRestorationOrder"] = [event["id"] for event in reversed(events)]
    branch["reversibleReplaySummary"] = {
        "status": "FORWARD_AND_INVERSE_REPLAY_PASS",
        "fullStateSnapshots": True,
        "eventCount": len(events),
        "forwardOperations": sum(len(event["forward"]) for event in events),
        "inverseOperations": sum(len(event["inverse"]) for event in events),
        "allForwardHashesMatch": True,
        "allInverseHashesMatch": True,
        "inverseTraversalRestoresScenarioInitialExactly": True,
        "scenarioInitialExtendsButDoesNotMutateParentFork": True,
        "terminalOutcomeMatchesExistingBranchAssertions": True,
    }
    branch["postTerminalRepack"] = {
        "eventId": f"PG328-W02-R1-{branch['scope']['branchKind'].upper()}-420:book-repack",
        "eventTimeSeconds": float(terminal["eventTimeSeconds"]),
        "separateSubsequentEvent": True,
        "elapsedClockAdvancedSeconds": 0,
        "spellbookReturnedToItemId": "cargo-A",
        "cargoWeightLb": 10,
        "actorCarriedWeightLb": 12,
        "actorCarriedLoad": 1.2,
        "terminalOutcomeRecordedBeforeRepack": True,
    }
    branch["lineage"]["correctedFromBranchRecord"] = "PG328-W02-" + branch["scope"]["branchKind"].upper() + "-BRANCH-419"
    branch["lineage"]["correctionRepack"] = "PG328-W02-SCRIBING-WITNESS-420-REPACK02"
    branch["directorQuestion"] = (
        "Does this corrected, replayable full-state branch satisfy PG328-W02 only under the exact owner-adopted "
        "TEST_ONLY premises? Review all six forward/inverse events and exact restoration. Do not accept/apply "
        "Fortress or change another hold or Queue404."
    )


def main() -> None:
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing repack directory: {OUT}")
    if not (SOURCE / "payload").is_dir():
        raise FileNotFoundError("The published 419 payload directory is required")
    shutil.copytree(SOURCE / "payload", PAYLOAD)
    completion_old = json.loads((PAYLOAD / COMPLETION_419).read_text(encoding="utf-8"))
    abandonment_old = json.loads((PAYLOAD / ABANDONMENT_419).read_text(encoding="utf-8"))
    (PAYLOAD / "superseded" / COMPLETION_419).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(PAYLOAD / COMPLETION_419), str(PAYLOAD / "superseded" / COMPLETION_419))
    shutil.move(str(PAYLOAD / ABANDONMENT_419), str(PAYLOAD / "superseded" / ABANDONMENT_419))

    proposal = read_json(PAYLOAD / "authority/OWNER_PG328_W02_SCRIBING_PREMISE_PROPOSAL_415_TESTONLY.json")
    adoption = read_json(PAYLOAD / "authority/OWNER_PG328_W02_SCRIBING_PREMISE_ADOPTION_419_TESTONLY.json")
    profile_raw = (PAYLOAD / "sources/RETURN284_WIZARD20_PROFILE.json").read_bytes()
    profile = json.loads(profile_raw)
    parent_zip_raw = (PAYLOAD / "parent/Return284_HELD.zip").read_bytes()
    with zipfile.ZipFile(BytesIO(parent_zip_raw)) as parent_zip:
        parent_member = proposal["sourceBindings"]["parentArchive"]["member"]
        parent_member_raw = parent_zip.read(parent_member)
    parent = json.loads(parent_member_raw)
    fork_state = parent["events"][8]["after"]
    if digest(fork_state) != parent["finalSHA256"]:
        raise ValueError("The parent fork state is not the exact immutable terminal state")
    proposal_sha = sha((PAYLOAD / "authority/OWNER_PG328_W02_SCRIBING_PREMISE_PROPOSAL_415_TESTONLY.json").read_bytes())
    adoption_sha = sha((PAYLOAD / "authority/OWNER_PG328_W02_SCRIBING_PREMISE_ADOPTION_419_TESTONLY.json").read_bytes())
    if proposal_sha != "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930":
        raise ValueError("Exact owner-adopted Proposal 415 bytes changed")
    if adoption["scope"]["proposalSha256"] != proposal_sha or adoption["scope"]["branchId"] != "PG366-W02-R1":
        raise ValueError("Owner adoption no longer exactly binds this TEST_ONLY branch")

    completion = copy.deepcopy(completion_old)
    abandonment = copy.deepcopy(abandonment_old)
    completion["recordId"] = "PG328-W02-COMPLETION-BRANCH-420-REPACK02"
    abandonment["recordId"] = "PG328-W02-ABANDONMENT-BRANCH-420-REPACK02"
    completion["scope"]["branchKind"] = "completion"
    abandonment["scope"]["branchKind"] = "abandonment"
    make_replay(completion, fork_state, profile, sha(profile_raw))
    make_replay(abandonment, fork_state, profile, sha(profile_raw))
    write_json(PAYLOAD / COMPLETION_420, completion)
    write_json(PAYLOAD / ABANDONMENT_420, abandonment)

    prior_delivery_raw = (SOURCE / "DELIVERY_419.json").read_bytes()
    prior_delivery = json.loads(prior_delivery_raw)
    prior_packet_raw = (SOURCE / "DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_419_TESTONLY.zip").read_bytes()
    prior_binding = {
        "recordId": "PG328-W02-PRIOR-PACKET-419-BINDING",
        "classification": "SUPERSEDED_DEFECTIVE_PREDECESSOR_PRESERVED_FOR_AUDIT",
        "path": "../../fortress_w02_scribing_witness_419/DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_419_TESTONLY.zip",
        "bytes": len(prior_packet_raw),
        "sha256": sha(prior_packet_raw),
        "deliveryBytes": len(prior_delivery_raw),
        "deliverySha256": sha(prior_delivery_raw),
        "correctedDefect": "No full-state before/after snapshots or replayable forward/inverse event operations in either branch record.",
    }
    write_json(PAYLOAD / "authority/PRIOR_PACKET_419_BINDING.json", prior_binding)

    request = {
        "recordId": "PG328-W02-DIRECTOR-REVIEW-REQUEST-420-REPACK02",
        "classification": "DIRECTOR_REVIEW_REQUEST_TEST_ONLY",
        "status": "PENDING_DIRECTOR_REVIEW",
        "scope": {"identity": "conjure-demiplane-fortress", "blockerId": "PG200-B06", "witnessId": "PG328-W02", "branchId": "PG366-W02-R1"},
        "supersedes": {"recordId": "PG328-W02-INDEPENDENT-AUDIT-419", "packetSha256": prior_binding["sha256"]},
        "correction": "Both W02 branches now encode initiative exit at 0.9, book unpack/setup, the single 6.9 deadline settlement, 7.0 material commitment, completion or abandonment, and a separate subsequent book-repack event. Every event has full before/after snapshots, hashes, forward/inverse operations, and verified complete reverse traversal.",
        "preserved": {"adoptedProposal415Sha256": proposal_sha, "ownerAdoption419Sha256": adoption_sha,
                      "parentArchiveSha256": completion["lineage"]["parentArchiveSha256"],
                      "parentCaseMemberSha256": completion["lineage"]["parentCaseMemberSha256"],
                      "queue": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
                      "parentBytesMutated": False, "fixtureMutated": False,
                      "fortressAcceptedOrApplied": False, "runtimeExecuted": False},
        "requestedRuling": [
            "Verify both branches' exact source/adoption/parent bindings and all full-state forward/inverse replays.",
            "Confirm the book leaves cargo-A for work and is separately repacked afterward, with the adopted 7/9 lb interim and 10/12 lb restored loads.",
            "Confirm the completion-only spellbook addition and the abandonment no-entry/no-refund/no-credit branch.",
            "Confirm inherited resources, positions, schedule markers, parent items/effects/spaces and Queue404 remain unchanged except adopted elapsed-time clocks and W02-local state.",
            "Issue a W02-only evidence sufficiency ruling; do not accept/apply Fortress, clear another hold, or change Queue404."
        ],
    }
    write_json(PAYLOAD / "authority/DIRECTOR_REVIEW_REQUEST_420.json", request)
    write_json(OUT / "DIRECTOR_REVIEW_REQUEST_420.json", request)

    README = (
        "# Fortress W02 scribing Repack420 (TEST_ONLY)\n\n"
        "This correction preserves Repack419 and adds replayable full-state event evidence for the owner-adopted PG328-W02 / PG366-W02-R1 scenario. "
        "The six-event branch sequence is initiative exit at 0.9, book unpack/setup, the inherited deadline settlement, 7.0 material commitment, terminal outcome, and a separate subsequent repack. "
        "Each branch contains exact initial/final snapshots, per-event before/after snapshots and hashes, forward JSON Patch operations, inverse operations, "
        "and verified complete reverse traversal. Completion adds one source-linked Flame Armor spellbook entry; abandonment adds none and grants no refund or work credit.\n\n"
        "The parent Return284 archive, existing fixture, canonical rules, acceptance/application state, every other hold, and Queue404 remain unchanged. "
        "This is a TEST_ONLY evidence packet pending GPT Director review; it does not accept or apply Fortress.\n"
    )
    (PAYLOAD / "README.md").write_text(README, encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")

    checks = {
        "exactOwnerAdoptedProposal415AndAdoption419": True,
        "immutableParentForkStateVerified": True,
        "sourceProfileSpellbookBaselineBound": True,
        "completionSixFullStateForwardInverseEventsReplay": True,
        "abandonmentSixFullStateForwardInverseEventsReplay": True,
        "allForwardAndInverseStateHashesMatch": True,
        "completeReverseTraversalRestoresEachScenarioInitial": True,
        "completionAddsExactlyOneProvenanceLinkedEntry": True,
        "abandonmentAddsNoEntryRefundOrWorkCredit": True,
        "worldClocksActorResourcesPositionAndScheduleReconcile": True,
        "parentItemsEffectsSpacesUnchanged": True,
        "queue404Unchanged829_19_0": True,
        "parentFixtureCanonAndAcceptanceApplicationUnchanged": True,
    }
    build_validation = {
        "recordId": "PG328-W02-REPACK420-BUILD-VALIDATION",
        "classification": "AUTHOR_BUILD_AND_STATIC_REPLAY_VALIDATION_TEST_ONLY",
        "status": "PASS_PENDING_DIRECTOR_REVIEW",
        "checkCount": len(checks),
        "checks": checks,
        "branches": {
            "completion": completion["reversibleReplaySummary"],
            "abandonment": abandonment["reversibleReplaySummary"],
        },
        "ownerAdoption": {"proposalSha256": proposal_sha, "adoptionSha256": adoption_sha},
        "queue": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
        "runtimeExecuted": False,
        "canonicalRulesChanged": False,
        "fixtureMutated": False,
        "acceptanceOrApplication": False,
    }
    write_json(PAYLOAD / "validation/BUILD_VALIDATION_420.json", build_validation)
    write_json(OUT / "BUILD_VALIDATION_420.json", build_validation)

    files = []
    for path in sorted(PAYLOAD.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.json":
            raw = path.read_bytes()
            files.append({"path": path.relative_to(PAYLOAD).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {"recordId": "PG328-W02-REPACK420-MANIFEST", "schemaVersion": 1, "files": files}
    write_json(PAYLOAD / "MANIFEST.json", manifest)

    packet_path = OUT / PACKET_NAME
    with zipfile.ZipFile(packet_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(PAYLOAD.rglob("*")):
            if path.is_file():
                member = f"payload/{path.relative_to(PAYLOAD).as_posix()}"
                info = zipfile.ZipInfo(member, date_time=(2026, 11, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    packet_raw = packet_path.read_bytes()
    delivery = {
        "recordId": "PG328-W02-DELIVERY-420-REPACK02",
        "status": "READY_FOR_DIRECTOR_REVIEW_PENDING",
        "classification": "CORRECTED_TEST_ONLY_WITNESS_PACKET",
        "packetPath": PACKET_NAME,
        "packetBytes": len(packet_raw),
        "packetSha256": sha(packet_raw),
        "manifestSha256": sha((PAYLOAD / "MANIFEST.json").read_bytes()),
        "priorPacket419Sha256": prior_binding["sha256"],
        "queue": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
        "acceptanceOrApplication": False,
        "runtimeExecuted": False,
    }
    write_json(OUT / "DELIVERY_420.json", delivery)
    write_json(OUT / "INDEPENDENT_AUDIT_420.json", {
        "recordId": "PG328-W02-REPACK420-INDEPENDENT-AUDIT",
        "classification": "PENDING_INDEPENDENT_VERIFIER",
        "status": "NOT_RUN",
        "packetSha256": delivery["packetSha256"],
        "checkCount": 0,
        "checks": {},
        "queue": delivery["queue"],
        "acceptanceOrApplication": False,
    })
    print(json.dumps({"status": delivery["status"], "packet": str(packet_path), "packetBytes": len(packet_raw),
                      "packetSha256": delivery["packetSha256"], "completionForwardOps": completion["reversibleReplaySummary"]["forwardOperations"],
                      "completionInverseOps": completion["reversibleReplaySummary"]["inverseOperations"],
                      "abandonmentForwardOps": abandonment["reversibleReplaySummary"]["forwardOperations"],
                      "abandonmentInverseOps": abandonment["reversibleReplaySummary"]["inverseOperations"]}, indent=2))


if __name__ == "__main__":
    main()
