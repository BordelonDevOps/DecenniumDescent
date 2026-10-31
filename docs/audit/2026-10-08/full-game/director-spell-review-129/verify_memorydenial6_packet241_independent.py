from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_memorydenial6_current_source_241_prepared"
PACKET = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_241.zip"
DELIVERY = OUT / "DD_Rank9_MemoryDenial6_CurrentSource_241_DELIVERY.json"
PREP = BASE / "RANK9MEMORYDENIAL6_SOURCE_PREPARATION_241.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_241.json"
HANDOFF = BASE / "CURRENT_HANDOFF_241.json"
PENDING = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_241.json"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
IDS = ["mind-collapse", "unravel-identity"]


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(part not in ("", ".", "..") for part in p.parts)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def zip_binding(archive: zipfile.ZipFile, name: str) -> dict:
    digest = hashlib.sha256()
    checksum = 0
    size = 0
    with archive.open(name) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
            checksum = zlib.crc32(chunk, checksum)
    return {"bytes": size, "sha256": digest.hexdigest(), "crc32": f"{checksum & 0xffffffff:08x}"}


def file_binding(path: Path) -> dict:
    digest = hashlib.sha256()
    checksum = 0
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
            checksum = zlib.crc32(chunk, checksum)
    return {"bytes": size, "sha256": digest.hexdigest(), "crc32": f"{checksum & 0xffffffff:08x}"}


