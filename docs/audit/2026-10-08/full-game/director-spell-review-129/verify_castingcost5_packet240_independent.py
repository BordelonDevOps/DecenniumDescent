from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_castingcost5_current_source_240_prepared"
PACKET = OUT / "DD_Rank9_CastingCost5_CurrentSource_240.zip"
DELIVERY = OUT / "DD_Rank9_CastingCost5_CurrentSource_240_DELIVERY.json"
OLD222 = BASE / "rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_240.json"
HANDOFF = BASE / "CURRENT_HANDOFF_240.json"
PENDING = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_240.json"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_239.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_239.json"
PENDING0 = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_239.json"
TARGET = "unholy-ascendance"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def info(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def main() -> None:
    checks: list[dict] = []

    def ck(name: str, passed: bool, detail=None) -> None:
        checks.append({"id": name, "passed": bool(passed), "details": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    delivery = readj(DELIVERY)
    packet_raw = PACKET.read_bytes()
    queue, handoff, pending = readj(QUEUE), readj(HANDOFF), readj(PENDING)
    index, catalog = readj(INDEX), readj(CATALOG)
    r222_receipt = readj(BASE / "RANK9_CASTINGCOST5_RETURN222_RECEIPT.json")
    r222_audit = readj(BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json")
    r239_receipt = readj(BASE / "RANK9_TIMEFATE6_RETURN239_RECEIPT.json")
    r239_audit = readj(BASE / "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json")
    r238_delivery = readj(BASE / "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json")

    ck("packet bytes/hash/CRC match delivery sidecar", all(digest(packet_raw)[key] == delivery["archive"][key] for key in ("bytes", "sha256", "crc32")) and delivery["status"] == "PREPARED_UNSENT", digest(packet_raw))
    ck("authority is current at 811/37/0 and 535/173", delivery["sourceAuthority"] == queue["currentAuthority"] == handoff["currentAuthority"] == pending["authority"] == AUTH and index["authoredCounts"] == {"reviewed": 811, "pending": 37} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535, delivery["sourceAuthority"])
    ck("only unholy-ascendance is the pending Casting/Cost5 target", delivery["group"] == "rank9-casting-cost5" and delivery["pendingIds"] == [TARGET] and queue["nextGroup"] == handoff["nextGroup"] == delivery["group"] and pending["preparedNextGroup"]["pendingIds"] == [TARGET] and TARGET in pending["pendingIds"], {"group": delivery["group"], "ids": delivery["pendingIds"]})
    index_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    ck("target remains pending and non-operational; perfect-spell is outside pending", index_rows[TARGET]["authoredStatus"] == "pending-authored-procedure" and index_rows[TARGET]["sourceStatus"] == "blocked-pending-operational-review" and catalog_rows[TARGET].get("operational") is None and "perfect-spell" not in pending["pendingIds"], {"target": index_rows[TARGET]["authoredStatus"], "perfectSpellPending": "perfect-spell" in pending["pendingIds"]})
    ck("Return222 preserves perfect-spell acceptance and CC194-B04 hold", r222_audit["status"] == "PASS" and r222_audit["checksFailed"] == 0 and r222_receipt["acceptedIds"] == ["perfect-spell"] and r222_receipt["heldIds"] == [TARGET] and r222_receipt["blockers"][TARGET] == ["CC194-B04"], r222_receipt["blockers"])
    ck("Return239 and Return238 independent audits preserve latest holds", r239_audit["checksFailed"] == 0 and r239_receipt["heldIds"] == ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"] and r238_delivery["heldIds"] == ["absolute-domination", "puppetmaster-s-realm"], {"timefate": r239_receipt["heldIds"], "agency": r238_delivery["heldIds"]})

    with zipfile.ZipFile(PACKET) as archive:
        names = archive.namelist()
        manifest = json.loads(archive.read("MANIFEST.json"))
        rows = {row["path"]: row for row in manifest["members"]}
        ck("ZIP CRC is clean, paths are safe and unique", archive.testzip() is None and len(names) == len(set(names)) and all(safe(name) for name in names), {"members": len(names)})
        ck("manifest exactly covers every payload member", manifest["sourceAuthority"] == AUTH and manifest["group"] == delivery["group"] and manifest["pendingIds"] == [TARGET] and manifest["payloadMemberCount"] == len(rows) == len(names) - 1 and set(rows) == set(names) - {"MANIFEST.json"}, {"rows": len(rows), "names": len(names)})
        mismatches = []
        for name, row in rows.items():
            if digest(archive.read(name)) != {key: row[key] for key in ("bytes", "sha256", "crc32")}:
                mismatches.append(name)
        ck("all payload members match manifest size/SHA/CRC", not mismatches, mismatches[:10])

        candidate = json.loads(archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_240.json"))
        context = json.loads(archive.read("CURRENT_CONTEXT_240.json"))
        source_rows = {row["path"]: row for row in candidate["sourceBindings"]}
        ck("current candidate and context bind exact identity, authority and branch", candidate["currentAuthority"] == context["sourceAuthority"] == AUTH and candidate["currentPendingGroup"] == {"group": "rank9-casting-cost5", "spellIds": [TARGET], "count": 1} and candidate["currentBranch"] == candidate["sourceSnapshot"]["branch"] == "main" and candidate["sourceSnapshot"]["headCommit"] == delivery["sourceSnapshot"]["headCommit"] and context["pendingIds"] == [TARGET], {"authority": candidate["currentAuthority"], "group": candidate["currentPendingGroup"]})
        ck("only accepted/applied counterparts are excluded from this review", candidate["excludedAcceptedAppliedIds"] == ["perfect-spell", "ritual-mastery", "world-rewrite", "resonance-perfection"] and candidate["priorUnholyBlocker"] == "CC194-B04", candidate["excludedAcceptedAppliedIds"])
        source_errors = []
        source_manifest_rows = rows
        for path, binding in source_rows.items():
            name = "sources_current/" + path
            raw = archive.read(name)
            local = (ROOT / Path(path)).read_bytes()
            mr = source_manifest_rows[name]
            if len(raw) != binding["bytes"] or hashlib.sha256(raw).hexdigest() != binding["sha256"] or raw != local or digest(raw) != {key: mr[key] for key in ("bytes", "sha256", "crc32")}:
                source_errors.append(path)
        ck("all 117 refreshed source bindings match packet, manifest and working-tree bytes", len(source_rows) == 117 and not source_errors, {"matched": len(source_rows) - len(source_errors), "errors": source_errors[:10]})
        authority_members = {
            "authority_current/authored_review_index.json": INDEX,
            "authority_current/catalog.json": CATALOG,
            "authority_current/CURRENT_SPELL_QUEUE_239_INPUT.json": QUEUE0,
            "authority_current/CURRENT_HANDOFF_239_INPUT.json": HANDOFF0,
            "authority_current/CURRENT37_PENDING_IDENTITY_AUDIT_239_INPUT.json": PENDING0,
        }
        authority_errors = [name for name, path in authority_members.items() if archive.read(name) != path.read_bytes()]
        ck("current authority and pending-hold snapshots are included byte-exactly", not authority_errors, authority_errors)
        historical_errors = []
        with zipfile.ZipFile(OLD222) as old:
            for name in old.namelist():
                if name.startswith("sources_current/") or name == "MANIFEST.json":
                    continue
                if archive.read("historical_packet_222/" + name) != old.read(name):
                    historical_errors.append(name)
        ck("prior Packet222 context is preserved byte-exactly under a historical namespace", not historical_errors, historical_errors[:10])
        history_paths = {
            "authority_history/" + path.relative_to(ROOT).as_posix(): path
            for path in [
                BASE / "RANK9_CASTINGCOST5_RETURN222_RECEIPT.json", BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json",
                BASE / "RANK9_CASTINGCOST5_DIRECTOR_DECISION_222.json", BASE / "RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_222.json",
                BASE / "RANK9_CASTINGCOST5_APPLICATION_222.json", BASE / "RANK9_CASTINGCOST5_APPLICATION_VALIDATION_222.json",
                BASE / "RANK9_CASTINGCOST5_INDEX_OPERATIONS_222.json",
                BASE / "RANK9_TIMEFATE6_RETURN239_RECEIPT.json", BASE / "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json",
                BASE / "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip",
                BASE / "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
                BASE / "RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json", BASE / "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json",
                BASE / "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip",
                BASE / "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
            ]
        }
        history_errors = [name for name, path in history_paths.items() if archive.read(name) != path.read_bytes()]
        ck("Return222, Return239 and Return238 audited records are included byte-exactly", not history_errors, history_errors)

        request = archive.read("REQUEST_240.txt").decode("utf-8")
        ck("request scopes review to unholy-ascendance, preserves CC194-B04 and forbids application", all(token in request for token in [TARGET, "CC194-B04", "Review only", "Keep every acceptance unapplied", "perfect-spell"]), {"requestBytes": len(request)})
        ck("candidate carries the independently audited Return222, Return239 and Return238 bindings", candidate["currentCastingCostReturn222AuditBinding"]["sha256"] == info(BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json")["sha256"] and candidate["currentTimeFateReturn239AuditBinding"]["sha256"] == info(BASE / "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json")["sha256"] and candidate["currentAgencyControlReturn238AuditBinding"]["sha256"] == info(BASE / "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json")["sha256"], None)

    report = {
        "id": "RANK9-CASTING-COST5-PACKET240-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
        "archive": info(PACKET),
        "deliveryManifest": info(DELIVERY),
        "sourceAuthority": AUTH,
        "group": "rank9-casting-cost5",
        "pendingIds": [TARGET],
        "sourceBindingsVerified": 117,
        "checkCount": len(checks),
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": sum(not row["passed"] for row in checks),
        "checks": checks,
        "scopeLimitation": "Validates source transfer, identity scope, current authority, preserved historical decisions and packet integrity; it does not independently adjudicate the underlying game rules.",
    }
    report_path = BASE / "RANK9_CASTINGCOST5_PACKET240_INDEPENDENT_AUDIT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-CASTING-COST5-PACKET240-RECEIPT", "status": report["status"], "archive": report["archive"],
               "deliveryManifest": report["deliveryManifest"], "independentAudit": info(report_path),
               "checkCount": report["checkCount"], "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"],
               "scopeLimitation": report["scopeLimitation"]}
    (BASE / "RANK9_CASTINGCOST5_PACKET240_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": report["checkCount"], "passed": report["checksPassed"], "failed": report["checksFailed"], "packet": report["archive"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
