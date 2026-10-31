from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
BLOCKERS = {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}
NEXT_IDS = ["nullification-wave", "reality-anchor"]


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{__import__('zlib').crc32(raw) & 0xffffffff:08x}"}


def info(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    report_path = BASE / "RANK9DEFENSEFORM8_RETURN236_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9DEFENSEFORM8_RETURN236_RECEIPT.json"
    report, receipt = read(report_path), read(receipt_path)
    assert report["status"] == receipt["status"] == "PASS" and report["failedChecks"] == receipt["failedChecks"] == 0
    archive = BASE / "rank9_defenseform8_return236_received/DD_Rank9_DefenseForm3_Director_Return236_HELD.zip"
    delivery_path = BASE / "rank9_defenseform8_return236_received/DD_Rank9_DefenseForm3_Director_Return236_HELD_DELIVERY.json"
    delivery = read(delivery_path)
    assert delivery["authority"] == AUTHORITY and delivery["heldIds"] == TARGETS and delivery["acceptedIds"] == delivery["appliedIds"] == []
    assert delivery["nextPendingGroup"] == "rank9-ward-control6" and delivery["nextPendingIds"] == NEXT_IDS
    decision = json.loads(__import__("zipfile").ZipFile(archive).read("DIRECTOR_DECISION.json"))
    assert decision["heldIds"] == TARGETS and decision["acceptedIds"] == decision["appliedIds"] == []

    now = datetime.now(timezone.utc).isoformat()
    return_record = {
        "return": 236,
        "group": "rank9-defense-form8",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockerIds": BLOCKERS,
        "archive": info(archive),
        "delivery": info(delivery_path),
        "independentAudit": info(report_path),
        "receipt": info(receipt_path),
        "segmentManifest": {"path": "C:/Users/cbord/Downloads/Return236_SEGMENTS.json", **digest(Path(r"C:\Users\cbord\Downloads\Return236_SEGMENTS.json").read_bytes())},
    }

    q236_path = BASE / "CURRENT_SPELL_QUEUE_236.json"
    h236_path = BASE / "CURRENT_HANDOFF_236.json"
    p236_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_236.json"
    q236, h236, p236 = read(q236_path), read(h236_path), read(p236_path)
    assert q236["currentAuthority"] == h236["currentAuthority"] == p236["authority"] == AUTHORITY
    assert p236["pendingCount"] == AUTHORITY["pending"]

    p237 = copy.deepcopy(p236)
    p237.update({
        "id": "CURRENT37-PENDING-IDENTITY-AUDIT-237",
        "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN236",
        "lastDirectorReturn": {**return_record, "auditStatus": "PASS"},
        "preparedNextGroup": {"group": "rank9-ward-control6", "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS), "historicalPhase": "HELD_RETURN188_WC188_B01_B02_REASSESS_FROM_CURRENT_SOURCES", "freshPacketRequiredForCurrentAuthority": True},
        "preservedRecentHolds": [*p236.get("preservedRecentHolds", []), {"ids": TARGETS, "blockerIds": BLOCKERS, "return": return_record}],
        "authority": AUTHORITY,
    })
    p237_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_237.json"
    write(p237_path, p237)

    q237 = copy.deepcopy(q236)
    q237.update({
        "id": "SPELL-REVIEW-QUEUE-237",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-236",
        "status": "RETURN236_AUDITED_HELD_811_37_0_PACKET237_PREPARATION",
        "packetStatus": "RETURN236_AUDITED_HELD_811_37_0_PACKET237_PREPARATION",
        "currentReturnAudit": return_record["independentAudit"],
        "currentReturnDelivery": return_record["delivery"],
        "currentReturnArchive": return_record["archive"],
        "currentReturnBinding": return_record["archive"],
        "currentReturnReceipt": return_record["receipt"],
        "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "currentReturnSourceArchive": info(BASE / "rank9_defenseform8_current_source_236_prepared/DD_Rank9_DefenseForm8_CurrentSource_236.zip"),
        "currentReturnSourceDelivery": info(BASE / "rank9_defenseform8_current_source_236_prepared/DD_Rank9_DefenseForm8_CurrentSource_236_DELIVERY.json"),
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
        "nextGroup": "rank9-ward-control6",
        "next": {"group": "rank9-ward-control6", "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS), "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {"group": "rank9-ward-control6", "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS), "status": "PACKET237_PREPARATION_IN_PROGRESS", "freshPacketRequiredForCurrentAuthority": True, "historicalWorkflow": "Return188 held nullification-wave under WC188-B01 and reality-anchor under WC188-B02. Four other Ward/Control6 identities were accepted and applied; reassess only the two pending identities.", "previousHeldBatches": [return_record], "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None},
        "lastReviewedBatch": {"group": "rank9-defense-form8", "pendingIds": TARGETS, "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS, "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"], "returnAudit": return_record["independentAudit"], "returnReceipt": return_record["receipt"]},
        "githubChanges": False,
    })
    group = next(g for g in q237["currentPendingGroups"] if g["group"] == "rank9-defense-form8")
    group.update({"status": "RETURN236_AUDITED_HELD_811_37_0", "freshPacketRequiredForCurrentAuthority": True, "lastDirectorReturn": return_record})
    pending_group = next((g for g in q237["currentPendingGroups"] if g["group"] == "rank9-ward-control6"), None)
    if pending_group:
        pending_group.update({"status": "FRESH_CURRENT_PACKET_REQUIRED_811_37_0", "freshPacketRequiredForCurrentAuthority": True})
    p237_binding = info(p237_path)
    q237["pendingIdentityAudit"] = p237_binding
    q237_path = BASE / "CURRENT_SPELL_QUEUE_237.json"
    write(q237_path, q237)

    h237 = copy.deepcopy(h236)
    h237.update({
        "id": "CURRENT-HANDOFF-237",
        "recordedAtUtc": now,
        "status": "RETURN236_AUDITED_HELD_PACKET237_PREPARATION_811_37",
        "currentAuthority": AUTHORITY,
        "pendingIdentityAudit": p237_binding,
        "queue": info(q237_path),
        "currentQueueBinding": info(q237_path),
        "latestBatch": {"group": "rank9-defense-form8", "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS, "returnArchive": return_record["archive"], "returnDelivery": return_record["delivery"], "independentAudit": return_record["independentAudit"], "receipt": return_record["receipt"]},
        "currentReturnBinding": return_record["archive"],
        "currentReturnArchive": return_record["archive"],
        "currentReturnDelivery": return_record["delivery"],
        "currentReturnAudit": return_record["independentAudit"],
        "currentReturnReceipt": return_record["receipt"],
        "currentReturnDecision": delivery["id"].replace("-DELIVERY", ""),
        "nextGroup": "rank9-ward-control6",
        "nextPendingIds": NEXT_IDS,
        "nextPendingCount": len(NEXT_IDS),
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
        "nextStep": "Prepare a fresh current-source packet for nullification-wave and reality-anchor; submit it to GPT, monitor and ping as needed; independently audit the sealed return before applying exact accepted identities.",
        "resumePriority": "Return236 independently passed 12 transfer/package checks and held all three Defense/Form8 identities. Continue with GPT's exact next group: nullification-wave and reality-anchor only; preserve the four prior Ward/Control6 acceptances and all completed feats.",
    })
    h237_path = BASE / "CURRENT_HANDOFF_237.json"
    write(h237_path, h237)

    snapshot = f"""# Current Ordinary Spell Review Snapshot 237

Authority remains **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.

Return236 independently passed {report['checkCount']} transfer and archive checks. GPT held `elemental-shell`, `timeless-form`, and `invulnerable-sphere`; no spell was accepted or applied. The Deep Crust Spike byte discrepancy was verified as Windows CRLF conversion and the exact LF-bound candidate/receipt match the index.

GPT's sealed next group is **rank9-ward-control6**: `nullification-wave` and `reality-anchor` only. Return188 previously applied `greater-spell-turning`, `eternal-ward`, `ultimate-ward`, and `prismatic-sphere`; preserve them and do not revisit completed feats.
"""
    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_237.md"
    snapshot_path.write_text(snapshot, encoding="utf-8")
    print(json.dumps({"status": q237["status"], "authority": AUTHORITY, "heldIds": TARGETS, "nextGroup": {"group": "rank9-ward-control6", "pendingIds": NEXT_IDS}, "queue": info(q237_path), "handoff": info(h237_path), "pendingAudit": p237_binding, "snapshot": info(snapshot_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
