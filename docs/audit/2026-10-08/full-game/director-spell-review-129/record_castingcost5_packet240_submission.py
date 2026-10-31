from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_castingcost5_current_source_240_prepared"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    prep = read(BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_240.json")
    audit = read(BASE / "RANK9_CASTINGCOST5_PACKET240_INDEPENDENT_AUDIT.json")
    receipt = read(BASE / "RANK9_CASTINGCOST5_PACKET240_RECEIPT.json")
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checksFailed"] == 0 and audit["checksPassed"] == 17

    archive = OUT / "DD_Rank9_CastingCost5_CurrentSource_240.zip"
    delivery = OUT / "DD_Rank9_CastingCost5_CurrentSource_240_DELIVERY.json"
    packet_info, delivery_info = info(archive), info(delivery)
    assert packet_info["sha256"] == prep["packet"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"]
    audit_info = info(BASE / "RANK9_CASTINGCOST5_PACKET240_INDEPENDENT_AUDIT.json")
    receipt_info = info(BASE / "RANK9_CASTINGCOST5_PACKET240_RECEIPT.json")

    status = "PACKET240_SUBMITTED_GPT_PENDING_811_37_0"
    submission = {
        "id": "RANK9CASTINGCOST5-PACKET240-SUBMISSION", "recordedAtUtc": now,
        "status": status, "group": "rank9-casting-cost5", "targetIds": ["unholy-ascendance"],
        "authority": prep["sourceAuthority"], "archive": packet_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "auditStatus": "PASS", "auditChecks": 17,
        "auditFailures": 0, "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "destination": "Calibration review part 6",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": True, "submittedAtUtc": now, "followUpPingsSent": 0,
        "githubChanges": False,
    }
    submission_path = BASE / "RANK9_CASTINGCOST5_PACKET_240_SUBMISSION.json"
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_240.json"
    pending = read(pending_path)
    pending["status"] = status
    pending["preparedNextGroup"].update({"status": status, "packet": packet_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "submittedAtUtc": now})
    pending["lastSubmittedPacket"] = {"group": submission["group"], "targetIds": submission["targetIds"],
        "archive": packet_info, "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "receipt": receipt_info, "acceptedIds": [], "appliedIds": [], "submittedAtUtc": now}
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_240.json"
    queue = read(queue_path)
    queue["recordedAtUtc"] = now
    queue["status"] = queue["packetStatus"] = status
    queue["pendingIdentityAudit"] = info(pending_path)
    queue["currentPacket"] = packet_info
    queue["currentDeliveryManifest"] = queue["currentPacketDelivery"] = delivery_info
    queue["currentPacketAudit"] = audit_info
    queue["currentPacketAuditReceipt"] = receipt_info
    queue["currentPacketAuditStatus"] = "PASS"
    queue["currentPacketAuditChecks"] = 17
    queue["currentPacketAuditFailures"] = 0
    queue["sourcePreparation"] = info(BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_240.json")
    queue["currentSubmission"] = info(submission_path)
    queue["submittedAtUtc"] = now
    queue["githubChanges"] = False
    row = next(group for group in queue["currentPendingGroups"] if group["group"] == submission["group"])
    row["status"] = status
    row["freshPacketRequiredForCurrentAuthority"] = True
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_240.json"
    handoff = read(handoff_path)
    handoff["recordedAtUtc"] = now
    handoff["status"] = status
    handoff["pendingIdentityAudit"] = info(pending_path)
    handoff["queue"] = handoff["currentQueueBinding"] = info(queue_path)
    handoff["currentPacket"] = packet_info
    handoff["currentPacketDelivery"] = delivery_info
    handoff["currentPacketAudit"] = audit_info
    handoff["currentPacketAuditReceipt"] = receipt_info
    handoff["packetAuditStatus"] = "PASS"
    handoff["packetAuditChecks"] = 17
    handoff["packetAuditFailures"] = 0
    handoff["sourcePreparation"] = info(BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_240.json")
    handoff["currentSubmission"] = info(submission_path)
    handoff["submittedAtUtc"] = now
    handoff["nextStep"] = "GPT director is reviewing Packet240 for unholy-ascendance. Monitor Calibration review part 6; independently audit the sealed return before applying any exact acceptance."
    handoff["resumePriority"] = "Packet240 for unholy-ascendance was sent with its independently passing packet audit. Capture and audit the sealed decision and next group before making any application."
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_240.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    snapshot = snapshot.replace("Packet240 is prepared and not yet sent.",
                                "Packet240 is submitted to GPT and awaiting its director decision.")
    snapshot_path.write_text(snapshot, encoding="utf-8")
    print(json.dumps({"status": status, "submission": info(submission_path),
                      "queue": info(queue_path), "handoff": info(handoff_path),
                      "pendingAudit": info(pending_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
