from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = REVIEW.parents[4]
PROPOSAL_DIR = REVIEW / "elemental_shell_b01_test_source_proposal_478_repack01"
PROPOSAL_PATH = PROPOSAL_DIR / "OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_REPACK01_TESTONLY.json"
READBACK_PATH = PROPOSAL_DIR / "DIRECTOR_READBACK_478_REPACK01.json"
ADOPTION_PATH = PROPOSAL_DIR / "OWNER_DF218_B01_ADOPTION_478_REPACK01_TESTONLY.json"
QUEUE_PATH = REVIEW / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
WITNESS_PATH = HERE / "DF218_B01_WITNESS_481_TESTONLY.json"
TRACE_PATH = HERE / "B01_EVENT_TRACE_481.json"
DIRECTOR_HOLD_PATH = HERE / "DIRECTOR_READBACK_480_HOLD.json"
ADOPTION_ERRATUM_PATH = HERE / "OWNER_DF218_B01_ADOPTION_478_CASTER_BINDING_ERRATUM_481_TESTONLY.json"
PRIOR_WITNESS_PATH = HERE.parent / "elemental_shell_b01_witness_480_repack01" / "DF218_B01_WITNESS_480_TESTONLY.json"
PRIOR_TRACE_PATH = HERE.parent / "elemental_shell_b01_witness_480_repack01" / "B01_EVENT_TRACE_480.json"
EXPECTED_PROPOSAL_SHA = "e00c3c8fad96883b6fe1d7ac07e1ed07f4b2f7b2f275dcee1853ce30b576ea69"


def b(path: Path) -> bytes:
    return path.read_bytes()


def j(path: Path):
    return json.loads(b(path))


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ho(value) -> str:
    return h(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def first_difference(left, right, path=""):
    if type(left) is not type(right):
        return {"path": path, "leftType": str(type(left)), "rightType": str(type(right)), "left": repr(left), "right": repr(right)}
    if isinstance(left, dict):
        if set(left) != set(right):
            return {"path": path, "leftKeys": sorted(left), "rightKeys": sorted(right)}
        for key in sorted(left):
            found = first_difference(left[key], right[key], path + "/" + str(key))
            if found:
                return found
    elif isinstance(left, list):
        if len(left) != len(right):
            return {"path": path, "leftLen": len(left), "rightLen": len(right)}
        for index, (lv, rv) in enumerate(zip(left, right)):
            found = first_difference(lv, rv, path + "/" + str(index))
            if found:
                return found
    elif left != right:
        return {"path": path, "left": repr(left), "right": repr(right)}
    return None


def apply_ops(state, operations):
    result = copy.deepcopy(state)
    for op in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in op["path"].split("/")[1:]]
        target = result
        for part in parts[:-1]:
            target = target[int(part)] if isinstance(target, list) else target[part]
        leaf = parts[-1]
        if isinstance(target, list):
            index = int(leaf)
            if op["afterExists"]:
                target[index] = copy.deepcopy(op["after"])
            else:
                target.pop(index)
        elif op["afterExists"]:
            target[leaf] = copy.deepcopy(op["after"])
        else:
            target.pop(leaf)
    return result


proposal_bytes = b(PROPOSAL_PATH)
proposal = j(PROPOSAL_PATH)
readback = j(READBACK_PATH)
adoption = j(ADOPTION_PATH)
erratum = j(ADOPTION_ERRATUM_PATH)
director_hold = j(DIRECTOR_HOLD_PATH)
queue_bytes = b(QUEUE_PATH)
queue = json.loads(queue_bytes)
witness = j(WITNESS_PATH)
trace = j(TRACE_PATH)
replay = witness["stateTransitionReplay"]
snapshots = replay["stateSnapshots"]
events = replay["eventTransitions"]

