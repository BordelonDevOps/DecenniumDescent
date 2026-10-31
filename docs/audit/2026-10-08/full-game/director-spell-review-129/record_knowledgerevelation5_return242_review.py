from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    audit_path = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN242_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["acceptedIds"] == audit["appliedIds"] == [] and audit["heldIds"] == ["faction-omniscience-supreme"]
    now = datetime.now(timezone.utc).isoformat()
    retzip = BASE / "rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip"
    retdelivery = BASE / "rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json"
    retzip_info, retdelivery_info = info(retzip), info(retdelivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "RETURN242_AUDITED_HELD_NEXT_PLANAR_GATES5_811_37_0"

    sub_path = BASE / "RANK9KNOWLEDGEREVELATION5_PACKET_242_SUBMISSION.json"
    sub = read(sub_path)
    sub.update({"status": status, "return": 242, "returnArchive": retzip_info,
        "returnDeliveryManifest": retdelivery_info, "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info, "acceptedIds": [], "appliedIds": [],
        "heldIds": audit["heldIds"], "blockers": audit["blockers"], "conditionalQualifications": audit["conditionalQualifications"],
        "nextGroup": audit["nextGroup"], "returnedAtUtc": now, "canonicalChanges": False, "githubChanges": False})
    write(sub_path, sub)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
    pending = read(pending_path)
    pending.update({"recordedAtUtc": now, "status": status,
        "lastDirectorReturn": {"return": 242, "group": "rank9-knowledge-revelation5",
            "acceptedIds": [], "appliedIds": [], "heldIds": audit["heldIds"],
            "blockers": audit["blockers"], "conditionalQualifications": audit["conditionalQualifications"],
            "independentAudit": audit_info, "receipt": receipt_info, "archive": retzip_info,
            "deliveryManifest": retdelivery_info, "nextGroup": audit["nextGroup"]},
        "appliedReturn242": False,
        "preparedNextGroup": {"group": audit["nextGroup"]["group"], "pendingIds": audit["nextGroup"]["pendingIds"],
            "pendingCount": len(audit["nextGroup"]["pendingIds"]), "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN242",
            "freshPacketRequiredForCurrentAuthority": True},
        "acceptedIds": [], "appliedIds": [], "heldIds": audit["heldIds"]})
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_242.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": info(pending_path), "currentSubmission": info(sub_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": retzip_info, "currentReturnDelivery": retdelivery_info,
        "nextGroup": audit["nextGroup"]["group"], "nextPendingIds": audit["nextGroup"]["pendingIds"],
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": audit["heldIds"],
        "currentReturnBlockers": audit["blockers"], "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-knowledge-revelation5":
            row.update({"status": status, "heldIds": audit["heldIds"], "blockers": audit["blockers"]})
        if row.get("group") == audit["nextGroup"]["group"]:
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN242", "freshPacketRequiredForCurrentAuthority": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_242.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status, "pendingIdentityAudit": info(pending_path),
        "queue": info(queue_path), "currentQueueBinding": info(queue_path), "currentSubmission": info(sub_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": retzip_info, "currentReturnDelivery": retdelivery_info,
        "latestBatch": {"return": 242, "group": "rank9-knowledge-revelation5", "ids": audit["targetIds"],
            "acceptedIds": [], "appliedIds": [], "heldIds": audit["heldIds"], "blockers": audit["blockers"],
            "conditionalQualifications": audit["conditionalQualifications"], "independentAudit": audit_info,
            "receipt": receipt_info},
        "nextGroup": audit["nextGroup"]["group"], "nextPendingIds": audit["nextGroup"]["pendingIds"],
        "nextPendingCount": len(audit["nextGroup"]["pendingIds"]),
        "nextStep": "Prepare a fresh exact-source Planar Gates5 packet for banishment-gate and conjure-demiplane-fortress; preserve Return242 and prior holds.",
        "resumePriority": "Return242 passed 15 independent checks and both authority and canonical files remain unchanged. Continue with the director-selected Planar Gates5 pair; audit the sealed return before applying only any exact accepted identity."})
    write(handoff_path, handoff)
    print(json.dumps({"status": status, "submission": info(sub_path), "pendingAudit": info(pending_path),
        "queue": info(queue_path), "handoff": info(handoff_path), "audit": audit_info}, indent=2))


if __name__ == "__main__":
    main()
