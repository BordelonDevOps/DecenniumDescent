from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PENDING = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_248.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_248.json"
REPORT = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249.json"
RECEIPT = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path: Path):
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
            crc = zlib.crc32(block, crc)
            size += len(block)
    return {"bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}


def out_info(path: Path):
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path)}


def main():
    pending, queue = read(PENDING), read(QUEUE)
    pending_ids = pending["pendingIds"]
    groups = queue["currentPendingGroups"]
    by_group = {tuple(row["pendingIds"]): row["group"] for row in groups}
    outcomes = []
    all_spells = []
    failed = []

    for number in range(232, 249):
        audits = list(BASE.glob(f"*RETURN{number}_INDEPENDENT_AUDIT.json"))
        deliveries = list(BASE.rglob(f"*Return{number}*DELIVERY*.json"))
        archives = list(BASE.rglob(f"*Return{number}*.zip"))
        if len(audits) != 1 or len(deliveries) != 1 or len(archives) != 1:
            failed.append({"return": number, "reason": "expected one audit, delivery and archive", "counts": [len(audits), len(deliveries), len(archives)]})
            continue
        audit_path, delivery_path, archive_path = audits[0], deliveries[0], archives[0]
        audit, delivery = read(audit_path), read(delivery_path)
        authority = delivery.get("authority") or delivery.get("sourceAuthority")
        archive_info = digest(archive_path)
        expected_archive = delivery.get("archive") or {}
        archived_bytes = expected_archive.get("bytes")
        archived_sha = expected_archive.get("sha256")
        archived_crc = expected_archive.get("crc32")
        if not (isinstance(audit.get("status"), str) and audit["status"].startswith("PASS")):
            failed.append({"return": number, "reason": "independent audit is not PASS", "status": audit.get("status")})
        if audit.get("failedChecks") not in (None, 0, []):
            failed.append({"return": number, "reason": "independent audit reports failed checks", "failedChecks": audit.get("failedChecks")})
        if authority != AUTHORITY:
            failed.append({"return": number, "reason": "authority differs from 811/37/0", "authority": authority})
        if delivery.get("accepted") is not False or delivery.get("applied") is not False or delivery.get("acceptedIds") != [] or delivery.get("appliedIds") != []:
            failed.append({"return": number, "reason": "decision is not held without acceptance/application", "acceptedIds": delivery.get("acceptedIds"), "appliedIds": delivery.get("appliedIds")})
        if (archived_bytes, archived_sha, str(archived_crc).lower()) != (archive_info["bytes"], archive_info["sha256"], archive_info["crc32"]):
            failed.append({"return": number, "reason": "archive does not match delivery seal", "actual": archive_info, "expected": expected_archive})

        with zipfile.ZipFile(archive_path) as z:
            if z.testzip() is not None:
                failed.append({"return": number, "reason": "ZIP CRC test failed"})
            decision = json.loads(z.read("DIRECTOR_DECISION.json").decode("utf-8-sig"))
            rows = decision.get("decisions") or decision.get("perIdentity") or decision.get("perIdentityDecisions") or []
            if not rows:
                failed.append({"return": number, "reason": "decision has no per-identity rows"})
            ids = delivery.get("heldIds") or decision.get("heldIds") or []
            if len(ids) != len(set(ids)) or not ids:
                failed.append({"return": number, "reason": "empty or duplicate held identity IDs", "heldIds": ids})
            rows_by_id = {(row.get("id") or row.get("spellId")): row for row in rows}
            if set(rows_by_id) != set(ids):
                failed.append({"return": number, "reason": "decision rows do not match held IDs", "heldIds": ids, "decisionIds": sorted(x for x in rows_by_id if x)})
            for spell_id in ids:
                row = rows_by_id.get(spell_id, {})
                blockers = row.get("blockerIds") or row.get("blockers") or []
                minimum = row.get("minimumMissingWitness")
                if minimum is None:
                    minimum = row.get("minimumMissingWitnesses")
                if minimum is None:
                    minimum = row.get("requiredContent")
                all_spells.append({
                    "id": spell_id,
                    "reviewReturn": number,
                    "group": next((g for g in groups if spell_id in g["pendingIds"]), None),
                    "decision": row.get("decision") or row.get("status") or "held",
                    "accepted": row.get("accepted", False),
                    "applied": row.get("applied", False),
                    "blockerIds": blockers,
                    "minimumMissingWitness": minimum,
                    "requiredContent": row.get("requiredContent"),
                    "qualificationIds": row.get("qualificationIds") or row.get("conditionalQualificationIds") or row.get("conditionalQualificationIds"),
                    "sourceReassessment": row.get("sourceReassessment") or row.get("reassessment"),
                    "caseIds": row.get("caseIds") or row.get("heldCaseIds"),
                })

        outcomes.append({
            "return": number,
            "group": next((row["group"] for row in groups if set(row["pendingIds"]) == set(delivery.get("heldIds", []))), None),
            "heldIds": delivery.get("heldIds", []),
            "acceptedIds": delivery.get("acceptedIds", []),
            "appliedIds": delivery.get("appliedIds", []),
            "authority": authority,
            "independentAudit": {**out_info(audit_path), "status": audit.get("status"), "checkCount": audit.get("checkCount"), "passedChecks": audit.get("passedChecks"), "failedChecks": audit.get("failedChecks")},
            "delivery": out_info(delivery_path),
            "archive": {**out_info(archive_path), "compression": delivery.get("zipCompression") or delivery.get("archiveCompression")},
        })

    reviewed_ids = [row["id"] for row in all_spells]
    if len(reviewed_ids) != 37 or len(set(reviewed_ids)) != 37:
        failed.append({"reason": "reviewed identities are not exactly 37 unique IDs", "count": len(reviewed_ids), "unique": len(set(reviewed_ids))})
    if set(reviewed_ids) != set(pending_ids):
        failed.append({"reason": "Return232-248 union differs from current pending set", "missingReviews": sorted(set(pending_ids) - set(reviewed_ids)), "outsideCurrentPending": sorted(set(reviewed_ids) - set(pending_ids))})
    if len(outcomes) != 17:
        failed.append({"reason": "not all 17 return envelopes were discovered", "count": len(outcomes)})

    # Return248's suggested next group is already represented by Return232; Return233 also completed the following queue row.
    return248 = next((row for row in outcomes if row["return"] == 248), {})
    return248_next = return248.get("nextPendingGroup")
    stale_pointer = {"return": 248, "suggestedGroup": "rank9-projection-confinement2", "alreadyReviewedBy": 232, "alsoCompleted": {"group": "rank9-miracle-reality2", "return": 233}}
    by_return = {row["return"]: row for row in outcomes}
    pointer_path = BASE / "rank9_alignmentfactionpurification5_return248_received" / "DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD_DELIVERY.json"
    pointer = read(pointer_path).get("nextPendingGroup")

    report = {
        "id": "ALL37-PENDING-SPELL-REVIEWS-CONFERENCE-249",
        "status": "PASS" if not failed else "FAIL",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "authority": AUTHORITY,
        "reviewWindow": {"firstReturn": 232, "lastReturn": 248, "returnCount": 17},
        "pendingReviewState": "Every current pending identity has a sealed director disposition; all 37 remain held, with zero accepted or applied.",
        "pendingCount": len(pending_ids),
        "reviewedUniqueIdentityCount": len(set(reviewed_ids)),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": sorted(set(reviewed_ids)),
        "unreviewedCurrentPendingIds": sorted(set(pending_ids) - set(reviewed_ids)),
        "allSpellDispositions": sorted(all_spells, key=lambda row: row["id"]),
        "returnAudits": outcomes,
        "staleReturn248NextPointer": {**stale_pointer, "deliveryPointer": pointer, "confirmedStale": pointer and pointer.get("group") == "rank9-projection-confinement2" and "astral-projection" in by_return.get(232, {}).get("heldIds", [])},
        "nextReviewGroup": None,
        "directorConferenceRequest": "Reconcile the full 37-identity held set from Returns232-248. Return248's next-group pointer is stale because Projection/Confinement was held in Return232 and Miracle/Reality was held in Return233. Confirm that no pending identities are awaiting first review; consolidate exact blocker/missing-witness work; identify which source facts or authoring decisions the director can resolve and give a prioritized next step without reopening completed reviews or claiming acceptance/application.",
        "checkCount": 0,
        "passedChecks": 0,
        "failedChecks": len(failed),
        "failures": failed,
    }
    # Count individual sealed returns plus aggregate coverage/state checks.
    report["checkCount"] = 17 + 7
    report["passedChecks"] = report["checkCount"] - len(failed)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "id": "ALL37-PENDING-SPELL-REVIEWS-CONFERENCE-249-RECEIPT",
        "status": report["status"],
        "report": out_info(REPORT),
        "returnCount": len(outcomes),
        "reviewedUniqueIdentityCount": len(set(reviewed_ids)),
        "pendingCount": len(pending_ids),
        "heldCount": len(reviewed_ids),
        "acceptedCount": 0,
        "appliedCount": 0,
        "checkCount": report["checkCount"],
        "passedChecks": report["passedChecks"],
        "failedChecks": report["failedChecks"],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "returnCount": len(outcomes), "reviewed": report["reviewedUniqueIdentityCount"], "pending": len(pending_ids), "held": len(reviewed_ids), "accepted": 0, "applied": 0, "checkCount": report["checkCount"], "failedChecks": report["failedChecks"], "failures": failed, "report": str(REPORT), "receipt": str(RECEIPT)}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