checks = {}
checks["exactProposalHashAndDirectorReadiness"] = h(proposal_bytes) == EXPECTED_PROPOSAL_SHA and readback["status"] == "READY_FOR_OWNER_ADOPTION" and readback["reviewedProposal"]["sha256"] == EXPECTED_PROPOSAL_SHA
checks["exactOwnerAdoptionRecordedAndPreserved"] = h(b(ADOPTION_PATH)) == "23b99a464927dcd62d60dcb17b5f6f25a2244eafe3e6601f423b38b3405e8144" and adoption["ownerAuthorization"]["verbatim"] == "Adopt exact B01 Proposal478 Repack01 (Recommended)" and adoption["scope"]["proposalSha256"] == EXPECTED_PROPOSAL_SHA and adoption["directorReadiness"]["status"] == "READY_FOR_OWNER_ADOPTION"
checks["casterProposalHashBindingErratum"] = director_hold["decision"] == "HOLD" and erratum["originalAdoption"]["preservedUnchanged"] is True and erratum["correctedBinding"]["proposalPath"].endswith("OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json") and erratum["correctedBinding"]["proposalSha256"] == adoption["supportingCasterQualification"]["proposal468Sha256"] and erratum["correctedBinding"]["separatePreparationPremiseSha256"] == "0d66f106211fc705cfdc88d0916494511a30e91472aad36efbc05eafec73e05f"
checks["scopeB01Only"] = witness["branchId"] == proposal["scope"]["branchId"] and witness["component"] == "DF218-B01" and witness["decisionBoundary"]["B02WitnessConstructed"] is False and witness["decisionBoundary"]["identityAcceptedOrApplied"] is False
checks["exactSourceBindings"] = len(witness["sourceBindings"]) >= 26
bindings_ok = True
for binding in witness["sourceBindings"]:
    path = ROOT / binding["path"]
    if not path.is_file():
        bindings_ok = False
        break
    raw = b(path)
    if binding.get("byteDomain") == "exact committed Git blob":
        try:
            git_raw = subprocess.check_output(["git", "cat-file", "blob", binding["gitBlobSha1"]], cwd=ROOT)
        except subprocess.CalledProcessError:
            bindings_ok = False
            break
        if h(git_raw) != binding["sha256"]:
            bindings_ok = False
            break
        if binding.get("workingTreeSha256") and h(raw) != binding["workingTreeSha256"]:
            bindings_ok = False
            break
    elif h(raw) != binding["sha256"] or blob_hash(raw) != binding["gitBlobSha1"]:
        bindings_ok = False
        break
checks["allBoundSourcesResolve"] = bindings_ok
checks["currentQueueStill831_17_0"] = (queue["currentAuthority"]["reviewedApplied"], queue["currentAuthority"]["pending"], queue["currentAuthority"]["acceptedUnapplied"]) == (831, 17, 0) and h(queue_bytes) == adoption["queueAuthorityAtAdoption"]["queueSha256"]

states_by_id = {snapshot["stateId"]: snapshot["completeState"] for snapshot in snapshots}
checks["completeSevenStateSnapshots"] = len(snapshots) == 7 and all("completeState" in s and s["stateSha256"] == ho(s["completeState"]) for s in snapshots)
checks["endPreservesUnspentReactionAndCastFlag"] = states_by_id["S005"]["actor"]["turn"]["status"] == "ENDED" and states_by_id["S005"]["actor"]["turn"]["reactionAvailable"] is True and states_by_id["S005"]["actor"]["turn"]["magicThisTurn"] is True and states_by_id["S005"]["actor"]["turn"]["actionAvailable"] is False and states_by_id["S005"]["actor"]["turn"]["bonusActionAvailable"] is False and states_by_id["S005"]["actor"]["turn"]["movementAvailableFeet"] == 0 and states_by_id["S006"]["actor"]["turn"]["reactionAvailable"] is True and states_by_id["S006"]["actor"]["turn"]["magicThisTurn"] is True
checks["preparedFamilyHistoryMirrorConsistent"] = states_by_id["S000"]["actor"]["preparedFamiliesUsed"] == states_by_id["S000"]["actor"]["vitals"]["preparedRankedCastFamiliesUsed"] == [] and all(s["completeState"]["actor"]["preparedFamiliesUsed"] == s["completeState"]["actor"]["vitals"]["preparedRankedCastFamiliesUsed"] for s in snapshots[2:])
response_event = next((event for event in events if event["eventId"] == "B01-E003"), {})
checks["responseWindowAdvancesWithoutSpend"] = response_event.get("afterStateId") == "S003" and response_event.get("timeSeconds") == 0.2 and states_by_id["S003"]["timeSeconds"] == 0.2 and states_by_id["S003"]["phase"] == "NO_COUNTERSPELL_RESPONDER" and not any("resourceHistory" in op["path"] or "/vitals/RP" in op["path"] or "reactionAvailable" in op["path"] for op in response_event.get("forwardOperations", []))
checks["stateHashChainAndForwardReplay"] = True
replay_error = None
current = copy.deepcopy(states_by_id["S000"])
for event in events:
    if event["beforeStateSha256"] != ho(current) or event["beforeStateId"] not in states_by_id:
        checks["stateHashChainAndForwardReplay"] = False
        replay_error = f"before mismatch at {event['eventId']}: expected {event['beforeStateSha256']}, actual {ho(current)}"
        break
    after = apply_ops(current, event["forwardOperations"])
    if after != states_by_id[event["afterStateId"]] or ho(after) != event["afterStateSha256"]:
        checks["stateHashChainAndForwardReplay"] = False
        replay_error = {"eventId": event["eventId"], "stateEqual": after == states_by_id[event["afterStateId"]], "expected": event["afterStateSha256"], "actual": ho(after), "firstDifference": first_difference(after, states_by_id[event["afterStateId"]])}
        break
    current = after
