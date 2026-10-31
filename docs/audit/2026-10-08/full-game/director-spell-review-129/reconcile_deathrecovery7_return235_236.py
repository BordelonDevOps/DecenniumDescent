from __future__ import annotations

import copy
import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["final-word"]
BLOCKERS = {"final-word": ["DR217-B01"]}
NEXT = ["elemental-shell", "timeless-form", "invulnerable-sphere"]


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def info(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    report_path = BASE / "RANK9DEATHRECOVERY7_RETURN235_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9DEATHRECOVERY7_RETURN235_RECEIPT.json"
    report, receipt = read(report_path), read(receipt_path)
    assert report["status"] == receipt["status"] == "PASS" and report["failedChecks"] == receipt["failedChecks"] == 0
    archive = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"
    delivery_path = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json"
    delivery = read(delivery_path)
    assert delivery["authority"] == AUTHORITY and delivery["heldIds"] == TARGETS and delivery["acceptedIds"] == delivery["appliedIds"] == []
    next_group = report["nextGroup"]
    assert next_group["group"] == delivery["nextPendingGroup"] == "rank9-defense-form8" and next_group["pendingIds"] == delivery["nextPendingIds"] == NEXT

    now = datetime.now(timezone.utc).isoformat()
    return_record = {
        "return": 235,
        "group": "rank9-death-recovery7",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockerIds": BLOCKERS,
        "archive": info(archive),
        "delivery": info(delivery_path),
        "independentAudit": info(report_path),
        "receipt": info(receipt_path),
    }

    q235_path = BASE / "CURRENT_SPELL_QUEUE_235.json"
    h235_path = BASE / "CURRENT_HANDOFF_235.json"
    p235_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_235.json"
    q235, h235, p235 = read(q235_path), read(h235_path), read(p235_path)
    assert q235["currentAuthority"] == h235["currentAuthority"] == p235["authority"] == AUTHORITY
    assert p235["pendingCount"] == len(p235["pendingIds"]) == AUTHORITY["pending"]

    p236 = copy.deepcopy(p235)
    p236.update({
        "id": "CURRENT37-PENDING-IDENTITY-AUDIT-236",
        "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN235",
        "lastDirectorReturn": {**return_record, "auditStatus": "PASS"},
        "preparedNextGroup": {"group": next_group["group"], "pendingIds": NEXT, "pendingCount": len(NEXT), "historicalPhase": "HELD_RETURN218_DF218_BLOCKERS_REASSESS_FROM_CURRENT_SOURCES", "freshPacketRequiredForCurrentAuthority": True},
        "preservedRecentHolds": [*p235.get("preservedRecentHolds", []), {"ids": TARGETS, "blockerIds": BLOCKERS, "return": return_record}],
        "authority": AUTHORITY,
    })
    p236_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_236.json"
    write(p236_path, p236)

    q236 = copy.deepcopy(q235)
    q236.update({
        "id": "SPELL-REVIEW-QUEUE-236",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-235",
        "status": "RETURN235_AUDITED_HELD_811_37_0_PACKET236_PREPARATION",
        "packetStatus": "RETURN235_AUDITED_HELD_811_37_0_PACKET236_PREPARATION",
        "currentReturnAudit": return_record["independentAudit"],
        "currentReturnDelivery": return_record["delivery"],
        "currentReturnArchive": return_record["archive"],
        "currentReturnBinding": return_record["archive"],
        "currentReturnReceipt": return_record["receipt"],
        "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "currentReturnSourceArchive": info(BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235.zip"),
        "currentReturnSourceDelivery": info(BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"),
        "currentPacket": None,
        "currentDeliveryManifest": None,
        "currentPacketDelivery": None,
        "currentPreparation": None,
        "currentSubmission": None,
        "currentPacketAudit": None,
        "currentPacketAuditReceipt": None,
        "currentPacketAuditStatus": None,
        "currentPacketAuditChecks": None,
        "currentPacketAuditFailures": None,
        "submittedAtUtc": None,
        "nextGroup": next_group["group"],
        "next": {"group": next_group["group"], "pendingIds": NEXT, "pendingCount": len(NEXT), "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {"group": next_group["group"], "pendingIds": NEXT, "pendingCount": len(NEXT), "status": "PACKET236_PREPARATION_IN_PROGRESS", "freshPacketRequiredForCurrentAuthority": True, "historicalWorkflow": "Return218 applied absolute-immunity and body-to-void. Three identities remained held under DF218-B01/B02/B03/B04; obtain a fresh current-source reassessment of these three only.", "previousHeldBatches": [return_record], "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None},
        "lastReviewedBatch": {"group": "rank9-death-recovery7", "pendingIds": TARGETS, "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS, "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"], "returnAudit": return_record["independentAudit"], "returnReceipt": return_record["receipt"]},
        "githubChanges": False,
    })
    p236_binding = info(p236_path)
    q236["pendingIdentityAudit"] = p236_binding
    q236_path = BASE / "CURRENT_SPELL_QUEUE_236.json"
    write(q236_path, q236)

    h236 = copy.deepcopy(h235)
    h236.update({
        "id": "CURRENT-HANDOFF-236",
        "recordedAtUtc": now,
        "status": "RETURN235_AUDITED_HELD_PACKET236_PREPARATION_811_37",
        "currentAuthority": AUTHORITY,
        "pendingIdentityAudit": p236_binding,
        "queue": info(q236_path),
        "currentQueueBinding": info(q236_path),
        "latestBatch": {"group": "rank9-death-recovery7", "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS, "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"], "independentAudit": return_record["independentAudit"], "receipt": return_record["receipt"]},
        "currentReturnBinding": return_record["archive"],
        "currentReturnArchive": return_record["archive"],
        "currentReturnDelivery": return_record["delivery"],
        "currentReturnAudit": return_record["independentAudit"],
        "currentReturnReceipt": return_record["receipt"],
        "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "nextGroup": next_group["group"],
        "nextPendingIds": NEXT,
        "nextPendingCount": len(NEXT),
        "currentPacket": None,
        "currentPacketDelivery": None,
        "currentPacketAudit": None,
        "currentPacketAuditReceipt": None,
        "currentPreparation": None,
        "currentSubmission": None,
        "packetAuditStatus": None,
        "packetAuditChecks": None,
        "packetAuditFailures": None,
        "githubChanges": False,
        "runtimeSelectionEnabled": False,
        "canonicalRuntimeApplicationPerformed": False,
        "nextStep": "Prepare a fresh current-source packet for elemental-shell, timeless-form, and invulnerable-sphere; submit it to GPT, monitor and ping as needed; independently audit the sealed return before applying exact accepted identities.",
        "resumePriority": "Return235 independently passed 19 checks and held final-word under DR217-B01. Continue with GPT's next group: exactly the three Defense/Form8 identities; refresh all current source bindings, ping if needed, and apply only independently audited exact acceptances.",
    })
    h236_path = BASE / "CURRENT_HANDOFF_236.json"
    write(h236_path, h236)

    snapshot = f"""# Current Ordinary Spell Review Snapshot 236\n\nAuthority remains **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\nReturn235 independently passed {report['checkCount']} checks. GPT held `final-word` under DR217-B01 after assessing the Gorthan source lead. No spell was accepted or applied.\n\nGPT's sealed next group is **rank9-defense-form8**: `elemental-shell`, `timeless-form`, and `invulnerable-sphere`. Return218 had already applied `absolute-immunity` and `body-to-void`; only these three remain in this group. Prepare a fresh current-source review and preserve the prior accepted identities and unrelated holds.\n"""
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_236.md").write_text(snapshot, encoding="utf-8")
    print(json.dumps({"status": q236["status"], "authority": AUTHORITY, "heldIds": TARGETS, "nextGroup": next_group, "queue": info(q236_path), "handoff": info(h236_path), "pendingAudit": p236_binding}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
