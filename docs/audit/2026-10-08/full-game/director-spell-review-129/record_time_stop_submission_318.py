from __future__ import annotations

import hashlib
import json
import pathlib
import zlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
PACKET_DIR = AUDIT / "rank9_time_stop_current_source_318_prepared"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def bind(p: pathlib.Path) -> dict:
    raw = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(name: str) -> dict:
    return json.loads((AUDIT / name).read_text(encoding="utf-8"))


def write(name: str, obj: dict) -> None:
    (AUDIT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    queue317 = read("CURRENT_SPELL_QUEUE_317.json")
    handoff317 = read("CURRENT_HANDOFF_317.json")
    audit317 = read("CURRENT25_PENDING_IDENTITY_AUDIT_317.json")
    base_dir = AUDIT / "rank9_time_stop_current_source_318_prepared"
    packet = base_dir / "DD_Rank9_TimeStop_CurrentSource_318.zip"
    delivery = base_dir / "DD_Rank9_TimeStop_CurrentSource_318_DELIVERY.json"
    audit1 = AUDIT / "TIME_STOP_PACKET_318_INDEPENDENT_AUDIT.json"
    audit2 = AUDIT / "TIME_STOP_PACKET_318_READBACK_AUDIT.json"
    comparison = base_dir / "PACKET282_140_SOURCE_BINDING_COMPARISON.json"
    request = base_dir / "TIME_STOP_DIRECTOR_REQUEST_318.md"
    attachments = [bind(x) for x in [packet, delivery, audit1, audit2, comparison, request]]

    submission = {
        "id": "TIME-STOP-PACKET-318-DIRECTOR-SUBMISSION",
        "recordedAtUtc": now,
        "status": "SUBMITTED_DIRECTOR_WORKING",
        "destination": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": CHAT},
        "userAuthorization": "User directed continued Director review, frequent pings, and completion before GitHub push.",
        "messageSent": True,
        "messageTextSummary": "Adjudicate only time-stop / TF192-B01 at 823/25/0; if still held, return exact witness gap and joint-interface authoring decision. Preserve queue and five separate holds; no application unless expressly accepted.",
        "attachments": attachments,
        "packet": attachments[0],
        "delivery": attachments[1],
        "independentAudit": attachments[2],
        "readbackAudit": attachments[3],
        "sourceComparison": attachments[4],
        "request": attachments[5],
        "directorLastStatus": "No change to scope or priority; Time Stop-only submission; Timeless Form cannot be treated as accepted authority; request joint-interface authoring decision if it remains the only immunity route.",
        "directorStateAtCapture": "WORKING",
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "authority": queue317["currentAuthority"],
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
    }
    submission_path = AUDIT / "TIME_STOP_PACKET_318_DIRECTOR_SUBMISSION_20261031.json"
    write(submission_path.name, submission)

    queue318 = dict(queue317)
    queue318.update({
        "id": "SPELL-REVIEW-QUEUE-318",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-317",
        "activeReview": {"spellId": "time-stop", "blockerIds": ["TF192-B01"], "packet": "TIME_STOP_PACKET_318", "status": "SUBMITTED_WAITING_DIRECTOR_DECISION"},
        "currentPacketStatus": "PACKET318_SUBMITTED_TO_DIRECTOR_WAITING_TF192_B01_DECISION",
        "currentSubmission": bind(submission_path),
        "currentPacket": {"archive": attachments[0], "delivery": attachments[1], "independentAudit": attachments[2], "readbackAudit": attachments[3], "sourceComparison": attachments[4]},
        "pendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_318.json",
        "directorConnectionStatus": "Packet318 uploaded and sent; Director response is working. Last status ping confirmed Time Stop-only scope/priority, Timeless Form is not accepted authority, and joint-interface authoring request is in the packet.",
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [],
        "githubChanges": False,
    })
    queue318_path = AUDIT / "CURRENT_SPELL_QUEUE_318.json"
    write(queue318_path.name, queue318)

    audit318 = dict(audit317)
    audit318.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-318",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_823_25_TIME_STOP_SUBMITTED_WAITING_DIRECTOR",
        "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_317.json",
        "sourceQueue": bind(queue318_path),
        "nextStep": "Receive Director decision on Time Stop / TF192-B01; apply only an exact accepted identity; refresh authority, queue and remaining tasks after adjudication.",
        "activeSubmission": bind(submission_path),
        "pendingCount": 25,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
    })
    audit318_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_318.json"
    write(audit318_path.name, audit318)

    handoff318 = dict(handoff317)
    handoff318.update({
        "id": "SPELL-REVIEW-HANDOFF-318",
        "recordedAtUtc": now,
        "supersedes": "CURRENT-HANDOFF-317",
        "status": "TIME_STOP_PACKET318_SUBMITTED_WAITING_DIRECTOR_DECISION",
        "scopeIds": ["time-stop"],
        "currentBlocker": "TF192-B01",
        "queue": queue318_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue318_path),
        "pendingIdentityAudit": audit318_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAuditBinding": bind(audit318_path),
        "appliedThisStep": [], "acceptedThisStep": [], "heldThisStep": [],
        "currentSubmission": bind(submission_path),
        "nextStep": "Wait for the Director's Time Stop-only decision. If held, track exact missing witness and any joint-interface authoring work before proceeding to Fate Rewrite.",
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
    })
    write("CURRENT_HANDOFF_318.json", handoff318)
    print(json.dumps({"status": submission["status"], "submission": bind(submission_path), "queue": bind(queue318_path), "pendingAudit": bind(audit318_path), "handoff": bind(AUDIT / "CURRENT_HANDOFF_318.json"), "authority": queue318["currentAuthority"], "remaining": 25, "attachments": len(attachments)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
