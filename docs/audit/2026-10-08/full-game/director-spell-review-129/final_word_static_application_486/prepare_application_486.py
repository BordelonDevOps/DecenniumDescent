import copy
import hashlib
import json
import subprocess
import zlib
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:\Users\cbord\AppData\Local\Temp\dd-main-r03-push-20261102")
STAGE = Path(r"C:\Users\cbord\AppData\Local\Temp\dd-fw486-application\stage")
BASE_SHA = "7bbb2c18ab1ebfb8c5f82f24645394f936cac3c8"
BASE = "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PROC = f"{BASE}/rank9_deathrecovery7_return217_received/extracted/procedures/final-word.json"
ROOT = f"{BASE}/final_word_testonly_fixture_proposal_485"
PROPOSAL = f"{ROOT}/FINAL_WORD_FW485_TESTONLY_FIXTURE_PROPOSAL_REPACK01.json"
READY = f"{ROOT}/DIRECTOR_READBACK_FINAL_WORD_FW485_READY_01.json"
ROUTE = f"{ROOT}/DIRECTOR_READBACK_FINAL_WORD_TESTONLY_ROUTE_484_01.json"
OWNER = f"{ROOT}/OWNER_ADOPTION_FW485_TESTONLY.json"
WITNESS = f"{ROOT}/FW485_R1_TESTONLY_WITNESS_01.json"
Q477 = f"{BASE}/CURRENT_SPELL_QUEUE_477_REPACK01.json"
P477 = f"{BASE}/CURRENT16_PENDING_IDENTITY_AUDIT_477_REPACK01.json"
H477 = f"{BASE}/CURRENT_HANDOFF_477_REPACK01.json"
APP = f"{BASE}/final_word_static_application_486"
REC = f"{BASE}/final_word_identity_reconciliation_486"
CAND = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9finalword_static_reviewed_486"
Q478 = f"{BASE}/CURRENT_SPELL_QUEUE_478.json"
P478 = f"{BASE}/CURRENT15_PENDING_IDENTITY_AUDIT_478.json"
H478 = f"{BASE}/CURRENT_HANDOFF_478.json"
STAMP = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
HOLDS = ["DR217-H-SOURCE", "DR217-H-RUNTIME", "DR217-H-BALANCE", "DR217-H-COSMOLOGY", "DR217-H-RELEASE"]


