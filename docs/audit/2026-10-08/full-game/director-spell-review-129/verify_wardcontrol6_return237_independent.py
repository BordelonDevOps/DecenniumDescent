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
RECEIVED = BASE / "rank9_wardcontrol6_return237_received"
ARCHIVE = RECEIVED / "DD_Rank9_WardControl2_Director_Return237.zip"
DELIVERY = RECEIVED / "DD_Rank9_WardControl2_Director_Return237_DELIVERY.json"
SOURCE_PACKET = BASE / "rank9_wardcontrol6_source_packet_237_refreshed/DD_Rank9_WardControl6_CurrentSource_237.zip"
REPORT = BASE / "RANK9_WARDCONTROL6_RETURN237_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_WARDCONTROL6_RETURN237_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["nullification-wave", "reality-anchor"]
BLOCKERS = {"nullification-wave": "WC188-B01", "reality-anchor": "WC188-B02"}
NEXT = {"group": "rank9-agency-control9", "spellIds": ["absolute-domination", "puppetmaster-s-realm"]}
checks: list[dict] = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def matches(raw: bytes, expected: dict) -> bool:
    got = digest(raw)
    return isinstance(expected, dict) and all(got.get(k) == expected.get(k) for k in ("bytes", "sha256")) and (expected.get("crc32") is None or got["crc32"] == expected["crc32"])


