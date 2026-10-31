from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FORGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/SUPPLEMENT255_W2.json"
SOURCE_ARCHIVE = AUDIT / "rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_HELD.zip"
SOURCE_MEMBER = "cases/MF210-F02.json"
TARGET_PRE_EVENT = "MF247-F-W2-E20-PAID-GREATER-DISPEL"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_sha(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def pointer_parts(path: str) -> list[str]:
    if path == "":
        return []
    if not path.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {path}")
    return [part.replace("~1", "/").replace("~0", "~") for part in path[1:].split("/")]


def parent_at(document: object, parts: list[str]) -> tuple[object, str]:
    if not parts:
        raise ValueError("root pointer is handled separately")
    node = document
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, parts[-1]


def get_at(document: object, parts: list[str]) -> object:
    node = document
    for part in parts:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def apply_ops(document: object, operations: list[dict]) -> object:
    for operation in operations:
        op = operation["op"]
        parts = pointer_parts(operation["path"])
        if op == "test":
            assert get_at(document, parts) == operation["value"], operation["path"]
            continue
        if not parts:
            if op != "replace":
                raise ValueError(f"unsupported root operation: {op}")
            document = copy.deepcopy(operation["value"])
            continue
        parent, key = parent_at(document, parts)
        if op == "replace":
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                parent[key] = copy.deepcopy(operation["value"])
        elif op == "add":
            if isinstance(parent, list):
                parent.insert(len(parent) if key == "-" else int(key), copy.deepcopy(operation["value"]))
            else:
                parent[key] = copy.deepcopy(operation["value"])
        elif op == "remove":
            if isinstance(parent, list):
                parent.pop(int(key))
            else:
                del parent[key]
        else:
            raise ValueError(f"unsupported JSON Patch operation: {op}")
    return document


def main() -> None:
    supplement = json.loads(FORGE.read_text(encoding="utf-8"))
    branch = supplement["eventReplay"]["branches"][0]
    events = branch["events"]
    target_index = next(i for i, event in enumerate(events) if event["id"] == TARGET_PRE_EVENT)
    assert target_index == 19, target_index

    with zipfile.ZipFile(SOURCE_ARCHIVE) as archive:
        source_case = json.loads(archive.read(SOURCE_MEMBER))
    source_base = copy.deepcopy(source_case["events"][-1]["after"])
    base_hash = state_sha(source_base)
    assert source_case["events"][-1]["id"] == "MF210-F02:6"
    assert base_hash == supplement["priorCase"]["endSnapshotSHA256"]
    assert base_hash == supplement["eventReplay"]["baseStateSHA256"]

    state = copy.deepcopy(source_base)
    replayed = []
    for event in events[:target_index]:
        assert state_sha(state) == event["beforeSHA256"], event["id"]
        state = apply_ops(state, event["forward"])
        assert state_sha(state) == event["afterSHA256"], event["id"]
        replayed.append({"id": event["id"], "kind": event["kind"], "stateSHA256": event["afterSHA256"]})

    e20 = events[target_index]
    assert e20["id"] == TARGET_PRE_EVENT
    assert state_sha(state) == e20["beforeSHA256"]
    assert state["time"] == e20["timeStartSeconds"] == 172800.4
    item = state["items"]["bracelet-1"]
    root = item["imprintRoot"]
    assert root["id"] == "castF2" and root["active"] is True
    assert item["charges"] == 0 and item["HP"] == 2

    embedded = supplement["priorCase"]["endState"]
    def first_diff(left: object, right: object, path: str = "") -> list[str]:
        if type(left) is not type(right):
            return [path or "/"]
        if isinstance(left, dict):
            for key in sorted(left.keys() | right.keys()):
                if key not in left or key not in right:
                    return [f"{path}/{key}"]
                diff = first_diff(left[key], right[key], f"{path}/{key}")
                if diff:
                    return diff
        elif isinstance(left, list):
            if len(left) != len(right):
                return [f"{path}/length"]
            for index, (a, b) in enumerate(zip(left, right)):
                diff = first_diff(a, b, f"{path}/{index}")
                if diff:
                    return diff
        elif left != right:
            return [path or "/"]
        return []

    source_difference = first_diff(source_base, embedded)
    assert source_difference == []
    report = {
        "id": "NULLIFICATION-WAVE-FORGE-BRANCH-REPLAY-355",
        "status": "PASS_EXACT_SOURCE_ARCHIVE_REPLAY_TO_PRE_E20_SNAPSHOT",
        "sourceArchive": SOURCE_ARCHIVE.relative_to(ROOT).as_posix(),
        "sourceMember": SOURCE_MEMBER,
        "supplement": FORGE.relative_to(ROOT).as_posix(),
        "baseEventId": source_case["events"][-1]["id"],
        "baseSnapshotSHA256": base_hash,
        "supplementEmbeddedBaseSHA256": state_sha(embedded),
        "embeddedBaseDiffersFromBoundArchiveAt": source_difference,
        "archiveVsEmbeddedBaseEqual": source_base == embedded,
        "embeddedBaseDifferenceDisposition": "The exact Return247 archive state and supplement-embedded state match under the canonical parsed-state hash; replay begins from the exact archived case state.",
        "replayedPriorEvents": replayed,
        "replayEventCount": len(replayed),
        "preE20Snapshot": {
            "eventId": e20["id"],
            "timeSeconds": state["time"],
            "stateSHA256": state_sha(state),
            "activeRootId": root["id"],
            "rootActive": root["active"],
            "itemId": item["id"],
            "itemHP": item["HP"],
            "itemCharges": item["charges"],
            "custodian": item["custodian"],
            "owner": item["owner"],
            "sourceLineage": root.get("sourceLineage"),
        },
        "preE20SnapshotState": state,
        "replayValidatedBeforeWaveConstruction": True,
        "waveCastOrTargetMutationPerformed": False,
    }
    out = AUDIT / "NULLIFICATION_WAVE_FORGE_BRANCH_REPLAY_355.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "replayEventCount": report["replayEventCount"],
        "preE20Snapshot": report["preE20Snapshot"],
        "actorPositions": {key: value.get("positionFeet") for key, value in state["actors"].items()},
        "item": {key: item.get(key) for key in ["id", "positionBoxFeet", "HP", "charges", "owner", "custodian", "worn", "imprintRoot"]},
        "scene": state.get("scene"),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
