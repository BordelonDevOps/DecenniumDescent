#!/usr/bin/env python3
"""Validate the adopted, synthetic IE286 W2 component-test packet only."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
PACKET_DIR = Path(__file__).resolve().parent
SUITE_PATH = PACKET_DIR / "IE286_W2_COMPONENT_CASES_TESTONLY.json"
PROPOSAL_PATH = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/reverse_gravity_ie286_w2_owner_proposal_2026-11-02/OWNER_PROPOSAL_IE286_W2_UPWARD_LOAD_RULE_01.json"
ADOPTION_PATH = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/reverse_gravity_ie286_w2_owner_adoption_2026-11-02/OWNER_ADOPTION_IE286_W2_TESTONLY.json"
QUEUE_PATH = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_479.json"
EXPECTED_PROPOSAL_SHA256 = "4a934f6055546387fe5bc17f81ea6be8b6d623334152729fa721722e255c06e7"
EXPECTED_ADOPTION_SHA256 = "b782c8692feaf7b758c929c284d458296218139bca097e09f65e29addcf3ea3b"
EXPECTED_QUEUE_SHA256 = "f6245df32958ae5438d08fbd2573f53f60cc70b343ff16d9e78d8cf0dffa804a"
EXPECTED_ADOPTION_COMMIT = "5400737f"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def d(value: object) -> Decimal:
    return Decimal(str(value))


def rounded6(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"origin/main:{path}"], cwd=ROOT)


def main() -> int:
    suite_bytes = SUITE_PATH.read_bytes()
    proposal_bytes = PROPOSAL_PATH.read_bytes()
    adoption_bytes = ADOPTION_PATH.read_bytes()
    suite = json.loads(suite_bytes)
    proposal = json.loads(proposal_bytes)
    adoption = json.loads(adoption_bytes)
    queue_bytes = git_bytes(QUEUE_PATH)
    queue = json.loads(queue_bytes)

    check("Exact R7 proposal bytes and hash", len(proposal_bytes) == 57122 and sha256(proposal_bytes) == EXPECTED_PROPOSAL_SHA256, {"bytes": len(proposal_bytes), "sha256": sha256(proposal_bytes)})
    check("Exact owner adoption bytes bind R7", sha256(adoption_bytes) == EXPECTED_ADOPTION_SHA256 and adoption["adoptedContract"]["sha256"] == EXPECTED_PROPOSAL_SHA256, {"sha256": sha256(adoption_bytes), "adoptedProposalSha256": adoption["adoptedContract"]["sha256"]})
    check("Owner adoption is an ancestor of current HEAD", subprocess.run(["git", "merge-base", "--is-ancestor", EXPECTED_ADOPTION_COMMIT, "HEAD"], cwd=ROOT).returncode == 0, {"ownerAdoptionCommitPrefix": EXPECTED_ADOPTION_COMMIT})
    check("Queue479 exact bytes and held baseline remain", sha256(queue_bytes) == EXPECTED_QUEUE_SHA256 and queue["currentAuthority"]["reviewedApplied"] == 834 and queue["currentAuthority"]["pending"] == 14 and queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextIdentity"] == "reverse-gravity-field" and queue["nextBlockerIds"] == ["IE204-B02"], {"sha256": sha256(queue_bytes), "applied": queue["currentAuthority"]["reviewedApplied"], "pending": queue["currentAuthority"]["pending"], "acceptedUnapplied": queue["currentAuthority"]["acceptedUnapplied"], "next": queue["nextIdentity"], "blockers": queue["nextBlockerIds"]})
    check("Suite binds the exact adopted contract and six scoped cases", suite["adoptedContract"]["proposalSha256"] == EXPECTED_PROPOSAL_SHA256 and suite["adoptedContract"]["ownerAdoptionSha256"] == EXPECTED_ADOPTION_SHA256 and len(suite["cases"]) == 6, {"caseIds": [case["id"] for case in suite["cases"]]})
    check("Suite remains explicitly non-runtime and non-campaign", suite["fixturePremises"]["allPremisesAreSynthetic"] and all(value is False for value in suite["nonEffects"].values()), suite["nonEffects"])

    fixture = suite["fixturePremises"]
    rule = proposal["proposedTestOnlyRule"]
    proposal_fixture = rule["fixture"]
    target = proposal_fixture["target"]
    rope = proposal_fixture["caster"]["cast"]["rope"]
    support_fixture = proposal_fixture["support"]
    source_expected = rule["expectedSettlement"]
    route = fixture["ropeRouteFt"]
    source_route = proposal_fixture["tether"]["initialDeployedRouteSegments"]
    route_sum = d(route["dRingToPatchEntry"]) + d(route["looseBightsReturningToEntry"]) + d(route["patchEntryToBracket"])
    check("Continuous rope route totals 50 ft", rounded6(route_sum) == d(route["total"]) == Decimal("50.000000"), {"sum": str(rounded6(route_sum)), "expected": route["total"]})
    leader_detour = d(route["dRingToPatchEntry"]) + d(route["patchEntryToBracket"]) - d(fixture["targetToBracketDirectReferenceFt"])
    slack = leader_detour + d(route["looseBightsReturningToEntry"])
    check("Leader detour and loose bights total 40.4 ft slack", rounded6(leader_detour) == d(fixture["ropeSlackFt"]["leaderDetourBeyondDirectReference"]) and rounded6(slack) == d(fixture["ropeSlackFt"]["total"]), {"leaderDetour": str(rounded6(leader_detour)), "bights": route["looseBightsReturningToEntry"], "slack": str(rounded6(slack))})

    movement = fixture["movement"]
    taut = d(movement["startsAtSeconds"]) + d(fixture["ropeSlackFt"]["total"]) / d(movement["rateFeetPerSecond"])
    check("First taut is 22.04 s at 40.4 ft rise", rounded6(taut) == d(movement["firstTautAtSeconds"]) and rounded6(taut - d(movement["startsAtSeconds"])) * d(movement["rateFeetPerSecond"]) == d(fixture["ropeSlackFt"]["total"]), {"timeSeconds": str(rounded6(taut)), "riseFeet": fixture["ropeSlackFt"]["total"]})

    inventory_total = sum(d(value) for value in fixture["gearInventoryMassesLb"].values())
    base_case, active, after, support, overload, changed = suite["cases"]
    route_copies_match = d(source_route[0]["lengthFeet"]) == d(route["dRingToPatchEntry"]) and d(source_route[1]["lengthFeet"]) == d(route["looseBightsReturningToEntry"]) and d(source_route[2]["lengthFeet"]) == d(route["patchEntryToBracket"]) and d(proposal_fixture["tether"]["initialDeployedPathLengthFeet"]) == d(route["total"]) and d(proposal_fixture["tether"]["initialSlackFeet"]) == d(fixture["ropeSlackFt"]["total"])
    check("Test route and slack inputs match adopted proposal's deployed path", route_copies_match, {"sourceRouteSegments": source_route, "suiteRoute": route})
    source_event = source_expected["event"]
    check("Movement schedule and first-taut time match adopted expected settlement", d(source_event["startsAtSeconds"]) == d(movement["startsAtSeconds"]) and d(source_event["rateFeetPerSecond"]) == d(movement["rateFeetPerSecond"]) and d(source_event["requestedFeet"]) == d(movement["requestedDistanceFeet"]) and d(source_event["eventEndsAtSeconds"]) == d(movement["eventEndsAtSeconds"]) and d(source_event["firstTautAtSeconds"]) == d(movement["firstTautAtSeconds"]) and d(source_expected["firstTaut"]["loadLb"]) == d(base_case["expected"]["totalLoadLb"]), source_event)
    source_first_taut = source_expected["firstTaut"]
    check("Base first-taut output matches adopted expected settlement", source_first_taut["verticalVelocityAfterSampleFeetPerSecond"] == base_case["expected"]["verticalVelocityAfterTautFeetPerSecond"] and d(source_first_taut["bodyFeetPositionFeet"][2]) == d(base_case["expected"]["bodyZAtTautFt"]) and d(source_first_taut["harnessPositionFeet"][2]) == d(base_case["expected"]["harnessZAtTautFt"]) and source_first_taut["supportAssembly"] == "Holds at 210 lb", {"firstTaut": source_first_taut})
    source_fall = source_expected["fall"]
    check("Fall order and procedure match adopted expected settlement", d(source_fall["bodyFeetStartZ"]) == d(base_case["expected"]["bodyZAtEventEndFt"]) and d(source_fall["landingPlatformTopZ"]) == d(fixture["fall"]["landingPlatformZFt"]) and source_fall["outsideInitiativeSchedule"]["stableOrder"] == fixture["fall"]["outsideInitiativeOrder"] and "min(10, floor(40.4/20))d6 = 2d6" in source_fall["impact"], {"fall": source_fall})
    source_gear = {item["id"]: d(item["massLb"]) for item in target["gearInventory"]}
    suite_gear = fixture["gearInventoryMassesLb"]
    source_gear_copy = {"TEST_WAIST_HARNESS_01": d(suite_gear["harness"]), "TEST_HARNESS_CONNECTOR_01": d(suite_gear["targetConnector"]), "TEST_SATCHEL_01": d(suite_gear["satchel"]), "TEST_OTHER_GEAR_01": d(suite_gear["otherGear"])}
    check("Synthetic body, gear inventory, rope, and support ratings match R7", d(target["bodyMassLb"]) == d(fixture["targetBodyMassLb"]) and d(target["gearAndCargoLb"]) == d(fixture["baseGearAndCargoMassLb"]) and source_gear == source_gear_copy and d(rope["massLb"]) == d(fixture["ropeMassLb"]) and d(rope["lengthFeet"]) == d(fixture["ropeLengthFt"]) and d(rope["maxStaticLoadLb"]) == d(fixture["ropeCapacityLb"]) and d(rope["deadlineSeconds"]) == d(fixture["syntheticCastInput"]["deadlineSeconds"]) and d(support_fixture["ratingLb"]) == d(fixture["completeSupportAssemblyCapacityLb"]), {"bodyLb": target["bodyMassLb"], "gearInventory": suite_gear, "rope": rope, "assemblyRatingLb": support_fixture["ratingLb"]})
    check("Base gear inventory sums to 20 lb and base load to 210 lb", inventory_total == d(fixture["baseGearAndCargoMassLb"]) and d(base_case["input"]["bodyLb"]) + d(base_case["input"]["gearCargoLb"]) + d(base_case["input"]["ropeLb"]) == d(base_case["expected"]["totalLoadLb"]) == Decimal("210"), {"gearInventoryLb": str(inventory_total), "baseLoadLb": base_case["expected"]["totalLoadLb"]})
    check("Base load holds both adopted limits", d(base_case["expected"]["totalLoadLb"]) <= d(fixture["completeSupportAssemblyCapacityLb"]) and d(base_case["expected"]["totalLoadLb"]) <= d(fixture["ropeCapacityLb"]) and base_case["expected"]["assembly"] == "holds" and base_case["expected"]["rope"] == "intact", {"loadLb": base_case["expected"]["totalLoadLb"], "assemblyRatingLb": fixture["completeSupportAssemblyCapacityLb"], "ropeRatingLb": fixture["ropeCapacityLb"]})
    check("Base target/harness geometry and fall result match contract", d(base_case["expected"]["bodyZAtTautFt"]) + d(fixture["harnessOffsetAboveBodyZFt"]) == d(base_case["expected"]["harnessZAtTautFt"]) and d(base_case["expected"]["fallDistanceFt"]) == d(base_case["expected"]["bodyZAtEventEndFt"]) - d(fixture["fall"]["landingPlatformZFt"]) and base_case["expected"]["impactDice"] == "2d6", {"bodyZ": base_case["expected"]["bodyZAtTautFt"], "harnessZ": base_case["expected"]["harnessZAtTautFt"], "fallFeet": base_case["expected"]["fallDistanceFt"]})
    formula = fixture["fall"]["impactFormula"]
    base_dice = min(10, math.floor(d(base_case["expected"]["fallDistanceFt"]) / Decimal("20")))
    active_dice = min(10, math.floor(d(active["expected"]["fallDistanceFt"]) / Decimal("20")))
    check("Provisional impact formula yields 2d6 for both fall distances", formula == "min(10, floor(distanceFeet / 20))d6" and base_dice == active_dice == 2 and base_case["expected"]["impactDice"] == active["expected"]["impactDice"] == after["expected"]["impactDice"] == "2d6", {"formula": formula, "baseDice": base_dice, "activeReleaseDice": active_dice})

    remaining_active = d(movement["eventEndsAtSeconds"]) - d(active["input"]["releaseTimeSeconds"])
    active_delta = remaining_active * d(active["input"]["rateFeetPerSecond"])
    check("Active-event release spends one Action and applies only remaining 10 ft", active["input"]["ordinaryActionSpent"] is True and rounded6(active_delta) == d(active["expected"]["remainingScheduledDisplacementFt"]) and d(active["input"]["bodyZAtReleaseFt"]) + active_delta == d(active["expected"]["bodyZAtEventEndFt"]) == Decimal("50.4") and d(active["expected"]["fallDistanceFt"]) == Decimal("50.4"), {"remainingSeconds": str(remaining_active), "remainingDisplacementFt": str(active_delta), "eventEndZFt": active["expected"]["bodyZAtEventEndFt"]})
    source_active = rule["releaseAndFailure"]["activeEventVoluntaryRelease"]
    check("Active-release branch binds exact t=23 one-Action source branch", d(source_active["timeSeconds"]) == d(active["input"]["releaseTimeSeconds"]) and source_active["actor"] == "TEST_TARGET_01" and "one Action" in source_active["action"] and "remaining 10-ft scheduled displacement" in source_active["result"] and "50.4-ft ordinary fall" in source_active["result"], source_active)
    check("After-event release cannot reset the separate 40.4 ft fall", after["input"]["eventEndsAtSeconds"] == 24 and after["input"]["releaseBeforeFirstFallMarkerV1"] is True and after["expected"]["fallAlreadyStarted"] is True and after["expected"]["releaseResetsFall"] is False and d(after["expected"]["fallDistanceFt"]) == Decimal("40.4"), after["expected"])
    source_after = rule["releaseAndFailure"]["afterEventVoluntaryRelease"]
    check("After-event release branch binds to target's Action before V1", source_after["actor"] == "TEST_TARGET_01" and "before first Fall Marker V1" in source_after["action"] and "Release cannot undo/reset it" in source_after["result"] and "40.4-ft fall" in source_after["result"], source_after)

    support_total = d(support["input"]["bodyLb"]) + d(support["input"]["gearCargoLb"]) + d(support["input"]["ropeLb"])
    check("260-lb probe releases only support weak link", support_total == d(support["expected"]["totalLoadLb"]) == Decimal("260") and support_total > d(support["input"]["supportRatingLb"]) and support_total <= d(support["input"]["ropeRatingLb"]) and support["expected"]["supportWeakLink"] == "releases" and support["expected"]["rope"] == "intact and attached to target-side connector" and support["snapshotOnly"] is True, {"loadLb": str(support_total), "supportRatingLb": support["input"]["supportRatingLb"], "ropeRatingLb": support["input"]["ropeRatingLb"]})
    source_probes = rule["failureProbeCases"]
    check("260-lb probe matches adopted isolated support-release case", source_probes[0]["id"] == support["id"] and d(source_probes[0]["loadLb"]["total"]) == support_total and "exceeds 250 but not 300" in source_probes[0]["decision"] and "no post-failure movement or landing claim" in source_probes[0]["immediatePropertyState"]["scope"], source_probes[0])

    overload_total = d(overload["input"]["bodyLb"]) + d(overload["input"]["gearCargoLb"]) + d(overload["input"]["ropeLb"])
    overload_remaining = d(overload["input"]["bodyLb"]) + d(overload["input"]["gearCargoLb"])
    check("301-lb probe independently releases support and rope", overload_total == d(overload["expected"]["totalLoadLb"]) == Decimal("301") and overload_total > d(overload["input"]["supportRatingLb"]) and overload_total > d(overload["input"]["ropeRatingLb"]) and overload["expected"]["supportWeakLink"] == "releases" and overload["expected"]["rope"] == "vanishes with rope-side connectors" and overload_remaining == d(overload["expected"]["survivingTargetMassLb"]) == Decimal("291") and overload["snapshotOnly"] is True, {"preFailureLoadLb": str(overload_total), "survivingTargetMassLb": str(overload_remaining)})
    check("301-lb probe matches adopted simultaneous-failure case", source_probes[1]["id"] == overload["id"] and d(source_probes[1]["loadLb"]["total"]) == overload_total and "exceeds both limits" in source_probes[1]["decision"] and "no post-failure movement or landing claim" in source_probes[1]["immediatePropertyState"]["scope"], source_probes[1])

    changed_gear = d(changed["input"]["baseGearCargoLb"]) + d(changed["input"]["addedCargoLb"])
    changed_total = d(changed["input"]["bodyLb"]) + changed_gear + d(changed["input"]["ropeLb"])
    changed_remaining = d(changed["input"]["bodyLb"]) + changed_gear
    check("310-lb post-taut recheck triggers both limits at t=23", changed["input"]["changeTimeSeconds"] == 23 and changed_gear == d(changed["expected"]["gearCargoAfterChangeLb"]) == Decimal("120") and changed_total == d(changed["expected"]["totalLoadAfterChangeLb"]) == Decimal("310") and changed_total > d(changed["input"]["supportRatingLb"]) and changed_total > d(changed["input"]["ropeRatingLb"]) and changed_remaining == d(changed["expected"]["survivingTargetMassLb"]) == Decimal("300") and changed["snapshotOnly"] is True, {"postChangeGearLb": str(changed_gear), "preFailureLoadLb": str(changed_total), "survivingTargetMassLb": str(changed_remaining)})
    check("310-lb probe matches adopted immediate-recheck case", source_probes[2]["id"] == changed["id"] and d(source_probes[2]["loadLb"]["afterChange"]["total"]) == changed_total and d(source_probes[2]["decisionSnapshot"]["massChangeAtSeconds"]) == d(changed["input"]["changeTimeSeconds"]) and "no post-failure movement or landing claim" in source_probes[2]["immediatePropertyState"]["scope"], source_probes[2])

    check("R7 contract and case IDs are exact and non-duplicated", proposal["id"] == suite["adoptedContract"]["proposalId"] and proposal["revision"] == 7 and len(proposal["sourceBindings"]) == 13 and proposal["proposedTestOnlyRule"]["id"] == suite["adoptedContract"]["id"] and len({case["id"] for case in suite["cases"]}) == len(suite["cases"]), {"proposalId": proposal["id"], "sourceBindings": len(proposal["sourceBindings"]), "contractId": proposal["proposedTestOnlyRule"]["id"], "cases": len(suite["cases"])})

    passed = sum(1 for item in checks if item["passed"])
    failed = len(checks) - passed
    report = {
        "schemaVersion": 1,
        "id": "IE286-W2-TESTONLY-COMPONENT-VALIDATION-01",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "classification": "LOCAL_TEST_ONLY_CONTRACT_ARITHMETIC_AND_BRANCH_CHECK_NOT_RUNTIME_OR_CAMPAIGN_EXECUTION",
        "proposal": {"path": str(PROPOSAL_PATH.relative_to(ROOT)).replace("\\", "/"), "bytes": len(proposal_bytes), "sha256": sha256(proposal_bytes)},
        "ownerAdoption": {"path": str(ADOPTION_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(adoption_bytes), "ownerAdoptionCommitPrefix": EXPECTED_ADOPTION_COMMIT},
        "queue": {"path": QUEUE_PATH, "sha256": sha256(queue_bytes), "applied": queue["currentAuthority"]["reviewedApplied"], "pending": queue["currentAuthority"]["pending"], "acceptedUnapplied": queue["currentAuthority"]["acceptedUnapplied"], "nextIdentity": queue["nextIdentity"], "blockers": queue["nextBlockerIds"]},
        "testSuite": {"path": str(SUITE_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(suite_bytes), "caseCount": len(suite["cases"])},
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": failed,
        "checks": checks,
        "nonEffects": {"gameRuntimeExecuted": False, "campaignEventAsserted": False, "legalPaidCastEstablished": False, "sealIssued": False, "blockerClosed": False, "identityAccepted": False, "identityApplied": False, "canonChanged": False, "runtimeChanged": False, "queueChanged": False}
    }
    (PACKET_DIR / "LOCAL_VALIDATION_REPORT.json").write_bytes((json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps({"report": str(PACKET_DIR / "LOCAL_VALIDATION_REPORT.json"), "checkCount": len(checks), "passedChecks": passed, "failedChecks": failed}, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
