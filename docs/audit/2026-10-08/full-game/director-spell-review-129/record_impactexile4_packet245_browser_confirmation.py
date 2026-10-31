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
    submission_path = BASE / "RANK9IMPACTEXILE4_PACKET_245_SUBMISSION.json"
    submission = read(submission_path)
    assert submission["status"] == "PACKET245_SUBMITTED_GPT_PENDING_811_37_0"
    assert submission["conversationId"] == "6adc506d-8770-83ea-b64c-0345d9b9b682"
    assert submission["targetIds"] == ["reverse-gravity-field"]
    assert submission["auditStatus"] == "PASS" and submission["auditChecks"] == 14
    assert submission["browserVerified"] is False and submission["submittedAtUtc"] is None
    submission["browserVerified"] = True
    submission["submittedAtUtc"] = now
    submission["browserEvidence"] = {
        "conversationTitle": "Calibration review part 6",
        "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
        "attachedFilesVisible": submission["attachedFiles"],
        "submittedMessageVisible": True,
        "directorStatusVisible": "Working",
    }
    write(submission_path, submission)
    submission_info = info(submission_path)

    packet_path = BASE / "RANK9IMPACTEXILE4_PACKET_245.json"
    packet = read(packet_path)
    packet["submission"] = submission_info
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_245.json"
    pending = read(pending_path)
    pending["submittedAtUtc"] = now
    pending["preparedNextGroup"]["submittedAtUtc"] = now
    pending["preparedNextGroup"]["submission"] = submission_info
    pending["lastSubmittedPacket"]["submittedAtUtc"] = now
    pending["lastSubmittedPacket"]["submission"] = submission_info
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_245.json"
    queue = read(queue_path)
    queue["pendingIdentityAudit"] = pending_info
    queue["currentSubmission"] = submission_info
    queue["submittedAtUtc"] = now
    write(queue_path, queue)
    queue_info = info(queue_path)

    handoff_path = BASE / "CURRENT_HANDOFF_245.json"
    handoff = read(handoff_path)
    handoff["pendingIdentityAudit"] = pending_info
    handoff["queue"] = queue_info
    handoff["currentQueueBinding"] = queue_info
    handoff["currentSubmission"] = submission_info
    handoff["submittedAtUtc"] = now
    handoff["nextStep"] = "Packet245 is submitted and GPT is reviewing exactly reverse-gravity-field. Monitor the browser, independently audit its sealed return, and apply only any exact acceptance."
    write(handoff_path, handoff)

    print(json.dumps({
        "status": submission["status"],
        "browserVerified": submission["browserVerified"],
        "submittedAtUtc": now,
        "submission": submission_info,
        "pendingIdentityAudit": pending_info,
        "queue": queue_info,
        "handoff": info(handoff_path),
    }, indent=2))


if __name__ == "__main__":
    main()
