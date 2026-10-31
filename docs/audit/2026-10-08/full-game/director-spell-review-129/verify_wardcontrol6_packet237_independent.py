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
PACKET_DIR = BASE / "rank9_wardcontrol6_source_packet_237_refreshed"
ARCHIVE = PACKET_DIR / "DD_Rank9_WardControl6_CurrentSource_237.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_WardControl6_CurrentSource_237_DELIVERY.json"
PREPARATION = BASE / "RANK9_WARDCONTROL6_SOURCE_PREPARATION_237.json"
REPORT = BASE / "RANK9_WARDCONTROL6_PACKET237_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_WARDCONTROL6_PACKET237_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["nullification-wave", "reality-anchor"]
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


delivery_raw = DELIVERY.read_bytes()
delivery = read_json(delivery_raw)
prep = read_json(PREPARATION.read_bytes())
archive_raw = ARCHIVE.read_bytes()
archive_hash = digest(archive_raw)
delivery_hash = digest(delivery_raw)
check("outer ZIP matches the exact delivery binding", delivery.get("id") == "RANK9-WARD-CONTROL6-CURRENT-SOURCE-DELIVERY-237" and pathlib.Path(delivery.get("archive", {}).get("path", "")).name == ARCHIVE.name and matches(archive_raw, delivery.get("archive", {})), {"actual": archive_hash, "expected": delivery.get("archive")})
check("scope, authority and packet-preparation status are exact", delivery.get("status") == "PREPARED_UNSENT" and delivery.get("sourceAuthority") == AUTHORITY and delivery.get("group") == "rank9-ward-control6" and delivery.get("pendingIds") == TARGETS and delivery.get("accepted") is False and delivery.get("applied") is False and prep.get("checksPassed") == 10 and prep.get("checksFailed") == 0, {"status": delivery.get("status"), "authority": delivery.get("sourceAuthority"), "group": delivery.get("group"), "pendingIds": delivery.get("pendingIds"), "prepChecks": [prep.get("checksPassed"), prep.get("checksFailed")]})

