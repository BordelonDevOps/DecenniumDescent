from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_alignmentfactionpurification5_return248_received"
TARGET = ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]
BLOCKERS = {spell: [f"AFP211-B0{i}"] for i, spell in enumerate(TARGET, 1)}
NEXT = {"group": "rank9-projection-confinement2", "pendingIds": ["astral-projection", "imprisonment"]}
STATUS = "RETURN248_AUDITED_HELD_NEXT_PROJECTION_CONFINEMENT2_811_37_0"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main():
    audit_path = BASE / "RANK9ALIGNFACTIONPURIFICATION5_RETURN248_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9ALIGNFACTIONPURIFICATION5_RETURN248_RECEIPT.json"
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit["status"] == receipt["status"] == "PASS"
    assert audit["checkCount"] == audit["passedChecks"] == 24 and audit["failedChecks"] == 0
    archive = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD.zip"
    delivery = RECEIVED / "DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD_DELIVERY.json"
    body = read(delivery)
    assert body["heldIds"] == TARGET and body["blockerIds"] == list(BLOCKERS.values())[0] + list(BLOCKERS.values())[1] + list(BLOCKERS.values())[2] + list(BLOCKERS.values())[3] + list(BLOCKERS.values())[4]
    assert body["accepted"] is False and body["applied"] is False
    assert body["nextPendingGroup"]["group"] == NEXT["group"] and body["nextPendingGroup"]["pendingIds"] == NEXT["pendingIds"]
    archive_info, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    qualifications = body["qualificationIds"]
    now = datetime.now(timezone.utc).isoformat()

    submission_path = BASE / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_248_SUBMISSION.json"
    submission = read(submission_path)
    assert submission["browserVerified"] is True
    submission.update({"status": STATUS, "return": 248, "returnArchive": archive_info,
                       "returnDeliveryManifest": delivery_info, "returnAudit": audit_info,
                       "returnAuditReceipt": receipt_info, "acceptedIds": [], "appliedIds": [],
                       "heldIds": TARGET, "blockers": BLOCKERS,
                       "conditionalQualifications": qualifications, "nextGroup": NEXT,
                       "returnedAtUtc": now, "canonicalChanges": False, "githubChanges": False})
    write(submission_path, submission)
    submission_info = info(submission_path)

    packet_path = BASE / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_248.json"
    packet = read(packet_path)
    packet.update({"status": STATUS, "return": 248, "returnArchive": archive_info,
                   "returnDeliveryManifest": delivery_info, "returnAudit": audit_info,
                   "returnAuditReceipt": receipt_info, "acceptedIds": [], "appliedIds": [],
                   "heldIds": TARGET, "blockers": BLOCKERS, "nextGroup": NEXT})
    write(packet_path, packet)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_248.json"
    pending = read(pending_path)
    pending.update({"recordedAtUtc": now, "status": STATUS, "acceptedIds": [],
                    "appliedIds": [], "heldIds": TARGET,
                    "lastDirectorReturn": {"return": 248, "group": "rank9-alignment-faction-purification5",
                        "targetIds": TARGET, "acceptedIds": [], "appliedIds": [], "heldIds": TARGET,
                        "blockers": BLOCKERS, "conditionalQualifications": qualifications,
                        "independentAudit": audit_info, "receipt": receipt_info,
                        "archive": archive_info, "deliveryManifest": delivery_info, "nextGroup": NEXT},
                    "preparedNextGroup": {"group": NEXT["group"], "pendingIds": NEXT["pendingIds"],
                        "pendingCount": len(NEXT["pendingIds"]), "status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN248",
                        "freshPacketRequiredForCurrentAuthority": True}})
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_248.json"
    queue = read(queue_path)
    queue.update({"recordedAtUtc": now, "status": STATUS, "packetStatus": STATUS,
                  "pendingIdentityAudit": pending_info, "currentSubmission": submission_info,
                  "currentReturnAudit": audit_info, "currentReturnAuditReceipt": receipt_info,
                  "currentReturnBinding": archive_info, "currentReturnDelivery": delivery_info,
                  "nextGroup": NEXT["group"], "nextPendingIds": NEXT["pendingIds"],
                  "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [],
                  "currentReturnHeldIds": TARGET, "currentReturnBlockers": BLOCKERS,
                  "currentReturn": archive_info, "currentReturnAuditStatus": "PASS",
                  "currentReturnAuditChecks": 24, "currentReturnAuditFailures": 0,
                  "githubChanges": False})
    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == "rank9-alignment-faction-purification5":
            row.update({"status": STATUS, "heldIds": TARGET, "blockers": BLOCKERS})
        if row.get("group") == NEXT["group"]:
            row.update({"status": "DIRECTOR_SELECTED_NEXT_AFTER_RETURN248",
                        "freshPacketRequiredForCurrentAuthority": True,
                        "currentAuthority": queue["currentAuthority"],
                        "previousHeldBatch": {"ids": TARGET, "blockers": BLOCKERS,
                                               "acceptedIds": [], "appliedIds": []}})
    write(queue_path, queue)
    queue_info = info(queue_path)

    handoff_path = BASE / "CURRENT_HANDOFF_248.json"
    handoff = read(handoff_path)
    handoff.update({"recordedAtUtc": now, "status": STATUS, "pendingIdentityAudit": pending_info,
                    "queue": queue_info, "currentQueueBinding": queue_info,
                    "currentSubmission": submission_info, "currentReturnAudit": audit_info,
                    "currentReturnAuditReceipt": receipt_info, "currentReturnBinding": archive_info,
                    "currentReturnDelivery": delivery_info, "currentReturnArchive": archive_info,
                    "currentReturn": archive_info, "currentReturnAuditStatus": "PASS",
                    "currentReturnAuditChecks": 24, "currentReturnAuditFailures": 0,
                    "latestBatch": {"return": 248, "group": "rank9-alignment-faction-purification5",
                        "ids": TARGET, "acceptedIds": [], "appliedIds": [], "heldIds": TARGET,
                        "blockers": BLOCKERS, "conditionalQualifications": qualifications,
                        "independentAudit": audit_info, "receipt": receipt_info,
                        "archive": archive_info, "deliveryManifest": delivery_info},
                    "nextGroup": NEXT["group"], "nextPendingIds": NEXT["pendingIds"],
                    "nextPendingCount": len(NEXT["pendingIds"]),
                    "nextStep": "Prepare and independently audit a fresh current-authority Packet249 for only astral-projection and imprisonment; preserve the five AFP holds and all other holds. Continue with GPT's sealed review, then audit any return before applying exact accepted IDs.",
                    "resumePriority": "Return248 passed 24 independent checks. All five alignment/faction/purification identities remain held under AFP211-B01 through B05; AFP211-E01 remains closed. Authority remains 811/37/0. Continue with the two Projection/Confinement identities.",
                    "githubChanges": False})
    write(handoff_path, handoff)

    snapshot = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_248.md"
    snapshot.write_text(
        "# Current Ordinary Spell Review Snapshot 248\n\n"
        "Return248 was independently audited PASS 24/24. Alignment Ascension, Alignment Perfection, Faction Incarnate, Faction Perfection, and Corruption Purification remain held under AFP211-B01 through B05. The six comparator gaps are resolved and AFP211-E01 remains closed. Their remaining witnesses are spell-local definitions and complete positive encounters: Ascension form/insight and lifecycle; Perfection's exact purification operation and axis-dependent benefit lifecycle; Incarnate's manifestation profile, actions/resources, invocation and lifecycle; Faction Perfection's concrete significant benefit with eligibility and finite entitlements; and Purification's complete cure matrix, geometry, and permanent-removal/Until-dispelled reconciliation. Ten component traces pass (10 events, 20 forward/20 inverse operations), but none is a complete positive spell encounter.\n\n"
        "Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** (535 complete standalone procedures; 173 scoped interfaces). GPT selected **Rank9 Projection/Confinement2** next: astral-projection and imprisonment. No acceptance or application occurred. All unrelated holds remain preserved.\n\n"
        "No canonical changes, GitHub changes, runtime execution, implementation approval, human playtest, balance, cosmology, domain closure, completion, or release approval are inferred.\n", encoding="utf-8")

    start = ROOT / "START_HERE.md"
    lines = start.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = ("**Current ordinary spell-review handoff [248](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_248.json):** "
                "Return248 is independently audited PASS 24/24; all five alignment/faction/purification spells remain held under AFP211-B01–B05, with AFP211-E01 closed. Authority is **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
                "Preparing a fresh current-source packet249 for astral-projection and imprisonment; preserve the AFP holds and all other holds.")
    start.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": STATUS, "archive": archive_info, "delivery": delivery_info,
                      "audit": audit_info, "receipt": receipt_info, "acceptedIds": [],
                      "appliedIds": [], "heldIds": TARGET, "blockers": BLOCKERS,
                      "nextGroup": NEXT, "queue": queue_info, "handoff": info(handoff_path)}, indent=2))


if __name__ == "__main__":
    main()
