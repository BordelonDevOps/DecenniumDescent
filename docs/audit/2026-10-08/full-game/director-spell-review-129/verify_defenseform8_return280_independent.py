from __future__ import annotations

import hashlib
import json
import shutil
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DOWNLOADS = Path(r"C:\Users\cbord\Downloads")
TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
EXPECTED_BLOCKERS = {"elemental-shell": ["DF218-B01", "DF218-B02"],
                     "timeless-form": ["DF218-B03"],
                     "invulnerable-sphere": ["DF218-B04"]}
checks = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(part not in ("", ".", "..") for part in p.parts)


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery_candidates = sorted(DOWNLOADS.glob("*Return280*DELIVERY.json"), key=lambda p: p.stat().st_mtime)
assert delivery_candidates, "No downloaded Return280 DELIVERY.json found"
delivery_path = delivery_candidates[-1]
delivery = json.loads(delivery_path.read_text(encoding="utf-8-sig"))
archive_record = delivery.get("archive", {})
archive_name = archive_record.get("fileName") or archive_record.get("path", "")
archive_path = DOWNLOADS / archive_name
if not archive_path.exists():
    matches = [p for p in DOWNLOADS.glob("*Return280*HELD.zip")
               if digest(p.read_bytes())["sha256"] == archive_record.get("sha256")]
    assert len(matches) == 1, f"Could not unambiguously locate Return280 archive: {matches}"
    archive_path = matches[0]
archive_raw = archive_path.read_bytes()
archive_digest = digest(archive_raw)
delivery_digest = digest(delivery_path.read_bytes())

check("delivery identifies the Defense/Form8 Return280 artifact", delivery.get("id") == "RANK9-DEFENSEFORM8-DIRECTOR-RETURN280-DELIVERY"
      and archive_name.startswith("DD_Rank9_DefenseForm8_"),
      {"deliveryId": delivery.get("id"), "archiveName": archive_name})
check("downloaded archive matches its external SHA-256, byte length and CRC", archive_digest == {k: archive_record.get(k) for k in ("bytes", "sha256", "crc32")},
      {"actual": archive_digest, "expected": archive_record})
check("scope, decision sets, blocker map and 816/32 authority reconcile exactly",
      delivery.get("accepted") is False and delivery.get("applied") is False
      and delivery.get("acceptedIds") == delivery.get("appliedIds") == []
      and delivery.get("heldIds") == TARGETS and delivery.get("authority") == AUTHORITY
      and {row.get("id"): row.get("blockerIds") for row in delivery.get("perIdentity", [])} == EXPECTED_BLOCKERS
      and set(delivery.get("blockerIds", [])) == {"DF218-B01", "DF218-B02", "DF218-B03", "DF218-B04"},
      {"acceptedIds": delivery.get("acceptedIds"), "appliedIds": delivery.get("appliedIds"),
       "heldIds": delivery.get("heldIds"), "perIdentity": delivery.get("perIdentity")})
check("next group and exact 32-identity ordered remainder match the Director checkpoint",
      delivery.get("nextPendingGroup") == "rank9-ward-control6"
      and delivery.get("nextPendingIds") == ["nullification-wave", "reality-anchor"]
      and len(delivery.get("remainingOrderedIds", [])) == 32
      and len(set(delivery.get("remainingOrderedIds", []))) == 32,
      {"nextPendingGroup": delivery.get("nextPendingGroup"), "nextPendingIds": delivery.get("nextPendingIds"),
       "remainingCount": len(delivery.get("remainingOrderedIds", []))})
