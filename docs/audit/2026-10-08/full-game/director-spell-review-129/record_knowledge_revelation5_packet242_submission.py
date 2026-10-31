from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_knowledgerevelation5_current_source_242_prepared"


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
    prep = read(BASE / "RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_242.json")
    audit = read(BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_INDEPENDENT_AUDIT.json")
    receipt = read(BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_RECEIPT.json")
    assert prep["status"] == "PASS" and audit["status"] == receipt["status"] == "PASS"
    assert audit["checksFailed"] == 0 and audit["checksPassed"] == 9
    archive = OUT / "DD_Rank9_KnowledgeRevelation5_CurrentSource_242.zip"
    delivery = OUT / "DD_Rank9_KnowledgeRevelation5_CurrentSource_242_DELIVERY.json"
    packet_info, delivery_info = info(archive), info(delivery)
    assert packet_info["sha256"] == prep["packet"]["sha256"] == audit["packet"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"]
    audit_info = info(BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_INDEPENDENT_AUDIT.json")
    receipt_info = info(BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_RECEIPT.json")
    status = "PACKET242_SUBMITTED_GPT_PENDING_811_37_0"
    submission_path = BASE / "RANK9KNOWLEDGEREVELATION5_PACKET_242_SUBMISSION.json"
    submission = {"id": "RANK9KNOWLEDGEREVELATION5-PACKET242-SUBMISSION", "recordedAtUtc": now,
        "status": status, "group": "rank9-knowledge-revelation5", "targetIds": ["faction-omniscience-supreme"],
        "authority": prep["sourceAuthority"], "archive": packet_info, "deliveryManifest": delivery_info,
        "independentAudit": audit_info, "auditReceipt": receipt_info, "auditStatus": "PASS",
        "auditChecks": 9, "auditFailures": 0, "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "destination": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": True, "attachedFiles": [archive.name, delivery.name,
            "RANK9_KNOWLEDGEREVELATION5_PACKET_242_INDEPENDENT_AUDIT.json",
            "RANK9_KNOWLEDGEREVELATION5_PACKET_242_RECEIPT.json"],
        "submittedAtUtc": now, "followUpPingsSent": 0, "githubChanges": False}
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
    pending = read(pending_path)
    pending["status"] = status
    pending["preparedNextGroup"].update({"status": status, "packet": packet_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "submittedAtUtc": now})
    pending["lastSubmittedPacket"] = {"group": submission["group"], "targetIds": submission["targetIds"],
        "archive": packet_info, "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "receipt": receipt_info, "acceptedIds": [], "appliedIds": [], "submittedAtUtc": now}
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_242.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": info(pending_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "currentPacketAuditStatus": "PASS",
        "currentPacketAuditChecks": 9, "currentPacketAuditFailures": 0,
        "sourcePreparation": info(BASE / "RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_242.json"),
        "currentSubmission": info(submission_path), "submittedAtUtc": now, "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == submission["group"]:
            row.update({"status": status, "freshPacketRequiredForCurrentAuthority": True,
                        "packet": packet_info, "deliveryManifest": delivery_info})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_242.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": info(pending_path), "queue": info(queue_path),
        "currentQueueBinding": info(queue_path), "currentPacket": packet_info,
        "currentPacketDelivery": delivery_info, "currentPacketAudit": audit_info,
        "currentPacketAuditReceipt": receipt_info, "packetAuditStatus": "PASS",
        "packetAuditChecks": 9, "packetAuditFailures": 0,
        "sourcePreparation": info(BASE / "RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_242.json"),
        "currentSubmission": info(submission_path), "submittedAtUtc": now,
        "nextStep": "GPT director is reviewing Packet242 for faction-omniscience-supreme. Monitor Calibration review part 6; independently audit the sealed return and apply only an exact acceptance.",
        "resumePriority": "Packet242 and its independent audit were sent to the GPT director after 9/9 checks. Preserve Return241 and earlier held reviews; capture the sealed decision and next group before applying any exact acceptance."})
    write(handoff_path, handoff)

    print(json.dumps({"status": status, "submission": info(submission_path),
        "queue": info(queue_path), "handoff": info(handoff_path), "pendingAudit": info(pending_path)}, indent=2))


if __name__ == "__main__":
    main()
