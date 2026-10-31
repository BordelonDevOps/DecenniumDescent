from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE_ARCHIVE = BASE / "DD_Rank9_UnholyAscendance_Director_Return274.zip"
SOURCE_DELIVERY = BASE / "DD_Rank9_UnholyAscendance_Director_Return274_DELIVERY.json"
OUT = BASE / "rank9_castingcost5_return275_prepared"
ARCHIVE = BASE / "DD_Rank9_UnholyAscendance_Director_Return275.zip"
DELIVERY = BASE / "DD_Rank9_UnholyAscendance_Director_Return275_DELIVERY.json"
AUDIT = BASE / "RANK9_CASTINGCOST5_RETURN275_INDEPENDENT_AUDIT.json"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def dump_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def binding(path: Path, relative: str) -> dict:
    raw = path.read_bytes()
    return {"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def sync_case_version(case: dict) -> None:
    old_id = case["id"]
    new_id = old_id.replace("CASTINGCOST5-274-", "CASTINGCOST5-275-")
    case["id"] = new_id
    case["mainCaseId"] = new_id
    for index, event in enumerate(case["events"], start=1):
        event["id"] = f"{new_id}:{index}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files: dict[str, bytes | dict] = {}
    with zipfile.ZipFile(SOURCE_ARCHIVE) as z:
        for old_name in z.namelist():
            name = old_name.replace("RETURN274", "RETURN275").replace("Return274", "Return275")
            name = name.replace("CASTINGCOST5-274-", "CASTINGCOST5-275-")
            raw = z.read(old_name)
            if old_name.startswith("cases/"):
                case = json.loads(raw.decode("utf-8-sig"))
                sync_case_version(case)
                files[name] = case
            elif old_name.startswith("case-index/"):
                index = json.loads(raw.decode("utf-8-sig"))
                index["id"] = "CC194-B04-RETURN275-CASE-INDEX"
                for row in index["cases"]:
                    row["caseId"] = row["caseId"].replace("CASTINGCOST5-274-", "CASTINGCOST5-275-")
                    row["member"] = row["member"].replace("CASTINGCOST5-274-", "CASTINGCOST5-275-")
                files[name] = index
            elif old_name == "procedures/unholy-ascendance.json":
                procedure = json.loads(raw.decode("utf-8-sig"))
                procedure["reviewVersion"] = "Return275 / exact current source hashes restored"
                procedure["caseIds"] = [x["caseId"] for x in json.loads(z.read("case-index/CC194-B04-RETURN274.json"))["cases"]]
                procedure["caseIds"] = [x.replace("CASTINGCOST5-274-", "CASTINGCOST5-275-") for x in procedure["caseIds"]]
                procedure["caseIndex"] = "case-index/CC194-B04-RETURN275.json"
                procedure["accepted"] = False
                procedure["applied"] = False
                procedure["blockerIds"] = ["CC194-B04"]
                files[name] = procedure
            elif old_name == "SOURCE_BINDING.json":
                files[name] = json.loads(raw.decode("utf-8-sig"))
            elif old_name.endswith(".md") or old_name.endswith(".txt"):
                files[name] = raw
            else:
                files[name] = raw

    source_candidate = json.loads(files["evidence/CURRENT_SOURCE_CONFERENCE_CANDIDATE_270.json"].decode("utf-8-sig"))
    source_rows = source_candidate["sourceBindings"]
    assert len(source_rows) == 117
    actual_hash_failures = []
    for row in source_rows:
        path = ROOT / Path(row["path"])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            actual_hash_failures.append(row["path"])
    assert not actual_hash_failures, json.dumps(actual_hash_failures, indent=2)

    source_binding = files["SOURCE_BINDING.json"]
    source_binding["id"] = "RETURN275-SOURCE-BINDING"
    # Rebind the list directly from the embedded current-source candidate; this
    # avoids any text replacement against hexadecimal SHA-256 values.
    source_binding["current117Bindings"] = copy.deepcopy(source_rows)
    source_binding["notes"] = list(source_binding.get("notes", [])) + [
        "Return274 hold I01-I02 corrected: current117Bindings exactly copy the bound candidate's 117 entries, with all 117 source bytes independently rehashed."
    ]
    files["SOURCE_BINDING.json"] = source_binding

    hold_note = ("# Director Return274 HOLD\n\n"
        "The director confirmed all five Return273 state corrections and identified two incorrect SHA-256 fields in "
        "SOURCE_BINDING.json. Return275 restores /current117Bindings/53/sha256 to "
        "1887160f0f5227383d19b8add6c26faec71e501195c1f2cf17d9e5592bdb9a88 and "
        "/current117Bindings/81/sha256 to 2e9612e80f2f907c4b30afddbcb75e611b57632739d264a84e074483bbb356b6. "
        "Both values match the current-source candidate and the actual workspace bytes. The 11 cases and 51-event replay are unchanged.\n")
    files["evidence/DIRECTOR_RETURN274_HOLD.md"] = hold_note.encode("utf-8")
    files["README.md"] = ("# Return275 - Unholy Ascendance lifecycle witnesses\n\n"
        "Target: unholy-ascendance / CC194-B04 only. Authority remains 815 applied / 33 pending / 0 accepted-unapplied; "
        "539 complete procedures / 173 scoped interfaces.\n\n"
        "Return275 preserves Return274's five director-confirmed state corrections and fixes the two incorrect current-source "
        "SHA-256 entries identified by the director. All 117 bindings are checked against the embedded current-source candidate "
        "and actual workspace bytes. The 11 conditional traces and 51-event replay remain unchanged. No acceptance/application is recorded.\n\n"
        "Please independently verify the source bindings and archive, then issue an explicit ACCEPT or HOLD for unholy-ascendance / "
        "CC194-B04 only. If accepted, leave it unapplied and report authority counts and next priority.\n").encode("utf-8")
    files.pop("REQUEST_274.txt", None)
    files["REQUEST_275.txt"] = ("Return275 is the corrected replacement for held Return274. The archive, delivery manifest, and independent audit are attached. "
        "All five prior state findings are director-confirmed as fixed; this packet changes only SOURCE_BINDING.json to restore the two exact current-source SHA-256 values. "
        "The 117 entries now match the embedded current-source candidate, and every source byte hashes to its declared value. "
        "The 11 cases, 51 events, procedures, and replay states are preserved.\n\n"
        "Please independently verify the package and issue an explicit ACCEPT or HOLD for unholy-ascendance / CC194-B04 only. "
        "If held, give exact remaining pointers. If accepted, confirm accepted=true/applied=false, current authority counts, and next pending identity. "
        "Preserve prior acceptances and do not reopen other identities.\n").encode("utf-8")

    case_values = {name: value for name, value in files.items() if name.startswith("cases/") and isinstance(value, dict)}
    case_index = next(value for name, value in files.items() if name.startswith("case-index/") and isinstance(value, dict))
    procedure = files["procedures/unholy-ascendance.json"]
    assert len(case_values) == 11 and len(case_index["cases"]) == 11
    assert source_binding["current117Bindings"][53]["sha256"] == "1887160f0f5227383d19b8add6c26faec71e501195c1f2cf17d9e5592bdb9a88"
    assert source_binding["current117Bindings"][81]["sha256"] == "2e9612e80f2f907c4b30afddbcb75e611b57632739d264a84e074483bbb356b6"

    for name, value in files.items():
        path = OUT / name
        if isinstance(value, dict):
            dump_json(path, value)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)

    members = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            raw = path.read_bytes()
            members.append({"name": path.relative_to(OUT).as_posix(), "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for member in members:
            z.write(OUT / member["name"], member["name"])
    archive_binding = binding(ARCHIVE, ARCHIVE.relative_to(ROOT).as_posix())
    old_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    authority = {"reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 539, "scopedInterfaces": 173}
    delivery = {"id": "DD_Rank9_UnholyAscendance_Director_Return275_DELIVERY",
        "status": "PREPARED_FOR_DIRECTOR_REVIEW", "archive": archive_binding,
        "memberCount": len(members), "payloadMemberCount": len(members), "members": members,
        "currentSourceDelivery": old_delivery["currentSourceDelivery"], "currentAuthority": authority,
        "spellId": "unholy-ascendance", "blockerIds": ["CC194-B04"], "accepted": False, "applied": False}
    dump_json(DELIVERY, delivery)

    checks = []
    def check(name: str, passed: bool, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
    check("current authority remains 815/33/0 and 539/173", delivery["currentAuthority"] == authority)
    check("proposal remains unaccepted/unapplied", procedure["accepted"] is False and procedure["applied"] is False)
    check("all 117 bindings equal candidate and actual source bytes", len(source_binding["current117Bindings"]) == 117 and source_binding["current117Bindings"] == source_rows and not actual_hash_failures)
    check("director-required hash I01 restored", source_binding["current117Bindings"][53]["sha256"] == "1887160f0f5227383d19b8add6c26faec71e501195c1f2cf17d9e5592bdb9a88")
    check("director-required hash I02 restored", source_binding["current117Bindings"][81]["sha256"] == "2e9612e80f2f907c4b30afddbcb75e611b57632739d264a84e074483bbb356b6")
    check("case identity and event counts preserved", len(case_values) == 11 and sum(len(c["events"]) for c in case_values.values()) == 51)
    for member, case in case_values.items():
        state = copy.deepcopy(case["initialState"])
        for i, event in enumerate(case["events"], start=1):
            good = event["before"] == state and sha(state) == event["beforeSHA256"] and sha(event["after"]) == event["afterSHA256"]
            good = good and event["id"] == f"{case['id']}:{i}"
            good = good and event["forward"] == [{"op": "test", "path": "", "value": state}, {"op": "replace", "path": "", "value": event["after"]}]
            good = good and event["inverse"] == [{"op": "test", "path": "", "value": event["after"]}, {"op": "replace", "path": "", "value": state}]
            check(f"{case['id']} event {i} forward/inverse and ID", good)
            state = copy.deepcopy(event["after"])
        check(f"{case['id']} final state", state == case["finalState"] and sha(state) == case["finalSHA256"])
    check("package member allowlist matches manifest", len(members) == delivery["memberCount"])
    with zipfile.ZipFile(ARCHIVE) as z:
        names = sorted(z.namelist())
        check("ZIP names equal delivery member list", names == sorted(x["name"] for x in members))
        for member in members:
            raw = z.read(member["name"])
            check(f"member binding {member['name']}", hashlib.sha256(raw).hexdigest() == member["sha256"] and f"{zlib.crc32(raw) & 0xffffffff:08x}" == member["crc32"])
    failures = [x for x in checks if not x["passed"]]
    audit = {"id": "RANK9_CASTINGCOST5_RETURN275_INDEPENDENT_AUDIT",
        "status": "PASS_PACKAGE_BINDING_AND_REPLAY" if not failures else "FAIL",
        "checkCount": len(checks), "checksPassed": len(checks) - len(failures), "checksFailed": len(failures),
        "checks": checks, "failures": failures, "archive": archive_binding, "caseCount": len(case_values),
        "eventCount": sum(len(c["events"]) for c in case_values.values()),
        "forwardInverseOperationCount": 2 * sum(len(c["events"]) for c in case_values.values()),
        "sourceBindingCount": 117, "authority": authority, "acceptedIds": [], "appliedIds": [],
        "heldIds": ["unholy-ascendance"]}
    dump_json(AUDIT, audit)
    assert not failures, json.dumps(failures, indent=2)
    print(json.dumps({"status": audit["status"], "checkCount": audit["checkCount"],
        "caseCount": audit["caseCount"], "eventCount": audit["eventCount"], "sourceBindingCount": 117,
        "archive": archive_binding}, indent=2))


if __name__ == "__main__":
    main()
