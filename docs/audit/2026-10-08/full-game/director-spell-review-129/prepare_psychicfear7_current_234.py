#!/usr/bin/env python3
"""Prepare a fresh, current-authority director packet for Psychic/Fear 7."""
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
GROUP = "rank9-psychic-fear7"
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
HIST_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Psychic_Fear_7_Source_Conference_01.zip"
PACKET215 = AUDIT / "rank9_psychicfear7_source_packet_215/DD_Rank9_PsychicFear7_CurrentSource_215.zip"
PACKET215_DELIVERY = AUDIT / "rank9_psychicfear7_source_packet_215/DD_Rank9_PsychicFear7_CurrentSource_215_DELIVERY.json"
RETURN216_DIR = AUDIT / "rank9_psychicfear7_return216_received"
RETURN216 = RETURN216_DIR / "DD_Rank9_PsychicFear3_Director_Return216_HELD.zip"
RETURN216_DELIVERY = RETURN216_DIR / "DD_Rank9_PsychicFear3_Director_Return216_HELD_DELIVERY.json"
RETURN216_DECISION = RETURN216_DIR / "DIRECTOR_DECISION_216.json"
RETURN216_BLOCKERS = RETURN216_DIR / "BLOCKERS_216.json"
RETURN216_AUDIT = RETURN216_DIR / "RETURN216_INDEPENDENT_AUDIT.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

RETURN_INFO = {
    228: ("rank9_impactexile4_return228_received", "DD_Rank9_ImpactExile1_Director_Return228.zip", "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json", ["reverse-gravity-field"], ["IE204-B02"]),
    229: ("rank9_illusionreality5_return229_received", "DD_Rank9_IllusionReality1_Director_Return229.zip", "DD_Rank9_IllusionReality1_Director_Return229_DELIVERY.json", "RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json", "RANK9ILLUSIONREALITY5_RETURN229_RECEIPT.json", ["soul-reflection"], ["IR207-B02"]),
    230: ("rank9_materialforging2_return230_received", "DD_Rank9_MaterialForging2_Director_Return230.zip", "DD_Rank9_MaterialForging2_Director_Return230_DELIVERY.json", "RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT.json", "RANK9MATERIALFORGING2_RETURN230_RECEIPT.json", ["eternal-forge", "matter-conversion"], ["MF210-B01", "MF210-B02"]),
    231: ("rank9_alignment_faction_purification5_return231_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json", ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]),
    232: ("rank9_projectionconfinement2_return232_received", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json", ["astral-projection", "imprisonment"], ["PC232-B01", "PC232-B02"]),
    233: ("rank9_miraclereality2_return233_received", "DD_Rank9_MiracleReality2_Director_Return233_HELD.zip", "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json", "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json", "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json", ["divine-intervention-greater", "wish"], ["MR233-B01", "MR233-B02"]),
}

RETURN216_EXCERPT_MEMBERS = [
    "BLOCKERS.json", "CANDIDATE_BINDING_RECONCILIATION.json", "CLOCK_CHECK.json", "COUNTS.json",
    "CURRENT_AUTHORITY.json", "DIRECTOR_DECISION.json", "FORWARD_INVERSE_CHECK.json",
    "HOLD_REGISTER_CURRENT.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
    "PRESERVED_CASE_BINDINGS.json", "QUESTION_DISPOSITION_RECONCILIATION.json",
    "RETRIEVED_AUDIT_BINDINGS.json", "SOURCE_AND_PRIOR_PACKAGE_CHECK.json", "SOURCE_SEARCH_216.json",
    "preserved/ACTOR_PROFILES.json", "preserved/CASE_INDEX.json", "preserved/HOLD_REGISTER.json",
    "preserved/ORIGINAL_OBLIGATIONS.json", "preserved/PROCEDURES.json", "preserved/PROCEDURE_PROPOSALS.json",
    "preserved/QUESTION_DISPOSITIONS.json", "preserved/SOURCE_SEARCH_REVIEW.json", "preserved/STANDALONE_PROCEDURES.md",
]


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


