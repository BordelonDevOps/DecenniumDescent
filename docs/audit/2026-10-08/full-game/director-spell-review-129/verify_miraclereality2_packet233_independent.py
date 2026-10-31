from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_miraclereality2_current_source_233_prepared"
ARCHIVE = OUT / "DD_Rank9_MiracleReality2_CurrentSource_233_CORRECTED_V2.zip"
DELIVERY = OUT / "DD_Rank9_MiracleReality2_CurrentSource_233_CORRECTED_V2_DELIVERY.json"
CANDIDATE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_233.json"
CONTEXT = OUT / "CURRENT_CONTEXT_233.json"
REQUEST = OUT / "REQUEST_233.txt"
TARGETS = ["divine-intervention-greater", "wish"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)


def file_info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def main() -> None:
    checks: list[dict] = []

    def check(name: str, ok: bool, details=None):
        checks.append({"id": name, "status": "PASS" if ok else "FAIL", "details": details})
        assert ok, (name, details)

    delivery_raw = DELIVERY.read_bytes()
    delivery, candidate, context = read(DELIVERY), read(CANDIDATE), read(CONTEXT)
    request = REQUEST.read_text(encoding="utf-8")
    queue_path, handoff_path, pending_path = AUDIT / "CURRENT_SPELL_QUEUE_233.json", AUDIT / "CURRENT_HANDOFF_233.json", AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_233.json"
    queue, handoff, pending = read(queue_path), read(handoff_path), read(pending_path)
    idx = read(ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")
    hist_candidate = read(ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_miracle_reality_2_source_conference_01.json")
    notes = read(AUDIT / "RANK9MIRACLEREALITY2_NEXT_CONFERENCE_NOTES_129.json")
    submission = read(AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_232_SUBMISSION.json")

    actual_archive = file_info(ARCHIVE)
    check("archive-binding", delivery["archive"] == actual_archive, actual_archive)
    check("delivery-identity-and-status", delivery["id"] == "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-DELIVERY-233" and delivery["status"] == "PREPARED_UNAUDITED_UNSENT")
    check("source-authority", delivery["sourceAuthority"] == context["sourceAuthority"] == AUTHORITY and delivery["sourceCommitBase"] == context["sourceCommitBase"])
    check("branch-main", delivery["sourceBranch"] == "main" and context["sourceBranch"] == "main")
    check("target-scope", delivery["group"] == context["targetGroup"]["group"] == "rank9-miracle-reality2" and delivery["pendingIds"] == TARGETS)
    check("no-acceptance-or-application", delivery["accepted"] is False and delivery["applied"] is False and delivery["canonicalChanges"] is False and delivery["applicationChanges"] is False)
    check("live-index-counts", idx["authoredCounts"] == {"reviewed": 811, "pending": 37} and idx["representationCounts"]["completeReviewedStandaloneProcedures"] == 535)
    current_pending = sorted(row["id"] for row in idx["entries"] if row.get("authoredStatus") == "pending-authored-procedure")
    check("exact-live-pending-set", len(current_pending) == 37 and set(TARGETS).issubset(current_pending))
    check("queue-authority-and-target", queue["currentAuthority"] == AUTHORITY and queue["nextPreparedRequest"]["pendingIds"] == TARGETS)
    check("pending-audit-identity-set", pending["pendingCount"] == 37 and TARGETS[0] in pending["pendingIds"] and TARGETS[1] in pending["pendingIds"])
    check("handoff-points-to-packet", handoff["currentPacket"]["sha256"] == actual_archive["sha256"] and handoff["currentPacketDelivery"]["sha256"] == sha(delivery_raw))
    check("preserved-history-status", hist_candidate["status"] == "SOURCE_CONFERENCE_PREPARED_UNSENT" and notes["status"] == "PREPARED_UNSENT_NOT_ACCEPTED")
    check("historical-question-preservation", len(hist_candidate["questions"]) == 24 and len(notes["completeOriginalQuestionsUnchanged"]) == 24 and len(notes["focusedAdditionalQuestions"]) == 2)
    check("historical-case-preservation", len(notes["requiredNewCases"]) == 4 and len(hist_candidate["futureCaseRequirements"]) == 8 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 8)
    check("all-source-bindings-refreshed", delivery["sourceBindings"] == len(candidate["sourceBindings"]) == 153 and candidate["sourceBindingRefresh"]["sourceFiles"] == 153)
    check("current-target-records", [row["spellId"] for row in candidate["currentReviewTargets"]] == TARGETS)
    check("prior-return232-audit-present", submission["status"] == "RETURN232_AUDITED_HELD_811_37_0" and submission["directorReturn"]["heldIds"] == ["astral-projection", "imprisonment"])
    check("request-scope-and-boundaries", all(token in request for token in TARGETS + ["Do not import D&D Wish", "all eight future-case requirements", "Do not modify canonical files"]))
    check("request-does-not-authorize-application", "apply any spell" in request and "accepted/applied/held" in request)

    with zipfile.ZipFile(ARCHIVE) as z:
        infos = z.infolist()
        names = [x.filename for x in infos]
        check("zip-integrity", z.testzip() is None)
        check("unique-safe-member-names", len(names) == len(set(names)) and all(safe(n) for n in names))
        manifest = json.loads(z.read("MANIFEST.json"))
        members = manifest["members"]
        check("manifest-member-count", len(members) == len(names) - 1 == delivery["manifestBindings"])
        check("manifest-identity-scope", manifest["id"] == "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-MANIFEST-233" and manifest["pendingIds"] == TARGETS)
        check("manifest-source-authority", manifest["sourceAuthority"] == AUTHORITY and manifest["sourceBranch"] == "main")
        member_paths = {row["path"] for row in members}
        check("request-delivery-in-archive", {"REQUEST_233.txt", "CURRENT_CONTEXT_233.json", "CURRENT_SOURCE_CONFERENCE_CANDIDATE_233.json"}.issubset(member_paths))
        tracking_paths = {
            "currentQueue": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_233.json",
            "currentHandoff": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_233.json",
            "currentPendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_233.json",
        }
        tracking_ok = True
        for key, path in tracking_paths.items():
            member = "current/" + path
            tracking_ok = tracking_ok and member in member_paths
            embedded = z.read(member) if member in member_paths else b""
            pointed = candidate["currentAuthorityEvidence"][key]
            tracking_ok = tracking_ok and (len(embedded), sha(embedded), crc(embedded)) == (pointed["bytes"], pointed["sha256"], pointed["crc32"])
        check("current-233-tracking-bindings-embedded", tracking_ok)
        each_ok = True
        for row in members:
            raw = z.read(row["path"])
            if (len(raw), sha(raw), crc(raw)) != (row["bytes"], row["sha256"], row["crc32"]):
                each_ok = False
                break
        check("all-member-hashes-and-crcs", each_ok)
        current_source_rows = [row for row in members if row["path"].startswith("sources_current/")]
        check("current-source-member-coverage", len(current_source_rows) == 153)
        source_map = {row["path"][len("sources_current/"):]: row for row in current_source_rows}
        binding_match = all(source_map.get(row["path"], {}).get("sha256") == row["sha256"] for row in candidate["sourceBindings"])
        check("candidate-to-archive-source-bindings", binding_match)
        check("previous-returns-carried-forward", all(f"evidence/RETURN{n}.zip" in member_paths and f"evidence/RETURN{n}_DELIVERY.json" in member_paths for n in (228, 229, 230, 231, 232)))
        check("historical-conference-carried-forward", "historical/DD_Rank9_Miracle_Reality_2_Source_Conference_01.zip" in member_paths)
        check("previous-return-audits-and-receipts-carried", all(f"current/evidence/RETURN{n}_INDEPENDENT_AUDIT.json" in member_paths and f"current/evidence/RETURN{n}_RECEIPT.json" in member_paths for n in (228, 229, 230, 231, 232)))

    audit = {
        "id": "RANK9MIRACLEREALITY2-PACKET233-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS", "failedChecks": 0,
        "archive": actual_archive, "deliveryManifest": file_info(DELIVERY), "candidate": file_info(CANDIDATE),
        "context": file_info(CONTEXT), "request": file_info(REQUEST), "targetGroup": "rank9-miracle-reality2",
        "pendingIds": TARGETS, "sourceBindings": 153, "memberCount": len(members) + 1,
        "questionCount": 26, "requiredMainCases": 4, "futureRequirements": 8,
        "checks": checks, "checkCount": len(checks), "failedChecks": 0,
        "scope": "Independent packet integrity, authority, target, carry-forward, and manifest review only; no game runtime or spell application.",
    }
    audit_path = AUDIT / "RANK9MIRACLEREALITY2_PACKET_233_CORRECTED_V2_INDEPENDENT_AUDIT.json"
    receipt_path = AUDIT / "RANK9MIRACLEREALITY2_PACKET_233_CORRECTED_V2_RECEIPT.json"
    audit_raw = (json.dumps(audit, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    audit_path.write_bytes(audit_raw)
    receipt = {"id": "RANK9MIRACLEREALITY2-PACKET233-INDEPENDENT-RECEIPT", "status": "PASS", "audit": file_info(audit_path),
               "archive": actual_archive, "deliveryManifest": file_info(DELIVERY), "targetGroup": "rank9-miracle-reality2",
               "pendingIds": TARGETS, "checkCount": len(checks), "failedChecks": 0, "canonicalChanges": False, "applicationChanges": False}
    receipt_raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    receipt_path.write_bytes(receipt_raw)

    packet_path = AUDIT / "RANK9MIRACLEREALITY2_PACKET_233.json"
    packet = read(packet_path)
    packet.update({"status": "PACKET233_INDEPENDENT_AUDIT_PASS_UNSENT", "independentAudit": file_info(audit_path), "auditReceipt": file_info(receipt_path)})
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    q = read(AUDIT / "CURRENT_SPELL_QUEUE_233.json")
    q["nextPreparedRequest"].update({"status": "PACKET233_INDEPENDENT_AUDIT_PASS_UNSENT", "independentAudit": file_info(audit_path), "auditReceipt": file_info(receipt_path)})
    q["currentPacketAudit"] = file_info(audit_path)
    q["currentPacketAuditReceipt"] = file_info(receipt_path)
    q["status"] = q["packetStatus"] = "PACKET233_INDEPENDENT_AUDIT_PASS_UNSENT_811_37_0"
    (AUDIT / "CURRENT_SPELL_QUEUE_233.json").write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    h = read(AUDIT / "CURRENT_HANDOFF_233.json")
    h["nextPreparedRequest"] = q["nextPreparedRequest"]
    h["currentQueueBinding"] = file_info(AUDIT / "CURRENT_SPELL_QUEUE_233.json")
    h["currentPacketAudit"] = file_info(audit_path)
    h["currentPacketAuditReceipt"] = file_info(receipt_path)
    h["status"] = "PACKET233_INDEPENDENT_AUDIT_PASS_UNSENT_811_37"
    h["resumePriority"] = "Packet233 independently audited PASS; submit to GPT, monitor and ping if needed, audit the sealed return, and apply only exact accepted IDs."
    (AUDIT / "CURRENT_HANDOFF_233.json").write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks": len(checks), "failedChecks": 0, "audit": str(audit_path), "receipt": str(receipt_path), "archiveSha256": actual_archive["sha256"]}, indent=2))


if __name__ == "__main__":
    main()
