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
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
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
    228: ("rank9_impactexile4_return228_received", "DD_Rank9_ImpactExile1_Director_Return228.zip", "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json", ["reverse-gravity-field"], ["IE204-B02"]),
    229: ("rank9_illusionreality5_return229_received", "DD_Rank9_IllusionReality1_Director_Return229.zip", "DD_Rank9_IllusionReality1_Director_Return229_DELIVERY.json", "RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json", "RANK9ILLUSIONREALITY5_RETURN229_RECEIPT.json", ["soul-reflection"], ["IR207-B02"]),
    230: ("rank9_materialforging2_return230_received", "DD_Rank9_MaterialForging2_Director_Return230.zip", "DD_Rank9_MaterialForging2_Director_Return230_DELIVERY.json", "RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT.json", "RANK9MATERIALFORGING2_RETURN230_RECEIPT.json", ["eternal-forge", "matter-conversion"], ["MF210-B01", "MF210-B02"]),
    231: ("rank9_alignment_faction_purification5_return231_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json", ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]),
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
    assert audit_doc["status"] == "PASS" and audit_doc["failedChecks"] == 0
    assert delivery_doc["accepted"] is False and delivery_doc["applied"] is False
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
    queue231_path = AUDIT / "CURRENT_SPELL_QUEUE_231.json"
    handoff231_path = AUDIT / "CURRENT_HANDOFF_231.json"
    pending231_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_231.json"
    q0, h0, p0 = read(queue231_path), read(handoff231_path), read(pending231_path)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    pending = sorted(row["id"] for row in index["entries"] if row.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending) == 37 and set(TARGETS) <= set(pending)
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
    returns = {number: return_artifacts(number) for number in (228, 229, 230, 231)}
    return231 = returns[231]
    assert return231["heldIds"] == ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]
    r231_delivery = read(return231["deliveryPath"])
    assert r231_delivery["closedEvidenceFinding"]["id"] == "AFP211-E01"
    assert r231_delivery["closedEvidenceFinding"]["status"] == "CLOSED"

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

    # Record Return231 as a completed held batch and publish the next queue snapshot.
    submission_path = AUDIT / "RANK9ALIGNFACTIONPURIFICATION5_PACKET_231_SUBMISSION.json"
    submission231 = read(submission_path)
    submission231.update({
        "status": "RETURN231_AUDITED_HELD_811_37_0",
        "directorReturn": {"archive": return231["archive"], "deliveryManifest": return231["delivery"], "decisionId": return231["decisionId"], "heldIds": return231["heldIds"], "acceptedIds": [], "appliedIds": []},
        "independentReturnAudit": return231["audit"],
        "returnReceipt": return231["receipt"],
        "canonicalChanges": False,
        "applicationChanges": False,
    })
    submission_path.write_bytes(enc(submission231))
    submission_info = info(submission_path)

    return_hold_entries = [
        {"heldIds": returns[n]["heldIds"], "blockerIds": returns[n]["blockerIds"], "archive": returns[n]["archive"], "audit": returns[n]["audit"], "receipt": returns[n]["receipt"]}
        for n in (228, 229, 230, 231)
    ]
    pending232 = copy.deepcopy(p0)
    pending232.update({
        "id": "CURRENT37-PENDING-IDENTITY-AUDIT-232",
        "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN231",
        "lastDirectorReturn": {"archive": return231["archive"], "deliveryManifest": return231["delivery"], "independentAudit": return231["audit"], "receipt": return231["receipt"], "acceptedIds": [], "appliedIds": [], "heldIds": return231["heldIds"], "blockerIds": return231["blockerIds"]},
        "preservedRecentHolds": return_hold_entries,
        "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "historicalPhase": "PREPARED_UNSENT_NOT_DIRECTOR_REVIEWED", "freshPacketRequiredForCurrentAuthority": True},
    })
    pending232_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_232.json"
    pending232_path.write_bytes(enc(pending232))

    queue232 = copy.deepcopy(q0)
    queue232.update({
        "id": "SPELL-REVIEW-QUEUE-232",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-231",
        "pendingIdentityAudit": info(pending232_path),
        "currentReturnAudit": return231["audit"],
        "currentReturnDelivery": return231["delivery"],
        "currentReturnArchive": return231["archive"],
        "currentReturnDecision": return231["decisionId"],
        "currentReturnReceipt": return231["receipt"],
        "currentReturnBinding": return231["archive"],
        "currentReturnSourceArchive": q0.get("currentPacket"),
        "currentReturnSourceDelivery": q0.get("currentDeliveryManifest"),
        "currentPacketAudit": return231["audit"],
        "currentPacketAuditReceipt": return231["receipt"],
        "packetStatus": "RETURN231_AUDITED_HELD_811_37_0",
        "status": "RETURN231_AUDITED_HELD_811_37_0",
        "githubChanges": False,
        "nextGroup": GROUP,
        "next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {
            "group": GROUP, "pendingIds": TARGETS, "pendingCount": 2,
            "status": "FRESH_PACKET232_PREPARATION_IN_PROGRESS",
            "freshPacketRequiredForCurrentAuthority": True,
            "historicalWorkflow": "Conference 129 and source-conference 01 were prepared but never sent; no prior director ruling exists for these two identities.",
            "preservedOriginalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26,
            "requiredMainCases": 4, "futureRequirements": 8,
            "previousHeldBatches": return_hold_entries,
            "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None,
        },
        "lastReviewedBatch": {
            "group": "rank9-alignment-faction-purification5", "pendingIds": return231["heldIds"],
            "acceptedIds": [], "appliedIds": [], "heldIds": return231["heldIds"],
            "blockerIds": {row["id"]: row["blockerIds"] for row in r231_delivery["perIdentityDecisions"]},
            "returnArchive": return231["archive"], "returnAudit": return231["audit"], "returnReceipt": return231["receipt"],
        },
    })
    target_row = next(row for row in queue232["currentPendingGroups"] if row["group"] == GROUP)
    target_row.update({"status": "FRESH_PACKET232_PREPARATION_IN_PROGRESS_811_37_0", "freshPacketRequiredForCurrentAuthority": True, "currentAuthority": AUTHORITY, "previousHeldBatch": {"ids": return231["heldIds"], "blockers": BLOCKERS, "acceptedIds": [], "appliedIds": []}, "historicalWorkflow": "Prepared unsent; no prior director decision."})
    queue232_path = AUDIT / "CURRENT_SPELL_QUEUE_232.json"
    queue232_path.write_bytes(enc(queue232))

    handoff232 = copy.deepcopy(h0)
    handoff232.update({
        "id": "CURRENT-HANDOFF-232", "recordedAtUtc": now,
        "status": "RETURN231_AUDITED_HELD_PACKET232_PREPARATION_811_37",
        "currentAuthority": AUTHORITY,
        "pendingIdentityAudit": info(pending232_path), "queue": info(queue232_path), "currentQueueBinding": info(queue232_path),
        "currentReturnBinding": return231["archive"], "currentReturnDelivery": return231["delivery"],
        "currentReturnAudit": return231["audit"], "currentReturnReceipt": return231["receipt"],
        "currentReturnDecision": return231["decisionId"],
        "latestBatch": {"group": "rank9-alignment-faction-purification5", "acceptedIds": [], "appliedIds": [], "heldIds": return231["heldIds"], "blockerIds": BLOCKERS, "returnArchive": return231["archive"], "independentAudit": return231["audit"], "receipt": return231["receipt"]},
        "nextStep": "Prepare, independently audit and send a fresh current-authority packet232 to GPT for only astral-projection and imprisonment. Preserve all four recent held returns and closed acceptances; audit GPT's sealed return and apply only exact accepted IDs.",
        "nextGroup": GROUP, "nextPendingCount": 2,
        "currentPacket": None, "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
        "nextPreparedRequest": queue232["nextPreparedRequest"],
        "githubChanges": False,
        "resumePriority": "Build and independently audit packet232; send it to GPT, read the browser frequently and ping again if needed; audit the sealed return before any application.",
    })
    handoff232_path = AUDIT / "CURRENT_HANDOFF_232.json"
    handoff232_path.write_bytes(enc(handoff232))
    snapshot232_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_232.md"
    snapshot232_path.write_text(
        "# Current Ordinary Spell Review Snapshot 232\n\n"
        "Authority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return231 independently passed 26/26 and held alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification. AFP211-E01 is closed; no identity was applied. The next group is **Rank9 Projection/Confinement2**: astral-projection and imprisonment. Their old conference packet was prepared but never sent, so no prior director ruling exists.\n\n"
        "Preserve Return231, Return230, Return229 and Return228 holds and all accepted/applied history. The new packet preserves 24 original questions, two focused additions, four required main cases and eight future requirements. No runtime, implementation, human-play, balance, cosmology, domain-closure, completion or release gate is opened.\n",
        encoding="utf-8",
    )
    start = ROOT / "START_HERE.md"
    lines = start.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = "**Current ordinary spell-review handoff [232](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_232.json):** Return231 independently audited PASS 26/26 and held all five Alignment/Faction/Purification targets; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Preparing fresh packet232 for only astral-projection and imprisonment; the historical conference was prepared but never sent, so there is no earlier director ruling for these targets."
    start.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Refresh the source conference candidate to current authority and bind each
    # target to the current authored index and complete catalog spell record.
    candidate = copy.deepcopy(old_candidate)
    candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-232",
        "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_PROJECTION_CONFINEMENT2_GROUP",
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
            {"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]), "completeCurrentCatalogSourceAndAccess": copy.deepcopy(spells[sid]), "status": "Pending at current 811/37/0 authority; no prior director ruling."}
            for sid in TARGETS
        ],
        "currentAuthorityEvidence": {"currentIndex": info(index_path), "currentCatalog": info(catalog_path), "currentAccessRegistry": info(access_path), "currentQueue": info(queue232_path), "currentHandoff": info(handoff232_path), "currentPendingIdentityAudit": info(pending232_path), "latestReturn231Audit": return231["audit"], "targetIdsStillPending": TARGETS},
        "preservedRecentHolds": return_hold_entries,
        "newRuleAdoptions": 0,
    })
    candidate_raw = enc(candidate)
    OUT = AUDIT / "rank9_projectionconfinement2_current_source_232_prepared"
    OUT.mkdir(parents=True, exist_ok=True)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_232.json"
    context_path = OUT / "CURRENT_CONTEXT_232.json"
    request_path = OUT / "REQUEST_232.txt"
    archive_path = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_232.zip"
    delivery_path = OUT / "DD_Rank9_ProjectionConfinement2_CurrentSource_232_DELIVERY.json"
    candidate_path.write_bytes(candidate_raw)

    return_records = []
    for number, art in returns.items():
        return_records.append({"returnNumber": number, "archive": art["archive"], "delivery": art["delivery"], "independentAudit": art["audit"], "receipt": art["receipt"], "heldIds": art["heldIds"], "blockerIds": art["blockerIds"]})
    context = {
        "id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-DIRECTOR-CONTEXT-232",
        "recordedAtUtc": now, "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True,
        "sourceAuthority": AUTHORITY, "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 2},
        "currentIndexCounts": index["authoredCounts"], "pendingIdentityAudit": info(pending232_path), "currentQueue": info(queue232_path), "currentHandoff": info(handoff232_path),
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
        f"GPT director — continue the ordinary spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). Review ONLY astral-projection and imprisonment in {GROUP}.\n\n"
        f"This packet snapshots main at base HEAD {head} plus the current working-tree source snapshot. It refreshes all 135 historical source bindings and includes the current catalog/index/access, queue232/handoff232/pending audit232, the source-conference-01 archive, its full preparation/check/request, Conference129 notes and packet record. The earlier conference was prepared but never sent; there is no prior director ruling or blocker list for these two identities, so reassess both afresh from source.\n\n"
        "Preserve all 24 original questions, two focused additions, four required main cases, eight future-case requirements, six printed placements, exact class routes, costs, components and source facts. Keep the historical prepared-only direction as unselected; do not treat its stale 616/232 authority, pending comparisons or unsubmitted proposal as an approval.\n\n"
        "The latest audited holds remain outside scope and must not be reopened or changed: Return231 alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification (AFP211-B01–B05; AFP211-E01 closed); Return230 eternal-forge and matter-conversion (MF210-B01/B02); Return229 soul-reflection (IR207-B02); Return228 reverse-gravity-field (IE204-B02). Their exact returns, delivery manifests, independent audits and receipts are included.\n\n"
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
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_232.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_PACKET_231_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json",
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
        "CURRENT_CONTEXT_232.json": context_raw,
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_232.json": candidate_raw,
        "REQUEST_232.txt": request_raw,
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
        manifest = {"id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-SOURCE-MANIFEST-232", "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "memberCountExcludingSelf": len(rows), "members": rows}
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
        "id": "RANK9-PROJECTION-CONFINEMENT2-CURRENT-SOURCE-DELIVERY-232",
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
    prep_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_SOURCE_PREPARATION_232.json"
    packet_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_232.json"
    prep = {"id": "RANK9PROJECTIONCONFINEMENT2-SOURCE-PREPARATION-232", "recordedAtUtc": now, "status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": TARGETS, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "context": context_info, "sourceBindings": len(refreshed), "changedHistoricalBindings": changed, "originalQuestions": 24, "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureCaseRequirements": 8, "historicalWorkflow": delivery["historicalWorkflow"], "priorReturns": return_records, "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path.write_bytes(enc(prep))
    packet = {"id": "RANK9PROJECTIONCONFINEMENT2-PACKET-232", "status": "PREPARED_UNAUDITED_UNSENT", "group": GROUP, "pendingIds": TARGETS, "sourceAuthority": AUTHORITY, "sourceBranch": branch, "sourceCommitBase": head, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "totalQuestions": 26, "originalQuestions": 24, "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureCaseRequirements": 8, "refreshedSourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "historicalWorkflow": delivery["historicalWorkflow"], "preservedRecentHolds": return_records, "canonicalChanges": False, "independentAudit": None}
    packet_path.write_bytes(enc(packet))

    # Bind the prepared, not-yet-audited packet into queue and handoff.
    queue_doc = read(queue232_path)
    prep_info = info(prep_path)
    delivery_info = info(delivery_path, delivery_raw)
    next_request = queue_doc["nextPreparedRequest"]
    next_request.update({"status": "PACKET232_PREPARED_UNAUDITED_UNSENT", "packet": archive_info, "deliveryManifest": delivery_info, "candidate": candidate_info, "sourcePreparation": prep_info})
    queue_doc["currentPacket"] = archive_info
    queue_doc["currentDeliveryManifest"] = delivery_info
    queue_doc["currentPreparation"] = prep_info
    queue_doc["status"] = "PACKET232_PREPARED_UNAUDITED_811_37_0"
    queue_doc["packetStatus"] = "PACKET232_PREPARED_UNAUDITED_811_37_0"
    queue232_path.write_bytes(enc(queue_doc))
    handoff_doc = read(handoff232_path)
    handoff_doc["nextPreparedRequest"] = next_request
    handoff_doc["currentPacket"] = archive_info
    handoff_doc["currentPacketDelivery"] = delivery_info
    handoff_doc["currentPreparation"] = prep_info
    handoff_doc["currentQueueBinding"] = info(queue232_path)
    handoff_doc["status"] = "PACKET232_PREPARED_UNAUDITED_811_37"
    handoff_doc["resumePriority"] = "Independently audit packet232 before sending it to GPT; monitor the browser frequently and ping if needed, audit the sealed return, then apply only exact accepted IDs."
    handoff232_path.write_bytes(enc(handoff_doc))
    lines = start.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = f"**Current ordinary spell-review handoff [232](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_232.json):** Return231 independently audited PASS 26/26 and held all five Alignment/Faction/Purification targets; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Packet232 for only astral-projection and imprisonment is prepared and awaiting its independent packet audit; their historical director conference was never sent."
    start.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch, "authority": AUTHORITY, "targets": TARGETS, "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "questions": 26, "mainCases": 4, "futureRequirements": 8, "members": len(rows) + 1, "archiveBytes": archive_info["bytes"], "archiveSha256": archive_info["sha256"], "deliveryManifestBytes": len(delivery_raw), "deliveryManifestSha256": sha(delivery_raw), "out": str(archive_path), "priorReturns": {number: art["heldIds"] for number, art in returns.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
