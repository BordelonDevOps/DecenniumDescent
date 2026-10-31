from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_summonhosts5_current_source_244_prepared"


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
    prep_path = BASE / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_244.json"
    audit_path = BASE / "RANK9SUMMONHOSTS5_PACKET_244_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9SUMMONHOSTS5_PACKET_244_RECEIPT.json"
    prep, audit, receipt = read(prep_path), read(audit_path), read(receipt_path)
    assert prep["status"] == "PASS" and audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 13 and audit["failedChecks"] == []
    archive = OUT / "DD_Rank9_SummonHosts5_CurrentSource_244.zip"
    delivery = OUT / "DD_Rank9_SummonHosts5_CurrentSource_244_DELIVERY.json"
    packet_info, delivery_info = info(archive), info(delivery)
    assert packet_info["sha256"] == prep["packet"]["sha256"] == audit["archive"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"] == audit["delivery"]["sha256"]
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "PACKET244_SUBMITTED_GPT_PENDING_811_37_0"
    submission_path = BASE / "RANK9SUMMONHOSTS5_PACKET_244_SUBMISSION.json"
    target_ids = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
    submission = {"id": "RANK9-SUMMONHOSTS5-PACKET244-SUBMISSION", "recordedAtUtc": now,
        "status": status, "group": "rank9-summon-hosts5", "targetIds": target_ids,
        "authority": prep["sourceAuthority"], "archive": packet_info, "deliveryManifest": delivery_info,
        "independentAudit": audit_info, "auditReceipt": receipt_info, "auditStatus": "PASS",
        "auditChecks": 13, "auditFailures": 0, "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "destination": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": True, "attachedFiles": [archive.name, delivery.name, audit_path.name, receipt_path.name],
        "submittedAtUtc": now, "followUpPingsSent": 0, "githubChanges": False}
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_244.json"
    pending = read(pending_path)
    pending["status"] = status
    pending["preparedNextGroup"].update({"status": status, "packet": packet_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "submittedAtUtc": now})
    pending["lastSubmittedPacket"] = {"group": submission["group"], "targetIds": target_ids,
        "archive": packet_info, "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "receipt": receipt_info, "acceptedIds": [], "appliedIds": [], "submittedAtUtc": now}
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_244.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": info(pending_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "currentPacketAuditStatus": "PASS",
        "currentPacketAuditChecks": 13, "currentPacketAuditFailures": 0,
        "sourcePreparation": info(prep_path), "currentSubmission": info(submission_path),
        "submittedAtUtc": now, "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == submission["group"]:
            row.update({"status": status, "freshPacketRequiredForCurrentAuthority": True,
                "packet": packet_info, "deliveryManifest": delivery_info})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_244.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": info(pending_path), "queue": info(queue_path),
        "currentQueueBinding": info(queue_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "packetAuditStatus": "PASS",
        "packetAuditChecks": 13, "packetAuditFailures": 0, "sourcePreparation": info(prep_path),
        "currentSubmission": info(submission_path), "submittedAtUtc": now,
        "nextStep": "GPT director is reviewing Packet244 for summon-elemental-avatar, summon-herald-of-the-planes, and summon-avatar-of-decay. Monitor Calibration review part 6; independently audit the sealed return and apply only an exact acceptance.",
        "resumePriority": "Packet244 and its 13/13 independent audit were sent to GPT. Preserve Return243 and Returns238–242, audit the sealed response, and apply only exact accepted identities."})
    write(handoff_path, handoff)
    print(json.dumps({"status": status, "submission": info(submission_path),
        "queue": info(queue_path), "handoff": info(handoff_path), "pendingAudit": info(pending_path)}, indent=2))


if __name__ == "__main__":
    main()