def main() -> None:
    checks = []

    def ck(name: str, passed: bool, detail=None):
        checks.append({"id": name, "passed": bool(passed), "details": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    delivery = readj(DELIVERY)
    prep = readj(PREP)
    packet_info = file_binding(PACKET)
    ck("packet file matches delivery byte count and SHA-256",
       packet_info["bytes"] == delivery["archive"]["bytes"] and packet_info["sha256"] == delivery["archive"]["sha256"] == prep["packet"]["sha256"], packet_info)
    ck("delivery binds prepared two-identity group and exact authority",
       delivery["status"] == "PREPARED_UNSENT" and delivery["group"] == "rank9-memory-denial6" and
       delivery["pendingIds"] == IDS and delivery["sourceAuthority"] == AUTH and prep["sourceAuthority"] == AUTH and
       prep["group"] == delivery["group"] and prep["pendingIds"] == IDS and prep["checksPassed"] == 11 and prep["checksFailed"] == 0,
       {"group": delivery["group"], "ids": delivery["pendingIds"], "authority": delivery["sourceAuthority"]})
    ck("queue, handoff and pending audit agree on current authority and director-selected group",
       readj(QUEUE)["currentAuthority"] == readj(HANDOFF)["currentAuthority"] == readj(PENDING)["authority"] == AUTH and
       readj(QUEUE)["nextGroup"] == readj(HANDOFF)["nextGroup"] == delivery["group"] and
       readj(PENDING)["preparedNextGroup"]["pendingIds"] == IDS,
       {"next": readj(QUEUE)["nextGroup"], "ids": IDS})

    with zipfile.ZipFile(PACKET) as archive:
        names = archive.namelist()
        manifest = json.loads(archive.read("MANIFEST.json"))
        rows = {row["path"]: row for row in manifest["members"]}
        ck("ZIP CRC, safe member names, uniqueness and packet count",
           archive.testzip() is None and len(names) == len(set(names)) == delivery["members"] and all(safe(n) for n in names),
           {"members": len(names), "testzip": archive.testzip()})
        ck("manifest exactly covers packet payload and binds the same authority/scope",
           manifest["sourceAuthority"] == AUTH and manifest["group"] == delivery["group"] and
           manifest["pendingIds"] == IDS and manifest["memberCountExcludingSelf"] == len(rows) == len(names) - 1 and
           set(rows) == set(names) - {"MANIFEST.json"}, {"manifestRows": len(rows), "archiveMembers": len(names)})
        member_errors = []
        for name, row in rows.items():
            actual = zip_binding(archive, name)
            if actual != {key: row[key] for key in ("bytes", "sha256", "crc32")}:
                member_errors.append(name)
        ck("every packet payload member matches manifest size/SHA/CRC", not member_errors, member_errors[:10])

        candidate = json.loads(archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_241.json"))
        context = json.loads(archive.read("CURRENT_CONTEXT_241.json"))
        request = archive.read("REQUEST_241.txt").decode("utf-8")
        source_bindings = {"sources_current/" + row["path"]: row for row in candidate["sourceBindings"]}
        ck("candidate and context bind only the pending two identities on main at current authority",
           candidate["currentAuthority"] == context["sourceAuthority"] == AUTH and
           candidate["currentBranch"] == "main" and
           candidate["currentPendingGroup"] == {"group": delivery["group"], "spellIds": IDS, "count": 2} and
           context["targetGroup"] == {"group": delivery["group"], "pendingIds": IDS, "count": 2} and
           [row["spellId"] for row in candidate["records"]] == IDS,
           {"authority": candidate["currentAuthority"], "group": candidate["currentPendingGroup"]})
        ck("candidate current source snapshot is the disclosed preparation commit",
           candidate["currentSourceCommit"] == delivery["sourceCommit"] == prep["sourceCommit"] and
           candidate["currentBranch"] == delivery["sourceBranch"] == "main" and
           candidate["currentAuthority"] == AUTH,
           {"branch": delivery["sourceBranch"], "head": delivery["sourceCommit"]})
        pending_rows = [r for r in candidate["records"] if r["spellId"] in IDS]
        ck("both targeted identities remain pending in current native index and catalog",
           len(pending_rows) == 2 and all(r["currentIndexEntry"]["authoredStatus"] == "pending-authored-procedure" and
             r["currentIndexEntry"]["sourceStatus"] == "blocked-pending-operational-review" for r in pending_rows),
           {r["spellId"]: r["currentIndexEntry"]["authoredStatus"] for r in pending_rows})
        ck("Packet241 preserves current Return240, Return239 and Return238 held evidence",
           any(n.endswith("RANK9_CASTINGCOST5_RETURN240_RECEIPT.json") for n in names) and
           any(n.endswith("RANK9_TIMEFATE6_RETURN239_RECEIPT.json") for n in names) and
           any(n.endswith("RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json") for n in names) and
           "CC194-B04" in request and "TF192-B01" in request and "AG190-B01" in request,
           {"return240": any("RETURN240_RECEIPT" in n for n in names), "return239": any("RETURN239_RECEIPT" in n for n in names),
            "return238": any("RETURN238_RECEIPT" in n for n in names)})
        ck("request preserves MD196 blockers and scopes review to the two selected identities",
           all(token in request for token in ["mind-collapse", "unravel-identity", "MD196-B01", "MD196-B02", "Return240", "Review exactly", "Do not edit canonical files"]),
           {"requestBytes": len(request)})

        current_snapshot_rows = {row["path"]: row for row in context["sourceRefresh"]["currentSnapshotBindings"]}
        source_errors = []
        if len(source_bindings) != 120:
            source_errors.append("candidate-binding-count")
        if set(source_bindings) != set("sources_current/" + row["path"] for row in candidate["sourceBindings"]):
            source_errors.append("candidate-path-set")
        if len(current_snapshot_rows) == 0:
            source_errors.append("missing-current-overlay-bindings")
        for name, binding in source_bindings.items():
            row = rows.get(name)
            local = ROOT / Path(*PurePosixPath(name.removeprefix("sources_current/")).parts)
            actual_file = file_binding(local)
            actual_zip = zip_binding(archive, name)
            if (row is None or actual_zip != {"bytes": binding["bytes"], "sha256": binding["sha256"], "crc32": row["crc32"]} or
                actual_file["bytes"] != binding["bytes"] or actual_file["sha256"] != binding["sha256"]):
                source_errors.append(name)
        overlay_errors = []
        for name, binding in current_snapshot_rows.items():
            member = rows.get(name)
            local_path = ROOT / Path(*PurePosixPath(name.removeprefix("current/")).parts)
            local_matches = (name.endswith("/START_HERE.md") or archive.read(name) == local_path.read_bytes())
            if (member is None or not local_matches or member["bytes"] != binding["bytes"] or
                member["sha256"] != binding["sha256"]):
                overlay_errors.append(name)
        ck("all 120 refreshed source bindings match packet, manifest and working-tree files", len(source_bindings) == 120 and not source_errors,
           {"verified": 120 - max(0, len(source_errors) - 1), "errors": source_errors[:10]})
        ck("all captured current overlay files match their packet bindings",
           bool(current_snapshot_rows) and not overlay_errors, {"overlays": len(current_snapshot_rows), "errors": overlay_errors[:10]})

    audit_path = BASE / "RANK9MEMORYDENIAL6_PACKET241_INDEPENDENT_AUDIT.json"
    report = {"id": "RANK9-MEMORYDENIAL6-PACKET241-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
        "archive": {"path": PACKET.relative_to(ROOT).as_posix(), **packet_info},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **file_binding(DELIVERY)},
        "sourceAuthority": AUTH, "group": "rank9-memory-denial6", "pendingIds": IDS,
        "sourceBindingsVerified": 120, "checkCount": len(checks), "checksPassed": sum(c["passed"] for c in checks),
        "checksFailed": sum(not c["passed"] for c in checks), "checks": checks,
        "scopeLimitation": "Verifies packet integrity, authority, scope and source transfer; it does not independently adjudicate game-rule semantics."}
    audit_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-MEMORYDENIAL6-PACKET241-RECEIPT", "status": report["status"],
        "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(), "bytes": audit_path.stat().st_size,
            "sha256": sha(audit_path.read_bytes()), "crc32": crc(audit_path.read_bytes())},
        "checkCount": report["checkCount"], "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"],
        "scopeLimitation": report["scopeLimitation"]}
    (BASE / "RANK9MEMORYDENIAL6_PACKET241_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": report["checkCount"], "passed": report["checksPassed"],
        "failed": report["checksFailed"], "archive": report["archive"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
