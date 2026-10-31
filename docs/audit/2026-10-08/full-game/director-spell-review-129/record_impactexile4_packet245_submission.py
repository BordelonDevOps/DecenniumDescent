from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_impactexile4_current_source_245_prepared"

def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    prep_path = BASE / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_245.json"
    audit_path = BASE / "RANK9IMPACTEXILE4_PACKET_245_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9IMPACTEXILE4_PACKET_245_RECEIPT.json"
    prep, audit, receipt = map(read, (prep_path, audit_path, receipt_path))
    assert prep["status"] == audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 14 and audit["failedChecks"] == []
    archive = OUT / "DD_Rank9_ImpactExile4_CurrentSource_245.zip"
    delivery = OUT / "DD_Rank9_ImpactExile4_CurrentSource_245_DELIVERY.json"
    packet_info, delivery_info = info(archive), info(delivery)
    assert packet_info["sha256"] == prep["packet"]["sha256"] == audit["archive"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"] == audit["delivery"]["sha256"]
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "PACKET245_SUBMITTED_GPT_PENDING_811_37_0"
    target_ids = ["reverse-gravity-field"]
    submission_path = BASE / "RANK9IMPACTEXILE4_PACKET_245_SUBMISSION.json"
    submission = {
        "id": "RANK9-IMPACTEXILE4-PACKET245-SUBMISSION",
        "recordedAtUtc": now,
        "status": status,
        "group": "rank9-impact-exile4",
        "targetIds": target_ids,
        "authority": prep["sourceAuthority"],
        "archive": packet_info,
        "deliveryManifest": delivery_info,
        "independentAudit": audit_info,
        "auditReceipt": receipt_info,
        "auditStatus": "PASS",
        "auditChecks": 14,
        "auditFailures": 0,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [],
        "destination": "Calibration review part 6",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": False,
        "attachedFiles": [archive.name, delivery.name, audit_path.name, receipt_path.name],
        "submittedAtUtc": None,
        "followUpPingsSent": 0,
        "githubChanges": False,
    }
    write(submission_path, submission)

    packet_path = BASE / "RANK9IMPACTEXILE4_PACKET_245.json"
    packet = read(packet_path)
    packet.update({"status": status, "submission": info(submission_path),
        "independentAudit": audit_info, "auditReceipt": receipt_info})
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_245.json"
    pending = read(pending_path)
    pending.update({"status": status, "recordedAtUtc": now})
    pending["preparedNextGroup"].update({"status": status, "packet": packet_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "submittedAtUtc": None})
    pending["lastSubmittedPacket"] = {"group": "rank9-impact-exile4", "targetIds": target_ids,
        "archive": packet_info, "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "receipt": receipt_info, "acceptedIds": [], "appliedIds": [], "submittedAtUtc": None}
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_245.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": info(pending_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "currentPacketAuditStatus": "PASS",
        "currentPacketAuditChecks": 14, "currentPacketAuditFailures": 0,
        "sourcePreparation": info(prep_path), "currentSubmission": info(submission_path),
        "submittedAtUtc": None, "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-impact-exile4":
            row.update({"status": status, "freshPacketRequiredForCurrentAuthority": True,
                "packet": packet_info, "deliveryManifest": delivery_info})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_245.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": info(pending_path), "queue": info(queue_path),
        "currentQueueBinding": info(queue_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "packetAuditStatus": "PASS",
        "packetAuditChecks": 14, "packetAuditFailures": 0,
        "sourcePreparation": info(prep_path), "currentSubmission": info(submission_path),
        "submittedAtUtc": None,
        "nextStep": "Packet245 is ready to send to the GPT director for exactly reverse-gravity-field. Monitor the browser, independently audit its sealed return, and apply only any exact acceptance.",
        "resumePriority": "Packet245 and its 14/14 independent audit are prepared. Preserve the Return228 same-identity hold, Return244 Summon Hosts holds, and the active Returns238–243 holds. Keep authority at 811/37/0 and do not apply without an independently passing exact acceptance."})
    write(handoff_path, handoff)
    print(json.dumps({"status": status, "submission": info(submission_path),
        "packet": packet_info, "deliveryManifest": delivery_info,
        "pendingAudit": info(pending_path), "queue": info(queue_path),
        "handoff": info(handoff_path), "audit": audit_info}, indent=2))

if __name__ == "__main__":
    main()
