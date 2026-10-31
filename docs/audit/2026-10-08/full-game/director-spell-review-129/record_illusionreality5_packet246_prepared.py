from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_illusionreality5_current_source_246_prepared"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    prep_path = BASE / "RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_246.json"
    audit_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246_RECEIPT.json"
    prep, audit, receipt = map(read, (prep_path, audit_path, receipt_path))
    assert prep["status"] == audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 16 and audit["failedChecks"] == 0
    archive = OUT / "DD_Rank9_IllusionReality5_CurrentSource_246.zip"
    delivery = OUT / "DD_Rank9_IllusionReality5_CurrentSource_246_DELIVERY.json"
    archive_info, delivery_info = info(archive), info(delivery)
    assert archive_info["sha256"] == prep["packet"]["sha256"] == audit["archive"]["sha256"]
    assert delivery_info["sha256"] == prep["deliveryManifest"]["sha256"] == audit["delivery"]["sha256"]
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    now = datetime.now(timezone.utc).isoformat()
    status = "PACKET246_PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT_811_37_0"
    submission_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246_SUBMISSION.json"
    submission = {
        "id": "RANK9ILLUSIONREALITY5-PACKET246-SUBMISSION",
        "recordedAtUtc": now,
        "status": status,
        "group": "rank9-illusion-reality5",
        "targetIds": ["soul-reflection"],
        "authority": prep["sourceAuthority"],
        "archive": archive_info,
        "deliveryManifest": delivery_info,
        "independentAudit": audit_info,
        "auditReceipt": receipt_info,
        "auditStatus": "PASS",
        "auditChecks": 16,
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

    packet_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246.json"
    packet = read(packet_path)
    packet.update({"status": status, "submission": info(submission_path),
                   "independentAudit": audit_info, "auditReceipt": receipt_info})
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_246.json"
    pending = read(pending_path)
    pending.update({"recordedAtUtc": now, "status": status})
    pending["preparedNextGroup"].update({"status": status, "packet": archive_info,
        "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "auditReceipt": receipt_info, "submittedAtUtc": None})
    pending["lastSubmittedPacket"] = {"group": "rank9-illusion-reality5", "targetIds": ["soul-reflection"],
        "archive": archive_info, "deliveryManifest": delivery_info, "independentAudit": audit_info,
        "receipt": receipt_info, "acceptedIds": [], "appliedIds": [], "submittedAtUtc": None}
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_246.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
                  "pendingIdentityAudit": pending_info, "currentSubmission": info(submission_path),
                  "submittedAtUtc": None, "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-illusion-reality5":
            row.update({"status": status, "freshPacketRequiredForCurrentAuthority": False,
                        "packet": archive_info, "deliveryManifest": delivery_info})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_246.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": pending_info, "queue": info(queue_path),
        "currentQueueBinding": info(queue_path), "currentSubmission": info(submission_path),
        "submittedAtUtc": None,
        "nextStep": "Packet246 is prepared and independently audited for exactly soul-reflection. Submit it to the GPT director, monitor the browser, independently audit the sealed return, and apply only an exact acceptance.",
        "resumePriority": "Packet246 passed 16 independent checks over 157 refreshed source bindings, the historical case/questions set, and Return207/245 context. Submit to GPT; preserve the four Return207 acceptances and Return245's reverse-gravity-field hold."})
    write(handoff_path, handoff)

    print(json.dumps({"status": status, "archive": archive_info, "deliveryManifest": delivery_info,
        "submission": info(submission_path), "pendingAudit": info(pending_path),
        "queue": info(queue_path), "handoff": info(handoff_path), "audit": audit_info}, indent=2))


if __name__ == "__main__":
    main()
