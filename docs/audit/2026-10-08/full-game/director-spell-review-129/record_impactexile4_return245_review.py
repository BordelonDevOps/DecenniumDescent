from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_impactexile4_return245_received"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}",
    }


def main() -> None:
    audit_path = BASE / "RANK9IMPACTEXILE4_RETURN245_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9IMPACTEXILE4_RETURN245_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 15 and audit["failedChecks"] == 0

    target_ids = ["reverse-gravity-field"]
    blockers = {"reverse-gravity-field": ["IE204-B02"]}
    qualifications = [
        "IE204-H-SOURCE", "IE204-H-ACCESS", "IE204-H-PHYSICAL", "IE204-H-CONTENT",
        "IE204-H-OBJECT-DURABILITY", "IE204-H-RUNTIME", "IE204-H-IMPLEMENTATION",
        "IE204-H-PLAY", "IE204-H-BALANCE", "IE204-H-COSMOLOGY", "IE204-H-DOMAIN",
        "IE204-H-COMPLETION", "IE204-H-RELEASE",
    ]
    next_group = {"group": "rank9-illusion-reality5", "pendingIds": ["soul-reflection"]}
    now = datetime.now(timezone.utc).isoformat()
    archive = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return245_HELD.zip"
    delivery = RECEIVED / "DD_Rank9_ImpactExile1_Director_Return245_DELIVERY.json"
    archive_info, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "RETURN245_AUDITED_HELD_NEXT_ILLUSION5_811_37_0"

    submission_path = BASE / "RANK9IMPACTEXILE4_PACKET_245_SUBMISSION.json"
    submission = read(submission_path)
    assert submission["browserVerified"] is True
    submission.update({
        "status": status,
        "return": 245,
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
        "artifactLabelAnomaly": "Return filename and internal decision ID say ImpactExile1 although the exact target and bound current source are ImpactExile4; content, member hashes, source binding and status independently pass.",
    })
    write(submission_path, submission)

    packet_path = BASE / "RANK9IMPACTEXILE4_PACKET_245.json"
    packet = read(packet_path)
    packet.update({
        "status": status,
        "return": 245,
        "returnArchive": archive_info,
        "returnDeliveryManifest": delivery_info,
        "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": target_ids,
        "blockers": blockers,
        "nextGroup": next_group,
    })
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_245.json"
    pending = read(pending_path)
    pending.update({
        "recordedAtUtc": now,
        "status": status,
        "lastDirectorReturn": {
            "return": 245,
            "group": "rank9-impact-exile4",
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
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": target_ids,
        "preparedNextGroup": {
            "group": next_group["group"],
            "pendingIds": next_group["pendingIds"],
            "pendingCount": len(next_group["pendingIds"]),
            "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN245",
            "freshPacketRequiredForCurrentAuthority": True,
        },
    })
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_245.json"
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
        if row.get("group") == "rank9-impact-exile4":
            row.update({"status": status, "heldIds": target_ids, "blockers": blockers})
        if row.get("group") == next_group["group"]:
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN245",
                        "freshPacketRequiredForCurrentAuthority": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_245.json"
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
            "return": 245,
            "group": "rank9-impact-exile4",
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
        "nextStep": "Prepare a fresh current-source packet for director-selected rank9-illusion-reality5, soul-reflection; preserve the Return245 hold and independently audit the next sealed return.",
        "resumePriority": "Return245 passed 15 independent checks with the exact Packet245 source archive binding. reverse-gravity-field remains held under IE204-B02; its six cases replay, but the crate durability/impact and tether/anchor strength witnesses remain missing. Authority remains 811/37/0. Continue with soul-reflection.",
    })
    write(handoff_path, handoff)

    print(json.dumps({
        "status": status,
        "submission": info(submission_path),
        "packet": info(packet_path),
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
