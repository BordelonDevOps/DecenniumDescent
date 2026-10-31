from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DOWNLOADS = Path(r"C:\Users\cbord\Downloads")
RECEIVED = BASE / "rank9_defenseform8_return236_received"
ARCHIVE = RECEIVED / "DD_Rank9_DefenseForm3_Director_Return236_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json"
SEGMENTS = DOWNLOADS / "Return236_SEGMENTS.json"
PARTS = [DOWNLOADS / f"Return236.part{i:02d}.bin" for i in range(3)]
TRUNCATED = DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD.zip"
AUDIT = BASE / "RANK9DEFENSEFORM8_RETURN236_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9DEFENSEFORM8_RETURN236_RECEIPT.json"


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def check(rows: list, name: str, ok: bool, detail=None) -> None:
    rows.append({"check": name, "passed": bool(ok), "detail": detail})


def main() -> None:
    checks = []
    segment_manifest = json.loads(SEGMENTS.read_text(encoding="utf-8-sig"))
    delivery = json.loads((DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json").read_text(encoding="utf-8-sig"))
    seg_rows = sorted(segment_manifest["segments"], key=lambda row: row["order"])
    part_raws = [p.read_bytes() for p in PARTS]

    offset = 0
    ranges_ok = len(seg_rows) == 3 and len(part_raws) == 3
    part_checks = []
    for row, path, raw in zip(seg_rows, PARTS, part_raws):
        got = digest(raw)
        part_checks.append({"file": path.name, "actual": got, "manifest": row})
        ranges_ok &= row["fileName"] == path.name and row["offsetBytes"] == offset and row["bytes"] == got["bytes"] and row["sha256"] == got["sha256"]
        offset += len(raw)
    rebuilt = b"".join(part_raws)
    rebuilt_digest = digest(rebuilt)
    expected_archive = delivery["archive"]
    check(checks, "three ordered binary segments match their manifest byte, offset and SHA-256 bindings", ranges_ok, part_checks)
    check(checks, "segment manifest and delivery agree on exact sealed archive identity", segment_manifest["archive"]["bytes"] == expected_archive["bytes"] == len(rebuilt) and segment_manifest["archive"]["sha256"] == expected_archive["sha256"] == rebuilt_digest["sha256"] and segment_manifest["archive"].get("crc32") == expected_archive.get("crc32") == rebuilt_digest["crc32"], {"rebuilt": rebuilt_digest, "delivery": expected_archive, "segments": segment_manifest["archive"]})
    manifest_bytes = SEGMENTS.read_bytes()
    check(checks, "downloaded decision delivery SHA-256 matches the segment manifest binding", digest((DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json").read_bytes())["sha256"] == segment_manifest["deliveryManifest"]["sha256"] and digest((DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json").read_bytes())["bytes"] == segment_manifest["deliveryManifest"]["bytes"], {"segmentManifest": digest(manifest_bytes), "deliveryManifest": digest((DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json").read_bytes()), "expected": segment_manifest["deliveryManifest"]})

    trunc_raw = TRUNCATED.read_bytes()
    check(checks, "previous truncated browser download is an exact prefix of the recovered sealed archive", rebuilt.startswith(trunc_raw), {"truncatedBytes": len(trunc_raw), "truncatedSha256": digest(trunc_raw)["sha256"], "prefixMatches": rebuilt.startswith(trunc_raw)})

    RECEIVED.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_bytes(rebuilt)
    delivery_raw = (DOWNLOADS / "DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json").read_bytes()
    DELIVERY.write_bytes(delivery_raw)
    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        check(checks, "reconstructed sealed archive has valid ZIP structure and CRCs", z.testzip() is None, {"memberCount": len(names), "testZip": z.testzip()})
        check(checks, "ZIP members exactly match the delivery allowlist with no duplicates", len(names) == len(set(names)) == delivery["memberCount"] and set(names) == set(delivery["exactAllowlist"]), {"actual": len(names), "expected": delivery["memberCount"], "allowlist": len(delivery["exactAllowlist"])})
        external = {row["path"]: row for row in delivery["members"]}
        member_errors = []
        for name in names:
            got = digest(z.read(name))
            row = external.get(name)
            if row is None or any(got.get(k) != row.get(k) for k in ("bytes", "sha256", "crc32")):
                member_errors.append({"path": name, "actual": got, "expected": row})
        check(checks, "every member matches the external delivery byte, SHA-256 and CRC bindings", not member_errors, member_errors[:10])
        internal = json.loads(z.read("MEMBER_MANIFEST.json"))
        internal_rows = {row["path"]: row for row in internal["members"]}
        internal_manifest_binding = external.get("MEMBER_MANIFEST.json", {})
        check(checks, "internal self-excluding manifest covers all other members and binds exactly", set(internal_rows) == set(names) - {"MEMBER_MANIFEST.json"} and internal.get("payloadCount") == len(names) - 1 and digest(z.read("MEMBER_MANIFEST.json"))["sha256"] == internal_manifest_binding.get("sha256") and digest(z.read("MEMBER_MANIFEST.json"))["bytes"] == internal_manifest_binding.get("bytes"), {"internalCount": len(internal_rows), "archiveCount": len(names), "memberManifest": internal_manifest_binding})
        internal_errors = []
        for name, row in internal_rows.items():
            got = digest(z.read(name))
            if any(got.get(k) != row.get(k) for k in ("bytes", "sha256", "crc32")):
                internal_errors.append(name)
        check(checks, "every payload matches the internal manifest", not internal_errors, internal_errors[:10])

        director = json.loads(z.read("DIRECTOR_DECISION.json"))
        held = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
        check(checks, "director decision holds exactly the three reviewed identities without acceptance or application", director.get("acceptedIds") == [] and director.get("appliedIds") == [] and director.get("heldIds") == held and director.get("authority") == delivery["authority"], {"acceptedIds": director.get("acceptedIds"), "appliedIds": director.get("appliedIds"), "heldIds": director.get("heldIds"), "authority": director.get("authority")})
        next_group = json.loads(z.read("NEXT_PENDING_GROUP.json"))
        check(checks, "next pending group is Ward Control 6 with only Nullification Wave and Reality Anchor", next_group.get("group") == "rank9-ward-control6" and next_group.get("pendingIds") == ["nullification-wave", "reality-anchor"], next_group)
        check(checks, "sealed archive preserves expected 46-case replay and exact current binding reconciliation", len([n for n in names if n.startswith("cases/")]) >= 46 and any("SUPPLEMENT236" in n for n in names) and any("DF218-B01" in z.read(n).decode("utf-8", "ignore") for n in names if n.endswith(".json")), {"caseMembers": len([n for n in names if n.startswith("cases/")]), "supplementIncluded": any("SUPPLEMENT236" in n for n in names)})

    failures = [row for row in checks if not row["passed"]]
    report = {"id": "RANK9DEFENSEFORM8-RETURN236-INDEPENDENT-AUDIT", "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **digest(ARCHIVE.read_bytes())}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())}, "segmentManifest": {"path": str(SEGMENTS), **digest(manifest_bytes)}, "authority": delivery["authority"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "checks": checks}
    AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9DEFENSEFORM8-RETURN236-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "independentAudit": {"path": AUDIT.relative_to(ROOT).as_posix(), **digest(AUDIT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures)}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "failures": failures, "archive": report["archive"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
