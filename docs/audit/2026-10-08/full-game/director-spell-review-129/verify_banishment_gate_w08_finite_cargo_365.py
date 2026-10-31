from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "banishment_gate_witness365_w08_finite_cargo01"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_hash(value: Any) -> str:
    return sha(canonical(value))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def get_at(root: Any, path: list[str]) -> Any:
    current = root
    for part in path:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def set_at(root: Any, path: list[str], value: Any, remove: bool = False) -> None:
    if not path:
        raise AssertionError("unexpected root patch")
    current = root
    for part in path[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    key = path[-1]
    if isinstance(current, list):
        idx = int(key)
        if remove:
            current.pop(idx)
        elif idx == len(current):
            current.append(value)
        else:
            current[idx] = value
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
            raise AssertionError(f"unknown operation {op['op']}")
    return result


def replay_events(start: Any, events: list[dict[str, Any]]) -> tuple[Any, list[dict[str, Any]]]:
    state = copy.deepcopy(start)
    inverses = []
    for event in events:
        assert state_hash(state) == event["beforeStateSha256"], event["eventId"]
        state = apply_ops(state, event["forwardOperations"])
        assert state == event["stateAfter"], event["eventId"]
        assert state_hash(state) == event["afterStateSha256"], event["eventId"]
        inverses.append({"eventId": event["eventId"], "inverseCount": len(event["inverseOperations"])})
    return state, inverses


def verify_source_files(packet: Path) -> dict[str, Any]:
    source_bindings = load_json(packet / "W08_SOURCE_BINDINGS_365.json")
    checked = []
    for binding in source_bindings["bindings"]:
        member = binding.get("packetMember") or binding.get("member")
        if not member:
            continue
        path = packet / Path(member)
        data = path.read_bytes()
        assert len(data) == binding["bytes"], member
        assert sha(data) == binding["sha256"], member
        checked.append({"member": member, "bytes": len(data), "sha256": sha(data)})

    gate = load_json(packet / "sources" / "RETURN327_banishment-gate.json")
    procedure = gate["procedure"]
    for token in ("PG9-Q17", "PG9-Q15", "PG9-Q29", "PG200-CELL-EXT"):
        assert token in procedure
    assert gate["sharedContract"]["terminalScope"].find("PG200-CELL-EXT") >= 0
    closure = gate["sharedContract"]["cellExtension"]["closure"]
    for key in ("originPlane", "looseObjectAnchors", "mandatoryPlaneReturn", "endpointBlockerException", "objects", "deathAndRemoval", "cellEnd"):
        assert key in closure

    body = (packet / "rules" / "BODY_EQUIPMENT.md").read_text(encoding="utf-8")
    lines = body.splitlines()
    assert "Drop an item that cannot be carried or equipped at the current position or the nearest legal adjacent item position." in lines[49]
    assert "If no legal drop position exists, record that item's placement as pending." in lines[50]
    assert "Medium | Strength score × 15 | Strength score × 30 | Strength score" in body
    assert "one legal attach, lift, transfer or protective operation" in body

    extract = load_json(packet / "sources" / "AC5_PROFILE_AND_CARGO_SOURCE_EXTRACT.json")
    receipt = load_json(packet / "authority" / "AC5_EXACT_ACCEPTANCE_05_RECEIPT.json")
    model = load_json(packet / "sources" / "AC5_ACCEPTED_SPELLS_MODEL.json")
    casebook = load_json(packet / "sources" / "AC5_ACCEPTED_CASEBOOK.json")
    assert "faction-champion" in receipt["acceptedSpellIds"]
    assert receipt["runtimeSelectionEnabled"] is False
    profile = model["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    assert profile == extract["profile"]
    assert model["sharedRules"]["AC5-CHAMPION-ALLY-01"] == extract["sharedRule"]
    spell = next(x for x in model["spells"] if x["id"] == "faction-champion")
    assert spell == extract["spellAccessAndRoute"]
    source_case = next(x for x in casebook["cases"] if x["id"] == "CJ5-07-B")
    assert source_case == extract["cargoExample"]
    assert "genuinely borrowed lantern drops intact" in source_case["historicalOriginalText"]
    assert "one live Champion" in source_case["currentInitialState"]
    assert "At source expiry body ends" in source_case["actionsAndResolution"][-1]
    assert any("not used as Gate rules" in note for note in extract["scopeLimits"])

    equip_catalog = load_json(packet / "sources" / "EQUIPMENT_SOURCE_CATALOG.json")
    lantern = next(x for x in equip_catalog["records"] if x["id"] == "adventuring-gear.lantern-hooded")
    assert lantern["sourcePriceCp"] == 500 and lantern["sourceWeightLb"] == 2.0
    item_text = load_json(packet / "sources" / "HOODED_LANTERN_SOURCE_EXTRACT.json")
    assert item_text["equipmentProjection"]["record"] == lantern
    assert "Lantern, hooded" in item_text["source"]["exactLine"]
    assert item_text["source"]["lineNumber"] == 6976

    clarification = load_json(packet / "authority" / "PG327_W08_TERMINAL_SETTLEMENT_SOURCE_CLARIFICATION_365.json")
    assert clarification["status"].startswith("DIRECTOR_GUIDANCE")
    assert clarification["gateSourceBinding"]["terminalSettlementPointer"] == "/sharedContract/cellExtension/closure"
    assert clarification["requiredForkOutcomes"]["anchorAndAdjacentUnavailable"].find("pending placement") >= 0

    w01 = load_json(packet / "authority" / "PG327_W01_DIRECTOR_SEAL_365_REPACK04.json")
    queue = load_json(packet / "authority" / "CURRENT_SPELL_QUEUE_361.json")
    assert w01["witnessDecision"] == "SEALED_TEST_ONLY" and w01["identityDecision"] == "HOLD"
    assert w01["applicationAuthorized"] is False
    q = queue["currentAuthority"]
    assert q["reviewedApplied"] == 828 and q["pending"] == 20 and q["acceptedUnapplied"] == 0
    return {"checkedBindings": checked, "gateRulePointersPass": True, "bodyEquipmentRulesPass": True,
            "acceptedAc5ProfileAndCasePass": True, "equipmentSourcePass": True, "authorityUnchangedPass": True}


def verify_case(packet: Path) -> dict[str, Any]:
    case = load_json(packet / "W08_FINITE_SUMMON_CARGO_CASE_365_TESTONLY.json")
    common = case["commonPrefix"]
    initial = common["initialState"]
    assert state_hash(initial) == common["initialStateSha256"]
    assert initial["testFixtureBoundaries"]["AC5BanishElementalExtensionImported"] is False
    assert initial["testFixtureBoundaries"]["AC5X17MechanicsImported"] is False
    end_common, _ = replay_events(initial, common["events"])
    assert end_common == common["finalState"]
    assert state_hash(end_common) == common["finalStateSha256"]
    assert end_common["gate"]["selectedCreatureType"] == "Humanoid"
    assert end_common["gate"]["active"] is True
    assert end_common["gate"]["concentrationDeadlineSeconds"] == 595
    assert end_common["gate"]["spellRpSpent"] == 26
    assert end_common["actors"]["gateCaster"]["rp"] == {"initial": 60, "current": 34, "spent": 26}

    owner = end_common["actors"]["championOwner"]
    champ = end_common["actors"]["champion"]
    assert owner["class"] == "Mage" and owner["classLevel"] == 9
    assert owner["spellAccess"]["minimumClassLevel"] == 9 and owner["spellAccess"]["baseRp"] == 10
    assert owner["factionEligibility"]["alliedStatus"] is True
    assert owner["factionEligibility"]["currentStanding"] > 0
    assert owner["factionEligibility"]["invocationPermission"] is True
    assert owner["factionEligibility"]["aidProhibition"] is False
    assert owner["rp"] == {"initial": 40, "current": 30, "spent": 10}
    assert champ["sourceSpellId"] == "faction-champion" and champ["creatureType"] == "Humanoid"
    assert champ["sourceDeadlineSeconds"] == 60
    assert champ["exists"] is False and champ["corpseExists"] is False
    assert champ["intrinsicManifestation"]["status"] == "vanished"
    assert champ["movement"]["spentFt"] == 20 and champ["movement"]["remainingFt"] == 10
    item_id = "object-genuine-hooded-lantern-w08-001"
    item = end_common["objects"][item_id]
    assert item["ownerId"] == owner["id"] and item["custodianId"] is None
    assert item["quantity"] == 1 and item["genuine"] is True and item["magical"] is False
    assert item["status"] == "loose-genuine-cargo-in-cell"
    assert end_common["cell"]["status"] == "active" and end_common["cell"]["deadlineSeconds"] == 66
    assert end_common["cell"]["looseCargoIds"] == [item_id]
    assert end_common["cell"]["contents"] == [item_id]
    assert end_common["elapsedSeconds"] == 60
    assert case["timeModel"]["sourceExpiryBeforeCellDeadline"] is True
    assert case["timeModel"]["sourceExpiryDoesNotCloseGateCell"] is True
    assert end_common["gate"]["liveCellIds"] == ["cell-w08-001"]

    crossing = common["events"][-2]
    crossing_result = crossing["stateAfter"]["eventReceipts"]["W08-E05-GATE-CROSSING"]
    assert crossing_result["movementFt"] == 20 and crossing_result["admitted"] is True
    assert crossing_result["worldPathStartFt"] == [85, 100, 0]
    assert crossing_result["worldPathEndFt"] == [105, 100, 0]
    assert crossing_result["completeBodyStartXBoundsFt"][1] < crossing_result["gatePlaneXFt"]
    assert crossing_result["completeBodyEndXBoundsFt"][0] > crossing_result["gatePlaneXFt"]
    assert crossing_result["portalWidthClearance"] == "5-ft body <= 10-ft aperture"
    assert crossing_result["portalHeightClearance"] == "6-ft fixture body <= 15-ft aperture"

    expected_branches = {
        "W08-DIRECT-ANCHOR-PLACEMENT": "placed-at-origin-anchor",
        "W08-OCCUPIED-ANCHOR-ADJACENT-DROP": "placed-at-nearest-legal-adjacent-position",
        "W08-OCCUPIED-AND-BLOCKED-PENDING-ITEM": "pending-origin-plane-item-placement",
    }
    assert len(case["terminalForks"]) == 3
    branch_audits = []
    for branch in case["terminalForks"]:
        assert branch["startStateSha256"] == common["finalStateSha256"]
        final, _ = replay_events(end_common, branch["events"])
        assert final == branch["finalState"]
        assert state_hash(final) == branch["terminalStateSha256"]
        assert branch["restoresCommonPrefix"] is True
        reverse = copy.deepcopy(final)
        for event in reversed(branch["events"]):
            reverse = apply_ops(reverse, event["inverseOperations"])
            assert state_hash(reverse) == event["beforeStateSha256"]
        assert reverse == end_common
        full_reverse = copy.deepcopy(reverse)
        for event in reversed(common["events"]):
            full_reverse = apply_ops(full_reverse, event["inverseOperations"])
            assert state_hash(full_reverse) == event["beforeStateSha256"]
        assert full_reverse == initial

        item_final = final["objects"][item_id]
        assert item_final["status"] == expected_branches[branch["branchId"]]
        assert item_final["quantity"] == 1 and item_final["ownerId"] == owner["id"]
        assert item_final["custodianId"] is None
        assert final["cell"]["status"] == "closed" and final["cell"]["destroyed"] is True
        assert final["cell"]["closureCount"] == 1 and final["cell"]["closedAtSeconds"] == 66
        assert final["gate"]["active"] is True and final["gate"]["liveCellIds"] == []
        assert final["gate"]["concentrationDeadlineSeconds"] == 595
        assert final["actors"]["champion"]["exists"] is False
        assert final["actors"]["champion"]["corpseExists"] is False
        assert final["actors"]["championOwner"]["rp"]["spent"] == 10
        assert final["actors"]["gateCaster"]["rp"]["spent"] == 26
        close = next(e for e in branch["events"] if e["kind"] == "gate-cell-terminal-closure")
        assert close["stateAfter"]["eventReceipts"][f"{branch['branchId']}-CLOSE"]["refundRp"] == 0
        duplicate = branch["events"][-1]
        assert duplicate["kind"] == "duplicate-terminal-callback"
        assert duplicate["forwardOperations"] == [] and duplicate["inverseOperations"] == []
        assert duplicate["afterStateSha256"] == duplicate["beforeStateSha256"]
        assert duplicate["returnedReceiptId"] == close["stateAfter"]["cell"]["closureReceiptId"]
        if branch["branchId"] == "W08-DIRECT-ANCHOR-PLACEMENT":
            assert item_final["physicalPosition"]["worldFt"] == [100, 100, 0]
            assert item_final["physicalPosition"]["placementPending"] is False
        elif branch["branchId"] == "W08-OCCUPIED-ANCHOR-ADJACENT-DROP":
            assert item_final["physicalPosition"]["worldFt"] == [105, 100, 0]
            assert item_final["physicalPosition"]["displacedOccupant"] is False
        else:
            assert item_final["physicalPosition"]["planeKey"] == "PLANE-W08-TEST-ORIGIN-01"
            assert item_final["physicalPosition"]["pendingAnchorWorldFt"] == [100, 100, 0]
            assert item_final["physicalPosition"]["placementPending"] is True
            assert item_final["physicalPosition"]["creaturePlacementConflict"] is False
        branch_audits.append({"branchId": branch["branchId"], "terminalSha256": state_hash(final),
                              "outcome": item_final["status"], "closureCount": final["cell"]["closureCount"],
                              "restoresExactFork": True})

    assert case["applicationAuthorized"] is False
    assert case["wholeIdentityGate"] == "HOLD"
    assert case["scenarioBoundary"]["noCampaignEvent"] is True
    assert case["scenarioBoundary"]["allActorFactionAndWorldFactsAreConditionalTestPremises"] is True
    assert case["scenarioBoundary"]["nativeRuntimeSelectionEnabled"] is False
    assert case["scenarioBoundary"]["spellImplementationOrRuntimeTestClaimed"] is False
    assert case["scenarioBoundary"]["identityAcceptanceOrApplicationClaimed"] is False
    assert case["scenarioBoundary"]["noAC5BanishElementalMechanicImported"] is True
    assert case["scenarioBoundary"]["noAC5X17MechanicImported"] is True
    assert "AC5-BANISH-EXT-01" not in [ref for b in case["terminalForks"] for e in b["events"] for ref in e["sourcePointers"]]
    assert "AC5-X17" not in [ref for e in common["events"] for ref in e["sourcePointers"]]
    return {"commonPrefixEventCount": len(common["events"]), "forkCount": len(case["terminalForks"]),
            "branchAudits": branch_audits, "forwardInverseReplayPass": True,
            "bodyExpiryBeforeCellDeadlinePass": True, "cargoIdentityAndExactlyOncePass": True,
            "gateAndQueueHoldPreserved": True}


def verify_archive(packet: Path, archive: Path, delivery_path: Path) -> dict[str, Any]:
    delivery = load_json(delivery_path)
    archive_bytes = archive.read_bytes()
    assert len(archive_bytes) == delivery["archive"]["bytes"]
    assert sha(archive_bytes) == delivery["archive"]["sha256"]
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        assert len(names) == len(set(names))
        assert "ARCHIVE_MANIFEST.json" in names
        manifest = json.loads(zf.read("ARCHIVE_MANIFEST.json").decode("utf-8"))
        assert manifest["memberCount"] == len(names) - 1
        assert delivery["archive"]["archiveMembers"] == len(names)
        seen = set()
        for record in manifest["members"]:
            member = record["path"]
            assert member not in seen and member in names
            seen.add(member)
            data = zf.read(member)
            assert len(data) == record["bytes"]
            assert sha(data) == record["sha256"]
            assert (zlib_crc32(data)) == record["crc32"]
        assert seen == set(names) - {"ARCHIVE_MANIFEST.json"}
    return {"archiveBytes": len(archive_bytes), "archiveSha256": sha(archive_bytes),
            "archiveMembers": len(names), "payloadMembers": len(names) - 1, "memberHashesAndCrcsPass": True}


def zlib_crc32(data: bytes) -> str:
    import zlib
    return f"{zlib.crc32(data) & 0xffffffff:08x}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_OUT / "packet")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--write-audit", type=Path)
    args = parser.parse_args()

    packet = args.packet_dir.resolve()
    source_audit = verify_source_files(packet)
    semantic_audit = verify_case(packet)
    audit = {
        "id": "PG327-W08-INDEPENDENT-AUDIT-365-01",
        "verifiedAtUtc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_TEST_ONLY_STATIC_WITNESS; DIRECTOR_DECISION_PENDING",
        "scope": "W08 only; no identity acceptance/application or whole Gate completion",
        "sourceAudit": source_audit,
        "semanticAudit": semantic_audit,
        "archiveAudit": None,
        "decisionBoundary": {"banishmentGate": "HOLD", "applicationAuthorized": False,
                             "queueAuthority": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                                                "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                                                "firstReviews": 0, "closureTasks": 20}},
    }
    if args.archive:
        delivery_path = args.delivery or args.archive.with_name("ARCHIVE_DELIVERY_365_W08.json")
        audit["archiveAudit"] = verify_archive(packet, args.archive.resolve(), delivery_path.resolve())
        audit["status"] = "PASS_TEST_ONLY_STATIC_WITNESS_AND_ARCHIVE; DIRECTOR_DECISION_PENDING"
    if args.write_audit:
        args.write_audit.parent.mkdir(parents=True, exist_ok=True)
        args.write_audit.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
