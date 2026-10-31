from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN = A / "rank9_defenseform8_return310_received"
RETURN_ZIP = RETURN / "DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
RETURN_DELIVERY = RETURN / "DD_Rank9_DefenseForm8_Director_Return310_HELD_DELIVERY.json"
AUDIT_PATH = A / "INVULNERABLE_SPHERE_RETURN310_INDEPENDENT_AUDIT.json"
PACKET = A / "rank9_defenseform8_current_source_310_prepared/DD_Rank9_DefenseForm8_CurrentSource_310.zip"
QUEUE_310 = A / "CURRENT_SPELL_QUEUE_310.json"
HANDOFF_310 = A / "CURRENT_HANDOFF_310.json"
PENDING_308 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_308.json"
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
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    audit = read(AUDIT_PATH)
    delivery = read(RETURN_DELIVERY)
    previous_queue = read(QUEUE_310)
    previous_handoff = read(HANDOFF_310)
    previous_pending = read(PENDING_308)
    with zipfile.ZipFile(RETURN_ZIP) as ret, zipfile.ZipFile(PACKET) as packet:
        decision_raw = ret.read("DIRECTOR_DECISION.json")
        decision = json.loads(decision_raw)
        next_data = json.loads(ret.read("NEXT_PENDING_GROUP.json"))
        source_rows = json.loads(ret.read("SOURCE_BINDINGS.json"))["sourceRows"]
        source_by_path = {r["path"]: r for r in source_rows}
    assert audit["status"] == "PASS" and audit["failedChecks"] == 0
    assert delivery["authority"] == AUTH and decision["authorityAfter"] == AUTH
    assert delivery["acceptedIds"] == delivery["appliedIds"] == []
    assert delivery["heldIds"] == ["invulnerable-sphere"] and delivery["blockerIds"] == ["DF218-B04"]
    assert next_data["closureTasksRemaining"] == 26 and next_data["firstReviewTasksRemaining"] == 0
    pending_ids = next_data["allPendingIds"]
    assert len(pending_ids) == 26 and len(set(pending_ids)) == 26
    assert set(next_data["remainingPriorityOrder"]) | set(next_data["separatelyHeld"]) == set(pending_ids)
    assert set(next_data["remainingPriorityOrder"]).isdisjoint(next_data["separatelyHeld"])
    assert next_data["nextPendingGroup"]["nextIdentity"] == "nullification-wave"

    decision_path = A / "INVULNERABLE_SPHERE_DIRECTOR_DECISION_310.json"
    decision_path.write_bytes(decision_raw)
    decision_binding = binding(decision_path)
    audit_binding = binding(AUDIT_PATH)
    archive_binding = binding(RETURN_ZIP)
    delivery_binding = binding(RETURN_DELIVERY)
    packet_binding = binding(PACKET)

    hold_receipt = {
        "id": "INVULNERABLE-SPHERE-HOLD-RECEIPT-310",
        "recordedAtUtc": now,
        "status": "HELD_PENDING_SOURCE_QUALIFIED_PLANAR_CROSSING_WITNESS",
        "scopeIds": ["invulnerable-sphere"],
        "blockerIds": ["DF218-B04"],
        "authority": AUTH,
        "acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"],
        "minimumMissingWitness": decision["decisions"][0]["minimumMissingWitness"],
        "finding": decision["decisions"][0]["finding"],
        "returnArchive": archive_binding,
        "returnDelivery": delivery_binding,
        "directorDecision": decision_binding,
        "independentAudit": audit_binding,
        "submittedSourcePacket": packet_binding,
        "priorSeparateHolds": decision["separatePriorHolds"],
        "nextPendingGroup": next_data["nextPendingGroup"],
        "remainingPriorityOrder": next_data["remainingPriorityOrder"],
        "separatelyHeld": next_data["separatelyHeld"],
        "closureTasksRemaining": 26,
        "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    hold_path = A / "INVULNERABLE_SPHERE_HOLD_RECEIPT_310.json"
    hold_path.write_text(json.dumps(hold_receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_row = source_by_path["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]
    catalog_row = source_by_path["DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"]
    with zipfile.ZipFile(PACKET) as packet:
        idx = json.loads(packet.read("sources_current/" + index_row["path"]))
        catalog = json.loads(packet.read("sources_current/" + catalog_row["path"]))
    index_ids = [r["id"] for r in idx["entries"] if r.get("authoredStatus") == "pending-authored-procedure"]
    assert set(index_ids) == set(pending_ids) and len(index_ids) == 26
    catalog_by_id = {r["id"]: r for r in catalog["spells"]}
    assert all(catalog_by_id[sid].get("operational") is None for sid in pending_ids)
    index_binding = {"path": index_row["path"], "bytes": index_row["bytes"], "sha256": index_row["sha256"], "crc32": index_row["crc32"]}
    catalog_binding = {"path": catalog_row["path"], "bytes": catalog_row["bytes"], "sha256": catalog_row["sha256"], "crc32": catalog_row["crc32"]}
    current = {"reviewedApplied": AUTH["reviewedApplied"], "pending": len(index_ids),
               "acceptedUnapplied": AUTH["acceptedUnapplied"],
               "completeStandaloneProcedures": AUTH["completeStandaloneProcedures"],
               "scopedInterfaces": AUTH["scopedInterfaces"]}
    assert current == AUTH

    pending_audit = {
        "id": "CURRENT26-PENDING-IDENTITY-AUDIT-310",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_822_26_AFTER_INVULNERABLE_SPHERE_HOLD_310",
        "supersedes": "CURRENT26-PENDING-IDENTITY-AUDIT-308",
        "authority": AUTH,
        "indexBinding": index_binding,
        "catalogBinding": catalog_binding,
        "pendingCount": 26,
        "pendingIds": sorted(pending_ids),
        "allPendingIdsExistInNativeCatalog": all(sid in catalog_by_id for sid in pending_ids),
        "noPendingTargetWasSilentlyAccepted": True,
        "acceptedIds": [], "appliedIds": [],
        "separatelyHeldIds": next_data["separatelyHeld"],
        "separatelyHeldBlockers": {"final-word": ["DR217-B01"], "elemental-shell": ["DF218-B01", "DF218-B02"],
                                    "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]},
        "allCurrentPendingIdentitiesReviewed": True,
        "unreviewedPendingIds": [],
        "firstReviewTasksRemaining": 0,
        "closureTasksRemaining": 26,
        "nextGroup": next_data["nextPendingGroup"]["group"],
        "nextPendingIds": [next_data["nextPendingGroup"]["nextIdentity"],
                           next_data["nextPendingGroup"]["thenIdentity"]],
        "nextPendingCount": 2,
        "nextPendingGroup": {"group": next_data["nextPendingGroup"]["group"],
                             "pendingIds": [next_data["nextPendingGroup"]["nextIdentity"]],
                             "pendingCount": 1,
                             "status": "DIRECTOR_NEXT_AFTER_SPHERE_HOLD_RETURN310",
                             "freshPacketRequiredForCurrentAuthority": True,
                             "blockerByIdentity": {next_data["nextPendingGroup"]["nextIdentity"]:
                                                    next_data["nextPendingGroup"]["blockerIds"]},
                             "then": {"identity": next_data["nextPendingGroup"]["thenIdentity"],
                                      "blockerIds": next_data["nextPendingGroup"]["thenBlockerIds"]}},
        "remainingPriorityOrder": next_data["remainingPriorityOrder"],
        "separatelyHeld": next_data["separatelyHeld"],
        "latestDirectorReturn": {"archive": archive_binding, "delivery": delivery_binding,
                                 "decision": decision_binding, "independentAudit": audit_binding,
                                 "acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"],
                                 "blockerIds": ["DF218-B04"]},
        "sourceQueue": binding(QUEUE_310),
        "canonicalFilesChanged": False,
    }
    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_310.json"
    pending_path.write_text(json.dumps(pending_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    queue = {
        "id": "SPELL-REVIEW-QUEUE-311",
        "recordedAtUtc": now,
        "supersedesQueue": binding(QUEUE_310),
        "currentAuthority": AUTH,
        "currentIndexBinding": index_binding,
        "currentCatalogBinding": catalog_binding,
        "pendingCount": 26,
        "acceptedUnapplied": 0,
        "nextGroup": "rank9-ward-control6",
        "nextPendingIds": ["nullification-wave", "reality-anchor"],
        "nextPendingCount": 2,
        "next": pending_audit["nextPendingGroup"],
        "remainingPriorityOrder": next_data["remainingPriorityOrder"],
        "separatelyHeld": next_data["separatelyHeld"],
        "closureTasksRemaining": 26,
        "firstReviewTasksRemaining": 0,
        "allPendingGroupsReviewed": True,
        "unreviewedPendingIds": [],
        "lastDirectorReturn": pending_audit["latestDirectorReturn"],
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["invulnerable-sphere"],
        "currentReturnBlockers": {"invulnerable-sphere": ["DF218-B04"]},
        "currentReturnDecision": decision_binding,
        "currentReturnArchive": archive_binding,
        "currentReturnDelivery": delivery_binding,
        "currentReturnAudit": audit_binding,
        "currentSourcePacket": packet_binding,
        "currentPreparation": None,
        "currentPacketStatus": "RETURN310_HELD; no new evidence or canonical change",
        "previousPreparation": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_SOURCE_PREPARATION_310.json",
                               "status": "SUBMITTED_AND_ADJUDICATED", "scopeIds": ["invulnerable-sphere"]},
        "pendingIdentityAudit": {"path": pending_path.relative_to(ROOT).as_posix(),
                                 "bytes": pending_path.stat().st_size, "sha256": sha(pending_path.read_bytes()),
                                 "crc32": crc(pending_path.read_bytes())},
        "directorNextInstructionRequired": "Ask Director for exact Nullification Wave / WC188-B01 evidence and packet scope before preparing the next packet.",
        "githubChanges": False,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    queue_path = A / "CURRENT_SPELL_QUEUE_311.json"
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    handoff = {
        "id": "CURRENT-HANDOFF-311",
        "recordedAtUtc": now,
        "supersedes": binding(HANDOFF_310),
        "status": "RETURN310_SPHERE_HELD_NEXT_NULLIFICATION_WAVE",
        "authority": AUTH,
        "indexBinding": index_binding,
        "queueBinding": binding(queue_path),
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "appliedThisStep": [], "acceptedThisStep": [],
        "heldThisStep": ["invulnerable-sphere"],
        "currentBlocker": {"identity": "nullification-wave", "group": "rank9-ward-control6",
                           "blockerIds": ["WC188-B01"]},
        "nextPendingGroup": queue["next"],
        "nextStep": "Ask GPT for Nullification Wave / WC188-B01 exact evidence, source bindings, and whether Reality Anchor should be in a joint packet; then prepare, independently audit, and submit the scoped packet.",
        "currentPreparation": None,
        "previousPreparation": queue["previousPreparation"],
        "currentSourcePacket": packet_binding,
        "currentReturn": {"archive": archive_binding, "delivery": delivery_binding,
                          "decision": decision_binding, "independentAudit": audit_binding,
                          "acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"],
                          "blockerIds": ["DF218-B04"]},
        "remainingPriorityOrder": next_data["remainingPriorityOrder"],
        "separatelyHeld": next_data["separatelyHeld"],
        "closureTasksRemaining": 26,
        "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Return310 sealed HOLD; follow-up for next scope is pending.",
        "githubChanges": False,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "notes": [
            "The prior handoff contained stale nextPendingGroup/currentPreparation fields inherited from Timeless Form Packet308. This successor replaces those current pointers with Return310's explicit Nullification Wave order.",
            "Return310 states the Sphere-specific blocker remains open because the lawful actor, authorized other-plane destination, and paid Sphere-caused denial witness are not bound.",
        ],
    }
    handoff_path = A / "CURRENT_HANDOFF_311.json"
    handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    checks = [
        {"check": "Return310 independent audit passed", "passed": audit["status"] == "PASS" and audit["failedChecks"] == 0},
        {"check": "Authority remains 822/26/0 and 546/173", "passed": current == AUTH},
        {"check": "26 pending IDs match Packet310 authored index", "passed": set(index_ids) == set(pending_ids)},
        {"check": "All pending catalog operational entries remain null", "passed": all(catalog_by_id[sid].get("operational") is None for sid in pending_ids)},
        {"check": "Return310 is only a Sphere hold and no accepted/apply", "passed": hold_receipt["heldIds"] == ["invulnerable-sphere"] and hold_receipt["acceptedIds"] == hold_receipt["appliedIds"] == []},
        {"check": "Next order points to Nullification Wave then Reality Anchor", "passed": queue["next"]["pendingIds"] == ["nullification-wave"] and queue["next"]["then"]["identity"] == "reality-anchor"},
        {"check": "No stale Timeless Form preparation remains in current handoff", "passed": handoff["currentPreparation"] is None and handoff["currentBlocker"]["identity"] == "nullification-wave"},
        {"check": "All 26 closure tasks remain and first review is complete", "passed": queue["closureTasksRemaining"] == 26 and queue["firstReviewTasksRemaining"] == 0},
    ]
    report = {"id": "INVULNERABLE-SPHERE-HOLD-TRANSITION-VALIDATION-311",
              "recordedAtUtc": now,
              "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
              "checkCount": len(checks), "failedChecks": sum(not c["passed"] for c in checks),
              "checks": checks,
              "outputs": {p.name: binding(p) for p in [decision_path, hold_path, pending_path, queue_path, handoff_path]},
              "priorInputs": {"queue310": binding(QUEUE_310), "handoff310": binding(HANDOFF_310),
                              "pendingAudit308": binding(PENDING_308)},
              "authority": AUTH,
              "next": queue["next"],
              "closureTasksRemaining": 26,
              "firstReviewTasksRemaining": 0}
    validation_path = A / "INVULNERABLE_SPHERE_HOLD_VALIDATION_311.json"
    validation_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if any(not c["passed"] for c in checks):
        raise SystemExit("Hold transition validation failed")

    snapshot = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_311.md"
    snapshot.write_text(
        "# Current spell review snapshot 311\n\n"
        "Authority remains **822 reviewed/applied / 26 pending / 0 accepted-unapplied**, with **546 complete standalone procedures / 173 scoped interfaces**. Return310 is independently verified PASS and holds only Invulnerable Sphere / DF218-B04. No acceptance, application, blocker revision, or canonical mutation occurred.\n\n"
        "The narrow missing witness is a source-qualified legal planar route with an acquired eligible actor, authorized specific other-plane endpoint, complete transported body/cargo/custody history, and an otherwise-valid paid crossing denied by the intact Sphere with exact terminal settlement.\n\n"
        "Next: **Nullification Wave / WC188-B01**, then **Reality Anchor / WC188-B02**. The Director must give the precise evidence and packet scope before preparation. The prior handoff's stale Timeless Form next/preparation pointers are superseded in `CURRENT_HANDOFF_311.json`.\n\n"
        "There are **26 closure tasks remaining and zero first-review tasks**. Separate holds: Final Word / DR217-B01; Elemental Shell / DF218-B01 and DF218-B02; Timeless Form / DF218-B03; Invulnerable Sphere / DF218-B04.\n",
        encoding="utf-8")
    print(json.dumps({"status": report["status"], "outputs": report["outputs"],
                      "next": report["next"], "closureTasksRemaining": 26}, indent=2))


if __name__ == "__main__":
    main()
