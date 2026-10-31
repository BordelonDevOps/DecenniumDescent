from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "banishment_gate_witness365_w05_separation365_repack02_build01"
DELIVERY = OUT / "ARCHIVE_DELIVERY_365_W05_REPACK02.json"
AUDIT_OUT = OUT / "INDEPENDENT_AUDIT_365_W05_REPACK02_ARCHIVE.json"
PIN = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
AC5_SHA = "43b0fe4359021c4d8f714e3986be3d1579889cf590cfac73333dbe99b31c50cd"
W08_SHA = "c277d95f1590a2ae6c2a63d8cf02b9158d7312694ca834491afa7ff9f00a7eb7"
TURN_ORDER = ["actor-w05-champion-owner", "actor-w05-firepet-owner", "actor-w05-gate-caster"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def state_sha(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def apply_ops(state: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in operations:
        parent = result
        for part in op["path"][:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = op["path"][-1]
        if isinstance(parent, list):
            index = int(key)
            old = parent[index] if op["op"] != "add" else None
            if op["op"] == "remove":
                assert old == op["before"]
                parent.pop(index)
            elif op["op"] == "add":
                assert index == len(parent)
                parent.append(copy.deepcopy(op["after"]))
            else:
                assert old == op["before"]
                parent[index] = copy.deepcopy(op["after"])
        elif op["op"] == "remove":
            assert parent[key] == op["before"]
            del parent[key]
        elif op["op"] == "add":
            assert key not in parent
            parent[key] = copy.deepcopy(op["after"])
        else:
            assert parent[key] == op["before"]
            parent[key] = copy.deepcopy(op["after"])
    return result


def resolve_pointer(payloads: dict[str, bytes], ref: str) -> Any:
    member, fragment = ref.split("#", 1)
    value = json.loads(payloads[member].decode("utf-8-sig"))
    if fragment:
        for part in fragment.split("/")[1:]:
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def replay(initial: dict[str, Any], events: list[dict[str, Any]]) -> tuple[dict[str, Any], int]:
    state = copy.deepcopy(initial)
    active_actor = None
    markers: list[tuple[float, int]] = []
    for event in events:
        assert event["timestampSeconds"] >= state["elapsedSeconds"]
        assert event["beforeStateSha256"] == state_sha(state)
        next_state = apply_ops(state, event["forwardOperations"])
        assert state_sha(next_state) == event["afterStateSha256"] == state_sha(event["stateAfter"])
        assert apply_ops(next_state, event["inverseOperations"]) == state
        next_active = next_state["turnScheduler"]["activeActorId"]
        if event["kind"] == "regular-turn-start":
            assert active_actor is None and next_active is not None
        elif event["kind"] == "regular-turn-end":
            assert active_actor is not None and next_active is None
        else:
            assert next_active == active_actor
        active_actor = next_active
        state = next_state
        markers.append((event["timestampSeconds"], event["sequenceAtTimestamp"]))
    assert active_actor is None and markers == sorted(markers)
    return state, len(events)


def main() -> None:
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    archive_path = OUT / delivery["archive"]
    archive_bytes = archive_path.read_bytes()
    assert len(archive_bytes) == delivery["bytes"] and sha(archive_bytes) == delivery["sha256"]
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == delivery["uniqueMembers"] == len(set(names))
        payloads = {name: archive.read(name) for name in names}
    manifest = json.loads(payloads["ARCHIVE_MANIFEST.json"].decode("utf-8-sig"))
    manifest_by_path = {x["path"]: x for x in manifest["members"]}
    assert len(manifest_by_path) == delivery["manifestPayloads"]
    assert set(manifest_by_path) == set(names) - {"ARCHIVE_MANIFEST.json"}
    for name, record in manifest_by_path.items():
        assert len(payloads[name]) == record["bytes"] and sha(payloads[name]) == record["sha256"]

    bindings = json.loads(payloads["W05_SOURCE_BINDINGS_365.json"].decode("utf-8-sig"))
    verified_sources = 0
    for binding in bindings["bindings"]:
        data = payloads[binding["member"]]
        assert len(data) == binding["bytes"] and sha(data) == binding["sha256"]
        origin = binding["origin"]
        if origin.get("kind") == "pinned-git-source":
            assert origin["commit"] == PIN
            git_data = subprocess.run(["git", "show", f'{PIN}:{origin["repositoryPath"]}'],
                cwd=REPO, check=True, capture_output=True).stdout
            assert sha(git_data) == sha(data)
        if origin.get("kind") == "accepted-AC5-archive":
            assert origin["archiveSha256"] == AC5_SHA
        if origin.get("kind") == "sealed-W08-archive":
            assert origin["archiveSha256"] == W08_SHA
        if origin.get("sourceExtractSha256"):
            assert origin["sourceExtractSha256"] == sha(data) == "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b"
        for pointer in binding.get("jsonPointers", []):
            resolve_pointer(payloads, binding["member"] + "#" + pointer)
        for locator in binding.get("textLocators", []):
            lines = data.decode("utf-8-sig").splitlines()
            start, end = locator["lines"][0], locator["lines"][-1]
            assert 1 <= start <= end <= len(lines) and lines[start - 1].strip() and lines[end - 1].strip()
        verified_sources += 1

    case = json.loads(payloads["W05_LIVING_BODY_CARRIAGE_CASE_365_TESTONLY.json"].decode("utf-8-sig"))
    coverage = json.loads(payloads["W05_CASE_COVERAGE_365.json"].decode("utf-8-sig"))
    assert case["identityDecision"] == {"decision": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False}
    assert case["wholeIdentityGate"]["blockerIds"] == ["PG200-B03", "PG200-B04"]
    assert case["applicationAuthorized"] is False and case["acceptanceDecision"] is None
    assert coverage["closedResidualIds"] == [f"W05-365-R{i}" for i in range(1, 8)]
    assert not coverage["identityAcceptance"] and not coverage["applicationAuthorization"]

    source_refs = []
    for event in case["commonPrefix"]["events"] + [e for fork in case["terminalForks"] for e in fork["events"]]:
        for ref in event["sourceRefs"]:
            assert "#" in ref
            resolve_pointer(payloads, ref)
            source_refs.append(ref)
        for locator in event["sourceTextLocators"]:
            lines = payloads[locator["member"]].decode("utf-8-sig").splitlines()
            start, end = locator["lines"]
            assert 1 <= start <= end <= len(lines)
            assert lines[start - 1].strip() and lines[end - 1].strip()
    for ref in case["sourceUse"]["sourceReferences"]:
        resolve_pointer(payloads, ref["pointer"])
        source_refs.append(ref["pointer"])

    prefix = case["commonPrefix"]
    common_state, event_count = replay(prefix["initialState"], prefix["events"])
    ORIGIN = common_state["world"]["originPlaneKey"]
    assert common_state == prefix["finalState"]
    assert [e["timestampSeconds"] for e in prefix["events"]] == sorted(e["timestampSeconds"] for e in prefix["events"])
    branch_results = {}
    all_states = []
    for fork in case["terminalForks"]:
        state, count = replay(prefix["finalState"], fork["events"])
        assert state == fork["finalState"]
        reverse = copy.deepcopy(state)
        for event in reversed(fork["events"]):
            reverse = apply_ops(reverse, event["inverseOperations"])
        assert reverse == prefix["finalState"]
        event_count += count
        all_states.append(state)
        branch_results[fork["id"]] = {"eventCount": count, "forwardInverseExact": True,
            "finalStateSha256": state_sha(state)}

    spells = {
        "actor-w05-firepet-owner": ("summon-greater-fire-pet", 5, 10, 1, 10),
        "actor-w05-champion-owner": ("faction-champion", 5, 10, 1, 10),
        "actor-w05-gate-caster": ("banishment-gate", 9, 26, 2, 12),
    }
    for actor, (spell_id, rank, rp_cost, dissonance_gain, limit) in spells.items():
        mage = common_state["mageActors"][actor]
        assert len(mage["castingHistory"]) == 1
        cast = mage["castingHistory"][0]
        assert (cast["spellId"], cast["rank"], cast["rpPaid"]) == (spell_id, rank, rp_cost)
        assert cast["baseDissonance"] == dissonance_gain and cast["refrainDissonance"] == 0
        assert cast["overcastDissonance"] == 0 and cast["dissonanceDelta"] == dissonance_gain
        assert cast["dissonanceRpSurcharge"] == 0 and cast["dissonanceLimit"] == limit
        assert mage["dissonance"]["current"] == dissonance_gain and mage["dissonance"]["state"] == "In Tune"
        assert mage["refrain"] == {"lastSpellId": spell_id, "repeatCount": 0}
        assert mage["nukeChain"] == [] and len(mage["concentrationHistory"]) == 1
        assert set(cast["components"]) == {"V", "S", "F"} and all(x["satisfied"] for x in cast["components"].values())
        assert mage["focus"]["custody"] == actor
        assert mage["handOccupancy"]["left"] == "free-for-somatic"
        assert mage["handOccupancy"]["right"] == mage["focus"]["objectId"]

    assert len(common_state["counterspellWindows"]) == 3
    for window in common_state["counterspellWindows"]:
        assert window["counterspellAttemptCount"] == 0 and len(window["otherCasterDecisions"]) == 2
        for decision in window["otherCasterDecisions"]:
            assert decision["eligibleToAttempt"] and decision["decision"] == "declined-no-attempt"
            assert decision["rangeFt"] <= 60 and decision["lineOfEffect"]
            assert not decision["reactionSpent"] and decision["rpSpent"] == 0
    checks = common_state["factionChecks"]
    assert [x["phase"] for x in checks] == ["pre-payment", "formation"]
    assert {x["factionId"] for x in checks} == {"FACTION-W05-TEST-01"}
    assert all(x["passesAllFourPredicates"] and x["fixtureOnly"] for x in checks)

    formation = common_state["carriageRelation"]
    g = formation["supportGeometry"]["formation"]
    assert g["carrierBoxFt"][1][1] == g["passengerBoxFt"][1][0] == 0
    assert g["interbodyGapFt"] == 0 and not g["bodyBoxesOverlap"]
    assert formation["capacity"]["physicalLimitLb"] == 210
    assert formation["capacity"]["passengerBodyAndAssociatedEquipmentLb"] == 180
    assert formation["capacity"]["passengerCasualtyLoad"] == 6 <= formation["capacity"]["carrierLoadCapacity"] == 14

    lawful = next(s for f, s in zip(case["terminalForks"], all_states) if f["id"] == "W05-LAWFUL-SEPARATION")
    passenger = lawful["actors"]["actor-w05-champion"]
    pet = lawful["actors"]["actor-w05-firepet"]
    cell = next(iter(lawful["cells"].values()))
    assert passenger["physicalPosition"]["centerFt"] == [-5, 7.5, 3]
    assert passenger["movementBudget"]["spentFt"] == 5 and passenger["movementBudget"]["remainingFt"] == 25
    assert cell["originAnchor"]["bodyOriginCenterFt"] == [5, -2.5, 3]
    assert cell["originAnchor"]["bodyBottomCenterFt"] == [5, -2.5, 0]
    assert cell["originAnchor"]["sourceWorldEndpointCenterFt"] == cell["originAnchor"]["bodyOriginCenterFt"]
    assert pet["movementBudget"]["commandedMoveFt"] == 10
    assert passenger["physicalPosition"]["planeKey"] == case["commonPrefix"]["finalState"]["world"]["originPlaneKey"]
    assert len(lawful["cells"]) == 1 and len(lawful["hardControlClaims"]) == 1
    # Target fixtures are static TEST_ONLY objects; only the attacking actors
    # carry attack histories in this state model.
    for fixture_id in ("actor-w05-target-champion-fixture", "actor-w05-target-firepet-fixture"):
        fixture = lawful["actors"][fixture_id]
        assert fixture["fixtureOnly"] and fixture["initiativeStatus"] == "static-test-target-no-slot"
        assert fixture["alive"] and fixture["hp"] > 0
    assert lawful["actors"]["actor-w05-champion"]["attackHistory"][0]["hit"] is False
    assert lawful["actors"]["actor-w05-firepet"]["attackHistory"][0]["hit"] is False

    impossible = next(s for f, s in zip(case["terminalForks"], all_states) if f["id"] == "W05-IMPOSSIBLE-SEPARATION")
    rel = impossible["carriageRelation"]["supportGeometry"]["current"]
    assert rel["supportActive"] and rel["carrierBoxFt"][0] == rel["passengerBoxFt"][0] == [2.5, 7.5]
    assert len(impossible["cells"]) == 0 and len(impossible["hardControlClaims"]) == 0
    assert impossible["actors"]["actor-w05-firepet"]["alive"] and impossible["actors"]["actor-w05-champion"]["alive"]
    assert impossible["actors"]["actor-w05-firepet"]["physicalPosition"]["planeKey"] == ORIGIN
    assert impossible["actors"]["actor-w05-champion"]["physicalPosition"]["planeKey"] == ORIGIN
    assert impossible["actors"]["actor-w05-firepet"]["isGear"] is False
    assert impossible["actors"]["actor-w05-champion"]["isGear"] is False
    assert impossible["actors"]["actor-w05-target-firepet-fixture"]["initiativeStatus"] == "static-test-target-no-slot"
    assert all(x["eligibleRecipientRegularStartOccurred"] is False
        for x in impossible["turnScheduler"]["firePetAuraCheckpointLedger"])

    queue = json.loads(payloads["authority/CURRENT_SPELL_QUEUE_361.json"].decode("utf-8-sig"))
    assert queue["currentAuthority"] == {"reviewedApplied": 828, "pending": 20, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 552, "scopedInterfaces": 173}
    assert case["queueAuthority"] == {"id": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 552, "scopedInterfaces": 173, "firstReviews": 0, "closureTasks": 20}

    result = {"id": "W05-INDEPENDENT-AUDIT-365-REPACK02", "status": "PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; FRESH_DIRECTOR_DECISION_PENDING",
        "archive": {"file": delivery["archive"], "bytes": len(archive_bytes), "sha256": sha(archive_bytes),
            "uniqueMembers": len(names), "manifestPayloads": len(manifest_by_path)},
        "independentChecks": {"sourceBindingsVerified": verified_sources, "sourceRefsResolved": len(source_refs),
            "archiveHashesAndCrcs": True, "eventsReplayed": event_count, "exactInverseReplay": True,
            "regularTurnsAndStanceBoundaries": True, "counterspellWindows": 3, "otherCasterDecisions": 6,
            "baseDissonanceAndRefrain": True, "factionEligibilityChecks": 2,
            "bodyGeometryAndCapacity": True, "branchOutcomes": branch_results,
            "firePetAuraNonqualification": True, "remainingResidualIds": []},
        "identityDisposition": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
        "blockerIds": ["PG200-B03", "PG200-B04"],
        "queueAuthority": case["queueAuthority"], "nextWitnessAfterSeal": "W03"}
    AUDIT_OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
