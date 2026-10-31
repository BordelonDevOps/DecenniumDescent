from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_impactexile4_return286_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return286_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json"
AUDIT = BASE / "RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9IMPACTEXILE4_RETURN286_RECEIPT.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_286.json"
HANDOFF = BASE / "CURRENT_HANDOFF_286.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_286.json"
PACKET = BASE / "RANK9IMPACTEXILE4_PACKET_286.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_286.md"
START = ROOT / "START_HERE.md"

TARGETS = ["reverse-gravity-field"]
BLOCKERS = {"reverse-gravity-field": ["IE204-B02"]}
NEXT = {
    "group": "rank9-alignment-faction-purification5",
    "pendingIds": [
        "alignment-ascension",
        "alignment-perfection",
        "faction-incarnate",
        "faction-perfection",
        "corruption-purification",
    ],
}
STATUS = "RETURN286_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_816_32_0"


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


def member_info(name: str) -> dict:
    with ZipFile(ARCHIVE) as archive:
        raw = archive.read(name)
    return {
        "archive": info(ARCHIVE),
        "member": name,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}",
    }


def main() -> None:
    audit, receipt, delivery = read(AUDIT), read(RECEIPT), read(DELIVERY)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 16 and audit["failedChecks"] == 0
    assert delivery["acceptedIds"] == delivery["appliedIds"] == []
    assert delivery["heldIds"] == TARGETS and delivery["blockerIds"] == BLOCKERS
    assert delivery["authority"]["reviewedApplied"] == 816 and delivery["authority"]["pending"] == 32

    now = datetime.now(timezone.utc).isoformat()
    archive_info, delivery_info = info(ARCHIVE), info(DELIVERY)
    audit_info, receipt_info = info(AUDIT), info(RECEIPT)
    decision_info = member_info("DIRECTOR_DECISION.json")
    qualifications = delivery["qualificationIds"]

    packet = read(PACKET)
    packet.update({
        "status": STATUS,
        "return": 286,
        "returnArchive": archive_info,
        "returnDeliveryManifest": delivery_info,
        "returnDecision": decision_info,
        "returnAudit": audit_info,
        "returnAuditReceipt": receipt_info,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": BLOCKERS,
        "conditionalQualifications": qualifications,
        "nextGroup": NEXT,
        "returnedAtUtc": now,
        "canonicalChanges": False,
        "githubChanges": False,
    })
    write(PACKET, packet)

    pending = read(PENDING)
    pending.update({
        "recordedAtUtc": now,
        "status": STATUS,
        "lastDirectorReturn": {
            "return": 286,
            "group": "rank9-impact-exile4",
            "targetIds": TARGETS,
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": TARGETS,
            "blockers": BLOCKERS,
            "conditionalQualifications": qualifications,
            "independentAudit": audit_info,
            "receipt": receipt_info,
            "archive": archive_info,
            "deliveryManifest": delivery_info,
            "nextGroup": NEXT,
            "minimumMissingWitnesses": audit["checks"][7]["detail"],
        },
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "preparedNextGroup": {
            "group": NEXT["group"],
            "pendingIds": NEXT["pendingIds"],
            "pendingCount": len(NEXT["pendingIds"]),
            "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN286",
            "freshPacketRequiredForCurrentAuthority": True,
        },
        "nextGroup": NEXT["group"],
    })
    write(PENDING, pending)

    queue = read(QUEUE)
    pending_info = info(PENDING)
    queue.update({
        "recordedAtUtc": now,
        "status": STATUS,
        "packetStatus": STATUS,
        "pendingIdentityAudit": pending_info,
        "currentPacketRecord": info(PACKET),
        "currentReturnArchive": archive_info,
        "currentReturnBinding": archive_info,
        "currentReturnDelivery": delivery_info,
        "currentReturnAudit": audit_info,
        "currentReturnReceipt": receipt_info,
        "currentReturnDecision": decision_info,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": TARGETS,
        "currentReturnBlockers": BLOCKERS,
        "nextGroup": NEXT["group"],
        "nextPendingIds": NEXT["pendingIds"],
        "nextPendingCount": len(NEXT["pendingIds"]),
        "githubChanges": False,
    })
    queue["next"] = {
        "group": NEXT["group"],
        "pendingIds": NEXT["pendingIds"],
        "pendingCount": len(NEXT["pendingIds"]),
        "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN286_FRESH_PACKET_REQUIRED",
        "freshPacketRequiredForCurrentAuthority": True,
    }
    queue["nextPreparedRequest"] = {
        "group": NEXT["group"],
        "pendingIds": NEXT["pendingIds"],
        "pendingCount": len(NEXT["pendingIds"]),
        "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN286_FRESH_PACKET_REQUIRED",
        "freshPacketRequiredForCurrentAuthority": True,
        "sourceReturn": archive_info,
        "returnAudit": audit_info,
    }
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-impact-exile4":
            row.update({"status": STATUS, "heldIds": TARGETS, "blockers": BLOCKERS})
        if row.get("group") == NEXT["group"]:
            row.update({
                "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN286",
                "freshPacketRequiredForCurrentAuthority": True,
            })
    write(QUEUE, queue)

    handoff = read(HANDOFF)
    queue_info = info(QUEUE)
    packet_info = info(PACKET)
    pending_info = info(PENDING)
    handoff.update({
        "recordedAtUtc": now,
        "status": STATUS,
        "pendingIdentityAudit": pending_info,
        "queue": queue_info,
        "queueBinding": queue_info,
        "currentQueueBinding": queue_info,
        "currentPacketRecord": packet_info,
        "currentReturnArchive": archive_info,
        "currentReturnBinding": archive_info,
        "currentReturnDelivery": delivery_info,
        "currentReturnAudit": audit_info,
        "currentReturnReceipt": receipt_info,
        "currentReturnDecision": decision_info,
        "acceptedThisStep": [],
        "latestBatch": {
            "return": 286,
            "group": "rank9-impact-exile4",
            "ids": TARGETS,
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": TARGETS,
            "blockers": BLOCKERS,
            "conditionalQualifications": qualifications,
            "independentAudit": audit_info,
            "auditReceipt": receipt_info,
            "archive": archive_info,
            "deliveryManifest": delivery_info,
        },
        "unacceptedThisStep": {"ids": TARGETS, "blockers": BLOCKERS, "retainedInPendingSet": True},
        "currentBlocker": {"identity": TARGETS[0], "group": "rank9-impact-exile4", "blockerId": "IE204-B02"},
        "nextGroup": NEXT["group"],
        "nextPendingIds": NEXT["pendingIds"],
        "nextPendingCount": len(NEXT["pendingIds"]),
        "nextStep": {
            "group": NEXT["group"],
            "pendingIds": NEXT["pendingIds"],
            "pendingCount": len(NEXT["pendingIds"]),
            "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN286_FRESH_PACKET_REQUIRED",
            "freshPacketRequiredForCurrentAuthority": True,
        },
        "nextStepText": "Prepare and independently audit a fresh current-source packet for alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, and corruption-purification; preserve the audited Return286 hold and all closed qualifications.",
        "resumePriority": "Return286 passed 16 independent checks and holds reverse-gravity-field under IE204-B02. The six preserved cases replayed, but crate durability/impact/custody and rated tether/anchor upward-load witnesses remain absent. Authority remains 816/32/0. Continue with rank9-alignment-faction-purification5.",
    })
    write(HANDOFF, handoff)

    SNAPSHOT.write_text(
        "# Current ordinary spell-review checkpoint 286\n\n"
        "Return286 passed an independent audit (16/16) and held **reverse-gravity-field** under IE204-B02. "
        "The six preserved cases replayed (224 events; 448 forward and 448 inverse operations), while five cases still lack "
        "the exact crate durability/impact/custody or tether/anchor upward-load witnesses. No acceptance or application occurred. "
        "Authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied** (540 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Next Director-selected group: **rank9-alignment-faction-purification5** — alignment-ascension, alignment-perfection, "
        "faction-incarnate, faction-perfection, and corruption-purification. Prepare a fresh current-source packet before review.\n",
        encoding="utf-8",
    )

    start_lines = START.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = (
        "**Current ordinary spell-review handoff [286](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_286.json):** "
        "Return286 independently audited PASS (16/16), holding reverse-gravity-field under IE204-B02 because crate durability/impact/custody "
        "and tether/anchor upward-load witnesses are missing. Authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**. "
        "Next is alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, and corruption-purification."
    )
    START.write_text("\n".join(start_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": STATUS,
        "archive": archive_info,
        "delivery": delivery_info,
        "audit": audit_info,
        "receipt": receipt_info,
        "packet": info(PACKET),
        "pendingAudit": info(PENDING),
        "queue": queue_info,
        "handoff": info(HANDOFF),
        "authority": delivery["authority"],
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "nextGroup": NEXT,
    }, indent=2))


if __name__ == "__main__":
    main()
