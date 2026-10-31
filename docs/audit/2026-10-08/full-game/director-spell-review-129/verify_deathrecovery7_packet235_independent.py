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
PREP = BASE / "rank9_deathrecovery7_current_source_235_prepared"
ARCHIVE = PREP / "DD_Rank9_DeathRecovery7_CurrentSource_235.zip"
DELIVERY = PREP / "DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"
REPORT = BASE / "RANK9DEATHRECOVERY7_PACKET235_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9DEATHRECOVERY7_PACKET235_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["final-word"]
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
check("outer archive identity and size/SHA-256/CRC32 match exact delivery", delivery.get("id") == "RANK9-DEATH-RECOVERY7-CURRENT-SOURCE-235-DELIVERY" and delivery.get("archive", {}).get("fileName") == ARCHIVE.name and matches(archive_bytes, delivery.get("archive", {})), {"actual": archive_digest, "expected": delivery.get("archive")})
check("packet scope and authority are exactly final-word at 811/37/0", delivery.get("group") == "rank9-death-recovery7" and delivery.get("targetIds") == TARGETS and delivery.get("authority") == AUTHORITY and delivery.get("canonicalChanges") is False and delivery.get("githubChanges") is False and delivery.get("sourceProgramsExecuted") is False and delivery.get("runtimeExecuted") is False, {k: delivery.get(k) for k in ("group", "targetIds", "authority", "canonicalChanges", "githubChanges", "sourceProgramsExecuted", "runtimeExecuted")})

