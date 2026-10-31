from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import zipfile


AUDIT = Path(__file__).resolve().parent
OUT = AUDIT / "rank9_summon_elemental_avatar_closure_350_delivery"
DELTA_PATH = OUT / "SH202_B01_SH330_CONDITIONAL_TRANSITION_DELTA_350.json"
REPORT_PATH = OUT / "SH202_B01_SH330_REPLAY_VERIFICATION_350.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def parts(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not pointer.startswith("/"):
        raise AssertionError(f"invalid JSON pointer: {pointer}")
    return [x.replace("~1", "/").replace("~0", "~") for x in pointer[1:].split("/")]


def get(state: object, pointer: str):
    value = state
    for part in parts(pointer):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def set_value(state: object, pointer: str, value: object) -> None:
    path = parts(pointer)
    parent = state
    for part in path[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    if isinstance(parent, list):
        parent[int(path[-1])] = copy.deepcopy(value)
    else:
        parent[path[-1]] = copy.deepcopy(value)


def main() -> None:
    delta = json.loads(DELTA_PATH.read_text(encoding="utf-8"))
    checks: list[dict] = []

    def ck(label: str, ok: bool, evidence: object = None) -> None:
        checks.append({"check": label, "passed": bool(ok), "evidence": evidence})
        if not ok:
            raise AssertionError(f"{label}: {evidence}")

    expected_tests = [f"SH330-T0{i}" for i in range(1, 7)]
    ck("only the six SH330 tests are in scope", [row["testId"] for row in delta["cases"]] == expected_tests, [row["testId"] for row in delta["cases"]])
    ck("authority is still 825 applied / 23 pending / 0 accepted-unapplied", delta["authorityBefore"] == delta["authorityAfter"] == {"reviewedApplied": 825, "pending": 23, "acceptedUnapplied": 0, "completeStandaloneProcedures": 549, "scopedInterfaces": 173}, delta["authorityAfter"])
    ck("packet does not accept, apply, or authorize an identity", delta["acceptedIds"] == delta["appliedIds"] == delta["applicationAuthorizedIds"] == [] and delta["heldIds"] == ["summon-elemental-avatar"], {k: delta[k] for k in ["acceptedIds", "appliedIds", "applicationAuthorizedIds", "heldIds"]})
    ck("current queue reclassifies DF218-B03 as historical and closed", delta["queueMetadataCorrection"]["fieldAfter"] == {"linkedPendingComparisonId": None, "linkedPendingBlockerIds": [], "linkedHistoricalComparisonId": "timeless-form", "linkedHistoricalBlockerIds": ["DF218-B03"], "linkedHistoricalDisposition": "SEALED_ACCEPT_APPLIED_CLOSURE346", "linkClassification": "HISTORICAL_CLOSED_NOT_PENDING"}, delta["queueMetadataCorrection"]["fieldAfter"])
    ck("Closure350 preserves the already corrected queue classification without changing its metadata or identity sets", delta["queueMetadataCorrection"]["fieldBefore"] == delta["queueMetadataCorrection"]["fieldAfter"] and delta["queueMetadataCorrection"]["metadataChangedThisStep"] is False and delta["queueMetadataCorrection"]["acceptedOrAppliedSetChanged"] is False, delta["queueMetadataCorrection"])
    repo_root = AUDIT.parents[4]
    bound_records = [delta["directorRuling"]["directorReturnBinding"], *delta["previousPacketBindings"].values()]
    for binding in bound_records:
        path = repo_root / binding["path"]
        raw = path.read_bytes()
        ck(f"{binding['path']}: prior ruling/evidence byte binding", len(raw) == binding["bytes"] and hashlib.sha256(raw).hexdigest() == binding["sha256"], binding)
    director_return = json.loads((repo_root / delta["directorRuling"]["directorReturnBinding"]["path"]).read_text(encoding="utf-8"))
    disposition = director_return["disposition"]
    ck("Closure349 sealed HOLD preserves closed R1/R2 and sole open R3 with no acceptance or application", disposition["status"] == "SEALED_HOLD" and disposition["acceptedIds"] == disposition["appliedIds"] == [] and disposition["heldIds"] == ["summon-elemental-avatar"] and disposition["closedResidualIds"] == ["SH348-R1", "SH348-R2"] and disposition["openResidualIds"] == ["SH348-R3"] and disposition["applicationAuthorized"] is False, disposition)
    residuals = {row["id"]: row for row in director_return["residuals"]}
    ck("Closure349 retains GPT's two closed rulings and exact native Avatar geometry requirement", residuals["SH348-R1"]["status"] == residuals["SH348-R2"]["status"] == "CLOSED" and residuals["SH348-R3"]["status"] == "PARTIALLY_CORRECTED_OPEN" and "[10,10,10]" in residuals["SH348-R3"]["exactDefect"] and "[5,5,5]" in residuals["SH348-R3"]["requiredCorrection"], residuals)
    closure349_delivery = json.loads((repo_root / delta["previousPacketBindings"]["delivery"]["path"]).read_text(encoding="utf-8"))
    ck("Closure349 director record binds the exact previously submitted archive", director_return["boundCommit"] == "ef1d8aa35d84fa660e8854821418cfb1716c7b9a" and director_return["archiveSha256"] == closure349_delivery["archive"]["sha256"] == "3c500e083ac838b77dc84ab6f5477f6325a8f5b6984674e796a9851eac0715c6" and director_return["independentReview"]["archiveMemberBindingsMatch"] == 26 and director_return["independentReview"]["mirroredGitBlobsMatch"] == 8, {"commit": director_return["boundCommit"], "archive": closure349_delivery["archive"], "independentReview": director_return["independentReview"]})

    scenario_lookup = {}
    transition_total = 0
    reverse_total = 0
    for case in delta["cases"]:
        for scenario in case["scenarios"]:
            sid = scenario["scenarioId"]
            scenario_lookup[sid] = scenario
            state = copy.deepcopy(scenario["startingState"])
            ck(f"{sid}: starting state hash", digest(state) == scenario["startingStateSha256"], scenario["startingStateSha256"])
            all_ops = []
            for transition in scenario["transitions"]:
                transition_total += 1
                ck(f"{sid}: ordered pre-state {transition['ordinal']}", state == transition["beforeState"] and digest(state) == transition["beforeStateSha256"], transition["beforeStateSha256"])
                for op in transition["forwardOperations"]:
                    before = copy.deepcopy(get(state, op["path"]))
                    if before != op["before"]:
                        raise AssertionError(f"{sid}: forward precondition mismatch at {op['path']}")
                    set_value(state, op["path"], op["after"])
                ck(f"{sid}: ordered post-state {transition['ordinal']}", state == transition["afterState"] and digest(state) == transition["afterStateSha256"], transition["afterStateSha256"])
                expected_inverse = [{"path": op["path"], "before": op["after"], "after": op["before"]} for op in reversed(transition["forwardOperations"])]
                ck(f"{sid}: exact inverse patch {transition['ordinal']}", transition["inverseOperations"] == expected_inverse, transition["inverseOperations"])
                all_ops.append(transition["forwardOperations"])
                for pointer in scenario["unchangedPaths"]:
                    ck(f"{sid}: unaffected path {pointer} after event {transition['ordinal']}", get(state, pointer) == get(scenario["startingState"], pointer), {"path": pointer, "value": get(state, pointer)})
            ck(f"{sid}: final state", state == scenario["finalState"] and digest(state) == scenario["finalStateSha256"], scenario["finalStateSha256"])
            reverse_state = copy.deepcopy(state)
            for operations in reversed(all_ops):
                for op in reversed(operations):
                    if get(reverse_state, op["path"]) != op["after"]:
                        raise AssertionError(f"{sid}: inverse precondition mismatch at {op['path']}")
                    set_value(reverse_state, op["path"], op["before"])
            reverse_total += 1
            ck(f"{sid}: full inverse traversal restores exact starting state", reverse_state == scenario["startingState"] and digest(reverse_state) == scenario["startingStateSha256"], digest(reverse_state))

    # Independently derive damage resistance, root settlement, tempHP/HP and finite-summon lifecycle.
    t02 = delta["cases"][1]["scenarios"]
    fork = delta["preservedSourceFork"]
    ck("T02 binds the preserved Return285 Avatar body/profile", fork["avatarBodyId"] == "A:cast1:body1" and fork["avatarProfileId"] == "SH202-ELEMENTAL" and fork["inheritedFixtureStatus"] == "CONDITIONAL_AUTHORED_FIXTURE_NOT_GAMEPLAY", fork)
    for scenario in t02:
        for transition in scenario["transitions"]:
            if transition["event"]["type"] != "resolve_avatar_damage_root":
                continue
            before_avatar = transition["beforeState"]["avatar"]
            root = transition["event"]["root"]
            calculated = []
            for component in root["components"]:
                if component["damageType"] in before_avatar["immunities"]:
                    resolved = 0
                    defense = "immune"
                elif component["damageType"] in before_avatar["resistances"]:
                    resolved = component["amount"] // 2
                    defense = "resistance-half-floor"
                else:
                    resolved = component["amount"]
                    defense = "none"
                calculated.append({"componentId": component["componentId"], "damageType": component["damageType"], "rawAmount": component["amount"], "resolvedAmount": resolved, "defense": defense, "rootId": root["rootId"], "dealerRootId": component["dealerRootId"]})
            total = sum(row["resolvedAmount"] for row in calculated)
            temp_used = min(before_avatar["tempHP"], total)
            hp_damage = max(0, total - temp_used)
            hp_after = max(0, before_avatar["HP"] - hp_damage)
            temp_after = before_avatar["tempHP"] - temp_used
            observed = transition["observedResult"]
            after_avatar = transition["afterState"]["avatar"]
            ck(f"{scenario['scenarioId']}: independently derived typed damage", observed["resolvedComponents"] == calculated and observed["totalResolvedOnce"] == total, calculated)
            ck(f"{scenario['scenarioId']}: independently derived one-time HP/tempHP settlement", after_avatar["HP"] == hp_after and after_avatar["tempHP"] == temp_after and observed["hpAfter"] == hp_after and observed["tempHPAfter"] == temp_after, {"expectedHP": hp_after, "expectedTempHP": temp_after})
            ck(f"{scenario['scenarioId']}: one root creates one lifecycle settlement", len(transition["afterState"]["lifecycleSettlements"]) == len(transition["beforeState"]["lifecycleSettlements"]) + 1 and transition["afterState"]["lifecycleSettlements"][-1]["rootId"] == root["rootId"], root["rootId"])
    c06 = t02[0]["transitions"][0]["observedResult"]
    c08 = t02[1]["transitions"][0]["observedResult"]
    temp = t02[2]["transitions"][0]["observedResult"]
    ck("Return331's same-root fire6->3 plus force8 totals11", c06["resolvedComponents"][0]["resolvedAmount"] == 3 and c06["resolvedComponents"][1]["resolvedAmount"] == 8 and c06["totalResolvedOnce"] == 11 and c06["settlementCountAfter"] == 1, c06)
    ck("SH330-T02 fire11/force8 totals13", c08["resolvedComponents"][0]["resolvedAmount"] == 5 and c08["resolvedComponents"][1]["resolvedAmount"] == 8 and c08["totalResolvedOnce"] == 13, c08)
    ck("synthetic HP30/tempHP3 overlay settles to HP20/tempHP0", temp["hpAfter"] == 20 and temp["tempHPAfter"] == 0 and temp["settlementCountAfter"] == 1, temp)
    separate = t02[3]["transitions"]
    ck("separate damage roots retain ordered independent settlements", separate[0]["event"]["root"]["rootId"] != separate[1]["event"]["root"]["rootId"] and separate[1]["observedResult"]["settlementCountAfter"] == 2 and separate[1]["observedResult"]["hpAfter"] == 22, [t["observedResult"] for t in separate])

    # Independently verify the controller reservation/cancellation correction.
    t03 = delta["cases"][2]["scenarios"]
    change = t03[0]["transitions"][0]
    initial_ledger = change["beforeState"]["strikeLedgers"]["round-21"]
    post_ledger = change["afterState"]["strikeLedgers"]["round-21"]
    ck("T03 C03 binds reservedSlots3/attempts2 and cancels slot3 without refund", initial_ledger["reservedSlots"] == 3 and initial_ledger["attemptedSlots"] == 2 and post_ledger["attemptedSlots"] == 3 and post_ledger["cancelledSlots"] == [3] and change["observedResult"]["thirdStrikeAccepted"] is False and change["observedResult"]["fourthStrikeAccepted"] is False and change["observedResult"]["refund"] == 0, {"before": initial_ledger, "after": post_ledger, "result": change["observedResult"]})
    issue = next(t for t in t03[0]["transitions"] if t["event"]["type"] == "issue_new_controller_order")
    execute = next(t for t in t03[0]["transitions"] if t["event"]["type"] == "execute_at_original_owner_attached_phase")
    restore = t03[0]["transitions"][-1]
    ck("T03 later controller order satisfies every stated issuance gate", issue["observedResult"]["accepted"] is True and all(issue["observedResult"]["checks"].values()), issue["observedResult"]["checks"])
    ck("T03 new order executes only on original owner's scheduled attached phase", execute["observedResult"]["executed"] is True and execute["observedResult"]["phaseOwner"] == "owner-A" and execute["observedResult"]["phaseId"] == "owner-A-attached-22", execute["observedResult"])
    ck("T03 return of control restores no old order, HP, or resources", restore["observedResult"]["oldOrderRestored"] is False and restore["observedResult"]["restorationGrantedHPOrResource"] is False and restore["afterState"]["pendingOrder"] is None and restore["afterState"]["hp"] == restore["beforeState"]["hp"] and restore["afterState"]["resourceHistory"] == restore["beforeState"]["resourceHistory"], restore["observedResult"])
    round22 = restore["afterState"]["strikeLedgers"]["round-22"]
    ck("T03 return cancels every unattempted reserved round-22 slot without refund, transfer, or order restoration", round22["reservedSlots"] == 3 and round22["attemptedSlots"] == 0 and round22["consumedSlots"] == [] and round22["cancelledSlots"] == [1, 2, 3] and restore["observedResult"]["capacityConsumed"] == 3 and restore["observedResult"]["refund"] == 0 and restore["observedResult"]["strikeCapReset"] is False and restore["observedResult"]["pendingOrderAfter"] is None, {"ledger": round22, "result": restore["observedResult"]})
    spent = t03[1]["transitions"][0]
    ck("T03 control change after three spent slots does not refresh cap", spent["afterState"]["strikeLedgers"]["round-21"]["attemptedSlots"] == 3 and t03[1]["transitions"][1]["observedResult"]["accepted"] is False, spent["afterState"]["strikeLedgers"]["round-21"])

    # Independently choose same-family aura winners and calculate packet defenses.
    t04 = delta["cases"][3]["scenarios"]
    for scenario in t04:
        transition = scenario["transitions"][0]
        before = transition["beforeState"]
        due = [s for s in before["auraSources"] if s["due"] and not s["consumed"]]
        eligible = [s for s in due if s["sourceAlive"] and s["withinAura"] and not s["auraIntersectionSuppressed"]]
        winner = min(eligible, key=lambda s: (-s["rolledPool"], s["applicationOrder"], s["sourceId"])) if eligible else None
        observed = transition["observedResult"]
        ck(f"{scenario['scenarioId']}: independent pool/tie winner", (observed["winner"]["sourceId"] if observed["winner"] else None) == (winner["sourceId"] if winner else None), {"expected": winner, "observed": observed["winner"]})
        ck(f"{scenario['scenarioId']}: every due source consumed", all(s["consumed"] for s in transition["afterState"]["auraSources"] if s["due"]), transition["afterState"]["auraSources"])
        if winner:
            saved = transition["event"]["dexSaveTotal"] >= winner["dc"]
            after_save = winner["rolledPool"] // 2 if saved else winner["rolledPool"]
            fire_after_resist = after_save // 2 if "fire" in before["recipient"]["resistances"] else after_save
            packet = observed["winner"]
            ck(f"{scenario['scenarioId']}: winning dealer/DC/root metadata", (packet["dealerId"], packet["dc"], packet["rootId"]) == (winner["dealerId"], winner["dc"], winner["rootId"]), packet)
            ck(f"{scenario['scenarioId']}: winning pool resolves save then fire resistance once", packet["damageAfterDefense"] == fire_after_resist and packet["saveSucceeded"] == saved, packet)
    ck("T04 packet application counts are one and later losing/suppressed work is never replayed", all(s["transitions"][0]["observedResult"]["packetsApplied"] == 1 and (len(s["transitions"]) < 2 or s["transitions"][1]["observedResult"]["priorLosingOrSuppressedPacketReplayed"] is False) for s in t04), [s["scenarioId"] for s in t04])

    # Clocks: no due-time drift or synthesized actor/source budget updates.
    t05 = delta["cases"][4]["scenarios"]
    standard = t05[0]["transitions"]
    due_index = next(i for i, t in enumerate(standard) if t["event"]["type"] == "resolve_carried_exposure_due")
    due = standard[due_index]
    ordinary_types = {"regular_start_before_carried_due", "later_regular_start_after_carried_due"}
    processed_calendar = [t["event"]["atMs"] for t in standard if t["event"]["type"] in ordinary_types | {"resolve_carried_exposure_due"}]
    ck("T05 immutable due6 survives initiative t2 and regular START t4", standard[0]["afterState"]["nextDueMs"] == 6000 and standard[1]["afterState"]["nextDueMs"] == 6000 and standard[1]["observedResult"]["auraPulse"] is False, [standard[0]["afterState"]["nextDueMs"], standard[1]["afterState"]["nextDueMs"]])
    ck("T05 due callback derives t6 coincidence from its declared calendar and consumes once", due["observedResult"]["dueTimestampMs"] == 6000 and due["observedResult"]["pulse"] is True and due["observedResult"]["coalescedCoincidentRegularStart"] is True and due["observedResult"]["coincidenceDerivedFromCalendar"] is True and due["afterState"]["consumedOpportunityIds"].count("avatar-A/recipient-B/exposure-due-6000") == 1 and processed_calendar == standard[0]["beforeState"]["regularStartCalendar"], {"result": due["observedResult"], "processed": processed_calendar})
    later = [t for t in standard if t["event"]["type"] == "later_regular_start_after_carried_due"]
    ck("T05 later actual START markers are calendar-bound, strictly after due and independently pulse", [t["event"]["atMs"] for t in later] == [10000, 16000] and all(t["observedResult"]["strictlyLaterThanCarriedDue"] and t["observedResult"]["calendarBound"] for t in later) and later[-1]["observedResult"]["pulseCountAfter"] == 3, [t["observedResult"] for t in later])
    for scenario in t05[1:]:
        callback = next(t for t in scenario["transitions"] if t["event"]["type"] == "resolve_carried_exposure_due")
        ordinary = [t for t in scenario["transitions"] if t["event"]["type"] in ordinary_types]
        processed = [t["event"]["atMs"] for t in ordinary]
        ck(f"{scenario['scenarioId']}: noncoincident due derives from [4000,10000] after every ordinary marker is processed", scenario["startingState"]["regularStartCalendar"] == [4000, 10000] and processed == [4000, 10000] and callback["observedResult"]["opportunityConsumed"] is True and callback["observedResult"]["pulse"] is False and callback["observedResult"]["coalescedCoincidentRegularStart"] is False and callback["observedResult"]["coincidenceDerivedFromCalendar"] is True and callback["afterState"]["pendingExposureDue"] is False, {"calendar": scenario["startingState"]["regularStartCalendar"], "processed": processed, "due": callback["observedResult"]})

    # A local field clips only the aura intersection; body identity and strike/command capacity remain.
    t06 = delta["cases"][5]["scenarios"]
    fork = delta["preservedSourceFork"]
    fork_archive = (repo_root / fork["archivePath"]).read_bytes()
    ck("preserved Return285 source archive and case member remain byte-bound", len(fork_archive) == fork["archiveBytes"] and hashlib.sha256(fork_archive).hexdigest() == fork["archiveSha256"], fork)
    with zipfile.ZipFile(repo_root / fork["archivePath"]) as archive:
        source_member = archive.read(fork["memberPath"])
    ck("preserved Return285 source case member remains byte-bound", len(source_member) == fork["memberBytes"] and hashlib.sha256(source_member).hexdigest() == fork["memberSha256"], fork)
    source_case = json.loads(source_member)
    source_event = source_case["events"][fork["eventIndexZeroBased"]]
    native_avatar = source_event["after"]["bodies"][fork["avatarBodyId"]]
    native_box = native_avatar["box"]
    ck("T06 profile dimensions are independently read from the bound Return285 formation event", source_event["id"] == "RANK9SUMMONHOSTS5129-SUMMON-ELEMENTAL-AVATAR-B:6" and native_avatar["profileId"] == "SH202-ELEMENTAL" and native_box == fork["avatarBoxFeet"] == [10, 10, 10], {"event": source_event["id"], "bodyId": native_avatar["id"], "profileId": native_avatar["profileId"], "nativeBoxFeet": native_box})
    expected_half_extents = [dimension / 2 for dimension in native_box]
    expected_bounds = {axis: [-half, half] for axis, half in zip(("x", "y", "z"), expected_half_extents)}
    for scenario in t06:
        start = scenario["startingState"]
        volume = start["sourceBodyVolume"]
        source_bounds = start["sourceBodyVolume"]["bounds"]
        recipient_bounds = start["recipientVolume"]["bounds"]
        region = start["suppressionRegion"]["bounds"]
        intersects = lambda volume, field: all(volume[axis][0] <= field[axis][1] and field[axis][0] <= volume[axis][1] for axis in ("x", "y", "z"))
        distance = sum((start["sourceBody"]["position"][i] - start["recipientPosition"][i]) ** 2 for i in range(3)) ** 0.5
        ck(f"{scenario['scenarioId']}: source body and both volume records match native profile dimensions", start["sourceBody"]["id"] == native_avatar["id"] == fork["avatarBodyId"] and start["sourceBody"]["profileId"] == native_avatar["profileId"] and start["sourceBody"]["box"] == native_box and volume["kind"] == "BOUND_NATIVE_PROFILE_BOX" and volume["profileId"] == native_avatar["profileId"] and volume["profileBoxFeet"] == native_box and volume["center"] == start["sourceBody"]["position"] == [0, 0, 0] and volume["halfExtentsFeet"] == expected_half_extents == [5, 5, 5] and volume["bounds"] == expected_bounds == {"x": [-5, 5], "y": [-5, 5], "z": [-5, 5]}, {"bodyBoxFeet": start["sourceBody"].get("box"), "profileBoxFeet": volume.get("profileBoxFeet"), "halfExtentsFeet": volume.get("halfExtentsFeet"), "bounds": volume.get("bounds")})
        ck(f"{scenario['scenarioId']}: actual 3D volumes bind source outside and recipient inside the suppression field while in aura", start["auraRadiusFeet"] == 10 and distance == start["recipientDistanceToSourceFeet"] and distance <= start["auraRadiusFeet"] and not intersects(source_bounds, region) and intersects(recipient_bounds, region) and start["sourceVolumeIntersectsSuppressionField"] is False and start["recipientVolumeIntersectsSuppressionField"] is True, {"sourceVolume": source_bounds, "recipientVolume": recipient_bounds, "field": region, "distance": distance})
        for transition in scenario["transitions"]:
            for label in ("beforeState", "afterState"):
                state_volume = transition[label]["sourceBodyVolume"]
                ck(f"{scenario['scenarioId']}: {label} preserves native-profile source volume at transition {transition['ordinal']}", state_volume == volume and transition[label]["sourceBody"]["box"] == native_box, {"volume": state_volume, "box": transition[label]["sourceBody"]["box"]})
            observed = transition["observedResult"]
            if "sourceVolumeBounds" in observed:
                ck(f"{scenario['scenarioId']}: observed transition {transition['ordinal']} volume fields use native bounds", observed["sourceVolumeBounds"] == expected_bounds and observed["sourceVolumeIntersectsSuppressionField"] is False, {"sourceVolumeBounds": observed["sourceVolumeBounds"], "intersects": observed["sourceVolumeIntersectsSuppressionField"]})
        due = scenario["transitions"][0]
        ck(f"{scenario['scenarioId']}: local due opportunity is consumed without body/strike/command loss", due["observedResult"]["dueOpportunityConsumed"] and due["observedResult"]["bodyPersists"] and due["observedResult"]["bodySuppressed"] is False and due["afterState"]["strikeLedger"] == due["beforeState"]["strikeLedger"] and due["afterState"]["commandEligible"] == due["beforeState"]["commandEligible"], due["observedResult"])
    first_exit = t06[0]["transitions"][1]
    ck("T06 exit records movement outside field while remaining inside aura; exit itself has no pulse", first_exit["event"]["recipientPositionAfter"] == [6, 0, 0] and first_exit["observedResult"]["recipientVolumeIntersectsSuppressionFieldAfter"] is False and first_exit["observedResult"]["recipientStillWithinAura"] is True and first_exit["observedResult"]["pulseOnLeaving"] is False, first_exit["observedResult"])
    ck("T06 next independent marker resumes only for the still-active source", t06[0]["transitions"][2]["event"]["atMs"] == 12000 and t06[0]["transitions"][2]["observedResult"]["pulse"] is True and t06[0]["transitions"][2]["observedResult"]["sourceBodyActive"] is True, t06[0]["transitions"][2]["observedResult"])
    expired = t06[1]
    markers = expired["startingState"]["regularStartCalendar"]
    suppressed = [t["event"]["atMs"] for t in expired["transitions"] if t["event"]["type"] == "local_suppressed_due"]
    expiry_transition = next(t for t in expired["transitions"] if t["event"]["type"] == "expire_source_at_original_deadline")
    ck("T06 expiry branch consumes every clipped t6-t54 marker and the expiry-coincident t60 marker on the original deadline", markers == list(range(6000, 66001, 6000)) and suppressed == markers[:-2] and expiry_transition["event"]["atMs"] == expired["startingState"]["sourceDeadlineMs"] == 60000 and expiry_transition["event"].get("coincidentMarkerId") == "recipient-B-start-60" and expiry_transition["observedResult"]["dueOpportunityConsumed"] is True and expiry_transition["observedResult"]["expiryPrecedesCoincidentMarker"] is True, {"markers": markers, "suppressed": suppressed, "expiry": expiry_transition["observedResult"]})
    expired_exit, expired_marker = expired["transitions"][-2:]
    ck("T06 after expiry, movement at t61 creates no pulse and declared t66 marker cannot revive source", expired_exit["event"]["atMs"] == 61000 and expired_exit["event"]["recipientPositionAfter"] == [6, 0, 0] and expired_exit["observedResult"]["pulseOnLeaving"] is False and expired_marker["event"]["atMs"] == 66000 and expired_marker["event"]["markerId"] == "recipient-B-start-66" and expired_marker["observedResult"]["pulse"] is False and expired_marker["observedResult"]["sourceBodyActive"] is False, {"exit": expired_exit["observedResult"], "marker": expired_marker["observedResult"]})
    ck("fixtures are conditional and do not claim runtime/gameplay or extra providers", delta["provenance"] == {"conditionalFixturesAreGameplay": False, "userAuthorshipClaim": False, "canonicalMutation": False, "runtimeExecuted": False, "identityAccepted": False, "applicationPerformed": False}, delta["provenance"])

    report = {
        "id": "SH202-B01-SH330-INDEPENDENT-REPLAY-VERIFICATION-350",
        "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
        "sourceDelta": {"path": DELTA_PATH.relative_to(AUDIT.parents[4]).as_posix(), "bytes": DELTA_PATH.stat().st_size, "sha256": hashlib.sha256(DELTA_PATH.read_bytes()).hexdigest()},
        "checkCount": len(checks), "passedChecks": sum(row["passed"] for row in checks), "failedChecks": sum(not row["passed"] for row in checks),
        "scenarioCount": len(scenario_lookup), "transitionCount": transition_total, "fullyReversedScenarioCount": reverse_total,
        "checks": checks,
        "scopeIds": ["summon-elemental-avatar"], "blockerIds": ["SH202-B01"],
        "runtimeExecuted": False, "canonicalFilesChanged": False, "acceptedIds": [], "appliedIds": [],
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checks": report["checkCount"], "passed": report["passedChecks"], "scenarios": report["scenarioCount"], "transitions": report["transitionCount"], "fullyReversed": report["fullyReversedScenarioCount"]}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