with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    name_set = set(names)
    check("ZIP central directory and member paths are valid", archive.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names), {"members": len(names), "unique": len(name_set)})
    manifest = read_json(archive.read("MANIFEST.json"))
    members = manifest.get("members", [])
    manifest_map = {item.get("path"): item for item in members if isinstance(item, dict)}
    check("embedded manifest exactly covers all payload members", set(manifest_map) == name_set - {"MANIFEST.json"} and len(manifest_map) == delivery.get("payloadMemberCount") and len(names) == delivery.get("memberCount"), {"zipMembers": len(names), "manifestMembers": len(manifest_map), "deliveryPayloadMembers": delivery.get("payloadMemberCount")})
    bad_members = [name for name, row in manifest_map.items() if not matches(archive.read(name), row)]
    check("every payload member matches embedded byte, SHA-256 and CRC32", not bad_members, bad_members[:20])
    check("manifest binds exact Ward/Control6 identities and authority", manifest.get("id") == "RANK9-WARD-CONTROL6-CURRENT-SOURCE-PACKET-MANIFEST-237" and manifest.get("sourceAuthority") == AUTHORITY and manifest.get("group") == "rank9-ward-control6" and manifest.get("pendingIds") == TARGETS, {"authority": manifest.get("sourceAuthority"), "group": manifest.get("group"), "pendingIds": manifest.get("pendingIds")})

    candidate = read_json(archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_237.json"))
    request = archive.read("REQUEST_237.txt").decode("utf-8")
    context = read_json(archive.read("CURRENT_CONTEXT_237.json"))
    record_ids = [r.get("spellId") for r in candidate.get("records", [])]
    current_pending = [r.get("spellId") for r in candidate.get("records", []) if r.get("currentPending")]
    check("candidate keeps the six-spell group and marks only the exact two pending", candidate.get("currentPendingGroup", {}).get("spellIds") == TARGETS and len(record_ids) == 6 and set(record_ids) == {"greater-spell-turning", "eternal-ward", "ultimate-ward", "prismatic-sphere", *TARGETS} and set(current_pending) == set(TARGETS), {"group": candidate.get("currentPendingGroup"), "records": record_ids, "pending": current_pending})
    check("prompt requests only Nullification Wave and Reality Anchor and preserves the prior scope gates", all(text in request for text in ("Review only the two currently pending", "nullification-wave and reality-anchor", "Do not re-review the four Ward/Control6 identities already accepted in Return188", "no-save all-spell reflection", "two native Reality Anchor placements", "Do not edit/apply anything")) and context.get("targetGroup", {}).get("pendingIds") == TARGETS and context.get("sourceAuthority") == AUTHORITY, {"targetGroup": context.get("targetGroup"), "authority": context.get("sourceAuthority")})

    source_rows = delivery.get("sourceBindingsRefreshed")
    candidate_rows = candidate.get("sourceBindings", [])
    source_failures = []
    for row in candidate_rows:
        path = "sources_current/" + row["path"]
        if path not in name_set or not matches(archive.read(path), row):
            source_failures.append(row["path"])
    check("all 91 refreshed source files are included and match their bindings", source_rows == 91 and len(candidate_rows) == 91 and not source_failures, {"deliveryCount": source_rows, "candidateCount": len(candidate_rows), "failures": source_failures[:12]})
    local_failures = []
    for row in candidate_rows:
        path = ROOT / row["path"]
        if not path.exists() or not matches(path.read_bytes(), row):
            local_failures.append(row["path"])
    check("all refreshed source files match the current working tree", not local_failures, local_failures[:12])

    index = read_json(archive.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
    catalog = read_json(archive.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
    queue = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_237.json"))
    handoff = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_237.json"))
    pending = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_237.json"))
    index_rows = {r.get("id"): r for r in index.get("entries", [])}
    cards = {r.get("id"): r for r in catalog.get("spells", [])}
    check("embedded authority remains 811 reviewed / 37 pending with these two pending identities", index.get("authoredCounts") == {"reviewed": 811, "pending": 37} and sum(r.get("authoredStatus") == "pending-authored-procedure" for r in index.get("entries", [])) == 37 and all(index_rows.get(i, {}).get("authoredStatus") == "pending-authored-procedure" and index_rows.get(i, {}).get("sourceStatus") == "blocked-pending-operational-review" and cards.get(i, {}).get("operational") is None for i in TARGETS), {"authoredCounts": index.get("authoredCounts"), "targetStatus": {i: index_rows.get(i, {}).get("authoredStatus") for i in TARGETS}})
    check("embedded queue, handoff and pending audit agree on authority and selected group", queue.get("currentAuthority") == handoff.get("currentAuthority") == pending.get("authority") == AUTHORITY and queue.get("nextGroup") == handoff.get("nextGroup") == "rank9-ward-control6" and queue.get("next", {}).get("pendingIds") == handoff.get("nextPendingIds") == pending.get("preparedNextGroup", {}).get("pendingIds") == TARGETS and handoff.get("currentReturnArchive", {}).get("sha256") == "df248b3dd6bd7bf36dd9bb7bbfb4d89d877814fb8fb7ab752d35d1f16d7784d5", {"queueAuthority": queue.get("currentAuthority"), "handoffAuthority": handoff.get("currentAuthority"), "pendingAuthority": pending.get("authority"), "nextGroup": queue.get("nextGroup"), "next": queue.get("next"), "handoffNext": handoff.get("nextPendingIds")})
    # The queued handoff embeds Return236's source and audit binding; verify its digest against the archived copies.
    return_decision = read_json(archive.read("current/return236/DIRECTOR_DECISION.json"))
    return_audit = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEFENSEFORM8_RETURN236_INDEPENDENT_AUDIT.json"))
    return_delivery = read_json(archive.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return236_received/DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json"))
    check("prior Return236 is present, independently PASS-audited and hands this exact group forward", return_audit.get("status") == "PASS" and return_decision.get("acceptedIds") == [] and return_decision.get("appliedIds") == [] and set(return_decision.get("heldIds", [])) == {"elemental-shell", "timeless-form", "invulnerable-sphere"} and return_delivery.get("nextPendingIds") == TARGETS and return_delivery.get("nextPendingGroup") == "rank9-ward-control6", {"audit": return_audit.get("status"), "held": return_decision.get("heldIds"), "next": return_delivery.get("nextPendingIds")})
    check("preparation declares ten passing checks and no canonical or GitHub application", prep.get("checksPassed") == 10 and prep.get("checksFailed") == 0 and prep.get("status") == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT" and delivery.get("accepted") is False and delivery.get("applied") is False and "Do not edit/apply anything" in request, {"checks": [prep.get("checksPassed"), prep.get("checksFailed")], "status": prep.get("status")})

failures = [item for item in checks if not item["passed"]]
report = {"id": "RANK9-WARD-CONTROL6-PACKET237-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL",
          "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_hash}, "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_hash},
          "authority": delivery.get("sourceAuthority"), "group": delivery.get("group"), "pendingIds": delivery.get("pendingIds"), "sourceBindings": delivery.get("sourceBindingsRefreshed"),
          "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9-WARD-CONTROL6-PACKET237-RECEIPT", "status": report["status"], "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
           "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archive": report["archive"]}, ensure_ascii=False, indent=2))
