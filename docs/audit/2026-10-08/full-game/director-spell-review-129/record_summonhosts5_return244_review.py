from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_summonhosts5_return244_received"

def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    audit_path = BASE / "RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9SUMMONHOSTS5_RETURN244_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checksFailed"] == 0 and audit["checksPassed"] == 21
    target_ids = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
    blockers = {
        "summon-elemental-avatar": ["SH202-B01"],
        "summon-herald-of-the-planes": ["SH202-B02"],
        "summon-avatar-of-decay": ["SH202-B03"],
    }
    qualifications = [f"SH202-H{i:02d}" for i in range(1, 13)]
    next_group = {"group": "rank9-impact-exile4", "pendingIds": ["reverse-gravity-field"]}
    now = datetime.now(timezone.utc).isoformat()
    archive = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return244_HELD.zip"
    delivery = RECEIVED / "DD_Rank9_SummonHosts3_Director_Return244_HELD_DELIVERY.json"
    archive_info, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "RETURN244_AUDITED_HELD_NEXT_IMPACT_EXILE4_811_37_0"

    submission_path = BASE / "RANK9SUMMONHOSTS5_PACKET_244_SUBMISSION.json"
    submission = read(submission_path)
    submission.update({
        "status": status,
        "return": 244,
        "returnArchive": archive_info,
        "returnDeliveryManifest": delivery_info,
        "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": target_ids,
        "blockers": blockers,
        "conditionalQualifications": qualifications,
        "nextGroup": next_group,
        "returnedAtUtc": now,
        "canonicalChanges": False,
        "githubChanges": False,
    })
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_244.json"
    pending = read(pending_path)
    pending.update({
        "recordedAtUtc": now,
        "status": status,
        "lastDirectorReturn": {
            "return": 244,
            "group": "rank9-summon-hosts5",
            "targetIds": target_ids,
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": target_ids,
            "blockers": blockers,
            "conditionalQualifications": qualifications,
            "independentAudit": audit_info,
            "receipt": receipt_info,
            "archive": archive_info,
            "deliveryManifest": delivery_info,
            "nextGroup": next_group,
        },
        "appliedReturn244": False,
        "preparedNextGroup": {
            "group": next_group["group"],
            "pendingIds": next_group["pendingIds"],
            "pendingCount": len(next_group["pendingIds"]),
            "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN244",
            "freshPacketRequiredForCurrentAuthority": True,
        },
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": target_ids,
    })
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_244.json"
    queue = read(queue_path)
    queue.update({
        "recordedAtUtc": now,
        "status": status,
        "packetStatus": status,
        "pendingIdentityAudit": info(pending_path),
        "currentSubmission": info(submission_path),
        "currentReturnAudit": audit_info,
        "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": archive_info,
        "currentReturnDelivery": delivery_info,
        "nextGroup": next_group["group"],
        "nextPendingIds": next_group["pendingIds"],
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": target_ids,
        "currentReturnBlockers": blockers,
        "githubChanges": False,
    })
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-summon-hosts5":
            row.update({"status": status, "heldIds": target_ids, "blockers": blockers})
        if row.get("group") == next_group["group"]:
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN244",
                "freshPacketRequiredForCurrentAuthority": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_244.json"
    handoff = read(handoff_path)
    handoff.update({
        "recordedAtUtc": now,
        "status": status,
        "pendingIdentityAudit": info(pending_path),
        "queue": info(queue_path),
        "currentQueueBinding": info(queue_path),
        "currentSubmission": info(submission_path),
        "currentReturnAudit": audit_info,
        "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": archive_info,
        "currentReturnDelivery": delivery_info,
        "latestBatch": {
            "return": 244,
            "group": "rank9-summon-hosts5",
            "ids": target_ids,
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": target_ids,
            "blockers": blockers,
            "conditionalQualifications": qualifications,
            "independentAudit": audit_info,
            "receipt": receipt_info,
        },
        "nextGroup": next_group["group"],
        "nextPendingIds": next_group["pendingIds"],
        "nextPendingCount": len(next_group["pendingIds"]),
        "nextStep": "Prepare a fresh current-source packet for director-selected rank9-impact-exile4, reverse-gravity-field; retain all Return244 holds and independently audit the next sealed return.",
        "resumePriority": "Return244 passed 21 independent checks. Its three identities remain held with SH202-B01/B02/B03; all 28 case and three procedure files are byte-exact to audited Return227. Authority and canonical content remain unchanged. Continue with the director-selected reverse-gravity-field review.",
    })
    write(handoff_path, handoff)

    print(json.dumps({
        "status": status,
        "submission": info(submission_path),
        "pendingAudit": info(pending_path),
        "queue": info(queue_path),
        "handoff": info(handoff_path),
        "audit": audit_info,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": target_ids,
        "nextGroup": next_group,
    }, indent=2))

if __name__ == "__main__":
    main()
