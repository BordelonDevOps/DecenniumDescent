from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
BASE_COMMIT = "cf0ea55dcbb781af4bae548513999c88daf022de"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def pointer_value(root: object, pointer: str) -> object:
    value = root
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def bounds(box: dict | list) -> list[float]:
    if isinstance(box, list):
        return box
    return [box[axis][i] for axis in ("x", "y", "z") for i in (0, 1)]


def overlap(a: list[float], b: list[float]) -> bool:
    return all(min(a[i + 1], b[i + 1]) > max(a[i], b[i]) for i in (0, 2, 4))


def segment_hits(a: list[float], b: list[float], box: list[float]) -> bool:
    t0, t1 = 0.0, 1.0
    for axis, (lo, hi) in enumerate(((box[0], box[1]), (box[2], box[3]), (box[4], box[5]))):
        delta = b[axis] - a[axis]
        if abs(delta) < 1e-12:
            if not lo < a[axis] < hi:
                return False
        else:
            u, v = (lo - a[axis]) / delta, (hi - a[axis]) / delta
            enter, leave = sorted((u, v))
            t0, t1 = max(t0, enter), min(t1, leave)
            if t0 >= t1:
                return False
    return t1 > max(t0, 0.0) and t0 < 1.0


def main() -> None:
    proposal_path = OUT / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.json"
    markdown_path = OUT / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.md"
    correction_path = OUT / "PG328_W13_DIRECTOR_CORRECTIONS_447.json"
    validation_path = OUT / "BUILD_VALIDATION_447.json"
    manifest_path = OUT / "MANIFEST_447.json"
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    inputs = proposal["ownerProposedInputs"]

    assert subprocess.check_output(["git", "rev-parse", BASE_COMMIT], cwd=REPO, text=True).strip() == BASE_COMMIT
    assert proposal["readAtCommit"] == BASE_COMMIT
    assert sha(proposal_path) == validation["proposalFileSha256"]
    assert sha(markdown_path) == validation["markdownFileSha256"]
    assert sha(correction_path) == validation["correctionRecordSha256"]
    assert validation["status"] == "PASS" and all(check["pass"] for check in validation["checks"])
    assert proposal["queueAtProposal"] == {"applied": 830, "pending": 18, "acceptedUnapplied": 0, "acceptedIds": ["invulnerable-sphere"], "appliedIds": ["invulnerable-sphere"], "mutated": False}

    source_rows = []
    for binding in proposal["sourceBindings"]:
        blob = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{binding['path']}"], cwd=REPO)
        blob_sha1 = subprocess.check_output(["git", "rev-parse", f"{BASE_COMMIT}:{binding['path']}"], cwd=REPO, text=True).strip()
        assert len(blob) == binding["bytes"] and sha_bytes(blob) == binding["sha256"] and blob_sha1 == binding["gitBlobSha1"]
        source_json = json.loads(blob.decode("utf-8")) if binding.get("jsonPointers") else None
        for pointer in binding.get("jsonPointers", []):
            pointer_value(source_json, pointer)
        source_rows.append(binding["path"])
    assert len(source_rows) == validation["sourceCount"] == 17

    geometry_path = REPO / inputs["geometryAudit"]["sourcePath"]
    geometry = json.loads(geometry_path.read_text(encoding="utf-8"))
    obstacles = []
    for panel in geometry["panels"]:
        obstacles.extend(bounds(box) for box in panel.get("occupiedFragments", []))
    for door in geometry["doorLeaves"]:
        obstacles.extend(bounds(box) for box in door.get("occupiedFragments", []))

    def swept(start: list[float], end: list[float], size: list[float] = [5, 5, 6]) -> list[float]:
        return [min(start[0], end[0]), max(start[0], end[0]) + size[0], min(start[1], end[1]), max(start[1], end[1]) + size[1], 0, size[2]]

    movement = inputs["parentDispel"]["approachMovement"]
    a_start = movement["from"]
    a_stops = [leg["to"] for leg in movement["route"]]
    b_legs = inputs["childEntry"]["route"][:3]
    route_segments = [(a_start, a_stops[0]), (a_stops[0], a_stops[1])] + [(leg["from"], leg["to"]) for leg in b_legs]
    assert len(route_segments) == 5
    assert all(not any(overlap(swept(start, end), obstacle) for obstacle in obstacles) for start, end in route_segments)

    sight = inputs["AArcaneSight"]
    child_dispel = inputs["childDispel"]
    parent_dispel = inputs["parentDispel"]
    rays = [(sight["casterCenter"], sight["targetAuraPoint"]), (parent_dispel["casterCenter"], parent_dispel["targetAuraPoint"]), (child_dispel["casterCenter"], child_dispel["targetInteriorPoint"])]
    assert all(not any(segment_hits(start, end, obstacle) for obstacle in obstacles) for start, end in rays)
    assert sight["observationReceipt"]["derivedFromW12Observation"] is False
    assert sight["observationReceipt"]["effectId"] == parent_dispel["targetEffect"]

    arrival = inputs["childEntry"]
    assert arrival["totalMovementFeet"] == 25 and arrival["route"][-1]["arrival"] == [0, 15, 0]
    assert arrival["bodyBoundsInChild"] == {"x": [0, 5], "y": [15, 20], "z": [0, 6]}
    assert inputs["childTerminalSettlement"]["cargoBParentPosition"] == [40, 15, 0]
    cargo_support = {"x": [40, 41], "y": [15, 16], "z": [0, 0]}
    assert inputs["childTerminalSettlement"]["cargoBParentSupport"]["bounds"] == cargo_support
    assert any(support["supports"] == "cargo-B only" and support["bounds"] == cargo_support for support in inputs["rootTerminalClosure"]["supportPatches"])

    ledger = inputs["resourceLedger"]
    assert ledger["A"]["startRP"] - ledger["A"]["arcaneSightCost"] - ledger["A"]["parentDispelCost"] == ledger["A"]["terminalRP"] == 48
    assert ledger["B"]["startRP"] - ledger["B"]["childDemiplaneCost"] - ledger["B"]["childDispelCost"] == ledger["B"]["terminalRP"] == 56
    assert inputs["rootTerminalClosure"]["geometryPairsCheckedAtExterior"] == 15
    assert proposal["classification"].endswith("NOT_A_WITNESS")
    assert validation["noWitnessConstructed"] and validation["noSealAcceptanceApplicationOrQueueChange"]

    listed = {item["path"]: item for item in manifest["artifacts"]}
    expected_files = [proposal_path, markdown_path, correction_path, validation_path, OUT / "VERIFY_W13_PROPOSAL_447.py"]
    assert set(listed) == {path.name for path in expected_files}
    for path in expected_files:
        item = listed[path.name]
        assert item["bytes"] == path.stat().st_size and item["sha256"] == sha(path)

    print("PASS: 17 source blobs/pointers, 5 body sweeps, 3 rays, child aperture/cargo support, RP/cadence scope, queue invariance, and 5 manifest artifacts.")


if __name__ == "__main__":
    main()
