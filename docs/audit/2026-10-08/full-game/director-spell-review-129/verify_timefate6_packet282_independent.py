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
OUT = BASE / "rank9_timefate6_current_source_282_prepared"
PACKET = OUT / "DD_Rank9_TimeFate6_CurrentSource_282.zip"
DELIVERY = OUT / "DD_Rank9_TimeFate6_CurrentSource_282_DELIVERY.json"
PREPARATION = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_282.json"
HANDOFF = BASE / "CURRENT_HANDOFF_282.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_282.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
RETURN221 = BASE / "rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD.zip"
RETURN221_DELIVERY = BASE / "rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json"
RETURN221_AUDIT = BASE / "RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json"
RETURN221_RECEIPT = BASE / "RANK9_TIMEFATE6_RETURN221_RECEIPT.json"
RETURN281 = BASE / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
RETURN281_DELIVERY = BASE / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
RETURN281_AUDIT = BASE / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
RETURN281_RECEIPT = BASE / "RANK9_WARDCONTROL6_RETURN281_RECEIPT.json"
PACKET281 = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"
PACKET281_DELIVERY = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json"
PACKET281_AUDIT = BASE / "RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json"
PACKET281_RECEIPT = BASE / "RANK9_WARDCONTROL6_PACKET281_RECEIPT.json"
REPORT = BASE / "RANK9_TIMEFATE6_PACKET282_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_TIMEFATE6_PACKET282_RECEIPT.json"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
IDS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
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


packet_raw = PACKET.read_bytes()
delivery_raw = DELIVERY.read_bytes()
delivery = read_json(delivery_raw)
prep = read_json(PREPARATION.read_bytes())
q = read_json(QUEUE.read_bytes())
h = read_json(HANDOFF.read_bytes())
p = read_json(PENDING.read_bytes())
index = read_json(INDEX.read_bytes())
catalog = read_json(CATALOG.read_bytes())
check("Packet282 ZIP matches its delivery size, SHA-256 and CRC32",
      delivery.get("id") == "RANK9-TIME-FATE6-CURRENT-SOURCE-DELIVERY-282"
      and delivery.get("status") == "PREPARED_UNSENT" and matches(packet_raw, delivery.get("archive", {})),
      {"actual": digest(packet_raw), "expected": delivery.get("archive")})
check("delivery, queue, handoff and pending audit agree on exact 816/32/0 scope",
      delivery.get("sourceAuthority") == q.get("currentAuthority") == h.get("currentAuthority") == p.get("authority") == AUTH
      and delivery.get("group") == q.get("nextGroup") == h.get("nextGroup") == "rank9-time-fate6"
      and delivery.get("pendingIds") == IDS and q.get("nextPendingIds") == IDS
      and set(IDS) <= set(p.get("pendingIds", [])) and p.get("pendingCount") == 32
      and delivery.get("accepted") is False and delivery.get("applied") is False,
      {"authority": delivery.get("sourceAuthority"), "pendingIds": delivery.get("pendingIds")})
ix = {row["id"]: row for row in index["entries"]}
cat = {row["id"]: row for row in catalog["spells"]}
check("four targets remain pending and non-operational; excluded identities stay excluded",
      index.get("authoredCounts") == {"reviewed": 816, "pending": 32}
      and index.get("representationCounts", {}).get("completeReviewedStandaloneProcedures") == 540
      and all(ix[sid]["authoredStatus"] == "pending-authored-procedure" and ix[sid]["sourceStatus"] == "blocked-pending-operational-review" and cat[sid].get("operational") is None for sid in IDS)
      and "time-fracture" not in p.get("pendingIds", []) and "foresight-perfect" not in p.get("pendingIds", []),
      {"indexCounts": index.get("authoredCounts")})

