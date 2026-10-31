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
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
BLOCKERS = {"psychic-scream": ["PF182-B01"], "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def info(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    report_path = BASE / "RANK9PSYCHICFEAR7_RETURN234_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"
    report, receipt = read(report_path), read(receipt_path)
    assert report["status"] == receipt["status"] == "PASS" and report["failedChecks"] == receipt["failedChecks"] == 0
    archive = BASE / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
    delivery_path = BASE / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD_DELIVERY.json"
    delivery = read(delivery_path)
    assert delivery["authority"] == AUTHORITY and delivery["heldIds"] == TARGETS and delivery["acceptedIds"] == delivery["appliedIds"] == []
    next_group = delivery["nextPendingGroup"]
    assert next_group["group"] == "rank9-death-recovery7" and next_group["pendingIds"] == ["final-word"]

    now = datetime.now(timezone.utc).isoformat()
    return_record = {
        "return": 234,
        "group": "rank9-psychic-fear7",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockerIds": BLOCKERS,
        "archive": info(archive),
        "delivery": info(delivery_path),
        "independentAudit": info(report_path),
        "receipt": info(receipt_path),
    }

    submission_path = BASE / "RANK9PSYCHICFEAR7_PACKET_234_SUBMISSION.json"
    submission = read(submission_path)
    submission.update({"status": "RETURN234_AUDITED_HELD_811_37_0", "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "return234": return_record, "auditStatus": "PASS", "auditChecks": report["checkCount"], "auditFailures": 0, "returnedAtUtc": now})
    write(submission_path, submission)

    q234_path = BASE / "CURRENT_SPELL_QUEUE_234.json"
    h234_path = BASE / "CURRENT_HANDOFF_234.json"
    p234_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_234.json"
    q234, h234, p234 = read(q234_path), read(h234_path), read(p234_path)
    assert q234["currentAuthority"] == h234["currentAuthority"] == p234["authority"] == AUTHORITY
    q = copy.deepcopy(q234)
    q.update({
        "id": "SPELL-REVIEW-QUEUE-235",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-234",
        "status": "RETURN234_AUDITED_HELD_811_37_0_PACKET235_PREPARATION",
        "packetStatus": "RETURN234_AUDITED_HELD_811_37_0_PACKET235_PREPARATION",
        "currentReturnAudit": return_record["independentAudit"],
        "currentReturnDelivery": return_record["delivery"],
        "currentReturnArchive": return_record["archive"],
        "currentReturnBinding": return_record["archive"],
        "currentReturnReceipt": return_record["receipt"],
        "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "currentReturnSourceArchive": info(BASE / "rank9_psychicfear7_current_source_234_prepared/DD_Rank9_PsychicFear7_CurrentSource_234.zip"),
        "currentReturnSourceDelivery": info(BASE / "rank9_psychicfear7_current_source_234_prepared/DD_Rank9_PsychicFear7_CurrentSource_234_DELIVERY.json"),
        "currentPacket": None,
        "currentDeliveryManifest": None,
        "currentPacketDelivery": None,
        "currentPreparation": None,
        "currentSubmission": None,
        "currentPacketAudit": None,
        "currentPacketAuditReceipt": None,
        "packetAuditStatus": None,
        "packetAuditChecks": None,
        "packetAuditFailures": None,
        "submittedAtUtc": None,
        "nextGroup": "rank9-death-recovery7",
        "next": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1, "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {
            "group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1,
            "status": "FRESH_PACKET235_PREPARATION_IN_PROGRESS", "freshPacketRequiredForCurrentAuthority": True,
            "historicalWorkflow": "Return184 accepted four other identities; Return217 accepted and applied doom and eternal-pact, while final-word remained held as DR217-B01. This is a fresh current-authority reassessment of final-word only.",
            "previousHeldBatches": [return_record], "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None,
        },
        "lastReviewedBatch": {
            "group": "rank9-psychic-fear7", "pendingIds": TARGETS, "acceptedIds": [], "appliedIds": [],
            "heldIds": TARGETS, "blockerIds": BLOCKERS,
            "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"],
            "returnAudit": return_record["independentAudit"], "returnReceipt": return_record["receipt"],
        },
        "githubChanges": False,
    })
    p = copy.deepcopy(p234)
    p.update({
        "id": "CURRENT37-PENDING-IDENTITY-AUDIT-235", "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN234",
        "lastDirectorReturn": {**return_record, "auditStatus": "PASS"},
        "preparedNextGroup": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1, "historicalPhase": "HELD_RETURN217_DR217-B01_REASSESSMENT_REQUIRED", "freshPacketRequiredForCurrentAuthority": True},
        "preservedRecentHolds": [*p234.get("preservedRecentHolds", []), {"ids": TARGETS, "blockerIds": BLOCKERS, "return": return_record}],
        "authority": AUTHORITY,
    })
    p235_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_235.json"
    write(p235_path, p)
    q["pendingIdentityAudit"] = info(p235_path)
    q235_path = BASE / "CURRENT_SPELL_QUEUE_235.json"
    write(q235_path, q)

    h = copy.deepcopy(h234)
    h.update({
        "id": "CURRENT-HANDOFF-235", "recordedAtUtc": now,
        "status": "RETURN234_AUDITED_HELD_PACKET235_PREPARATION_811_37",
        "currentAuthority": AUTHORITY,
        "pendingIdentityAudit": info(p235_path), "queue": info(q235_path), "currentQueueBinding": info(q235_path),
        "latestBatch": {"group": "rank9-psychic-fear7", "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS, "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"], "independentAudit": return_record["independentAudit"], "receipt": return_record["receipt"]},
        "currentReturnBinding": return_record["archive"], "currentReturnArchive": return_record["archive"], "currentReturnDelivery": return_record["delivery"],
        "currentReturnAudit": return_record["independentAudit"], "currentReturnReceipt": return_record["receipt"], "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "nextStep": "Prepare fresh current-authority Packet235 for final-word only; send to GPT, monitor the browser and ping as needed; audit the sealed return and apply only exact accepted identities.",
        "resumePriority": "Prepare and independently audit Packet235 for final-word only. GPT selected this as the next pending identity after Return234. Send to Calibration review part 6, keep reading the browser and ping if needed, then audit any decision before applying exact accepted IDs.",
        "nextGroup": "rank9-death-recovery7", "nextPendingCount": 1,
        "currentPacket": None, "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
        "currentPreparation": None, "currentSubmission": None, "packetAuditStatus": None, "packetAuditChecks": None, "packetAuditFailures": None,
        "githubChanges": False, "runtimeSelectionEnabled": False, "canonicalRuntimeApplicationPerformed": False,
    })
    h["queue"] = info(q235_path)
    h["currentQueueBinding"] = info(q235_path)
    h["pendingIdentityAudit"] = info(p235_path)
    h235_path = BASE / "CURRENT_HANDOFF_235.json"
    write(h235_path, h)

    snapshot = f"""# Current Ordinary Spell Review Snapshot 235\n\nAuthority remains **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\nReturn234 independently passed {report['checkCount']} checks. GPT held psychic-scream, mass-phantom-killer and weird under PF182-B01/B02, with no acceptance or application. Its sealed return identifies **rank9-death-recovery7 — final-word only** as the next group.\n\nThe final-word history is preserved: Return184 accepted four other Death/Recovery identities; Return217 accepted and applied doom and eternal-pact while final-word remained held under DR217-B01. Packet235 must refresh all evidence to current source and review only final-word. No canonical or GitHub changes have been made.\n"""
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_235.md").write_text(snapshot, encoding="utf-8")
    print(json.dumps({"status": q["status"], "authority": AUTHORITY, "heldIds": TARGETS, "nextGroup": next_group, "queue": info(q235_path), "handoff": info(h235_path), "pendingAudit": info(p235_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
