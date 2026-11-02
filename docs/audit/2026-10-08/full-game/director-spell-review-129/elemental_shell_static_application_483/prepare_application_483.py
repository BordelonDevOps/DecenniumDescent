import copy, hashlib, json, subprocess, zlib
from datetime import datetime, timezone
from pathlib import Path

BASE = "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
assert HEAD == "1ffec43395d6ecaa9e221cfe94eeaccc03b5e50b", HEAD
STAMP = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def G(path):
    return subprocess.check_output(["git", "show", f"HEAD:{path}"])
def J(path):
    return json.loads(G(path))
def CRC(data):
    return f"{zlib.crc32(data) & 0xffffffff:08x}"
def B(path, data=None):
    data = G(path) if data is None else data
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "crc32": CRC(data)}
def LB(path):
    return B(path, Path(path).read_bytes())
def W(path, value):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    data=(json.dumps(value, ensure_ascii=False, indent=2)+"\n").encode("utf-8"); p.write_bytes(data); return data

PROC=f"{BASE}/elemental_shell_caster_premise_proposal_468/payload/sources/ELEMENTAL_SHELL_PROCEDURE_SOURCE.json"
PACKET=f"{BASE}/elemental_shell_identity_reconciliation_483/SHELL_IDENTITY_RECONCILIATION_483.json"
RECON_MANIFEST=f"{BASE}/elemental_shell_identity_reconciliation_483/MANIFEST_483.json"
Q476=f"{BASE}/CURRENT_SPELL_QUEUE_476_REPACK01.json"
P476=f"{BASE}/CURRENT17_PENDING_IDENTITY_AUDIT_476_REPACK01.json"
H476=f"{BASE}/CURRENT_HANDOFF_476_REPACK01.json"
APP=f"{BASE}/elemental_shell_static_application_483"
CAND="DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9elementalshell_static_reviewed_483"
MODEL=f"{CAND}/MODEL.json"; CASE=f"{CAND}/CASE_COVERAGE.json"; PACKAGE=f"{CAND}/CANDIDATE_PACKAGE_MANIFEST.json"
ACCEPT=f"{APP}/DIRECTOR_ACCEPTANCE_483.json"; READBACK=f"{APP}/DIRECTOR_READBACK_483.json"
APPLICATION=f"{APP}/APPLICATION_483.json"; VALIDATION=f"{APP}/APPLICATION_VALIDATION_483.json"
BACKUP=f"{APP}/authored_review_index.before_shell_application_483.json"
Q477=f"{BASE}/CURRENT_SPELL_QUEUE_477_REPACK01.json"
P477=f"{BASE}/CURRENT16_PENDING_IDENTITY_AUDIT_477_REPACK01.json"
H477=f"{BASE}/CURRENT_HANDOFF_477_REPACK01.json"

proc=J(PROC); packet=J(PACKET); q0=J(Q476); p0=J(P476); h0=J(H476)
ib=G(INDEX); before=json.loads(ib); cb=G(CATALOG); catalog=json.loads(cb)
oldrow=copy.deepcopy(next(x for x in before["entries"] if x["id"]=="elemental-shell"))
native=copy.deepcopy(next(x for x in catalog["spells"] if x["id"]=="elemental-shell"))
qids=copy.deepcopy(proc["qualificationHoldIds"]); blockers=["DF218-B01","DF218-B02"]
assert before["authoredCounts"]=={"reviewed":831,"pending":17}
assert before["representationCounts"]["completeReviewedStandaloneProcedures"]==555
assert packet["historicalEvidence"]["freshHistoricalReplayPerformed"] is False
pb=B(PACKET); mb=B(RECON_MANIFEST)

