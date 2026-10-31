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
GROUP = "rank9-miracle-reality2"
TARGETS = ["divine-intervention-greater", "wish"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
HIST_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_miracle_reality_2_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Miracle_Reality_2_Source_Conference_01.zip"
HIST_NOTES = AUDIT / "RANK9MIRACLEREALITY2_NEXT_CONFERENCE_NOTES_129.json"
HIST_PACKET = AUDIT / "RANK9MIRACLEREALITY2_PACKET_129.json"
HIST_PREP = FULL / "RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_PREPARATION.json"
HIST_CHECK = FULL / "RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_CHECK.json"
HIST_REQUEST = FULL / "RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_REQUEST.txt"
HIST_MANIFEST = FULL / "rank9-miracle-reality2-source-conference-01/MANIFEST.json"
HIST_README = FULL / "rank9-miracle-reality2-source-conference-01/README.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

# Return number, received folder, archive, delivery, independent audit, receipt,
# held identities, and their blocker IDs. Each is independently audited.
RETURN_INFO = {
    228: ("rank9_impactexile4_return228_received", "DD_Rank9_ImpactExile1_Director_Return228.zip", "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json", ["reverse-gravity-field"], ["IE204-B02"]),
    229: ("rank9_illusionreality5_return229_received", "DD_Rank9_IllusionReality1_Director_Return229.zip", "DD_Rank9_IllusionReality1_Director_Return229_DELIVERY.json", "RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json", "RANK9ILLUSIONREALITY5_RETURN229_RECEIPT.json", ["soul-reflection"], ["IR207-B02"]),
    230: ("rank9_materialforging2_return230_received", "DD_Rank9_MaterialForging2_Director_Return230.zip", "DD_Rank9_MaterialForging2_Director_Return230_DELIVERY.json", "RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT.json", "RANK9MATERIALFORGING2_RETURN230_RECEIPT.json", ["eternal-forge", "matter-conversion"], ["MF210-B01", "MF210-B02"]),
    231: ("rank9_alignment_faction_purification5_return231_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json", ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]),
    232: ("rank9_projectionconfinement2_return232_received", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json", ["astral-projection", "imprisonment"], ["PC232-B01", "PC232-B02"]),
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
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def return_artifacts(number: int) -> dict:
    folder, archive_name, delivery_name, audit_name, receipt_name, held, blockers = RETURN_INFO[number]
    received = AUDIT / folder
    archive, delivery = received / archive_name, received / delivery_name
    audit, receipt = AUDIT / audit_name, AUDIT / receipt_name
    audit_doc, delivery_doc = read(audit), read(delivery)
    assert audit_doc["status"] == "PASS" and audit_doc["failedChecks"] == 0, number
    assert delivery_doc["accepted"] is False and delivery_doc["applied"] is False, number
    assert delivery_doc["heldIds"] == held, number
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    return {
        "archivePath": archive, "deliveryPath": delivery, "auditPath": audit, "receiptPath": receipt,
        "archive": info(archive), "delivery": info(delivery), "audit": info(audit), "receipt": info(receipt),
        "heldIds": held, "blockerIds": blockers, "decisionId": delivery_doc.get("id"),
    }


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    now = datetime.now(timezone.utc).isoformat()

    index_path, catalog_path, access_path = ROOT / INDEX, ROOT / CATALOG, ROOT / ACCESS
    index, catalog = read(index_path), read(catalog_path)
    queue232_path, handoff232_path = AUDIT / "CURRENT_SPELL_QUEUE_232.json", AUDIT / "CURRENT_HANDOFF_232.json"
    pending232_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_232.json"
    q0, h0, p0 = read(queue232_path), read(handoff232_path), read(pending232_path)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    pending = sorted(row["id"] for row in index["entries"] if row.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending) == 37 and set(TARGETS) <= set(pending)
    current_group = next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP)
    assert current_group["pendingIds"] == TARGETS and current_group["pendingCount"] == 2
    for spell_id in TARGETS:
        assert entries[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert entries[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert spells[spell_id]["id"] == spell_id

    old_candidate, old_notes = read(ROOT / HIST_CANDIDATE), read(HIST_NOTES)
    old_packet, old_prep = read(HIST_PACKET), read(HIST_PREP)
    assert old_prep["status"] == "PREPARED_UNSENT"
    assert old_packet["status"] == "PREPARED_NOT_SENT"
    assert [row["spellId"] for row in old_candidate["records"]] == TARGETS
    assert len(old_candidate["questions"]) == 24 and len(old_candidate["futureCaseRequirements"]) == 8
    assert len(old_notes["completeOriginalQuestionsUnchanged"]) == 24
    assert len(old_notes["focusedAdditionalQuestions"]) == 2 and len(old_notes["allQuestions"]) == 26
    assert len(old_notes["requiredNewCases"]) == 4 and len(old_notes["originalFutureCaseRequirementsUnchanged"]) == 8

    returns = {number: return_artifacts(number) for number in RETURN_INFO}
    return232 = returns[232]
    assert return232["heldIds"] == ["astral-projection", "imprisonment"]
    return_records = [
        {"returnNumber": n, "archive": a["archive"], "delivery": a["delivery"], "independentAudit": a["audit"], "receipt": a["receipt"], "heldIds": a["heldIds"], "blockerIds": a["blockerIds"]}
        for n, a in returns.items()
    ]
    hold_entries = [{"heldIds": a["heldIds"], "blockerIds": a["blockerIds"], "archive": a["archive"], "audit": a["audit"], "receipt": a["receipt"]} for a in returns.values()]

    # Verify every historical binding against the old conference archive, then
    # independently refresh the binding to the current working-tree bytes.
    source_archive_raw = HIST_ARCHIVE.read_bytes()
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        refreshed, changed, source_files = [], [], {}
        for old in old_candidate["sourceBindings"]:
            path = old["path"]
            assert safe(path)
            historical_raw = historical_zip.read("sources/" + path)
            assert (len(historical_raw), sha(historical_raw)) == (old["bytes"], old["sha256"])
            current_raw = (ROOT / path).read_bytes()
            row = {"path": path, "bytes": len(current_raw), "sha256": sha(current_raw), "gitBlobSHA1": git_blob_sha(current_raw)}
            refreshed.append(row)
            source_files["sources_current/" + path] = current_raw
            if (row["bytes"], row["sha256"]) != (old["bytes"], old["sha256"]):
                changed.append({"path": path, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"], "currentBytes": row["bytes"], "currentSha256": row["sha256"]})
    assert len(refreshed) == len(source_files) == 153 and len({row["path"] for row in refreshed}) == 153

    pending233 = copy.deepcopy(p0)
    pending233.update({
        "id": "CURRENT37-PENDING-IDENTITY-AUDIT-233", "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN232",
        "lastDirectorReturn": {"archive": return232["archive"], "deliveryManifest": return232["delivery"], "independentAudit": return232["audit"], "receipt": return232["receipt"], "acceptedIds": [], "appliedIds": [], "heldIds": return232["heldIds"], "blockerIds": return232["blockerIds"]},
        "preservedRecentHolds": hold_entries,
        "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "historicalPhase": "PREPARED_UNSENT_NOT_DIRECTOR_REVIEWED", "freshPacketRequiredForCurrentAuthority": True},
    })
    pending233_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_233.json"
    pending233_path.write_bytes(enc(pending233))

    blockers_by_id = {spell_id: [blocker] for a in returns.values() for spell_id, blocker in zip(a["heldIds"], a["blockerIds"])}
    queue233 = copy.deepcopy(q0)
    queue233.update({
        "id": "SPELL-REVIEW-QUEUE-233", "recordedAtUtc": now, "supersedesQueue": "SPELL-REVIEW-QUEUE-232",
        "pendingIdentityAudit": info(pending233_path),
        "currentReturnAudit": return232["audit"], "currentReturnDelivery": return232["delivery"],
        "currentReturnArchive": return232["archive"], "currentReturnDecision": return232["decisionId"],
        "currentReturnReceipt": return232["receipt"], "currentReturnBinding": return232["archive"],
        "currentReturnSourceArchive": q0.get("currentPacket"), "currentReturnSourceDelivery": q0.get("currentDeliveryManifest"),
        "currentPacketAudit": return232["audit"], "currentPacketAuditReceipt": return232["receipt"],
        "packetStatus": "RETURN232_AUDITED_HELD_811_37_0", "status": "RETURN232_AUDITED_HELD_811_37_0", "githubChanges": False,
        "nextGroup": GROUP,
        "next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
        "nextPreparedRequest": {
            "group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "status": "FRESH_PACKET233_PREPARATION_IN_PROGRESS",
            "freshPacketRequiredForCurrentAuthority": True,
            "historicalWorkflow": "The source conference was prepared but never sent; no director ruling exists for these two identities.",
            "preservedOriginalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26,
            "requiredMainCases": 4, "futureRequirements": 8, "previousHeldBatches": hold_entries,
            "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None,
        },
        "lastReviewedBatch": {
            "group": "rank9-projection-confinement2", "pendingIds": return232["heldIds"], "acceptedIds": [], "appliedIds": [],
            "heldIds": return232["heldIds"], "blockerIds": {sid: blockers_by_id[sid] for sid in return232["heldIds"]},
            "returnArchive": return232["archive"], "returnAudit": return232["audit"], "returnReceipt": return232["receipt"],
        },
    })
    target_row = next(row for row in queue233["currentPendingGroups"] if row["group"] == GROUP)
    target_row.update({"status": "FRESH_PACKET233_PREPARATION_IN_PROGRESS_811_37_0", "freshPacketRequiredForCurrentAuthority": True, "currentAuthority": AUTHORITY,
                       "previousHeldBatch": {"ids": return232["heldIds"], "blockers": return232["blockerIds"], "acceptedIds": [], "appliedIds": []},
                       "historicalWorkflow": "Prepared unsent; no prior director decision."})
    queue233_path = AUDIT / "CURRENT_SPELL_QUEUE_233.json"
    queue233_path.write_bytes(enc(queue233))

    handoff233 = copy.deepcopy(h0)
    handoff233.update({
        "id": "CURRENT-HANDOFF-233", "recordedAtUtc": now, "status": "RETURN232_AUDITED_HELD_PACKET233_PREPARATION_811_37",
        "currentAuthority": AUTHORITY, "pendingIdentityAudit": info(pending233_path), "queue": info(queue233_path), "currentQueueBinding": info(queue233_path),
        "currentReturnBinding": return232["archive"], "currentReturnDelivery": return232["delivery"], "currentReturnAudit": return232["audit"],
        "currentReturnReceipt": return232["receipt"], "currentReturnDecision": return232["decisionId"],
        "latestBatch": {"group": "rank9-projection-confinement2", "acceptedIds": [], "appliedIds": [], "heldIds": return232["heldIds"],
                        "blockerIds": {sid: blockers_by_id[sid] for sid in return232["heldIds"]}, "returnArchive": return232["archive"], "independentAudit": return232["audit"], "receipt": return232["receipt"]},
        "nextStep": "Prepare and independently audit fresh current-authority Packet233 for divine-intervention-greater and wish; submit to GPT, monitor and ping if needed, audit the sealed return, and apply only exact accepted IDs.",
        "nextGroup": GROUP, "nextPendingCount": 2, "currentPacket": None, "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
        "nextPreparedRequest": queue233["nextPreparedRequest"], "githubChanges": False,
        "resumePriority": "Build and independently audit packet233; send it to GPT, read the browser frequently and ping again if needed; audit the sealed return before any application.",
    })
    handoff233_path = AUDIT / "CURRENT_HANDOFF_233.json"
    handoff233_path.write_bytes(enc(handoff233))

    # Refresh the prepared candidate with current source/index bindings while
    # retaining all historical questions, cases, and future requirements.
    candidate = copy.deepcopy(old_candidate)
    candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-233", "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_MIRACLE_REALITY2_GROUP",
        "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True, "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 2},
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "priorDirectorReturn": None, "priorDirectorDecision": None},
        "historicalSourceBindings": copy.deepcopy(old_candidate["sourceBindings"]), "sourceBindings": refreshed,
        "sourceBindingRefresh": {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed, "sourceContentsFromCurrentWorkingTree": True, "sourceCommitBase": head},
        "currentReviewTargets": [{"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]), "completeCurrentCatalogSourceAndAccess": copy.deepcopy(spells[sid]), "status": "Pending at current 811/37/0 authority; no prior director ruling."} for sid in TARGETS],
        "currentAuthorityEvidence": {"currentIndex": info(index_path), "currentCatalog": info(catalog_path), "currentAccessRegistry": info(access_path),
                                    "currentQueue": info(queue233_path), "currentHandoff": info(handoff233_path), "currentPendingIdentityAudit": info(pending233_path),
                                    "latestReturn232Audit": return232["audit"], "targetIdsStillPending": TARGETS},
        "preservedRecentHolds": hold_entries, "newRuleAdoptions": 0,
    })
    candidate_raw = enc(candidate)
    OUT = AUDIT / "rank9_miraclereality2_current_source_233_prepared"
    OUT.mkdir(parents=True, exist_ok=True)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_233.json"
    context_path = OUT / "CURRENT_CONTEXT_233.json"
    request_path = OUT / "REQUEST_233.txt"
    archive_path = OUT / "DD_Rank9_MiracleReality2_CurrentSource_233_CORRECTED_V2.zip"
    delivery_path = OUT / "DD_Rank9_MiracleReality2_CurrentSource_233_CORRECTED_V2_DELIVERY.json"
    candidate_path.write_bytes(candidate_raw)

    native_placements = sum(len(spells[sid].get("source", {}).get("original", {}).get("placements", [])) for sid in TARGETS)
    context = {
        "id": "RANK9-MIRACLE-REALITY2-CURRENT-DIRECTOR-CONTEXT-233", "recordedAtUtc": now,
        "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 2}, "currentIndexCounts": index["authoredCounts"],
        "pendingIdentityAudit": info(pending233_path), "currentQueue": info(queue233_path), "currentHandoff": info(handoff233_path),
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "noPriorDirectorRuling": True},
        "historicalCandidate": info(ROOT / HIST_CANDIDATE), "historicalSourceArchive": info(HIST_ARCHIVE, source_archive_raw),
        "refreshedSourceBindings": len(refreshed), "changedHistoricalSourceBindings": changed,
        "preservation": {"originalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26, "requiredMainCases": 4,
                         "futureCaseRequirements": 8, "targetIdentities": 2, "nativePlacements": native_placements, "newRuleAdoptions": 0},
        "preparedUnsentConferenceRecord": info(HIST_PACKET), "priorConferenceNotes": info(HIST_NOTES), "preservedRecentHolds": return_records,
        "canonicalChanges": False, "runtimeExecuted": False, "applicationChanges": False,
    }
    context_raw = enc(context)
    context_path.write_bytes(context_raw)

    request = (
        f"GPT director — continue ordinary spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). Review ONLY divine-intervention-greater and wish in {GROUP}.\n\n"
        f"This packet snapshots main at base HEAD {head} plus current working-tree source bytes. It refreshes all 153 historical source bindings and includes the current catalog/index/access, queue233/handoff233/pending audit233, the source-conference-01 archive, its preparation/check/request, Conference129 notes and packet record. Those conferences were prepared but never sent; there is no prior director ruling or blocker list for these identities.\n\n"
        "Preserve all 24 original questions, both focused additions, all four required main cases and all eight future-case requirements. Preserve the exact current class routes and both printed Wish placements. Reconcile the current Player Rulebook and Core V2 records without erasing their source distinction: the short catalog summaries are not operational procedures. The record attributes Greater Divine Intervention to one question or task with a Director-determined miracle; Wish is described as reshaping reality. Surface the source gaps for casting, target/intent validation, resolution, costs, lifecycle, reversibility and adverse outcomes.\n\n"
        "The latest audited holds remain outside scope and must not be reopened or changed: Return232 astral-projection and imprisonment (PC232-B01/B02); Return231 alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification (AFP211-B01–B05; AFP211-E01 closed); Return230 eternal-forge and matter-conversion (MF210-B01/B02); Return229 soul-reflection (IR207-B02); Return228 reverse-gravity-field (IE204-B02). Their exact returns, delivery manifests, independent audits and receipts are included.\n\n"
        "Disposition every question and each identity. Provide source-linked operational procedures and positive plus meaningful adverse/edge cases for all four required cases; preserve the eight future requirements and clearly separate grounded source facts from any proposed new rule. Do not import D&D Wish or Divine Intervention rules, random success rolls, cooldowns, percentages, limits, costs, penalties, deity behavior, freeform authority, or automatic outcomes unless the current named project sources explicitly establish them. Do not broaden class access, infer new costs from missing data, or adopt any new rule. Report every data check and reversible operation, forward/inverse totals, component replay versus full positive-spell/actor-clock evidence, and exact accepted/applied/held IDs with blockers and minimum missing witnesses.\n\n"
        "Do not modify canonical files, apply any spell, run supplied programs or game runtime, or open implementation, human-play, balance, cosmology, domain-closure, completion or release gates. Seal the decision in a ZIP with a matching DELIVERY.json, state the exact next pending group, and continue through response caps until both deliverables are attached."
    )
    request_raw = request.encode("utf-8")
    request_path.write_bytes(request_raw)

    current_paths = [
        "START_HERE.md", INDEX, CATALOG, ACCESS,
        "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json", HIST_CANDIDATE,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_232.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_232.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_PACKET_232_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_PREPARATION.json",
        "docs/audit/2026-10-08/full-game/RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_CHECK.json",
        "docs/audit/2026-10-08/full-game/RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01_REQUEST.txt",
        "docs/audit/2026-10-08/full-game/rank9-miracle-reality2-source-conference-01/MANIFEST.json",
        "docs/audit/2026-10-08/full-game/rank9-miracle-reality2-source-conference-01/README.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_PACKET_129.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_NEXT_CONFERENCE_NOTES_129.json",
    ]
    current_files = {path: (ROOT / path).read_bytes() for path in current_paths if (ROOT / path).exists()}
    for number, art in returns.items():
        current_files[f"evidence/RETURN{number}_INDEPENDENT_AUDIT.json"] = art["auditPath"].read_bytes()
        current_files[f"evidence/RETURN{number}_RECEIPT.json"] = art["receiptPath"].read_bytes()
    evidence_files = {}
    for number, art in returns.items():
        evidence_files[f"evidence/RETURN{number}.zip"] = art["archivePath"].read_bytes()
        evidence_files[f"evidence/RETURN{number}_DELIVERY.json"] = art["deliveryPath"].read_bytes()

    files = {
        "CURRENT_CONTEXT_233.json": context_raw, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_233.json": candidate_raw,
        "REQUEST_233.txt": request_raw, "historical/DD_Rank9_Miracle_Reality_2_Source_Conference_01.zip": source_archive_raw,
        "historical/NEXT_CONFERENCE_NOTES_129.json": HIST_NOTES.read_bytes(), "historical/PACKET_129_SUBMISSION_RECORD.json": HIST_PACKET.read_bytes(),
        "historical/SOURCE_CONFERENCE_PREPARATION_01.json": HIST_PREP.read_bytes(), "historical/SOURCE_CONFERENCE_CHECK_01.json": HIST_CHECK.read_bytes(),
        "historical/SOURCE_CONFERENCE_REQUEST_01.txt": HIST_REQUEST.read_bytes(), "historical/SOURCE_CONFERENCE_MANIFEST_01.json": HIST_MANIFEST.read_bytes(),
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
        manifest = {"id": "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-MANIFEST-233", "sourceCommitBase": head, "sourceBranch": branch,
                    "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(rows) + 1 == len(set(archive.namelist()))
        for row in rows:
            raw = archive.read(row["path"])
            assert (len(raw), sha(raw), crc(raw)) == (row["bytes"], row["sha256"], row["crc32"])

    archive_info = info(archive_path)
    candidate_info, context_info, request_info = info(candidate_path, candidate_raw), info(context_path, context_raw), info(request_path, request_raw)
    delivery = {
        "id": "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-DELIVERY-233", "status": "PREPARED_UNAUDITED_UNSENT",
        "archive": archive_info, "members": len(rows) + 1, "manifestBindings": len(rows), "sourceCommitBase": head, "sourceBranch": branch,
        "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "accepted": False, "applied": False,
        "candidate": candidate_info, "context": context_info, "request": request_info,
        "historicalCandidate": info(ROOT / HIST_CANDIDATE), "historicalSourceArchive": info(HIST_ARCHIVE, source_archive_raw),
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT", "priorDirectorRuling": None},
        "sourceBindings": len(refreshed), "changedSourceBindings": changed, "originalQuestions": 24, "focusedAdditionalQuestions": 2,
        "requiredMainCases": 4, "futureRequirements": 8, "nativePlacements": native_placements, "preservedRecentHolds": return_records,
        "canonicalChanges": False, "applicationChanges": False, "conversation": CHAT,
    }
    delivery_raw = enc(delivery)
    delivery_path.write_bytes(delivery_raw)
    preparation_path = AUDIT / "RANK9MIRACLEREALITY2_SOURCE_PREPARATION_233.json"
    packet_path = AUDIT / "RANK9MIRACLEREALITY2_PACKET_233.json"
    preparation = {"id": "RANK9MIRACLEREALITY2-SOURCE-PREPARATION-233", "recordedAtUtc": now, "status": "PREPARED_UNAUDITED_UNSENT",
                   "sourceCommitBase": head, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": TARGETS,
                   "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "context": context_info,
                   "sourceBindings": len(refreshed), "changedHistoricalBindings": changed, "originalQuestions": 24, "focusedAdditionalQuestions": 2,
                   "requiredMainCases": 4, "futureCaseRequirements": 8, "nativePlacements": native_placements,
                   "historicalWorkflow": delivery["historicalWorkflow"], "priorReturns": return_records,
                   "canonicalChanges": False, "accepted": False, "applied": False}
    preparation_path.write_bytes(enc(preparation))
    packet = {"id": "RANK9MIRACLEREALITY2-PACKET-233", "revision": 2, "supersedesRevision": 1, "status": "PREPARED_UNAUDITED_UNSENT", "group": GROUP, "pendingIds": TARGETS,
              "sourceAuthority": AUTHORITY, "sourceBranch": branch, "sourceCommitBase": head, "archive": archive_info,
              "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "originalQuestions": 24,
              "focusedAdditionalQuestions": 2, "totalQuestions": 26, "requiredMainCases": 4, "futureCaseRequirements": 8,
              "nativePlacements": native_placements, "refreshedSourceBindings": len(refreshed), "changedHistoricalBindings": len(changed),
              "historicalWorkflow": delivery["historicalWorkflow"], "preservedRecentHolds": return_records,
              "canonicalChanges": False, "independentAudit": None}
    packet_path.write_bytes(enc(packet))

    queue_doc = read(queue233_path)
    preparation_info, delivery_info = info(preparation_path), info(delivery_path, delivery_raw)
    next_request = queue_doc["nextPreparedRequest"]
    next_request.update({"status": "PACKET233_PREPARED_UNAUDITED_UNSENT", "packet": archive_info, "deliveryManifest": delivery_info,
                         "candidate": candidate_info, "sourcePreparation": preparation_info})
    queue_doc["currentPacket"], queue_doc["currentDeliveryManifest"], queue_doc["currentPreparation"] = archive_info, delivery_info, preparation_info
    queue_doc["status"] = queue_doc["packetStatus"] = "PACKET233_PREPARED_UNAUDITED_811_37_0"
    queue233_path.write_bytes(enc(queue_doc))
    handoff_doc = read(handoff233_path)
    handoff_doc.update({"nextPreparedRequest": next_request, "currentPacket": archive_info, "currentPacketDelivery": delivery_info,
                        "currentPreparation": preparation_info, "currentQueueBinding": info(queue233_path),
                        "status": "PACKET233_PREPARED_UNAUDITED_811_37",
                        "resumePriority": "Independently audit Packet233 before sending it to GPT; monitor the browser frequently and ping if needed, audit the sealed return, then apply only exact accepted IDs."})
    handoff233_path.write_bytes(enc(handoff_doc))
    snapshot_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_233.md"
    snapshot_path.write_text(
        "# Current Ordinary Spell Review Snapshot 233\n\n"
        "Authority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return232 independently passed and held astral-projection and imprisonment. The next group is **Rank9 Miracle/Reality2**: divine-intervention-greater and wish. Their historical source conference was prepared but never sent, so no prior director ruling exists.\n\n"
        "Preserve all audited holds from Returns228–232 and all accepted/applied history. Packet233 refreshes 153 source bindings, carries 24 original questions, two focused additions, four required main cases and eight future requirements. No spell is accepted or applied by packet preparation.\n",
        encoding="utf-8")
    start_path = ROOT / "START_HERE.md"
    start_lines = start_path.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = "**Current ordinary spell-review handoff [233](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_233.json):** Return232 independently audited held astral-projection and imprisonment; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Fresh Packet233 for only divine-intervention-greater and wish is prepared for independent packet audit; their historical conference was prepared but never sent."
    start_path.write_text("\n".join(start_lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch, "authority": AUTHORITY,
                      "targets": TARGETS, "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "questions": 26,
                      "mainCases": 4, "futureRequirements": 8, "nativePlacements": native_placements, "members": len(rows) + 1,
                      "archiveBytes": archive_info["bytes"], "archiveSha256": archive_info["sha256"],
                      "deliveryManifestBytes": len(delivery_raw), "deliveryManifestSha256": sha(delivery_raw), "out": str(archive_path),
                      "priorReturns": {n: a["heldIds"] for n, a in returns.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