checks["inverseReplayRestoresExactStart"] = True
reverse = copy.deepcopy(current)
for event in reversed(events):
    reverse = apply_ops(reverse, event["inverseOperations"])
    if event["beforeStateSha256"] != ho(reverse):
        checks["inverseReplayRestoresExactStart"] = False
        break
checks["inverseReplayRestoresExactStart"] = checks["inverseReplayRestoresExactStart"] and reverse == states_by_id["S000"] and replay["inverseReplayResult"]["restoresExactInitialState"]

final = states_by_id[replay["finalStateId"]]
actor = final["actor"]
damage = actor["damageLedger"][-1]
reflection = actor["reflectionLedger"][-1]
checks["sourcePulseAfterManifestBeforeDeadline"] = [e["timeSeconds"] for e in events if e["kind"] == "SHELL_MANIFESTATION"][0] < 1.1 < actor["activeEffects"][0]["deadlineSeconds"]
checks["geometryAndSupportPass"] = final["environment"]["geometryAudit"]["checks"] == {"bearerWhollyInsideExposureVolume": True, "focusWhollyInsideExposureVolume": True, "bearerBottomExactlyOnSupportedFloor": True, "supportPatchCoversBearerFootprint": True, "noObstacleOrOccluderBetweenSourceVolumeAndBearer": True, "exposureVolumeDoesNotCreateAnActorOrDealer": True}
checks["paidCastCommittedBeforeResolution"] = actor["vitals"]["RP"] == 42 and actor["castHistory"][0]["preCastRP"] == 68 and actor["castHistory"][0]["costRP"] == 26 and actor["pendingCast"] is None
checks["shellPreventsSevenNoHPLoss"] = damage["rawAmount"] == 7 and damage["shellPrevents"] == 7 and damage["hpDamage"] == 0 and actor["vitals"]["HP"] == 110
checks["noCreatureDealerNoReflection"] = final["environment"]["source"]["responsibleCreatureDealer"] is None and reflection["recipient"] is None and not reflection["reflectedPacketEmitted"] and not reflection["nominalOrBankedReflectionRootCreated"] and final["createdReflectionRoots"] == [] and final["emittedReflectedPackets"] == []
checks["traceMatchesWitness"] = trace["witnessSha256"] == h(b(WITNESS_PATH)) and trace["events"] == events and trace["terminalStateSha256"] == replay["finalStateSha256"]
checks["noIdentityOrCanonicalOrQueueEffects"] = witness["decisionBoundary"]["B01Closed"] is False and witness["decisionBoundary"]["identityAcceptedOrApplied"] is False and witness["decisionBoundary"]["canonicalRuleChanged"] is False and witness["decisionBoundary"]["queueChanged"] is False and queue["acceptedUnapplied"] == 0

failed = [name for name, ok in checks.items() if not ok]
validation = {
    "schemaVersion": 1,
    "id": "INDEPENDENT-VALIDATION-DF218-B01-WITNESS-481",
    "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "status": "PASS" if not failed else "FAIL",
    "passed": len(checks) - len(failed),
    "failed": len(failed),
    "checks": checks,
    "proposalSha256": h(proposal_bytes),
    "ownerAdoptionSha256": h(b(ADOPTION_PATH)),
    "witnessSha256": h(b(WITNESS_PATH)),
    "eventTraceSha256": h(b(TRACE_PATH)),
    "queuePath": str(QUEUE_PATH.relative_to(ROOT)).replace("\\", "/"),
    "queueSha256": h(queue_bytes),
    "queueAuthority": {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0},
    "stateSnapshots": len(snapshots),
    "eventCount": len(events),
    "forwardOperationCount": sum(len(e["forwardOperations"]) for e in events),
    "inverseOperationCount": sum(len(e["inverseOperations"]) for e in events),
    "sourceBindingCount": len(witness["sourceBindings"]),
    "sourcePremiseClassification": "owner-adopted branch-local TEST_ONLY only",
    "nonEffects": {"B02Constructed": False, "B01Closed": False, "identityAcceptedOrApplied": False, "canonicalRuleChanged": False, "queueChanged": False, "campaignEventClaimed": False},
    "failedChecks": failed,
    "stateReplayDiagnostic": replay_error,
}
(HERE / "INDEPENDENT_VALIDATION_481.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": validation["status"], "passed": validation["passed"], "failed": validation["failed"], "failedChecks": failed, "witnessSha256": validation["witnessSha256"]}, indent=2))
if failed:
    raise SystemExit(1)
