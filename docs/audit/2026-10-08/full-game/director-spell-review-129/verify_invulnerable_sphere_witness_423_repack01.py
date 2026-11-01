#!/usr/bin/env python3
"""Independent integrity, geometry, queue, and reversibility audit for Sphere 423."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "invulnerable_sphere_witness_423_repack01"
REPLAY_PATH = OUT / "SPHERE_WITNESS_REPLAY_423_REPACK01_TESTONLY.json"
ADOPTION_PATH = OUT / "OWNER_SPHERE_PREMISES_ADOPTION_422_TESTONLY.json"
PROPOSAL_PATH = OUT / "SPHERE_CANDIDATE_PROPOSAL_421.json"
SOURCE_BINDINGS_PATH = OUT / "SOURCE_BINDINGS_423.json"
CORRECTIONS_PATH = OUT / "DIRECTOR_CORRECTIONS_423_REPACK01.json"
AUDIT_PATH = OUT / "INDEPENDENT_AUDIT_423_REPACK01.json"
MANIFEST_PATH = OUT / "MANIFEST_423_REPACK01.json"
DELIVERY_PATH = OUT / "DELIVERY_423_REPACK01.json"
ZIP_PATH = OUT / "DD_Rank9_InvulnerableSphere_DF218-B04_Witness_423_Repack01_TESTONLY.zip"


def raw_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return raw_sha(canonical(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def apply_patch(document: Any, operations: list[dict[str, Any]]) -> Any:
    result = copy.deepcopy(document)
    for operation in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in operation["path"][1:].split("/")]
        parent: Any = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = parts[-1]
        if operation["op"] == "add":
            if isinstance(parent, list):
                parent.insert(int(key), copy.deepcopy(operation["value"]))
            else:
                if key in parent:
                    raise ValueError(f"Add target exists: {operation['path']}")
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
            raise ValueError(f"Unsupported operation: {operation['op']}")
    return result


def close(a: float, b: float, tol: float = 1e-8) -> bool:
    return abs(a - b) <= tol


def box_max_radius(box: list[list[float]], center: list[float]) -> float:
    return math.sqrt(sum(max(abs(float(lo) - c), abs(float(hi) - c)) ** 2 for (lo, hi), c in zip(box, center)))


def box_min_radius(box: list[list[float]], center: list[float]) -> float:
    squares = []
    for (lo, hi), c in zip(box, center):
        distance = lo - c if c < lo else (c - hi if c > hi else 0.0)
        squares.append(distance * distance)
    return math.sqrt(sum(squares))


def crc32(raw: bytes) -> str:
    import zlib
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def main() -> None:
    replay = read_json(REPLAY_PATH)
    adoption = read_json(ADOPTION_PATH)
    proposal = read_json(PROPOSAL_PATH)
    source_bindings = read_json(SOURCE_BINDINGS_PATH)
    corrections = read_json(CORRECTIONS_PATH)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"id": check_id, "passed": bool(passed), "detail": detail})
        if not passed:
            raise ValueError(f"{check_id} failed: {detail}")

    check("adoption:premise-set", adoption["ownerAuthorization"]["adoptedPremiseIds"] == [f"SP-CAND-P0{i}" for i in range(1, 6)], "The user adoption record names P01 through P05 exactly.")
    check("adoption:proposal-binding", raw_sha(PROPOSAL_PATH.read_bytes()) == adoption["scope"]["proposalSha256"] == replay["initialState"]["sourceBindings"]["candidateProposal"]["sha256"], "The adopted record, extracted proposal, and replay bind the same exact proposal bytes.")
    check("adoption:authorization-text", adoption["ownerAuthorization"]["verbatim"] == "Adopt P01–P05 exactly", "The recorded authorization matches the owner's explicit instruction.")
    check("adoption:scope", adoption["scope"]["identity"] == "invulnerable-sphere" and adoption["scope"]["blockerId"] == "DF218-B04", "Adoption is limited to Invulnerable Sphere / DF218-B04 candidate witness.")
    check("corrections:director-set", [row["id"] for row in corrections["corrections"]] == ["SP423-C01", "SP423-C02", "SP423-C03"] and corrections["limits"] == {"newPremises": False, "parentChanged": False, "fixtureChanged": False, "canonicalRuleChanged": False, "queueChanged": False, "accepted": False, "applied": False, "sealed": False}, "Repack01 records exactly GPT's three requested corrections and no new authority or premise.")

    source_checks = []
    for key, binding in source_bindings["bindings"].items():
        if key in ("candidateProposal", "ownerAdoption"):
            continue
        if key == "heldB4Parent":
            archive_path = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
            with zipfile.ZipFile(archive_path) as archive:
                raw = archive.read("cases/RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR.json")
            actual = raw_sha(raw)
        else:
            actual = raw_sha((ROOT / binding["path"]).read_bytes())
        source_checks.append(actual == binding["sha256"])
    check("source:bound-bytes", all(source_checks), "All current source hashes match the replay bindings, including the preserved B4 case member.")
    check("source:adoption-hash", raw_sha(ADOPTION_PATH.read_bytes()) == replay["initialState"]["sourceBindings"]["ownerAdoption"]["sha256"], "Replay binds the exact owner adoption record bytes.")

    queue_binding = source_bindings["bindings"]["queue404"]
    queue = read_json(ROOT / queue_binding["path"])
    check("queue:unchanged-authority", queue_binding["sha256"] == raw_sha((ROOT / queue_binding["path"]).read_bytes()) and queue_binding["applied"] == 829 and queue_binding["pending"] == 19 and queue_binding["acceptedUnapplied"] == 0, "Queue404 bytes and 829/19/0 authority match the packet binding.")
    check("queue:witness-not-accepted", replay["finalState"]["disposition"] == {"acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"], "accepted": False, "applied": False, "sealed": False}, "The witness leaves the spell held and unaccepted/unapplied/unsealed.")
    check("queue:all-snapshots", all(s["queueAuthority"] == {"queueId": "CURRENT-SPELL-QUEUE-404", "applied": 829, "pending": 19, "acceptedUnapplied": 0} for row in replay["events"] for s in (row["beforeState"], row["afterState"])), "Every before/after state preserves Queue404 829/19/0.")

    start = replay["initialState"]
    final = replay["finalState"]
    events = replay["events"]
    check("replay:full-snapshots", all(isinstance(row.get("beforeState"), dict) and isinstance(row.get("afterState"), dict) for row in events), "Every transition contains complete before and after states.")
    check("replay:initial-hash", digest(start) == events[0]["beforeSHA256"], "Initial state hash matches the first event.")
    previous_event_hash = "0" * 64
    forward_state = copy.deepcopy(start)
    event_times = []
    for index, row in enumerate(events):
        check(f"replay:event-{index+1:03d}-before", digest(forward_state) == row["beforeSHA256"] == digest(row["beforeState"]), "Event before snapshot and chain state match.")
        check(f"replay:event-{index+1:03d}-prev", row["previousEventHash"] == previous_event_hash, "Previous event link matches.")
        check(f"replay:event-{index+1:03d}-hash", row["eventHash"] == digest({k: v for k, v in row.items() if k != "eventHash"}), "Event hash is self-consistent.")
        forward_state = apply_patch(forward_state, row["forward"])
        check(f"replay:event-{index+1:03d}-forward", forward_state == row["afterState"] and digest(forward_state) == row["afterSHA256"], "Forward operations reproduce the full after snapshot.")
        check(f"replay:event-{index+1:03d}-inverse", apply_patch(forward_state, row["inverse"]) == row["beforeState"], "Inverse operations restore the full before snapshot.")
        previous_event_hash = row["eventHash"]
        event_times.append(row["timeSeconds"])
    check("replay:final", forward_state == final and digest(final) == events[-1]["afterSHA256"], "Forward replay reaches exact final state.")
    check("replay:time-order", event_times == sorted(event_times), "Every actual event and turn marker is chronological.")
    reverse_state = copy.deepcopy(final)
    for row in reversed(events):
        reverse_state = apply_patch(reverse_state, row["inverse"])
        if digest(reverse_state) != row["beforeSHA256"]:
            raise ValueError(f"Complete reverse traversal mismatch at {row['id']}")
    check("replay:reverse-restoration", reverse_state == start and replay["inverseRestorationOrder"] == [row["id"] for row in reversed(events)], "All inverse operations restore the exact initial state in reverse event order.")
    check("replay:chain-head", replay["replaySummary"]["eventChainHead"] == previous_event_hash, "Recorded event chain head matches final event.")

    by_kind = {row["kind"]: row for row in events if row["kind"] in {"O_STUDY_COMPLETE", "CREATE_STEED", "MOUNT_STEED", "COMMIT_CROSSING_ATTEMPT", "DISMOUNT"}}
    check("correction:director-indexes", events[3]["kind"] == "O_STUDY_COMPLETE" and events[10]["kind"] == "CREATE_STEED" and events[16]["kind"] == "MOUNT_STEED" and events[20]["kind"] == "COMMIT_CROSSING_ATTEMPT" and events[25]["kind"] == "DISMOUNT", "Repack01 applies each correction at the Director's exact zero-based event index.")
    check("correction:C02-study-repack", by_kind["O_STUDY_COMPLETE"]["afterState"]["actors"]["O"]["bookAccess"]["repackedAfterStudy"] is True and final["actors"]["O"]["bookAccess"]["repackedAfterStudy"] is True, "O_STUDY_COMPLETE records repackedAfterStudy true and retains it through final state.")
    check("correction:C01-unburdened-create", by_kind["CREATE_STEED"]["afterState"]["actors"]["S1"]["burdened"] is False and by_kind["CREATE_STEED"]["afterState"]["actors"]["S1"]["speedFeet"] == 60, "S1 is unburdened and has 60-ft speed at creation.")
    check("correction:C01-mounted-load", by_kind["MOUNT_STEED"]["afterState"]["actors"]["S1"]["burdened"] is True and by_kind["MOUNT_STEED"]["afterState"]["actors"]["S1"]["speedFeet"] == 50, "Mounting the 170-lb / 7-Load rider payload makes S1 burdened at 50-ft speed.")
    committed = by_kind["COMMIT_CROSSING_ATTEMPT"]["afterState"]
    receipt = committed["transaction"]["commandReceipt"]
    check("correction:C03-command-consumed", committed["transaction"]["pendingCommand"] is None and committed["actors"]["S1"]["command"] is None and receipt["status"] == "CONSUMED_AT_ATTEMPT_START" and receipt["command"]["type"] == "Planar Crossing" and committed["transaction"]["crossingAttempt"]["commandReceipt"] == receipt and committed["actors"]["O"]["turn"]["actions"]["bonusAction"] == "SPENT" and committed["actors"]["O"]["turn"]["sharedCommandUsed"] is True and committed["actors"]["S1"]["action"] == "SPENT" and committed["actors"]["S1"]["crossingUsesRemaining"] == 0, "The command clears at attempt start while full command receipt and spent owner Bonus Action, Steed Action, and crossing use remain recorded.")
    later_attached = [row for row in events if row["kind"] == "STEED_ATTACHED_PHASE" and row["timeSeconds"] > by_kind["COMMIT_CROSSING_ATTEMPT"]["timeSeconds"]]
    check("correction:C03-later-dodge", len(later_attached) > 0 and all(row["afterState"]["transaction"]["pendingCommand"] is None and row["afterState"]["actors"]["S1"]["command"] is None and row["afterState"]["actors"]["S1"]["lastAction"] == "Dodge" for row in later_attached), "Every later attached phase defaults to Dodge with no pending crossing command.")
    dismounted = by_kind["DISMOUNT"]["afterState"]["actors"]["S1"]
    check("correction:C01-unburdened-dismount", dismounted["burdened"] is False and dismounted["speedFeet"] == 60 and dismounted["rider"] is None, "Dismount restores S1's unburdened 60-ft state.")
    check("correction:C01-through-state", all(row["afterState"]["actors"]["S1"]["burdened"] is True and row["afterState"]["actors"]["S1"]["speedFeet"] == 50 for row in events if by_kind["MOUNT_STEED"]["timeSeconds"] <= row["timeSeconds"] < by_kind["DISMOUNT"]["timeSeconds"]), "Mounted burden and speed persist through every intermediate state until dismount.")

    counts: dict[str, int] = {}
    for row in events:
        counts[row["kind"]] = counts.get(row["kind"], 0) + 1
    check("markers:C-counts", counts.get("REGULAR_START", 0) == 22 and sum(1 for row in events if row["kind"] == "REGULAR_START" and row["actor"] == "C") == 11 and sum(1 for row in events if row["kind"] == "REGULAR_START" and row["actor"] == "O") == 11, "Dispatch all 11 C and 11 O regular START markers.")
    check("markers:ends", sum(1 for row in events if row["kind"] == "REGULAR_END" and row["actor"] == "C") == 11 and sum(1 for row in events if row["kind"] == "REGULAR_END" and row["actor"] == "O") == 10, "Dispatch 11 C and 10 O END markers; O has no END after expiry at START 62.")
    check("markers:steed-attached", counts.get("STEED_ATTACHED_PHASE", 0) == 10, "Dispatch every S1 attached phase while its original application is active.")

    sphere = final["scene"]["objects"]["sphere"]
    geom = proposal["geometry"]
    inner = float(geom["conservativeClearInteriorRadiusFeet"])
    center = list(geom["sphereCenter"])
    mount_radius = box_max_radius(geom["destinationMountBox"], center)
    rider_radius = box_max_radius(geom["destinationRiderBox"], center)
    caster_nearest = box_min_radius(geom["destinationCasterBox"], center)
    check("geometry:mount-inside", mount_radius < inner, f"Destination mount's farthest occupied corner {mount_radius:.6f} ft is inside the conservative clear radius {inner:.6f} ft.")
    check("geometry:rider-inside", rider_radius < inner, f"Destination rider/cargo envelope's farthest occupied corner {rider_radius:.6f} ft is inside the conservative clear radius {inner:.6f} ft.")
    check("geometry:caster-outside", caster_nearest > float(geom["radiusFeet"]) + float(geom["thicknessFeet"]), f"C's nearest occupied point is {caster_nearest:.6f} ft from center and outside the shell.")
    check("geometry:ground-clear", float(geom["sphereCenter"][2]) - float(geom["radiusFeet"]) > float(geom["destinationGroundZ"]), "The Sphere shell is above ground and does not intersect the declared floor.")
    caster_distance = math.dist([30, 0, 0], center)
    check("geometry:caster-range", caster_distance <= 120, f"C-to-center distance {caster_distance:.6f} ft is within the 120-ft native range.")
    check("geometry:steed-creation-range", math.dist([7.5, 0, 0], [0, 0, 0]) <= 60, "O perceives clear S1 creation space within the Steed's 60-ft range.")
    check("geometry:boundary-not-grounded", sphere["status"] == "EXPIRED" and sphere["boundaryIntersectsBodyOrSolid"] is False, "The manifested shell had no body/solid intersection; its expiry did not affect the ground or other scene geometry.")

    crossing = final["transaction"]["crossingAttempt"]
    check("state:paid-casts", final["actors"]["C"]["rp"] == 14 and final["actors"]["O"]["rp"] == 35, "C pays 26 RP and O pays 5 RP once; neither payment is refunded.")
    check("state:first-family-protection", final["actors"]["C"]["dissonance"] == 0 and final["actors"]["O"]["dissonance"] == 0 and all(cast["effectiveDissonance"] == 0 and cast["refrain"] == 0 and cast["firstDistinctFamily"] for actor in ("C", "O") for cast in final["actors"][actor]["castingHistory"]), "Both separate first-family casts use only the stated protection; Dissonance and Refrain remain zero.")
    c_prep = final["actors"]["C"]["preparation"]
    check("state:ordinary-preparation", c_prep["status"] == "COMPLETE" and close(c_prep["completionTime"] - c_prep["startTime"], 2700) and len(final["actors"]["C"]["prepared"]) == 24 and "invulnerable-sphere" in final["actors"]["C"]["prepared"], "C completes the source-bound 45-minute 24-entry ordinary preparation with Sphere prepared.")
    check("state:book-access-repack", final["actors"]["C"]["preparationBookAccess"]["status"] == "REPACKED_OFFSCENE" and final["actors"]["C"]["preparationBookAccess"]["carriedIntoEncounter"] is False and final["actors"]["O"]["bookAccess"]["status"] == "REPACKED_IN_KIT" and final["actors"]["O"]["bookAccess"]["weightCountedOnceInAggregate"] is True, "Both source book-access operations and repacks are recorded before paid casts without double-counting cargo.")
    check("state:components-custody", all(cast["componentCustodyAtCast"]["freeSHand"] and cast["componentCustodyAtCast"]["focusAccessible"] and cast["components"] == ["V", "S", "F"] for actor in ("C", "O") for cast in final["actors"][actor]["castingHistory"]) and final["actors"]["C"]["castingHistory"][0]["preparationBookRepackedBeforeCast"] and final["actors"]["O"]["castingHistory"][0]["bookRepackedBeforeCast"], "Each paid cast has exact V/S/F, accessible focus, free somatic hand, custody, and prior book repack recorded.")
    check("state:rider-cargo", final["actors"]["O"]["totalRiderPayload"] == {"weightLb": 170, "load": 7, "limits": {"weightLb": 350, "load": 12}, "withinCapacity": True, "burdened": True, "speedFeet": 50}, "Rider and all declared gear fit the exact capacity and burden calculation.")
    check("state:denial-spend", crossing["status"] == "DENIED_AT_ORIGIN" and crossing["useSpent"] and crossing["actionSpent"] and crossing["translated"] is False and final["actors"]["S1"]["crossingUsesRemaining"] == 0, "S1 spends its Action and sole crossing attempt before the Sphere-caused denial.")
    check("state:origin-custody", crossing["originPoses"] == {"O": [2.5, 0, 6], "S1": [0, 0, 0]} and final["actors"]["O"]["position"] == [7.5, 0, 0] and final["actors"]["O"]["mountedOn"] is None, "The group remains at origin through denial; O later dismounts legally, retaining all gear custody.")
    check("state:original-deadlines", final["scene"]["objects"]["sphere"]["deadline"] == 60.21 and final["actors"]["S1"]["originalDeadline"] == 62.0 and final["actors"]["S1"]["endedTime"] == 62.0, "Sphere and Steed expire at their original independent deadlines.")
    check("state:no-retry-or-corpse", final["transaction"]["automaticRetry"] is False and final["actors"]["S1"]["status"] == "EXPIRED" and final["actors"]["O"]["alive"] is True, "No automatic retry, corpse, loot, deletion, teleport, or additional resource trigger is created.")
    check("state:concentrations-ended", final["actors"]["C"]["concentration"] is None and final["actors"]["O"]["concentration"] is None, "Both original concentration effects close only at their stated endpoints.")

    readme = (OUT / "README.md").read_text(encoding="utf-8")
    review_request = (OUT / "DIRECTOR_REVIEW_REQUEST_423_REPACK01.md").read_text(encoding="utf-8")
    check("scope:status-limits", all(value is False for value in replay["limits"].values()) and "does not accept or apply" in readme, "Packet records no parent/canon/fixture/queue mutation, no acceptance/application, and no seal.")
    check("scope:director-request", "Preserve Queue404 at 829/19/0" in review_request and "Do not accept or apply" in review_request, "Director request explicitly preserves all unrelated authority and holds.")

    audit = {
        "schemaVersion": 1,
        "id": "DF218-B04-WITNESS-423-REPACK01-INDEPENDENT-AUDIT",
        "classification": "INDEPENDENT_TEST_ONLY_EVIDENCE_AND_REPLAY_VALIDATION",
        "status": "PASS_PENDING_GPT_DIRECTOR_READBACK",
        "checkedAtLocalDate": datetime.now().astimezone().date().isoformat(),
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checks": checks,
        "summary": {
            "eventCount": len(events),
            "forwardOperations": replay["replaySummary"]["forwardOperations"],
            "inverseOperations": replay["replaySummary"]["inverseOperations"],
            "eventChainHead": replay["replaySummary"]["eventChainHead"],
            "geometry": {"mountFarthestCornerFeet": round(mount_radius, 6), "riderFarthestCornerFeet": round(rider_radius, 6), "casterNearestPointFeet": round(caster_nearest, 6), "clearInteriorRadiusFeet": inner, "casterToSphereCenterFeet": round(caster_distance, 6)},
            "actualRegularMarkers": {"CStarts": 11, "CEnds": 11, "OStarts": 11, "OEnds": 10, "steedAttachedPhases": 10},
        },
        "authority": {"applied": 829, "pending": 19, "acceptedUnapplied": 0, "acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"], "applicationAuthorized": False},
        "limitations": ["This is a hypothetical TEST_ONLY branch; no campaign/real-play event is claimed.", "The held B4 parent and fixture were not modified or repaired.", "The packet does not accept/apply Sphere or seal the witness; GPT Director readback remains required."],
    }
    write_json(AUDIT_PATH, audit)

    package_files = [
        "README.md",
        "DIRECTOR_REVIEW_REQUEST_423_REPACK01.md",
        "SPHERE_WITNESS_REPLAY_423_REPACK01_TESTONLY.json",
        "OWNER_SPHERE_PREMISES_ADOPTION_422_TESTONLY.json",
        "SPHERE_CANDIDATE_PROPOSAL_421.json",
        "SOURCE_BINDINGS_423.json",
        "DIRECTOR_CORRECTIONS_423_REPACK01.json",
        "INDEPENDENT_AUDIT_423_REPACK01.json",
    ]
    manifest = {"schemaVersion": 1, "id": "DF218-B04-WITNESS-423-REPACK01-MANIFEST", "classification": "TEST_ONLY_DIRECTOR_REVIEW_PACKET", "files": []}
    for name in package_files:
        raw = (OUT / name).read_bytes()
        manifest["files"].append({"path": name, "bytes": len(raw), "sha256": raw_sha(raw)})
    write_json(MANIFEST_PATH, manifest)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in [*package_files, "MANIFEST_423_REPACK01.json"]:
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (OUT / name).read_bytes())
    packet_raw = ZIP_PATH.read_bytes()
    delivery = {
        "schemaVersion": 1,
        "id": "DF218-B04-WITNESS-423-REPACK01-DELIVERY",
        "fileName": ZIP_PATH.name,
        "bytes": len(packet_raw),
        "sha256": raw_sha(packet_raw),
        "crc32": crc32(packet_raw),
        "memberCount": len(package_files) + 1,
        "manifestSha256": raw_sha(MANIFEST_PATH.read_bytes()),
        "eventCount": len(events),
        "forwardOperations": replay["replaySummary"]["forwardOperations"],
        "inverseOperations": replay["replaySummary"]["inverseOperations"],
        "queue": {"applied": 829, "pending": 19, "acceptedUnapplied": 0},
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["invulnerable-sphere"],
        "witnessSealed": False,
        "applicationAuthorized": False,
    }
    write_json(DELIVERY_PATH, delivery)
    print(json.dumps({"status": audit["status"], "checksPassed": len(checks), "eventCount": len(events), "forwardOperations": replay["replaySummary"]["forwardOperations"], "inverseOperations": replay["replaySummary"]["inverseOperations"], "packetBytes": len(packet_raw), "packetSha256": delivery["sha256"], "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
