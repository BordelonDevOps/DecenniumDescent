from __future__ import annotations
import copy, datetime as dt, hashlib, json, pathlib, subprocess, zipfile, zlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID, BLOCKER = "summon-elemental-avatar", "SH202-B01"
NEXT_ID, NEXT_BLOCKER = "summon-herald-of-the-planes", "SH202-B02"
COMMIT = "66e9c2ad2090261526fc3de8daf9bf3a05924fc5"
ARCHIVE_SHA = "d3e5f19d03507e6b20a5bd2259a589504dc5ae86f3baca87fa839730f112c873"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750"
BEFORE = {"reviewedApplied":825,"pending":23,"acceptedUnapplied":0,"completeStandaloneProcedures":549,"scopedInterfaces":173}
AFTER = {"reviewedApplied":826,"pending":22,"acceptedUnapplied":0,"completeStandaloneProcedures":550,"scopedInterfaces":173}
HOLDS = [*[f"SH202-H{i:02d}" for i in range(1,13)],"SH330-Q-EXTERNAL-INPUTS","SH330-Q-TEST-PROVENANCE"]
OMITTED = ["elemental-shell","final-word","invulnerable-sphere","nullification-wave"]
INDEX = ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonelementalavatar_reviewed_351")
PKG = ROOT/PKG_REL
MANUSCRIPT = ROOT/"DescentReviewChanges/ReviewBible/docs/spells/candidates/SUMMON_ELEMENTAL_AVATAR_REVIEWED_351.md"
C = A/"rank9_summon_elemental_avatar_closure_350_delivery"
ARCHIVE = C/"DD_Rank9_SummonElementalAvatar_SH202B01_Closure350.zip"
DELIVERY = C/"DD_Rank9_SummonElementalAvatar_SH202B01_Closure350_DELIVERY.json"
DELTA = C/"SH202_B01_SH330_CONDITIONAL_TRANSITION_DELTA_350.json"
AUDIT = C/"SH202_B01_SH330_INDEPENDENT_TRANSITION_AUDIT_350.json"
REPLAY = C/"SH202_B01_SH330_REPLAY_VERIFICATION_350.json"
VERIFIER = A/"verify_summon_elemental_avatar_closure350.py"
Q0, H0, P0 = A/"CURRENT_SPELL_QUEUE_350.json", A/"CURRENT_HANDOFF_350.json", A/"CURRENT23_PENDING_IDENTITY_AUDIT_350.json"
BACKUP = A/"authored_review_index.before_summon_elemental_avatar_351.json"
DEC = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_DIRECTOR_DECISION.json"
ACC = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_ACCEPTANCE.json"
RCPT = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_RECEIPT.json"
APP = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_APPLICATION.json"
OPS = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_INDEX_OPERATIONS.json"
VAL = A/"SUMMON_ELEMENTAL_AVATAR_CLOSURE350_APPLICATION_VALIDATION.json"
RECON = A/"SH202_B01_SH330_CATALOG_BINDING_RECONCILIATION_351.json"
Q1, H1, P1 = A/"CURRENT_SPELL_QUEUE_351.json", A/"CURRENT_HANDOFF_351.json", A/"CURRENT22_PENDING_IDENTITY_AUDIT_351.json"
SNAPSHOT = A/"CURRENT_SPELL_REVIEW_SNAPSHOT_351.md"

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f"{zlib.crc32(b)&0xffffffff:08x}"
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def write(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(enc(x))
def now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
def bind(p,b=None):
    raw=p.read_bytes() if b is None else b
    return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(raw),"sha256":sha(raw),"crc32":crc(raw)}
def git_blob(p,commit):
    return subprocess.check_output(["git","show",f"{commit}:{p.relative_to(ROOT).as_posix()}"],cwd=ROOT)
