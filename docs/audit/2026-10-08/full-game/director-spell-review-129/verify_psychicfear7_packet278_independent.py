from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_psychicfear7_current_source_278_prepared_review1"
ARCHIVE = OUT / "DD_Rank9_PsychicFear7_CurrentSource_278.zip"
DELIVERY = OUT / "DD_Rank9_PsychicFear7_CurrentSource_278_DELIVERY.json"
AUDIT = BASE / "RANK9PSYCHICFEAR7_PACKET278_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PSYCHICFEAR7_PACKET278_RECEIPT.json"
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
CHECKS: list[dict] = []


def digest(data: bytes) -> dict:
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}"}


def check(name: str, passed: bool, detail=None) -> None:
    CHECKS.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def matches(data: bytes, rec: dict) -> bool:
    got = digest(data)
    return all(got.get(k) == rec.get(k) for k in ("bytes", "sha256")) and (rec.get("crc32") is None or got["crc32"] == rec["crc32"])


def safe_path(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
check("archive digest matches delivery", matches(archive_bytes, delivery.get("archive", {})), archive_digest)
check("delivery binds target group and exact 816/32 authority", delivery.get("group") == "rank9-psychic-fear7" and delivery.get("targetIds") == TARGETS and delivery.get("authority") == AUTH and delivery.get("accepted") is False and delivery.get("applied") is False,
      {"group": delivery.get("group"), "targets": delivery.get("targetIds"), "authority": delivery.get("authority")})

z = zipfile.ZipFile(io.BytesIO(archive_bytes))
names, name_set = z.namelist(), set(z.namelist())
external = {r.get("path"): r for r in delivery.get("members", []) if isinstance(r, dict)}
check("archive paths are unique, safe, and contain no directories", len(names) == len(name_set) and all(safe_path(n) and not i.is_dir() for n, i in zip(names, z.infolist())), {"members": len(names)})
check("delivery allowlist covers every member exactly", set(external) == name_set and len(external) == delivery.get("memberCount") == len(names) and delivery.get("payloadCount") == len(names) - 1, {"members": len(names), "allowlist": len(external)})
external_bad = [n for n in names if n not in external or not matches(z.read(n), external[n])]
check("all payloads match external SHA/size/CRC", not external_bad, external_bad[:20])
manifest_raw = z.read("MANIFEST.json")
manifest = read_json(manifest_raw)
manifest_rows = manifest.get("members", [])
manifest_map = {r.get("path"): r for r in manifest_rows}
check("embedded manifest matches delivery", matches(manifest_raw, delivery.get("memberManifest", {})) and delivery.get("memberManifest", {}).get("path") == "MANIFEST.json", digest(manifest_raw))
check("embedded manifest covers every payload and verifies each", set(manifest_map) == name_set - {"MANIFEST.json"} and len(manifest_rows) == delivery.get("payloadCount") and all(matches(z.read(n), r) for n, r in manifest_map.items()), {"manifestPayloads": len(manifest_rows), "archivePayloads": len(name_set)-1})

candidate = read_json(z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json"))
context = read_json(z.read("CURRENT_CONTEXT_278.json"))
request = z.read("REQUEST_278.txt").decode("utf-8")
check("candidate and context scope only current Psychic/Fear7 group", candidate.get("currentPendingGroup", {}).get("spellIds") == TARGETS and context.get("targetGroup") == {"group": "rank9-psychic-fear7", "pendingIds": TARGETS, "count": 3} and candidate.get("currentAuthority") == AUTH and context.get("authority") == AUTH, {"group": context.get("targetGroup"), "authority": context.get("authority")})
check("request preserves evidence thresholds and excludes acceptance/application", all(x in request for x in TARGETS) and "No acceptance or application is requested" in request and "Do not substitute an extra Action" in request, request[:600])
check("candidate carries 84 refreshed source bindings", len(candidate.get("sourceBindings", [])) == 84 and candidate.get("sourceBindingRefresh", {}).get("sourceBytesFromCurrentWorkingTree") is True, len(candidate.get("sourceBindings", [])))
source_failures = []
for binding in candidate.get("sourceBindings", []):
    member = "sources_current/" + binding["path"]
    if member not in name_set or not matches(z.read(member), binding):
        source_failures.append(binding.get("path"))
    local = ROOT / pathlib.PurePosixPath(binding["path"])
    if not local.is_file() or not matches(local.read_bytes(), binding):
        source_failures.append("working-tree:" + binding.get("path", ""))
check("every refreshed source binding matches archive and current working tree", not source_failures, source_failures[:20])

idx = read_json(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
catalog = read_json(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
entries = {r.get("id"): r for r in idx.get("entries", [])}
cards = {r.get("id"): r for r in catalog.get("spells", [])}
check("current index/catalog preserve all three as pending and non-operational", idx.get("authoredCounts") == {"reviewed": 816, "pending": 32} and all(entries.get(s, {}).get("authoredStatus") == "pending-authored-procedure" and entries.get(s, {}).get("sourceStatus") == "blocked-pending-operational-review" and cards.get(s, {}).get("operational") is None for s in TARGETS), {s: entries.get(s, {}).get("authoredStatus") for s in TARGETS})
check("only target records are carried and retain PF182 blocker mapping", {r.get("spellId") for r in candidate.get("targetRecords", [])} == set(TARGETS) and candidate.get("priorReturn234Disposition", {}).get("blockerIds") == {"psychic-scream": ["PF182-B01"], "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}, {"records": [r.get("spellId") for r in candidate.get("targetRecords", [])], "priorBlockers": candidate.get("priorReturn234Disposition", {}).get("blockerIds")})
check("candidate source branch/base match delivery", candidate.get("sourceBranch") == "main" and candidate.get("sourceCommitBase") == delivery.get("sourceCommitBase"), {"branch": candidate.get("sourceBranch"), "base": candidate.get("sourceCommitBase")})

queue = read_json((BASE / "CURRENT_SPELL_QUEUE_278.json").read_bytes())
handoff = read_json((BASE / "CURRENT_HANDOFF_278.json").read_bytes())
pending = read_json((BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_278.json").read_bytes())
check("external queue/handoff/pending snapshot agree on authority and 3-ID next group", queue.get("currentAuthority") == AUTH and handoff.get("currentAuthority") == AUTH and pending.get("authority") == AUTH and queue.get("nextGroup") == "rank9-psychic-fear7" and queue.get("nextPendingIds") == TARGETS and pending.get("pendingCount") == 32 and len(pending.get("pendingIds", [])) == 32, {"queue": queue.get("nextGroup"), "pending": pending.get("pendingCount")})
check("no canonical or application state is claimed changed", delivery.get("canonicalChanges") is False and delivery.get("applicationChanges") is False and delivery.get("runtimeExecuted") is False and delivery.get("githubChanges") is False, {k: delivery.get(k) for k in ["canonicalChanges", "applicationChanges", "runtimeExecuted", "githubChanges"]})

failures = [r for r in CHECKS if not r["passed"]]
report = {"id": "RANK9PSYCHICFEAR7-PACKET278-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
          "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())}, "authority": AUTH,
          "group": "rank9-psychic-fear7", "targetIds": TARGETS, "checkCount": len(CHECKS),
          "passedChecks": len(CHECKS)-len(failures), "failedChecks": len(failures), "checks": CHECKS}
AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9PSYCHICFEAR7-PACKET278-RECEIPT", "status": report["status"], "archive": report["archive"],
           "delivery": report["delivery"], "independentAudit": {"path": AUDIT.relative_to(ROOT).as_posix(), **digest(AUDIT.read_bytes())},
           "checkCount": len(CHECKS), "passedChecks": len(CHECKS)-len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(CHECKS), "passedChecks": report["passedChecks"],
                  "failedChecks": report["failedChecks"], "failures": failures, "archiveSha256": archive_digest["sha256"]}, indent=2))
