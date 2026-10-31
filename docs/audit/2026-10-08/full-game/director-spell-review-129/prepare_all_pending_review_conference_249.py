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
STATUS = "ALL37_PENDING_IDENTITIES_REVIEWED_HELD_DIRECTOR_CONFERENCE_249_811_37_0"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main():
    report_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249.json"
    receipt_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_RECEIPT.json"
    report, receipt = read(report_path), read(receipt_path)
    assert report["status"] == receipt["status"] == "PASS"
    assert report["authority"] == AUTHORITY and report["reviewedUniqueIdentityCount"] == report["pendingCount"] == 37
    assert report["acceptedIds"] == report["appliedIds"] == report["unreviewedCurrentPendingIds"] == []

    now = datetime.now(timezone.utc).isoformat()
    pending_old_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_248.json"
    pending_old = read(pending_old_path)
    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_249.json"
    pending = copy.deepcopy(pending_old)
    pending.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-249", "recordedAtUtc": now, "status": STATUS,
                    "reviewReconciliation": info(report_path), "reviewReconciliationReceipt": info(receipt_path),
                    "allCurrentPendingIdentitiesHaveDirectorDisposition": True,
                    "acceptedIds": [], "appliedIds": [], "heldIds": report["heldIds"],
                    "unreviewedPendingIds": []})
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_old_path = BASE / "CURRENT_SPELL_QUEUE_248.json"
    queue_old = read(queue_old_path)
    spell_rows = {row["id"]: row for row in report["allSpellDispositions"]}
    return_by_group = {row["group"]: row for row in report["returnAudits"]}
    queue = copy.deepcopy(queue_old)
    queue.update({"id": "SPELL-REVIEW-QUEUE-249", "recordedAtUtc": now,
                  "supersedesQueue": "SPELL-REVIEW-QUEUE-248", "parentQueue": info(queue_old_path),
                  "pendingIdentityAudit": pending_info, "status": STATUS, "packetStatus": STATUS,
                  "allPendingGroupsReviewed": True, "reviewedPendingIdentityCount": 37,
                  "unreviewedPendingIds": [], "allPendingReviewReconciliation": info(report_path),
                  "allPendingReviewReconciliationReceipt": info(receipt_path),
                  "nextGroup": None, "nextPendingIds": [],
                  "next": {"group": None, "pendingIds": [], "pendingCount": 0,
                           "status": "ALL_CURRENT_PENDING_GROUPS_HAVE_SEALED_DIRECTOR_DISPOSITIONS",
                           "nextAction": "DIRECTOR_CONFERENCE_ON_REMAINING_HELD_WITNESSES"},
                  "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [],
                  "currentReturnHeldIds": report["returnAudits"][-1]["heldIds"],
                  "allPendingReviewReturnRange": [232, 248], "githubChanges": False})
    for group_row in queue["currentPendingGroups"]:
        target_ids = group_row["pendingIds"]
        return_record = next((r for r in report["returnAudits"] if set(r["heldIds"]) == set(target_ids)), None)
        if return_record is None:
            continue
        blockers = {spell_id: spell_rows[spell_id]["blockerIds"] for spell_id in target_ids}
        group_row.update({"status": f"RETURN{return_record['return']}_AUDITED_HELD_ALL37_REVIEWED",
                          "reviewReturn": return_record["return"], "heldIds": target_ids,
                          "blockers": blockers, "independentAudit": return_record["independentAudit"],
                          "noAcceptanceOrApplication": True})
    assert all(any(set(r["heldIds"]) == set(group["pendingIds"]) for r in report["returnAudits"]) for group in queue["currentPendingGroups"])
    queue_path = BASE / "CURRENT_SPELL_QUEUE_249.json"
    write(queue_path, queue)
    queue_info = info(queue_path)

    handoff_old_path = BASE / "CURRENT_HANDOFF_248.json"
    handoff = copy.deepcopy(read(handoff_old_path))
    handoff.update({"id": "CURRENT-HANDOFF-249", "recordedAtUtc": now, "status": STATUS,
                    "pendingIdentityAudit": pending_info, "queue": queue_info, "currentQueueBinding": queue_info,
                    "allPendingReviewReconciliation": info(report_path),
                    "allPendingReviewReconciliationReceipt": info(receipt_path),
                    "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [],
                    "nextGroup": None, "nextPendingCount": 0, "nextPendingIds": [],
                    "nextStep": "Confer with the GPT director on the consolidated 37 held identities, exact blockers and minimum missing witnesses. Return248's next-group pointer to Projection/Confinement is stale because Return232 already reviewed that group and Return233 reviewed Miracle/Reality. Do not duplicate either review; proceed with evidence/authoring work only after GPT's reconciliation.",
                    "resumePriority": "All 37 current pending spell identities have sealed, independently audited held decisions across Returns232-248. No identity was accepted or applied. Reconcile the stale next-group pointer with GPT and obtain a prioritized blocker/witness plan; authority remains 811/37/0.",
                    "githubChanges": False})
    handoff_path = BASE / "CURRENT_HANDOFF_249.json"
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_249.md"
    snapshot_path.write_text(
        "# Current Ordinary Spell Review Snapshot 249\n\n"
        "The sealed return chain 232-248 has now been independently reconciled: **17 returns cover all 37 current pending identities exactly once; all 37 remain held, with zero accepted and zero applied**. Every return audit passed. Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. No pending identity is awaiting its first director review.\n\n"
        "Return248's next-group pointer is stale: it points to Projection/Confinement, already reviewed and held in Return232. Miracle/Reality was also reviewed and held in Return233. The remaining work is to consolidate the blockers and minimum missing source witnesses for the 37 holds, identify director-resolvable authoring decisions versus external evidence needs, and set a priority. The complete per-spell dispositions are in [the 37-spell reconciliation](ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249.json).\n\n"
        "No acceptance, application, canonical change, GitHub change, runtime execution, implementation approval, human playtest, balance, cosmology, domain closure, completion, or release approval is inferred.\n",
        encoding="utf-8")

    start_path = ROOT / "START_HERE.md"
    lines = start_path.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = ("**Current ordinary spell-review handoff [249](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_249.json):** "
                "Returns232-248 have been independently reconciled: all 37 pending identities have sealed held decisions; none is unreviewed, accepted, or applied. Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
                "Conferring with GPT on the consolidated remaining blockers and missing witnesses; Return248's pointer to Projection/Confinement is stale because Return232 already reviewed that group.")
    start_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    request_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_REQUEST.txt"
    request_path.write_text(
        "GPT director — this is a reconciliation of completed reviews, not a new review or application request. The attached independent reconciliation verifies Returns232–248: 17 sealed return packages, 37 unique identities, exact coverage of the current 37 pending IDs, all 37 held, zero accepted, zero applied, authority unchanged at 811/37/0. All return audits passed.\n\n"
        "Return248 names Projection/Confinement as next, but that pointer is stale: astral-projection and imprisonment were already reviewed and held in Return232. Miracle/Reality was reviewed and held in Return233. No pending identity is awaiting its first review.\n\n"
        "Please reconcile that status and provide a consolidated remaining-work plan from the attached per-spell blocker and minimum-witness records. Distinguish what can be resolved by source-grounded authoring or explicit director decisions from what requires new external source evidence or a complete witness. Prioritize the next actions that could move an identity toward acceptance. Do not reopen prior completed reviews, invent source facts, accept or apply any identity, or modify canonical files. Report whether any review tasks remain after this reconciliation and the exact remaining gates.\n",
        encoding="utf-8")

    print(json.dumps({"status": STATUS, "pending": 37, "reviewed": 37, "held": 37, "accepted": 0, "applied": 0,
                      "queue": queue_info, "handoff": info(handoff_path), "pendingAudit": pending_info,
                      "snapshot": info(snapshot_path), "request": info(request_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
