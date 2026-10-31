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
    submission_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246_SUBMISSION.json"
    submission = read(submission_path)
    assert submission["status"] == "PACKET246_PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT_811_37_0"
    assert submission["targetIds"] == ["soul-reflection"]
    assert submission["auditStatus"] == "PASS" and submission["auditChecks"] == 16
    assert submission["browserVerified"] is False and submission["submittedAtUtc"] is None
    now = datetime.now(timezone.utc).isoformat()
    status = "PACKET246_SUBMITTED_GPT_PENDING_811_37_0"
    submission.update({
        "status": status,
        "browserVerified": True,
        "submittedAtUtc": now,
        "browserEvidence": {
            "conversationTitle": "Calibration review part 6",
            "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
            "attachedFilesVisible": submission["attachedFiles"],
            "submittedMessageVisible": True,
            "directorStatusVisible": "Working",
        },
    })
    write(submission_path, submission)
    submission_info = info(submission_path)

    packet_path = BASE / "RANK9ILLUSIONREALITY5_PACKET_246.json"
    packet = read(packet_path)
    packet.update({"status": status, "submission": submission_info})
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_246.json"
    pending = read(pending_path)
    pending.update({"recordedAtUtc": now, "status": status})
    pending["preparedNextGroup"].update({"status": status, "submittedAtUtc": now,
        "submission": submission_info})
    pending["lastSubmittedPacket"].update({"status": status, "submittedAtUtc": now,
        "submission": submission_info})
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_246.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": pending_info, "currentSubmission": submission_info,
        "submittedAtUtc": now, "githubChanges": False})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_246.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status,
        "pendingIdentityAudit": pending_info, "queue": info(queue_path),
        "currentQueueBinding": info(queue_path), "currentSubmission": submission_info,
        "submittedAtUtc": now,
        "nextStep": "Packet246 is submitted to GPT for exactly soul-reflection. Monitor the browser, independently audit its sealed return, and apply only an exact acceptance."})
    write(handoff_path, handoff)

    print(json.dumps({"status": status, "browserVerified": True, "submittedAtUtc": now,
        "submission": submission_info, "pendingAudit": pending_info,
        "queue": info(queue_path), "handoff": info(handoff_path)}, indent=2))


if __name__ == "__main__":
    main()