expected_order = [item for row in json.loads((BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279.json").read_text(encoding="utf-8-sig")).get("orderedRemainder", []) for item in row["ids"]]
check("ordered remainder preserves Return279's complete 32-identity order", delivery.get("remainingOrderedIds") == expected_order,
      {"matches": delivery.get("remainingOrderedIds") == expected_order})
counts = delivery.get("counts", {})
check("source and replay totals match the Director's visible report with zero failures",
      counts.get("sourceBindings") == 87 and counts.get("cases") == 46 and counts.get("events") == 993
      and counts.get("forwardOperations") == counts.get("inverseOperations") == 1986
      and counts.get("freshCheckTotal") == 24596 and counts.get("freshCheckFailures") == 0
      and counts.get("heldIdentities") == 3 and counts.get("acceptedIdentities") == counts.get("appliedIdentities") == 0,
      counts)
check("no canonical edit, application, runtime or supplied-program execution is claimed",
      delivery.get("canonicalChanges") is False and delivery.get("applicationPerformed") is False,
      {k: delivery.get(k) for k in ("canonicalChanges", "applicationPerformed")})

with zipfile.ZipFile(archive_path) as z:
    names = z.namelist()
    name_set = set(names)
    test = z.testzip()
    check("ZIP CRC scan, unique safe member names and exact allowlist pass",
          test is None and len(names) == len(name_set) and all(safe(n) for n in names)
          and set(delivery.get("exactAllowlist", [])) == name_set and len(names) == delivery.get("memberCount"),
          {"testzip": test, "memberCount": len(names), "unique": len(name_set),
           "externalMemberCount": delivery.get("memberCount")})
    ext_rows = {row["path"]: row for row in delivery.get("members", [])}
    manifest_raw = z.read("MEMBER_MANIFEST.json")
    manifest = json.loads(manifest_raw.decode("utf-8-sig"))
    internal_rows = {row["path"]: row for row in manifest.get("members", [])}
    mismatches = []
    for name in names:
        raw = z.read(name)
        actual = digest(raw)
        expected = ext_rows.get(name)
        if expected is None or any(actual.get(k) != expected.get(k) for k in ("bytes", "sha256", "crc32")):
            mismatches.append(name)
        if name != "MEMBER_MANIFEST.json":
            expected_internal = internal_rows.get(name)
            if expected_internal is None or any(actual.get(k) != expected_internal.get(k) for k in ("bytes", "sha256", "crc32")):
                mismatches.append("internal:" + name)
    check("all 81 archive members match external delivery and embedded exact manifests",
          not mismatches and set(ext_rows) == name_set and set(internal_rows) == name_set - {"MEMBER_MANIFEST.json"}
          and all(digest(manifest_raw).get(k) == delivery.get("memberManifest", {}).get(k) for k in ("bytes", "sha256", "crc32")),
          {"mismatchCount": len(mismatches), "mismatches": mismatches[:20],
           "externalRows": len(ext_rows), "internalRows": len(internal_rows)})
    decision = json.loads(z.read("DIRECTOR_DECISION.json").decode("utf-8-sig"))
    queue = json.loads(z.read("REMAINING_QUEUE.json").decode("utf-8-sig"))
    semantic = json.loads(z.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json").decode("utf-8-sig"))
    validate = json.loads(z.read("VALIDATION.json").decode("utf-8-sig"))
    check("internal decision agrees with delivery sets, blockers and authority",
          decision.get("id") == "RANK9-DEFENSEFORM8-DIRECTOR-RETURN280"
          and decision.get("authority") == AUTHORITY and decision.get("heldIds") == TARGETS
          and decision.get("acceptedIds") == decision.get("appliedIds") == []
          and decision.get("blockerIds") == delivery.get("blockerIds"),
          {"decisionId": decision.get("id"), "heldIds": decision.get("heldIds")})
    check("internal remaining queue agrees exactly with the external delivery remainder and next group",
          queue.get("orderedPendingIds") == delivery.get("remainingOrderedIds")
          and queue.get("nextPendingGroup") == delivery.get("nextPendingGroup")
          and queue.get("nextPendingIds") == delivery.get("nextPendingIds"),
          {"orderedCount": len(queue.get("orderedPendingIds", [])), "next": queue.get("nextPendingGroup")})
    check("semantic failure check confirms hold-required witnesses and data integrity",
          semantic.get("result") == "HOLD_REQUIRED_WITNESSES" and semantic.get("dataIntegrityPassed") is True
          and semantic.get("blockerIds") == delivery.get("blockerIds")
          and len(semantic.get("findings", [])) == 4,
          {"result": semantic.get("result"), "integrity": semantic.get("dataIntegrityPassed"),
           "findingCount": len(semantic.get("findings", []))})
    check("validation and next-group members are present and agree with the delivery",
          validate.get("failures") == [] and validate.get("freshCheckTotal") == 24596
          and "NEXT_GROUP.json" in name_set,
          {"validation": validate, "nextGroupMemberPresent": "NEXT_GROUP.json" in name_set})
    case_names = [n for n in names if n.startswith("cases/") and n.endswith(".json")]
    check("exact 46 source-bound case records and three procedures are present",
          len(case_names) == 46 and all(f"procedures/{spell}.json" in name_set for spell in TARGETS),
          {"cases": len(case_names), "procedures": [f"procedures/{spell}.json" in name_set for spell in TARGETS]})
    source_packet = json.loads(z.read("input/DD_Rank9_DefenseForm8_CurrentSource_280_DELIVERY.json").decode("utf-8-sig"))
    check("Return280 binds the local independently audited Packet280 source delivery",
          source_packet.get("authority") == AUTHORITY and source_packet.get("targetIds") == TARGETS
          and source_packet.get("archive", {}).get("sha256") == delivery.get("sourcePacket", {}).get("sha256")
          and delivery.get("sourcePacket", {}).get("sha256") == digest((BASE / "rank9_defenseform8_current_source_280_prepared/DD_Rank9_DefenseForm8_CurrentSource_280.zip").read_bytes())["sha256"],
          {"sourceAuthority": source_packet.get("authority"), "sourcePacket": delivery.get("sourcePacket")})

failures = [row for row in checks if not row["passed"]]
report = {"id": "RANK9DEFENSEFORM8-RETURN280-INDEPENDENT-AUDIT",
          "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "PASS" if not failures else "FAIL",
          "archive": {"downloadName": archive_path.name, **archive_digest},
          "delivery": {"downloadName": delivery_path.name, **delivery_digest},
          "authority": delivery.get("authority"), "targetIds": TARGETS,
          "checkCount": len(checks), "passedChecks": len(checks)-len(failures),
          "failedChecks": len(failures), "checks": checks}

received = BASE / "rank9_defenseform8_return280_received"
received.mkdir(parents=True, exist_ok=True)
archive_dest = received / "DD_Rank9_DefenseForm8_Director_Return280_HELD.zip"
delivery_dest = received / "DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json"
shutil.copy2(archive_path, archive_dest)
shutil.copy2(delivery_path, delivery_dest)
report["archive"]["path"] = archive_dest.relative_to(ROOT).as_posix()
report["delivery"]["path"] = delivery_dest.relative_to(ROOT).as_posix()
report_path = BASE / "RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9DEFENSEFORM8-RETURN280-RECEIPT", "status": report["status"],
           "archive": report["archive"], "delivery": report["delivery"],
           "independentAudit": {"path": report_path.relative_to(ROOT).as_posix(), **digest(report_path.read_bytes())},
           "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures)}
receipt_path = BASE / "RANK9DEFENSEFORM8_RETURN280_RECEIPT.json"
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks),
                  "passedChecks": len(checks)-len(failures), "failedChecks": len(failures),
                  "failures": failures, "archive": report["archive"],
                  "delivery": report["delivery"], "receipt": {"path": receipt_path.relative_to(ROOT).as_posix(), "status": receipt["status"]}},
                 ensure_ascii=False, indent=2))
