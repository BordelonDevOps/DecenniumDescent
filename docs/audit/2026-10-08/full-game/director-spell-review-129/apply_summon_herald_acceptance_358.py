import copy, datetime as dt, hashlib, json, pathlib, subprocess, zipfile, zlib

R = pathlib.Path.cwd()
A = R / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID, NAME, BLOCKER = "summon-herald-of-the-planes", "Summon Herald of the Planes", "SH202-B02"
RES = [f"SH358-R{i}" for i in range(1, 6)]
NEXT, NEXT_GROUP, NEXT_BLOCKERS = "banishment-gate", "rank9-planar-gates5", ["PG200-B03", "PG200-B04"]
INDEX = R / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = R / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0, P0, H0 = [A / x for x in ("CURRENT_SPELL_QUEUE_357.json", "CURRENT21_PENDING_IDENTITY_AUDIT_357.json", "CURRENT_HANDOFF_357.json")]
PK = A / "rank9_summon_herald_w02_witness_358_repack04"
ARCHIVE = PK / "DD_Rank9_SummonHerald_SH332_W02_W03_W04_TESTONLY_358_Repack04.zip"
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonherald_reviewed_359")
PKG, MANUSCRIPT = R / PKG_REL, R / "DescentReviewChanges/ReviewBible/docs/spells/candidates/SUMMON_HERALD_OF_THE_PLANES_REVIEWED_359.md"
OUT = {k: A / v for k, v in {
 "decision":"SUMMON_HERALD_SH332_REPACK04_DIRECTOR_DECISION.json","accept":"SUMMON_HERALD_SH332_REPACK04_ACCEPTANCE.json",
 "app":"SUMMON_HERALD_SH332_REPACK04_APPLICATION.json","receipt":"SUMMON_HERALD_SH332_REPACK04_RECEIPT.json",
 "ops":"SUMMON_HERALD_SH332_REPACK04_INDEX_OPERATIONS.json","validation":"SUMMON_HERALD_SH332_REPACK04_APPLICATION_VALIDATION.json",
 "backup":"authored_review_index.before_summon_herald_359.json","queue":"CURRENT_SPELL_QUEUE_359.json",
 "pending":"CURRENT20_PENDING_IDENTITY_AUDIT_359.json","handoff":"CURRENT_HANDOFF_359.json",
 "snapshot":"CURRENT_SPELL_REVIEW_SNAPSHOT_359.md"}.items()}
BEFORE = {"reviewedApplied":827,"pending":21,"acceptedUnapplied":0,"completeStandaloneProcedures":551,"scopedInterfaces":173}
AFTER = {"reviewedApplied":828,"pending":20,"acceptedUnapplied":0,"completeStandaloneProcedures":552,"scopedInterfaces":173}
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750"
RULING = {
 "rulingId":"SH332-W02-W03-W04-358-REPACK04-DIRECTOR-ACCEPT","decision":"SEALED_ACCEPT","spellId":ID,
 "explicitAcceptance":"I accept Summon Herald of the Planes / SH202-B02 and authorize application of this sealed acceptance.",
 "archive":{"name":ARCHIVE.name,"bytes":511437,"sha256":"8ba903b84347ec7e4d450f495e2322d802770403745f61269d4bbbbf7d8e75ed"},
 "independentVerification":{"manifestMemberHashes":"PASS: 11/11","exactMemberSet":"PASS: 11 payloads plus manifest; no extras or duplicates","CRCs":"PASS",
 "sourceBinding":"PASS: repository Ready text and sealed W01 clock exception","forwardTransitions":281,"inverseTransitions":281,
 "completeStateRestorations":4,"snapshotsPatchesAndHashes":"PASS","mirroredW02Calendars":"PASS","orderedSlotsAndExactlyOnceRefreshes":"PASS"},
 "witnesses":{"W01":"PASS_PRESERVED","W02":"PASS","W03":"PASS","W04":"PASS"},
 "residuals":{f"SH358-R{i}":("PASS_CLOSED" if i==5 else "PASS_PRESERVED") for i in range(1,6)},
 "R5Findings":{"paidPreparationMs":0,"releaseAndManifestationMs":1000,"absoluteDeadlineMs":60000,"remainingDurationAtReleaseMs":59000,
 "deadlineEventIndex":104,"followingBRegularStartEventIndex":105,
 "endingState":"Call and concentration end; blocked return is recorded; reservation is released and returnOutstanding becomes true before B regular-start refresh.",
 "laterState":"No revival or deadline reset. Independent recovery at 75000ms restores the same body and carried token to the original location.",
 "costs":"Both legal casts retain their 26-RP payments; each caster finishes with 38 RP.",
 "clockInterpretation":"Release begins manifestation only. The explicit paid-preparation deadline remains controlling."},
 "acceptedIds":[ID],"appliedIds":[],"heldIds":[],"blockerIds":[],"closedBlockerIds":[BLOCKER],"closedResidualIds":RES,
 "remainingResidualIds":[],"remainingDefectPaths":[],"applicationAuthorized":True,"applicationPerformed":False,
 "applicationScope":"Apply only this identity's sealed acceptance to the authored review index and corresponding queue records under the standing instruction.",
 "boundAuthorityBeforeThisRuling":{"applied":827,"pending":21,"acceptedUnapplied":0,"completeProcedures":551,"scopedInterfaces":173,"firstReviews":0,"closureTasks":21},
 "authorityRecordsModified":False,"preservedBoundaries":["W01 approval and profile remain unchanged.","W02-W04 are conditional TEST_ONLY evidence; no campaign facts are established.",
 "Unrelated identities and dispositions remain unchanged.","Native catalog/source and runtime/downstream gates remain unchanged or disabled."]}

