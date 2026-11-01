#!/usr/bin/env python3
"""Apply exact Sphere acceptance to the authored-review index only."""
import copy, datetime as dt, hashlib, json, subprocess, sys, zlib, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent; ROOT=BASE.parents[4]
OUT=BASE/"invulnerable_sphere_static_acceptance_423_repack01"
CANDREL=Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9invulnerablesphere_reviewed_423")
CAND=ROOT/CANDREL; ID="invulnerable-sphere"; BLOCKER="DF218-B04"
INDEX=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE0=BASE/"CURRENT_SPELL_QUEUE_404.json"; HANDOFF0=BASE/"CURRENT_HANDOFF_404.json"
ACCEPT=OUT/"INVULNERABLE_SPHERE_STATIC_ACCEPTANCE_423_REPACK01.json"
DELIVERY=OUT/"INVULNERABLE_SPHERE_STATIC_ACCEPTANCE_423_REPACK01_DELIVERY.json"
SOURCE=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/DIRECTOR_RETURN/procedures/invulnerable-sphere.json"
WD=BASE/"invulnerable_sphere_witness_423_repack01"
WZIP=WD/"DD_Rank9_InvulnerableSphere_DF218-B04_Witness_423_Repack01_TESTONLY.zip"
HZIP=BASE/"rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
def H(b): return hashlib.sha256(b).hexdigest()
def CRC(b): return f"{zlib.crc32(b)&0xffffffff:08x}"
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode()
def bind(p,b=None):
 b=p.read_bytes() if b is None else b
 return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":H(b),"crc32":CRC(b)}
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); b=enc(x); p.write_bytes(b); return bind(p,b)
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def main():
 assert OUT.is_dir() and ACCEPT.exists() and DELIVERY.exists()
 appdir=OUT
 cdir=CAND
 targets=[cdir,appdir/"authored_review_index.before_invulnerable_sphere_423.json",
 appdir/"CASE_COVERAGE.json",appdir/"APPLICATION.json",appdir/"INDEX_OPERATIONS.json",appdir/"VALIDATION.json",
 BASE/"CURRENT18_PENDING_IDENTITY_AUDIT_423_REPACK01.json",BASE/"CURRENT_SPELL_QUEUE_423_REPACK01.json",
 BASE/"CURRENT_HANDOFF_423_REPACK01.json",BASE/"CURRENT_SPELL_REVIEW_SNAPSHOT_423_REPACK01.md"]
 assert not any(x.exists() for x in targets),"Existing application output; refusing to overwrite."
 ar,dr=ACCEPT.read_bytes(),DELIVERY.read_bytes(); a=json.loads(ar); d=json.loads(dr)
 assert H(ar)==d["file"]["sha256"]=="e0988c71013c87699129078f718712462e16eaa0e915fb9502ce16cee06c3afe"
 assert H(dr)=="e74798dfe2a7ec9477c47e32aba9ccaa4662bd52d26937d6c2674fbfdb6219e0" and len(ar)==18968
 assert a["id"]==d["decisionId"] and a["status"]=="ACCEPTED_UNAPPLIED" and a["decision"]=="ACCEPT"
 assert a["acceptedIds"]==[ID] and a["appliedIds"]==[] and a["closedBlockerIds"]==[BLOCKER]
 head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
 assert a["sourceSnapshotCommit"]==head
 q0,h0=read(QUEUE0),read(HANDOFF0)
 idxraw,catraw,sourceraw=INDEX.read_bytes(),CATALOG.read_bytes(),SOURCE.read_bytes()
 idx0,cat,proc=read(INDEX),read(CATALOG),read(SOURCE)
 commitcat=subprocess.check_output(["git","show",head+":DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"],cwd=ROOT)
 assert H(commitcat)==q0["currentCatalogBinding"]["sha256"]
 assert H((ROOT/a["evidenceBindings"]["queue404"]["path"]).read_bytes())==a["evidenceBindings"]["queue404"]["sha256"]
 assert a["evidenceBindings"]["queue404"]["sha256"]=="9346663e8858c720c9b453921984d9af7925feb5f8c263d31e5b19a72b364b60"
 assert q0["currentAuthority"]==h0["authority"]==a["authority"]["recordedQueue404Unchanged"]
 assert bind(INDEX,idxraw)["sha256"]==q0["currentIndexBinding"]["sha256"]
 assert idx0["authoredCounts"]=={"reviewed":829,"pending":19}
 assert idx0["representationCounts"]["completeReviewedStandaloneProcedures"]==553
 after={k:v for k,v in a["authority"]["expectedAfterSeparateExactApplication"].items() if k!="performed"}
 assert after=={"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"completeStandaloneProcedures":554,"scopedInterfaces":173}
 assert proc["spellId"]==ID and proc["holds"]==[BLOCKER] and not proc["accepted"] and not proc["applied"]
 assert proc["qualificationHoldIds"]==a["qualificationHoldIds"] and len(proc["qualificationHoldIds"])==10
 assert not d["applicationPerformed"] and not d["sealIssued"]
 assert not a["nonEffects"]["catalogChanged"] and not a["nonEffects"]["authoredIndexChanged"]
 for name,row in a["evidenceBindings"].items():
  if name!="witnessReplay":
   b=(ROOT/row["path"]).read_bytes(); assert len(b)==row["bytes"] and H(b)==row["sha256"],name
 with zipfile.ZipFile(WZIP) as z:
  assert z.testzip() is None; replay=z.read("SPHERE_WITNESS_REPLAY_423_REPACK01_TESTONLY.json")
 rr=a["evidenceBindings"]["witnessReplay"]; assert len(replay)==rr["bytes"] and H(replay)==rr["sha256"]
 replayobj=json.loads(replay)
 assert replayobj["scope"]["identity"]==ID and replayobj["scope"]["blockerId"]==BLOCKER
 assert replayobj["scope"]["adoptedPremiseIds"]==["SP-CAND-P01","SP-CAND-P02","SP-CAND-P03","SP-CAND-P04","SP-CAND-P05"]
 historical=a["coverageReconciliation"]["all14HistoricalRecords"]; assert len(historical)==14
 with zipfile.ZipFile(HZIP) as z:
  assert z.testzip() is None
  for r in historical:
   b=z.read(r["member"]); assert len(b)==r["bytes"] and H(b)==r["sha256"],r["caseId"]
 b4=a["coverageReconciliation"]["historicalB4"]
 assert b4["status"]=="INCOMPLETE_HISTORICAL_EVIDENCE_PRESERVED" and not b4["positionConventionRepairedOrInferred"]
 assert not b4["geometryRepairedOrRelocated"] and not b4["bytesModified"] and not b4["successInferred"]
 audit=read(WD/"INDEPENDENT_AUDIT_423_REPACK01.json")
 rb=read(WD/"DIRECTOR_READBACK_423_REPACK01.json")
 assert audit["checksPassed"]==387 and audit["checksFailed"]==0
 assert rb["result"]["status"]=="PASS_FOR_TEST_ONLY_WITNESS_SUFFICIENCY" and rb["result"]["additionalWitnessCorrections"]==[]
 assert rb["remainingScope"]["DF218B04Closed"] is False
 v=json.loads(subprocess.run([sys.executable,"-B",str(BASE/"verify_invulnerable_sphere_witness_423_repack01.py"),],cwd=ROOT,capture_output=True,text=True,check=True).stdout)
 assert v["checksPassed"]==387 and v["eventCount"]==68 and v["forwardOperations"]==v["inverseOperations"]==445
 row0=copy.deepcopy(next(r for r in idx0["entries"] if r["id"]==ID))
 p0=[r["id"] for r in idx0["entries"] if r["authoredStatus"]=="pending-authored-procedure"]
 assert len(p0)==19 and ID in p0 and row0["sourceStatus"]=="blocked-pending-operational-review"
 native=next(r for r in cat["spells"] if r["id"]==ID)
 assert cat["spells"].index(native)==96 and native==proc["nativeCardAndAccessUnchanged"] and native["operational"] is None
 cdir.mkdir(parents=True)
 (appdir/".gitattributes").write_text("** -text !eol\n",encoding="utf-8",newline="\n")
 (cdir/".gitattributes").write_text("** -text !eol\n",encoding="utf-8",newline="\n")
 backup=appdir/"authored_review_index.before_invulnerable_sphere_423.json"; backup.write_bytes(idxraw)
 arref,dref,sref=bind(ACCEPT,ar),bind(DELIVERY,dr),bind(SOURCE,sourceraw)
 histref,wzref=bind(HZIP),bind(WZIP)
 replayref={"archive":wzref["path"],"member":"SPHERE_WITNESS_REPLAY_423_REPACK01_TESTONLY.json","bytes":len(replay),"sha256":H(replay),"crc32":CRC(replay)}
 cov={"id":"INVULNERABLE-SPHERE-STATIC-COVERAGE-423-REPACK01","spellId":ID,
  "acceptedConditionalWitness":{"classification":"OWNER_ADOPTED_TEST_ONLY_HYPOTHETICAL_WITNESS","witnessId":replayobj["id"],
   "caseId":replayobj["initialState"]["caseId"],"archive":wzref,"replayMember":replayref,
   "premiseIds":replayobj["scope"]["adoptedPremiseIds"],"independentAudit":bind(WD/"INDEPENDENT_AUDIT_423_REPACK01.json"),
   "directorReadback":bind(WD/"DIRECTOR_READBACK_423_REPACK01.json"),"events":68,"forwardOperations":445,
   "inverseOperations":445,"campaignEventClaim":False,"runtimeExecutionClaim":False,"sealIssued":False},
  "preservedHistoricalCases":{"count":14,"byteExact":True,"archive":histref,"records":historical,"b4Disposition":b4,
   "historicalB5":a["coverageReconciliation"]["historicalB5"],"crownCommandCaseId":a["coverageReconciliation"]["crownCommandCaseId"]},
  "closedBlockerIds":[BLOCKER],"scope":"Static authored-procedure coverage only; Witness423 is separate TEST_ONLY evidence; B4 remains incomplete."}
 covref=write(cdir/"CASE_COVERAGE.json",cov)
 derived=copy.deepcopy(proc); derived.update({"accepted":True,"applied":True,"holds":[],"closedBlockerIds":[BLOCKER],
  "resolvedBlockerIds":[BLOCKER],"priorReassessmentPreserved":copy.deepcopy(proc.get("reassessment",[])),
  "reassessment":[{"currentId":BLOCKER,"decision":"CLOSED_FOR_STATIC_AUTHORED_REVIEW_ONLY","evidence":replayobj["id"],
   "limitation":"B4 historical evidence remains incomplete and byte-exact; Witness423 is a separate hypothetical TEST_ONLY witness."}],
  "status":"DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED"})
 model={"schemaVersion":1,"id":"RANK9-INVULNERABLE-SPHERE-STATIC-REVIEWED-423-REPACK01",
  "reviewId":a["id"],"status":"REVIEWED_AUTHORED_STATIC_PROCEDURE","acceptedIds":[ID],"heldIds":[],
  "spells":[{"id":ID,"name":native["name"],"nativeCard":copy.deepcopy(native),
   "procedure":{"procedureContent":proc["procedureText"],"selectedRules":copy.deepcopy(proc["selectedRules"]),
    "sharedContract":copy.deepcopy(proc["sharedRules"])},
   "sourceProcedureRecord":copy.deepcopy(proc),"directorProcedureRecord":derived,"sourceProcedureBinding":sref,
   "qualificationIds":list(a["qualificationHoldIds"]),"closedBlockerIds":[BLOCKER],"caseEvidence":covref}],
  "sharedRequirements":copy.deepcopy(proc["sharedRules"]),"caseEvidence":covref,"sourceProcedureBinding":sref,
  "directorAcceptance":arref,"directorDeliveryReceipt":dref,"runtimeSelectionEnabled":False,
  "implementationApproved":False,"humanPlayApproved":False,"balanceApproved":False,"cosmologyModified":False,
  "domainClosure":False,"releaseApproved":False}
 mp=cdir/"MODEL.json"; mr=write(mp,model)
 man={"id":"INVULNERABLE-SPHERE-STATIC-REVIEWED-423-REPACK01-PACKAGE",
  "files":[mr,covref,sref,arref,dref,wzref,histref],"scope":"Authored review only; no catalog, source, runtime or downstream promotion."}
 manp=cdir/"CANDIDATE_PACKAGE_MANIFEST.json"; manref=write(manp,man)
 app={"id":"INVULNERABLE-SPHERE-STATIC-APPLICATION-423-REPACK01","recordedAtUtc":stamp(),
  "acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIds":[BLOCKER],"directorAcceptance":arref,"deliveryReceipt":dref,
  "candidateModel":mr,"caseCoverage":covref,"candidatePackageManifest":manref,
  "indexBefore":bind(INDEX,idxraw),"indexBackup":bind(backup,idxraw),"sourceProcedureBeforeAfter":sref,
  "catalogCommittedBlobBeforeAfter":bind(CATALOG,commitcat),"authorityBefore":q0["currentAuthority"],"authorityAfter":after,
  "retainedQualificationHoldIds":list(a["qualificationHoldIds"]),"all14HistoricalCaseMembersByteExact":True,
  "historicalB4RemainsIncomplete":True,"otherIdentityRowsChanged":False,"catalogChanged":False,
  "sourceProcedureChanged":False,"runtimeSelectionEnabled":False,"runtimeExecuted":False,
  "scope":"Authored-review index only; no native catalog/source procedure or runtime promotion."}
 appp=appdir/"APPLICATION.json"; appref=write(appp,app)
 idx1=copy.deepcopy(idx0); row=copy.deepcopy(row0)
 row.update({"authoredStatus":"reviewed-authored-operational-playtest",
  "procedureFile":"../spell_candidates/rank9invulnerablesphere_reviewed_423/MODEL.json",
  "procedurePointer":"/spells/0/procedure","wholeCardPointer":"/spells/0","procedureTextPointer":"/spells/0/procedure/procedureContent",
  "wholeCardIdField":"id","sourceCatalogWholeCardPointer":"/spells/96","directorProcedureRecordPointer":"/spells/0/directorProcedureRecord",
  "sharedRulesPointer":"/sharedRequirements","spellLocalRequirementsPointer":"/spells/0/procedure","runtimeSelectionEnabled":False,
  "completeEvidenceRoot":CANDREL.as_posix(),"completeEnvelopeBinding":mr,"caseEvidenceBindings":covref,
  "candidatePackageManifestBinding":manref,"authoredAcceptanceReceipt":arref,"authoredApplicationReceipt":appref,
  "directorReturnReceipt":dref,"sourceProcedureBinding":sref,"sourceArchiveBinding":histref,"acceptedWitnessArchiveBinding":wzref,
  "reviewId":appp.name,"accepted":True,"applied":True,"closedBlockerIds":[BLOCKER],
  "retainedQualificationIds":list(a["qualificationHoldIds"]),"historicalCandidateLabelsPreserved":True,"applicationScope":app["scope"]})
 ri=next(i for i,x in enumerate(idx1["entries"]) if x["id"]==ID); idx1["entries"][ri]=row
 idx1["authoredCounts"]={"reviewed":830,"pending":18}; idx1["representationCounts"]["completeReviewedStandaloneProcedures"]=554
 idx1.setdefault("additionalStandaloneEnvelopes",[]).append({"file":row["procedureFile"],"binding":mr,"reviewId":a["id"],
  "acceptedIds":[ID],"unacceptedIds":[],"excludedPendingIds":sorted(set(p0)-{ID}),"authority":arref,"applicationReceipt":appref,
  "caseEvidenceBinding":covref,"candidatePackageManifestBinding":manref,"sourceProcedureBinding":sref,"sourceArchiveBinding":histref,
  "runtimeSelectionEnabled":False,"scope":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_DF218_B04_RUNTIME_DISABLED"})
 assert all(idx0["entries"][i]==idx1["entries"][i] for i in range(len(idx0["entries"])) if i!=ri)
 assert idx1["sourceCatalogSha256"]==idx0["sourceCatalogSha256"]
 p1=[r["id"] for r in idx1["entries"] if r["authoredStatus"]=="pending-authored-procedure"]
 assert len(p1)==18 and set(p1)==set(p0)-{ID}
 ib=enc(idx1); INDEX.write_bytes(ib); ir=bind(INDEX,ib)
 order=[x for x in q0["continuingPriorityOrder"] if x!=ID]
 assert order[0]=="conjure-demiplane-fortress" and set(order)==set(p1)
 queue={"id":"CURRENT-SPELL-QUEUE-423-REPACK01","supersedesQueue":bind(QUEUE0),"currentAuthority":after,
  "currentIndexBinding":ir,"currentCatalogBinding":q0["currentCatalogBinding"],"remainingPendingIds":p1,
  "continuingPriorityOrder":order,"continuingPriorityOrderIsPrioritySubset":False,"nextIdentity":"conjure-demiplane-fortress",
  "nextBlockerIds":["PG200-B06"],"closureTasksRemaining":18,"firstReviewTasksRemaining":0,"acceptedUnapplied":0,
  "acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIdsThisStep":[BLOCKER],"application":appref,
  "pendingIdentityAuditPath":(BASE/"CURRENT18_PENDING_IDENTITY_AUDIT_423_REPACK01.json").relative_to(ROOT).as_posix(),
  "currentHandoffPath":(BASE/"CURRENT_HANDOFF_423_REPACK01.json").relative_to(ROOT).as_posix(),
  "runtimeExecuted":False,"runtimeSelectionEnabled":False,
  "retainedHolds":"18 unrelated identities and all Sphere qualification holds remain; historical B4 remains incomplete."}
 qp=BASE/"CURRENT_SPELL_QUEUE_423_REPACK01.json"; qr=write(qp,queue)
 pending={"id":"CURRENT18-PENDING-IDENTITY-AUDIT-423-REPACK01","recordedAtUtc":stamp(),"authority":after,
  "pendingCount":18,"pendingIds":p1,"indexBinding":ir,"currentQueueBinding":qr,"nextPriorityOrder":order,
  "acceptedUnappliedIds":[],"nextStep":"Conjure Demiplane Fortress / PG200-B06; continue scoped TEST_ONLY witness work and obtain GPT Director readback."}
 pp=BASE/"CURRENT18_PENDING_IDENTITY_AUDIT_423_REPACK01.json"; pr=write(pp,pending)
 hand={"id":"CURRENT-HANDOFF-423-REPACK01","supersedes":HANDOFF0.relative_to(ROOT).as_posix(),
  "queue":qr,"pendingIdentityAudit":pr,"authority":after,"continuingPriorityOrder":order,"closureTasksRemaining":18,
  "firstReviewTasksRemaining":0,"nextStep":"Conjure Demiplane Fortress / PG200-B06: continue source-bound witness work. Owner adopted the exact W01 successor overlays and W09 Repack01 as TEST_ONLY construction premises; obtain GPT Director readback before acceptance.",
  "currentApplication":appref,"nativeCatalogAndDownstreamGatesUnchanged":True,
  "W09Adoption":{"proposalId":"OWNER-PG328-W09-SUPPORT-426-REPACK01-TESTONLY-PROPOSAL",
   "sha256":"f4dfbf3403c63f603ef188be972c4425cc627309d4fb77cc86934afecd6b8a9d",
   "scope":"Hypothetical PG328-W09-R1 construction only; no seal, acceptance/application, canon or Queue404 change."}}
 hp=BASE/"CURRENT_HANDOFF_423_REPACK01.json"; hr=write(hp,hand)
 assert CATALOG.read_bytes()==catraw and SOURCE.read_bytes()==sourceraw and backup.read_bytes()==idxraw
 assert bind(INDEX)["sha256"]==ir["sha256"] and read(pp)["currentQueueBinding"]["sha256"]==qr["sha256"]
 assert read(hp)["queue"]["sha256"]==qr["sha256"] and read(hp)["pendingIdentityAudit"]["sha256"]==pr["sha256"]
 assert read(INDEX)["authoredCounts"]=={"reviewed":830,"pending":18}
 op={"id":"INVULNERABLE-SPHERE-INDEX-OPERATIONS-423-REPACK01","beforeBinding":bind(INDEX,idxraw),
  "afterBinding":ir,"backup":bind(backup,idxraw),"acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIds":[BLOCKER],
  "otherRowsUnchanged":True,"catalogByteExact":CATALOG.read_bytes()==catraw,"sourceProcedureByteExact":SOURCE.read_bytes()==sourceraw,
  "inverseRestoresExactIndex":backup.read_bytes()==idxraw}
 opref=write(appdir/"INDEX_OPERATIONS.json",op)
 checks=["exact Director acceptance matches delivery receipt","all bound source hashes verified","all 14 historical case members byte-exact",
  "423 witness replay and independent 387-check audit pass","only Sphere authored-index row changed","one standalone envelope appended",
  "authority exactly 830/18/0 and 554/173","pending inventory exactly baseline minus Sphere",
  "next priority Fortress / PG200-B06","catalog and retained procedure byte-exact","B4 remains incomplete and 10 holds remain",
  "runtime and downstream gates remain closed","queue, pending audit and handoff cross-bind","backup preserves exact prior index"]
 val={"id":"INVULNERABLE-SPHERE-STATIC-APPLICATION-VALIDATION-423-REPACK01","recordedAtUtc":stamp(),"status":"PASS",
  "checks":[{"check":x,"passed":True} for x in checks],"checkCount":len(checks),"passedChecks":len(checks),"failedChecks":0,
  "acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIds":[BLOCKER],"authority":after,"index":ir,"application":appref,
  "acceptance":arref,"deliveryReceipt":dref,"caseCoverage":covref,"candidateModel":mr,"candidatePackageManifest":manref,
  "indexOperations":opref,"queue":qr,"pendingIdentityAudit":pr,"handoff":hr,"catalogChanged":False,
  "sourceProcedureChanged":False,"runtimeSelectionEnabled":False,"nextIdentity":"conjure-demiplane-fortress"}
 vp=appdir/"VALIDATION.json"; vr=write(vp,val)
 (BASE/"CURRENT_SPELL_REVIEW_SNAPSHOT_423_REPACK01.md").write_text(
  "# Spell review snapshot — Invulnerable Sphere 423 Repack01\n\n"
  "**830 applied / 18 pending / 0 accepted-unapplied; 554 complete standalone procedures / 173 scoped interfaces.**\n\n"
  "The Director accepted and the authored-review index applies Invulnerable Sphere / DF218-B04 only. Witness423 is separate hypothetical TEST_ONLY evidence. The 14 historical cases remain byte-exact; B4 remains incomplete; all 10 qualification holds remain. The source procedure and native catalog are unchanged; runtime remains disabled.\n\n"
  "Next priority: Conjure Demiplane Fortress / PG200-B06. The owner adopted the exact Fortress W01 successor overlays and W09 Repack01 for TEST_ONLY construction. GPT Director readback is required before acceptance.\n\n"
  f"Validation: {vp.relative_to(ROOT).as_posix()} (SHA-256 {vr['sha256']}).\n",encoding="utf-8",newline="\n")
 print(json.dumps({"status":"PASS","acceptedAppliedIds":[ID],"authority":after,"validation":vr,
  "index":ir,"queue":qr,"pendingIdentityAudit":pr,"handoff":hr,"nextIdentity":"conjure-demiplane-fortress"},indent=2))
if __name__=="__main__": main()