def main():
    branch=subprocess.check_output(["git","branch","--show-current"],cwd=ROOT,text=True).strip()
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    assert (branch,head)==("main",COMMIT),(branch,head)
    assert not PKG.exists() and not MANUSCRIPT.exists()
    outputs=[BACKUP,DEC,ACC,RCPT,APP,OPS,VAL,RECON,Q1,H1,P1,SNAPSHOT]
    assert all(not p.exists() for p in outputs)

    index_raw=INDEX.read_bytes(); catalog_raw=CATALOG.read_bytes()
    index0,catalog0=read(INDEX),read(CATALOG)
    q0,h0,p0=map(read,(Q0,H0,P0))
    entry0=copy.deepcopy(next(x for x in index0["entries"] if x["id"]==ID))
    live0={x["id"] for x in index0["entries"] if x.get("authoredStatus")=="pending-authored-procedure"}
    card=copy.deepcopy(next(x for x in catalog0["spells"] if x["id"]==ID))
    assert index0["authoredCounts"]=={"reviewed":825,"pending":23}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"]==549
    assert q0["currentAuthority"]==h0["authority"]==p0["authority"]==BEFORE
    assert sha(index_raw)==q0["currentIndexBinding"]["sha256"]==p0["indexBinding"]["sha256"]
    assert set(p0["pendingIds"])==live0 and len(live0)==23 and ID in live0
    assert card["status"]=="blocked-pending-operational-review" and card["operational"] is None
    assert len(q0["continuingPriorityOrder"])==19
    assert set(p0["pendingIds"])-set(q0["continuingPriorityOrder"])==set(OMITTED)
    assert "timeless-form" in h0["separatelyRetainedHolds"]

    verification=subprocess.run(["python",str(VERIFIER)],cwd=ROOT,capture_output=True,text=True,check=True)
    verify=json.loads(verification.stdout)
    delivery,delta,audit,replay=map(read,(DELIVERY,DELTA,AUDIT,REPLAY))
    archive_raw=ARCHIVE.read_bytes()
    assert verify["status"]=="PASS" and verify["checks"]==verify["passed"]==966
    assert sha(archive_raw)==ARCHIVE_SHA==delivery["archive"]["sha256"]
    assert delivery["scopeIds"]==[ID] and delivery["blockerIds"]==[BLOCKER]
    assert delivery["acceptedIds"]==delivery["appliedIds"]==delivery["applicationAuthorizedIds"]==[]
    assert audit["status"]==replay["status"]=="PASS"
    assert replay["passedChecks"]==966 and replay["scenarioCount"]==audit["scenarioCount"]==18
    assert replay["transitionCount"]==audit["transitionCount"]==65
    assert replay["fullyReversedScenarioCount"]==audit["fullInverseTraversals"]==18
    assert delta["testSpecification"]["testIds"]==[f"SH330-T{i:02d}" for i in range(1,7)]
    assert delta["provenance"]["conditionalFixturesAreGameplay"] is False
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==26
        rows={x["path"]:x for x in delivery["memberBindings"]}
        assert set(rows)==set(z.namelist())
        for name,row in rows.items():
            b=z.read(name)
            assert len(b)==row["bytes"] and sha(b)==row["sha256"] and crc(b)==row["crc32"]

    git_catalog=git_blob(CATALOG,head)
    git_catalog_binding={"path":CATALOG.relative_to(ROOT).as_posix(),"bytes":len(git_catalog),"sha256":sha(git_catalog),"crc32":crc(git_catalog)}
    work_catalog_binding=bind(CATALOG,catalog_raw)
    prior_catalog=delta["currentAuthorityBindingsBeforeCorrection"]["catalog"]
    assert prior_catalog["sha256"]==q0["currentCatalogBinding"]["sha256"]==p0["catalogBinding"]["sha256"]==work_catalog_binding["sha256"]
    assert len(git_catalog)==4945319 and sha(git_catalog)=="f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8" and crc(git_catalog)=="75a4fd7c"
    assert catalog_raw.replace(bytes([13,10]),bytes([10]))==git_catalog
    stamp=now()
    archref,delref,deltaref,auditref,replayref=map(bind,(ARCHIVE,DELIVERY,DELTA,AUDIT,REPLAY))
    q0ref,h0ref,p0ref=map(bind,(Q0,H0,P0)); idx0ref=bind(INDEX,index_raw)
    commitref={"branch":branch,"commit":head,"url":f"https://github.com/BordelonDevOps/DecenniumDescent/commit/{head}"}
    reconciliation={
      "id":"SH202-B01-CATALOG-BINDING-RECONCILIATION-351","recordedAtUtc":stamp,
      "status":"PASS_GIT_BLOB_AND_CRLF_WORKING_COPY_RECONCILED",
      "scope":"Serialization metadata only; no rules, native catalog records, or accepted Closure350 archive members changed.",
      "sourceCommit":commitref,"catalogPath":CATALOG.relative_to(ROOT).as_posix(),
      "committedGitBlobBinding":git_catalog_binding,"workingCopyBinding":work_catalog_binding,
      "closure350DeltaPriorBinding":prior_catalog,
      "verification":{"workingCopyNewlines":"CRLF","gitBlobNewlines":"LF",
        "normalizingWorkingCopyCRLFToLFMatchesGitBlob":True,"semanticJsonEquality":json.loads(git_catalog.decode("utf-8-sig"))==catalog0,
        "classification":"Line-ending serialization discrepancy only; no rules change."},
      "acceptedArchivePreservedByteExact":archref,
      "queueAndPendingAuditBindingRule":"Use the committed Git blob binding for currentCatalogBinding/catalogBinding and record the CRLF working-copy binding separately."
    }
    write(RECON,reconciliation); reconref=bind(RECON)
    decision={
      "id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-DIRECTOR-DECISION","recordedAtUtc":stamp,
      "status":"SEALED_ACCEPT_SUMMON_ELEMENTAL_AVATAR_SH202_B01_CLOSURE350","decision":"EXACT_ACCEPT",
      "identity":ID,"acceptedIds":[ID],"appliedIds":[],"heldIds":[],"closedBlockerIds":[BLOCKER],
      "closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],"openResidualIds":[],
      "accepted":True,"appliedAtDecision":False,"applicationAuthorized":True,"applicationAuthorizedIds":[ID],
      "source":{"service":"ChatGPT","conversationTitle":"Review Time Stop Witness Evidence","url":URL},
      "sourceCommit":commitref,
      "directorTranscriptExcerpt":(
        "SEALED ACCEPT — Summon Elemental Avatar / SH202-B01 only, bound to commit "+head+
        " and the supplied Closure350 archive hash. acceptedIds=[summon-elemental-avatar], appliedIds=[], heldIds=[], "+
        "closedBlockerIds=[SH202-B01], closedResidualIds=[SH348-R1,SH348-R2,SH348-R3], openResidualIds=[], "+
        "applicationAuthorized=true, applicationAuthorizedIds=[summon-elemental-avatar]. Archive hash, all 26 member bindings "+
        "and eight mirrored Git blobs match. Independent replay confirms 65 transitions, 113 forward/113 inverse operations, "+
        "all 18 reversals, and 966/966 PASS. No scoped witness gap remains. Apply this identity's authored-review acceptance only, "+
        "preserving historical evidence, SH202-H01–H12, both SH330 qualifications, and the synthetic-recipient limitation. "+
        "Native catalog/source status and runtime/downstream gates remain unchanged. No other identity is accepted or authorized."
      ),
      "closureArchive":archref,"deliveryManifest":delref,"conditionalTransitionDelta":deltaref,
      "independentReview":auditref,"replayVerification":replayref,"verifier":bind(VERIFIER),
      "catalogBindingReconciliation":reconref,"authorityAtDecision":BEFORE,"authorityAfterApplicationExpected":AFTER,
      "retainedQualificationIds":HOLDS,
      "syntheticRecipientLimitation":"All recipients are synthetic conditional test fixtures; no gameplay occurrence or authenticated campaign recipient is claimed.",
      "queueFindings":{"pendingIdListMatchesExactly":True,"priorityOrderIsSubset":True,"prioritySubsetOmittedPendingIds":OMITTED,
        "staleTimelessFormInHandoffHolds":True,"staleCurrentStepFieldsNamedTimelessForm":True,"catalogSerializationReconciliation":reconref},
      "nextPriority":{"identity":NEXT_ID,"blocker":NEXT_BLOCKER,"witnesses":[
        {"id":"SH332-W01","requiredEvidence":"Authorized complete profile for one existing named CR15+ eligible being. For Lumen: Thread Lance/Bind reach and range, Thread Shatter area, body fit, and applicable Seal/arena/phase constraints."},
        {"id":"SH332-W02","requiredEvidence":"Authority-tagged present or expressly authorized state: location, availability/reservation, affirmative consent, current HP/conditions/uses/recharge, equipment/custody, Seal state, and disclosure permissions."},
        {"id":"SH332-W03","requiredEvidence":"Compatible temporary departure, arrival, original 60-second expiry, and ordinary/blocked-return settlement, including cargo, suppression, and death."}],
        "packetStatus":"No newer Herald closure packet was found; unchanged Return332 is not a new submission."},
      "nativeCatalogChanged":False,"sourceStatusChanged":False,"runtimeSelectionEnabled":False,
      "gatesStillClosed":["runtime","implementation","human-play","balance","cosmology","domain-closure","completion","release"]
    }
    write(DEC,decision); decref=bind(DEC)
    acceptance={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-EXACT-AUTHORED-ACCEPTANCE","recordedAtUtc":stamp,
      "status":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_APPLICATION_AUTHORIZED","acceptedIds":[ID],"appliedIds":[],
      "heldIds":[],"closedBlockerIds":[BLOCKER],"closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],
      "applicationAuthorizedIds":[ID],"directorDecision":decref,"closureArchive":archref,"deliveryManifest":delref,
      "independentReview":auditref,"authorityBeforeApplication":BEFORE,"authorityAfterApplicationExpected":AFTER,
      "retainedQualificationIds":HOLDS,"runtimeSelectionEnabled":False,"catalogChanged":False}
    write(ACC,acceptance); accref=bind(ACC)
    receipt={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-DIRECTOR-RETURN-RECEIPT","recordedAtUtc":stamp,
      "status":"SEALED_ACCEPT_SH202_B01_CLOSURE350_ONLY","acceptedIds":[ID],"appliedIds":[],"heldIds":[],
      "closedBlockerIds":[BLOCKER],"closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],
      "applicationAuthorizedIds":[ID],"directorDecision":decref,"acceptance":accref,"acceptedArchive":archref,
      "deliveryManifest":delref,"independentReview":auditref,"sourceResponseSummary":decision["directorTranscriptExcerpt"],
      "retainedQualificationIds":HOLDS,"applicationPerformedByDirector":False}
    write(RCPT,receipt); rcptref=bind(RCPT)

    PKG.mkdir(parents=True)
    qual=[
      "SH202-H01 through SH202-H12 remain retained unchanged.",
      "SH330-Q-EXTERNAL-INPUTS remains retained.","SH330-Q-TEST-PROVENANCE remains retained.",
      decision["syntheticRecipientLimitation"],
      "Native catalog card, class access, source status, and operational:null remain unchanged and blocked for runtime selection.",
      "No runtime, human playtest, implementation, balance, cosmology, domain-closure, completion, or release approval is claimed."
    ]
    procedure={
      "id":"SH202-B01-STATIC-AUTHORED-REVIEW-351","spellId":ID,
      "status":"director-accepted static authored-review procedure; authored index applied; native operation remains blocked",
      "accepted":True,"applied":True,"scope":"Summon Elemental Avatar / SH202-B01 only; SH348-R1/R2/R3 closed.",
      "directorDecisionId":decision["id"],"acceptedArchive":archref,"deliveryManifest":delref,
      "localProcedure":{"scope":"Static authored review only; not a runtime spell procedure.",
        "instructions":"Evaluate the preserved native card only through the six SH330 test groups and their bound conditional scenarios. Do not infer untested mechanics or runtime behavior.",
        "testIds":delta["testSpecification"]["testIds"],"scenarioCount":18,"transitionCount":65,
        "forwardOperations":113,"inverseOperations":113,"fullyReversedScenarioCount":18},
      "sourceCatalogWholeCardPointer":entry0["wholeCardPointer"],"nativeCardPreserved":card,
      "nativeCardStatus":card["status"],"nativeOperationalField":card["operational"],"nativeSourceStatusPreservedAsBlocked":True,
      "acceptedReviewEvidence":{"delta":deltaref,"independentAudit":auditref,"replayVerification":replayref,
        "testIds":delta["testSpecification"]["testIds"],"scenarioCount":18,"transitionCount":65,"fullyReversedScenarioCount":18},
      "retainedQualificationIds":HOLDS,"retainedQualifications":qual,"syntheticRecipientLimitation":decision["syntheticRecipientLimitation"],
      "closedBlockerIds":[BLOCKER],"runtimeSelectionEnabled":False,"runtimeExecuted":False,"implementationApproved":False,"releaseApproved":False
    }
    write(PKG/"PROCEDURE_RECORD.json",procedure)
    write(PKG/"SOURCE_CARD.json",{"id":ID,"pointer":entry0["wholeCardPointer"],"gitBlobBinding":git_catalog_binding,
      "card":card,"changed":False,"status":card["status"],"operational":None,"runtimeSelectionEnabled":False})
    coverage={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-CASE-COVERAGE-351","sourceArchive":archref,
      "delta":deltaref,"independentReview":auditref,"replayVerification":replayref,
      "testIds":delta["testSpecification"]["testIds"],"testCaseIds":[x["id"] for x in delta["cases"]],
      "scenarioCount":18,"transitionCount":65,"forwardOperations":113,"inverseOperations":113,
      "fullyReversedScenarioCount":18,"fixtureStatus":"TEST_ONLY_CONDITIONAL_INPUT","gameplayOccurrenceClaim":False,
      "runtimeOrCampaignEvidence":False,"retainedQualificationIds":HOLDS}
    write(PKG/"CASE_COVERAGE.json",coverage); covref=bind(PKG/"CASE_COVERAGE.json")
    evidence={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-EVIDENCE-BINDINGS-351","archive":archref,"delivery":delref,
      "delta":deltaref,"independentReview":auditref,"replayVerification":replayref,"verifier":bind(VERIFIER),
      "directorDecision":decref,"acceptance":accref,"directorReturnReceipt":rcptref,"caseCoverage":covref,
      "catalogBindingReconciliation":reconref,"nativeCatalogGitBlob":git_catalog_binding,
      "currentAuthorityBeforeApplication":{"index":idx0ref,"queue":q0ref,"handoff":h0ref,"pendingAudit":p0ref},
      "authorityBeforeApplication":BEFORE,"baseCommit":COMMIT,"retainedQualificationIds":HOLDS,
      "nativeCatalogChanged":False,"sourceStatusChanged":False,"runtimeSelectionEnabled":False}
    write(PKG/"EVIDENCE_BINDINGS.json",evidence); evref=bind(PKG/"EVIDENCE_BINDINGS.json")
    model={"schemaVersion":1,"moduleId":"rank9summonelementalavatar-reviewed-351",
      "status":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
      "scope":"Authored-review evidence envelope only; no operational card promotion.",
      "acceptedIds":[ID],"excludedPendingIds":sorted(live0-{ID}),"sharedRequirements":{"runtimeSelectionEnabled":False},
      "spells":[{"id":ID,"name":card["name"],"position":int(entry0["wholeCardPointer"].rsplit("/",1)[1]),
        "procedure":{"id":procedure["id"],"spellId":ID,"status":procedure["status"],"accepted":True,"applied":True,
          "procedureContent":json.dumps(procedure["localProcedure"],ensure_ascii=False,sort_keys=True),
          "procedureRecordFile":"PROCEDURE_RECORD.json","sourceCardFile":"SOURCE_CARD.json",
          "caseCoverageFile":"CASE_COVERAGE.json","evidenceBindingsFile":"EVIDENCE_BINDINGS.json",
          "directorDecisionId":decision["id"],"retainedQualificationIds":HOLDS,"closedBlockerIds":[BLOCKER],
          "runtimeSelectionEnabled":False},
        "directorProcedureRecord":procedure,"nativeCardUnchanged":True,"retainedQualificationIds":HOLDS,
        "runtimeSelectionEnabled":False}],
      "sourceCatalogGitBlob":git_catalog_binding,"sourceArchive":archref,"directorDecision":decref,
      "acceptanceReceipt":accref,"directorReturnReceipt":rcptref,"caseCoverage":covref,"evidenceBindings":evref,
      "runtimeSelectionEnabled":False,"runtimeExecuted":False,"implementationApproved":False,
      "humanPlaytested":False,"balanceApproved":False,"cosmologyModified":False,"domainClosure":False,
      "completionApproved":False,"releaseApproved":False}
    write(PKG/"MODEL.json",model); modelref=bind(PKG/"MODEL.json")
    MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True)
    MANUSCRIPT.write_text(
      "# Summon Elemental Avatar — accepted static authored review 351\n\n"
      "GPT accepted Summon Elemental Avatar / SH202-B01 after Closure350 closed SH348-R1/R2/R3. The packet covers 18 conditional scenarios and 65 transitions; independent replay passed 966/966 checks and reversed all 18 scenarios.\n\n"
      "This application preserves the native card, class access, source status, and operational:null. Recipients remain synthetic conditional fixtures. Runtime selection and downstream gates remain closed.\n\n"
      "Retained qualification IDs: "+", ".join(HOLDS)+".\n\n"
      "Next: Summon Herald of the Planes / SH202-B02; bind SH332-W01/W02/W03 before preparing a new witness packet.\n",
      encoding="utf-8",newline="\n")
    manpath=PKG/"CANDIDATE_PACKAGE_MANIFEST.json"
    files=[]
    for p in sorted(x for x in PKG.rglob("*") if x.is_file() and x!=manpath):
        b=p.read_bytes(); files.append({"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
    write(manpath,{"id":"SUMMON-ELEMENTAL-AVATAR-PACKAGE-MANIFEST-351","recordedAtUtc":stamp,
      "directorDecision":decref,"acceptedArchive":archref,"files":files})
    manref=bind(manpath); manusref=bind(MANUSCRIPT)

    index1=copy.deepcopy(index0); ti=next(i for i,x in enumerate(index1["entries"]) if x["id"]==ID)
    entry1=copy.deepcopy(entry0); entry1.update({
      "authoredStatus":"reviewed-authored-operational-playtest",
      "procedureFile":"../spell_candidates/rank9summonelementalavatar_reviewed_351/MODEL.json",
      "procedurePointer":"/spells/0/procedure","wholeCardPointer":"/spells/0","sourceStatus":entry0["sourceStatus"],
      "wholeCardIdField":"id","sourceCatalogWholeCardPointer":entry0["wholeCardPointer"],
      "procedureTextPointer":"/spells/0/procedure/procedureContent","directorProcedureRecordPointer":"/spells/0/directorProcedureRecord",
      "sharedRulesPointer":"/sharedRequirements","spellLocalRequirementsPointer":"/spells/0/procedure",
      "manuscript":"../../../docs/spells/candidates/SUMMON_ELEMENTAL_AVATAR_REVIEWED_351.md",
      "reviewId":APP.name,"runtimeSelectionEnabled":False,"historicalCandidateLabelsPreserved":True,
      "completeEvidenceRoot":PKG_REL.as_posix(),"completeEnvelopeBinding":modelref,"caseEvidenceBindings":covref,
      "sourceArchiveBinding":archref,"deliveryManifestBinding":delref,"independentReviewBinding":auditref,
      "candidatePackageManifestBinding":manref,"procedureSourceBinding":decref,"authoredAcceptanceReceipt":accref,
      "authoredApplicationReceipt":APP.relative_to(ROOT).as_posix(),"directorReturnReceipt":rcptref,
      "accepted":True,"applied":True,"closedBlockerIds":[BLOCKER],
      "closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],"retainedQualificationIds":HOLDS,
      "retainedQualifications":qual,"syntheticRecipientLimitation":decision["syntheticRecipientLimitation"],
      "catalogBindingReconciliation":reconref})
    index1["entries"][ti]=entry1
    excluded=sorted(live0-{ID})
    envelope={"file":"../spell_candidates/rank9summonelementalavatar_reviewed_351/MODEL.json","binding":modelref,
      "reviewId":APP.name,"acceptedIds":[ID],"unacceptedIds":[],"excludedPendingIds":excluded,"authority":accref,
      "applicationReceipt":APP.relative_to(ROOT).as_posix(),"directorDecision":decref,"sourceArchive":archref,
      "deliveryManifest":delref,"caseCoverageBinding":covref,"candidatePackageManifestBinding":manref,
      "catalogBindingReconciliation":reconref,"scope":"ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED"}
    assert not any(ID in x.get("acceptedIds",[]) for x in index1["additionalStandaloneEnvelopes"])
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"]={"reviewed":826,"pending":22}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"]=550
    live1={x["id"] for x in index1["entries"] if x.get("authoredStatus")=="pending-authored-procedure"}
    assert live1==live0-{ID} and len(live1)==22
    BACKUP.write_bytes(index_raw); write(INDEX,index1); core_ref=bind(INDEX)
    application={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-AUTHORED-APPLICATION","recordedAtUtc":stamp,
      "status":"APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE","acceptedIds":[ID],"appliedIds":[ID],
      "closedBlockerIds":[BLOCKER],"closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],
      "directorAcceptance":accref,"directorDecision":decref,"directorReturnReceipt":rcptref,
      "acceptedArchive":archref,"deliveryManifest":delref,"independentReview":auditref,"replayVerification":replayref,
      "candidateEnvelope":modelref,"candidatePackageManifest":manref,"caseCoverage":covref,"evidenceBindings":evref,
      "catalogBindingReconciliation":reconref,"manuscript":manusref,"indexBefore":bind(BACKUP,index_raw),
      "indexAfterCoreUpdate":core_ref,"countsBefore":BEFORE,"countsAfter":AFTER,
      "completeReviewedStandaloneProcedures":{"before":549,"after":550},"scopedInterfaces":173,
      "catalogChanged":False,"sourceStatusPreservedAsBlocked":True,"runtimeSelectionEnabled":False,
      "runtimeExecuted":False,"implementationApproved":False,"humanPlaytested":False,"balanceApproved":False,
      "cosmologyModified":False,"domainClosure":False,"completionApproved":False,"releaseApproved":False,
      "retainedQualificationIds":HOLDS,"prioritySubsetOmittedPendingIds":OMITTED}
    write(APP,application); appref=bind(APP)
    entry1["authoredApplicationReceipt"]=appref; index1["entries"][ti]=entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"]=appref
    write(INDEX,index1); idxref=bind(INDEX)
    order=[NEXT_ID]+[x for x in q0["continuingPriorityOrder"] if x not in {ID,NEXT_ID} and x in live1]
    omitted=sorted(live1-set(order)); assert set(omitted)==set(OMITTED) and len(order)==18
    status="CLOSURE350_SEALED_ACCEPT_SUMMON_ELEMENTAL_AVATAR_SH202_B01_APPLIED; 22_CLOSURE_TASKS_REMAIN"
    last={"identity":ID,"blockerId":BLOCKER,"group":"summon-elemental-avatar-closure350"}
    q=copy.deepcopy(q0); q.update({
      "id":"SPELL-REVIEW-QUEUE-351","recordedAtUtc":stamp,"supersedesQueue":bind(Q0),"currentAuthority":AFTER,
      "currentIndexBinding":idxref,"currentCatalogBinding":git_catalog_binding,"currentCatalogWorkingCopyBinding":work_catalog_binding,
      "catalogBindingReconciliation":reconref,"pendingCount":22,"acceptedUnapplied":0,"activeReview":None,
      "nextGroup":None,"nextPendingIds":[],"nextPendingCount":0,"next":f"{NEXT_ID} / {NEXT_BLOCKER}",
      "nextIdentity":NEXT_ID,"nextBlockerIds":[NEXT_BLOCKER],"continuingPriorityOrder":order,
      "continuingPriorityOrderIsPrioritySubset":True,"prioritySubsetOmittedPendingIds":omitted,
      "remainingPendingIds":sorted(live1),"separatelyRetainedHolds":[x for x in q0.get("separatelyRetainedHolds",[]) if x not in {ID,"timeless-form"}],
      "closureTasksRemaining":22,"firstReviewTasksRemaining":0,"allPendingGroupsReviewed":True,"unreviewedPendingIds":[],
      "lastDirectorReturn":decision["id"],"currentReturnAcceptedIds":[ID],"currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],
      "currentReturnBlockers":{k:v for k,v in q0.get("currentReturnBlockers",{}).items() if k!=ID},
      "currentReturnDecision":decref,"currentReturn":decref,"currentReturnArchive":archref,"currentReturnDelivery":delref,
      "currentReturnAudit":auditref,"currentReturnReplay":replayref,"currentReturnReceipt":rcptref,
      "currentSourcePacket":archref,"currentPacket":archref["path"],"currentPacketSubmission":archref,"currentSubmission":archref,
      "currentPacketStatus":status,"currentPacketReadbackAudit":auditref,"currentPreparation":None,"submissionReceipt":None,
      "pendingIdentityAudit":P1.relative_to(ROOT).as_posix(),"currentPendingIdentityAudit":P1.relative_to(ROOT).as_posix(),
      "currentHandoff":H1.relative_to(ROOT).as_posix(),"currentReview":None,"currentBlocker":None,
      "directorConnectionStatus":"GPT sealed-accepted and explicitly authorized Summon Elemental Avatar / SH202-B01 application only.",
      "githubChanges":True,"canonicalFilesChanged":True,"applicationPerformed":True,
      "acceptedThisStep":[ID],"appliedThisStep":[ID],"heldThisStep":[],"lastReviewedBlocker":last,
      "closedBlockerIdsThisStep":[BLOCKER],"currentCorrectionIds":["SH348-R1","SH348-R2","SH348-R3"],
      "currentDirectorInstruction":decref,"nextPriorityRequirements":decision["nextPriority"]})
    write(Q1,q); qref=bind(Q1)
    p=copy.deepcopy(p0); p.update({
      "id":"SPELL-REVIEW-CURRENT22-PENDING-IDENTITY-AUDIT-351","recordedAtUtc":stamp,
      "status":"PASS_CURRENT_826_22_SUMMON_ELEMENTAL_AVATAR_SH202_B01_ACCEPTED_AND_APPLIED",
      "supersedes":bind(P0),"authority":AFTER,"indexBinding":idxref,"catalogBinding":git_catalog_binding,
      "catalogWorkingCopyBinding":work_catalog_binding,"catalogBindingReconciliation":reconref,
      "pendingCount":22,"pendingIds":sorted(live1),"acceptedIds":[ID],"appliedIds":[ID],
      "separatelyHeldIds":[x for x in p0.get("separatelyHeldIds",[]) if x!=ID],
      "allPendingIdsExistInNativeCatalog":True,"noPendingTargetSilentlyAccepted":True,"allCurrentPendingIdentitiesReviewed":True,
      "unreviewedPendingIds":[],"firstReviewTasksRemaining":0,"closureTasksRemaining":22,"nextGroup":None,
      "nextPendingIds":[],"nextPendingCount":0,
      "nextStep":"Next directed closure: Summon Herald of the Planes / SH202-B02. Bind SH332-W01/W02/W03 evidence before preparing a new packet.",
      "sourceQueue":Q1.relative_to(ROOT).as_posix(),"canonicalFilesChanged":True,"heldThisStep":[],
      "currentQueueBinding":qref,"currentPacketStatus":status,"currentPacketSubmission":archref,"currentSubmission":archref,
      "currentPacketReadbackAudit":auditref,"currentReturnDecision":decref,"currentReturnArchive":archref,
      "currentReturnDelivery":delref,"currentReturnAudit":auditref,"currentReturnReplay":replayref,
      "currentReturnAcceptedIds":[ID],"currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],"currentReturnBlockers":{},
      "lastReviewedBlocker":last,"applicationPerformed":True,"currentReturn":decref,"currentReturnReceipt":rcptref,
      "currentHandoff":H1.relative_to(ROOT).as_posix(),"closedBlockerIdsThisStep":[BLOCKER],
      "lastDirectorReturn":{"decisionId":decision["id"],"acceptedIds":[ID],"appliedIds":[ID],"heldIds":[],
        "closedBlockerIds":[BLOCKER],"closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],"archive":archref,"independentReview":auditref},
      "continuingPriorityOrder":order,"continuingPriorityOrderIsPrioritySubset":True,
      "prioritySubsetOmittedPendingIds":omitted,"remainingPendingIds":sorted(live1),
      "nextIdentity":NEXT_ID,"nextBlockerIds":[NEXT_BLOCKER],"nextPriorityRequirements":decision["nextPriority"]})
    write(P1,p); pref=bind(P1)
    h=copy.deepcopy(h0); h.update({
      "id":"CURRENT-HANDOFF-351","recordedAtUtc":stamp,"supersedes":h0["id"],
      "status":"SUMMON_ELEMENTAL_AVATAR_SH202_B01_ACCEPTED_AND_APPLIED_826_22_0","authority":AFTER,"currentAuthority":AFTER,
      "indexBinding":idxref,"currentCatalogBinding":git_catalog_binding,"catalogWorkingCopyBinding":work_catalog_binding,
      "catalogBindingReconciliation":reconref,"queue":Q1.relative_to(ROOT).as_posix(),"queueBinding":qref,
      "pendingIdentityAudit":P1.relative_to(ROOT).as_posix(),"pendingIdentityAuditBinding":pref,
      "continuingPriorityOrder":order,"continuingPriorityOrderIsPrioritySubset":True,
      "prioritySubsetOmittedPendingIds":omitted,"remainingPendingIds":sorted(live1),
      "separatelyRetainedHolds":[x for x in h0.get("separatelyRetainedHolds",[]) if x not in {ID,"timeless-form"}],
      "scopeIds":[ID],"blockerIds":[],"currentBlocker":None,"nextIdentity":NEXT_ID,"nextBlockerIds":[NEXT_BLOCKER],
      "nextPendingGroup":None,"nextStep":"Summon Herald of the Planes / SH202-B02 is next. Return332 requires SH332-W01 authorized named-being profile, SH332-W02 authority-tagged call state, and SH332-W03 compatible departure/arrival/expiry/return settlement. No newer Herald closure packet was found.",
      "nextPriorityRequirements":decision["nextPriority"],"acceptedThisStep":[ID],"appliedThisStep":True,"heldThisStep":[],
      "closedBlockerIds":list(dict.fromkeys(h0.get("closedBlockerIds",[])+[BLOCKER])),
      "closedResidualIdsThisStep":["SH348-R1","SH348-R2","SH348-R3"],"firstReviewTasksRemaining":0,"closureTasksRemaining":22,
      "directorConnectionStatus":"GPT sealed-accepted and explicitly authorized application of Summon Elemental Avatar / SH202-B01 only.",
      "directorReturnDecision":decref,"directorReturnArchive":archref,"directorReturnDelivery":delref,"directorReturnAudit":auditref,
      "directorReturnReplay":replayref,"currentPacketStatus":status,"currentPacketSubmission":archref,"currentSubmission":archref,
      "currentPacketReadbackAudit":auditref,"lastReviewedBlocker":last,"acceptedIds":[ID],"appliedIds":[ID],
      "currentDirectorInstruction":decref,"currentReturnReceipt":rcptref,"currentReturnAcceptedIds":[ID],
      "currentReturnAppliedIds":[ID],"currentReturnHeldIds":[],"currentDirectorReturn":decref,"currentDirectorDelivery":delref,
      "currentReturnAudit":auditref,"currentReadbackAudit":auditref,"currentReturn":decref,"currentReturnArchive":archref,
      "currentReturnDelivery":delref,"currentReturnAuditBinding":auditref,"currentPreparation":None,"currentReview":None,
      "currentReturnBlockers":{},"canonicalFilesChanged":True,"applicationPerformed":True})
    write(H1,h); href=bind(H1)
    operations={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-INDEX-OPERATIONS","recordedAtUtc":stamp,
      "before":bind(BACKUP,index_raw),"after":idxref,
      "operations":[{"op":"update-entry","id":ID,"before":entry0,"after":entry1},
        {"op":"append-standalone-authored-review-envelope","acceptedIds":[ID]},
        {"op":"update-authored-counts","before":{"reviewed":825,"pending":23},"after":{"reviewed":826,"pending":22}},
        {"op":"increment-complete-standalone-procedure-count","before":549,"after":550}],
      "inverse":[{"op":"restore-entry","id":ID,"value":entry0},{"op":"remove-appended-envelope","acceptedIds":[ID]},
        {"op":"restore-authored-counts","value":{"reviewed":825,"pending":23}},
        {"op":"restore-procedure-count","value":549},{"op":"restore-byte-exact-index-from-backup","backup":bind(BACKUP,index_raw)}],
      "catalogByteExact":CATALOG.read_bytes()==catalog_raw,"nativeCardUnchanged":True,
      "historicalClosure350ArchiveRewritten":False,"inverseRestoresExactIndex":BACKUP.read_bytes()==index_raw}
    write(OPS,operations); opsref=bind(OPS)
    checks=[
      ("Closure350 verifier 966/966 PASS",verify["status"]=="PASS" and verify["checks"]==966 and verify["passed"]==966),
      ("Director accepts and authorizes only this identity",decision["acceptedIds"]==[ID] and decision["applicationAuthorizedIds"]==[ID]),
      ("Archive and all 26 member bindings pass",sha(ARCHIVE.read_bytes())==ARCHIVE_SHA and delivery["memberCount"]==26),
      ("Exact identity removed; 22 remain",live1==live0-{ID} and len(live1)==22),
      ("Authority advances to 826/22/0 and 550/173",index1["authoredCounts"]=={"reviewed":826,"pending":22} and index1["representationCounts"]["completeReviewedStandaloneProcedures"]==550),
      ("Native card remains blocked and operational-null",card["status"]=="blocked-pending-operational-review" and card["operational"] is None and CATALOG.read_bytes()==catalog_raw),
      ("22 pending split into 18 priority IDs and four explicit omissions",len(order)==18 and set(order)|set(omitted)==live1 and set(omitted)==set(OMITTED)),
      ("Summon Herald is next with SH202-B02",q["nextIdentity"]==h["nextIdentity"]==NEXT_ID and q["nextBlockerIds"]==h["nextBlockerIds"]==[NEXT_BLOCKER]),
      ("Timeless Form stale handoff hold removed", "timeless-form" not in h["separatelyRetainedHolds"]),
      ("Catalog LF Git blob and CRLF working copy reconcile",catalog_raw.replace(bytes([13,10]),bytes([10]))==git_catalog and q["currentCatalogBinding"]["sha256"]==git_catalog_binding["sha256"]),
      ("Queue, pending audit, and handoff share index and authority",q["currentIndexBinding"]["sha256"]==p["indexBinding"]["sha256"]==h["indexBinding"]["sha256"]==idxref["sha256"] and q["currentAuthority"]==p["authority"]==h["authority"]==AFTER),
      ("Queue, pending and handoff cross-bind current files",p["currentQueueBinding"]["sha256"]==qref["sha256"] and h["queueBinding"]["sha256"]==qref["sha256"] and h["pendingIdentityAuditBinding"]["sha256"]==pref["sha256"]),
      ("All SH202/SH330 qualifications retained",entry1["retainedQualificationIds"]==HOLDS and entry1["syntheticRecipientLimitation"]==decision["syntheticRecipientLimitation"]),
      ("Runtime and downstream gates remain disabled",model["runtimeSelectionEnabled"] is False and application["runtimeSelectionEnabled"] is False)]
    assert all(ok for _,ok in checks),[name for name,ok in checks if not ok]
    validation={"id":"SUMMON-ELEMENTAL-AVATAR-CLOSURE350-APPLICATION-VALIDATION","recordedAtUtc":stamp,
      "status":"PASS","checks":[{"check":n,"passed":bool(ok)} for n,ok in checks],
      "checkCount":len(checks),"failedChecks":0,"acceptedIds":[ID],"appliedIds":[ID],
      "closedBlockerIds":[BLOCKER],"closedResidualIds":["SH348-R1","SH348-R2","SH348-R3"],
      "authority":AFTER,"index":idxref,"application":appref,"acceptance":accref,"directorDecision":decref,
      "archive":archref,"catalogBindingReconciliation":reconref,"pendingIdentityAudit":pref,
      "queue":qref,"handoff":href,"indexOperations":opsref,"catalogChanged":False,
      "sourceStatusPreservedAsBlocked":True,"runtimeSelectionEnabled":False,
      "prioritySubsetOmittedPendingIds":omitted,"nextIdentity":NEXT_ID}
    write(VAL,validation); valref=bind(VAL)
    SNAPSHOT.write_text("# Spell review snapshot — Summon Elemental Avatar Closure350 application\n\n"
      "**826 applied / 22 pending / 0 accepted-unapplied; 550 complete standalone procedures / 173 scoped interfaces; 0 first reviews / 22 closure tasks.**\n\n"
      "GPT accepted and authorized Summon Elemental Avatar / SH202-B01 only. Closure350 closes SH348-R1/R2/R3; native catalog, source status, and runtime remain blocked.\n\n"
      "The continuing priority order is a subset; four other IDs remain pending: "+", ".join(omitted)+".\n\n"
      "Next directed closure: Summon Herald of the Planes / SH202-B02 under SH332-W01/W02/W03.\n\n"
      f"Validation: {valref['path']} (SHA-256 {valref['sha256']}).\n",encoding="utf-8",newline="\n")
    assert CATALOG.read_bytes()==catalog_raw and read(INDEX)["authoredCounts"]=={"reviewed":826,"pending":22}
    print(json.dumps({"status":"PASS","acceptedApplied":ID,"closedBlockerIds":[BLOCKER],
      "authority":AFTER,"index":bind(INDEX),"application":appref,"validation":valref,
      "queue":qref,"pendingAudit":pref,"handoff":href,"catalogGitBlob":git_catalog_binding,
      "next":NEXT_ID},indent=2))

if __name__=="__main__": main()
