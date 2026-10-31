from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
TARGET = "unholy-ascendance"
NEXT = {"group": "rank9-memory-denial6", "pendingIds": ["mind-collapse", "unravel-identity"]}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    submission_path = BASE / "RANK9_CASTINGCOST5_PACKET_240_SUBMISSION.json"
    submission = read(submission_path)
    audit_path = BASE / "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["checksFailed"] == 0 and audit["status"] == "PASS_PACKAGE_BINDING_AND_SCOPE; UNHOLY_ASCENDANCE_HELD_CC194_B04"
    assert receipt["heldIds"] == [TARGET] and receipt["acceptedIds"] == receipt["appliedIds"] == []

    return_archive = audit["returnArchive"]
    delivery = audit["deliveryManifest"]
    audit_info = {"path": audit_path.relative_to(ROOT).as_posix(), "bytes": audit_path.stat().st_size,
                  "sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
                  "crc32": f"{zlib.crc32(audit_path.read_bytes()) & 0xffffffff:08x}"}
    receipt_info = {"path": receipt_path.relative_to(ROOT).as_posix(), "bytes": receipt_path.stat().st_size,
                    "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
                    "crc32": f"{zlib.crc32(receipt_path.read_bytes()) & 0xffffffff:08x}"}

    status = "RETURN240_AUDIT_PASS_HELD_811_37_0"
    submission.update({"status": status, "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET],
        "directorReturn": return_archive, "directorReturnDelivery": delivery,
        "returnIndependentAudit": audit_info, "returnReceipt": receipt_info,
        "returnAuditStatus": audit["status"], "returnAuditChecks": audit["checkCount"],
        "returnAuditFailures": 0, "nextGroup": NEXT["group"], "nextPendingIds": NEXT["pendingIds"],
        "followUpPingsSent": 0})
    write(submission_path, submission)
    submission_info = {"path": submission_path.relative_to(ROOT).as_posix(), "bytes": submission_path.stat().st_size,
        "sha256": hashlib.sha256(submission_path.read_bytes()).hexdigest(),
                       "crc32": f"{zlib.crc32(submission_path.read_bytes()) & 0xffffffff:08x}"}

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_240.json"
    pending = read(pending_path)
    pending["recordedAtUtc"] = now
    pending["status"] = status
    pending["currentReturnAudit"] = audit_info
    pending["lastDirectorReturn"] = {"return": 240, "group": "rank9-casting-cost5",
        "reviewedIds": [TARGET], "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET],
        "blockers": receipt["blockers"], "independentAudit": audit_info, "receipt": receipt_info}
    pending["preparedNextGroup"] = {"group": NEXT["group"], "pendingIds": NEXT["pendingIds"],
        "status": "DIRECTOR_SELECTED_AWAITING_FRESH_CURRENT_SOURCE_PACKET",
        "selectedBy": "GPT director in Return240", "freshPacketRequired": True,
        "acceptedIds": [], "appliedIds": []}
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_240.json"
    queue = read(queue_path)
    queue["recordedAtUtc"] = now
    queue["status"] = queue["packetStatus"] = status
    queue["pendingIdentityAudit"] = {"path": pending_path.relative_to(ROOT).as_posix(),
        "bytes": pending_path.stat().st_size,
        "sha256": hashlib.sha256(pending_path.read_bytes()).hexdigest(),
        "crc32": f"{zlib.crc32(pending_path.read_bytes()) & 0xffffffff:08x}"}
    queue["currentReturn"] = return_archive
    queue["currentReturnDelivery"] = delivery
    queue["currentReturnAudit"] = audit_info
    queue["currentReturnReceipt"] = receipt_info
    queue["currentReturnAuditStatus"] = audit["status"]
    queue["currentReturnAuditChecks"] = audit["checkCount"]
    queue["currentReturnAuditFailures"] = 0
    queue["currentSubmission"] = submission_info
    queue["nextGroup"] = NEXT["group"]
    queue["next"] = {"group": NEXT["group"], "pendingIds": NEXT["pendingIds"], "pendingCount": len(NEXT["pendingIds"]),
        "status": "DIRECTOR_SELECTED_AWAITING_FRESH_CURRENT_SOURCE_PACKET"}
    queue["lastReviewedBatch"] = {"return": 240, "group": "rank9-casting-cost5",
        "reviewedIds": [TARGET], "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET],
        "blockers": {TARGET: ["CC194-B04"]}, "independentAudit": audit_info,
        "receipt": receipt_info, "ids": [TARGET], "authorityAfter": queue["currentAuthority"],
        "auditStatus": audit["status"]}
    row = next(group for group in queue["currentPendingGroups"] if group["group"] == "rank9-casting-cost5")
    row["status"] = "RETURN240_AUDIT_PASS_HELD_CC194-B04"
    row["freshPacketRequiredForCurrentAuthority"] = True
    next_row = next(group for group in queue["currentPendingGroups"] if group["group"] == NEXT["group"])
    next_row["status"] = "DIRECTOR_SELECTED_AWAITING_FRESH_CURRENT_SOURCE_PACKET"
    next_row["freshPacketRequiredForCurrentAuthority"] = True
    queue["nextPreparedRequest"] = {"group": NEXT["group"], "pendingIds": NEXT["pendingIds"],
        "status": "DIRECTOR_SELECTED_AWAITING_FRESH_CURRENT_SOURCE_PACKET"}
    write(queue_path, queue)
    queue_info = {"path": queue_path.relative_to(ROOT).as_posix(), "bytes": queue_path.stat().st_size,
                  "sha256": hashlib.sha256(queue_path.read_bytes()).hexdigest(),
                  "crc32": f"{zlib.crc32(queue_path.read_bytes()) & 0xffffffff:08x}"}

    handoff_path = BASE / "CURRENT_HANDOFF_240.json"
    handoff = read(handoff_path)
    handoff["recordedAtUtc"] = now
    handoff["status"] = status
    handoff["pendingIdentityAudit"] = queue["pendingIdentityAudit"]
    handoff["queue"] = handoff["currentQueueBinding"] = queue_info
    handoff["currentReturn"] = return_archive
    handoff["currentReturnDelivery"] = delivery
    handoff["currentReturnAudit"] = audit_info
    handoff["currentReturnReceipt"] = receipt_info
    handoff["currentReturnAuditStatus"] = audit["status"]
    handoff["currentReturnAuditChecks"] = audit["checkCount"]
    handoff["currentReturnAuditFailures"] = 0
    handoff["currentSubmission"] = submission_info
    handoff["latestBatch"] = queue["lastReviewedBatch"]
    handoff["nextGroup"] = NEXT["group"]
    handoff["nextPendingIds"] = NEXT["pendingIds"]
    handoff["nextPendingCount"] = len(NEXT["pendingIds"])
    handoff["nextStep"] = "Return240 is independently package/source-bound and unholy-ascendance remains held under CC194-B04. Prepare a fresh current-authority packet for GPT-selected rank9-memory-denial6 — mind-collapse and unravel-identity."
    handoff["resumePriority"] = "Authority remains 811 reviewed/applied, 37 pending and 0 accepted-unapplied. Casting/Cost5 unholy-ascendance remains held under CC194-B04. GPT selected Memory/Denial6 — mind-collapse and unravel-identity — next; create a fresh source packet and await the director decision."
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_240.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    snapshot = snapshot.replace("Packet240 is submitted to GPT and awaiting its director decision.",
        "Return240 independently passed package/source-binding verification; unholy-ascendance remains held under CC194-B04.")
    snapshot += "\n\nGPT selected **rank9-memory-denial6 — mind-collapse and unravel-identity** next. Authority remains **811/37/0**.\n"
    snapshot_path.write_text(snapshot, encoding="utf-8", newline="\n")

    print(json.dumps({"status": status, "audit": audit_info, "receipt": receipt_info,
                      "nextGroup": NEXT, "queue": queue_info}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
