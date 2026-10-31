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
RECEIVED = BASE / "rank9_deathrecovery7_return235_received"
ARCHIVE = RECEIVED / "DD_Rank9_FinalWord_Director_Return235_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json"
SOURCE = BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235.zip"
SOURCE_DELIVERY = BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"
REPORT = BASE / "RANK9DEATHRECOVERY7_RETURN235_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9DEATHRECOVERY7_RETURN235_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["final-word"]
BLOCKERS = {"final-word": ["DR217-B01"]}
checks: list[dict] = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def matches(raw: bytes, expected: dict) -> bool:
    got = digest(raw)
    return isinstance(expected, dict) and all(got.get(k) == expected.get(k) for k in ("bytes", "sha256")) and (expected.get("crc32") is None or got["crc32"] == expected["crc32"])


def safe(name: str) -> bool:
    path = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in path.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
delivery_digest = digest(DELIVERY.read_bytes())
check("archive SHA-256/size/CRC32 and exact delivery identity match", delivery.get("id") == "RANK9-FINALWORD-DIRECTOR-RETURN235-DELIVERY" and delivery.get("archive", {}).get("fileName") == ARCHIVE.name and matches(archive_bytes, delivery.get("archive", {})), {"actual": archive_digest, "expected": delivery.get("archive")})
check("external delivery hash matches the GPT-stated exact manifest hash", delivery_digest["sha256"] == "a0762f32385c63d6c29c0ad3995767358244ab2b5cb6f80ba87960995441e380", delivery_digest)
check("authority remains 811/37/0 and the return accepts or applies nothing", delivery.get("authority") == AUTHORITY and delivery.get("accepted") is False and delivery.get("applied") is False and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("heldIds") == TARGETS, {k: delivery.get(k) for k in ("authority", "accepted", "applied", "acceptedIds", "appliedIds", "heldIds")})
check("delivered source packet binding matches the exact audited Packet235", matches(SOURCE.read_bytes(), delivery.get("sourcePacket", {})) and delivery.get("sourcePacket", {}).get("fileName") == SOURCE.name and matches(SOURCE_DELIVERY.read_bytes(), delivery.get("sourceDelivery", {})), {"archive": digest(SOURCE.read_bytes()), "delivery": digest(SOURCE_DELIVERY.read_bytes())})

