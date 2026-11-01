#!/usr/bin/env python3
"""Independent source, graph, geometry, custody, and package checks for W01 overlays 425."""

from __future__ import annotations

import hashlib
import json
import zipfile
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OWNER = BASE / "fortress_w01_owner_adoption_424"
OUT = BASE / "fortress_w01_successor_overlays_425"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def inside(b, v):
    return b[0] >= v[0] and b[1] <= v[1] and b[2] >= v[2] and b[3] <= v[3] and b[4] >= v[4] and b[5] <= v[5]


def main() -> None:
    checks = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"id": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    adoption = read_json(OWNER / "OWNER_PG328_W01_PROPOSALS_ADOPTION_424_TESTONLY.json")
    proposal_zip = OWNER / "DD_Fortress_W01_Support_Z40_Director_Proposals_V1_TESTONLY.zip"
    proposal_delivery = OWNER / "DD_Fortress_W01_Support_Z40_Director_Proposals_V1_DELIVERY.json"
    check("owner-verbatim-adoption", adoption["ownerAuthorization"]["verbatim"] == "Adopt both exactly", "The owner record stores the exact authorization and both proposal IDs.")
    check("director-archive-hash", sha(proposal_zip.read_bytes()) == adoption["scope"]["directorProposalArchiveSha256"] == "18451b3b9f353a96d0f6d06d635f568db8c190d8b96acd6e51f1189a443b026b", "Exact Director proposal archive bytes are preserved.")
    check("director-delivery-hash", sha(proposal_delivery.read_bytes()) == adoption["scope"]["directorDeliverySha256"] == "117dd885d2f101f1a20c31634b9ee64e7855148c61b0fe039e2f06a292452055", "Exact Director delivery bytes are preserved.")
    with zipfile.ZipFile(proposal_zip) as zf:
        director_proposal = json.loads(zf.read("DIRECTOR_PROPOSAL.json"))
        exact_terms = json.loads(zf.read("EXACT_PROPOSAL_TERMS.json"))
        check("exact-proposal-binding", sha(zf.read("DIRECTOR_PROPOSAL.json")) == adoption["scope"]["directorProposalSha256"] and sha(zf.read("EXACT_PROPOSAL_TERMS.json")) == adoption["scope"]["exactTermsSha256"], "Adoption binds the exact Director proposal and terms members.")
        check("proposal-ids", director_proposal["proposalIds"] == adoption["scope"]["proposalIds"] and len(exact_terms["support"]) == 5 and len(exact_terms["z40"]) == 4, "Both adopted proposal IDs and all exact term clauses are present.")

    bindings = read_json(OUT / "SOURCE_BINDINGS_425.json")
    source_map = {item["repositoryPath"]: item for item in bindings["sources"] if "repositoryPath" in item}
    for repo_path, binding in source_map.items():
        data = (ROOT / repo_path).read_bytes()
        check(f"source:{Path(repo_path).name}", len(data) == binding["bytes"] and sha(data) == binding["sha256"], f"Exact source bytes match: {repo_path}")
    check("source-snapshot", bindings["snapshotCommit"] == "8fa2dee1e450faf385b0b6dfdd11565cd7e18a3b", "Overlays bind to the same source snapshot reviewed by the Director.")

    geometry = read_json(BASE / "fortress_w01_geometry_405/GEOMETRY_405.json")
    connections = read_json(BASE / "fortress_w01_geometry_405/GEOMETRIC_CONNECTIONS_405.json")
    support = read_json(OUT / "SUPPORT_OVERLAY_425_TESTONLY.json")
    panel_ids = {item["id"] for item in geometry["panels"]}
    leaf_ids = {item["id"] for item in geometry["doorLeaves"]}
    check("source-node-and-edge-counts", len(panel_ids) == 2660 and len(connections["connections"]) == 4904, "Geometry405 has 2,660 panel nodes and 4,904 geometric connections.")
    check("adopted-edge-partition", len(support["structuralJoints"]) == 4851 and len(support["leafAttachments"]) == 53, "The adopted partition enumerates 4,851 support joints and 53 leaf attachments.")
    graph = {node: set() for node in panel_ids}
    for edge in support["structuralJoints"]:
        check("joint-endpoint-membership", edge["a"] in panel_ids and edge["b"] in panel_ids, "Every adopted joint uses existing panel IDs only.")
        graph[edge["a"]].add(edge["b"])
        graph[edge["b"]].add(edge["a"])
    leaves_valid = all(x["structuralPartId"] in panel_ids and x["leafId"] in leaf_ids and x["leafSupportsBuilding"] is False and x["supportDirection"] == "structural part supports leaf only" for x in support["leafAttachments"])
    check("leaf-attachments-one-way", leaves_valid, "Each leaf edge points from a structural part to a named leaf and cannot support the building.")
    root = support["rootId"]
    seen, queue = {root}, deque([root])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node] - seen:
            seen.add(neighbor)
            queue.append(neighbor)
    check("root-reachability", root == "origin-ground-face" and seen == panel_ids and support["reachableStructuralPartCount"] == 2660, "All surviving structural nodes reach the adopted root through existing adopted joints.")
    check("contract-predicate-examples", support["smallPredicateChecks"]["onePathToRootSuffices"]["supported"] is True and support["smallPredicateChecks"]["unrootedCycleDoesNotSelfSupport"]["supportedNodes"] == [], "A single rooted path suffices; an isolated cycle has no root support.")

    w403_dir = BASE / "fortress_w01_structural_damage_witness_403_repack02"
    replay403 = read_json(w403_dir / "W01_REPLAY_403.json")
    terminal = replay403["stateSnapshots"][replay403["terminalStateId"]]
    damage = replay403["targetDamage"]
    cross = support["w01403CrossBinding"]
    panel_id = "W01-SOUTH-WALL-X25-Z0"
    tile_id = "PG328-W01-403:CLAY-TILE-1"
    tile = terminal["items"][tile_id]
    check("historical-panel-state", damage["panelId"] == panel_id and damage["hpBefore"] == 60 and damage["hpAfter"] == 55 and damage["destroyed"] is False and panel_id in seen, "The unchanged historical attack leaves the named panel alive at 55 HP and structurally connected.")
    check("terminal-cargo-custody", terminal["actors"]["A"]["equipment"] == ["focus-A", "pack-A", "cargo-A", tile_id] and terminal["actors"]["A"]["w01HandState"]["right"] == tile_id and tile["custodian"] == "A" and tile["heldBy"] == "A:right", "The historical 403 terminal state preserves exact carried-item custody.")
    check("tile-expiry-unchanged", tile["createdAtEventTime"] == 6.13 and tile["expiresAtEventTime"] == 3606.13 and cross["expiryExtended"] is False, "No item lifetime extension is inferred or applied.")
    check("historical-replay-untouched", len(replay403["events"]) == 30 and len(replay403["stateSnapshots"]) == 31 and cross["historicalReplayReplayedOrMutated"] is False, "W01-403 remains an unchanged source; no damage events were replayed.")

    volume = read_json(OUT / "USABLE_VOLUME_OVERLAY_425_TESTONLY.json")
    original_volume = geometry["worldBounds"]
    v = volume["usableVolumeBoundsFeet"]
    check("separate-z46-only-overlay", volume["retainedGeometryWorldBounds"] == original_volume == [0, 120, 0, 120, 0, 40] and volume["structureAndRoofHeightFeet"] == 40 and v == [0, 120, 0, 120, 0, 46], "Only the usable z maximum changes; structure/roof and original geometry remain at z40.")
    cargo = geometry["bodyAndCargo"]["cargoRelativeBounds"]
    body = geometry["bodyAndCargo"]["bodyFeet"]
    pose_count = 0
    route_map = {route["id"]: route for route in geometry["navigationPaths"]}
    for route in volume["routes"]:
        src = route_map[route["id"]]
        check(f"route-position-count:{route['id']}", route["positionCount"] == len(src["positions"]) and len(route["poses"]) == len(src["positions"]), "Every source pose is present exactly once in the static overlay.")
        for pose in route["poses"]:
            x, y, z = pose["position"]
            body_box = [x, x + body[0], y, y + body[1], z, z + body[2]]
            cargo_boxes = {}
            for key, rb in cargo.items():
                cargo_boxes[key] = [x + rb[0], x + rb[1], y + rb[2], y + rb[3], z + rb[4], z + rb[5]]
            check(f"body-bounds:{route['id']}:{pose_count}", pose["bodyBounds"] == body_box and inside(body_box, v), "Swept actor body is within adopted bounds; boundary contact is allowed.")
            check(f"cargo-bounds:{route['id']}:{pose_count}", pose["cargoBounds"] == cargo_boxes and all(inside(box, v) for box in cargo_boxes.values()), "All carried item bounds are within adopted bounds.")
            pose_count += 1
    check("all-routes-and-poses", len(volume["routes"]) == 54 and pose_count == 1586 and volume["overallPoseCount"] == pose_count, "All 54 source routes and all 1,586 tested positions have body/cargo bounds checked.")
    expected_failing = {"tower-SW-stairs-30", "tower-SE-stairs-30", "tower-NW-stairs-30", "tower-NE-stairs-30"}
    old_verification = read_json(BASE / "fortress_w01_geometry_405/VERIFICATION_405.json")
    check("four-prior-tower-failures", set(old_verification["expectedWorldBoundFailures"]) == expected_failing and {x["routeId"] for x in volume["fourPreviouslyFailingTowerRoutes"]} == expected_failing and all(x["staticBoundsPassAt46"] for x in volume["fourPreviouslyFailingTowerRoutes"]), "The four previously failing tower ascents fit z46 with no movement or action claim.")
    check("no-extra-geometry", volume["physicalGeometryAdded"] is False and volume["floorRoomPlatformOrSupportAdded"] is False and volume["routeTraversalOrActionClaimed"] is False, "No floor, room, platform, physical support, or actual traversal is asserted.")

    queue_data = read_json(BASE / "CURRENT_SPELL_QUEUE_404.json")["currentAuthority"]
    delivery403 = read_json(w403_dir / "DELIVERY_403.json")
    check("unchanged-current-queue", queue_data == {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0, "completeStandaloneProcedures": 553, "scopedInterfaces": 173}, "Queue404 authority remains unchanged at 829/19/0.")
    check("unaccepted-unapplied-held", adoption["effects"]["witnessSealed"] is False and adoption["effects"]["identityAcceptedOrApplied"] is False and delivery403["heldIds"] == ["conjure-demiplane-fortress"], "Fortress remains held; no sealing, acceptance, or application occurred.")

    manifest = read_json(OUT / "MANIFEST_425.json")
    delivery = read_json(OUT / "DELIVERY_425.json")
    archive = OUT / delivery["archive"]["fileName"]
    check("delivery-archive-hash", len(archive.read_bytes()) == delivery["archive"]["bytes"] and sha(archive.read_bytes()) == delivery["archive"]["sha256"], "Delivery hash matches the final W01 package archive.")
    check("manifest-hash", sha((OUT / "MANIFEST_425.json").read_bytes()) == delivery["manifestSha256"], "Delivery hash matches the independent member manifest.")
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        names = {x.filename for x in infos}
        manifest_member = (OUT.relative_to(BASE) / "MANIFEST_425.json").as_posix()
        check("archive-member-count", len(infos) == delivery["archive"]["memberCount"] and manifest_member in names, "Final ZIP contains the declared member count and manifest.")
        records = {x["path"]: x for x in manifest["members"]}
        check("manifest-member-set", set(records) == names - {manifest_member}, "Manifest enumerates every payload member; its own hash is carried by delivery.")
        for name, record in records.items():
            data = zf.read(name)
            check(f"archive-member-hash:{Path(name).name}", len(data) == record["bytes"] and sha(data) == record["sha256"], "Archive member bytes match the manifest.")

    groups = {}
    for item in checks:
        group = item["id"].split(":", 1)[0]
        entry = groups.setdefault(group, {"checksPassed": 0, "checksFailed": 0})
        entry["checksPassed" if item["passed"] else "checksFailed"] += 1
    result = {
        "schemaVersion": 1,
        "id": "PG328-W01-OVERLAYS-425-VERIFIER-RESULT",
        "classification": "INDEPENDENT_TEST_ONLY_STATIC_VERIFICATION",
        "status": "PASS_PENDING_GPT_DIRECTOR_READBACK",
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checkGroups": groups,
        "archiveSha256": delivery["archive"]["sha256"],
        "archiveBytes": delivery["archive"]["bytes"],
        "queue": delivery["queue"],
        "witnessSealed": False,
        "applicationAuthorized": False,
    }
    result_path = OUT / "VERIFIER_RESULT_425.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checksPassed": result["checksPassed"], "archiveBytes": result["archiveBytes"], "archiveSha256": result["archiveSha256"], "queue": result["queue"]}, indent=2))


if __name__ == "__main__":
    main()