def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2)+"\n").encode()
def write(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(enc(x))
def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f"{zlib.crc32(b)&0xffffffff:08x}"
def bind(p,b=None):
 b=p.read_bytes() if b is None else b
 return {"path":p.relative_to(R).as_posix(),"bytes":len(b),"sha256":sha(b),"crc32":crc(b)}

def main():
 assert subprocess.check_output(["git","branch","--show-current"],cwd=R,text=True).strip()=="main"
 assert not PKG.exists() and not MANUSCRIPT.exists() and all(not p.exists() for p in OUT.values()), "Refusing to overwrite application outputs."
 ir,cr=INDEX.read_bytes(),CATALOG.read_bytes(); ix,cat=read(INDEX),read(CATALOG)
 q0,p0,h0=map(read,(Q0,P0,H0))
 assert ix["authoredCounts"]=={"reviewed":827,"pending":21} and ix["representationCounts"]["completeReviewedStandaloneProcedures"]==551
 assert q0["currentAuthority"]==p0["authority"]==BEFORE and q0["pendingCount"]==p0["pendingCount"]==21 and q0["acceptedUnapplied"]==0
 ids=list(p0["pendingIds"]); assert len(ids)==21 and ID in ids
 row0=copy.deepcopy(next(e for e in ix["entries"] if e["id"]==ID)); card=copy.deepcopy(next(s for s in cat["spells"] if s["id"]==ID))
 assert row0["authoredStatus"]=="pending-authored-procedure" and row0["wholeCardPointer"]=="/spells/287" and card["status"]=="blocked-pending-operational-review"
 assert bind(INDEX)["sha256"]==p0["indexBinding"]["sha256"]
 delivery=read(PK/"DELIVERY.json"); assert delivery["archiveSHA256"]==RULING["archive"]["sha256"] and delivery["archiveBytes"]==RULING["archive"]["bytes"]
 assert ARCHIVE.stat().st_size==511437 and sha(ARCHIVE.read_bytes())==RULING["archive"]["sha256"]
 manifest=read(PK/"MEMBER_MANIFEST.json")
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); assert z.testzip() is None and len(names)==12 and len(set(names))==12
  declared={x["path"]:x for x in manifest["members"]}
  assert manifest["memberCountExcludingSelf"]==11 and set(declared)==set(names)-{"MEMBER_MANIFEST.json"}
  for n,x in declared.items():
   b=z.read(n); assert len(b)==x["bytes"] and sha(b)==x["sha256"]
 ver=json.loads(subprocess.check_output(["python",str(PK/"verify_herald_w02_witness_358.py")],cwd=R,text=True,encoding="utf-8"))
 assert ver["status"]=="PASS" and ver["checks"]==14 and ver["forwardTransitions"]==ver["inverseTransitions"]==281 and not ver["failedChecks"]
 assert RULING["applicationAuthorized"] and not RULING["remainingResidualIds"]
 stamp=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
 ar,dr,mr,vr=map(bind,(ARCHIVE,PK/"DELIVERY.json",PK/"MEMBER_MANIFEST.json",PK/"verify_herald_w02_witness_358.py"))
 q0r,p0r,h0r=map(bind,(Q0,P0,H0)); commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=R,text=True).strip()
 commitref={"branch":"main","commit":commit,"url":f"https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}"}
 decision={"id":RULING["rulingId"],"recordedAtUtc":stamp,"status":"SEALED_ACCEPT_SUMMON_HERALD_SH202_B02_REPACK04",**copy.deepcopy(RULING),
  "source":{"service":"ChatGPT","conversationTitle":"Review Time Stop Witness Evidence","url":URL},"sourceCommit":commitref,
  "acceptedPacket":ar,"deliveryManifest":dr,"manifest":mr,"independentVerifier":vr,"queueAtDecision":BEFORE,
  "authorityAfterAuthorizedApplicationExpected":AFTER,"nativeCatalogChanged":False,"nativeSourceChanged":False,
  "runtimeSelectionEnabled":False,"runtimeExecuted":False,"gatesStillClosed":["runtime","implementation","human-play","balance","cosmology","domain-closure","completion","release"]}
 write(OUT["decision"],decision); dref=bind(OUT["decision"])
 acceptance={"id":"SUMMON-HERALD-SH332-REPACK04-EXACT-AUTHORED-ACCEPTANCE","recordedAtUtc":stamp,
  "status":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_APPLICATION_AUTHORIZED_RUNTIME_DISABLED","acceptedIds":[ID],"appliedIds":[],"heldIds":[],
  "closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"applicationAuthorizedIds":[ID],"directorDecision":dref,"acceptedPacket":ar,
  "deliveryManifest":dr,"independentVerification":vr,"authorityBeforeApplication":BEFORE,"authorityAfterApplicationExpected":AFTER,
  "scope":"Authored-index application only; W02-W04 remain TEST_ONLY; no catalog/source promotion or runtime enablement."}
 write(OUT["accept"],acceptance); aref=bind(OUT["accept"])
 # A minimal, traceable static envelope: every factual claim is bound to GPT's accepted witness package.
 evidence={"acceptedArchive":ar,"deliveryManifest":dr,"manifest":mr,"independentVerification":vr,"directorDecision":dref,"acceptance":aref,
  "w01":"01_SH332_W01_CLEAN_REAFFIRMATION_358.json","w02Authorization":"OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json",
  "w02State":"02_SH332_W02_AUTHORIZED_TEST_STATE_358.json","w03":"04_SH332_W03_LIFECYCLE_WITNESSES_358.json",
  "w04":"05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json","readyRule":"08_READY_ACTION_RULE_BINDING_358.json",
  "fixtureClassification":"TEST_ONLY_AUTHORED_CONDITIONAL_WITNESS","campaignEventClaimed":False,"runtimeExecutionClaimed":False,
  "closedResidualIds":RES}
 procedure={"id":"SUMMON-HERALD-SH202-B02-STATIC-AUTHORED-359","spellId":ID,"status":"director-accepted static authored procedure; authored index applied; runtime remains disabled",
  "accepted":True,"applied":True,"scope":"Summon Herald of the Planes / SH202-B02; SH358-R1 through SH358-R5 closed.",
  "directorDecision":dref,"sourceArchive":ar,"nativeCatalogWholeCardPointer":row0["wholeCardPointer"],"nativeCardPreserved":card,
  "acceptedReviewEvidence":evidence,"witnesses":RULING["witnesses"],"verification":RULING["independentVerification"],
  "testOnlyLimit":"All W02-W04 evidence is hypothetical TEST_ONLY; no campaign event, actual consent, location, availability, or runtime execution is asserted.",
  "runtimeSelectionEnabled":False,"runtimeExecuted":False,"implementationApproved":False,"releaseApproved":False}
 pkg={"schemaVersion":1,"moduleId":"rank9summonherald-reviewed-359","status":"ONE_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
  "scope":"Authored-review index envelope only; no native operational promotion.","acceptedIds":[ID],"excludedPendingIds":sorted(set(ids)-{ID}),
  "sharedRequirements":{"runtimeSelectionEnabled":False,"catalogSourceStatusChanged":False},
  "spells":[{"id":ID,"name":NAME,"position":287,"procedure":{"id":procedure["id"],"spellId":ID,"status":procedure["status"],
   "accepted":True,"applied":True,"procedureContent":json.dumps(evidence,ensure_ascii=False,sort_keys=True),"directorDecisionId":RULING["rulingId"],
   "closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"runtimeSelectionEnabled":False},"directorProcedureRecord":procedure,
   "nativeCardUnchanged":True,"runtimeSelectionEnabled":False}],
  "sourceArchive":ar,"directorDecision":dref,"acceptance":aref,"runtimeSelectionEnabled":False,"runtimeExecuted":False,
  "implementationApproved":False,"humanPlaytested":False,"balanceApproved":False,"cosmologyModified":False,"completionApproved":False,"releaseApproved":False}
 write(PKG/"MODEL.json",pkg); write(PKG/"PROCEDURE_RECORD.json",procedure)
 write(PKG/"CASE_COVERAGE.json",{"archive":ar,"directorDecision":dref,"independentVerification":vr,"witnesses":RULING["witnesses"],
  "closedResidualIds":RES,"forwardTransitions":281,"inverseTransitions":281,"completeStateRestorations":4,
  "fixtureClassification":"TEST_ONLY_AUTHORED_CONDITIONAL_WITNESS","campaignEventClaimed":False,"runtimeExecutionClaimed":False})
 write(PKG/"SOURCE_CARD.json",{"id":ID,"sourceCatalogWholeCardPointer":row0["wholeCardPointer"],"gitBlobBinding":bind(CATALOG),
  "card":card,"changed":False,"runtimeSelectionEnabled":False})
 write(PKG/"EVIDENCE_BINDINGS.json",evidence)
 pkgmembers=[]
 for p in sorted(PKG.iterdir()):
  if p.is_file():
   b=p.read_bytes();pkgmembers.append({"path":p.name,"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
 write(PKG/"CANDIDATE_PACKAGE_MANIFEST.json",{"id":"SUMMON-HERALD-SH332-PACKAGE-MANIFEST-359","memberCountExcludingSelf":len(pkgmembers),"members":pkgmembers,"selfExcluded":True})
 modelref=bind(PKG/"MODEL.json"); pmref=bind(PKG/"CANDIDATE_PACKAGE_MANIFEST.json")
 write(MANUSCRIPT,{"title":NAME+" — reviewed authored evidence 359","spellId":ID,"directorRulingId":RULING["rulingId"],
  "accepted":True,"applied":True,"summary":"GPT accepted SH202-B02 and closed SH358-R1–R5. W02-W04 remain TEST_ONLY. Native catalog/runtime/downstream gates remain unchanged or disabled.",
  "archive":ar,"candidatePackage":modelref,"application":OUT["app"].relative_to(R).as_posix()})
 receipt={"id":"SUMMON-HERALD-SH332-REPACK04-APPLICATION-RECEIPT-359","recordedAtUtc":stamp,"acceptedIds":[ID],"appliedIds":[ID],
  "applicationAuthorized":True,"directorRulingId":RULING["rulingId"],"archive":ar,"indexPath":INDEX.relative_to(R).as_posix(),
  "authorityBefore":BEFORE,"authorityAfter":AFTER,"nativeCatalogChanged":False,"runtimeSelectionEnabled":False}
 write(OUT["receipt"],receipt); rref=bind(OUT["receipt"])
 app={"id":"SUMMON-HERALD-SH332-REPACK04-AUTHORED-APPLICATION-359","recordedAtUtc":stamp,
  "status":"APPLIED_ONE_STATIC_AUTHORED_PROCEDURE_AUTHORED_INDEX_ONLY_RUNTIME_DISABLED","acceptedIds":[ID],"appliedIds":[ID],"heldIds":[],
  "closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"applicationAuthorizedIds":[ID],"directorDecision":dref,"acceptance":aref,"receipt":rref,
  "archive":ar,"deliveryManifest":dr,"independentVerification":vr,"candidatePackage":modelref,"candidatePackageManifest":pmref,
  "applicationScope":"One authored_review_index.json entry and one static authored-review envelope only.",
  "indexPath":INDEX.relative_to(R).as_posix(),"indexBindingBefore":bind(INDEX,ir),"authorityBefore":BEFORE,"authorityAfterExpected":AFTER,
  "sourceProcedureChanged":False,"nativeCatalogChanged":False,"runtimeSelectionEnabled":False,"runtimeExecuted":False,
  "otherPendingIdentitiesChanged":False,"unrelatedDispositionsChanged":False}
 write(OUT["app"],app); appref=bind(OUT["app"]); OUT["backup"].write_bytes(ir)
 ix1=copy.deepcopy(ix); row1=next(e for e in ix1["entries"] if e["id"]==ID)
 row1.update({"authoredStatus":"reviewed-authored-operational-playtest","procedureFile":"../spell_candidates/rank9summonherald_reviewed_359/MODEL.json",
  "procedurePointer":"/spells/0/procedure","wholeCardPointer":"/spells/0","sourceStatus":row0["sourceStatus"],"priorCatalogSelectionStatusUnchanged":True,
  "wholeCardIdField":"id","sourceCatalogWholeCardPointer":row0["wholeCardPointer"],"procedureTextPointer":"/spells/0/procedure/procedureContent",
  "directorProcedureRecordPointer":"/spells/0/directorProcedureRecord","sharedRulesPointer":"/sharedRequirements","spellLocalRequirementsPointer":"/spells/0/procedure",
  "manuscript":"../../../docs/spells/candidates/SUMMON_HERALD_OF_THE_PLANES_REVIEWED_359.md","reviewId":OUT["app"].name,"runtimeSelectionEnabled":False,
  "historicalCandidateLabelsPreserved":True,"completeEvidenceRoot":PKG_REL.as_posix(),"completeEnvelopeBinding":modelref,
  "caseEvidenceBindings":bind(PKG/"CASE_COVERAGE.json"),"sourceArchiveBinding":ar,"deliveryManifestBinding":dr,
  "candidatePackageManifestBinding":pmref,"authoredAcceptanceReceipt":aref,"authoredApplicationReceipt":appref,"directorReturnReceipt":rref,
  "accepted":True,"applied":True,"closedBlockerIds":[BLOCKER],"closedResidualIds":RES,
  "retainedQualifications":["W02-W04 are hypothetical TEST_ONLY evidence; no campaign occurrence is asserted.","W01 remains unchanged.","Native catalog/source and downstream gates remain unchanged or disabled."],
  "applicationScope":"Authored review index application only; no native spell procedure or catalog promotion."})
 ix1["additionalStandaloneEnvelopes"].append({"file":"../spell_candidates/rank9summonherald_reviewed_359/MODEL.json","binding":modelref,
  "reviewId":OUT["app"].name,"acceptedIds":[ID],"unacceptedIds":[],"excludedPendingIds":sorted(set(ids)-{ID}),
  "authority":aref,"applicationReceipt":appref,"directorDecision":dref,"sourceArchive":ar,"deliveryManifest":dr,
  "caseCoverageBinding":bind(PKG/"CASE_COVERAGE.json"),"candidatePackageManifestBinding":pmref,
  "scope":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_SH202_B02_RUNTIME_DISABLED","runtimeSelectionEnabled":False})
 ix1["authoredCounts"]={"reviewed":828,"pending":20};ix1["representationCounts"]["completeReviewedStandaloneProcedures"]=552
 pids=[x for x in ids if x!=ID]; assert len(pids)==20 and {e["id"] for e in ix1["entries"] if e.get("authoredStatus")=="pending-authored-procedure"}==set(pids)
 INDEX.write_bytes(enc(ix1)); iref=bind(INDEX)
 priority=[x for x in q0["continuingPriorityOrder"] if x!=ID]; assert priority[0]==NEXT and set(priority)==set(pids)
 q1=copy.deepcopy(q0);q1.update({"id":"CURRENT-SPELL-QUEUE-359","recordedAtUtc":stamp,"supersedesQueue":Q0.relative_to(R).as_posix(),
  "currentAuthority":AFTER,"authority":AFTER,"pendingCount":20,"acceptedUnapplied":0,"currentIndexBinding":iref,
  "continuingPriorityOrder":priority,"remainingPendingIds":pids,"nextGroup":NEXT_GROUP,"nextPendingIds":[NEXT],"nextPendingCount":1,
  "next":NEXT+" / PG200-B03, PG200-B04 — prepare source-bound crossing and cell-local lifecycle witnesses.",
  "activeReview":{"scopeIds":[NEXT],"blockerIds":NEXT_BLOCKERS,"status":"NEXT PRIORITY; source-bound crossing/lifecycle witnesses required"},
  "lastDirectorReturn":RULING["rulingId"],"currentReturnAcceptedIds":[ID],"currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],"currentReturnBlockers":[],
  "currentReturnDecision":dref,"currentReturnArchive":ar,"currentReturnDelivery":dr,"currentReturnAudit":vr,
  "currentPacketStatus":"SEALED_ACCEPT_AND_AUTHORIZED_AUTHORED_INDEX_APPLICATION_COMPLETED_FOR_SUMMON_HERALD_ONLY",
  "currentPacket":{"path":ar["path"],"status":"SEALED_ACCEPTED_AND_APPLIED"},
  "currentPreparation":{"scopeIds":[ID],"blockerIds":[BLOCKER],"path":ar["path"],"status":"ACCEPTED_AND_APPLIED"},
  "acceptedIds":[ID],"appliedIds":[ID],"heldIds":[],"acceptedThisStep":[ID],"appliedThisStep":[ID],"applicationPerformed":True,
  "closedBlockerIdsThisStep":[BLOCKER],"closedResidualIdsThisStep":RES,"nextIdentity":NEXT,"nextBlockerIds":NEXT_BLOCKERS,
  "nextActionablePriority":{"identity":NEXT,"blockerIds":NEXT_BLOCKERS},"currentDirectorRulingSupplement":dref["path"],
  "currentDirectorReturn":dref,"currentDirectorSourceCheck":dref,"currentApplication":{"path":OUT["app"].relative_to(R).as_posix(),**appref},
  "currentPendingIdentityAudit":OUT["pending"].relative_to(R).as_posix(),"currentPendingIdentityAuditPath":OUT["pending"].relative_to(R).as_posix(),
  "pendingIdentityAudit":OUT["pending"].relative_to(R).as_posix(),"currentHandoff":OUT["handoff"].relative_to(R).as_posix(),
  "currentHandoffPath":OUT["handoff"].relative_to(R).as_posix(),"separatelyRetainedHolds":[x for x in q0.get("separatelyRetainedHolds",[]) if x!=ID],
  "closureTasksRemaining":20,"firstReviewTasksRemaining":0,"directorConnectionStatus":"GPT sealed-accepted and authorized Herald application.",
  "canonicalFilesChanged":False,"runtimeExecuted":False,"githubChanges":False,"currentApplicationValidation":OUT["validation"].relative_to(R).as_posix()})
 write(OUT["queue"],q1); qr=bind(OUT["queue"])
 p1=copy.deepcopy(p0);p1.update({"id":"CURRENT20-PENDING-IDENTITY-AUDIT-359","recordedAtUtc":stamp,
  "supersedes":{"path":P0.relative_to(R).as_posix(),**bind(P0)},"status":"PASS_CURRENT_828_20_SUMMON_HERALD_APPLIED_NEXT_BANISHMENT_GATE",
  "authority":AFTER,"pendingCount":20,"pendingIds":pids,"acceptedIds":[ID],"appliedIds":[ID],"indexBinding":iref,
  "currentQueueBinding":qr,"currentHandoff":OUT["handoff"].relative_to(R).as_posix(),"closureTasksRemaining":20,"firstReviewTasksRemaining":0,
  "nextGroup":NEXT_GROUP,"nextPendingIds":[NEXT],"nextPendingCount":1,"nextIdentity":NEXT,"nextBlockerIds":NEXT_BLOCKERS,
  "nextStep":"Prepare current-authority Banishment Gate / PG200-B03 and PG200-B04 evidence; preserve accepted AC5 source/closures and prior matched cases; supply source-legal nonmatching crossings and cell-local lifecycle witnesses.",
  "currentBlocker":NEXT_BLOCKERS[0],"continuingPriorityOrder":priority,"remainingPendingIds":pids,"heldThisStep":[],"acceptedThisStep":[ID],"appliedThisStep":True,
  "applicationPerformed":True,"canonicalFilesChanged":False,"currentReturnAcceptedIds":[ID],"currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],
  "currentReturnBlockers":[],"currentReturnDecision":dref,"currentReturnArchive":ar,"currentReturnDelivery":dr,"currentReturnAudit":vr,
  "currentPacketStatus":"SEALED_ACCEPTED_AND_AUTHORIZED_APPLICATION_COMPLETED_FOR_SUMMON_HERALD_ONLY","currentPacket":ar["path"],
  "closedBlockerIdsThisStep":[BLOCKER],"closedResidualIdsThisStep":RES,
  "lastDirectorReturn":{"decisionId":RULING["rulingId"],"acceptedIds":[ID],"appliedIds":[ID],"heldIds":[],"blockerIds":[],
   "closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"applicationAuthorized":True}})
 write(OUT["pending"],p1); pr=bind(OUT["pending"])
 h1=copy.deepcopy(h0);closed=list(h1.get("closedBlockerIds",[]))
 if BLOCKER not in closed: closed.append(BLOCKER)
 h1.update({"id":"CURRENT-HANDOFF-359","recordedAtUtc":stamp,"supersedes":h0.get("id"),
  "status":"CURRENT DIRECTOR HANDOFF; SUMMON HERALD ACCEPTED/APPLIED; 20 CLOSURE TASKS REMAIN","authority":AFTER,"currentAuthority":AFTER,
  "scopeIds":pids,"pendingIds":pids,"continuingPriorityOrder":priority,"remainingPendingIds":pids,"blockerIds":NEXT_BLOCKERS,
  "currentBlocker":{"identity":NEXT,"group":NEXT_GROUP,"blockerIds":NEXT_BLOCKERS},"nextPendingGroup":NEXT_GROUP,"nextIdentity":NEXT,"nextBlockerIds":NEXT_BLOCKERS,
  "nextStep":"Prepare current-authority Banishment Gate / PG200-B03/B04 evidence. GPT remains Director; apply only exact sealed acceptances.",
  "currentPacketStatus":"Herald SH202-B02 accepted and applied; next task is Banishment Gate.","currentPreparation":None,
  "acceptedIds":[ID],"appliedIds":[ID],"heldIds":[],"currentReturnAcceptedIds":[ID],"currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],
  "currentReturnBlockers":[],"currentReturnDecision":dref,"currentPacket":ar["path"],"currentDirectorSourceCheck":dref,
  "closedBlockerIds":closed,"closedBlockerIdsThisStep":[BLOCKER],"closedResidualIdsThisStep":RES,"closureTasksRemaining":20,"firstReviewTasksRemaining":0,
  "canonicalFilesChanged":False,"applicationPerformed":True,"runtimeExecuted":False,"queueBinding":qr,"pendingIdentityAuditBinding":pr,
  "currentPendingIdentityAudit":OUT["pending"].relative_to(R).as_posix(),"pendingIdentityAudit":OUT["pending"].relative_to(R).as_posix(),"currentDirectorReturn":dref})
 write(OUT["handoff"],h1);hr=bind(OUT["handoff"])
 checks=[
  ("GPT sealed acceptance authorizes exactly Herald",decision["decision"]=="SEALED_ACCEPT" and decision["acceptedIds"]==[ID] and decision["applicationAuthorized"]),
  ("archive hash, exact manifest, CRC, independent replay pass",ar["sha256"]==RULING["archive"]["sha256"] and ver["status"]=="PASS" and len(declared)==11),
  ("W01-W04 pass and all five residuals close",len(RULING["witnesses"])==4 and len(RES)==5 and not RULING["remainingResidualIds"]),
  ("only the accepted index entry and authored counts change",row1["authoredStatus"]=="reviewed-authored-operational-playtest" and ix1["authoredCounts"]=={"reviewed":828,"pending":20} and all(next(e for e in ix1["entries"] if e["id"]==x)==next(e for e in ix["entries"] if e["id"]==x) for x in pids)),
  ("pending IDs equal old queue minus Herald",len(pids)==20 and set(pids)==set(ids)-{ID}),
  ("queue/pending/handoff cross-bind the 828/20/552/173 authority",q1["currentAuthority"]==p1["authority"]==h1["authority"]==AFTER and q1["currentIndexBinding"]["sha256"]==p1["indexBinding"]["sha256"]==iref["sha256"] and p1["currentQueueBinding"]["sha256"]==qr["sha256"] and h1["queueBinding"]["sha256"]==qr["sha256"] and h1["pendingIdentityAuditBinding"]["sha256"]==pr["sha256"]),
  ("Banishment Gate is next with PG200-B03/B04",q1["nextIdentity"]==p1["nextIdentity"]==h1["nextIdentity"]==NEXT and q1["nextBlockerIds"]==p1["nextBlockerIds"]==NEXT_BLOCKERS),
  ("catalog remains byte-exact and runtime stays disabled",CATALOG.read_bytes()==cr and pkg["runtimeSelectionEnabled"] is False),
  ("index backup is byte-exact",OUT["backup"].read_bytes()==ir)]
 assert all(ok for _,ok in checks),[n for n,ok in checks if not ok]
 write(OUT["ops"],{"id":"SUMMON-HERALD-SH332-REPACK04-INDEX-OPERATIONS-359","beforeBinding":bind(INDEX,ir),"afterBinding":iref,
  "backup":bind(OUT["backup"],ir),"acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIds":[BLOCKER],"closedResidualIds":RES,
  "operations":[{"op":"replace-authored-entry","id":ID,"before":row0,"after":row1},{"op":"append-standalone-envelope","model":modelref},
  {"op":"update-authored-counts","before":{"reviewed":827,"pending":21},"after":{"reviewed":828,"pending":20}},{"op":"increment-procedure-count","before":551,"after":552}],
  "inverseRestoresExactIndex":True,"catalogByteExact":True})
 validation={"id":"SUMMON-HERALD-SH332-REPACK04-APPLICATION-VALIDATION-359","recordedAtUtc":stamp,"status":"PASS",
  "checks":[{"check":n,"passed":ok} for n,ok in checks],"checkCount":len(checks),"passedChecks":len(checks),"failedChecks":0,
  "acceptedIds":[ID],"appliedIds":[ID],"closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"authority":AFTER,
  "index":iref,"application":appref,"decision":dref,"acceptance":aref,"receipt":rref,"archive":ar,"independentVerifier":vr,
  "queue":qr,"pendingIdentityAudit":pr,"handoff":hr,"nativeCatalogChanged":False,"runtimeSelectionEnabled":False,"nextIdentity":NEXT}
 write(OUT["validation"],validation);vref=bind(OUT["validation"])
 OUT["snapshot"].write_text("# Spell review snapshot — Summon Herald SH332 Repack04 application\n\n**828 applied / 20 pending / 0 accepted-unapplied; 552 complete standalone procedures / 173 scoped interfaces; 0 first reviews / 20 closure tasks.**\n\nGPT accepted SH202-B02 and closed SH358-R1–R5. Applied only the static authored-review entry. W02–W04 remain TEST_ONLY; catalog/runtime/downstream gates remain unchanged or disabled.\n\nNext priority: Banishment Gate / PG200-B03 and PG200-B04.\n\nApplication validation: "+vref["path"]+" (SHA-256 "+vref["sha256"]+").\n",encoding="utf-8",newline="\n")
 print(json.dumps({"status":"PASS","acceptedApplied":ID,"closedBlockerIds":[BLOCKER],"closedResidualIds":RES,"authority":AFTER,
  "index":iref,"application":appref,"validation":vref,"queue":qr,"pendingAudit":pr,"handoff":hr,"next":NEXT},indent=2))

if __name__=="__main__": main()