with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    name_set = set(names)
    check("ZIP integrity passes and member names are unique and safe", archive.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names), {"members": len(names), "unique": len(name_set)})
    allowlist = delivery.get("exactAllowlist", [])
    outer_members = delivery.get("members", [])
    by_path = {item.get("path"): item for item in outer_members if isinstance(item, dict)}
    check("delivery allowlist and member map exactly cover ZIP", set(allowlist) == name_set and len(allowlist) == len(names) and set(by_path) == name_set and len(by_path) == len(names) == delivery.get("memberCount"), {"archive": len(names), "allowlist": len(allowlist), "memberCount": delivery.get("memberCount")})
    outer_failures = [name for name in names if name not in by_path or not matches(archive.read(name), by_path[name])]
    check("every member matches external byte/hash/CRC binding", not outer_failures, outer_failures[:12])
    manifest_raw = archive.read("MEMBER_MANIFEST.json")
    manifest = read_json(manifest_raw)
    manifest_info = delivery.get("memberManifest", {})
    manifest_map = {item.get("path"): item for item in manifest.get("members", []) if isinstance(item, dict)}
    check("embedded manifest is externally bound and excludes itself", manifest_info.get("path") == "MEMBER_MANIFEST.json" and matches(manifest_raw, manifest_info) and set(manifest_map) == name_set - {"MEMBER_MANIFEST.json"} and len(manifest_map) == delivery.get("payloadCount"), {"manifestEntries": len(manifest_map), "payloadCount": delivery.get("payloadCount")})
    inner_failures = [name for name, record in manifest_map.items() if name not in name_set or not matches(archive.read(name), record)]
    check("every payload member matches embedded byte/hash/CRC binding", not inner_failures, inner_failures[:12])

    current_index = "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    current_catalog = "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    current_access = "current/DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    current_queue = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_235.json"
    current_handoff = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_235.json"
    pending_audit = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_235.json"
    candidate_path = "current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json"
    request_path = "current/REQUEST_235.txt"
    index = read_json(archive.read(current_index))
    catalog = read_json(archive.read(current_catalog))
    access = read_json(archive.read(current_access))
    queue = read_json(archive.read(current_queue))
    handoff = read_json(archive.read(current_handoff))
    pending = read_json(archive.read(pending_audit))
    candidate = read_json(archive.read(candidate_path))
    request = archive.read(request_path).decode("utf-8")
    check("current index and catalog retain exactly 811 reviewed / 37 pending with final-word pending", index.get("authoredCounts") == {"reviewed": 811, "pending": 37} and sum(1 for row in index.get("entries", []) if row.get("authoredStatus") == "pending-authored-procedure") == 37 and any(row.get("id") == "final-word" and row.get("authoredStatus") == "pending-authored-procedure" for row in index.get("entries", [])) and any(row.get("id") == "final-word" for row in catalog.get("spells", [])), {"authoredCounts": index.get("authoredCounts"), "targetStatus": next((row.get("authoredStatus") for row in index.get("entries", []) if row.get("id") == "final-word"), None)})
    check("queue, handoff and pending audit agree on current authority and sole target", queue.get("currentAuthority") == handoff.get("currentAuthority") == pending.get("authority") == AUTHORITY and queue.get("nextGroup") == "rank9-death-recovery7" and queue.get("next", {}).get("pendingIds") == TARGETS and handoff.get("nextGroup") == "rank9-death-recovery7" and handoff.get("nextPendingCount") == 1 and pending.get("preparedNextGroup", {}).get("pendingIds") == TARGETS, {"queue": queue.get("currentAuthority"), "handoff": handoff.get("currentAuthority"), "pending": pending.get("authority")})
    check("candidate and prompt restrict this review to final-word", candidate.get("currentPendingGroup", {}).get("spellIds") == TARGETS and candidate.get("currentReviewTargets", [{}])[0].get("spellId") == "final-word" and delivery.get("targetIds") == TARGETS and "Exact target: final-word. No other identity is in scope." in request and "doom" in request and "eternal-pact" in request, {"group": candidate.get("currentPendingGroup"), "targets": [x.get("spellId") for x in candidate.get("currentReviewTargets", [])]})
    current_source_rows = delivery.get("sourceBindings", [])
    source_failures = []
    for row in current_source_rows:
        member = "sources_current/" + row["path"]
        if member not in name_set or not matches(archive.read(member), row):
            source_failures.append(row["path"])
    check("all 74 historical source paths were refreshed and included byte-exactly", len(current_source_rows) == 74 and not source_failures and candidate.get("sourceBindingRefresh", {}).get("sourceFiles") == 74, {"bindings": len(current_source_rows), "failures": source_failures[:10]})
    local_source_failures = []
    for row in current_source_rows:
        path = ROOT / row["path"]
        if not path.exists() or not matches(path.read_bytes(), row):
            local_source_failures.append(row["path"])
    check("refreshed source bindings still match current working-tree source files", not local_source_failures, local_source_failures[:10])
    for rel, member in [("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_235.json", current_queue), ("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_235.json", current_handoff), ("docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_235.json", pending_audit)]:
        local = ROOT / rel
        check(f"embedded {local.name} matches its prepared local snapshot", local.exists() and local.read_bytes() == archive.read(member), {"path": rel, "bytes": len(archive.read(member))})

    r184_audit = read_json(archive.read("history/RETURN184_INDEPENDENT_AUDIT.json"))
    r184_decision = read_json(archive.read("history/RETURN184_DIRECTOR_DECISION.json"))
    r217_audit = read_json(archive.read("history/RETURN217_INDEPENDENT_AUDIT.json"))
    r217_decision = read_json(archive.read("history/Return217/DIRECTOR_DECISION.json"))
    r217_blockers = read_json(archive.read("history/Return217/BLOCKERS.json"))
    fw_blocker = next((row for row in r217_blockers.get("blockers", []) if row.get("id") == "DR217-B01"), {})
    check("prior Return184 and Return217 audit receipts are PASS", r184_audit.get("status") == "PASS" and r184_decision.get("acceptedIds") == ["soul-harvest", "power-word-kill", "thread-severance", "wail-of-the-banshee"] and r217_audit.get("status") == "PASS", {"return184": r184_audit.get("status"), "return217": r217_audit.get("status"), "accepted184": r184_decision.get("acceptedIds")})
    check("Return217 confirms only doom and eternal-pact accepted/applied while final-word is held DR217-B01", r217_decision.get("acceptedIds") == ["doom", "eternal-pact"] and r217_decision.get("heldIds") == TARGETS and any(x.get("id") == "final-word" and x.get("blockerIds") == ["DR217-B01"] for x in r217_decision.get("perIdentity", [])) and fw_blocker.get("spellIds") == TARGETS and bool(fw_blocker.get("missingEvidence")), {"accepted": r217_decision.get("acceptedIds"), "held": r217_decision.get("heldIds"), "blocker": fw_blocker.get("id")})
    final_word_cases = [name for name in names if re.fullmatch(r"history/Return217/preserved_cases/DR184-FINAL-WORD-[^/]+\.json", name)]
    case_source = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217.zip"
    with zipfile.ZipFile(case_source) as source_return:
        recovered_case_failures = []
        for name in final_word_cases:
            member = name.split("history/Return217/", 1)[1]
            if member not in source_return.namelist() or source_return.read(member) != archive.read(name):
                recovered_case_failures.append(member)
    check("all 16 preserved final-word cases match exact Return217 archive members", len(final_word_cases) == 16 and not recovered_case_failures, recovered_case_failures)
    check("no canonical, GitHub, runtime or supplied-program changes are part of this packet", delivery.get("canonicalChanges") is False and delivery.get("githubChanges") is False and delivery.get("runtimeExecuted") is False and delivery.get("sourceProgramsExecuted") is False and "Do not edit canonical files" in request and "execute supplied programs" in request, {k: delivery.get(k) for k in ("canonicalChanges", "githubChanges", "runtimeExecuted", "sourceProgramsExecuted")})

failures = [item for item in checks if not item["passed"]]
report = {"id": "RANK9DEATHRECOVERY7-PACKET235-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL",
          "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest}, "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_digest},
          "authority": delivery.get("authority"), "targetIds": delivery.get("targetIds"), "sourceBindings": len(delivery.get("sourceBindings", [])),
          "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9DEATHRECOVERY7-PACKET235-RECEIPT", "status": report["status"], "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
           "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archiveSha256": archive_digest["sha256"]}, ensure_ascii=False, indent=2))
