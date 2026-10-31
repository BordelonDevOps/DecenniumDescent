from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    audit_path = BASE / "RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["acceptedIds"] == audit["appliedIds"] == []
    assert audit["heldIds"] == ["mind-collapse", "unravel-identity"]
    now = datetime.now(timezone.utc).isoformat()
    return_zip = BASE / "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip"
    return_delivery = BASE / "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json"
    return_zip_info, return_delivery_info = binding(return_zip), binding(return_delivery)
    audit_info, receipt_info = binding(audit_path), binding(receipt_path)
    status = "RETURN241_AUDITED_HELD_NEXT_KNOWLEDGE_REVELATION5_811_37_0"

    submission_path = BASE / "RANK9MEMORYDENIAL6_PACKET_241_SUBMISSION.json"
    submission = read(submission_path)
    submission.update({"status": status, "return": 241, "returnArchive": return_zip_info,
        "returnDeliveryManifest": return_delivery_info, "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info, "acceptedIds": [], "appliedIds": [],
        "heldIds": audit["heldIds"], "blockers": audit["blockers"],
        "nextGroup": audit["nextPendingGroup"], "returnedAtUtc": now,
        "canonicalChanges": False, "githubChanges": False})
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_241.json"
    pending = read(pending_path)
    pending["recordedAtUtc"] = now
    pending["status"] = status
    pending["lastDirectorReturn"] = {"return": 241, "group": "rank9-memory-denial6",
        "acceptedIds": [], "appliedIds": [], "heldIds": audit["heldIds"],
        "blockers": audit["blockers"], "conditionalQualifications": audit["conditionalQualifications"],
        "independentAudit": audit_info, "receipt": receipt_info, "archive": return_zip_info,
        "deliveryManifest": return_delivery_info, "nextPendingGroup": audit["nextPendingGroup"]}
    pending["appliedReturn241"] = False
    pending["preparedNextGroup"] = {"group": "rank9-knowledge-revelation5",
        "pendingIds": ["faction-omniscience-supreme"], "pendingCount": 1,
        "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN241", "freshPacketRequiredForCurrentAuthority": True}
    pending["acceptedIds"] = []
    pending["appliedIds"] = []
    pending["heldIds"] = audit["heldIds"]
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_241.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": binding(pending_path), "currentSubmission": binding(submission_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": return_zip_info, "currentReturnDelivery": return_delivery_info,
        "nextGroup": "rank9-knowledge-revelation5", "nextPendingIds": ["faction-omniscience-supreme"],
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [],
        "currentReturnHeldIds": audit["heldIds"], "currentReturnBlockers": audit["blockers"],
        "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-memory-denial6":
            row.update({"status": status, "heldIds": audit["heldIds"], "blockers": audit["blockers"]})
        if row.get("group") == "rank9-knowledge-revelation5":
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN241",
                        "freshPacketRequiredForCurrentAuthority": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_241.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": binding(pending_path), "queue": binding(queue_path),
        "currentQueueBinding": binding(queue_path), "currentSubmission": binding(submission_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": return_zip_info, "currentReturnDelivery": return_delivery_info,
        "latestBatch": {"return": 241, "group": "rank9-memory-denial6", "ids": audit["targetIds"],
            "acceptedIds": [], "appliedIds": [], "heldIds": audit["heldIds"],
            "blockers": audit["blockers"], "conditionalQualifications": audit["conditionalQualifications"],
            "independentAudit": audit_info, "receipt": receipt_info},
        "nextGroup": "rank9-knowledge-revelation5", "nextPendingIds": ["faction-omniscience-supreme"],
        "nextPendingCount": 1,
        "nextStep": "Prepare a fresh exact-source packet for faction-omniscience-supreme at the unchanged 811/37/0 authority; retain Return241 held rulings and the earlier named holds, then send to GPT for static review only.",
        "resumePriority": "Return241 passed independent archive, source-binding and replay checks. Both Memory/Denial6 identities remain held with MD196-B01/B02; proceed to the director-selected Knowledge/Revelation5 identity and do not reopen completed reviews."})
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_241.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    snapshot += ("\n\nReturn241 has now been independently audited: 13/13 checks passed, both Memory/Denial6 identities remain held and unapplied, and the authority is still 811/37/0. "
                 "GPT selected faction-omniscience-supreme (Knowledge/Revelation5) next. The fresh packet must include Return241 and preserve the earlier sealed holds.\n")
    snapshot_path.write_text(snapshot, encoding="utf-8", newline="\n")

    print(json.dumps({"status": status, "submission": binding(submission_path),
        "pendingAudit": binding(pending_path), "queue": binding(queue_path),
        "handoff": binding(handoff_path), "audit": audit_info}, indent=2))


if __name__ == "__main__":
    main()