def verify_return(number: int) -> dict:
    folder, archive_name, delivery_name, audit_name, receipt_name, held, blockers = RETURN_INFO[number]
    folder_path = AUDIT / folder
    archive = folder_path / archive_name
    delivery = folder_path / delivery_name
    audit = AUDIT / audit_name
    receipt = AUDIT / receipt_name
    audit_doc, delivery_doc = read(audit), read(delivery)
    if number == 233:
        assert audit_doc["status"] == "PASS" and audit_doc["failedChecks"] == 0
    else:
        assert audit_doc.get("status") == "PASS" and audit_doc.get("failedChecks", 0) == 0
    assert delivery_doc.get("accepted") is False and delivery_doc.get("applied") is False
    actual_held = delivery_doc.get("heldIds", delivery_doc.get("heldIds"))
    assert actual_held == held, (number, actual_held)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    return {"archivePath": archive, "deliveryPath": delivery, "auditPath": audit, "receiptPath": receipt,
            "archive": info(archive), "delivery": info(delivery), "audit": info(audit), "receipt": info(receipt),
            "heldIds": held, "blockerIds": blockers, "decisionId": delivery_doc.get("id", delivery_doc.get("return"))}


def main() -> None:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch
    now = datetime.now(timezone.utc).isoformat()
    index_path, catalog_path, access_path = ROOT / INDEX, ROOT / CATALOG, ROOT / ACCESS
    index, catalog = read(index_path), read(catalog_path)
    queue233_path, handoff233_path = AUDIT / "CURRENT_SPELL_QUEUE_233.json", AUDIT / "CURRENT_HANDOFF_233.json"
    pending233_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_233.json"
    q0, h0, p0 = read(queue233_path), read(handoff233_path), read(pending233_path)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    pending = sorted(row["id"] for row in index["entries"] if row.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending) == 37 and set(TARGETS) <= set(pending)
    queue_group = next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP)
    assert queue_group["pendingIds"] == TARGETS and queue_group["pendingCount"] == 3
    for spell_id in TARGETS:
        assert entries[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert entries[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert spells[spell_id]["id"] == spell_id

    old_candidate = read(ROOT / HIST_CANDIDATE)
    with zipfile.ZipFile(HIST_ARCHIVE) as historical:
        assert historical.testzip() is None
        refreshed, changed, source_files = [], [], {}
        for old in old_candidate["sourceBindings"]:
            path = old["path"]
            assert safe(path)
            old_bytes = historical.read("sources/" + path)
            assert (len(old_bytes), sha(old_bytes)) == (old["bytes"], old["sha256"]), path
            current_bytes = (ROOT / path).read_bytes()
            binding = {"path": path, "bytes": len(current_bytes), "sha256": sha(current_bytes), "crc32": crc(current_bytes), "gitBlobSHA1": git_blob_sha(current_bytes)}
            refreshed.append(binding)
            source_files["sources_current/" + path] = current_bytes
            if (len(current_bytes), sha(current_bytes)) != (old["bytes"], old["sha256"]):
                changed.append({"path": path, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"], "currentBytes": len(current_bytes), "currentSha256": sha(current_bytes)})
    assert len(refreshed) == len(source_files) == len(old_candidate["sourceBindings"]) == 84

    returns = {n: verify_return(n) for n in RETURN_INFO}
    held_history = [{"returnNumber": n, "archive": a["archive"], "delivery": a["delivery"], "independentAudit": a["audit"], "receipt": a["receipt"], "heldIds": a["heldIds"], "blockerIds": a["blockerIds"]} for n, a in returns.items()]
    return233 = returns[233]
    previous_blockers = read(RETURN216_BLOCKERS)
    previous_decision = read(RETURN216_DECISION)
    previous_delivery = read(RETURN216_DELIVERY)
    previous_audit = read(RETURN216_AUDIT)
    assert previous_decision["authorityUnchanged"]["reviewedApplied"] == 806
    assert previous_decision["heldIds"] == TARGETS
    assert previous_audit.get("passed") is True

    with zipfile.ZipFile(RETURN216) as previous_zip:
        assert previous_zip.testzip() is None
        original_obligations = json.loads(previous_zip.read("preserved/ORIGINAL_OBLIGATIONS.json"))
        prior_question_dispositions = json.loads(previous_zip.read("preserved/QUESTION_DISPOSITIONS.json"))
        case_index = json.loads(previous_zip.read("preserved/CASE_INDEX.json"))
        excerpt_rows, excerpt_files = [], {}
        for name in RETURN216_EXCERPT_MEMBERS:
            raw = previous_zip.read(name)
            excerpt_files["evidence/return216_excerpt/" + name] = raw
            excerpt_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        return216_delivery = read(RETURN216_DELIVERY)
        excerpt_manifest = {"id": "RETURN216-REVIEW-EXCERPT-MANIFEST", "originalArchive": {"fileName": RETURN216.name, "bytes": len(RETURN216.read_bytes()), "sha256": sha(RETURN216.read_bytes()), "crc32": crc(RETURN216.read_bytes())},
                           "membersCopiedByteExactFromOriginalArchive": excerpt_rows,
                           "excludedRedundantMember": "prior/Return183.zip (70,580,152 bytes; remains represented by the bound original Return216 archive; Return216 includes the selected current 47-case evidence, procedures, questions, blockers and replay trace in the copied members)."}
        excerpt_files["evidence/return216_excerpt/EXCERPT_MANIFEST.json"] = enc(excerpt_manifest)

    target_records = [copy.deepcopy(next(r for r in old_candidate["records"] if r["spellId"] == sid)) for sid in TARGETS]
    for record in target_records:
        sid = record["spellId"]
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(spells[sid])
        record["currentAuthorityDisposition"] = "Still pending and requires fresh director review at 811/37/0; prior 806/42/0 blockers are historical evidence, not an automatic current ruling."
    target_set = set(TARGETS)
    scoped_questions = [copy.deepcopy(q) for q in old_candidate["questions"] if target_set.intersection(q.get("spellIds", []))]
    original_obligations_for_targets = [copy.deepcopy(x) for x in original_obligations["requiredMainCasesUnchanged"] if x.get("spellId") in target_set]
    future_for_targets = copy.deepcopy(original_obligations["futureRequirementsUnchanged"])
    selected_prior_dispositions = [copy.deepcopy(x) for x in prior_question_dispositions if target_set.intersection(x.get("spellIds", []))]
    assert len(old_candidate["questions"]) == 23 and len(scoped_questions) == 13
    assert len(original_obligations["focusedAdditionalQuestionsUnchanged"]) == 2 and len(selected_prior_dispositions) == 15

    # Record Return233 as the completed prior batch and give the director's
    # explicitly selected group an exact current-authority queue handoff.
    preserved_holds = copy.deepcopy(p0.get("preservedRecentHolds", []))
    preserved_holds.append({"heldIds": return233["heldIds"], "blockerIds": return233["blockerIds"], "archive": return233["archive"], "audit": return233["audit"], "receipt": return233["receipt"]})
    latest233 = {"group": "rank9-miracle-reality2", "acceptedIds": [], "appliedIds": [], "heldIds": return233["heldIds"],
                 "blockerIds": dict(zip(return233["heldIds"], [["MR233-B01"], ["MR233-B02"]])), "returnArchive": return233["archive"],
                 "returnDelivery": return233["delivery"], "independentAudit": return233["audit"], "receipt": return233["receipt"]}

    pending234 = copy.deepcopy(p0)
    pending234.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-234", "recordedAtUtc": now,
                       "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN233",
                       "authority": AUTHORITY, "indexBinding": info(index_path), "catalogBinding": info(catalog_path),
                       "pendingCount": len(pending), "pendingIds": pending, "preservedRecentHolds": preserved_holds,
                       "lastDirectorReturn": {"archive": return233["archive"], "deliveryManifest": return233["delivery"], "independentAudit": return233["audit"], "receipt": return233["receipt"], "acceptedIds": [], "appliedIds": [], "heldIds": return233["heldIds"], "blockerIds": ["MR233-B01", "MR233-B02"]},
                       "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": len(TARGETS), "status": "DIRECTOR_PRIORITY_CONFIRMED_PACKET234_PREPARATION_IN_PROGRESS", "freshPacketRequiredForCurrentAuthority": True, "directorPriority": "GPT confirmed rank9-psychic-fear7 for Packet234.", "priorReturn216BlockersForReassessment": ["PF182-B01", "PF182-B02"]}})
    pending234_path = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_234.json"
    pending234_path.write_bytes(enc(pending234))

    queue234 = copy.deepcopy(q0)
    queue234.update({"id": "SPELL-REVIEW-QUEUE-234", "recordedAtUtc": now, "supersedesQueue": "SPELL-REVIEW-QUEUE-233", "parentQueue": info(queue233_path),
                     "currentAuthority": AUTHORITY, "pendingIdentityAudit": info(pending234_path), "currentReturnAudit": return233["audit"],
                     "currentReturnDelivery": return233["delivery"], "currentReturnArchive": return233["archive"], "currentReturnReceipt": return233["receipt"],
                     "currentReturnDecision": "RANK9-MIRACLE-REALITY2-DIRECTOR-RETURN233-DELIVERY", "currentReturnBinding": return233["archive"],
                     "currentPacketAudit": return233["audit"], "currentPacketAuditReceipt": return233["receipt"],
                     "packetStatus": "RETURN233_AUDITED_HELD_811_37_0", "status": "RETURN233_AUDITED_HELD_811_37_0", "githubChanges": False,
                     "nextGroup": GROUP, "next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3, "status": "FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True},
                     "lastReviewedBatch": latest233,
                     "nextPreparedRequest": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3, "status": "PACKET234_PREPARATION_IN_PROGRESS", "freshPacketRequiredForCurrentAuthority": True,
                                             "historicalPhaseCorrection": "Queue233's historicalPhase label is stale: Packet215 was submitted and Return216 held all three targets at 806/42/0; current packet234 is a fresh 811/37/0 reassessment.",
                                             "preservedOriginalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditionalQuestions": 2,
                                             "priorSelectedQuestionDispositions": len(selected_prior_dispositions), "priorTargetMainObligations": len(original_obligations_for_targets),
                                             "priorPreservedCaseCount": previous_decision["counts"]["preservedCases"], "priorHeldCases": previous_decision["counts"]["heldCases"],
                                             "previousHeldBatches": preserved_holds, "priorReturn216BlockerIds": ["PF182-B01", "PF182-B02"], "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None}})
    row = next(x for x in queue234["currentPendingGroups"] if x["group"] == GROUP)
    row.update({"historicalPhase": "prior-director-return-216-held", "status": "FRESH_PACKET234_PREPARATION_IN_PROGRESS_811_37_0", "freshPacketRequiredForCurrentAuthority": True,
                "currentAuthority": AUTHORITY, "previousHeldBatch": {"ids": TARGETS, "blockers": ["PF182-B01", "PF182-B02"], "acceptedIds": [], "appliedIds": []},
                "historicalPhaseCorrection": "Packet215 was submitted and Return216 held these targets at 806/42/0; this is a fresh current-authority review.",
                "directorPriority": "GPT confirmed this group for Packet234."})
    queue234_path = AUDIT / "CURRENT_SPELL_QUEUE_234.json"
    queue234_path.write_bytes(enc(queue234))

    handoff234 = copy.deepcopy(h0)
    handoff234.update({"id": "CURRENT-HANDOFF-234", "recordedAtUtc": now, "status": "RETURN233_AUDITED_HELD_PACKET234_PREPARATION_811_37",
                       "currentAuthority": AUTHORITY, "pendingIdentityAudit": info(pending234_path), "queue": info(queue234_path), "currentQueueBinding": info(queue234_path),
                       "currentReturnBinding": return233["archive"], "currentReturnArchive": return233["archive"], "currentReturnDelivery": return233["delivery"],
                       "currentReturnAudit": return233["audit"], "currentReturnReceipt": return233["receipt"], "currentReturnDecision": "RANK9-MIRACLE-REALITY2-DIRECTOR-RETURN233-DELIVERY",
                       "latestBatch": latest233, "nextGroup": GROUP, "nextPendingCount": 3, "currentPreparation": None, "currentPacket": None,
                       "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
                       "nextStep": "Independently audit fresh Packet234 for psychic-scream, mass-phantom-killer and weird; send it to GPT, read the browser frequently and ping as needed; audit its sealed decision and apply only exact accepted identities.",
                       "nextPreparedRequest": queue234["nextPreparedRequest"], "githubChanges": False,
                       "resumePriority": "GPT selected rank9-psychic-fear7 for Packet234. Reassess only the three pending identities at 811/37/0, preserve all completed/accepted identities and prior evidence, and do not apply unless the sealed director decision explicitly accepts an identity."})
    handoff234_path = AUDIT / "CURRENT_HANDOFF_234.json"
    handoff234_path.write_bytes(enc(handoff234))

    current_target_records = []
    for sid in TARGETS:
        current_target_records.append({"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]), "currentCatalogCard": copy.deepcopy(spells[sid]), "status": "pending-authored-procedure at current 811/37/0 authority"})
    candidate = {"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-234", "recordedAtUtc": now, "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_PSYCHIC_FEAR7_GROUP",
                 "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True, "currentAuthority": AUTHORITY,
                 "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 3}, "targetRecords": target_records, "currentTargets": current_target_records,
                 "originalQuestionsUnchanged": copy.deepcopy(old_candidate["questions"]), "targetRelevantOriginalQuestionIds": [x["id"] for x in scoped_questions],
                 "focusedAdditionalQuestionsUnchanged": copy.deepcopy(original_obligations["focusedAdditionalQuestionsUnchanged"]),
                 "priorSelectedQuestionDispositions": selected_prior_dispositions,
                 "priorTargetMainCaseObligations": original_obligations_for_targets, "priorTargetFutureRequirements": future_for_targets,
                 "priorReturn216CaseIndex": case_index, "priorBlockersForFreshReassessment": previous_blockers,
                 "priorDirectorDecision216": previous_decision, "priorReturn216Counts": previous_decision["counts"],
                 "priorHeldCaseIds": previous_decision.get("blockers", []), "currentAuthorityEvidence": {"index": info(index_path), "catalog": info(catalog_path), "accessRegistry": info(access_path),
                     "queue": info(queue234_path), "handoff": info(handoff234_path), "pendingIdentityAudit": info(pending234_path), "latestReturn233Audit": return233["audit"]},
                 "historicalSourceCandidate": info(ROOT / HIST_CANDIDATE), "historicalSourceArchive": info(HIST_ARCHIVE), "priorPacket215": info(PACKET215), "priorReturn216": info(RETURN216),
                 "sourceBindings": refreshed, "sourceBindingRefresh": {"count": len(refreshed), "changedHistoricalBindings": changed, "sourceBytesFromCurrentWorkingTree": True},
                 "preservedRecentHolds": held_history, "closedAndCompletedIdentitiesOutOfScope": True, "newRuleAdoptions": 0}
    candidate_raw = enc(candidate)

    context = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-DIRECTOR-CONTEXT-234", "recordedAtUtc": now, "sourceCommitBase": head, "sourceBranch": branch,
               "currentWorkingTreeSnapshot": True, "currentAuthority": AUTHORITY, "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 3},
               "pendingIdentityAudit": info(pending234_path), "currentQueue": info(queue234_path), "currentHandoff": info(handoff234_path),
               "historicalPhaseCorrection": "Packet215 was sent and Return216 held the three targets at 806/42/0; queue233's earlier prepared-unsent label is stale.",
               "priorReturn216Blockers": ["PF182-B01", "PF182-B02"], "priorBlockerStatus": "historical; re-evaluate against current source and witness data, do not carry forward automatically",
               "refreshedSourceBindings": len(refreshed), "changedHistoricalSourceBindings": changed,
               "preservation": {"originalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditions": 2, "previousSelectedDispositions": len(selected_prior_dispositions),
                                "previousTargetMainObligations": len(original_obligations_for_targets), "previousCaseCount": previous_decision["counts"]["preservedCases"],
                                "previousHeldCases": previous_decision["counts"]["heldCases"], "targetIdentities": 3, "newRuleAdoptions": 0},
               "directorPriority": "GPT confirmed rank9-psychic-fear7 for Packet234.", "latestReturn233Audit": return233["audit"], "preservedRecentHolds": held_history,
               "canonicalChanges": False, "runtimeExecuted": False, "applicationChanges": False}
    context_raw = enc(context)

    request = (
        f"GPT director — continue the ordinary spell review at authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). You selected {GROUP} for Packet234. Review ONLY psychic-scream, mass-phantom-killer and weird.\n\n"
        f"This current packet is based on main HEAD {head} plus current working-tree source bytes and refreshes all {len(refreshed)} source bindings from the historical conference. The three exact targets remain pending at 811/37/0. Packet215 and Return216 show a historical 806/42/0 review; its PF182-B01/B02 blockers are evidence to reassess, not automatic current decisions. The earlier queue row's 'prepared-unsent' label is stale: Packet215 was submitted and Return216 was sealed.\n\n"
        "Reconcile the present index, catalog, current accepted-interface registry, source archive and exact class/school access for only these three spells. Preserve the 23 original questions, two focused addenda, 15 previously selected target-relevant question dispositions, six target main obligations, and the 47 previously preserved cases including their 43 complete conditional cases. Revisit only the four previously held case obligations and any directly dependent questions. Preserve source-grounded complete cases and all unrelated accepted/applied identities. Keep each old accepted procedure separate from the current pending status.\n\n"
        "For each exact target, reassess whether current source records and actual state witnesses now satisfy every previous blocker. Do not infer anatomy, extra full turns, time sources, nightmare custody, head counts, body forms or actor schedules from names or summaries. Distinguish each class/school route, native placement, damage, fear/stun, sleep, illusion, body state, resistance, death and source clock. If evidence closes a blocker, identify the exact current source facts and complete required positive witness; if it remains held, give the exact blocker and minimum missing source witness. Do not convert missing facts into failed branches or invent a universal timing/cap/cost/rule. No D&D imports or new rules.\n\n"
        "Preserve recent audited holds unchanged: Return233 divine-intervention-greater/wish (MR233-B01/B02, packet-reference finding closed); Return232 astral-projection/imprisonment (PC232-B01/B02); Return231 five alignment/faction holds (AFP211-B01..B05; AFP211-E01 closed); Return230 eternal-forge/matter-conversion (MF210-B01/B02); Return229 soul-reflection (IR207-B02); Return228 reverse-gravity-field (IE204-B02). Matching delivery manifests, independent audits, receipts and archives are included. Return216's selected decision, blockers, current case index/replay, procedures, obligations, questions and related findings are included as an exact-member excerpt bound to the original archive; only its redundant nested Return183 ZIP is omitted.\n\n"
        "Return an explicit accepted/applied/held decision per target, blocker and conditional-boundary IDs, source-qualified minimum witness, question dispositions, current-source checks, replay/check totals and forward/inverse counts. Separate audit replay from complete positive spell and actor-clock evidence. Keep authority at 811/37/0 and the three pending identities unchanged unless a complete sealed decision authorizes acceptance. Do not edit canonical/runtime/GitHub files, apply a spell, run supplied programs or game runtime, or open implementation, human-play, balance, cosmology, domain-closure, completion or release gates. Seal the decision ZIP with its exact matching DELIVERY.json, state the next pending group, and continue through response caps until both files are attached."
    )

    out = AUDIT / "rank9_psychicfear7_current_source_234_prepared"
    out.mkdir(parents=True, exist_ok=True)
    candidate_path = out / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_234.json"
    context_path = out / "CURRENT_CONTEXT_234.json"
    request_path = out / "REQUEST_234.txt"
    archive_path = out / "DD_Rank9_PsychicFear7_CurrentSource_234.zip"
    delivery_path = out / "DD_Rank9_PsychicFear7_CurrentSource_234_DELIVERY.json"
    candidate_path.write_bytes(candidate_raw)
    context_path.write_bytes(context_raw)
    request_raw = request.encode("utf-8")
    request_path.write_bytes(request_raw)

    prior_packet_manifest = read(PACKET215_DELIVERY)
    for art in returns.values():
        pass
    current_paths = [
        "START_HERE.md", INDEX, CATALOG, ACCESS,
        "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_234.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_234.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_234.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_233.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_PACKET_233_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/verify_miraclereality2_return233_independent.py",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PSYCHICFEAR7_GPT_RETURN_182.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PSYCHICFEAR7_RETURN214_REQUEST.txt",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PSYCHICFEAR7_NEXT_CONFERENCE_NOTES_129.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PSYCHICFEAR7_NEXT_CONFERENCE_NOTES_180.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PSYCHICFEAR7_PACKET_129.json",
    ]
    current_files = {path: (ROOT / path).read_bytes() for path in current_paths if (ROOT / path).exists()}
    for number, art in returns.items():
        current_files[f"evidence/RETURN{number}_INDEPENDENT_AUDIT.json"] = art["auditPath"].read_bytes()
        current_files[f"evidence/RETURN{number}_RECEIPT.json"] = art["receiptPath"].read_bytes()

    evidence_files = {"evidence/PACKET215.zip": PACKET215.read_bytes(), "evidence/PACKET215_DELIVERY.json": PACKET215_DELIVERY.read_bytes(),
                      "evidence/RETURN216_DELIVERY.json": RETURN216_DELIVERY.read_bytes(), "evidence/RETURN216_DECISION.json": RETURN216_DECISION.read_bytes(),
                      "evidence/RETURN216_BLOCKERS.json": RETURN216_BLOCKERS.read_bytes(), "evidence/RETURN216_INDEPENDENT_AUDIT.json": RETURN216_AUDIT.read_bytes(),
                      "evidence/PSYCHIC_FEAR_SOURCE_CONFERENCE_01.zip": HIST_ARCHIVE.read_bytes(), "evidence/PSYCHIC_FEAR_SOURCE_CANDIDATE_01.json": (ROOT / HIST_CANDIDATE).read_bytes()}
    evidence_files.update({"evidence/RETURN" + str(n) + ".zip": art["archivePath"].read_bytes() for n, art in returns.items()})
    evidence_files.update({"evidence/RETURN" + str(n) + "_DELIVERY.json": art["deliveryPath"].read_bytes() for n, art in returns.items()})
    files = {"CURRENT_CONTEXT_234.json": context_raw, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_234.json": candidate_raw, "REQUEST_234.txt": request_raw,
             "historical/SOURCE_CANDIDATE_01.json": (ROOT / HIST_CANDIDATE).read_bytes(), "historical/SOURCE_CONFERENCE_01.zip": HIST_ARCHIVE.read_bytes(),
             "historical/PACKET215_DELIVERY.json": PACKET215_DELIVERY.read_bytes(), "evidence/return216_excerpt/DELIVERY.json": RETURN216_DELIVERY.read_bytes(),
             "evidence/return216_excerpt/DIRECTOR_DECISION_216.json": RETURN216_DECISION.read_bytes(), "evidence/return216_excerpt/BLOCKERS_216.json": RETURN216_BLOCKERS.read_bytes(),
             "evidence/return216_excerpt/INDEPENDENT_AUDIT.json": RETURN216_AUDIT.read_bytes(), "evidence/return216_excerpt/EXCERPT_MANIFEST.json": enc(excerpt_manifest)}
    files.update({"current/" + path: raw for path, raw in current_files.items()})
    files.update(source_files)
    files.update(excerpt_files)
    files.update(evidence_files)
    assert all(safe(name) for name in files)

    rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        manifest = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-SOURCE-MANIFEST-234", "sourceCommitBase": head, "sourceBranch": branch,
                    "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(rows) + 1 == len(set(archive.namelist()))
        for row in rows:
            raw = archive.read(row["path"])
            assert (len(raw), sha(raw), crc(raw)) == (row["bytes"], row["sha256"], row["crc32"])

    archive_raw = archive_path.read_bytes()
    archive_info = info(archive_path, archive_raw)
    candidate_info, context_info = info(candidate_path, candidate_raw), info(context_path, context_raw)
    request_info = info(request_path, request_raw)
    delivery = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-SOURCE-DELIVERY-234", "status": "PREPARED_UNAUDITED_UNSENT", "archive": archive_info,
                "memberCount": len(rows) + 1, "payloadCount": len(rows), "members": [{"path": "MANIFEST.json", **({"bytes": len(enc(manifest)), "sha256": sha(enc(manifest)), "crc32": crc(enc(manifest))})}] + rows,
                "memberManifest": {"path": "MANIFEST.json", "bytes": len(enc(manifest)), "sha256": sha(enc(manifest)), "crc32": crc(enc(manifest))},
                "sourceCommitBase": head, "sourceBranch": branch, "authority": AUTHORITY, "group": GROUP, "targetIds": TARGETS, "accepted": False, "applied": False,
                "candidate": candidate_info, "context": context_info, "request": request_info, "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
                "originalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditionalQuestions": 2,
                "priorSelectedQuestionDispositions": len(selected_prior_dispositions), "priorTargetMainObligations": len(original_obligations_for_targets),
                "priorPreservedCases": previous_decision["counts"]["preservedCases"], "priorHeldCases": previous_decision["counts"]["heldCases"],
                "preservedRecentHolds": held_history, "priorPacket215": {"archive": info(PACKET215), "delivery": info(PACKET215_DELIVERY)},
                "priorReturn216": {"archive": info(RETURN216), "delivery": info(RETURN216_DELIVERY), "audit": info(RETURN216_AUDIT), "excerptManifest": excerpt_manifest},
                "canonicalChanges": False, "applicationChanges": False, "runtimeExecuted": False, "githubChanges": False, "conversation": CHAT}
    delivery_raw = enc(delivery)
    delivery_path.write_bytes(delivery_raw)
    prep_path = AUDIT / "RANK9PSYCHICFEAR7_SOURCE_PREPARATION_234.json"
    packet_path = AUDIT / "RANK9PSYCHICFEAR7_PACKET_234.json"
    prep = {"id": "RANK9PSYCHICFEAR7-SOURCE-PREPARATION-234", "recordedAtUtc": now, "status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head,
            "sourceBranch": branch, "authority": AUTHORITY, "group": GROUP, "targetIds": TARGETS, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw),
            "candidate": candidate_info, "context": context_info, "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
            "originalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditionalQuestions": 2,
            "priorSelectedQuestionDispositions": len(selected_prior_dispositions), "priorTargetMainObligations": len(original_obligations_for_targets),
            "priorPreservedCases": previous_decision["counts"]["preservedCases"], "priorHeldCases": previous_decision["counts"]["heldCases"],
            "priorReturns": held_history, "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path.write_bytes(enc(prep))
    packet = {"id": "RANK9PSYCHICFEAR7-PACKET-234", "status": "PREPARED_UNAUDITED_UNSENT", "group": GROUP, "targetIds": TARGETS, "authority": AUTHORITY,
              "sourceBranch": branch, "sourceCommitBase": head, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw),
              "candidate": candidate_info, "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed),
              "originalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditionalQuestions": 2,
              "priorSelectedQuestionDispositions": len(selected_prior_dispositions), "priorTargetMainObligations": len(original_obligations_for_targets),
              "priorPreservedCases": previous_decision["counts"]["preservedCases"], "priorHeldCases": previous_decision["counts"]["heldCases"],
              "historicalPhaseCorrection": "Packet215 was submitted and Return216 held the targets at 806/42/0; this is a fresh 811/37/0 reassessment.",
              "preservedRecentHolds": held_history, "independentAudit": None, "canonicalChanges": False}
    packet_path.write_bytes(enc(packet))

    queue_doc = read(queue234_path)
    prep_info = info(prep_path)
    delivery_info = info(delivery_path, delivery_raw)
    next_request = queue_doc["nextPreparedRequest"]
    next_request.update({"status": "PACKET234_PREPARED_UNAUDITED_UNSENT", "packet": archive_info, "deliveryManifest": delivery_info, "candidate": candidate_info, "sourcePreparation": prep_info})
    queue_doc.update({"currentPacket": archive_info, "currentDeliveryManifest": delivery_info, "currentPreparation": prep_info,
                      "status": "PACKET234_PREPARED_UNAUDITED_811_37_0", "packetStatus": "PACKET234_PREPARED_UNAUDITED_811_37_0"})
    queue234_path.write_bytes(enc(queue_doc))
    handoff_doc = read(handoff234_path)
    handoff_doc.update({"nextPreparedRequest": next_request, "currentPacket": archive_info, "currentPacketDelivery": delivery_info, "currentPreparation": prep_info,
                        "currentQueueBinding": info(queue234_path), "status": "PACKET234_PREPARED_UNAUDITED_811_37",
                        "resumePriority": "Independently audit Packet234; send it to GPT, keep reading the browser and ping again if progress stalls, audit the sealed decision, and apply only explicit accepted IDs."})
    handoff234_path.write_bytes(enc(handoff_doc))

    snapshot_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_234.md"
    snapshot_path.write_text("# Current Ordinary Spell Review Snapshot 234\n\n"
        "Authority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return233 independently passed 30 checks and held divine-intervention-greater and wish. GPT selected **Rank9 Psychic/Fear7** for the next review: psychic-scream, mass-phantom-killer and weird. Packet234 refreshes 84 historical source bindings and preserves the previous Return216 case and question evidence while reassessing its 806/42/0 holds against current source at 811/37/0.\n\n"
        "The queue233 historicalPhase label is stale: Packet215 was submitted and Return216 held all three targets. No completed identity is reopened. Packet234 is prepared for independent audit before upload; no spell is accepted or applied by preparation.\n", encoding="utf-8")
    start_path = ROOT / "START_HERE.md"
    start_lines = start_path.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = "**Current ordinary spell-review handoff [234](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_234.json):** Return233 independently audited and held divine-intervention-greater and wish; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. GPT selected psychic-scream, mass-phantom-killer and weird for fresh Packet234, now prepared for independent audit."
    start_path.write_text("\n".join(start_lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch, "authority": AUTHORITY,
                      "targets": TARGETS, "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed),
                      "originalQuestions": 23, "targetRelevantOriginalQuestions": len(scoped_questions), "focusedAdditions": 2,
                      "priorSelectedQuestionDispositions": len(selected_prior_dispositions), "priorTargetMainObligations": len(original_obligations_for_targets),
                      "priorPreservedCases": previous_decision["counts"]["preservedCases"], "priorHeldCases": previous_decision["counts"]["heldCases"],
                      "members": len(rows) + 1, "archiveBytes": archive_info["bytes"], "archiveSha256": archive_info["sha256"],
                      "deliveryBytes": len(delivery_raw), "deliverySha256": sha(delivery_raw), "out": str(archive_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
