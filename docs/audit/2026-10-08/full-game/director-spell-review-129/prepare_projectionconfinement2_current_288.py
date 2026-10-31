from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
GROUP = "rank9-projection-confinement2"
TARGETS = ["astral-projection", "imprisonment"]
BLOCKERS = ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
HIST_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_projection_confinement_2_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Projection_Confinement_2_Source_Conference_01.zip"
HIST_NOTES = AUDIT / "RANK9PROJECTIONCONFINEMENT2_NEXT_CONFERENCE_NOTES_129.json"
HIST_PACKET_RECORD = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_129.json"
HIST_PREP = FULL / "RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_PREPARATION.json"
HIST_CHECK = FULL / "RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_CHECK.json"
HIST_REQUEST = FULL / "RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_REQUEST.txt"
HIST_MANIFEST = FULL / "rank9-projection-confinement2-source-conference-01/MANIFEST.json"
HIST_README = FULL / "rank9-projection-confinement2-source-conference-01/README.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

RETURN_INFO = {
    284: ("rank9_planargates5_return284_received", "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip", "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json", "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json", "RANK9_PLANARGATES5_RETURN284_RECEIPT.json", ["banishment-gate", "conjure-demiplane-fortress"], ["PG200-B03", "PG200-B04", "PG200-B06"]),
    285: ("rank9_summonhosts5_return285_received", "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip", "DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json", "RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json", "RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json", ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"], ["SH202-B01", "SH202-B02", "SH202-B03"]),
    286: ("rank9_impactexile4_return286_received", "DD_Rank9_ImpactExile4_Director_Return286_HELD.zip", "DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN286_RECEIPT.json", ["reverse-gravity-field"], ["IE204-B02"]),
    287: ("rank9_alignmentfactionpurification5_return287_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT.json", ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]),
}


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def info(path: Path, raw: bytes | None = None) -> dict:
    b = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def return_artifacts(number: int) -> dict:
    folder, archive_name, delivery_name, audit_name, receipt_name, held, blockers = RETURN_INFO[number]
    received = AUDIT / folder
    archive = received / archive_name
    delivery = received / delivery_name
    audit = AUDIT / audit_name
    receipt = AUDIT / receipt_name
    audit_doc, delivery_doc = read(audit), read(delivery)
    assert audit_doc["status"] == "PASS" and (audit_doc.get("failedChecks", 0) == 0) and all(x.get("passed") is True for x in audit_doc.get("checks", []))
    assert (delivery_doc.get("acceptedIds", []) == [] and delivery_doc.get("appliedIds", []) == []) if "acceptedIds" in delivery_doc else (delivery_doc["accepted"] is False and delivery_doc["applied"] is False)
    assert delivery_doc["heldIds"] == held
    return {"archivePath": archive, "deliveryPath": delivery, "auditPath": audit, "receiptPath": receipt,
            "archive": info(archive), "delivery": info(delivery), "audit": info(audit), "receipt": info(receipt),
            "heldIds": held, "blockerIds": blockers, "decisionId": delivery_doc.get("id")}


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    now = datetime.now(timezone.utc).isoformat()

    index_path, catalog_path, access_path = ROOT / INDEX, ROOT / CATALOG, ROOT / ACCESS
    index, catalog = read(index_path), read(catalog_path)
    queue287_path = AUDIT / "CURRENT_SPELL_QUEUE_287.json"
    handoff287_path = AUDIT / "CURRENT_HANDOFF_287.json"
    pending287_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_287.json"
    q0, h0, p0 = read(queue287_path), read(handoff287_path), read(pending287_path)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    pending = sorted(row["id"] for row in index["entries"] if row.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending) == 32 and set(TARGETS) <= set(pending)
    group_row = next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP)
    assert group_row["pendingIds"] == TARGETS and group_row["pendingCount"] == 2
    for spell_id in TARGETS:
        assert entries[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert entries[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert spells[spell_id]["id"] == spell_id

    old_candidate = read(ROOT / HIST_CANDIDATE)
    old_notes = read(HIST_NOTES)
    old_packet = read(HIST_PACKET_RECORD)
    old_prep = read(HIST_PREP)
    assert old_prep["status"] == "PREPARED_UNSENT"
    assert old_packet["status"] == "PREPARED_NOT_SENT"
    assert [row["spellId"] for row in old_candidate["records"]] == TARGETS
    assert len(old_candidate["questions"]) == 24 and len(old_candidate["futureCaseRequirements"]) == 8
    assert len(old_notes["completeOriginalQuestionsUnchanged"]) == 24 and len(old_notes["focusedAdditionalQuestions"]) == 2
    assert len(old_notes["allQuestions"]) == 26 and len(old_notes["requiredNewCases"]) == 4
    assert len(old_notes["originalFutureCaseRequirementsUnchanged"]) == 8

    # Bind exact former decisions and holds before preparing the next request.
    returns = {number: return_artifacts(number) for number in (284, 285, 286, 287)}
    return287 = returns[287]
    assert return287["heldIds"] == ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]
    r287_delivery = read(return287["deliveryPath"])
    assert r287_delivery["closedEvidenceFindings"] == ["AFP211-E01"]

    # Re-read the 135 historical source bindings from the current working tree;
    # retain the old archive and record every changed byte binding explicitly.
    source_archive_raw = HIST_ARCHIVE.read_bytes()
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        refreshed, changed, source_files = [], [], {}
        for old in old_candidate["sourceBindings"]:
            path = old["path"]
            historical_raw = historical_zip.read("sources/" + path)
            assert (len(historical_raw), sha(historical_raw)) == (old["bytes"], old["sha256"])
            current_raw = (ROOT / path).read_bytes()
            row = {"path": path, "bytes": len(current_raw), "sha256": sha(current_raw), "gitBlobSHA1": git_blob_sha(current_raw)}
            refreshed.append(row)
            source_files["sources_current/" + path] = current_raw
            if (row["bytes"], row["sha256"]) != (old["bytes"], old["sha256"]):
                changed.append({"path": path, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"], "currentBytes": row["bytes"], "currentSha256": row["sha256"]})
    assert len(refreshed) == len(source_files) == 135 and len({row["path"] for row in refreshed}) == 135

    # Record Return287 as a completed held batch and publish the next queue snapshot.
    submission_path = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_SUBMISSION.json"
    submission287 = read(submission_path)
    submission287.update({
        "status": "RETURN287_AUDITED_HELD_816_32_0",
        "directorReturn": {"archive": return287["archive"], "deliveryManifest": return287["delivery"], "decisionId": return287["decisionId"], "heldIds": return287["heldIds"], "acceptedIds": [], "appliedIds": []},
        "independentReturnAudit": return287["audit"],
        "returnReceipt": return287["receipt"],
        "canonicalChanges": False,
        "applicationChanges": False,
    })
    submission_path.write_bytes(enc(submission287))
    submission_info = info(submission_path)

    return_hold_entries = [
        {"heldIds": returns[n]["heldIds"], "blockerIds": returns[n]["blockerIds"], "archive": returns[n]["archive"], "audit": returns[n]["audit"], "receipt": returns[n]["receipt"]}
        for n in (284, 285, 286, 287)
    ]
    pending288 = copy.deepcopy(p0)
    pending288.update({
        "id": "CURRENT32-PENDING-IDENTITY-AUDIT-288",
        "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN287",
        "lastDirectorReturn": {"archive": return287["archive"], "deliveryManifest": return287["delivery"], "independentAudit": return287["audit"], "receipt": return287["receipt"], "acceptedIds": [], "appliedIds": [], "heldIds": return287["heldIds"], "blockerIds": return287["blockerIds"]},
        "preservedRecentHolds": return_hold_entries,
        "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "historicalPhase": "PREPARED_UNSENT_NOT_DIRECTOR_REVIEWED", "freshPacketRequiredForCurrentAuthority": True},
    })
    pending288_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_288.json"
    pending288_path.write_bytes(enc(pending288))

    queue288 = copy.deepcopy(q0)
    queue288.update({
        "id": "SPELL-REVIEW-QUEUE-288",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-287",
        "pendingIdentityAudit": info(pending288_path),
        "currentReturnAudit": return287["audit"],
        "currentReturnDelivery": return287["delivery"],
        "currentReturnArchive": return287["archive"],
        "currentReturnDecision": return287["decisionId"],
        "currentReturnReceipt": return287["receipt"],
        "currentReturnBinding": return287["archive"],
        "currentReturnSourceArchive": q0.get("currentPacket"),
        "currentReturnSourceDelivery": q0.get("currentDeliveryManifest"),
        "currentPacketAudit": return287["audit"],
        "currentPacketAuditReceipt": return287["receipt"],
        "packetStatus": "RETURN287_AUDITED_HELD_816_32_0",
        "status": "RETURN287_AUDITED_HELD_816_32_0",
        "githubChanges": False,
        "nextGroup": GROUP,
        "next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_816_32_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {
            "group": GROUP, "pendingIds": TARGETS, "pendingCount": 2,
            "status": "FRESH_PACKET288_PREPARATION_IN_PROGRESS",
            "freshPacketRequiredForCurrentAuthority": True,
            "historicalWorkflow": "Conference 129 and source-conference 01 were prepared but never sent; no prior director ruling exists for these two identities.",
            "preservedOriginalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26,
            "requiredMainCases": 4, "futureRequirements": 8,
            "previousHeldBatches": return_hold_entries,
            "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None,
        },
        "lastReviewedBatch": {
            "group": "rank9-alignment-faction-purification5", "pendingIds": return287["heldIds"],
            "acceptedIds": [], "appliedIds": [], "heldIds": return287["heldIds"],
            "blockerIds": {row["id"]: row["blockerIds"] for row in r287_delivery["decisions"]},
            "returnArchive": return287["archive"], "returnAudit": return287["audit"], "returnReceipt": return287["receipt"],
        },
    })
    target_row = next(row for row in queue288["currentPendingGroups"] if row["group"] == GROUP)
    target_row.update({"status": "FRESH_PACKET288_PREPARATION_IN_PROGRESS_816_32_0", "freshPacketRequiredForCurrentAuthority": True, "currentAuthority": AUTHORITY, "previousHeldBatch": {"ids": return287["heldIds"], "blockers": BLOCKERS, "acceptedIds": [], "appliedIds": []}, "historicalWorkflow": "Prepared unsent; no prior director decision."})
    queue288_path = AUDIT / "CURRENT_SPELL_QUEUE_288.json"
    queue288["nextSuggestedGroups"] = [{"group": GROUP, "pendingIds": TARGETS, "pendingCount": len(TARGETS), "selectedByDirectorReturn": 287}]
    queue288_path.write_bytes(enc(queue288))

    handoff288 = copy.deepcopy(h0)
    handoff288.update({
        "id": "CURRENT-HANDOFF-288", "recordedAtUtc": now,
        "status": "RETURN287_AUDITED_HELD_PACKET288_PREPARATION_816_32",
        "currentAuthority": AUTHORITY,
        "pendingIdentityAudit": info(pending288_path), "queue": info(queue288_path), "currentQueueBinding": info(queue288_path),
        "currentReturnBinding": return287["archive"], "currentReturnDelivery": return287["delivery"],
        "currentReturnAudit": return287["audit"], "currentReturnReceipt": return287["receipt"],
        "currentReturnDecision": return287["decisionId"],
        "latestBatch": {"group": "rank9-alignment-faction-purification5", "acceptedIds": [], "appliedIds": [], "heldIds": return287["heldIds"], "blockerIds": BLOCKERS, "returnArchive": return287["archive"], "independentAudit": return287["audit"], "receipt": return287["receipt"]},
        "nextStep": "Prepare, independently audit and send a fresh current-authority packet288 to GPT for only astral-projection and imprisonment. Preserve all four recent held returns and closed acceptances; audit GPT's sealed return and apply only exact accepted IDs.",
        "nextGroup": GROUP, "nextPendingCount": 2,
        "currentPacket": None, "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
        "nextPreparedRequest": queue288["nextPreparedRequest"],
        "githubChanges": False,
        "resumePriority": "Build and independently audit packet288; send it to GPT, read the browser frequently and ping again if needed; audit the sealed return before any application.",
    })
    handoff288_path = AUDIT / "CURRENT_HANDOFF_288.json"
    handoff288_path.write_bytes(enc(handoff288))
    snapshot288_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_288.md"
    snapshot288_path.write_text(
        "# Current Ordinary Spell Review Snapshot 288\n\n"
        "Authority: **816 reviewed/applied / 32 pending / 0 accepted-unapplied**; 540 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return287 independently passed 21/21 and held alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification. AFP211-E01 is closed; no identity was applied. The next group is **Rank9 Projection/Confinement2**: astral-projection and imprisonment. Their old conference packet was prepared but never sent, so no prior director ruling exists.\n\n"
        "Preserve the Return287, Return286, Return285 and Return284 holds and all accepted/applied history. The new packet preserves 24 original questions, two focused additions, four required main cases and eight future requirements. No runtime, implementation, human-play, balance, cosmology, domain-closure, completion or release gate is opened.\n",
        encoding="utf-8",
    )
    start = ROOT / "START_HERE.md"
    lines = start.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = "**Current ordinary spell-review handoff [288](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json):** Return287 independently audited PASS 21/21 and held all five Alignment/Faction/Purification targets; authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**. Preparing fresh packet288 for only astral-projection and imprisonment; the historical conference was prepared but never sent, so there is no earlier director ruling for these targets."
    start.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Refresh the source conference candidate to current authority and bind each
    # target to the current authored index and complete catalog spell record.
    candidate = copy.deepcopy(old_candidate)
    candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-288",
        "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_816_32_EXACT_PROJECTION_CONFINEMENT2_GROUP",
        "sourceCommitBase": head,
        "sourceBranch": branch,
        "currentWorkingTreeSnapshot": True,
        "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 2},
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "priorDirectorReturn": None, "priorDirectorDecision": None},
        "historicalSourceBindings": copy.deepcopy(old_candidate["sourceBindings"]),
        "sourceBindings": refreshed,
        "sourceBindingRefresh": {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "sourceContentsFromCurrentWorkingTree": True, "sourceCommitBase": head},
        "currentReviewTargets": [
            {"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]), "completeCurrentCatalogSourceAndAccess": copy.deepcopy(spells[sid]), "status": "Pending at current 816/32/0 authority; no prior director ruling."}
            for sid in TARGETS
        ],
        "currentAuthorityEvidence": {"currentIndex": info(index_path), "currentCatalog": info(catalog_path), "currentAccessRegistry": info(access_path), "currentQueue": info(queue288_path), "currentHandoff": info(handoff288_path), "currentPendingIdentityAudit": info(pending288_path), "latestReturn287Audit": return287["audit"], "targetIdsStillPending": TARGETS},
        "preservedRecentHolds": return_hold_entries,
        "newRuleAdoptions": 0,
    })
    candidate_raw = enc(candidate)
    OUT = AUDIT / "rank9_projectionconfinement2_current_source_288_prepared"
    OUT.mkdir(parents=True, exist_ok=True)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_288.json"
    context_path = OUT / "CURRENT_CONTEXT_288.json"
    request_path = OUT / "REQUEST_288.txt"
    archive_path = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_288.zip"
    delivery_path = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_288_DELIVERY.json"
    candidate_path.write_bytes(candidate_raw)

    return_records = []
    for number, art in returns.items():
        return_records.append({"returnNumber": number, "archive": art["archive"], "delivery": art["delivery"], "independentAudit": art["audit"], "receipt": art["receipt"], "heldIds": art["heldIds"], "blockerIds": art["blockerIds"]})
    context = {
        "id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-DIRECTOR-CONTEXT-288",
        "recordedAtUtc": now, "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True,
        "sourceAuthority": AUTHORITY, "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 2},
        "currentIndexCounts": index["authoredCounts"], "pendingIdentityAudit": info(pending288_path), "currentQueue": info(queue288_path), "currentHandoff": info(handoff288_path),
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "noPriorDirectorRuling": True},
        "historicalCandidate": info(ROOT / HIST_CANDIDATE), "historicalSourceArchive": info(HIST_ARCHIVE, source_archive_raw),
        "refreshedSourceBindings": len(refreshed), "changedHistoricalSourceBindings": changed,
        "preservation": {"originalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26, "requiredMainCases": 4, "futureCaseRequirements": 8, "targetIdentities": 2, "nativePlacements": 6, "newRuleAdoptions": 0},
        "preparedUnsentConferenceRecord": info(HIST_PACKET_RECORD), "priorConferenceNotes": info(HIST_NOTES),
        "preservedRecentHolds": return_records, "canonicalChanges": False, "runtimeExecuted": False, "applicationChanges": False,
    }
    context_raw = enc(context)
    context_path.write_bytes(context_raw)

    request = (
        f"GPT director â€” continue the ordinary spell review at current authority 816 reviewed/applied / 32 pending / 0 accepted-unapplied (540 complete standalone procedures; 173 scoped interfaces). Review ONLY astral-projection and imprisonment in {GROUP}.\n\n"
        f"This packet snapshots main at base HEAD {head} plus the current working-tree source snapshot. It refreshes all 135 historical source bindings and includes the current catalog/index/access, queue288/handoff288/pending audit288, the source-conference-01 archive, its full preparation/check/request, Conference129 notes and packet record. The earlier conference was prepared but never sent; there is no prior director ruling or blocker list for these two identities, so reassess both afresh from source.\n\n"
        "Preserve all 24 original questions, two focused additions, four required main cases, eight future-case requirements, six printed placements, exact class routes, costs, components and source facts. Keep the historical prepared-only direction as unselected; do not treat its stale 616/232 authority, pending comparisons or unsubmitted proposal as an approval.\n\n"
        "The latest audited holds remain outside scope and must not be reopened or changed: Return287 alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification (AFP211-B01â€“B05; AFP211-E01 closed); Return286 reverse-gravity-field (IE204-B02); Return285 summon-elemental-avatar, summon-herald-of-the-planes and summon-avatar-of-decay (SH202-B01/B02/B03); Return284 banishment-gate and conjure-demiplane-fortress (PG200-B03/B04/B06). Their exact returns, delivery manifests, independent audits and receipts are included.\n\n"
        "For each target, provide explicit accepted/applied/held status, exact blocker IDs and minimum missing source witnesses. Disposition every question; reassess source-grounded procedures and all four original main cases, preserving the eight future requirements. Report all cases, data checks, reversible operations and forward/inverse totals, separating component replay from full positive spell and actor-clock evidence. Do not invent Astral topology, imported silver-cord rules, new confinement geometry, fixed participant caps, copied bodies/resources, or imported Sequester/Maze/Plane Shift authority.\n\n"
        "Do not modify canonical files, apply any spell, run supplied programs or game runtime, or open implementation, human-play, balance, cosmology, domain-closure, completion or release gates. Seal a decision ZIP with a matching DELIVERY.json, report exact next pending group, and continue through response caps until both deliverables are attached."
    )
    request_raw = request.encode("utf-8")
    request_path.write_bytes(request_raw)

    # Snapshot current tracking documents and the audited carry-forward artifacts.
    current_paths = [
        "START_HERE.md", INDEX, CATALOG, ACCESS,
        "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json",
        "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_projection_confinement_2_source_conference_01.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_288.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_PREPARATION.json",
        "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_CHECK.json",
        "docs/audit/2026-10-08/full-game/RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01_REQUEST.txt",
        "docs/audit/2026-10-08/full-game/rank9-projection-confinement2-source-conference-01/MANIFEST.json",
        "docs/audit/2026-10-08/full-game/rank9-projection-confinement2-source-conference-01/README.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_PACKET_129.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_NEXT_CONFERENCE_NOTES_129.json",
    ]
    current_files = {path: (ROOT / path).read_bytes() for path in current_paths if (ROOT / path).exists()}
    for number, art in returns.items():
        evidence_prefix = f"evidence/RETURN{number}"
        current_files[f"{evidence_prefix}_INDEPENDENT_AUDIT.json"] = art["auditPath"].read_bytes()
        current_files[f"{evidence_prefix}_RECEIPT.json"] = art["receiptPath"].read_bytes()
    evidence_files = {}
    for number, art in returns.items():
        evidence_files[f"evidence/RETURN{number}.zip"] = art["archivePath"].read_bytes()
        evidence_files[f"evidence/RETURN{number}_DELIVERY.json"] = art["deliveryPath"].read_bytes()

    files = {
        "CURRENT_CONTEXT_288.json": context_raw,
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_288.json": candidate_raw,
        "REQUEST_288.txt": request_raw,
        "historical/DD_Rank9_Projection_Confinement_2_Source_Conference_01.zip": source_archive_raw,
        "historical/NEXT_CONFERENCE_NOTES_129.json": HIST_NOTES.read_bytes(),
        "historical/PACKET_129_SUBMISSION_RECORD.json": HIST_PACKET_RECORD.read_bytes(),
        "historical/SOURCE_CONFERENCE_PREPARATION_01.json": HIST_PREP.read_bytes(),
        "historical/SOURCE_CONFERENCE_CHECK_01.json": HIST_CHECK.read_bytes(),
        "historical/SOURCE_CONFERENCE_REQUEST_01.txt": HIST_REQUEST.read_bytes(),
        "historical/SOURCE_CONFERENCE_MANIFEST_01.json": HIST_MANIFEST.read_bytes(),
        "historical/SOURCE_CONFERENCE_README_01.md": HIST_README.read_bytes(),
    }
    files.update({"current/" + path: raw for path, raw in current_files.items()})
    files.update(source_files)
    files.update(evidence_files)
    assert all(safe(name) for name in files)
    rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        manifest = {"id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-SOURCE-MANIFEST-288", "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(rows) + 1 == len(set(archive.namelist()))
        for row in rows:
            raw = archive.read(row["path"])
            assert (len(raw), sha(raw), crc(raw)) == (row["bytes"], row["sha256"], row["crc32"])

    archive_info = info(archive_path)
    candidate_info = info(candidate_path, candidate_raw)
    context_info = info(context_path, context_raw)
    request_info = info(request_path, request_raw)
    delivery = {
        "id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-SOURCE-DELIVERY-288",
        "status": "PREPARED_UNAUDITED_UNSENT",
        "archive": archive_info, "members": len(rows) + 1, "manifestBindings": len(rows),
        "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "group": GROUP, "pendingIds": TARGETS, "accepted": False, "applied": False,
        "candidate": candidate_info, "context": context_info, "request": request_info,
        "historicalCandidate": info(ROOT / HIST_CANDIDATE), "historicalSourceArchive": info(HIST_ARCHIVE, source_archive_raw),
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "priorDirectorRuling": None},
        "sourceBindings": len(refreshed), "changedSourceBindings": changed,
        "originalQuestions": 24, "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureRequirements": 8,
        "preservedRecentHolds": return_records, "canonicalChanges": False, "applicationChanges": False,
        "conversation": CHAT,
    }
    delivery_raw = enc(delivery)
    delivery_path.write_bytes(delivery_raw)
    prep_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_SOURCE_PREPARATION_288.json"
    packet_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288.json"
    prep = {"id": "RANK9PROJECTIONCONFINEMENT2-SOURCE-PREPARATION-288", "recordedAtUtc": now, "status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": TARGETS, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "context": context_info, "sourceBindings": len(refreshed), "changedHistoricalBindings": changed, "originalQuestions": 24, "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureCaseRequirements": 8, "historicalWorkflow": delivery["historicalWorkflow"], "priorReturns": return_records, "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path.write_bytes(enc(prep))
    packet = {"id": "RANK9PROJECTIONCONFINEMENT2-PACKET-288", "status": "PREPARED_UNAUDITED_UNSENT", "group": GROUP, "pendingIds": TARGETS, "sourceAuthority": AUTHORITY, "sourceBranch": branch, "sourceCommitBase": head, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "totalQuestions": 26, "originalQuestions": 24, "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureCaseRequirements": 8, "refreshedSourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "historicalWorkflow": delivery["historicalWorkflow"], "preservedRecentHolds": return_records, "canonicalChanges": False, "independentAudit": None}
    packet_path.write_bytes(enc(packet))

    # Bind the prepared, not-yet-audited packet into queue and handoff.
    queue_doc = read(queue288_path)
    prep_info = info(prep_path)
    delivery_info = info(delivery_path, delivery_raw)
    next_request = queue_doc["nextPreparedRequest"]
    next_request.update({"status": "PACKET288_PREPARED_UNAUDITED_UNSENT", "packet": archive_info, "deliveryManifest": delivery_info, "candidate": candidate_info, "sourcePreparation": prep_info})
    queue_doc["currentPacket"] = archive_info
    queue_doc["currentDeliveryManifest"] = delivery_info
    queue_doc["currentPreparation"] = prep_info
    queue_doc["status"] = "PACKET288_PREPARED_UNAUDITED_816_32_0"
    queue_doc["packetStatus"] = "PACKET288_PREPARED_UNAUDITED_816_32_0"
    queue288_path.write_bytes(enc(queue_doc))
    handoff_doc = read(handoff288_path)
    handoff_doc["nextPreparedRequest"] = next_request
    handoff_doc["currentPacket"] = archive_info
    handoff_doc["currentPacketDelivery"] = delivery_info
    handoff_doc["currentPreparation"] = prep_info
    handoff_doc["currentQueueBinding"] = info(queue288_path)
    handoff_doc["status"] = "PACKET288_PREPARED_UNAUDITED_816_32"
    handoff_doc["resumePriority"] = "Independently audit packet288 before sending it to GPT; monitor the browser frequently and ping if needed, audit the sealed return, then apply only exact accepted IDs."
    handoff288_path.write_bytes(enc(handoff_doc))
    lines = start.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = f"**Current ordinary spell-review handoff [288](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json):** Return287 independently audited PASS 21/21 and held all five Alignment/Faction/Purification targets; authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**. Packet288 for only astral-projection and imprisonment is prepared and awaiting its independent packet audit; their historical director conference was never sent."
    start.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch, "authority": AUTHORITY, "targets": TARGETS, "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "questions": 26, "mainCases": 4, "futureRequirements": 8, "members": len(rows) + 1, "archiveBytes": archive_info["bytes"], "archiveSha256": archive_info["sha256"], "deliveryManifestBytes": len(delivery_raw), "deliveryManifestSha256": sha(delivery_raw), "out": str(archive_path), "priorReturns": {number: art["heldIds"] for number, art in returns.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