def git_bytes(path):
    return subprocess.check_output(["git", "show", f"{BASE_SHA}:{path}"], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bind(path, data=None):
    data = git_bytes(path) if data is None else data
    return {"path": path, "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}"}


def load(path):
    return json.loads(git_bytes(path))


def write(path, data):
    target = STAGE / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return data


def write_json(path, obj):
    return write(path, (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def staged(path):
    return bind(path, (STAGE / path).read_bytes())


remote = subprocess.check_output(["git", "ls-remote", "origin", "refs/heads/main"], cwd=REPO, text=True).strip().split()
assert remote and remote[0] == BASE_SHA, f"remote main moved: {remote}"
index_raw, catalog_raw = git_bytes(INDEX), git_bytes(CATALOG)
before, catalog = json.loads(index_raw), json.loads(catalog_raw)
proc, proposal, owner = load(PROC), load(PROPOSAL), load(OWNER)
queue0, pending0, handoff0 = load(Q477), load(P477), load(H477)
oldrow = copy.deepcopy(next(x for x in before["entries"] if x["id"] == "final-word"))
native = copy.deepcopy(next(x for x in catalog["spells"] if x["id"] == "final-word"))
proposal_b, ready_b, route_b = bind(PROPOSAL), bind(READY), bind(ROUTE)
owner_b, witness_b, proc_b = bind(OWNER), bind(WITNESS), bind(PROC)
assert proposal_b["sha256"] == "20a49fe2e413498c64df3d5a87b6503d77326270d038cb797af69ad0722be462"
assert owner_b["sha256"] == "8fb3fa5ef67d8afb2dd0464a176f2116434473d6affb7212a0c0ee83b30761c8"
assert witness_b["sha256"] == "9677561e5d2f3f3854fddff831f13fca4239242a7e1d060c4ff98cc0c06caca8"
assert ready_b["bytes"] == 5756 and ready_b["sha256"] == "d087535ae75358066929034df6baf347fa3fcaaa544b7a732a0b6e8d47e528e8"
assert owner["scope"]["directorReadinessSha256"] == "cadc3f30e8b473ee6b70a3e24229607e679d1471c201593926f527d5c89e1ff2"
assert owner["scope"]["directorReadinessSha256"] != ready_b["sha256"]
assert before["authoredCounts"] == {"reviewed": 832, "pending": 16}
assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == 556
assert native["operational"] is None and native["status"] == "blocked-pending-operational-review"
assert oldrow["authoredStatus"] == "pending-authored-procedure"
assert queue0["currentAuthority"]["reviewedApplied"] == 832 and queue0["currentAuthority"]["pending"] == 16

decision = {
    "decisionId": "DR217-B01-FW485-STATIC-ACCEPT-01",
    "identity": "final-word",
    "decision": "ACCEPT",
    "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "acceptedIds": ["final-word"],
    "appliedIds": [],
    "heldIds": [],
    "closedBlockersWithinScope": ["DR217-B01"],
    "retainedQualifications": HOLDS,
}

erratum_path = f"{APP}/OWNER_ADOPTION_RECEIPT_BINDING_ERRATUM_486.json"
erratum = {
    "schemaVersion": 1,
    "id": "OWNER-ADOPTION-FW485-READINESS-RECEIPT-BINDING-ERRATUM-486",
    "recordedAtUtc": STAMP,
    "classification": "NONBLOCKING_RECEIPT_REFERENCE_ERRATUM_ORIGINAL_ADOPTION_PRESERVED",
    "source": "GPT Director response in Calibration review part 6",
    "ownerAdoption": owner_b,
    "field": "/scope/directorReadinessSha256",
    "recordedValue": owner["scope"]["directorReadinessSha256"],
    "correctValue": ready_b["sha256"],
    "correctReceipt": ready_b,
    "correction": "The original owner-adoption bytes are preserved. The Director confirmed this is not an LF/CRLF difference and directed a separate correction record. The exact adopted proposal and witness are independently established; no new adoption, reconstruction or replay is required.",
    "effects": {"adoptionScopeChanged": False, "proposalBindingChanged": False, "witnessBindingChanged": False, "newAdoptionRequired": False, "identityDecisionChanged": False, "queueChanged": False},
}
write_json(erratum_path, erratum)
erratum_b = staged(erratum_path)

readback_path = f"{APP}/DIRECTOR_READBACK_486.json"
readback = {
    "schemaVersion": 1,
    "id": "DIRECTOR-READBACK-FINAL-WORD-FW485-STATIC-ACCEPT-486",
    "recordedAtUtc": STAMP,
    "source": {"service": "GPT Director", "conversationTitle": "Calibration review part 6", "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
    "classification": "DIRECTOR_WITNESS_PASS_AND_STATIC_IDENTITY_ACCEPTANCE_READBACK_NOT_APPLICATION",
    "reviewedCommit": BASE_SHA,
    "witnessDisposition": "PASS",
    "identityDisposition": decision,
    "evidenceBindings": {"proposal": proposal_b, "ownerAdoption": owner_b, "witness": witness_b, "directorReadinessReceipt": ready_b, "routeRuling": route_b, "retainedProcedure": proc_b},
    "verification": {"eventGroups": 8, "snapshots": 8, "forwardOperations": 38, "inverseOperations": 38, "allIntermediateStateHashesVerified": True, "exactRestoration": True, "textSourceBindingsVerified": 15, "preservedArchiveLfsPointerMatches": True, "historicalCasesReplayed": False},
    "semanticFindings": {
        "castingBookkeeping": "Both casts correctly maintain family history, Refrain, magicThisTurn and pending-cast state.",
        "ArcaneWard": "Inherited force Arcane Ward remains unchanged; Spell Efficiency is not acquired.",
        "deathAndCapture": "Final Word causes direct death while retaining normal-HP ledger 49, followed by capture.",
        "reserveAndFalseLife": "False Life consumes the reserve once: 2 RP paid, 3 forfeited; caster remains at RP42 and gains 5 temporary HP.",
        "bodyAndEquipmentCustody": "Body and equipment custody remain unchanged.",
        "inverseBoundary": "Inverse restoration is audit-only, not gameplay resurrection or refund.",
    },
    "receiptBindingErratum": erratum_b,
    "decisionAccountingBeforeApplication": {"reviewedApplied": 832, "pending": 15, "acceptedUnapplied": 1, "committedQueueUnchanged": {"reviewedApplied": 832, "pending": 16, "acceptedUnapplied": 0}},
    "limits": {"identityScope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "actualSourceQualificationGranted": False, "campaignClaim": False, "runtimeOrCanonPromotion": False, "evidenceSealIssued": False, "historicalCasesChangedOrReplayed": False, "applicationPerformedInDirectorResponse": False},
}
write_json(readback_path, readback)
readback_b = staged(readback_path)

accept_path = f"{APP}/DIRECTOR_ACCEPTANCE_486.json"
accept = {
    "schemaVersion": 1, "id": decision["decisionId"], "classification": "GPT_DIRECTOR_STATIC_AUTHORED_PROCEDURE_ACCEPTANCE_NOT_APPLICATION",
    "status": "ACCEPTED_UNAPPLIED", "issuer": "GPT Director", "observedAtUtc": STAMP, "sourceConversation": "Calibration review part 6", "sourceSnapshotCommit": BASE_SHA,
    "scopeIds": ["final-word"], "decision": "ACCEPT", "accepted": True, "applied": False, "acceptedIds": ["final-word"], "appliedIds": [], "heldIdsInReviewedScope": [],
    "closedBlockerIdsWithinScope": ["DR217-B01"], "retainedQualificationIds": HOLDS, "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "authorityAfterDecision": {"applied": 832, "stillHeldPending": 15, "acceptedUnapplied": 1},
    "evidenceBindings": {"proposal": proposal_b, "ownerAdoption": owner_b, "witness": witness_b, "directorReadinessReceipt": ready_b, "directorReadback": readback_b, "ownerAdoptionErratum": erratum_b},
    "structuredDecision": decision, "applicationPerformedInDirectorResponse": False,
    "limitations": {"actualSourceQualificationEstablished": False, "campaignEventClaimed": False, "componentWitnessSealed": False, "canonicalOrRuntimePromotion": False, "historicalCasesReplayed": False, "queueFileChanged": False},
}
write_json(accept_path, accept)
accept_b = staged(accept_path)

recon_path = f"{REC}/FINAL_WORD_IDENTITY_RECONCILIATION_486.json"
archive = next(x for x in proposal["sourceBindings"] if x["id"] == "preserved-return217-closure-delta-303")
recon = {
    "schemaVersion": 1, "id": "FINAL-WORD-IDENTITY-RECONCILIATION-486", "recordedAtUtc": STAMP,
    "classification": "POST_DIRECTOR_ACCEPTANCE_STATIC_AUTHORED_PROCEDURE_APPLICATION_BINDING",
    "identity": "final-word", "blocker": "DR217-B01", "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "directorDisposition": decision, "applicationStatus": "APPLIED_TO_AUTHORED_REVIEW_INDEX_ONLY",
    "reviewedEvidence": {"proposal": proposal_b, "ownerAdoption": owner_b, "witness": witness_b, "directorReadinessReceipt": ready_b, "directorReadback": readback_b, "ownerAdoptionErratum": erratum_b},
    "procedureSource": proc_b, "preservedHistoricalEvidence": {"sourceArchive": archive, "historicalCaseCount": 16, "historicalCasesReplayed": False, "historicalEvidenceChanged": False},
    "effects": {"identityAccepted": True, "identityAppliedToAuthoredReviewIndex": True, "closedBlockersWithinScope": ["DR217-B01"], "retainedQualifications": HOLDS, "sourceProcedureChanged": False, "nativeCatalogChanged": False, "runtimeSelectionEnabled": False, "canonicalOrRuntimePromotion": False, "campaignEventClaimed": False, "evidenceSealIssued": False, "historicalCasesReplayed": False},
}
write_json(recon_path, recon)
recon_b = staged(recon_path)

case_path = f"{CAND}/CASE_COVERAGE.json"
case = {
    "schemaVersion": 1, "id": "FINAL-WORD-STATIC-AUTHORED-COVERAGE-486", "spellId": "final-word", "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "identityReconciliation": recon_b, "directorAcceptance": accept_b, "directorReadback": readback_b,
    "testOnlyWitness": {"branchId": "DR217-B01-TESTONLY-ROUTE-484-01/FW485-R1", "binding": witness_b, "eventGroups": 8, "snapshots": 8, "forwardOperations": 38, "inverseOperations": 38, "exactInitialStateRestoration": True, "componentStatus": "PASS_UNSEALED"},
    "historicalInventory": {"archiveBinding": archive, "caseCount": 16, "historicalCasesReplayed": False},
    "componentCounts": {"reviewedTestOnlyWitnesses": 1, "historicalCaseRecordsPreserved": 16, "historicalCasesReplayed": 0, "closedBlockersWithinScope": 1, "retainedQualificationHolds": len(HOLDS), "sealedWitnesses": 0},
    "closedBlockerIds": ["DR217-B01"], "retainedQualificationIds": HOLDS,
    "preservedLimits": {"actualSourceQualificationEstablished": False, "campaignEventsClaimed": False, "witnessSealed": False, "qualificationHoldsCleared": False, "runtimeSelectionEnabled": False, "nativeCatalogChanged": False, "retainedProcedureChanged": False},
}
write_json(case_path, case)
case_b = staged(case_path)

model_path = f"{CAND}/MODEL.json"
director_record = {
    "id": "final-word", "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
    "accepted": True, "applied": True, "holdIds": HOLDS, "qualificationHoldIds": HOLDS, "closedBlockerIds": ["DR217-B01"], "resolvedBlockerIds": ["DR217-B01"],
    "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "sourceProcedureStatusPreserved": True, "sourceOperationalValuePreserved": None,
    "directorAcceptance": accept_b, "directorReadback": readback_b, "ownerAdoptionReceiptErratum": erratum_b, "witnessBinding": witness_b,
    "caseEvidenceBinding": case_b, "reconciliationBinding": recon_b,
    "reassessment": [{"blockerId": "DR217-B01", "decision": "CLOSED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "directorReadback": readback_path, "witnessPath": WITNESS, "limitation": "No actual-source qualification or campaign fact is established; all five qualification holds remain."}],
}
model = {
    "schemaVersion": 1, "id": "RANK9-FINAL-WORD-STATIC-REVIEWED-486", "reviewId": decision["decisionId"], "status": "REVIEWED_AUTHORED_STATIC_PROCEDURE",
    "acceptedIds": ["final-word"], "heldIds": [], "closedBlockerIds": ["DR217-B01"], "retainedQualificationIds": HOLDS,
    "sourceProcedureBinding": proc_b, "directorReadback": readback_b, "directorAcceptance": accept_b, "ownerAdoptionReceiptErratum": erratum_b, "caseEvidence": case_b,
    "spells": [{"id": "final-word", "name": "Final Word", "nativeCard": native,
        "procedure": {"procedureContent": proc["procedure"], "sharedContract": copy.deepcopy(proc["sharedRules"]), "questionIds": copy.deepcopy(proc["questionIds"]), "focusedQuestionIds": []},
        "sourceProcedureRecord": copy.deepcopy(proc), "directorProcedureRecord": director_record, "sourceProcedureBinding": proc_b,
        "qualificationIds": HOLDS, "closedBlockerIds": ["DR217-B01"], "caseEvidence": case_b, "identityReconciliation": recon_b}],
    "sharedRequirements": copy.deepcopy(proc["sharedRules"]), "runtimeSelectionEnabled": False, "implementationApproved": False, "humanPlayApproved": False,
    "balanceApproved": False, "cosmologyModified": False, "domainClosure": False, "releaseApproved": False, "nativeCatalogChanged": False, "historicalEvidenceChanged": False,
}
write_json(model_path, model)
model_b = staged(model_path)

manifest_path = f"{REC}/MANIFEST_486.json"
manifest = {"schemaVersion": 1, "id": "FINAL-WORD-IDENTITY-RECONCILIATION-486-MANIFEST", "recordedAtUtc": STAMP, "identity": "final-word", "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "files": [proposal_b, owner_b, witness_b, ready_b, route_b, proc_b, bind(INDEX, index_raw), bind(CATALOG, catalog_raw), accept_b, readback_b, erratum_b, recon_b, case_b, model_b],
    "limits": {"nativeCatalogChanged": False, "sourceProcedureChanged": False, "historicalCasesReplayed": False, "runtimePromoted": False, "canonChanged": False}}
write_json(manifest_path, manifest)
manifest_b = staged(manifest_path)
package_path = f"{CAND}/CANDIDATE_PACKAGE_MANIFEST.json"
package = {"schemaVersion": 1, "id": "RANK9-FINAL-WORD-STATIC-REVIEWED-486-PACKAGE", "scope": "Static authored-review index only; native catalog, retained source procedure, canon and runtime remain unchanged.",
    "files": [model_b, case_b, proc_b, accept_b, readback_b, erratum_b, recon_b, manifest_b, proposal_b, owner_b, witness_b, ready_b, route_b]}
write_json(package_path, package)
package_b = staged(package_path)

backup_path = f"{APP}/authored_review_index.before_final_word_application_486.json"
write(backup_path, index_raw)
backup_b = staged(backup_path)
script_path = f"{APP}/prepare_application_486.py"
write(script_path, Path(__file__).read_bytes())
script_b = staged(script_path)
app_path = f"{APP}/APPLICATION_486.json"
app = {
    "id": "FINAL-WORD-STATIC-APPLICATION-486", "recordedAtUtc": STAMP, "acceptedIds": ["final-word"], "appliedIds": ["final-word"], "closedBlockerIdsWithinScope": ["DR217-B01"],
    "directorAcceptance": accept_b, "directorReadback": readback_b, "ownerAdoptionReceiptErratum": erratum_b, "identityReconciliation": recon_b, "identityReconciliationManifest": manifest_b,
    "candidateModel": model_b, "caseCoverage": case_b, "candidatePackageManifest": package_b, "sourceProcedureBeforeAfter": proc_b, "sourceQualificationHoldsBeforeAfter": proc_b,
    "nativeCatalogCommittedBytesBeforeAfter": bind(CATALOG, catalog_raw), "indexBefore": backup_b, "indexBackup": backup_b,
    "authorityBefore": {"reviewedApplied": 832, "pending": 16, "acceptedUnapplied": 0, "completeStandaloneProcedures": 556, "scopedInterfaces": 173},
    "authorityAfter": {"reviewedApplied": 833, "pending": 15, "acceptedUnapplied": 0, "completeStandaloneProcedures": 557, "scopedInterfaces": 173},
    "retainedQualificationIds": HOLDS, "applicationScope": "FINAL_WORD_AUTHORED_REVIEW_INDEX_ONLY", "acceptanceScope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
    "ownerInstruction": "Keep working on the spells until they are accepted and then apply. Apply each batch once it is accepted.",
    "applicationPerformedByDirectorResponse": False, "applicationPerformedUnderOwnerInstruction": True, "sourceStatusPreservedAsBlocked": True,
    "nativeCatalogChanged": False, "sourceProcedureChanged": False, "sourceQualificationHoldsChanged": False, "historicalEvidenceChanged": False, "componentWitnessSealChanged": False,
    "runtimeSelectionEnabled": False, "runtimeExecuted": False, "implementationHumanPlayBalanceCosmologyDomainReleaseApproved": False, "unrelatedIdentityRowsChanged": False,
    "executionScript": script_b,
}
write_json(app_path, app)
app_b = staged(app_path)

after = copy.deepcopy(before)
pos = next(i for i, e in enumerate(after["entries"]) if e["id"] == "final-word")
updated = copy.deepcopy(oldrow)
updated.update({
    "authoredStatus": "reviewed-authored-operational-playtest", "procedureFile": "../spell_candidates/rank9finalword_static_reviewed_486/MODEL.json",
    "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0", "sourceStatus": oldrow["sourceStatus"], "priorCatalogSelectionStatusUnchanged": True,
    "sourceCatalogWholeCardPointer": oldrow["wholeCardPointer"], "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord", "sharedRulesPointer": "/sharedRequirements",
    "spellLocalRequirementsPointer": "/spells/0/procedure", "completeEvidenceRoot": CAND, "completeEnvelopeBinding": model_b, "caseEvidenceBindings": case_b,
    "candidatePackageManifestBinding": package_b, "authoredAcceptanceReceipt": accept_b, "authoredApplicationReceipt": app_b, "sourceProcedureBinding": proc_b,
    "historicalCoverageBinding": case_b, "coverageReconciliationBinding": recon_b, "directorReadbackBinding": readback_b, "reviewId": decision["decisionId"],
    "accepted": True, "applied": True, "closedBlockerIds": ["DR217-B01"], "retainedQualificationIds": HOLDS, "retainedQualifications": HOLDS,
    "historicalCandidateLabelsPreserved": True, "applicationScope": "FINAL_WORD_AUTHORED_REVIEW_INDEX_ONLY",
})
after["entries"][pos] = updated
after["authoredCounts"] = {"reviewed": 833, "pending": 15}
after["representationCounts"]["completeReviewedStandaloneProcedures"] = 557
assert before["standaloneEnvelopeSha256"] == after["standaloneEnvelopeSha256"]
index_after_raw = (json.dumps(after, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
write(INDEX, index_after_raw)
index_after_b = staged(INDEX)

remaining = [x for x in queue0["remainingPendingIds"] if x != "final-word"]
priority = [x for x in queue0["continuingPriorityOrder"] if x != "final-word"]
assert len(remaining) == 15 and priority[0] == "summon-avatar-of-decay"
queue = copy.deepcopy(queue0)
queue.update({
    "id": "CURRENT-SPELL-QUEUE-478", "recordedAtUtc": STAMP, "supersedesQueue": bind(Q477),
    "currentAuthority": {"reviewedApplied": 833, "pending": 15, "acceptedUnapplied": 0, "completeStandaloneProcedures": 557, "scopedInterfaces": 173},
    "currentIndexBinding": index_after_b, "currentCatalogBinding": bind(CATALOG, catalog_raw), "remainingPendingIds": remaining, "continuingPriorityOrder": priority,
    "nextIdentity": "summon-avatar-of-decay", "nextBlockerIds": ["SH202-B03"], "closureTasksRemaining": 15, "firstReviewTasksRemaining": 0,
    "acceptedUnapplied": 0, "acceptedIds": ["final-word"], "appliedIds": ["final-word"], "closedBlockerIdsThisStep": ["DR217-B01"],
    "currentApplication": app_b, "currentDirectorReadback": readback_b,
    "currentReviewPacket": {"path": recon_path, "sha256": recon_b["sha256"], "manifestSha256": manifest_b["sha256"], "classification": "GPT_DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "ownerAdopted": True,
        "fullIdentityDisposition": "ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "identityAccepted": True, "identityAppliedToAuthoredIndex": True, "applicationScope": "FINAL_WORD_AUTHORED_REVIEW_INDEX_ONLY", "runtimeSelectionEnabled": False},
    "pendingIdentityAuditPath": P478, "currentHandoffPath": H478, "runtimeExecuted": False, "runtimeSelectionEnabled": False,
    "repackNote": "GPT independently passed FW485-R1 and accepted Final Word for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY, closing DR217-B01 within scope. The nonblocking owner-readiness receipt-binding erratum was recorded separately without rewriting the original adoption. Applied only to the authored review index; all five qualification holds remain, native catalog/source procedure and runtime are unchanged, and Summon Avatar of Decay / SH202-B03 is next.",
})
write_json(Q478, queue)
queue_b = staged(Q478)
pending = {"id": "CURRENT15-PENDING-IDENTITY-AUDIT-478", "recordedAtUtc": STAMP, "authority": queue["currentAuthority"], "pendingCount": 15, "pendingIds": remaining,
    "indexBinding": index_after_b, "currentQueueBinding": queue_b, "nextPriorityOrder": priority, "allPendingExistInSourceCatalog": True, "acceptedUnappliedIds": [],
    "reviewDispositionThisStep": "FINAL_WORD_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY", "identityAppliedThisStep": "final-word", "blockerClosedThisStep": ["DR217-B01"],
    "nextIdentity": "summon-avatar-of-decay", "nextBlockerIds": ["SH202-B03"], "nextStep": "Continue with Summon Avatar of Decay / SH202-B03 at Queue478 authority 833 applied / 15 pending / 0 accepted-unapplied."}
write_json(P478, pending)
pending_b = staged(P478)
handoff = {"id": "CURRENT-HANDOFF-478", "recordedAtUtc": STAMP, "status": "FINAL_WORD_ACCEPTED_AND_APPLIED_STATIC_AUTHORED_REVIEW_ONLY_NEXT_15_PENDING", "supersedes": bind(H477),
    "queue": queue_b, "pendingIdentityAudit": pending_b, "authority": queue["currentAuthority"], "currentIndexBinding": index_after_b, "currentCatalogBinding": bind(CATALOG, catalog_raw),
    "continuingPriorityOrder": priority, "closureTasksRemaining": 15, "firstReviewTasksRemaining": 0,
    "appliedThisStep": {"reviewId": decision["decisionId"], "ids": ["final-word"], "count": 1, "applicationReceipt": app_path, "directorAcceptance": accept_path, "directorReadback": readback_path},
    "retainedQualificationIds": HOLDS, "closedBlockerIdsWithinScope": ["DR217-B01"], "applicationScope": "FINAL_WORD_AUTHORED_REVIEW_INDEX_ONLY",
    "nativeCatalogAndSourceProcedureUnchanged": True, "runtimeSelectionEnabled": False, "canonicalOrRuntimePromotion": False, "campaignEventClaimed": False,
    "nextIdentity": "summon-avatar-of-decay", "nextBlockerIds": ["SH202-B03"], "nextStep": "Continue with Summon Avatar of Decay / SH202-B03; apply only Director-accepted identities and keep runtime disabled.", "directorAcceptance": accept_b, "applicationReceipt": app_b}
write_json(H478, handoff)
handoff_b = staged(H478)

readme = ("# Final Word static authored review application 486\n\n"
    "GPT independently passed FW485-R1 and accepted Final Word only for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY, closing DR217-B01 within that scope. All five qualification holds remain.\n\n"
    "Only the authored review index and its superseding queue, pending audit, handoff, and activity records changed. The native catalog, retained source procedure, canon, and runtime remain unchanged. The 16 historical Final Word cases remain preserved and were not replayed.\n\n"
    "The nonblocking readiness-receipt hash erratum is recorded separately; the original adoption bytes are preserved.\n\n"
    "Authority: 833 applied / 15 pending / 0 accepted-unapplied. Next: summon-avatar-of-decay / SH202-B03.\n")
write(f"{APP}/README_486.md", readme.encode("utf-8"))

checks = []
def check(name, ok): checks.append({"check": name, "passed": bool(ok)})
check("Director ACCEPT is static-only and binds exact proposal, adoption and witness", accept["decision"] == "ACCEPT" and accept["scope"] == "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY" and accept["evidenceBindings"]["proposal"]["sha256"] == proposal_b["sha256"] and accept["evidenceBindings"]["witness"]["sha256"] == witness_b["sha256"])
check("Director PASS records eight groups, 38 forward/inverse operations and exact restoration", readback["verification"]["eventGroups"] == 8 and readback["verification"]["forwardOperations"] == 38 and readback["verification"]["inverseOperations"] == 38 and readback["verification"]["exactRestoration"] is True)
check("Receipt erratum is additive, correct and does not rewrite the adoption", erratum["recordedValue"] != erratum["correctValue"] and erratum["correctReceipt"]["sha256"] == ready_b["sha256"] and owner_b["sha256"] == owner_b["sha256"])
check("All other authored-index rows are byte-semantically unchanged", [x for x in after["entries"] if x["id"] != "final-word"] == [x for x in before["entries"] if x["id"] != "final-word"])
check("Index becomes 833 reviewed / 15 pending / 557 standalone procedures", after["authoredCounts"] == {"reviewed": 833, "pending": 15} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 557)
check("Final Word row binds exact candidate, coverage, package, acceptance and application", updated["completeEnvelopeBinding"] == model_b and updated["caseEvidenceBindings"] == case_b and updated["candidatePackageManifestBinding"] == package_b and updated["authoredAcceptanceReceipt"] == accept_b and updated["authoredApplicationReceipt"] == app_b)
check("Only DR217-B01 closes within static scope; five qualification holds remain", updated["closedBlockerIds"] == ["DR217-B01"] and updated["retainedQualificationIds"] == HOLDS and model["retainedQualificationIds"] == HOLDS)
check("Catalog and retained procedure unchanged; source remains blocked and runtime disabled", native["operational"] is None and updated["sourceStatus"] == oldrow["sourceStatus"] and model["runtimeSelectionEnabled"] is False)
check("16 historical cases are preserved without replay", case["historicalInventory"]["caseCount"] == 16 and case["historicalInventory"]["historicalCasesReplayed"] is False and case["historicalInventory"]["archiveBinding"]["sha256"] == archive["sha256"])
check("Queue is 833/15/0, with Summon Avatar / SH202-B03 next", queue["currentAuthority"]["reviewedApplied"] == 833 and queue["currentAuthority"]["pending"] == 15 and queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextIdentity"] == "summon-avatar-of-decay" and queue["nextBlockerIds"] == ["SH202-B03"])
check("The remaining 15 identities are still in the catalog and final-word is removed", len(remaining) == 15 and set(remaining) <= {x["id"] for x in catalog["spells"]} and "final-word" not in remaining)
check("Application is limited to authored review index; no canon/runtime/campaign/seal effects", app["applicationScope"] == "FINAL_WORD_AUTHORED_REVIEW_INDEX_ONLY" and app["nativeCatalogChanged"] is False and app["runtimeSelectionEnabled"] is False and app["componentWitnessSealChanged"] is False)
restored = copy.deepcopy(after)
restored["entries"][pos] = copy.deepcopy(oldrow)
restored["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
restored["representationCounts"] = copy.deepcopy(before["representationCounts"])
check("Inverse index transformation restores exact prior state", restored == before)
assert all(x["passed"] for x in checks), [x["check"] for x in checks if not x["passed"]]

validation = {"id": "FINAL-WORD-APPLICATION-VALIDATION-486", "recordedAtUtc": STAMP, "status": "PASS", "checksPassed": len(checks), "checksFailed": 0, "checks": checks,
    "indexBefore": bind(INDEX, index_raw), "indexAfter": index_after_b, "indexBackup": backup_b, "catalog": bind(CATALOG, catalog_raw), "sourceProcedure": proc_b,
    "directorAcceptance": accept_b, "directorReadback": readback_b, "applicationReceipt": app_b, "queueAfter": queue_b, "pendingAuditAfter": pending_b, "handoffAfter": handoff_b,
    "changedIdentityIds": ["final-word"], "acceptedIds": ["final-word"], "appliedIds": ["final-word"], "closedBlockerIdsWithinScope": ["DR217-B01"],
    "retainedQualificationIds": HOLDS, "authorityAfter": queue["currentAuthority"], "nativeCatalogChanged": False, "sourceProcedureChanged": False,
    "runtimeSelectionEnabled": False, "canonicalOrRuntimePromotion": False, "historicalCasesReplayed": False, "inverseSemanticReplayExact": True, "executionScript": script_b}
validation_path = f"{APP}/APPLICATION_VALIDATION_486.json"
write_json(validation_path, validation)
validation_b = staged(validation_path)

activity_path = "docs/activity/2026-11-02.md"
activity = git_bytes(activity_path).decode("utf-8")
activity += ("\n- GPT Director independently passed the hash-bound Final Word FW485-R1 TEST_ONLY witness and accepted Final Word for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY, closing DR217-B01 within scope. Recorded the nonblocking owner-readiness receipt-binding erratum separately and preserved the original adoption bytes.\n"
    "- Applied only the authored review index under the owner instruction; Queue478 is 833 applied / 15 pending / 0 accepted-unapplied. All five qualification holds remain, the native catalog and retained source procedure are unchanged, runtime remains disabled, and Summon Avatar of Decay / SH202-B03 is next. The 16 historical Final Word cases were preserved, not replayed.\n")
write(activity_path, activity.encode("utf-8"))

for p in [erratum_path, readback_path, accept_path, recon_path, case_path, model_path, manifest_path, package_path, app_path, INDEX, Q478, P478, H478, validation_path]:
    json.loads((STAGE / p).read_text(encoding="utf-8"))
print(json.dumps({"status": "APPLICATION_READY_TO_PUBLISH", "baseCommit": BASE_SHA, "filesWritten": sum(1 for p in STAGE.rglob("*") if p.is_file()),
    "decision": decision, "indexBefore": bind(INDEX, index_raw), "indexAfter": index_after_b, "acceptance": accept_b, "readback": readback_b,
    "erratum": erratum_b, "application": app_b, "queue": queue_b, "pendingAudit": pending_b, "handoff": handoff_b, "validation": validation_b,
    "checksPassed": len(checks), "stageRoot": str(STAGE)}, indent=2))
