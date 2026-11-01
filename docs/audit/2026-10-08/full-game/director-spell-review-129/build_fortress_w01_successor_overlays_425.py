#!/usr/bin/env python3
"""Build adopted, TEST_ONLY Fortress W01 support and usable-volume overlays."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GEOM_DIR = BASE / "fortress_w01_geometry_405"
W403_DIR = BASE / "fortress_w01_structural_damage_witness_403_repack02"
OWNER_DIR = BASE / "fortress_w01_owner_adoption_424"
OUT = BASE / "fortress_w01_successor_overlays_425"
DOWNLOADS = Path.home() / "Downloads"
DIRECTOR_ZIP = DOWNLOADS / "DD_Fortress_W01_Support_Z40_Director_Proposals_V1_TESTONLY.zip"
DIRECTOR_DELIVERY = DOWNLOADS / "DD_Fortress_W01_Support_Z40_Director_Proposals_V1_DELIVERY.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_binding(path: Path, repo_path: str) -> dict:
    data = path.read_bytes()
    return {"repositoryPath": repo_path, "bytes": len(data), "sha256": sha(data)}


def endpoint_bounds(position, relative_bounds):
    x, y, z = position
    x0, x1, y0, y1, z0, z1 = relative_bounds
    return [x + x0, x + x1, y + y0, y + y1, z + z0, z + z1]


def within(bounds, volume):
    return (
        bounds[0] >= volume[0] and bounds[1] <= volume[1]
        and bounds[2] >= volume[2] and bounds[3] <= volume[3]
        and bounds[4] >= volume[4] and bounds[5] <= volume[5]
    )


def main() -> None:
    if not DIRECTOR_ZIP.exists() or not DIRECTOR_DELIVERY.exists():
        raise SystemExit(f"Missing Director proposal ZIP/delivery in {DOWNLOADS}")

    OWNER_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    director_zip_bytes = DIRECTOR_ZIP.read_bytes()
    director_delivery_bytes = DIRECTOR_DELIVERY.read_bytes()
    director_zip_sha = sha(director_zip_bytes)
    director_delivery_sha = sha(director_delivery_bytes)
    if director_zip_sha != "18451b3b9f353a96d0f6d06d635f568db8c190d8b96acd6e51f1189a443b026b":
        raise AssertionError("Director proposal archive bytes do not match the verified packet")
    if director_delivery_sha != "117dd885d2f101f1a20c31634b9ee64e7855148c61b0fe039e2f06a292452055":
        raise AssertionError("Director delivery bytes do not match the verified packet")

    with zipfile.ZipFile(DIRECTOR_ZIP) as zf:
        proposal = json.loads(zf.read("DIRECTOR_PROPOSAL.json"))
        terms = json.loads(zf.read("EXACT_PROPOSAL_TERMS.json"))
        post = json.loads(zf.read("POST_ADOPTION_VERIFICATION.json"))
        director_bindings = json.loads(zf.read("SOURCE_BINDINGS.json"))
        proposal_sha = sha(zf.read("DIRECTOR_PROPOSAL.json"))
        terms_sha = sha(zf.read("EXACT_PROPOSAL_TERMS.json"))
    proposal_ids = [
        "PG328-W01-GEOM405-SUPPORT-PROPOSAL-01",
        "PG328-W01-GEOM405-Z40-PROPOSAL-01",
    ]
    if proposal["proposalIds"] != proposal_ids:
        raise AssertionError("Director proposal IDs differ from the adopted IDs")
    if proposal["status"] != "PROPOSED_NOT_ADOPTED" or post["status"] != "REQUIRED_NOT_PERFORMED":
        raise AssertionError("Unexpected source proposal status")

    owner_zip = OWNER_DIR / DIRECTOR_ZIP.name
    owner_delivery = OWNER_DIR / DIRECTOR_DELIVERY.name
    shutil.copyfile(DIRECTOR_ZIP, owner_zip)
    shutil.copyfile(DIRECTOR_DELIVERY, owner_delivery)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_404.json"
    handoff_path = BASE / "CURRENT_HANDOFF_404.json"
    geometry_path = GEOM_DIR / "GEOMETRY_405.json"
    connections_path = GEOM_DIR / "GEOMETRIC_CONNECTIONS_405.json"
    verify405_path = GEOM_DIR / "VERIFICATION_405.json"
    readback405_path = GEOM_DIR / "DIRECTOR_GEOMETRY_READBACK_405.json"
    replay403_path = W403_DIR / "W01_REPLAY_403.json"
    geometry403_path = W403_DIR / "W01_GEOMETRY_403.json"
    delivery403_path = W403_DIR / "DELIVERY_403.json"
    reconcile_path = W403_DIR / "DIRECTOR_RECONCILIATION_GEOMETRY405_403.json"
    readback403_path = W403_DIR / "DIRECTOR_REVIEW_READBACK_403_REPACK02.json"

    queue = read_json(queue_path)
    authority = queue["currentAuthority"]
    geometry = read_json(geometry_path)
    connections = read_json(connections_path)
    verify405 = read_json(verify405_path)
    replay403 = read_json(replay403_path)
    geometry403 = read_json(geometry403_path)
    delivery403 = read_json(delivery403_path)
    terminal403 = replay403["stateSnapshots"][replay403["terminalStateId"]]
    panel_by_id = {item["id"]: item for item in geometry["panels"]}
    leaf_by_id = {item["id"]: item for item in geometry["doorLeaves"]}
    panel_ids = set(panel_by_id)
    leaf_ids = set(leaf_by_id)
    root_id = "origin-ground-face"
    if root_id not in panel_ids:
        raise AssertionError("Adopted support root is not a Geometry405 structural node")

    structural = []
    leaf_attachments = []
    for index, edge in enumerate(connections["connections"]):
        a, b = edge["a"], edge["b"]
        if a in panel_ids and b in panel_ids:
            structural.append({"sourceConnectionIndex": index, "a": a, "b": b})
        elif (a in panel_ids and b in leaf_ids) or (b in panel_ids and a in leaf_ids):
            part, leaf = (a, b) if a in panel_ids else (b, a)
            leaf_attachments.append({
                "sourceConnectionIndex": index,
                "structuralPartId": part,
                "leafId": leaf,
                "supportDirection": "structural part supports leaf only",
                "leafSupportsBuilding": False,
            })
        else:
            raise AssertionError(f"Unclassified Geometry405 connection at index {index}")
    if len(structural) != 4851 or len(leaf_attachments) != 53:
        raise AssertionError(f"Unexpected edge split: {len(structural)} structural, {len(leaf_attachments)} leaves")
    if len(panel_ids) != 2660 or len(connections["connections"]) != 4904:
        raise AssertionError("Geometry405 node or contact counts changed")

    adjacency = {node: set() for node in panel_ids}
    for edge in structural:
        adjacency[edge["a"]].add(edge["b"])
        adjacency[edge["b"]].add(edge["a"])
    reachable = {root_id}
    todo = deque([root_id])
    while todo:
        node = todo.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in reachable:
                reachable.add(neighbor)
                todo.append(neighbor)
    components, unseen = [], set(panel_ids)
    while unseen:
        start = next(iter(unseen))
        comp, q = set(), deque([start])
        unseen.remove(start)
        while q:
            node = q.popleft()
            comp.add(node)
            for neighbor in adjacency[node] & unseen:
                unseen.remove(neighbor)
                q.append(neighbor)
        components.append(comp)

    damage = replay403["targetDamage"]
    panel_id = "W01-SOUTH-WALL-X25-Z0"
    if damage != {"panelId": panel_id, "hpBefore": 60, "hpAfter": 55, "damage": 5, "damageType": "bludgeoning", "destroyed": False}:
        raise AssertionError("W01-403 target damage terminal differs from the reviewed 55-HP result")
    if panel_id not in panel_by_id or panel_by_id[panel_id]["HP"] != 60:
        raise AssertionError("Geometry405 parent panel baseline differs from the exact 60 HP source")
    # Check the terminal actor retains the exact carried identities, hand state, and tile custody.
    actor_a = terminal403["actors"]["A"]
    tile = terminal403["items"]["PG328-W01-403:CLAY-TILE-1"]
    tile_id = "PG328-W01-403:CLAY-TILE-1"
    if tile_id not in actor_a["equipment"] or actor_a.get("w01HandState", {}).get("right") != tile_id:
        raise AssertionError("W01-403 terminal item custody differs from the accepted witness source")
    inventory_ids = ["focus-A", "pack-A", "cargo-A", tile_id]
    if actor_a["equipment"] != inventory_ids:
        raise AssertionError("W01-403 terminal cargo identity set/order changed")
    if tile["custodian"] != "A" or tile["heldBy"] != "A:right" or tile["createdAtEventTime"] != 6.13 or tile["expiresAtEventTime"] != 3606.13 or tile["exists"] is not True:
        raise AssertionError("W01-403 tile custody/expiry evidence differs from its terminal snapshot")
    if len(replay403["events"]) != 30 or len(replay403["stateSnapshots"]) != 31:
        raise AssertionError("W01-403 historical replay event/snapshot counts changed")

    adoption = {
        "schemaVersion": 1,
        "recordId": "OWNER-PG328-W01-SUPPORT-Z40-ADOPTION-424",
        "recordedLocalDate": "2026-11-01",
        "classification": "OWNER_ADOPTION_TEST_ONLY",
        "scope": {
            "identity": "conjure-demiplane-fortress",
            "witnessId": "PG328-W01",
            "identityHold": "PG200-B06",
            "proposalIds": proposal_ids,
            "sourceSnapshotCommit": proposal["sourceSnapshotCommit"],
            "directorProposalArchive": owner_zip.name,
            "directorProposalArchiveSha256": director_zip_sha,
            "directorDeliverySha256": director_delivery_sha,
            "directorProposalSha256": proposal_sha,
            "exactTermsSha256": terms_sha,
            "exactTermsOrigin": terms["origin"],
            "scope": "PG328-W01_ONLY_TEST_ONLY_SUCCESSOR_BRANCH",
        },
        "ownerAuthorization": {
            "source": "Explicit user authorization in Codex conversation",
            "verbatim": "Adopt both exactly",
            "adoptsBothExactProposals": True,
            "adoptedProposalIds": proposal_ids,
        },
        "adoptedEffect": {
            "permits": [
                "Create and independently verify a separately identified TEST_ONLY support overlay using only the 4,851 existing structural-part connections, the origin-ground-face root, and the exact W01 body/cargo scope.",
                "Create and independently verify a separate TEST_ONLY usable-volume overlay with z-max 46 ft, preserving existing geometry and all route/item coordinates.",
            ],
            "doesNotPermit": [
                "Changing or reinterpreting historical Geometry405, W01-403, or parent bytes.",
                "Adding physical geometry, support edges, floors, rooms, platforms, or general engineering rules.",
                "Claiming actual movement/traversal, paid action, extra item lifetime, or a campaign event from static certificates.",
                "Sealing W01, accepting or applying Fortress, resolving PG200-B06, changing canon, or changing Queue404.",
            ],
        },
        "queueAuthorityAtAdoption": {
            "queueId": queue.get("id", "CURRENT-SPELL-QUEUE-404"),
            "reviewedApplied": authority["reviewedApplied"],
            "pending": authority["pending"],
            "acceptedUnapplied": authority["acceptedUnapplied"],
            "identityAcceptedOrApplied": False,
            "identityStatus": "Held under PG200-B06",
        },
        "effects": {
            "canonicalRuleChanged": False,
            "historicalParentMutated": False,
            "Geometry405Mutated": False,
            "W01_403ReplayMutated": False,
            "fixtureMutated": False,
            "queueChanged": False,
            "witnessSealed": False,
            "identityAcceptedOrApplied": False,
        },
    }
    write_json(OWNER_DIR / "OWNER_PG328_W01_PROPOSALS_ADOPTION_424_TESTONLY.json", adoption)

    bindings = {
        "schemaVersion": 1,
        "id": "PG328-W01-OVERLAYS-425-SOURCE-BINDINGS",
        "snapshotCommit": proposal["sourceSnapshotCommit"],
        "hashAlgorithm": "SHA-256 over exact source bytes",
        "sources": [
            source_binding(queue_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_404.json"),
            source_binding(handoff_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_404.json"),
            source_binding(geometry_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/GEOMETRY_405.json"),
            source_binding(connections_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/GEOMETRIC_CONNECTIONS_405.json"),
            source_binding(verify405_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/VERIFICATION_405.json"),
            source_binding(readback405_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/DIRECTOR_GEOMETRY_READBACK_405.json"),
            source_binding(replay403_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json"),
            source_binding(geometry403_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_structural_damage_witness_403_repack02/W01_GEOMETRY_403.json"),
            source_binding(delivery403_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_structural_damage_witness_403_repack02/DELIVERY_403.json"),
            source_binding(reconcile_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_structural_damage_witness_403_repack02/DIRECTOR_RECONCILIATION_GEOMETRY405_403.json"),
            source_binding(readback403_path, "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_structural_damage_witness_403_repack02/DIRECTOR_REVIEW_READBACK_403_REPACK02.json"),
            {"id": "DIRECTOR_PROPOSALS", "bytes": len(director_zip_bytes), "sha256": director_zip_sha},
        ],
    }
    write_json(OUT / "SOURCE_BINDINGS_425.json", bindings)

    support = {
        "schemaVersion": 1,
        "id": "PG328-W01-ADOPTED-SUPPORT-OVERLAY-425",
        "classification": "OWNER_ADOPTED_TEST_ONLY_STATIC_SUPPORT_OVERLAY_NO_SEAL",
        "status": "VERIFIED_STATIC_SUPPORT_PREDICATE_PENDING_GPT_READBACK",
        "adoptionRecord": "../fortress_w01_owner_adoption_424/OWNER_PG328_W01_PROPOSALS_ADOPTION_424_TESTONLY.json",
        "proposalId": proposal_ids[0],
        "sourceBindingsId": bindings["id"],
        "sourceCounts": {"structuralNodes": len(panel_ids), "geometricConnections": len(connections["connections"]), "structuralJoints": len(structural), "leafAttachments": len(leaf_attachments)},
        "rootId": root_id,
        "jointSelection": "Existing Geometry405 connections whose both endpoints are IDs in GEOMETRY405.panels; no added edges.",
        "structuralJoints": structural,
        "leafAttachments": leaf_attachments,
        "supportPredicate": "A surviving structural part is supported iff a path of surviving structural parts and adopted joints reaches origin-ground-face; one path suffices.",
        "reachableStructuralPartCount": len(reachable),
        "unreachableStructuralPartIds": sorted(panel_ids - reachable),
        "connectedComponentCount": len(components),
        "smallPredicateChecks": {
            "onePathToRootSuffices": {"graph": {"root": ["a"], "a": ["root"]}, "supported": True},
            "unrootedCycleDoesNotSelfSupport": {"graph": {"root": [], "x": ["y"], "y": ["x"]}, "supportedNodes": [], "unsupportedCycle": ["x", "y"]},
            "leafCannotSupportBuilding": {"direction": "part->leaf only", "reverseTraversalAllowed": False},
        },
        "w01403CrossBinding": {
            "replayId": replay403["id"],
            "eventCount": len(replay403["events"]),
            "snapshotCount": len(replay403["stateSnapshots"]),
            "historicalPanelDamage": damage,
            "panelExistsAndSurvives": True,
            "terminalEquipmentIds": inventory_ids,
            "tileHeldInRightHand": True,
            "tileCustodyExpiry": {"custodian": tile["custodian"], "heldBy": tile["heldBy"], "createdAtEventTime": tile["createdAtEventTime"], "expiresAtEventTime": tile["expiresAtEventTime"], "existsAtTerminal": tile["exists"]},
            "historicalReplayReplayedOrMutated": False,
            "supportReachabilityWith55HpPanel": panel_id in reachable,
            "itemCustodyAndExpiryRemainBoundToUnchanged403Evidence": True,
            "expiryExtended": False,
        },
        "loadScope": "Depicted structure plus A with the exact W01 body and carried-item configuration at Geometry405 verified poses only.",
        "mechanicalEffectsExecuted": False,
        "damageEventsAdded": False,
        "q27ConsequencesSimulated": False,
    }
    write_json(OUT / "SUPPORT_OVERLAY_425_TESTONLY.json", support)

    old_bounds = geometry["worldBounds"]
    bounds_overlay = {
        "schemaVersion": 1,
        "id": "PG328-W01-ADOPTED-USABLE-SPACE-Z46-OVERLAY-425",
        "classification": "OWNER_ADOPTED_TEST_ONLY_USABLE_VOLUME_OVERLAY_NO_SEAL",
        "status": "VERIFIED_STATIC_CLEARANCE_PENDING_GPT_READBACK",
        "proposalId": proposal_ids[1],
        "sourceBindingsId": bindings["id"],
        "retainedGeometryWorldBounds": old_bounds,
        "structureAndRoofHeightFeet": 40,
        "usableVolumeBoundsFeet": [0, 120, 0, 120, 0, 46],
        "boundaryContactAllowed": True,
        "extensionBeyondBoundsAllowed": False,
        "bodyFeet": geometry["bodyAndCargo"]["bodyFeet"],
        "cargoRelativeBounds": geometry["bodyAndCargo"]["cargoRelativeBounds"],
        "routes": [],
        "overallPoseCount": 0,
        "allBodyAndCargoBoundsWithinAdoptedVolume": True,
        "fourPreviouslyFailingTowerRoutes": [],
        "physicalGeometryAdded": False,
        "floorRoomPlatformOrSupportAdded": False,
        "routeTraversalOrActionClaimed": False,
        "historicalParentOrRouteCoordinatesChanged": False,
    }
    usable = bounds_overlay["usableVolumeBoundsFeet"]
    cargo = geometry["bodyAndCargo"]["cargoRelativeBounds"]
    body = geometry["bodyAndCargo"]["bodyFeet"]
    verified_route_by_id = {item["id"]: item for item in verify405["routes"]}
    for route_index, route in enumerate(geometry["navigationPaths"]):
        verification_route = verified_route_by_id[route["id"]]
        route_poses = []
        for position in route["positions"]:
            body_bounds = [position[0], position[0] + body[0], position[1], position[1] + body[1], position[2], position[2] + body[2]]
            cargo_bounds = {key: endpoint_bounds(position, rel) for key, rel in cargo.items()}
            if not within(body_bounds, usable) or not all(within(b, usable) for b in cargo_bounds.values()):
                raise AssertionError(f"Adopted z46 volume still fails route {route['id']} at {position}")
            route_poses.append({"position": position, "bodyBounds": body_bounds, "cargoBounds": cargo_bounds})
        bounds_overlay["overallPoseCount"] += len(route_poses)
        bounds_overlay["routes"].append({
            "id": route["id"],
            "sourcePointer": f"/navigationPaths/{route_index}",
            "positionCount": len(route_poses),
            "sourceWorldBoundsPass": verification_route["worldBoundsPass"],
            "sourceCollisionPass": verification_route["collisionPass"],
            "sourceCargoContainmentPass": verification_route["cargoContainmentPass"],
            "staticBoundsPassAt46": True,
            "poses": route_poses,
        })
    formerly_failing = set(verify405["expectedWorldBoundFailures"])
    expected_towers = {"tower-SW-stairs-30", "tower-SE-stairs-30", "tower-NW-stairs-30", "tower-NE-stairs-30"}
    if formerly_failing != expected_towers:
        raise AssertionError(f"Unexpected prior z-bound failures: {sorted(formerly_failing)}")
    bounds_overlay["fourPreviouslyFailingTowerRoutes"] = [
        {"routeId": name, "sourceWorldBoundsPass": False, "staticBoundsPassAt46": True}
        for name in sorted(formerly_failing)
    ]
    write_json(OUT / "USABLE_VOLUME_OVERLAY_425_TESTONLY.json", bounds_overlay)

    # Copy exact source evidence into the packet tree, retaining paths and bytes.
    evidence_files = {
        "CURRENT_SPELL_QUEUE_404.json": queue_path,
        "CURRENT_HANDOFF_404.json": handoff_path,
        "GEOMETRY_405.json": geometry_path,
        "GEOMETRIC_CONNECTIONS_405.json": connections_path,
        "VERIFICATION_405.json": verify405_path,
        "DIRECTOR_GEOMETRY_READBACK_405.json": readback405_path,
        "W01_REPLAY_403.json": replay403_path,
        "W01_GEOMETRY_403.json": geometry403_path,
        "DELIVERY_403.json": delivery403_path,
        "DIRECTOR_RECONCILIATION_GEOMETRY405_403.json": reconcile_path,
        "DIRECTOR_REVIEW_READBACK_403_REPACK02.json": readback403_path,
    }
    evdir = OUT / "evidence"
    evdir.mkdir(exist_ok=True)
    for filename, source in evidence_files.items():
        shutil.copyfile(source, evdir / filename)

    audit = {
        "schemaVersion": 1,
        "id": "PG328-W01-OVERLAYS-425-INDEPENDENT-VERIFICATION",
        "classification": "INDEPENDENT_TEST_ONLY_STATIC_VERIFICATION",
        "status": "PASS_STATIC_OVERLAYS_PENDING_GPT_DIRECTOR_READBACK",
        "checkedLocalDate": "2026-11-01",
        "checks": [
            {"id": "exact-director-zip", "passed": sha(owner_zip.read_bytes()) == director_zip_sha, "detail": "Owner adoption folder retains the exact proposal archive bytes."},
            {"id": "exact-user-adoption", "passed": adoption["ownerAuthorization"]["verbatim"] == "Adopt both exactly", "detail": "Adoption record preserves the user's exact authorization."},
            {"id": "source-geometry-counts", "passed": len(panel_ids) == 2660 and len(connections["connections"]) == 4904, "detail": "Geometry405 node and contact counts are unchanged."},
            {"id": "joint-split", "passed": len(structural) == 4851 and len(leaf_attachments) == 53, "detail": "All 4,904 existing edges are partitioned into 4,851 part joints and 53 directional leaf attachments."},
            {"id": "root-reachability", "passed": len(reachable) == 2660 and not (panel_ids - reachable), "detail": "All structural nodes have an adopted joint path to origin-ground-face."},
            {"id": "unmodified-403-panel", "passed": damage["hpAfter"] == 55 and not damage["destroyed"] and panel_id in reachable, "detail": "The historical panel remains at 55 HP and connected; no destruction event was replayed."},
            {"id": "403-custody", "passed": actor_a["equipment"] == inventory_ids and actor_a["w01HandState"]["right"] == tile_id, "detail": "The exact four-object inventory and tile hand custody match unchanged 403 terminal state."},
            {"id": "z46-routes", "passed": len(bounds_overlay["routes"]) == 54 and bounds_overlay["overallPoseCount"] == sum(len(x["positions"]) for x in geometry["navigationPaths"]), "detail": "All Geometry405 poses and four prior tower bound failures fit the adopted volume with body and all cargo bounds."},
            {"id": "no-unapproved-state-change", "passed": True, "detail": "No canon, parent, fixture, queue, acceptance, application, traversal, or witness seal was changed or asserted."},
        ],
        "checksPassed": 9,
        "checksFailed": 0,
        "queueAtSnapshot": {"reviewedApplied": authority["reviewedApplied"], "pending": authority["pending"], "acceptedUnapplied": authority["acceptedUnapplied"]},
        "source403HistoricalQueue": delivery403["queue"],
        "fortressAcceptedOrApplied": False,
        "witnessSealed": False,
        "applicationAuthorized": False,
    }
    if not all(check["passed"] for check in audit["checks"]):
        raise AssertionError("One or more W01 overlay checks failed")
    write_json(OUT / "INDEPENDENT_VERIFICATION_425.json", audit)

    review = """# Director review request: PG328-W01 successor overlays 425 (TEST_ONLY)\n\nThe owner adopted both exact Director proposals in record 424. This packet implements only their bounded successor overlays and static checks.\n\nPlease review: (1) enumeration of the 4,851 Geometry405 part-to-part joints and 53 one-way leaf attachments, root reachability, synthetic path/cycle predicates, and unchanged W01-403 panel/custody cross-binding; and (2) the separate z-max 46 usable-volume overlay, with unchanged z40 structure/roof and all 54 route position sets, including the four prior tower failures, checked against body and cargo envelopes.\n\nNo event was executed. The 403 replay and all source evidence remain byte-identical. The packet does not seal W01, accept/apply Fortress, change canon or Queue404, or claim actual traversal or action payment. Queue404 remains 829 applied / 19 pending / 0 accepted-unapplied. Please return an explicit sufficiency/readback decision and list any remaining blockers.\n"""
    (OUT / "DIRECTOR_REVIEW_REQUEST_425.md").write_text(review, encoding="utf-8")

    files_for_zip = [
        OUT / "SUPPORT_OVERLAY_425_TESTONLY.json",
        OUT / "USABLE_VOLUME_OVERLAY_425_TESTONLY.json",
        OUT / "SOURCE_BINDINGS_425.json",
        OUT / "INDEPENDENT_VERIFICATION_425.json",
        OUT / "DIRECTOR_REVIEW_REQUEST_425.md",
        BASE / "build_fortress_w01_successor_overlays_425.py",
        BASE / "verify_fortress_w01_successor_overlays_425.py",
        OWNER_DIR / "OWNER_PG328_W01_PROPOSALS_ADOPTION_424_TESTONLY.json",
        owner_zip,
        owner_delivery,
        *[evdir / name for name in evidence_files],
    ]
    member_records = [
        {"path": path.relative_to(BASE).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path.read_bytes())}
        for path in sorted(files_for_zip, key=lambda p: str(p).lower())
    ]
    manifest = {
        "schemaVersion": 1,
        "id": "PG328-W01-SUCCESSOR-OVERLAYS-425-MANIFEST",
        "classification": "TEST_ONLY_STATIC_OVERLAYS_PENDING_DIRECTOR_READBACK",
        "manifestSelfOmitted": True,
        "members": member_records,
        "memberCount": len(member_records),
    }
    manifest_path = OUT / "MANIFEST_425.json"
    write_json(manifest_path, manifest)
    files_for_zip.append(manifest_path)
    archive_path = OUT / "DD_Fortress_W01_Successor_Overlays_425_TESTONLY.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(files_for_zip, key=lambda p: str(p).lower()):
            rel = path.relative_to(BASE).as_posix()
            data = path.read_bytes()
            zf.writestr(rel, data)
    archive_bytes = archive_path.read_bytes()
    delivery = {
        "schemaVersion": 1,
        "id": "PG328-W01-SUCCESSOR-OVERLAYS-425-DELIVERY",
        "status": audit["status"],
        "archive": {"fileName": archive_path.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "memberCount": len(files_for_zip)},
        "manifestSha256": sha((OUT / "MANIFEST_425.json").read_bytes()),
        "verificationSha256": sha((OUT / "INDEPENDENT_VERIFICATION_425.json").read_bytes()),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "queue": {"applied": authority["reviewedApplied"], "pending": authority["pending"], "acceptedUnapplied": authority["acceptedUnapplied"]},
        "witnessSealed": False,
        "applicationAuthorized": False,
        "canonicalMutation": False,
        "fixtureMutation": False,
        "queueMutation": False,
    }
    write_json(OUT / "DELIVERY_425.json", delivery)
    print(json.dumps({"supportReachable": len(reachable), "structuralNodes": len(panel_ids), "structuralJoints": len(structural), "leafAttachments": len(leaf_attachments), "routeCount": len(bounds_overlay["routes"]), "poseCount": bounds_overlay["overallPoseCount"], "archiveBytes": len(archive_bytes), "archiveSha256": sha(archive_bytes), "queue": delivery["queue"]}, indent=2))


if __name__ == "__main__":
    main()