decision={
 "decisionId":"DIRECTOR-ELEMENTAL-SHELL-IDENTITY-483","decision":"ACCEPT",
 "scope":"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY","reviewedCommit":HEAD,
 "reconciliationSha256":pb["sha256"],"manifestSha256":mb["sha256"],
 "acceptedIds":["elemental-shell"],"appliedIds":[],"heldIdsWithinReviewedScope":[],
 "accepted":True,"applied":False,"closedBlockerIdsWithinScope":blockers,
 "remainingRequirementsWithinScope":[],"retainedQualificationIds":qids,
 "componentWitnessSealsIssued":False,"applicationPerformed":False,
 "canonicalOrRuntimePromotion":False,"campaignEventClaimed":False,
 "queueFileChanged":False,"nextPendingIdentity":"final-word"
}
response=(
 "ACCEPT — Elemental Shell only, for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY.\n\n"
 "DF218-B01 and DF218-B02 are CLOSED within that scope. No remaining identity-level requirement was identified for this static review.\n\n"
 "I verified the packet’s raw hash, all 13 witness-chain bindings, retained procedure/rules, ten qualifications, current Shell rows and all 21 historical inventory records—including both completed CH07 Null cases. The historical cases were preserved, not freshly replayed.\n\n"
 "Witness481 satisfies B01 through its exact adopted noncreature-source contract; witness482 Repack03 satisfies B02 through its exact adopted companion attack/reflection branch. Their hypothetical premises remain branch-scoped. All selected rules, historical evidence and unrelated decisions remain preserved.\n\n"
 "Post-decision accounting: 831 applied / 16 still-held pending / 1 accepted-unapplied. The stored Queue476 remains unchanged at its submission snapshot.\n\n"
 "The next administrative step is the separate audited authored-index application of this exact acceptance. No application is performed here. Final Word / DR217-B01 is the next closure identity."
)
acceptance={
 "schemaVersion":1,"id":decision["decisionId"],
 "classification":"GPT_DIRECTOR_STATIC_AUTHORED_PROCEDURE_ACCEPTANCE_NOT_APPLICATION",
 "status":"ACCEPTED_UNAPPLIED","issuer":"GPT Director","observedAtUtc":STAMP,
 "sourceConversation":"Calibration review part 6","sourceSnapshotCommit":HEAD,
 "scopeIds":["elemental-shell"],"decision":"ACCEPT","accepted":True,"applied":False,
 "acceptedIds":["elemental-shell"],"appliedIds":[],"heldIdsInReviewedScope":[],
 "closedBlockerIds":blockers,"retainedQualificationIds":qids,
 "scope":"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
 "authorityAfterDecision":{"applied":831,"stillHeldPending":16,"acceptedUnapplied":1},
 "evidenceBindings":{"reconciliation":pb,"manifest":mb},"structuredDecision":decision,
 "applicationPerformedInDirectorResponse":False,
 "limitations":{"componentWitnessSealsIssued":False,"canonicalOrRuntimePromotion":False,
  "campaignEventClaimed":False,"queueFileChanged":False,"historicalCasesReplayed":False}
}
W(ACCEPT,acceptance)
readback={
 "schemaVersion":1,"id":"ELEMENTAL-SHELL-DIRECTOR-READBACK-483","recordedAtUtc":STAMP,
 "source":{"service":"GPT Director","conversationTitle":"Calibration review part 6",
  "conversationUrl":"https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
 "classification":"DIRECTOR_IDENTITY_ACCEPTANCE_READBACK_NOT_APPLICATION",
 "decision":decision,"directorResponseText":response,"applicationOccurredInDirectorResponse":False,
 "evidenceBindings":{"reconciliation":pb,"manifest":mb}
}
W(READBACK,readback)

B01=f"{BASE}/elemental_shell_b01_witness_481_repack01/"
B02=f"{BASE}/elemental_shell_b02_witness_482_repack03/"
b01read=J(B01+"DIRECTOR_READBACK_481.json"); b01w=J(B01+"DF218_B01_WITNESS_481_TESTONLY.json")
b02delivery=J(B02+"DELIVERY_482_REPACK03.json")
dpath=f"{BASE}/rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306_DELIVERY.json"
d306=J(dpath)
cases=[{k:m[k] for k in ("path","bytes","sha256","crc32")} for m in d306["members"][37:58]]
assert len(cases)==21
assert cases[0]["sha256"]=="7ff339950289e3e0c23e6847fc1edbcd2166edaf7e1698b77f39d911d9a8f997"
assert cases[1]["sha256"]=="9f64281f350c01ed70e8bec25877e023f26125b511d6db340ff260d37acee601"
proc_member=d306["members"][58]; case_index=d306["members"][31]
coverage={
 "schemaVersion":1,"id":"ELEMENTAL-SHELL-STATIC-AUTHORED-COVERAGE-483",
 "spellId":"elemental-shell","scope":"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
 "coverageReconciliation":pb,"identityDecision":LB(ACCEPT),
 "historicalInventory":B(dpath),"historicalCaseMemberPointerRange":"/members/37 through /members/57 inclusive",
 "historicalCaseHashDomain":"Raw, uncompressed ZIP-member bytes from the authoritative Packet306 delivery inventory.",
 "historicalArchive":{"path":f"{BASE}/rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306.zip",
  "storage":"Git LFS","payloadBytes":13255922,
  "payloadSha256":"d165cd0f44d728a5cdb27c5dcdbdbdec0f1cf1ae4220be8efea94649566ca45b",
  "crc32":"290c4eaa","locallyRehashedByThisApplication":False},
 "retainedProcedureArchiveMember":{k:proc_member[k] for k in ("path","bytes","sha256","crc32")},
 "retainedCaseIndexArchiveMember":{k:case_index[k] for k in ("path","bytes","sha256","crc32")},
 "componentCounts":{"componentSufficientUnsealed":2,"closedBlockersWithinScope":2,
  "sealedWitnesses":0,"historicalCaseRecords":21,"retainedQualificationHolds":10},
 "componentRows":[
  {"id":"DF218-B01","title":"Noncreature source / reflection without creature dealer",
   "disposition":"CLOSED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY","componentStatus":"COMPONENT_SUFFICIENT_UNSEALED",
   "witnessSha256":b01read["reviewedWitness"]["sha256"],
   "directorReadback":B(B01+"DIRECTOR_READBACK_481.json"),
   "validation":B(B01+"INDEPENDENT_VALIDATION_481.json"),
   "events":b01read["verified"]["events"],"stateSnapshots":b01read["verified"]["stateSnapshots"],
   "forwardOperations":b01read["verified"]["forwardOperations"],
   "inverseOperations":b01read["verified"]["inverseOperations"],
   "exactStartRestoration":b01read["verified"]["restoresExactS000"]},
  {"id":"DF218-B02","branchId":b02delivery["branchId"],
   "title":"Companion attack and reflection branch",
   "disposition":"CLOSED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY","componentStatus":"COMPONENT_SUFFICIENT_UNSEALED",
   "witnessSha256":b02delivery["witnessSha256"],
   "directorReadback":B(B02+"DIRECTOR_READBACK_482_PASS_REPACK03.json"),
   "validation":B(B02+"INDEPENDENT_VALIDATION_482_REPACK03.json"),
   "validationChecksPassed":b02delivery["validationChecksPassed"],
   "events":b02delivery["eventCount"],"stateSnapshots":b02delivery["snapshotCount"],
   "forwardOperations":b02delivery["forwardOperationCount"],
   "inverseOperations":b02delivery["inverseOperationCount"],"exactStartRestoration":True}
 ],
 "historicalRecordCount":21,"historicalCaseBindings":cases,
 "preservedLimits":{"historicalCasesFreshlyReplayed":False,"campaignEventsClaimed":False,
  "componentWitnessesSealed":False,"allTenQualificationHoldsRetained":True,
  "runtimeSelectionEnabled":False,"nativeCatalogChanged":False,"retainedProcedureChanged":False},
 "closure":{"closedBlockerIds":blockers,"scope":"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
  "remainingRequirementsWithinScope":[]},
 "effects":{"acceptedIds":["elemental-shell"],"appliedToAuthoredReviewIndex":True,
  "canonicalRuleChanged":False,"runtimePromoted":False,
  "spellApplicationToNativeCatalog":False,"queueChangedByIdentityDecision":False}
}
W(CASE,coverage)
source_binding=B(PROC); accept_binding=LB(ACCEPT); readback_binding=LB(READBACK); case_binding=LB(CASE)
source_record={
 "id":"elemental-shell","procedureId":proc["id"],"status":proc["status"],
 "nativeCardUnchanged":copy.deepcopy(proc["nativeCardAndAccessUnchanged"]),
 "sourceIndexEntryUnchanged":oldrow,"sharedContract":copy.deepcopy(proc["sharedRules"]),
 "procedure":{"procedureContent":proc["procedureText"],"sharedContract":copy.deepcopy(proc["sharedRules"]),
  "selectedRules":copy.deepcopy(proc["selectedRules"])},
 "questionIds":copy.deepcopy(proc["questionIds"]),
 "focusedQuestionIds":copy.deepcopy(proc["focusedQuestionIds"]),
 "accepted":False,"applied":False,"holdIds":qids+proc["holds"],
 "caseIds":copy.deepcopy(proc["caseIds"])
}
reassessment=[
 {"blockerId":x,"decision":"CLOSED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
  "directorReadback":READBACK,
  "witnessPath":B01+"DF218_B01_WITNESS_481_TESTONLY.json" if x=="DF218-B01" else B02+"DF218_B02_WITNESS_482_REPACK03_TESTONLY.json",
  "limitation":"Closure is static-review-only. Hypothetical branch facts are not campaign events; all ten qualification holds remain."}
 for x in blockers
]
director_record={**source_record,
 "status":"DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
 "accepted":True,"applied":True,"holdIds":qids,"qualificationHoldIds":qids,
 "closedBlockerIds":blockers,"resolvedBlockerIds":blockers,
 "sourceProcedureStatusPreserved":True,"sourceOperationalValuePreserved":None,
 "reassessment":reassessment}
model={
 "schemaVersion":1,"id":"RANK9-ELEMENTAL-SHELL-STATIC-REVIEWED-483",
 "reviewId":decision["decisionId"],"status":"REVIEWED_AUTHORED_STATIC_PROCEDURE",
 "acceptedIds":["elemental-shell"],"heldIds":[],"closedBlockerIds":blockers,
 "retainedQualificationIds":qids,"sourceProcedureBinding":source_binding,
 "directorReadback":readback_binding,"directorAcceptance":accept_binding,"caseEvidence":case_binding,
 "spells":[{"id":"elemental-shell","name":"Elemental Shell","nativeCard":native,
  "procedure":{"procedureContent":proc["procedureText"],"sharedContract":copy.deepcopy(proc["sharedRules"]),
   "selectedRules":copy.deepcopy(proc["selectedRules"]),"questionIds":copy.deepcopy(proc["questionIds"]),
   "focusedQuestionIds":copy.deepcopy(proc["focusedQuestionIds"])},
  "sourceProcedureRecord":source_record,"directorProcedureRecord":director_record,
  "sourceProcedureBinding":source_binding,"qualificationIds":qids,
  "closedBlockerIds":blockers,"caseEvidence":case_binding}],
 "sharedRequirements":copy.deepcopy(proc["sharedRules"]),
 "runtimeSelectionEnabled":False,"implementationApproved":False,
 "humanPlayApproved":False,"balanceApproved":False,"cosmologyModified":False,
 "domainClosure":False,"releaseApproved":False,"nativeCatalogChanged":False,
 "historicalEvidenceChanged":False}
W(MODEL,model); model_binding=LB(MODEL)
evidence=[MODEL,CASE,PROC,ACCEPT,READBACK,PACKET,RECON_MANIFEST,dpath,
 B01+"DELIVERY_481.json",B01+"DF218_B01_WITNESS_481_TESTONLY.json",B01+"INDEPENDENT_VALIDATION_481.json",
 B02+"DELIVERY_482_REPACK03.json",B02+"DF218_B02_WITNESS_482_REPACK03_TESTONLY.json",B02+"INDEPENDENT_VALIDATION_482_REPACK03.json"]
package={"schemaVersion":1,"id":"RANK9-ELEMENTAL-SHELL-STATIC-REVIEWED-483-PACKAGE",
 "files":[LB(x) if Path(x).exists() else B(x) for x in evidence],
 "scope":"Static authored-review index only; native catalog, retained source procedure and runtime remain unchanged."}
W(PACKAGE,package); package_binding=LB(PACKAGE)
Path(BACKUP).parent.mkdir(parents=True,exist_ok=True); Path(BACKUP).write_bytes(ib)
backup_binding=LB(BACKUP)
application={
 "id":"ELEMENTAL-SHELL-STATIC-APPLICATION-483","recordedAtUtc":STAMP,
 "acceptedIds":["elemental-shell"],"appliedIds":["elemental-shell"],"closedBlockerIds":blockers,
 "directorAcceptance":accept_binding,"directorReadback":readback_binding,
 "identityReconciliation":pb,"identityReconciliationManifest":mb,
 "candidateModel":model_binding,"caseCoverage":case_binding,"candidatePackageManifest":package_binding,
 "sourceProcedureBeforeAfter":source_binding,"sourceQualificationHoldsBeforeAfter":source_binding,
 "nativeCatalogCommittedGitBlobBeforeAfter":B(CATALOG,cb),
 "indexBefore":backup_binding,"indexBackup":backup_binding,
 "authorityBefore":{"reviewedApplied":831,"pending":16,"acceptedUnapplied":1,"completeStandaloneProcedures":555,"scopedInterfaces":173},
 "authorityAfter":{"reviewedApplied":832,"pending":16,"acceptedUnapplied":0,"completeStandaloneProcedures":556,"scopedInterfaces":173},
 "retainedQualificationIds":qids,"applicationScope":"ELEMENTAL_SHELL_AUTHORED_REVIEW_INDEX_ONLY",
 "acceptanceScope":"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
 "ownerInstruction":"Keep working on the spells until they are accepted and then apply. Apply each batch once it is accepted.",
 "applicationPerformedByDirectorResponse":False,"applicationPerformedUnderOwnerInstruction":True,
 "sourceStatusPreservedAsBlocked":True,"nativeCatalogChanged":False,"sourceProcedureChanged":False,
 "sourceQualificationHoldsChanged":False,"historicalEvidenceChanged":False,
 "componentWitnessSealsChanged":False,"runtimeSelectionEnabled":False,"runtimeExecuted":False,
 "implementationHumanPlayBalanceCosmologyDomainReleaseApproved":False,"unrelatedIdentityRowsChanged":False,
 "executionScript":LB(f"{APP}/prepare_application_483.py")}
W(APPLICATION,application); application_binding=LB(APPLICATION)

after=copy.deepcopy(before); pos=next(i for i,x in enumerate(after["entries"]) if x["id"]=="elemental-shell")
updated=copy.deepcopy(oldrow)
updated.update({
 "authoredStatus":"reviewed-authored-operational-playtest",
 "procedureFile":"../spell_candidates/rank9elementalshell_static_reviewed_483/MODEL.json",
 "procedurePointer":"/spells/0/procedure","wholeCardPointer":"/spells/0",
 "sourceStatus":oldrow["sourceStatus"],"priorCatalogSelectionStatusUnchanged":True,
 "procedureTextPointer":"/spells/0/procedure/procedureContent","wholeCardIdField":"id",
 "sourceCatalogWholeCardPointer":oldrow["wholeCardPointer"],
 "directorProcedureRecordPointer":"/spells/0/directorProcedureRecord",
 "sharedRulesPointer":"/sharedRequirements","spellLocalRequirementsPointer":"/spells/0/procedure",
 "runtimeSelectionEnabled":False,"completeEvidenceRoot":CAND,
 "completeEnvelopeBinding":model_binding,"caseEvidenceBindings":case_binding,
 "candidatePackageManifestBinding":package_binding,"authoredAcceptanceReceipt":accept_binding,
 "authoredApplicationReceipt":application_binding,"sourceProcedureBinding":source_binding,
 "historicalCoverageBinding":case_binding,"coverageReconciliationBinding":pb,
 "directorReadbackBinding":readback_binding,"reviewId":decision["decisionId"],
 "accepted":True,"applied":True,"closedBlockerIds":blockers,
 "retainedQualificationIds":qids,"retainedQualifications":copy.deepcopy(proc["qualifications"]),
 "historicalCandidateLabelsPreserved":True,
 "applicationScope":"ELEMENTAL_SHELL_AUTHORED_REVIEW_INDEX_ONLY"})
after["entries"][pos]=updated
after["authoredCounts"]={"reviewed":832,"pending":16}
after["representationCounts"]["completeReviewedStandaloneProcedures"]=556
assert before["standaloneEnvelopeSha256"]==after["standaloneEnvelopeSha256"]
assert (json.dumps(before,ensure_ascii=False,indent=2)+"\n").encode("utf-8")==ib
ia=(json.dumps(after,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
Path(INDEX).parent.mkdir(parents=True,exist_ok=True); Path(INDEX).write_bytes(ia)
index_after=LB(INDEX)

queue=copy.deepcopy(q0)
pending_ids=[x for x in q0["remainingPendingIds"] if x!="elemental-shell"]
priority=[x for x in q0["continuingPriorityOrder"] if x!="elemental-shell"]
queue.update({
 "id":"CURRENT-SPELL-QUEUE-477-REPACK01","recordedAtUtc":STAMP,
 "supersedesQueue":B(Q476),
 "currentAuthority":{"reviewedApplied":832,"pending":16,"acceptedUnapplied":0,"completeStandaloneProcedures":556,"scopedInterfaces":173},
 "currentIndexBinding":index_after,"currentCatalogBinding":B(CATALOG,cb),
 "remainingPendingIds":pending_ids,"continuingPriorityOrder":priority,
 "nextIdentity":"final-word","nextBlockerIds":["DR217-B01"],
 "closureTasksRemaining":16,"firstReviewTasksRemaining":0,"acceptedUnapplied":0,
 "acceptedIds":["elemental-shell"],"appliedIds":["elemental-shell"],
 "closedBlockerIdsThisStep":blockers,"currentApplication":application_binding,
 "currentDirectorReadback":readback_binding,
 "currentReviewPacket":{"path":PACKET,"sha256":pb["sha256"],"manifestSha256":mb["sha256"],
  "classification":"GPT_DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
  "ownerAdopted":True,"fullIdentityDisposition":"ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
  "identityAccepted":True,"identityAppliedToAuthoredIndex":True,
  "applicationScope":"ELEMENTAL_SHELL_AUTHORED_REVIEW_INDEX_ONLY","runtimeSelectionEnabled":False},
 "pendingIdentityAuditPath":P477,"currentHandoffPath":H477,
 "runtimeExecuted":False,"runtimeSelectionEnabled":False,
 "repackNote":"GPT accepted Elemental Shell for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY and closed DF218-B01/B02 within scope. The owner-authorized authored-index application is complete. All ten qualification holds remain; native catalog/source procedure, runtime, canon and campaign state are unchanged. Next identity: Final Word / DR217-B01."})
W(Q477,queue); queue_binding=LB(Q477)
catalog_ids={x["id"] for x in catalog["spells"]}
assert len(pending_ids)==16 and set(pending_ids)<=catalog_ids and "elemental-shell" not in pending_ids
pending={"id":"CURRENT16-PENDING-IDENTITY-AUDIT-477-REPACK01","recordedAtUtc":STAMP,
 "authority":queue["currentAuthority"],"pendingCount":16,"pendingIds":pending_ids,
 "indexBinding":index_after,"currentQueueBinding":queue_binding,"nextPriorityOrder":priority,
 "allPendingExistInSourceCatalog":True,"acceptedUnappliedIds":[],
 "reviewDispositionThisStep":"ELEMENTAL_SHELL_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
 "identityAppliedThisStep":"elemental-shell","blockerClosedThisStep":blockers,
 "nextIdentity":"final-word","nextBlockerIds":["DR217-B01"],
 "nextStep":"Prepare Final Word / DR217-B01 against current 832/16/0 authority. Preserve unrelated identities and the ten Elemental Shell qualification holds."}
W(P477,pending); pending_binding=LB(P477)
handoff={"id":"CURRENT-HANDOFF-477-REPACK01","recordedAtUtc":STAMP,
 "status":"ELEMENTAL_SHELL_ACCEPTED_AND_APPLIED_STATIC_AUTHORED_REVIEW_ONLY_NEXT_16_PENDING",
 "supersedes":B(H476),"queue":queue_binding,"pendingIdentityAudit":pending_binding,
 "authority":queue["currentAuthority"],"currentIndexBinding":index_after,
 "currentCatalogBinding":B(CATALOG,cb),"continuingPriorityOrder":priority,
 "closureTasksRemaining":16,"firstReviewTasksRemaining":0,
 "appliedThisStep":{"reviewId":decision["decisionId"],"ids":["elemental-shell"],"count":1,
  "applicationReceipt":APPLICATION,"directorAcceptance":ACCEPT,"directorReadback":READBACK},
 "retainedQualificationIds":qids,"closedBlockerIdsWithinScope":blockers,
 "applicationScope":"ELEMENTAL_SHELL_AUTHORED_REVIEW_INDEX_ONLY",
 "nativeCatalogAndSourceProcedureUnchanged":True,"runtimeSelectionEnabled":False,
 "canonicalOrRuntimePromotion":False,"campaignEventClaimed":False,
 "nextIdentity":"final-word","nextBlockerIds":["DR217-B01"],
 "nextStep":"Continue with Final Word / DR217-B01 at Queue477 authority 832 applied / 16 pending / 0 accepted-unapplied. Apply only exact Director-accepted IDs; preserve unrelated holds and keep runtime disabled.",
 "directorAcceptance":accept_binding,"applicationReceipt":application_binding}
W(H477,handoff); handoff_binding=LB(H477)

restored=copy.deepcopy(after); restored["entries"][pos]=copy.deepcopy(oldrow)
restored["authoredCounts"]=copy.deepcopy(before["authoredCounts"])
restored["representationCounts"]=copy.deepcopy(before["representationCounts"])
checks=[
 ("Director ACCEPT binds exact packet, manifest and reviewed commit",decision["reviewedCommit"]==HEAD and decision["reconciliationSha256"]==pb["sha256"] and decision["manifestSha256"]==mb["sha256"]),
 ("Only accepted Shell was applied to the authored index",acceptance["acceptedIds"]==["elemental-shell"] and application["appliedIds"]==["elemental-shell"]),
 ("B01/B02 close only within the accepted static scope",updated["closedBlockerIds"]==blockers and updated["applicationScope"]=="ELEMENTAL_SHELL_AUTHORED_REVIEW_INDEX_ONLY"),
 ("All unrelated index rows are unchanged",[x for x in after["entries"] if x["id"]!="elemental-shell"]==[x for x in before["entries"] if x["id"]!="elemental-shell"]),
 ("Index totals are 832 reviewed / 16 pending and 556 standalone procedures",after["authoredCounts"]=={"reviewed":832,"pending":16} and after["representationCounts"]["completeReviewedStandaloneProcedures"]==556),
 ("Index row binds exact candidate, coverage, package, acceptance and application",updated["completeEnvelopeBinding"]==model_binding and updated["caseEvidenceBindings"]==case_binding and updated["candidatePackageManifestBinding"]==package_binding and updated["authoredApplicationReceipt"]==application_binding),
 ("All ten qualification holds remain",updated["retainedQualificationIds"]==qids and model["retainedQualificationIds"]==qids and len(qids)==10),
 ("Catalog and retained procedure are unchanged; runtime stays disabled",native["operational"] is None and cb==G(CATALOG) and source_binding["sha256"]==B(PROC)["sha256"] and not model["runtimeSelectionEnabled"]),
 ("All 21 historical hashes match Packet306 delivery members 37-57",cases==packet["historicalEvidence"]["cases"] and len(cases)==21),
 ("No historical case replay or witness seal is claimed",not coverage["preservedLimits"]["historicalCasesFreshlyReplayed"] and not coverage["preservedLimits"]["componentWitnessesSealed"]),
 ("Queue477 is 832/16/0 and Final Word/DR217-B01 is next",queue["currentAuthority"]["reviewedApplied"]==832 and queue["currentAuthority"]["pending"]==16 and queue["currentAuthority"]["acceptedUnapplied"]==0 and queue["nextIdentity"]=="final-word" and queue["nextBlockerIds"]==["DR217-B01"]),
 ("All 16 pending identities exist in unchanged source catalog",len(pending_ids)==16 and set(pending_ids)<=catalog_ids and "elemental-shell" not in pending_ids),
 ("Inverse application restores exact prior index semantics",restored==before),
 ("Implementation, play, balance, cosmology, domain and release remain unapproved",not model["implementationApproved"] and not model["humanPlayApproved"] and not model["balanceApproved"] and not model["cosmologyModified"] and not model["domainClosure"] and not model["releaseApproved"])
]
assert all(ok for _,ok in checks),[name for name,ok in checks if not ok]
validation={"id":"ELEMENTAL-SHELL-APPLICATION-VALIDATION-483","recordedAtUtc":STAMP,
 "status":"PASS","checksPassed":len(checks),"checksFailed":0,
 "checks":[{"check":name,"passed":ok} for name,ok in checks],
 "beforeIndex":B(INDEX,ib),"afterIndex":index_after,"indexBackup":backup_binding,
 "catalog":B(CATALOG,cb),"sourceProcedure":source_binding,"directorAcceptance":accept_binding,
 "applicationReceipt":application_binding,"queueAfter":queue_binding,
 "pendingAuditAfter":pending_binding,"handoffAfter":handoff_binding,
 "changedIdentityIds":["elemental-shell"],"acceptedIds":["elemental-shell"],
 "appliedIds":["elemental-shell"],"closedBlockerIdsWithinScope":blockers,
 "retainedQualificationIds":qids,"authorityAfter":queue["currentAuthority"],
 "nativeCatalogChanged":False,"sourceProcedureChanged":False,"runtimeSelectionEnabled":False,
 "canonicalOrRuntimePromotion":False,"historicalCasesReplayed":False,"inverseSemanticReplayExact":True}
validation["executionScript"]=LB(f"{APP}/prepare_application_483.py")
W(VALIDATION,validation)
activity_path="docs/activity/2026-11-02.md"
activity=G(activity_path).decode("utf-8")
activity+=(
 "\n- GPT Director accepted Elemental Shell for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY and closed DF218-B01/B02 within that scope. Recorded the decision and applied only the authored-review index under the owner’s standing instruction; Queue477 is 832 applied / 16 pending / 0 accepted-unapplied. All ten qualification holds remain, the native catalog and source procedure are unchanged, runtime remains disabled, and Final Word / DR217-B01 is next.\n"
 "- Published the static candidate envelope, 21-record historical coverage binding, acceptance/application receipts, index backup, Queue477, pending audit, handoff and PASS application validation. No historical replay, witness seal, campaign event, canonical change or runtime promotion is claimed.\n")
Path(activity_path).write_text(activity,encoding="utf-8",newline="\n")
for path in (ACCEPT,READBACK,CASE,MODEL,PACKAGE,APPLICATION,Q477,P477,H477,VALIDATION):
    json.loads(Path(path).read_text(encoding="utf-8"))
print(json.dumps({"status":"APPLICATION_READY_TO_PUBLISH","sourceCommit":HEAD,
 "decisionId":decision["decisionId"],"acceptance":accept_binding,"model":model_binding,
 "caseCoverage":case_binding,"candidatePackageManifest":package_binding,
 "applicationReceipt":application_binding,"indexBefore":backup_binding,
 "indexAfter":index_after,"queueAfter":queue_binding,"pendingAuditAfter":pending_binding,
 "handoffAfter":handoff_binding,"validation":LB(VALIDATION),"checksPassed":len(checks)},indent=2))