with zipfile.ZipFile(PACKET) as archive:
    names = archive.namelist()
    name_set = set(names)
    check("ZIP directory is sound and member paths are unique and safe",
          archive.testzip() is None and len(names) == len(name_set) and all(safe(name) for name in names),
          {"members": len(names), "unique": len(name_set)})
    manifest = read_json(archive.read("MANIFEST.json"))
    rows = {row.get("path"): row for row in manifest.get("members", []) if isinstance(row, dict)}
    check("embedded manifest covers every payload member and exact Time/Fate scope",
          manifest.get("sourceAuthority") == AUTH and manifest.get("group") == "rank9-time-fate6"
          and manifest.get("pendingIds") == IDS and manifest.get("payloadMemberCount") == len(rows) == len(names) - 1
          and set(rows) == name_set - {"MANIFEST.json"},
          {"payload": len(rows), "zipMembers": len(names), "authority": manifest.get("sourceAuthority")})
    bad_members = [name for name, row in rows.items() if not matches(archive.read(name), row)]
    check("every payload member matches embedded byte, SHA-256 and CRC32", not bad_members, bad_members[:15])
    candidate = read_json(archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json"))
    context = read_json(archive.read("CURRENT_CONTEXT_282.json"))
    source_rows = candidate.get("sourceBindings", [])
    source_failures = []
    for row in source_rows:
        member = "sources_current/" + row["path"]
        if member not in name_set or not matches(archive.read(member), row) or (ROOT / row["path"]).read_bytes() != archive.read(member):
            source_failures.append(row["path"])
    check("candidate and context bind the exact current group, 140 sources and latest Return281",
          candidate.get("currentAuthority") == context.get("sourceAuthority") == AUTH
          and candidate.get("currentPendingGroup") == {"group": "rank9-time-fate6", "spellIds": IDS, "count": 4}
          and context.get("pendingIds") == IDS and len(source_rows) == 140
          and context.get("latestReturn281Audit", {}).get("sha256") == digest(RETURN281_AUDIT.read_bytes())["sha256"]
          and context.get("latestPacket281Audit", {}).get("sha256") == digest(PACKET281_AUDIT.read_bytes())["sha256"],
          {"sources": len(source_rows), "authority": candidate.get("currentAuthority"), "pendingIds": context.get("pendingIds")})
    check("all 140 refreshed source files match both packet bindings and working-tree bytes",
          not source_failures, source_failures[:15])
    history = {
        "history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD.zip": RETURN221,
        "history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json": RETURN221_DELIVERY,
        "history/return221/INDEPENDENT_AUDIT.json": RETURN221_AUDIT,
        "history/return221/RECEIPT.json": RETURN221_RECEIPT,
        "history/return281/DD_Rank9_WardControl6_Director_Return281_HELD.zip": RETURN281,
        "history/return281/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json": RETURN281_DELIVERY,
        "history/return281/INDEPENDENT_AUDIT.json": RETURN281_AUDIT,
        "history/return281/RECEIPT.json": RETURN281_RECEIPT,
        "history/packet281/DD_Rank9_WardControl6_CurrentSource_281.zip": PACKET281,
        "history/packet281/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json": PACKET281_DELIVERY,
        "history/packet281/INDEPENDENT_AUDIT.json": PACKET281_AUDIT,
        "history/packet281/RECEIPT.json": PACKET281_RECEIPT,
    }
    history_failures = [name for name, path in history.items() if name not in name_set or archive.read(name) != path.read_bytes()]
    check("Return221, Return281 and Packet281 source evidence are bundled byte-exactly", not history_failures, history_failures)
    request = archive.read("REQUEST_282.txt").decode("utf-8")
    check("request confines review to four IDs, retains exact blockers and forbids unrelated re-review/application",
          all(sid in request for sid in IDS) and all(blocker in request for blocker in ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"])
          and "Review only" in request and "Do not re-review completed feats" in request and "Keep all acceptances unapplied" in request,
          {"requestBytes": len(request)})
    prep_check = read_json(PREPARATION.read_bytes())
    check("preparation records ten passing checks and no canonical changes or applications",
          prep_check.get("checksPassed") == 10 and prep_check.get("checksFailed") == 0
          and prep_check.get("canonicalChangesBeforePreparation") is False
          and prep_check.get("accepted") is False and prep_check.get("applied") is False,
          {"status": prep_check.get("status"), "checks": [prep_check.get("checksPassed"), prep_check.get("checksFailed")]})
    check("Return281 is independently audited as held with unchanged authority and exact Time/Fate next group",
          read_json(RETURN281_DELIVERY.read_bytes()).get("heldIds") == ["nullification-wave", "reality-anchor"]
          and read_json(RETURN281_DELIVERY.read_bytes()).get("acceptedIds") == []
          and read_json(RETURN281_AUDIT.read_bytes()).get("status") == "PASS"
          and read_json(RETURN281_AUDIT.read_bytes()).get("failedChecks") == 0
          and read_json(RETURN281_DELIVERY.read_bytes()).get("nextPendingGroup") == {"group": "rank9-time-fate6", "pendingIds": IDS},
          {"returnAudit": read_json(RETURN281_AUDIT.read_bytes()).get("status"), "next": read_json(RETURN281_DELIVERY.read_bytes()).get("nextPendingGroup")})

failures = [row for row in checks if not row["passed"]]
report = {"id": "RANK9-TIMEFATE6-PACKET282-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "PASS" if not failures else "FAIL", "archive": {"path": PACKET.relative_to(ROOT).as_posix(), **digest(packet_raw)},
          "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(delivery_raw)},
          "authority": AUTH, "group": "rank9-time-fate6", "pendingIds": IDS, "sourceBindingsVerified": 140,
          "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures),
          "checks": checks, "scopeLimitation": "Validates transfer, source/member bindings, authority and prior ruling evidence; it does not adjudicate game rules."}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9-TIMEFATE6-PACKET282-RECEIPT", "status": report["status"], "archive": report["archive"],
           "deliveryManifest": report["deliveryManifest"], "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())},
           "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures),
           "scopeLimitation": report["scopeLimitation"]}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures),
                  "failedChecks": len(failures), "failures": failures, "archive": report["archive"]}, ensure_ascii=False, indent=2))
