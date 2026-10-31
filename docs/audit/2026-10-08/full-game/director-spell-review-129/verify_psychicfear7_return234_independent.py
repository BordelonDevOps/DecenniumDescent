#!/usr/bin/env python3
"""Independent packaging and decision audit of Director Return234."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_psychicfear7_return234_received"
ARCHIVE = RECEIVED / "DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_PsychicFear3_Director_Return234_HELD_DELIVERY.json"
SOURCE = BASE / "rank9_psychicfear7_current_source_234_prepared/DD_Rank9_PsychicFear7_CurrentSource_234.zip"
REPORT = BASE / "RANK9PSYCHICFEAR7_RETURN234_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"

EXPECTED_AUTHORITY = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
BLOCKERS = {
    "psychic-scream": ["PF182-B01"],
    "mass-phantom-killer": ["PF182-B02"],
    "weird": ["PF182-B02"],
}
checks: list[dict] = []


def digest(data: bytes) -> dict:
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}",
    }


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def matches(data: bytes, record: dict) -> bool:
    got = digest(data)
    return (
        isinstance(record, dict)
        and all(got.get(k) == record.get(k) for k in ("bytes", "sha256"))
        and (record.get("crc32") is None or got["crc32"] == record["crc32"])
    )


def safe_path(name: str) -> bool:
    path = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in path.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_hash = digest(archive_bytes)
delivery_hash = digest(DELIVERY.read_bytes())
check("delivery identity and archive bytes/SHA-256/CRC32 match", delivery.get("id") == "RANK9-PSYCHIC-FEAR3-DIRECTOR-RETURN234-DELIVERY" and matches(archive_bytes, delivery.get("archive", {})) and delivery.get("archive", {}).get("fileName") == ARCHIVE.name, {"actual": archive_hash, "expected": delivery.get("archive")})
check("delivery carries exact current source archive binding", delivery.get("sourceArchive", {}).get("fileName") == SOURCE.name and matches(SOURCE.read_bytes(), delivery.get("sourceArchive", {})), {"actual": digest(SOURCE.read_bytes()), "expected": delivery.get("sourceArchive")})
check("delivery authority remains 811/37/0", delivery.get("authority") == EXPECTED_AUTHORITY, delivery.get("authority"))
check("delivery holds exactly the three submitted identities", delivery.get("heldIds") == TARGETS and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("accepted") is False and delivery.get("applied") is False, {k: delivery.get(k) for k in ("heldIds", "acceptedIds", "appliedIds", "accepted", "applied")})

with zipfile.ZipFile(ARCHIVE) as outer:
    infos = outer.infolist()
    names = [item.filename for item in infos]
    name_set = set(names)
    corrupt_member = outer.testzip()
    check("ZIP CRC test passes", corrupt_member is None, corrupt_member)
    check("archive members are unique, safe regular paths", len(names) == len(name_set) and all(safe_path(n) for n in names) and all(not item.is_dir() for item in infos), {"members": len(names), "unique": len(name_set), "unsafe": [n for n in names if not safe_path(n)][:10]})
    listed = delivery.get("members", [])
    by_path = {item.get("path"): item for item in listed if isinstance(item, dict)}
    allowlist = delivery.get("exactAllowlist", [])
    check("external allowlist exactly matches archive members", len(by_path) == len(listed) == delivery.get("memberCount") == len(names) and set(by_path) == name_set and set(allowlist) == name_set and len(allowlist) == len(names), {"archive": len(names), "listed": len(listed), "memberCount": delivery.get("memberCount"), "allowlistCount": len(allowlist)})
    member_failures = [n for n in names if n not in by_path or not matches(outer.read(n), by_path[n])]
    check("every archive member matches exact external byte/hash/CRC binding", not member_failures, member_failures[:15])
    manifest_bytes = outer.read("MEMBER_MANIFEST.json")
    manifest = read_json(manifest_bytes)
    check("embedded manifest matches external binding", matches(manifest_bytes, delivery.get("memberManifest", {})) and delivery.get("memberManifest", {}).get("path") == "MEMBER_MANIFEST.json", digest(manifest_bytes))
    manifest_members = manifest.get("members", [])
    manifest_by_path = {item.get("path"): item for item in manifest_members if isinstance(item, dict)}
    check("embedded manifest covers every non-manifest member exactly", set(manifest_by_path) == name_set - {"MEMBER_MANIFEST.json"} and len(manifest_by_path) == len(manifest_members) == delivery.get("payloadCount"), {"listed": len(manifest_by_path), "payloadCount": delivery.get("payloadCount"), "archivePayload": len(name_set) - 1})
    internal_failures = [n for n, record in manifest_by_path.items() if n not in name_set or not matches(outer.read(n), record)]
    check("every payload member matches embedded byte/hash/CRC binding", not internal_failures, internal_failures[:15])

    def obj(name: str):
        return read_json(outer.read(name))

    decision = obj("DIRECTOR_DECISION.json")
    authority = obj("CURRENT_AUTHORITY.json")
    counts = obj("COUNTS.json")
    next_group = obj("NEXT_GROUP.json")
    recover = obj("CASE_RECOVERY_BINDINGS.json")
    cases = obj("CASE_RESULTS_234.json")
    clock = obj("CLOCK_CHECK_234.json")
    replay = obj("FORWARD_INVERSE_CHECK_234.json")
    source_verification = obj("SOURCE_VERIFICATION.json")
    preseal = obj("PRESEAL_CHECK.json")
    hold = obj("HOLD_REGISTER_CURRENT.json")

    check("sealed decision authority and target IDs are exact", decision.get("authority") == EXPECTED_AUTHORITY and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("heldIds") == TARGETS and authority.get("targetIds") == TARGETS and authority.get("authority") == EXPECTED_AUTHORITY and authority.get("acceptedIds") == [] and authority.get("appliedIds") == [], {"decision": decision.get("heldIds"), "authority": authority})
    per_identity = decision.get("perIdentityDecisions", [])
    check("all per-identity decisions are held with the reported blockers and witnesses", len(per_identity) == 3 and {item.get("id") for item in per_identity} == set(TARGETS) and all(item.get("decision") == "HELD" and item.get("held") is True and item.get("accepted") is False and item.get("applied") is False and item.get("blockerIds") == BLOCKERS[item["id"]] and bool(item.get("minimumMissingWitness")) for item in per_identity), [{k: item.get(k) for k in ("id", "decision", "blockerIds", "minimumMissingWitness")} for item in per_identity])
    check("no canonical, GitHub, application, supplied-program or runtime changes", decision.get("accepted") is False and decision.get("applied") is False and decision.get("canonicalChanges") is False and decision.get("githubChanges") is False and decision.get("suppliedProgramsExecuted") is False and decision.get("runtimeExecuted") is False and delivery.get("canonicalChanges") is False and delivery.get("githubChanges") is False and delivery.get("sourceProgramsExecuted") is False and delivery.get("runtimeExecuted") is False, {k: decision.get(k) for k in ("canonicalChanges", "githubChanges", "suppliedProgramsExecuted", "runtimeExecuted")})
    check("preserved evidence totals reconcile to 47 cases, 2,464 events and clean calendar checks", counts.get("caseRecordsPreserved") == 47 and counts.get("completeConditionalCases") == 43 and counts.get("heldCases") == 4 and counts.get("eventsReplayed") == 2464 and counts.get("eventForwardOperations") == 4928 and counts.get("eventInverseOperations") == 4928 and counts.get("proposalOperations") == 12 and len(cases) == 47 and all(item.get("passed") is True for item in cases) and clock.get("checkCount") == 183 and clock.get("passed") == 183 and clock.get("failed") == 0 and all(item.get("passed") is True for item in clock.get("checks", [])), {k: counts.get(k) for k in ("caseRecordsPreserved", "completeConditionalCases", "heldCases", "eventsReplayed", "eventForwardOperations", "eventInverseOperations", "proposalOperations")})
    check("forward/inverse replay checks pass without changing accepted/applied authority", isinstance(replay, dict) and replay.get("failed") == 0 and authority.get("canonicalChanges") is False, {k: replay.get(k) for k in ("checkCount", "passed", "failed", "forwardOperations", "inverseOperations") if isinstance(replay, dict)})
    recovered = recover.get("cases", [])
    check("Return216/Return183 recovery is byte-exact for all 47 preserved cases", recover.get("status") == "RECOVERED_BYTE_EXACT" and recover.get("caseCount") == 47 and len(recovered) == 47 and recover.get("sourcePacket", {}).get("sha256") == delivery.get("sourceArchive", {}).get("sha256"), {"status": recover.get("status"), "caseCount": recover.get("caseCount"), "listed": len(recovered)})
    check("all source and preseal verification totals report zero failures", source_verification.get("failed") == 0 and source_verification.get("passed") == source_verification.get("checkCount") and delivery.get("packageChecks", {}).get("failed") == 0 and delivery.get("packageChecks", {}).get("passed") == delivery.get("packageChecks", {}).get("count") == 1471 and all(x.get("passed") is True for x in preseal.get("checks", [])), {"source": {k: source_verification.get(k) for k in ("checkCount", "passed", "failed")}, "package": {k: delivery.get("packageChecks", {}).get(k) for k in ("count", "passed", "failed")}, "preseal": {k: preseal.get(k) for k in ("checkCount", "passed", "failed")}})
    expected_next = {"group": "rank9-death-recovery7", "pendingIds": ["final-word"]}
    check("director points to final-word as the sole next pending Death/Recovery identity", all(next_group.get(k) == v for k, v in expected_next.items()) and next_group.get("reviewStarted") is False and next_group.get("requiresFreshCurrentAuthorityPacket") is True and delivery.get("nextPendingGroup") == next_group, next_group)
    queue_binding = next_group.get("queueBinding", {})
    queue_path = ROOT / queue_binding.get("path", "")
    queue_in_archive = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_234.json"
    handoff_in_archive = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_234.json"
    pending_in_archive = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_234.json"
    queue_member_bytes = outer.read(queue_in_archive) if queue_in_archive in name_set else b""
    queue_ok = queue_in_archive in name_set and matches(queue_member_bytes, queue_binding) and json.loads(queue_member_bytes).get("currentAuthority") == EXPECTED_AUTHORITY
    check("next-group binding matches the packet's embedded pre-submission queue snapshot", queue_path.name == "CURRENT_SPELL_QUEUE_234.json" and queue_ok, {"embeddedDigest": digest(queue_member_bytes), "expectedBinding": queue_binding})
    check("embedded current queue, handoff and pending audit are present", all(p in name_set for p in (queue_in_archive, handoff_in_archive, pending_in_archive)), [p for p in (queue_in_archive, handoff_in_archive, pending_in_archive) if p not in name_set])
    local_queue = read_json(queue_path.read_bytes()) if queue_path.exists() else {}
    check("newer local queue records Packet234 submission at unchanged authority", local_queue.get("id") == "SPELL-REVIEW-QUEUE-234" and local_queue.get("status") == "PACKET234_SUBMITTED_GPT_PENDING_811_37_0" and local_queue.get("currentAuthority") == EXPECTED_AUTHORITY, {"id": local_queue.get("id"), "status": local_queue.get("status"), "authority": local_queue.get("currentAuthority"), "digest": digest(queue_path.read_bytes()) if queue_path.exists() else None})

failures = [item for item in checks if not item["passed"]]
report = {
    "id": "RANK9PSYCHICFEAR7-RETURN234-INDEPENDENT-AUDIT",
    "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS" if not failures else "FAIL",
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_hash},
    "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_hash},
    "sourceArchive": {"path": SOURCE.relative_to(ROOT).as_posix(), **digest(SOURCE.read_bytes())},
    "authority": delivery.get("authority"),
    "heldIds": delivery.get("heldIds"),
    "blockerIds": BLOCKERS,
    "nextGroup": delivery.get("nextPendingGroup"),
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
    "checks": checks,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {
    "id": "RANK9PSYCHICFEAR7-RETURN234-RECEIPT",
    "status": report["status"],
    "archive": report["archive"],
    "delivery": report["delivery"],
    "sourceArchive": report["sourceArchive"],
    "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())},
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "failures": failures, "archiveSha256": archive_hash["sha256"]}, ensure_ascii=False, indent=2))