with zipfile.ZipFile(ARCHIVE) as outer:
    names = outer.namelist()
    name_set = set(names)
    check("ZIP integrity passes; all member paths are unique, safe and ordinary files", outer.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names) and all(not i.is_dir() for i in outer.infolist()), {"members": len(names), "unique": len(name_set), "unsafe": [n for n in names if not safe(n)][:10]})
    listed = delivery.get("members", [])
    member_map = {item.get("path"): item for item in listed if isinstance(item, dict)}
    allowlist = delivery.get("exactAllowlist", [])
    check("external exact allowlist and byte bindings cover all ZIP members", set(allowlist) == name_set and len(allowlist) == len(names) and set(member_map) == name_set and len(member_map) == len(names) == delivery.get("memberCount"), {"archive": len(names), "allowlist": len(allowlist), "memberMap": len(member_map), "memberCount": delivery.get("memberCount")})
    external_failures = [n for n in names if n not in member_map or not matches(outer.read(n), member_map[n])]
    check("every ZIP member matches the external byte/SHA/CRC binding", not external_failures, external_failures[:12])
    manifest_bytes = outer.read("MEMBER_MANIFEST.json")
    manifest = read_json(manifest_bytes)
    manifest_record = member_map.get("MEMBER_MANIFEST.json", {})
    manifest_members = manifest.get("members", [])
    manifest_map = {item.get("path"): item for item in manifest_members if isinstance(item, dict)}
    check("embedded manifest is externally bound and covers every other member exactly", matches(manifest_bytes, manifest_record) and set(manifest_map) == name_set - {"MEMBER_MANIFEST.json"} and len(manifest_map) == delivery.get("payloadCount"), {"manifestMembers": len(manifest_map), "payloadCount": delivery.get("payloadCount")})
    internal_failures = [n for n, rec in manifest_map.items() if n not in name_set or not matches(outer.read(n), rec)]
    check("every payload member matches embedded byte/SHA/CRC bindings", not internal_failures, internal_failures[:12])

    decision = read_json(outer.read("DIRECTOR_DECISION.json"))
    blocker_doc = read_json(outer.read("BLOCKERS.json"))
    count = read_json(outer.read("COUNTS.json"))
    cases = read_json(outer.read("CASE_RESULTS.json"))
    source_verification = read_json(outer.read("SOURCE_VERIFICATION.json"))
    integrity = read_json(outer.read("DATA_INTEGRITY_CHECK.json"))
    clock = read_json(outer.read("CLOCK_CHECK.json"))
    preseal = read_json(outer.read("PRESEAL_CHECK.json"))
    gorthan = read_json(outer.read("GORTHAN_SOURCE_LEAD.json"))
    next_group = read_json(outer.read("NEXT_PENDING_GROUP.json"))
    current_reassessment = read_json(outer.read("CURRENT_SOURCE_REASSESSMENT.json"))

    per_identity = decision.get("perIdentity", [])
    check("sealed decision holds only final-word under DR217-B01", decision.get("scopeIds") == TARGETS and decision.get("authority") == AUTHORITY and decision.get("accepted") is False and decision.get("applied") is False and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("heldIds") == TARGETS and len(per_identity) == 1 and per_identity[0].get("id") == "final-word" and per_identity[0].get("blockerIds") == BLOCKERS["final-word"] and per_identity[0].get("status") == "HELD_REQUIRED_SOURCE_WITNESS", decision)
    blocker = next((row for row in blocker_doc.get("blockers", []) if row.get("id") == "DR217-B01"), {})
    check("blocker accurately retains the source-qualified victim, soul-availability and capture-history gap", blocker_doc.get("targetIds") == TARGETS and blocker.get("spellIds") == TARGETS and blocker.get("status") == "OPEN" and blocker.get("wholeSpellGate") is True and bool(blocker.get("missingEvidence")) and bool(blocker.get("requiredCorrection")), {"id": blocker.get("id"), "status": blocker.get("status"), "missingEvidence": blocker.get("missingEvidence")})
    check("Gorthan is explicitly assessed without inferring current body, HP, soul availability or custody", gorthan.get("source", {}).get("path") == "The_World_of_Aethel_Lore.docx" and "Has died thrice, returned by soulbinding." in gorthan.get("source", {}).get("exactText", "") and len(gorthan.get("notEstablished", [])) >= 4 and "Insufficient to close DR217-B01" in gorthan.get("decision", "") and gorthan.get("accepted") is False and gorthan.get("applied") is False and gorthan.get("failedChecks") == 0, {"established": gorthan.get("established"), "notEstablished": gorthan.get("notEstablished"), "decision": gorthan.get("decision")})

    check("all 16 prior cases replay and preserve exact classifications and operations", len(cases) == 16 and count.get("cases") == 16 and count.get("completeConditionalCases") == 6 and count.get("heldCases") == 10 and count.get("events") == 223 and count.get("forwardOperations") == 446 and count.get("inverseOperations") == 446 and all(item.get("replayPassed") is True for item in cases), {k: count.get(k) for k in ("cases", "completeConditionalCases", "heldCases", "events", "forwardOperations", "inverseOperations")})
    exact_case_members = [n for n in names if re.fullmatch(r"cases/DR184-FINAL-WORD-[^/]+\.json", n)]
    source_return = BASE / "rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217.zip"
    case_differences = []
    with zipfile.ZipFile(source_return) as prior:
        prior_cases = {pathlib.PurePosixPath(n).name: n for n in prior.namelist() if n.startswith("preserved_cases/") and n.endswith(".json")}
        for name in exact_case_members:
            basename = pathlib.PurePosixPath(name).name
            if basename not in prior_cases or read_json(prior.read(prior_cases[basename])) != read_json(outer.read(name)):
                case_differences.append(name)
    check("all 16 preserved final-word case files equal the prior Return217 case records as JSON", len(exact_case_members) == 16 and not case_differences, case_differences)

    check("source verification, data replay, clock and preseal checks pass with no failures", source_verification.get("failedChecks") == 0 and source_verification.get("passedChecks") == source_verification.get("checkCount") == 1173 and integrity.get("failedChecks") == 0 and integrity.get("passedChecks") == integrity.get("checkCount") and clock.get("failedChecks") == 0 and clock.get("passedChecks") == clock.get("checkCount") and preseal.get("failedChecks") == 0 and preseal.get("passedChecks") == preseal.get("checkCount") and delivery.get("packageChecks", {}).get("checkCount") == delivery.get("packageChecks", {}).get("passedChecks") == 993 and delivery.get("packageChecks", {}).get("failedChecks") == 0, {"source": {k: source_verification.get(k) for k in ("checkCount", "passedChecks", "failedChecks")}, "integrity": {k: integrity.get(k) for k in ("checkCount", "passedChecks", "failedChecks")}, "clock": {k: clock.get(k) for k in ("checkCount", "passedChecks", "failedChecks")}, "preseal": {k: preseal.get(k) for k in ("checkCount", "passedChecks", "failedChecks")}, "package": delivery.get("packageChecks") and {k: delivery["packageChecks"].get(k) for k in ("checkCount", "passedChecks", "failedChecks")}})

    queue_member = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_235.json"
    queue_binding = next_group.get("queueBinding", {})
    embedded_queue_raw = outer.read(queue_member) if queue_member in name_set else b""
    embedded_queue = read_json(embedded_queue_raw) if embedded_queue_raw else {}
    queue_path = BASE / "CURRENT_SPELL_QUEUE_235.json"
    local_queue = read_json(queue_path.read_bytes())
    check("next group is Defense/Form8 with exactly its three pending IDs and unchanged authority", next_group.get("group") == "rank9-defense-form8" and next_group.get("pendingIds") == ["elemental-shell", "timeless-form", "invulnerable-sphere"] and next_group.get("freshPacketRequiredBeforeReview") is True and next_group.get("authorityUnchanged") == AUTHORITY, next_group)
    check("next-group queue reference binds its embedded pre-submission queue snapshot", queue_member in name_set and matches(embedded_queue_raw, queue_binding) and embedded_queue.get("currentAuthority") == AUTHORITY, {"embedded": digest(embedded_queue_raw), "expected": queue_binding})
    check("newer local queue records Packet235 submission and the same next pending group", local_queue.get("status") == "PACKET235_SUBMITTED_GPT_PENDING_811_37_0" and local_queue.get("currentAuthority") == AUTHORITY and local_queue.get("nextGroup") == "rank9-death-recovery7" and next_group.get("pendingIds") == [x for row in local_queue.get("currentPendingGroups", []) if row.get("group") == "rank9-defense-form8" for x in row.get("pendingIds", [])], {"status": local_queue.get("status"), "authority": local_queue.get("currentAuthority"), "nextTargetIds": next_group.get("pendingIds")})
    check("current-source reassessment preserves authority and confirms no positive capture witness was found", current_reassessment.get("authority") == AUTHORITY and current_reassessment.get("sourceBindingsVerified") == 74 and current_reassessment.get("captureWitnessFound") is False and len(current_reassessment.get("findings", [])) >= 5 and any("missing positive witness" in finding for finding in current_reassessment.get("findings", [])), {k: current_reassessment.get(k) for k in ("authority", "sourceBindingsVerified", "captureWitnessFound", "findings")})

failures = [item for item in checks if not item["passed"]]
report = {"id": "RANK9DEATHRECOVERY7-RETURN235-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL",
          "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_digest},
          "sourcePacket": {"path": SOURCE.relative_to(ROOT).as_posix(), **digest(SOURCE.read_bytes())}, "authority": delivery.get("authority"), "heldIds": delivery.get("heldIds"),
          "blockerIds": BLOCKERS, "nextGroup": next_group, "caseCount": len(cases), "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9DEATHRECOVERY7-RETURN235-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "sourcePacket": report["sourcePacket"],
           "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archiveSha256": archive_digest["sha256"], "nextGroup": next_group}, ensure_ascii=False, indent=2))