def safe(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery_raw = DELIVERY.read_bytes()
delivery = read_json(delivery_raw)
archive_raw = ARCHIVE.read_bytes()
archive_hash = digest(archive_raw)
delivery_hash = digest(delivery_raw)
check("downloaded Return237 ZIP exactly matches its delivery size, SHA-256 and CRC32", delivery.get("return") == 237 and pathlib.Path(delivery.get("archive", {}).get("path", "")).name == ARCHIVE.name and matches(archive_raw, delivery.get("archive", {})), {"actual": archive_hash, "expected": delivery.get("archive")})

duplicate_manifests = [
    pathlib.Path(r"C:\Users\cbord\Downloads\DD_Rank9_WardControl2_Director_Return237_DELIVERY (1).json"),
    pathlib.Path(r"C:\Users\cbord\Downloads\DD_Rank9_WardControl2_Director_Return237_DELIVERY (2).json"),
]
duplicate_failures = [str(p) for p in duplicate_manifests if not p.exists() or p.read_bytes() != delivery_raw]
check("repeated browser downloads of the delivery JSON are byte-identical", not duplicate_failures, duplicate_failures)

with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    name_set = set(names)
    check("ZIP central directory is valid and all names are unique and safe", archive.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names), {"members": len(names), "unique": len(name_set)})
    allowlist = delivery.get("exactAllowlist", [])
    member_rows = delivery.get("members", [])
    external = {row.get("path"): row for row in member_rows if isinstance(row, dict)}
    check("delivery allowlist, external member list and ZIP exactly agree", len(names) == delivery.get("memberCount") == len(allowlist) == len(external) == 50 and set(allowlist) == name_set == set(external), {"zip": len(names), "allowlist": len(allowlist), "external": len(external), "declared": delivery.get("memberCount")})
    external_bad = [name for name in names if name not in external or not matches(archive.read(name), external[name])]
    check("every ZIP member matches external delivery SHA-256/size/CRC32", not external_bad, external_bad[:15])

    manifest_raw = archive.read("MEMBER_MANIFEST.json")
    manifest = read_json(manifest_raw)
    manifest_map = {row.get("path"): row for row in manifest.get("members", []) if isinstance(row, dict)}
    check("embedded manifest covers exactly the 49 non-self ZIP members", manifest.get("return") == 237 and manifest.get("memberCountExcludingSelf") == 49 and manifest.get("manifestSelfExcluded") is True and set(manifest_map) == name_set - {"MEMBER_MANIFEST.json"}, {"manifestCount": len(manifest_map), "declared": manifest.get("memberCountExcludingSelf")})
    internal_bad = [name for name in manifest_map if not matches(archive.read(name), manifest_map[name])]
    check("every non-self ZIP member matches embedded hash, size and CRC32", not internal_bad, internal_bad[:15])

    decision = read_json(archive.read("DIRECTOR_DECISION.json"))
    counts = read_json(archive.read("COUNTS.json"))
    case_index = read_json(archive.read("CASE_INDEX.json"))
    preservation = read_json(archive.read("PRESERVATION.json"))
    hold_register = read_json(archive.read("HOLD_REGISTER.json"))
    source_bindings = read_json(archive.read("SOURCE_BINDINGS.json"))
    package_integrity = delivery.get("packageIntegrity", {})
    check("decision remains held and unapplied for only the two requested identities", decision.get("accepted") is False and decision.get("applied") is False and decision.get("acceptedIds") == delivery.get("acceptedIds") == [] and decision.get("appliedIds") == delivery.get("appliedIds") == [] and decision.get("heldIds") == delivery.get("heldIds") == TARGETS and delivery.get("accepted") is False and delivery.get("applied") is False, {"acceptedIds": decision.get("acceptedIds"), "appliedIds": decision.get("appliedIds"), "heldIds": decision.get("heldIds")})
    decision_blockers = {row.get("spellId"): (row.get("blockerIds") or [None])[0] for row in decision.get("decisions", [])}
    hold_ids = {row.get("spellId"): row.get("id") for row in hold_register.get("holds", []) if row.get("spellId") in TARGETS}
    check("both retained blockers alias the exact Return188 gates", decision_blockers == BLOCKERS and hold_ids == BLOCKERS and set(delivery.get("blockerIds", [])) == set(BLOCKERS.values()), {"decision": decision_blockers, "holds": hold_ids, "delivery": delivery.get("blockerIds")})
    check("authority is unchanged and next group is Agency Control9", decision.get("authorityBefore") == decision.get("authorityAfter") == AUTHORITY and delivery.get("authority") == AUTHORITY and decision.get("nextPendingGroup") == delivery.get("nextPendingGroup") == NEXT, {"before": decision.get("authorityBefore"), "after": decision.get("authorityAfter"), "next": decision.get("nextPendingGroup")})
    check("canonical files, application and downstream approvals remain explicitly out of scope", decision.get("canonicalChanged") is False and decision.get("applied") is False and "No application" in delivery.get("qualification", "") and "or runtime/" in delivery.get("qualification", ""), {"canonicalChanged": decision.get("canonicalChanged"), "applied": decision.get("applied"), "qualification": delivery.get("qualification")})

    all_integrity = package_integrity.get("checks", [])
    check("the sealed package reports all 153 integrity checks passing", package_integrity.get("status") == "PASS" and package_integrity.get("checkCount") == 153 and len(all_integrity) == 153 and all(x.get("pass") is True for x in all_integrity) and package_integrity.get("failedCount") == 0 and package_integrity.get("failures") == [], {"status": package_integrity.get("status"), "checkCount": package_integrity.get("checkCount"), "failedCount": package_integrity.get("failedCount")})

    case_rows = case_index.get("cases", [])
    case_names = [row.get("path") for row in case_rows]
    preserved = preservation.get("cases", [])
    preserved_names = [row.get("path") for row in preserved]
    corrected_names = sorted(n for n in names if n.startswith("cases/corrected/"))
    case_hash_failures = [row.get("path") for row in preserved if row.get("path") not in name_set or not matches(archive.read(row["path"]), row)]
    aggregate = {key: sum(int(row.get(key, 0)) for row in case_rows) for key in ("events", "forwardOperations", "inverseOperations")}
    check("14 preserved and two corrected trace members reconcile with the case index", len(case_rows) == 16 and len(preserved) == 14 and set(preserved_names) == {n for n in names if n.startswith("cases/preserved/")} and len(corrected_names) == 2 and all(n in name_set for n in corrected_names) and not case_hash_failures and aggregate == {"events": 324, "forwardOperations": 648, "inverseOperations": 648} and all(row.get("numericReplay") == "PASS" for row in case_rows), {"cases": len(case_rows), "preserved": len(preserved), "corrected": corrected_names, "aggregates": aggregate, "preservationBindingFailures": case_hash_failures[:10]})
    integrity = read_json(archive.read("DATA_INTEGRITY_CHECK.json"))
    clocks = read_json(archive.read("CLOCK_CHECK.json"))
    actor_access = read_json(archive.read("ACTOR_ACCESS_CHECK.json"))
    source_check = read_json(archive.read("SOURCE_CHECK.json"))
    check("data, clock, actor-access and source checks all pass at their declared counts", len(integrity.get("checks", [])) == integrity.get("checkCount") == 3936 and all(r.get("pass") is True for r in integrity["checks"]) and len(clocks.get("checks", [])) == clocks.get("checkCount") == 2412 and all(r.get("pass") is True for r in clocks["checks"]) and len(actor_access.get("checks", [])) == actor_access.get("checkCount") == 125 and all(r.get("pass") is True for r in actor_access["checks"]) and len(source_check.get("checks", [])) == source_check.get("checkCount") == 561 and all(r.get("pass") is True for r in source_check["checks"]), {"data": integrity.get("checkCount"), "clock": clocks.get("checkCount"), "actorAccess": actor_access.get("checkCount"), "source": source_check.get("checkCount")})
    check("published counts agree with the case index and both spell-specific procedures", counts == delivery.get("counts") == decision.get("counts") and counts.get("caseFiles") == 16 and counts.get("procedures") == 2 and counts.get("heldIds") == 2 and all(("procedures/" + sid + ".json") in name_set for sid in TARGETS), {"counts": {k: counts.get(k) for k in ("caseFiles", "events", "forwardOperations", "inverseOperations", "sourceBindingsVerified", "procedures", "heldIds")}})

    # Independently bind the return's 91 source rows to the exact current-source Packet237 archive.
    current_packet_hash = digest(SOURCE_PACKET.read_bytes())
    packet_binding = delivery.get("sourcePacket", {})
    source_rows = source_bindings.get("currentBindings", [])
    with zipfile.ZipFile(SOURCE_PACKET) as source_zip:
        source_members = set(source_zip.namelist())
        source_failures = []
        for row in source_rows:
            member = "sources_current/" + row["path"]
            if member not in source_members or not matches(source_zip.read(member), row):
                source_failures.append(row["path"])
    check("return binds the exact independently audited Packet237 and its 91 current source files", matches(SOURCE_PACKET.read_bytes(), packet_binding) and len(source_rows) == counts.get("sourceBindingsVerified") == 91 and not source_failures, {"packet": current_packet_hash, "declaredPacket": packet_binding, "sourceRows": len(source_rows), "failures": source_failures[:12]})

    # Preserve the limitation explicitly: Return219 had an inline ruling only, not a sealed archive of the 14 case bytes.
    inline = read_json(archive.read("preserved/RETURN219_INLINE_CAPTURE.json"))
    check("Return219 provenance is identified as inline-only rather than misrepresented as a sealed base archive", inline.get("status") == "INLINE_DIRECTOR_RULING_RECEIVED_NO_SEALED_ARCHIVE" and "not a director ZIP" in inline.get("receiptScope", "") and len(preserved) == 14, {"status": inline.get("status"), "receiptScope": inline.get("receiptScope"), "note": "The 14 case files self-match Return237's preservation manifest; exact byte-for-byte comparison against a Return219 sealed archive is unavailable because Return219 has no sealed archive."})

failures = [item for item in checks if not item["passed"]]
report = {"id": "RANK9-WARD-CONTROL6-RETURN237-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL",
          "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_hash}, "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_hash},
          "authority": delivery.get("authority"), "acceptedIds": delivery.get("acceptedIds"), "appliedIds": delivery.get("appliedIds"), "heldIds": delivery.get("heldIds"), "blockerIds": delivery.get("blockerIds"), "nextPendingGroup": delivery.get("nextPendingGroup"),
          "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "checks": checks,
          "scopeLimitation": "The prior Return219 has no sealed archive, so its 14 original trace bytes cannot be independently compared to the preservation copies. Return237's own preservation hashes, manifest hashes, and case-index bindings pass."}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9-WARD-CONTROL6-RETURN237-RECEIPT", "status": report["status"], "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
           "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "scopeLimitation": report["scopeLimitation"]}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archive": report["archive"], "heldIds": delivery.get("heldIds"), "next": delivery.get("nextPendingGroup"), "scopeLimitation": report["scopeLimitation"]}, ensure_ascii=False, indent=2))
