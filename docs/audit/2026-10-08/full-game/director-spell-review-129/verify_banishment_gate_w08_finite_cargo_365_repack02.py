from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "banishment_gate_witness365_w08_finite_cargo02_final03"
OLD_VERIFIER = HERE / "verify_banishment_gate_w08_finite_cargo_365.py"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_hash(value: Any) -> str:
    return sha(canonical(value))


def get_at(root: Any, parts: list[str]) -> Any:
    current = root
    for part in parts:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def set_at(root: Any, parts: list[str], value: Any, remove: bool = False) -> None:
    current = root
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    key = parts[-1]
    if isinstance(current, list):
        index = int(key)
        if remove:
            current.pop(index)
        elif index == len(current):
            current.append(value)
        else:
            current[index] = value
    elif remove:
        del current[key]
    else:
        current[key] = value


def apply_ops(state: Any, ops: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(state)
    for op in ops:
        path = op["path"]
        if op["op"] == "remove":
            assert get_at(result, path) == op["before"]
            set_at(result, path, None, remove=True)
        elif op["op"] == "add":
            set_at(result, path, copy.deepcopy(op["after"]))
        elif op["op"] == "replace":
            assert get_at(result, path) == op["before"]
            set_at(result, path, copy.deepcopy(op["after"]))
        else:
            raise AssertionError(f"unknown state operation: {op['op']}")
    return result


def replay(start: Any, events: list[dict[str, Any]]) -> Any:
    state = copy.deepcopy(start)
    for event in events:
        assert state_hash(state) == event["beforeStateSha256"], event["eventId"]
        state = apply_ops(state, event["forwardOperations"])
        assert state == event["stateAfter"], event["eventId"]
        assert state_hash(state) == event["afterStateSha256"], event["eventId"]
    return state


def reverse_replay(final: Any, events: list[dict[str, Any]]) -> Any:
    state = copy.deepcopy(final)
    for event in reversed(events):
        assert state_hash(state) == event["afterStateSha256"], event["eventId"]
        state = apply_ops(state, event["inverseOperations"])
        assert state_hash(state) == event["beforeStateSha256"], event["eventId"]
    return state


def resolve_json_pointer(value: Any, pointer: str) -> Any:
    assert pointer.startswith("/") and "#" not in pointer
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    return get_at(value, parts)


def source_audit(packet: Path) -> dict[str, Any]:
    old_spec = importlib.util.spec_from_file_location("w08_repack01_verifier", OLD_VERIFIER)
    assert old_spec and old_spec.loader
    old = importlib.util.module_from_spec(old_spec)
    sys.modules[old_spec.name] = old
    old_spec.loader.exec_module(old)
    legacy_checks = old.verify_source_files(packet)

    bindings = load(packet / "W08_SOURCE_BINDINGS_365.json")["bindings"]
    bound_members: set[str] = set()
    checked = 0
    for binding in bindings:
        member = binding.get("packetMember") or binding.get("member")
        if not member:
            continue
        path = packet / member
        data = path.read_bytes()
        assert len(data) == binding["bytes"], member
        assert sha(data) == binding["sha256"], member
        bound_members.add(member)
        checked += 1

    case = load(packet / "W08_FINITE_SUMMON_CARGO_CASE_365_TESTONLY.json")
    gate = load(packet / "sources" / "RETURN327_banishment-gate.json")
    model = load(packet / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json")
    label_sources = {"PG9": gate["procedure"], "AC5": model["sharedRules"]}
    json_refs = 0
    text_refs = 0
    events = case["commonPrefix"]["events"] + [e for b in case["terminalForks"] for e in b["events"]]
    for event in events:
        assert all("#PG9-" not in ref for ref in event.get("sourcePointers", []))
        for ref in event.get("sourcePointers", []):
            member, sep, pointer = ref.partition("#")
            assert sep and member.endswith(".json") and pointer.startswith("/")
            assert member in bound_members and (packet / member).is_file(), (event["eventId"], ref)
            resolve_json_pointer(load(packet / member), pointer)
            json_refs += 1
        for locator in event.get("sourceTextLocations", []):
            member, sep, fragment = locator.partition("#")
            assert sep and member.lower().endswith((".md", ".txt"))
            assert (packet / member).is_file(), (event["eventId"], locator)
            raw = (packet / member).read_text(encoding="utf-8")
            if fragment.startswith("line-"):
                line = int(fragment[5:])
                assert 1 <= line <= len(raw.splitlines()), locator
            elif fragment.startswith("lines-"):
                first, last = map(int, fragment[6:].split("-"))
                assert 1 <= first <= last <= len(raw.splitlines()), locator
            else:
                assert fragment and fragment in raw, locator
            text_refs += 1
        for label in event.get("sourceParagraphLabels", []):
            source_group = "PG9" if label.startswith("PG9-") else "AC5" if label.startswith("AC5-") else None
            assert source_group is not None and label in label_sources[source_group], (event["eventId"], label)

    mage = load(packet / "sources" / "MAGE_CLASS_PLAYTEST.json")
    profile = load(packet / "sources" / "W08_CASTER_PROFILES_365_TESTONLY.json")
    counterspell_index = next(i for i, card in enumerate(mage["cards"]) if card.get("id") == "mage.arch.counterspell")
    assert profile["profileSourceBindings"]["mageClass"]["counterspellPointer"] == f"/cards/{counterspell_index}"
    profile_data = packet / profile["profileSourceBindings"]["mageClass"]["member"]
    assert profile_data.is_file()
    assert mage["rpByClassLevel"][8] == 26 and mage["rpByClassLevel"][16] == 50
    assert profile["profiles"][0]["derived"]["RPMaximum"] == 50
    assert profile["profiles"][1]["derived"]["RPMaximum"] == 26
    return {"legacyPinnedSourceChecks": legacy_checks, "sourceBindingsVerified": checked,
            "resolvableJsonPointers": json_refs, "separateTextLocations": text_refs,
            "paragraphLabelsSeparateAndResolvable": True, "mageCounterspellIndex": counterspell_index,
            "sourcePointerAuditPass": True}


def semantic_audit(packet: Path) -> dict[str, Any]:
    case = load(packet / "W08_FINITE_SUMMON_CARGO_CASE_365_TESTONLY.json")
    common = case["commonPrefix"]
    initial = common["initialState"]
    assert state_hash(initial) == common["initialStateSha256"]
    assert initial["testFixtureBoundaries"]["allCasterProfilesAreTestOnly"] is True
    assert initial["testFixtureBoundaries"]["AC5BanishElementalExtensionImported"] is False
    assert initial["testFixtureBoundaries"]["AC5X17MechanicsImported"] is False
    end_common = replay(initial, common["events"])
    assert end_common == common["finalState"]
    assert state_hash(end_common) == common["finalStateSha256"]
    assert reverse_replay(end_common, common["events"]) == initial

    gate_caster = end_common["actors"]["gateCaster"]
    owner = end_common["actors"]["championOwner"]
    champion = end_common["actors"]["champion"]
    assert gate_caster["class"] == owner["class"] == "Mage"
    assert gate_caster["classLevel"] == 17 and owner["classLevel"] == 9
    assert gate_caster["rp"] == {"initial": 50, "maximum": 50, "current": 24, "spent": 26}
    assert owner["rp"] == {"initial": 26, "maximum": 26, "current": 16, "spent": 10}
    assert gate_caster["derived"]["spellAttackBonus"] == 10 and gate_caster["derived"]["spellSaveDC"] == 18
    assert owner["derived"]["spellAttackBonus"] == 8 and owner["derived"]["spellSaveDC"] == 16
    assert owner["factionEligibility"]["currentStanding"] == 3
    assert owner["factionEligibility"]["alliedStatus"] and owner["factionEligibility"]["invocationPermission"]
    assert not owner["factionEligibility"]["aidProhibition"]
    assert gate_caster["magicState"]["dissonance"] == 0 and owner["magicState"]["dissonance"] == 0
    assert gate_caster["magicState"]["refrain"] == {"lastSpellId": "banishment-gate", "consecutiveRepeatCount": 0}
    assert owner["magicState"]["refrain"] == {"lastSpellId": "faction-champion", "consecutiveRepeatCount": 0}
    assert gate_caster["concentration"]["deadlineSeconds"] == 595
    assert owner["concentration"]["active"] is False and owner["concentration"]["endedAtSeconds"] == 60
    assert champion["exists"] is False and champion["corpseExists"] is False
    assert champion["intrinsicManifestation"]["status"] == "vanished"
    assert champion["movement"]["spentFt"] == 20 and champion["movement"]["expiredUnusedFt"] == 10

    events_by_id = {event["eventId"]: event for event in common["events"]}
    assert events_by_id["W08-E07-GATE-CAST-RESOLVE"]["stateAfter"]["actors"]["gateCaster"]["magicState"]["dissonance"] == 2
    assert events_by_id["W08-E10-GATECASTER-END-T00"]["stateAfter"]["actors"]["gateCaster"]["magicState"]["dissonance"] == 1
    assert events_by_id["W08-E14-CHAMPION-CAST-RESOLVE"]["stateAfter"]["actors"]["championOwner"]["magicState"]["dissonance"] == 1
    gate_commit = events_by_id["W08-E05-GATE-CAST-COMMIT"]["stateAfter"]["actors"]["gateCaster"]["spellcasting"]["pendingCast"]
    champion_commit = events_by_id["W08-E12-CHAMPION-CAST-COMMIT"]["stateAfter"]["actors"]["championOwner"]["spellcasting"]["pendingCast"]
    for commit, expected_spell, rp_before, cost, dissonance in [
        (gate_commit, "banishment-gate", 50, 26, 2),
        (champion_commit, "faction-champion", 26, 10, 1),
    ]:
        assert commit["spellId"] == expected_spell and commit["actionConsumed"] is True
        assert commit["rangeValid"] and commit["perceived"] and commit["lineOfEffectClear"]
        assert all(commit["components"][key]["available"] for key in ("V", "S", "F"))
        assert commit["components"]["F"]["heldByCaster"] is True
        assert commit["rp"] == {"before": rp_before, "cost": cost, "after": rp_before - cost}
        assert commit["dissonance"]["baseIncrease"] == dissonance

    for event_id, caster_key, other_key in [
        ("W08-E06-GATE-COUNTERSPELL-WINDOW", "gateCaster", "championOwner"),
        ("W08-E13-CHAMPION-COUNTERSPELL-WINDOW", "championOwner", "gateCaster"),
    ]:
        receipt = events_by_id[event_id]["stateAfter"]["eventReceipts"][event_id]
        decisions = {d["actorKey"]: d for d in receipt["participantDecisions"]}
        assert set(decisions) == {"gateCaster", "championOwner"}
        assert decisions[caster_key]["eligible"] is False
        assert decisions[caster_key]["decision"] == "not-eligible-self"
        other = decisions[other_key]
        assert other["eligible"] is True and other["decision"] == "declines"
        assert other["cardSelected"] and other["reactionAvailable"] and other["withinRange"]
        assert other["rpSufficient"] and other["rechargeReady"] and other["perceivesCaster"]
        assert other["counterspellAttempted"] is False and other["rpSpent"] == 0

    start_times = {-6, *range(0, 67, 6)}
    expected_markers = {
        (actor, time, "START")
        for actor in ("actor-gate-caster-w08", "actor-champion-owner-w08")
        for time in start_times
    }
    expected_markers.update({("actor-gate-caster-w08", time, "END") for time in {-4, *range(0, 67, 6)}})
    expected_markers.update({("actor-champion-owner-w08", time, "END") for time in {-6, *range(0, 67, 6)}})
    marker_events = []
    for event in common["events"]:
        if event.get("regularTurnMarker"):
            marker_events.append(event)
    for branch in case["terminalForks"]:
        for event in branch["events"]:
            if event.get("regularTurnMarker"):
                marker_events.append(event)
    actual_markers = {(e["regularTurnMarker"]["actorId"], e["timestampSeconds"], e["regularTurnMarker"]["marker"])
                      for e in marker_events}
    assert expected_markers <= actual_markers
    expiry = events_by_id["W08-E28-CHAMPION-SOURCE-EXPIRY"]
    assert expiry["sequenceAtTimestamp"] == 1
    assert all(e["sequenceAtTimestamp"] > 1 for e in common["events"] if e.get("regularTurnMarker") and e["timestampSeconds"] == 60)

    crossing = events_by_id["W08-E26-GATE-CROSSING"]["stateAfter"]["eventReceipts"]["W08-E26-GATE-CROSSING"]
    assert crossing["actualAdmissionPoseFt"] == [105, 100, 0]
    assert crossing["fixedOriginAnchorFt"] == [105, 100, 0]
    assert crossing["worldPathStartFt"] == [85, 100, 0] and crossing["worldPathEndFt"] == [105, 100, 0]
    assert crossing["completeBodyStartXBoundsFt"][1] < crossing["gatePlaneXFt"]
    assert crossing["completeBodyEndXBoundsFt"][0] > crossing["gatePlaneXFt"]
    assert crossing["portalWidthClearance"] and crossing["portalHeightClearance"]
    assert crossing["bodyFullyCrossedAtEndpoint"] and crossing["cargoFullyCrossedAtEndpoint"]
    assert crossing["cellBoundsFt"] == {"min": [-7.5, -7.5, 0], "max": [7.5, 7.5, 15]}
    assert crossing["cargoCellLocal"]["centerFt"] == [2, 0, 3]
    assert crossing["ownerWholeTurnEndedBeforePhase"] is True
    assert events_by_id["W08-E22-COMPANION-COMMAND"]["stateAfter"]["eventReceipts"]["W08-E22-COMPANION-COMMAND"]["globalAllowanceUsedOnce"]
    assert events_by_id["W08-E24-ATTACHED-PHASE-START"]["stateAfter"]["eventReceipts"]["W08-E24-ATTACHED-PHASE-START"]["ownerTurnEndedFirst"]
    expiry_receipt = expiry["stateAfter"]["eventReceipts"]["W08-E28-CHAMPION-SOURCE-EXPIRY"]
    assert expiry_receipt["sameGenuineLanternPersists"] and expiry_receipt["cellRemainsActiveUntil"] == 66

    assert len(case["terminalForks"]) == 3
    outcomes = {
        "W08-DIRECT-ANCHOR-PLACEMENT": "placed-at-origin-anchor",
        "W08-OCCUPIED-ANCHOR-ADJACENT-DROP": "placed-at-nearest-legal-adjacent-position",
        "W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM": "pending-origin-plane-item-placement",
    }
    fork_reports = []
    for branch in case["terminalForks"]:
        final = replay(end_common, branch["events"])
        assert final == branch["finalState"] and state_hash(final) == branch["terminalStateSha256"]
        assert reverse_replay(final, branch["events"]) == end_common
        geometry = next(e["stateAfter"]["world"]["terminalGeometryFixture"]
                        for e in branch["events"] if e["kind"] == "terminal-placement-geometry")
        assert geometry["itemPlacementModel"]["allGeometryIsTEST_ONLY"]
        assert geometry["floorSupport"]["continuousSupport"]
        item = final["objects"]["object-genuine-hooded-lantern-w08-001"]
        assert item["status"] == outcomes[branch["branchId"]]
        assert item["ownerId"] == "actor-champion-owner-w08" and item["quantity"] == 1
        assert final["cell"]["status"] == "closed" and final["cell"]["destroyed"]
        assert final["cell"]["closureCount"] == 1 and final["cell"]["closedAtSeconds"] == 66
        assert final["gate"]["active"] and final["gate"]["liveCellIds"] == []
        assert final["gate"]["concentrationDeadlineSeconds"] == 595
        close = next(e for e in branch["events"] if e["kind"] == "gate-cell-terminal-closure")
        assert close["sequenceAtTimestamp"] == 2
        assert branch["events"][-1]["kind"] == "duplicate-terminal-callback"
        assert branch["events"][-1]["forwardOperations"] == []
        assert branch["events"][-1]["afterStateSha256"] == branch["events"][-1]["beforeStateSha256"]
        decision = geometry["derivedDecision"]
        if branch["branchId"] == "W08-OCCUPIED-ANCHOR-ADJACENT-DROP":
            assert decision["nearestLegalCandidateFt"] == [107.5, 100, 0.25]
            assert decision["unique"] and decision["placementPathCrossesWall"] is False
            assert decision["wouldDisplaceBlocker"] is False
            assert item["physicalPosition"]["worldFt"] == [107.5, 100, 0.25]
        elif branch["branchId"] == "W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM":
            assert decision["adjacentDomainFullyOccupied"] and decision["adjacentLegalCandidateCount"] == 0
            assert decision["displacedBlockerIds"] == [] and decision["placementPathCrossesWall"] is False
            assert item["physicalPosition"]["placementPending"] is True
            assert item["physicalPosition"]["creaturePlacementConflict"] is False
        else:
            assert decision["nearestLegalCandidateFt"] == [107, 100, 0.25]
            assert item["physicalPosition"]["worldFt"] == [107, 100, 0.25]
        fork_reports.append({"branchId": branch["branchId"], "outcome": item["status"],
                             "terminalStateSha256": state_hash(final), "reverseReplay": "PASS"})

    assert case["wholeIdentityGate"] == "HOLD" and case["applicationAuthorized"] is False
    assert case["acceptanceDecision"].startswith("not accepted")
    assert case["scenarioBoundary"]["noCampaignEvent"]
    assert case["scenarioBoundary"]["allActorFactionAndWorldFactsAreConditionalTestPremises"]
    return {"commonPrefixEvents": len(common["events"]), "forks": fork_reports,
            "regularTurnMarkersVerified": len(actual_markers), "sourceExpiryAndCellClosureOrder": "PASS",
            "casterAndCounterspellPredicates": "PASS", "cargoAdmissionAndContinuousPlacement": "PASS",
            "replayAndInverseReplay": "PASS", "identityDecision": "HOLD", "applicationAuthorized": False}


def archive_audit(packet: Path, archive: Path, delivery_path: Path) -> dict[str, Any]:
    delivery = load(delivery_path)
    data = archive.read_bytes()
    assert len(data) == delivery["archive"]["bytes"] and sha(data) == delivery["archive"]["sha256"]
    assert delivery["manifest"]["path"] == "ARCHIVE_MANIFEST.json"
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        assert len(names) == len(set(names)) and "ARCHIVE_MANIFEST.json" in names
        manifest_data = zf.read("ARCHIVE_MANIFEST.json")
        assert len(manifest_data) == delivery["manifest"]["bytes"]
        assert sha(manifest_data) == delivery["manifest"]["sha256"]
        manifest = json.loads(manifest_data)
        assert manifest["memberCount"] == len(names) - 1
        seen: set[str] = set()
        for record in manifest["members"]:
            member = record["path"]
            assert member not in seen and member in names
            payload = zf.read(member)
            assert len(payload) == record["bytes"] and sha(payload) == record["sha256"]
            import zlib
            assert f"{zlib.crc32(payload) & 0xffffffff:08x}" == record["crc32"]
            seen.add(member)
        assert seen == set(names) - {"ARCHIVE_MANIFEST.json"}
    return {"archiveBytes": len(data), "archiveSha256": sha(data), "members": len(names),
            "manifestPath": delivery["manifest"]["path"], "allMemberHashesAndCrcs": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_OUT / "packet")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--write-audit", type=Path)
    args = parser.parse_args()
    packet = args.packet_dir.resolve()
    report: dict[str, Any] = {
        "id": "PG327-W08-INDEPENDENT-AUDIT-365-REPACK02",
        "verifiedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_TEST_ONLY_STATIC_WITNESS; FRESH_DIRECTOR_DECISION_PENDING",
        "scope": "W08 only; no identity acceptance or application",
        "sourceAudit": source_audit(packet),
        "semanticAudit": semantic_audit(packet),
        "archiveAudit": None,
        "decisionBoundary": {"banishmentGate": "HOLD", "applicationAuthorized": False,
                             "acceptedIds": [], "appliedIds": [],
                             "queueAuthority": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                                                "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                                                "firstReviews": 0, "closureTasks": 20}},
    }
    if args.archive:
        delivery = args.delivery or args.archive.with_name("ARCHIVE_DELIVERY_365_W08_REPACK02.json")
        report["archiveAudit"] = archive_audit(packet, args.archive.resolve(), delivery.resolve())
        report["status"] = "PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; FRESH_DIRECTOR_DECISION_PENDING"
    if args.write_audit:
        args.write_audit.parent.mkdir(parents=True, exist_ok=True)
        args.write_audit.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
