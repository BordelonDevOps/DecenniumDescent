from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zlib
from datetime import datetime, timezone
from zipfile import ZipFile
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
RETURN318 = AUDIT / "rank9_time_stop_return318_received"
PACKET = AUDIT / "rank9_time_stop_joint_witness_344_delivery"
ARCHIVE = PACKET / "DD_Rank9_TimeStop_TF318_Witness344.zip"
DELIVERY = PACKET / "DD_Rank9_TimeStop_TF318_Witness344_DELIVERY.json"
REPORT = PACKET / "TIME_STOP_TF318_WITNESS344_INDEPENDENT_REVIEW.json"
SOURCE_PATHS = {
    "catalog": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "index": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "core": ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "spells": ROOT / "DescentReviewChanges/ReviewBible/src/data/spells.js",
    "placements": ROOT / "DescentReviewChanges/ReviewBible/src/data/spell-placements.json",
    "wizard": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json",
    "cleric": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
    "integration": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "ancestry_background": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
}
ARCHIVE_SOURCE_NAMES = {
    "catalog": "evidence/sources/catalog.json",
    "index": "evidence/sources/authored_review_index.json",
    "core": "evidence/sources/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "spells": "evidence/sources/spells.js",
    "placements": "evidence/sources/spell-placements.json",
    "wizard": "evidence/sources/class_playtests/wizard.json",
    "cleric": "evidence/sources/class_playtests/cleric.json",
    "integration": "evidence/sources/SPELL_INTEGRATION_RULES.md",
    "ancestry_background": "evidence/sources/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def apply_ops(state: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(state)
    for operation in operations:
        if operation.get("path") != "":
            raise ValueError("unsupported JSON-patch path")
        if operation["op"] == "test":
            if canonical(result) != canonical(operation["value"]):
                raise ValueError("state test precondition failed")
        elif operation["op"] == "replace":
            result = copy.deepcopy(operation["value"])
        else:
            raise ValueError(f"unknown operation: {operation['op']}")
    return result


def replay_and_reverse(case: dict[str, Any]) -> dict[str, Any]:
    state = copy.deepcopy(case["initialState"])
    for event in case["events"]:
        if canonical(state) != canonical(event["before"]):
            raise ValueError(f"{event['id']}: broken event continuity")
        if sha(canonical(event["before"])) != event["beforeSHA256"] or sha(canonical(event["after"])) != event["afterSHA256"]:
            raise ValueError(f"{event['id']}: state hash mismatch")
        state = apply_ops(state, event["forward"])
        if canonical(state) != canonical(event["after"]):
            raise ValueError(f"{event['id']}: forward replay mismatch")
        if canonical(apply_ops(state, event["inverse"])) != canonical(event["before"]):
            raise ValueError(f"{event['id']}: inverse replay mismatch")
    if canonical(state) != canonical(case["finalState"]):
        raise ValueError(f"{case['id']}: final state mismatch")
    state = copy.deepcopy(case["finalState"])
    for event in reversed(case["events"]):
        state = apply_ops(state, event["inverse"])
    if canonical(state) != canonical(case["initialState"]):
        raise ValueError(f"{case['id']}: complete reverse chain did not reach initial state")
    return {"caseId": case["id"], "eventCount": len(case["events"]), "forwardInverseReplayed": True}


def check_case(case: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    replay = replay_and_reverse(case)
    initial, final = case["initialState"], case["finalState"]
    if initial.get("fixtureMode") != "AUTHORED_CONDITIONAL_REVIEW_FIXTURE_ONLY" or initial.get("campaignEvent") is not False:
        raise ValueError(f"{case['id']}: fixture provenance is not explicitly conditional")
    if final["world"]["paused"] or final["world"]["temporalInterval"] is not None:
        raise ValueError(f"{case['id']}: interval remains open at final state")
    for actor_id in ("C", "P"):
        actor = initial["actors"][actor_id]
        if actor["classLevel"] != 17 or actor["life"] != "alive" or actor["maxHP"] <= 0:
            raise ValueError(f"{case['id']}: incomplete or ineligible fixture actor {actor_id}")
        if actor["candidateSpellAcquisitions"][0]["status"].find("candidate-only") < 0:
            raise ValueError(f"{case['id']}: pending spell acquisition is not marked candidate-only")

    spells = {row["id"]: row for row in catalog["spells"]}
    for identity, actor_id in (("time-stop", "C"), ("timeless-form", "P")):
        actor = initial["actors"][actor_id]
        access = spells[identity]["classAccess"][actor["class"]]
        if access["rank"] != 9 or access["minimumClassLevel"] > actor["classLevel"]:
            raise ValueError(f"{case['id']}: illegal source access for {identity}")
    casts = {row["id"]: row for row in final["casts"]}
    ts_cast = casts[case["id"] + "-TS"]
    tf_cast = casts[case["id"] + "-TF"]
    if ts_cast["actualPaid"] != 26 or tf_cast["actualPaid"] != 26:
        raise ValueError(f"{case['id']}: candidate rank-9 cast did not pay 26 RP")
    if "V" not in ts_cast["components"] or "S" not in ts_cast["components"] or "F" not in ts_cast["components"]:
        raise ValueError(f"{case['id']}: Time Stop component record incomplete")

    stop = final["effects"].get("time-stop", {})
    form = final["effects"].get("timeless-form-P", {})
    if stop.get("status", "").startswith("ended-by-successful"):
        pass
    elif stop.get("status") != "naturally-completed-after-final-peer-end":
        raise ValueError(f"{case['id']}: Time Stop ended-source record missing")
    if form.get("originalDeadlineWorldMs") != 60000 or form.get("expiredAtWorldMs") != 60000 or form.get("status") != "expired-before-any-later-payload":
        raise ValueError(f"{case['id']}: Timeless Form deadline was reset, lost or misprocessed")
    opened = next(event for event in case["events"] if event["kind"] == "TIME_STOP_OPEN")
    anchor = opened["after"]["world"]["temporalInterval"]["worldAnchorMs"]
    for event in case["events"]:
        if event["kind"] in ("PERSONAL_PHASE_START", "PERSONAL_PHASE_END", "IMMUNE_PEER_MOVEMENT"):
            clock = event["after"]["clockLedger"][-1]
            if clock.get("worldTimeMs") != anchor:
                raise ValueError(f"{case['id']}: personal turn incorrectly advances world time")

    if case["branch"].startswith("natural"):
        close = next(event for event in case["events"] if event["kind"] == "TIME_STOP_NATURAL_CLOSE")
        preceding = case["events"][case["events"].index(close) - 1]
        if preceding["kind"] != "PERSONAL_PHASE_END" or preceding["inputs"].get("actor") != "P":
            raise ValueError(f"{case['id']}: natural completion did not wait for final peer END")
        if close["after"]["effects"]["time-stop"].get("status") != "naturally-completed-after-final-peer-end":
            raise ValueError(f"{case['id']}: natural close status mismatch")
    else:
        checks = [event for event in case["events"] if event["kind"] == "PAID_ARCH_DISPEL_CHECK"]
        if [event["inputs"]["expected"] for event in checks] != ["failure", "success"]:
            raise ValueError(f"{case['id']}: expected one failed and one successful Dispel")
        failed, succeeded = checks
        if failed["after"]["world"]["temporalInterval"] is None:
            raise ValueError(f"{case['id']}: failed Dispel ended the interval")
        recharge = failed["after"]["actors"]["P"]["recharge"]["wizard.arch.dispel-magic"]
        if recharge["roundsRemaining"] != 2 or recharge["ticksDuringPersonalTurns"] != 0:
            raise ValueError(f"{case['id']}: failed Dispel did not retain Recharge2")
        if succeeded["after"]["world"]["temporalInterval"] is not None or succeeded["after"]["actors"]["C"].get("currentTemporalPhase") is not None:
            raise ValueError(f"{case['id']}: successful Dispel did not terminate and clean up mid-phase")
    return {**replay, "branch": case["branch"], "worldAnchorMs": anchor, "sourceDeadlineMs": form["originalDeadlineWorldMs"]}


def main() -> None:
    for path in SOURCE_PATHS.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8"))
    archive_raw = ARCHIVE.read_bytes()
    if sha(archive_raw) != delivery["archive"]["sha256"] or len(archive_raw) != delivery["archive"]["bytes"]:
        raise ValueError("delivery archive binding mismatch")
    if zlib.crc32(archive_raw) & 0xFFFFFFFF != int(delivery["archive"]["crc32"], 16):
        raise ValueError("delivery archive CRC mismatch")

    with ZipFile(ARCHIVE) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        allowlist = set(manifest["exactPayloadAllowlist"])
        if names - {"MEMBER_MANIFEST.json"} != allowlist:
            raise ValueError("ZIP contents do not exactly match the manifest allowlist")
        if len(names) != manifest["memberCount"] or manifest["payloadMemberCount"] != len(names) - 1:
            raise ValueError("ZIP manifest member counts mismatch")
        for row in manifest["members"]:
            raw = archive.read(row["path"])
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" != row["crc32"]:
                raise ValueError(f"ZIP member binding mismatch: {row['path']}")
        for key, path in SOURCE_PATHS.items():
            if archive.read(ARCHIVE_SOURCE_NAMES[key]) != path.read_bytes():
                raise ValueError(f"current-source copy mismatch: {key}")
        old_paths = sorted((RETURN318 / "cases").glob("*.json"))
        if len(old_paths) != 14:
            raise ValueError(f"expected 14 preserved historical cases, found {len(old_paths)}")
        for path in old_paths:
            if archive.read("cases/preserved/" + path.name) != path.read_bytes():
                raise ValueError(f"historical case was not preserved byte-exact: {path.name}")
        catalog = json.loads(archive.read(ARCHIVE_SOURCE_NAMES["catalog"]))
        cases = [json.loads(archive.read(name)) for name in sorted(names) if name.startswith("cases/new/")]
        if len(cases) != 3:
            raise ValueError(f"expected three new conditional cases, found {len(cases)}")
        case_reports = [check_case(case, catalog) for case in cases]

    report = {
        "id": "TIME-STOP-TF318-WITNESS344-INDEPENDENT-REVIEW",
        "status": "PASS",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archiveSha256": sha(archive_raw),
        "zipMemberCount": len(names),
        "exactPayloadAllowlistPassed": True,
        "currentSourceByteBindingsPassed": len(SOURCE_PATHS),
        "preservedHistoricalCasesByteExact": 14,
        "caseReplaysAndFullReversePassed": case_reports,
        "applicationPerformed": False,
        "runtimeExecuted": False,
        "humanPlayExecuted": False,
        "directorAcceptanceClaimed": False,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
