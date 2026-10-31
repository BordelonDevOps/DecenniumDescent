from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = A / "rank9_wardcontrol6_return312_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_WardControl6_Director_Return312_HELD.zip"
RETURN_DELIVERY = RETURN_DIR / "DD_Rank9_WardControl6_Director_Return312_HELD_DELIVERY.json"
PACKET = A / "rank9_wardcontrol6_source_packet_312_prepared/DD_Rank9_WardControl6_CurrentSource_312.zip"
AUDIT_PATH = A / "NULLIFICATION_WAVE_RETURN312_INDEPENDENT_AUDIT.json"
QUEUE_313 = A / "CURRENT_SPELL_QUEUE_313.json"
HANDOFF_313 = A / "CURRENT_HANDOFF_313.json"
PENDING_311 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_311.json"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def binding(path: pathlib.Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": sha(raw), "crc32": crc(raw)}


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    audit = read(AUDIT_PATH)
    delivery = read(RETURN_DELIVERY)
    queue_313 = read(QUEUE_313)
    handoff_313 = read(HANDOFF_313)
    pending_311 = read(PENDING_311)
    assert audit["status"] == "PASS" and audit["failedChecks"] == 0
    assert delivery["authority"] == AUTH
    assert delivery["scopeIds"] == ["nullification-wave"]
    assert delivery["acceptedIds"] == delivery["appliedIds"] == []
    assert delivery["heldIds"] == ["nullification-wave"]
    assert delivery["blockerIds"] == ["WC188-B01"]
    with zipfile.ZipFile(RETURN_ZIP) as ret:
        decision_raw = ret.read("DIRECTOR_DECISION.json")
        decision = json.loads(decision_raw)
        queue_return = json.loads(ret.read("REMAINING_QUEUE.json"))
        pending_ids = queue_return["pendingIds"]
        assert len(pending_ids) == len(set(pending_ids)) == 26
        assert queue_return["closureTasksRemaining"] == 26
        assert queue_return["firstReviewTasksRemaining"] == 0
        assert queue_return["separatelyRetainedHolds"] == [
            "final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave"]
        assert queue_return["nextPendingGroup"]["nextIdentity"] == "reality-anchor"
        assert queue_return["nextPendingGroup"]["blockerIds"] == ["WC188-B02"]
        assert queue_return["nextPendingGroup"]["separatePacket"] is True
        assert pending_ids == pending_311["pendingIds"]
        assert handoff_313["currentBlocker"]["identity"] == "nullification-wave"

    decision_path = A / "NULLIFICATION_WAVE_DIRECTOR_DECISION_312.json"
    decision_path.write_bytes(decision_raw)
    archive_binding = binding(RETURN_ZIP)
    delivery_binding = binding(RETURN_DELIVERY)
    decision_binding = binding(decision_path)
    audit_binding = binding(AUDIT_PATH)
    packet_binding = binding(PACKET)
    source_packet_delivery = A / "rank9_wardcontrol6_source_packet_312_prepared/DD_Rank9_WardControl6_CurrentSource_312_DELIVERY.json"
    packet_delivery_binding = binding(source_packet_delivery)

    hold = decision["decisions"][0]
    receipt = {
        "id": "NULLIFICATION-WAVE-HOLD-RECEIPT-312",
        "recordedAtUtc": now,
        "status": "HELD_PENDING_INTEGRATED_PAID_WAVE_WITNESS_AGAINST_ACCEPTED_FORGE_IMPRINT",
        "scopeIds": ["nullification-wave"], "blockerIds": ["WC188-B01"],
        "authority": AUTH, "acceptedIds": [], "appliedIds": [], "heldIds": ["nullification-wave"],
        "finding": hold["finding"], "minimumMissingWitness": hold["minimumMissingWitness"],
        "returnArchive": archive_binding, "returnDelivery": delivery_binding,
        "directorDecision": decision_binding, "independentAudit": audit_binding,
        "submittedSourcePacket": packet_binding, "submittedSourceDelivery": packet_delivery_binding,
        "nextPendingGroup": queue_return["nextPendingGroup"],
        "continuingPriorityOrder": queue_return["continuingPriorityOrder"],
        "separatelyRetainedHolds": queue_return["separatelyRetainedHolds"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    receipt_path = A / "NULLIFICATION_WAVE_HOLD_RECEIPT_312.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    source_bindings = json.loads(zipfile.ZipFile(PACKET).read("SOURCE_REFRESH_312.json"))
    idx_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    index = read(idx_path)
    catalog = read(catalog_path)
    index_pending = [r["id"] for r in index["entries"] if r.get("authoredStatus") == "pending-authored-procedure"]
    catalog_by_id = {r["id"]: r for r in catalog["spells"]}
    assert set(index_pending) == set(pending_ids) and len(index_pending) == 26
    assert all(sid in catalog_by_id and catalog_by_id[sid].get("operational") is None for sid in pending_ids)
    index_binding = binding(idx_path)
    catalog_binding = binding(catalog_path)
    pending_audit = {
        "id": "CURRENT26-PENDING-IDENTITY-AUDIT-312",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_822_26_AFTER_NULLIFICATION_WAVE_HOLD_312",
        "supersedes": "CURRENT26-PENDING-IDENTITY-AUDIT-311",
        "authority": AUTH, "indexBinding": index_binding, "catalogBinding": catalog_binding,
        "pendingCount": 26, "pendingIds": sorted(pending_ids),
        "allPendingIdsExistInNativeCatalog": True,
        "noPendingTargetWasSilentlyAccepted": True,
        "acceptedIds": [], "appliedIds": [],
        "separatelyHeldIds": queue_return["separatelyRetainedHolds"],
        "separatelyHeldBlockers": {
            "final-word": ["DR217-B01"],
            "elemental-shell": ["DF218-B01", "DF218-B02"],
            "timeless-form": ["DF218-B03"],
            "invulnerable-sphere": ["DF218-B04"],
            "nullification-wave": ["WC188-B01"],
        },
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [],
        "firstReviewTasksRemaining": 0, "closureTasksRemaining": 26,
        "nextGroup": queue_return["nextPendingGroup"]["group"],
        "nextPendingIds": ["reality-anchor", "time-stop"], "nextPendingCount": 2,
        "nextPendingGroup": {
            "group": queue_return["nextPendingGroup"]["group"],
            "pendingIds": ["reality-anchor"], "pendingCount": 1,
            "status": "DIRECTOR_NEXT_AFTER_NULLIFICATION_WAVE_HOLD_RETURN312",
            "freshPacketRequiredForCurrentAuthority": True,
            "blockerByIdentity": {"reality-anchor": ["WC188-B02"]},
            "then": {"identity": "time-stop"},
        },
        "continuingPriorityOrder": queue_return["continuingPriorityOrder"],
        "separatelyRetainedHolds": queue_return["separatelyRetainedHolds"],
        "latestDirectorReturn": {"archive": archive_binding, "delivery": delivery_binding,
                                 "decision": decision_binding, "independentAudit": audit_binding,
                                 "acceptedIds": [], "appliedIds": [],
                                 "heldIds": ["nullification-wave"], "blockerIds": ["WC188-B01"]},
        "priorDirectorHoldReceipt": receipt_path.relative_to(ROOT).as_posix(),
        "sourceQueue": binding(QUEUE_313), "canonicalFilesChanged": False,
    }
    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_312.json"
    pending_path.write_text(json.dumps(pending_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    queue = {
        "id": "SPELL-REVIEW-QUEUE-314", "recordedAtUtc": now,
        "supersedesQueue": binding(QUEUE_313), "currentAuthority": AUTH,
        "currentIndexBinding": index_binding, "currentCatalogBinding": catalog_binding,
        "pendingCount": 26, "acceptedUnapplied": 0, "nextGroup": "rank9-ward-control6",
        "nextPendingIds": ["reality-anchor", "time-stop"], "nextPendingCount": 2,
        "activeReview": {"identity": "reality-anchor", "blockerIds": ["WC188-B02"],
                         "scopeIds": ["reality-anchor"], "jointReview": False,
                         "status": "DIRECTOR_NEXT_AFTER_WAVE_HOLD_PACKET_PREPARATION"},
        "next": pending_audit["nextPendingGroup"],
        "continuingPriorityOrder": queue_return["continuingPriorityOrder"],
        "separatelyRetainedHolds": queue_return["separatelyRetainedHolds"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "allPendingGroupsReviewed": True, "unreviewedPendingIds": [],
        "lastDirectorReturn": pending_audit["latestDirectorReturn"],
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["nullification-wave"],
        "currentReturnBlockers": {"nullification-wave": ["WC188-B01"]},
        "currentReturnDecision": decision_binding, "currentReturnArchive": archive_binding,
        "currentReturnDelivery": delivery_binding, "currentReturnAudit": audit_binding,
        "currentSourcePacket": packet_binding, "currentPreparation": None,
        "currentPacketStatus": "RETURN312_WAVE_HELD; RA separate and next; no canonical change",
        "pendingIdentityAudit": binding(pending_path),
        "directorConnectionStatus": "Return312 sealed HOLD; checking Director for Reality Anchor evidence guidance.",
        "githubChanges": False, "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    queue_path = A / "CURRENT_SPELL_QUEUE_314.json"
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    handoff = {
        "id": "CURRENT-HANDOFF-314", "recordedAtUtc": now,
        "supersedes": binding(HANDOFF_313),
        "status": "RETURN312_NULLIFICATION_WAVE_HELD_NEXT_REALITY_ANCHOR",
        "authority": AUTH, "scopeIds": ["nullification-wave"], "blockerIds": ["WC188-B01"],
        "queue": queue_path.relative_to(ROOT).as_posix(), "queueBinding": binding(queue_path),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "appliedThisStep": [], "acceptedThisStep": [], "heldThisStep": ["nullification-wave"],
        "currentBlocker": {"identity": "reality-anchor", "group": "rank9-ward-control6",
                           "blockerIds": ["WC188-B02"]},
        "nextPendingGroup": queue["next"],
        "nextStep": "Ask Director for the exact Reality Anchor / WC188-B02 evidence and source bindings, then prepare and independently audit a fresh RA-only packet. Keep WC188-B01 held and Wave separate.",
        "previousPreparation": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_SOURCE_PREPARATION_312.json",
                                "status": "SUBMITTED_AND_ADJUDICATED", "scopeIds": ["nullification-wave"]},
        "currentSourcePacket": packet_binding,
        "currentReturn": {"archive": archive_binding, "delivery": delivery_binding,
                          "decision": decision_binding, "independentAudit": audit_binding,
                          "acceptedIds": [], "appliedIds": [], "heldIds": ["nullification-wave"],
                          "blockerIds": ["WC188-B01"]},
        "continuingPriorityOrder": queue_return["continuingPriorityOrder"],
        "separatelyRetainedHolds": queue_return["separatelyRetainedHolds"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Director’s Return312 sealed hold recorded; RA preparation guidance requested.",
        "githubChanges": False, "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    handoff_path = A / "CURRENT_HANDOFF_314.json"
    handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_314.md"
    snapshot_path.write_text(
        "# Current spell review snapshot 314\n\n"
        "Authority remains **822 reviewed/applied / 26 pending / 0 accepted-unapplied**, with **546 complete standalone procedures / 173 scoped interfaces**. Return312 independently audited PASS (14 checks, 0 failures) and held **Nullification Wave / WC188-B01**. No IDs were accepted or applied.\n\n"
        "Director found an accepted Eternal Forge imprint with explicit continuing-component and terminal/remainder rules, but the package contains no integrated paid Nullification Wave encounter against that exact imprint. The Glove of Null Ink still lacks an underlying-property removal contract. The two `-Infinity` inputs are confined to preserved zero-event held-case summary rows; Return312 documented their derived final timestamp as -1 without rewriting evidence.\n\n"
        "**Reality Anchor / WC188-B02 is next in a separate packet.** Then Time Stop → Fate Rewrite → Collapse Timeline → Eternal Prophecy. The queue remains at **26 closure tasks and zero first-review tasks**. Five identities are separately held: Final Word, Elemental Shell, Timeless Form, Invulnerable Sphere, and Nullification Wave. No canonical spell files changed and no application occurred.\n",
        encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": binding(receipt_path),
                      "pendingAudit": binding(pending_path), "queue": binding(queue_path),
                      "handoff": binding(handoff_path), "snapshot": binding(snapshot_path)}, indent=2))


if __name__ == "__main__":
    main()
