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
    audit_path = BASE / "RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9_PLANARGATES5_RETURN243_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checksFailed"] == 0 and audit["checksPassed"] == 17
    target_ids = ["banishment-gate", "conjure-demiplane-fortress"]
    blockers = {"banishment-gate": ["PG200-B03", "PG200-B04"],
        "conjure-demiplane-fortress": ["PG200-B06"]}
    quals = [f"PG200-H{i:02d}" for i in range(1, 11)]
    next_group = {"group": "rank9-summon-hosts5", "pendingIds": [
        "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]}
    now = datetime.now(timezone.utc).isoformat()
    retzip = BASE / "rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD.zip"
    retdelivery = BASE / "rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD_DELIVERY.json"
    retzip_info, retdelivery_info = info(retzip), info(retdelivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    status = "RETURN243_AUDITED_HELD_NEXT_SUMMON_HOSTS5_811_37_0"

    sub_path = BASE / "RANK9PLANARGATES5_PACKET_243_SUBMISSION.json"
    sub = read(sub_path)
    sub.update({"status": status, "return": 243, "returnArchive": retzip_info,
        "returnDeliveryManifest": retdelivery_info, "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info, "acceptedIds": [], "appliedIds": [],
        "heldIds": target_ids, "blockers": blockers, "conditionalQualifications": quals,
        "nextGroup": next_group, "returnedAtUtc": now, "canonicalChanges": False, "githubChanges": False})
    write(sub_path, sub)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
    pending = read(pending_path)
    pending.update({"recordedAtUtc": now, "status": status,
        "lastDirectorReturn": {"return": 243, "group": "rank9-planar-gates5", "targetIds": target_ids,
            "acceptedIds": [], "appliedIds": [], "heldIds": target_ids, "blockers": blockers,
            "conditionalQualifications": quals, "independentAudit": audit_info, "receipt": receipt_info,
            "archive": retzip_info, "deliveryManifest": retdelivery_info, "nextGroup": next_group},
        "appliedReturn243": False,
        "preparedNextGroup": {"group": next_group["group"], "pendingIds": next_group["pendingIds"],
            "pendingCount": len(next_group["pendingIds"]), "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN243",
            "freshPacketRequiredForCurrentAuthority": True},
        "acceptedIds": [], "appliedIds": [], "heldIds": target_ids})
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_243.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": status, "packetStatus": status,
        "pendingIdentityAudit": info(pending_path), "currentSubmission": info(sub_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": retzip_info, "currentReturnDelivery": retdelivery_info,
        "nextGroup": next_group["group"], "nextPendingIds": next_group["pendingIds"],
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": target_ids,
        "currentReturnBlockers": blockers, "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-planar-gates5":
            row.update({"status": status, "heldIds": target_ids, "blockers": blockers})
        if row.get("group") == next_group["group"]:
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN243", "freshPacketRequiredForCurrentAuthority": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_243.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": status, "pendingIdentityAudit": info(pending_path),
        "queue": info(queue_path), "currentQueueBinding": info(queue_path), "currentSubmission": info(sub_path),
        "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
        "currentReturnBinding": retzip_info, "currentReturnDelivery": retdelivery_info,
        "latestBatch": {"return": 243, "group": "rank9-planar-gates5", "ids": target_ids,
            "acceptedIds": [], "appliedIds": [], "heldIds": target_ids, "blockers": blockers,
            "conditionalQualifications": quals, "independentAudit": audit_info, "receipt": receipt_info},
        "nextGroup": next_group["group"], "nextPendingIds": next_group["pendingIds"],
        "nextPendingCount": len(next_group["pendingIds"]),
        "nextStep": "Prepare the director-selected Rank9 Summon/Hosts5 packet for summon-elemental-avatar, summon-herald-of-the-planes, and summon-avatar-of-decay; preserve Return243 and earlier holds.",
        "resumePriority": "Return243 passed 17 independent checks; its 23 historical cases remain byte-exact and authority/canonical content remain unchanged. Continue with director-selected Summon/Hosts5; audit the next sealed return before applying only an exact acceptance."})
    write(handoff_path, handoff)
    print(json.dumps({"status": status, "submission": info(sub_path), "pendingAudit": info(pending_path),
        "queue": info(queue_path), "handoff": info(handoff_path), "audit": audit_info}, indent=2))


if __name__ == "__main__":
    main()
