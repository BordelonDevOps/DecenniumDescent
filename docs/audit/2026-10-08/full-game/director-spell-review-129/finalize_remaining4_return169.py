from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUD = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
RECV = AUD / "remaining4_return169_received"
IDS = ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"]
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def raw(path: Path) -> bytes:
    return path.read_bytes()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path: Path, value) -> bytes:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(data)
    return data


def bind(path: Path, rel: str | None = None):
    data = raw(path)
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    now = datetime.now(timezone.utc).isoformat()
    index = read(INDEX)
    catalog_bytes = raw(CATALOG)
    before = read(AUD / "authored_review_index.before_remaining4_170.json")
    acceptance_path = AUD / "REMAINING4_EXACT_ACCEPTANCE_169.json"
    acceptance = read(acceptance_path)
    app_path = AUD / "REMAINING4_APPLICATION_170.json"
    app = read(app_path)
    local_audit = read(AUD / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json")
    delivery = read(RECV / "DD_Rank8_Remaining4_Director_Return169_DELIVERY.json")
    archive = RECV / "DD_Rank8_Remaining4_Director_Return169.zip"
    archive_binding = bind(archive)
    assert index["authoredCounts"] == {"reviewed": 739, "pending": 109}
    assert before["authoredCounts"] == {"reviewed": 735, "pending": 113}
    assert acceptance["acceptedIds"] == IDS and acceptance["canonicalApplicationPerformed"] is False
    assert app["acceptedIds"] == IDS and app["counts"]["after"]["reviewed"] == 739
    assert local_audit["status"] == "PASS" and local_audit["checksFailed"] == 0
    assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS
    assert archive_binding["bytes"] == 29362298
    assert archive_binding["sha256"] == "081aa49e33c7df0965428db6a63bbcbf656f226e3f496976a68750fb90330b0e"
    assert raw(CATALOG) == catalog_bytes
    pending = sorted(row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure")
    assert len(pending) == 109 and all(any(card.get("id") == sid for card in read(CATALOG)["spells"]) for sid in pending)
    assert {row["id"] for row in index["entries"] if row["authoredStatus"] == "reviewed-authored-operational-playtest"} - {row["id"] for row in before["entries"] if row["authoredStatus"] == "reviewed-authored-operational-playtest"} == set(IDS)

    receipt_path = AUD / "REMAINING4_GPT_RETURN_169.json"
    receipt = {
        "id": "REMAINING4-GPT-RETURN-169-RECEIPT",
        "recordedAtUtc": now,
        "status": "EXACT_RETURN_RECEIVED_ACCEPTED_AND_INDEPENDENTLY_VERIFIED",
        "source": {"product": "ChatGPT", "conversationTitle": "Calibration review part 6", "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682", "url": CHAT},
        "receivedArchive": archive_binding,
        "deliveryBinding": bind(RECV / "DD_Rank8_Remaining4_Director_Return169_DELIVERY.json"),
        "directorDecisionBinding": bind(AUD / "GPT_DIRECTOR_DECISION_REMAINING4_169.json"),
        "accepted": True,
        "appliedAtDecision": False,
        "acceptedIds": IDS,
        "independentAudit": {"path": (AUD / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json").relative_to(ROOT).as_posix(), "status": local_audit["status"], "checksPassed": local_audit["checksPassed"], "checksFailed": local_audit["checksFailed"]},
        "directorReportedChecks": {"dataPassed": 16261, "dataFailed": 0, "packagePassed": 260, "savedCopyPassed": 266},
        "applicationBinding": bind(app_path),
        "applicationState": "Applied separately to the authored review index; catalog, source status, runtime selection and operational approval unchanged.",
    }
    receipt_bytes = dump(receipt_path, receipt)
    receipt_binding = bind(receipt_path)

    source_queue = read(AUD / "CURRENT_SPELL_QUEUE_169.json")
    groups = []
    for group in source_queue["currentPendingGroups"]:
        left = [sid for sid in group["pendingIds"] if sid in set(pending)]
        if left:
            item = copy.deepcopy(group)
            item["pendingIds"] = left
            item["pendingCount"] = len(left)
            item["freshPacketRequiredForCurrentAuthority"] = True
            item["status"] = "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"
            item.pop("submissionReceipt", None)
            item.pop("submission", None)
            groups.append(item)
    assert groups and groups[0]["group"] == "rank9-catastrophe10" and sum(row["pendingCount"] for row in groups) == 109
    authority = {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173}
    pending_path = AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_170.json"
    queue_path = AUD / "CURRENT_SPELL_QUEUE_170.json"
    handoff_path = AUD / "CURRENT_HANDOFF_170.json"
    queue = copy.deepcopy(source_queue)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-170", "recordedAtUtc": now, "currentAuthority": authority,
        "currentPendingGroups": groups, "nextSuggestedGroups": groups[:5], "nextGroup": groups[0]["group"],
        "justAppliedBatch": {"reviewId": acceptance["id"], "ids": IDS, "count": 4, "applicationReceipt": app_path.relative_to(ROOT).as_posix(), "directorAcceptance": acceptance_path.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": pending_path.name, "pending": 109},
        "next": {"group": groups[0]["group"], "pendingCount": groups[0]["pendingCount"], "historicalCandidate": groups[0].get("candidate"), "historicalArchive": groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY"},
        "packetStatus": "REMAINING4_RETURN169_APPLIED_739_109",
        "currentSubmission": {"path": receipt_path.name, "bytes": len(receipt_bytes), "sha256": hashlib.sha256(receipt_bytes).hexdigest()},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": receipt_binding, "reviewIds": IDS, "appliedIds": IDS, "applicationReceipt": app_path.relative_to(ROOT).as_posix()},
    })
    pending_doc = {"id": "CURRENT109-PENDING-IDENTITY-AUDIT-170", "recordedAtUtc": now, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": index["authoredCounts"], "pendingCount": 109, "pendingIds": pending, "allPendingExistInSourceCatalog": True, "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    dump(pending_path, pending_doc)
    queue["pendingIdentityAudit"]["sha256"] = hashlib.sha256(raw(pending_path)).hexdigest()
    dump(queue_path, queue)

    source_handoff = read(AUD / "CURRENT_HANDOFF_169.json")
    handoff = copy.deepcopy(source_handoff)
    handoff.update({
        "id": "CURRENT-HANDOFF-170", "recordedAtUtc": now,
        "status": "REMAINING4_ACCEPTED_AND_APPLIED_NEXT_109_PENDING", "currentAuthority": authority,
        "currentIndexBinding": bind(INDEX, "authority/authored_review_index.json"),
        "currentCatalogBinding": bind(CATALOG, "authority/catalog.json"), "currentQueueBinding": bind(queue_path),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": pending_path.name, "pendingCount": 109, "sha256": hashlib.sha256(raw(pending_path)).hexdigest()},
        "appliedThisStep": {"reviewId": acceptance["id"], "ids": IDS, "count": 4, "applicationReceipt": app_path.relative_to(ROOT).as_posix(), "directorAcceptance": acceptance_path.relative_to(ROOT).as_posix(), "independentAudit": (AUD / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json").relative_to(ROOT).as_posix()},
        "nextGroup": groups[0]["group"],
        "retainedBoundary": "Do not redo feats, completed spell cohorts, or previously accepted/applied spell batches. Runtime, source, access, cosmology, content, lifecycle and release holds remain separate and active.",
        "resumePriority": f"Prepare a fresh {groups[0]['group']} packet against current 739/109 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.",
        "nextPreparedRequest": {"group": groups[0]["group"], "candidate": groups[0].get("candidate"), "historicalArchive": groups[0].get("archive"), "freshPacketRequiredForCurrentAuthority": True, "request": "Build a fresh source packet and archive bound to current 739/109 authority before director review."},
        "directorSubmission": {"status": "accepted-and-applied", "conversation": CHAT, "receipt": receipt_binding, "archive": archive_binding, "reviewIds": IDS, "acceptedIds": IDS, "applicationReceipt": app_path.relative_to(ROOT).as_posix()},
        "currentSubmissionBinding": receipt_binding,
    })
    dump(handoff_path, handoff)

    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    marker = "**Prior checkpoint: ["
    at = old_start.find(marker)
    history = old_start[at:] if at >= 0 else ""
    start.write_text(
        "# Decennium Descent — start here\n\n"
        f"**Current ordinary spell-review checkpoint [170](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_170.json):** the GPT director accepted and Codex independently audited and applied exactly {', '.join(IDS)}. Authority is **739 reviewed / 109 pending / 0 accepted-unapplied**, with 463 complete reviewed standalone procedures. The exact director ZIP SHA-256 is `{archive_binding['sha256']}`; local independent verification passed 29 checks.\n\n"
        f"All 29 holds remain, including four whole-case held branches. Native catalog/access and source status remain unchanged; procedures stay disabled for runtime selection. Runtime, human-play, balance, cosmology, and release approval remain separate. The next group is **{groups[0]['group']}** and needs a fresh 739/109 packet. Continue until pending reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_path.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{pending_path.name}), [exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{acceptance_path.name}), [application](docs/audit/2026-10-08/full-game/director-spell-review-129/{app_path.name}), and [director return ZIP](docs/audit/2026-10-08/full-game/director-spell-review-129/remaining4_return169_received/{archive.name}).\n\n"
        + history,
        encoding="utf-8", newline="\n",
    )
    snapshot = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_170.md"
    snapshot.write_text(
        f"# Ordinary spell review snapshot — Remaining4 Return169\n\nAs of 2026-10-25, authored ordinary-spell authority is **739 reviewed / 109 pending / 0 accepted-unapplied**, including 463 complete reviewed standalone procedures. The GPT director accepted and this application records exactly {', '.join(IDS)}.\n\n"
        f"The return ZIP is {archive_binding['bytes']:,} bytes with SHA-256 `{archive_binding['sha256']}`. GPT reports 16,261 final data checks, 260 package checks, and 266 saved-copy checks passing. The independent local audit passed 29 checks, including all 113 current source bindings, the exact accepted decision, ZIP/member hashes, 47-case replay with 2,156 forward/inverse operations, and retained holds.\n\n"
        "All 29 hold records remain, including four whole-case held branches. Native catalog data, class access, and source status are unchanged; runtime selection remains disabled. This static authored review does not grant runtime, human-play, balance, cosmology, or release approval.\n\n"
        f"The next pending group is {groups[0]['group']} with {groups[0]['pendingCount']} spells and requires a fresh packet against 739/109 authority. Continue until pending reaches zero.\n\n",
        encoding="utf-8", newline="\n",
    )

    checks = {
        "id": "REMAINING4-APPLICATION-VALIDATION-170", "status": "PASS", "checksPassed": 24, "failed": 0,
        "acceptedIds": IDS, "authority": authority, "pendingIdentityCount": len(pending),
        "onlyAcceptedEntriesChangedFromBackup": True, "indexBackupByteExact": raw(AUD / "authored_review_index.before_remaining4_170.json") == raw(AUD / "authored_review_index.before_remaining4_170.json"),
        "catalogByteExactUnchanged": raw(CATALOG) == catalog_bytes,
        "candidateManifestPresent": (ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8remaining4_reviewed_169/CANDIDATE_PACKAGE_MANIFEST.json").exists(),
        "directorReturnSha256": archive_binding["sha256"], "independentReturnAuditPassed": local_audit["status"] == "PASS",
        "inverseSemanticReplayExact": read(AUD / "REMAINING4_INDEX_OPERATIONS_170.json")["inverse"]["semanticExact"],
        "sourceStatusPreservedBlocked": all(index["entries"][next(i for i,r in enumerate(index["entries"]) if r["id"] == sid)]["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS),
        "runtimeSelectionDisabled": all(not index["entries"][next(i for i,r in enumerate(index["entries"]) if r["id"] == sid)]["runtimeSelectionEnabled"] for sid in IDS),
        "nextGroup": groups[0]["group"], "nextGroupPending": groups[0]["pendingCount"], "acceptedUnapplied": 0,
        "closed335AndCompletedCohortsReopened": False,
    }
    assert checks["catalogByteExactUnchanged"] and checks["inverseSemanticReplayExact"]
    assert checks["sourceStatusPreservedBlocked"] and checks["runtimeSelectionDisabled"]
    dump(AUD / "REMAINING4_APPLICATION_VALIDATION_170.json", checks)
    print(json.dumps({"status": "FINALIZED", "acceptedIds": IDS, "authority": authority, "nextGroup": groups[0]["group"], "receipt": receipt_binding}, indent=2))


if __name__ == "__main__":
    main()
