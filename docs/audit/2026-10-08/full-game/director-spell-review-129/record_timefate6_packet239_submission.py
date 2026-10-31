from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


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
    now = datetime.now(timezone.utc).isoformat()
    prep = read(BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json")
    audit = read(BASE / "RANK9_TIMEFATE6_PACKET239_INDEPENDENT_AUDIT.json")
    receipt = read(BASE / "RANK9_TIMEFATE6_PACKET239_RECEIPT.json")
    assert prep["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT"
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["failedChecks"] == receipt["failedChecks"] == 0

    archive = BASE / "rank9_timefate6_current_source_239_prepared/DD_Rank9_TimeFate6_CurrentSource_239.zip"
    delivery = BASE / "rank9_timefate6_current_source_239_prepared/DD_Rank9_TimeFate6_CurrentSource_239_DELIVERY.json"
    packet_info, delivery_info = info(archive), info(delivery)
    assert packet_info["sha256"] == prep["packet"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"]

    audit_info = info(BASE / "RANK9_TIMEFATE6_PACKET239_INDEPENDENT_AUDIT.json")
    receipt_info = info(BASE / "RANK9_TIMEFATE6_PACKET239_RECEIPT.json")
    status = "PACKET239_SUBMITTED_GPT_PENDING_811_37_0"
    submission = {
        "id": "RANK9TIMEFATE6-PACKET239-SUBMISSION",
        "recordedAtUtc": now,
        "status": status,
        "group": "rank9-time-fate6",
        "targetIds": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"],
        "authority": prep["sourceAuthority"],
        "archive": packet_info,
        "deliveryManifest": delivery_info,
        "independentAudit": audit_info,
        "auditReceipt": receipt_info,
        "auditStatus": "PASS",
        "auditChecks": audit["checkCount"],
        "auditFailures": 0,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [],
        "destination": "Calibration review part 6",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": True,
        "submittedAtUtc": now,
        "followUpPingsSent": 2,
        "githubChanges": False,
    }
    submission_path = BASE / "RANK9_TIMEFATE6_PACKET_239_SUBMISSION.json"
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_239.json"
    pending = read(pending_path)
    pending["status"] = status
    pending["preparedNextGroup"].update(
        {
            "status": status,
            "packet": packet_info,
            "deliveryManifest": delivery_info,
            "independentAudit": audit_info,
            "auditReceipt": receipt_info,
            "submittedAtUtc": now,
        }
    )
    pending["lastSubmittedPacket"] = {
        "group": submission["group"],
        "targetIds": submission["targetIds"],
        "archive": packet_info,
        "deliveryManifest": delivery_info,
        "independentAudit": audit_info,
        "receipt": receipt_info,
        "acceptedIds": [],
        "appliedIds": [],
        "submittedAtUtc": now,
    }
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_239.json"
    queue = read(queue_path)
    queue["recordedAtUtc"] = now
    queue["status"] = queue["packetStatus"] = status
    queue["pendingIdentityAudit"] = info(pending_path)
    queue["currentPacket"] = packet_info
    queue["currentDeliveryManifest"] = delivery_info
    queue["currentPacketDelivery"] = delivery_info
    queue["currentPacketAudit"] = audit_info
    queue["currentPacketAuditReceipt"] = receipt_info
    queue["currentPacketAuditStatus"] = "PASS"
    queue["currentPacketAuditChecks"] = audit["checkCount"]
    queue["currentPacketAuditFailures"] = 0
    queue["sourcePreparation"] = info(BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json")
    queue["currentSubmission"] = info(submission_path)
    queue["submittedAtUtc"] = now
    queue["githubChanges"] = False
    row = next(group for group in queue["currentPendingGroups"] if group["group"] == submission["group"])
    row["status"] = status
    row["freshPacketRequiredForCurrentAuthority"] = True
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_239.json"
    handoff = read(handoff_path)
    handoff["recordedAtUtc"] = now
    handoff["status"] = status
    handoff["pendingIdentityAudit"] = info(pending_path)
    handoff["queue"] = info(queue_path)
    handoff["currentQueueBinding"] = info(queue_path)
    handoff["currentPacket"] = packet_info
    handoff["currentPacketDelivery"] = delivery_info
    handoff["currentPacketAudit"] = audit_info
    handoff["currentPacketAuditReceipt"] = receipt_info
    handoff["packetAuditStatus"] = "PASS"
    handoff["packetAuditChecks"] = audit["checkCount"]
    handoff["packetAuditFailures"] = 0
    handoff["sourcePreparation"] = info(BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json")
    handoff["currentSubmission"] = info(submission_path)
    handoff["submittedAtUtc"] = now
    handoff["nextStep"] = "GPT director is reviewing Packet239. Continue monitoring Calibration review part 6; independently audit the sealed return before applying exact accepted identities."
    handoff["resumePriority"] = "Packet239 for time-stop, fate-rewrite, collapse-timeline and eternal-prophecy was submitted with its independently passing packet audit. GPT has been pinged twice; capture and audit the sealed decision before applying exact acceptances."
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_239.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    snapshot = snapshot.replace("Packet239 is prepared and not yet sent.", "Packet239 is submitted to GPT and awaiting its director decision.")
    snapshot_path.write_text(snapshot, encoding="utf-8")

    print(json.dumps({"status": status, "submission": info(submission_path), "queue": info(queue_path), "handoff": info(handoff_path), "pendingAudit": info(pending_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
