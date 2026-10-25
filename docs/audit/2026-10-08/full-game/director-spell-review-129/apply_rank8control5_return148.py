from __future__ import annotations
import copy, gzip, hashlib, json, os, shutil, sys, zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(r"C:\Github\DecenniumDescent")
FULL=ROOT/"docs/audit/2026-10-08/full-game"
AUDIT=FULL/"director-spell-review-129"
ZIP=FULL/"DD_Rank8_Control5_Director_Return148_Reupload01.zip"
DELIVERY=FULL/"DD_Rank8_Control5_Director_Return148_Reupload01_DELIVERY.json"
SRC=ROOT/"DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_control_5_source_conference_02.json"
SRCZIP=FULL/"DD_Rank8_Control_5_Source_Conference_02.zip"
INDEX=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QB=AUDIT/"CURRENT_SPELL_QUEUE_147.json"
PB=AUDIT/"CURRENT153_PENDING_IDENTITY_AUDIT_147.json"
HB=AUDIT/"CURRENT_HANDOFF_147.json"
IDS=["frozen-time-prism","paralyzing-presence","power-word-stun","mental-collapse","reality-rewrite"]
RID="RANK8-CONTROL5-EXACT-AUTHORED-ACCEPTANCE-148"
CAND=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8control5_reviewed_148"
STAGE=CAND.with_name(CAND.name+".staging")
MANUSCRIPT=ROOT/"DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_CONTROL5_REVIEWED_148.md"
RECEIVED=AUDIT/"rank8control5_return148_received"
DECISION=AUDIT/"GPT_DIRECTOR_DECISION_RANK8_CONTROL5_148.json"
RECEIPT=AUDIT/"RANK8_CONTROL5_EXACT_ACCEPTANCE_148.json"
APP=AUDIT/"RANK8_CONTROL5_APPLICATION_148.json"
OPS=AUDIT/"RANK8_CONTROL5_INDEX_OPERATIONS_148.json"
VALIDATION=AUDIT/"RANK8_CONTROL5_APPLICATION_VALIDATION_148.json"
BACKUP=AUDIT/"authored_review_index.before_rank8control5_148.json"
QA=AUDIT/"CURRENT_SPELL_QUEUE_148.json"
PA=AUDIT/"CURRENT148_PENDING_IDENTITY_AUDIT_148.json"
HA=AUDIT/"CURRENT_HANDOFF_148.json"
START=ROOT/"START_HERE.md"

def sha(b): return hashlib.sha256(b).hexdigest()
def rj(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def jb(x): return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode()
def wj(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(jb(x))
def bind(p,rel=None,data=None):
    b=p.read_bytes() if data is None else data
    return {"path":rel or p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":sha(b)}
def now(): return datetime.now(timezone.utc).isoformat()

def main(apply):
    zsha="524f62ae6e761fed5a47d1fdc7c19342f380d42652f2d6cc31c2a1818b38ee6b"
    csha="7726b6ffef52f4b3ca4dff2542b5eeddf166fbc583c176954815141313a75b9d"
    ssha="ffa8dc96550ef9b5b5eed7890aa3269feb9ea1c287c47426c7ea4c360ecc7cf3"
    isha="4b3d76f330dec707a6635f62e1b8f4ed549263a407f90203af3cd1be098ff419"
    catsha="f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8"
    rawzip=ZIP.read_bytes(); d=json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    assert len(rawzip)==39773931 and sha(rawzip)==zsha
    assert d["archive"]=={"file":ZIP.name,"bytes":len(rawzip),"sha256":zsha}
    assert d["accepted"] and not d["applied"] and d["acceptedIds"]==IDS
    assert d["authorityInput"]=={"applied":695,"pending":153,"acceptedUnapplied":0}
    assert (d["localPackageChecks"],d["packageFailures"],d["memberCount"])==(985,0,245)
    assert sha(SRC.read_bytes())==csha and sha(SRCZIP.read_bytes())==ssha
    assert d["savedArtifactVerification"]["downloadedSHA256"]==zsha
    assert d["savedArtifactVerification"]["checks"]==743 and d["savedArtifactVerification"]["failures"]==0

    before_bytes=INDEX.read_bytes(); cat_bytes=CATALOG.read_bytes()
    before=json.loads(before_bytes.decode("utf-8-sig")); catalog=json.loads(cat_bytes.decode("utf-8-sig"))
    qb,pb,hb=map(rj,[QB,PB,HB])
    assert sha(before_bytes)==isha and sha(cat_bytes)==catsha==before["sourceCatalogSha256"]
    assert before["authoredCounts"]=={"reviewed":695,"pending":153}
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"]==419
    assert qb["currentAuthority"]["reviewedApplied"]==695 and qb["currentAuthority"]["pending"]==153
    assert pb["pendingCount"]==153 and pb["indexBinding"]["sha256"]==isha
    assert hb["currentIndexBinding"]["sha256"]==isha and hb["currentAuthority"]["reviewedApplied"]==695

    md={}; casebook=None
    with ZipFile(ZIP) as z:
        assert z.testzip() is None
        names=z.namelist(); assert len(names)==245 and len(set(names))==245
        mm=json.loads(z.read("MEMBER_MANIFEST.json"))
        assert mm["archiveMemberCount"]==245 and mm["payloadMemberCount"]==244
        assert set(names)==set(mm["zipMemberAllowlist"])
        dm={x["path"]:x for x in d["members"]}; assert set(dm)==set(names)
        for name in names:
            raw=z.read(name); info=z.getinfo(name); row=dm[name]
            assert len(raw)==row["bytes"] and sha(raw)==row["sha256"] and info.CRC==int(row["crc32"],16)
            assert f"{info.CRC:08x}"==row["crc32"].lower() and info.file_size==row["bytes"]
            if name=="CASEBOOK.json": casebook=raw
            elif "/" not in name or name.startswith(("procedures/","evidence/source02/","history/","validation/")):
                md[name]=raw
        decision=json.loads(md["DIRECTOR_DECISION.json"])
        fail=json.loads(md["INDEPENDENT_FAILURE_CHECK.json"])
        procs=json.loads(md["PROCEDURES.json"])
        pop=json.loads(md["PROPOSAL_OPERATIONS.json"])
        counts=json.loads(md["COUNTS.json"])["counts"]
        holds=json.loads(md["HOLD_REGISTER.json"])
        model0=json.loads(md["MODEL.json"])
        assert z.read("evidence/source02/CANDIDATE.json")==SRC.read_bytes()
        assert z.read("history/DD_Rank8_Control_5_Source_Conference_02.zip")==SRCZIP.read_bytes()
    assert sha(casebook)== "fdb7cd0cfa2af9c69b3f7f57624706e03c6fc62ddb304757c93d1ca4e1dc32d7"
    assert decision["accepted"] and not decision["applied"] and decision["acceptedIds"]==IDS
    assert not decision["rejectedIds"] and not decision["remainingBlockingDefects"]
    assert decision["sourceAuthorityInput"]["applied"]==695 and decision["sourceAuthorityInput"]["pending"]==153
    assert fail["checkCount"]==36451 and fail["failureCount"]==0 and not fail["failures"]
    assert [p["id"] for p in procs]==IDS and all(p["accepted"] and not p["applied"] for p in procs)
    assert model0["accepted"] and not model0["applied"] and model0["acceptedIds"]==IDS
    assert not pop["applied"] and not pop["canonicalMutation"] and pop["operationCount"]==20
    assert counts["cases"]==132 and counts["events"]==774 and counts["holds"]==10
    assert counts["retainedResource6ComparisonHolds"]==13 and len(holds)==10

    rows={e["id"]:e for e in before["entries"]}
    assert len(rows)==len(before["entries"])==848
    pids=set(pb["pendingIds"])
    assert pids=={e["id"] for e in before["entries"] if e["authoredStatus"]=="pending-authored-procedure"}
    assert qb["currentPendingGroups"][0]["group"]=="rank8-control5" and qb["currentPendingGroups"][0]["pendingIds"]==IDS
    assert all(s in pids and rows[s]["authoredStatus"]=="pending-authored-procedure" for s in IDS)
    assert all(rows[s]["sourceStatus"]=="blocked-pending-operational-review" for s in IDS)

    excluded=sorted(pids-set(IDS)); ts=now()
    decision_record={"id":"GPT-DIRECTOR-DECISION-RANK8-CONTROL5-148","recordedAtUtc":ts,
        "source":{"product":"ChatGPT","project":"Dungeon Crawler","conversation":"Calibration review part 6","conversationId":"6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "decision":decision["decision"],"accepted":True,"appliedAtDecision":False,"acceptedIds":IDS,
        "rejectedIds":[],"remainingBlockingDefects":[],"verification":{"independentChecksPassed":36451,"independentCheckFailures":0,
        "packageChecksPassed":985,"packageFailures":0,"zipRoundTripChecksPassed":743,"zipRoundTripFailures":0,
        "archiveMembers":245,"cases":132,"events":774,"newHolds":10,"retainedComparisonHolds":13},
        "acceptedArchive":{"name":ZIP.name,"bytes":len(rawzip),"sha256":zsha},"scope":decision["acceptanceScope"],"directorMadeNoLocalChanges":True}
    receipt={"id":RID,"recordedAtUtc":now(),"status":"DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "decision":"ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY","directorDecision":decision_record,
        "directorReturn":{"path":f"docs/audit/2026-10-08/full-game/{ZIP.name}","bytes":len(rawzip),"sha256":zsha},
        "directorReturnDelivery":{"path":f"docs/audit/2026-10-08/full-game/{DELIVERY.name}","bytes":DELIVERY.stat().st_size,"sha256":sha(DELIVERY.read_bytes())},
        "acceptedIds":IDS,"countsBefore":{"reviewed":695,"pending":153,"acceptedUnapplied":0},
        "countsAfter":{"reviewed":700,"pending":148,"acceptedUnapplied":0},"newHolds":10,"retainedComparisonHolds":13,
        "sourceStatusPreserved":"blocked-pending-operational-review for all five identities; authored manuscript review only.",
        "runtimeSelectionEnabled":False,"runtimeTestsExecuted":False,"sourceProgramsExecuted":False,"humanPlaytested":False,
        "balanceApproved":False,"cosmologyModified":False,"releaseApproved":False,"canonicalApplicationPerformed":False}
    receipt_bytes=jb(receipt); decision_bytes=jb(decision_record)
    common=procs[0]["sharedRules"]; assert all(p["sharedRules"]==common for p in procs)
    spells=[]
    for i,p in enumerate(procs):
        row=rows[p["id"]]
        spells.append({"id":p["id"],"name":row["name"],"procedure":copy.deepcopy(p["procedure"]),
            "directorProcedureRecord":copy.deepcopy(p),"nativeCardAndAccessUnchanged":copy.deepcopy(p["completeNativeCardUnchanged"]),
            "sourceCatalogWholeCardPointer":row.get("sourceCatalogWholeCardPointer") or row["wholeCardPointer"],
            "sourceRecordPointer":p["sourceRecordPointer"],"runtimeSelectionEnabled":False})
    scope="Only the five director-accepted Control5 authored procedures and their bound static evidence are applied. All 10 new qualification/source holds and 13 inherited Resource6 comparison holds remain; conditional cases remain conditional. Native source cards, class access, source status, catalog and other identities are unchanged. Authored manuscript/static data review only; runtime selection remains disabled and no runtime, human-play, balance, cosmology, release or domain-closure approval is granted."
    model={"schemaVersion":3,"moduleId":"rank8control5-reviewed-148","status":"EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
        "scope":scope,"acceptedIds":IDS,"excludedPendingIds":excluded,"sharedRules":common,"spells":spells,
        "questionDispositions":json.loads(md["QUESTION_DISPOSITIONS.json"]),"futureObligationDispositions":json.loads(md["FUTURE_OBLIGATION_DISPOSITIONS.json"]),
        "originalQuestions":json.loads(md["ORIGINAL_QUESTIONS.json"]),"casebookFile":"CASEBOOK.json.gz",
        "casebookEncoding":"gzip; exact decompression reproduces the director return CASEBOOK.json member",
        "casebookSourceMemberBinding":{"path":"CASEBOOK.json","bytes":len(casebook),"sha256":sha(casebook)},
        "holdsFile":"HOLD_REGISTER.json","inheritedHoldsFile":"INHERITED_HOLDS.json","procedureSourceFile":"PROCEDURES.json",
        "proposalOperationsFile":"PROPOSAL_OPERATIONS.json","directorDecisionFile":"GPT_DIRECTOR_DECISION.json",
        "directorReturnArchive":"DIRECTOR_RETURN_ARCHIVE.zip","directorReturnDelivery":"DIRECTOR_RETURN_DELIVERY.json",
        "sourceConferenceArchive":"SOURCE_CONFERENCE_ARCHIVE.zip","sourceConferenceCandidate":"SOURCE_CONFERENCE_CANDIDATE.json",
        "independentFailureCheckFile":"INDEPENDENT_FAILURE_CHECK.json","directorReturnBinding":{"path":f"docs/audit/2026-10-08/full-game/{ZIP.name}","bytes":len(rawzip),"sha256":zsha},
        "sourceArchiveMemberCount":245,"independentAcceptanceGranted":True,"canonicalApplicationPerformed":False,
        "runtimeTestsExecuted":False,"sourceProgramsExecuted":False,"humanPlaytested":False,"balanceApproved":False,"cosmologyModified":False,"releaseApproved":False}

    dest=[CAND,STAGE,RECEIVED,DECISION,RECEIPT,APP,OPS,VALIDATION,BACKUP,QA,PA,HA,MANUSCRIPT]
    assert not any(p.exists() for p in dest),"An application destination already exists; inspect it before retrying."
    assert sha(INDEX.read_bytes())==isha and sha(CATALOG.read_bytes())==catsha
    preview={}; after=copy.deepcopy(before)
    for i,old in enumerate(before["entries"]):
        if old["id"] not in IDS: continue
        sid=old["id"]; n=IDS.index(sid); new=copy.deepcopy(old)
        new.update({"authoredStatus":"reviewed-authored-operational-playtest",
            "procedureFile":"../spell_candidates/rank8control5_reviewed_148/MODEL.json",
            "procedurePointer":f"/spells/{n}/procedure","wholeCardPointer":f"/spells/{n}",
            "sourceCatalogWholeCardPointer":old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField":"id","procedureTextPointer":f"/spells/{n}/procedure",
            "directorProcedureRecordPointer":f"/spells/{n}/directorProcedureRecord","sharedRulesPointer":"/sharedRules",
            "manuscript":"../../../docs/spells/candidates/RANK8_CONTROL5_REVIEWED_148.md","reviewId":"RANK8-CONTROL5-APPLICATION-148",
            "runtimeSelectionEnabled":False,"historicalCandidateLabelsPreserved":True,"completeEvidenceRoot":CAND.relative_to(ROOT).as_posix()})
        after["entries"][i]=new
    after["authoredCounts"]={"reviewed":700,"pending":148}
    after["representationCounts"]["completeReviewedStandaloneProcedures"]=424
    pending={e["id"] for e in after["entries"] if e["authoredStatus"]=="pending-authored-procedure"}
    assert len(pending)==148 and not (pending&set(IDS))
    groups=[]
    for g in qb["currentPendingGroups"]:
        keep=[s for s in g["pendingIds"] if s in pending]
        if keep:
            x=copy.deepcopy(g); x["pendingIds"]=keep; x["pendingCount"]=len(keep); groups.append(x)
    assert groups and groups[0]["group"]=="rank8-ward5"
    inverse=copy.deepcopy(after)
    for i,e in enumerate(before["entries"]):
        if e["id"] in IDS: inverse["entries"][i]=copy.deepcopy(e)
    assert inverse["entries"]==before["entries"]

    checks={"directorAcceptedExactReturn148":True,"archiveDeliveryAnd245MemberHashesCrcsPass":True,
        "independentFailureCheck36541Passes":fail["checkCount"]==36451 and fail["failureCount"]==0,
        "package985AndZipRoundTrip743Pass":d["localPackageChecks"]==985 and d["savedArtifactVerification"]["checks"]==743,
        "sourcePacketAndArchiveMatchExactHashes":sha(SRC.read_bytes())==csha and sha(SRCZIP.read_bytes())==ssha,
        "fivePendingIdentitiesMatchAcceptedIds":all(s in pids for s in IDS),
        "allTenNewAndThirteenComparisonHoldsRetained":len(holds)==10 and counts["retainedResource6ComparisonHolds"]==13,
        "700Reviewed148PendingAnd424Standalone":after["authoredCounts"]=={"reviewed":700,"pending":148} and after["representationCounts"]["completeReviewedStandaloneProcedures"]==424,
        "onlyFiveIdentityRowsChanged":all(after["entries"][i]==before["entries"][i] for i in range(len(before["entries"])) if before["entries"][i]["id"] not in IDS),
        "allFiveSourceStatusesRemainBlocked":all(next(e for e in after["entries"] if e["id"]==s)["sourceStatus"]=="blocked-pending-operational-review" for s in IDS),
        "catalogAndPriorStandaloneEnvelopeHashUnchanged":CATALOG.read_bytes()==cat_bytes and after["standaloneEnvelopeSha256"]==before["standaloneEnvelopeSha256"],
        "all148PendingIdsExistInCatalog":all(any(x.get("id")==s for x in catalog["spells"]) for s in pending),
        "inverseRestoresPriorRows":inverse["entries"]==before["entries"],
        "runtimeSelectionDisabled":not any(next(e for e in after["entries"] if e["id"]==s).get("runtimeSelectionEnabled",False) for s in IDS),
        "nextGroupIsRank8Ward5":groups[0]["group"]=="rank8-ward5"}
    assert all(checks.values()),{k:v for k,v in checks.items() if not v}
    if not apply:
        print(json.dumps({"status":"PREFLIGHT_PASS","acceptedIds":IDS,"authorityAfter":{"reviewed":700,"pending":148,"acceptedUnapplied":0,"standalone":424},
            "nextGroup":groups[0]["group"],"nextIds":groups[0]["pendingIds"],"checks":len(checks),"archiveSha256":zsha},indent=2)); return

    RECEIVED.mkdir(parents=True); shutil.copyfile(ZIP,RECEIVED/ZIP.name); shutil.copyfile(DELIVERY,RECEIVED/"DIRECTOR_RETURN_DELIVERY.json")
    wj(DECISION,decision_record); wj(RECEIPT,receipt); STAGE.mkdir(parents=True)
    for name,b in md.items():
        if "/" not in name and name!="CASEBOOK.json": (STAGE/name).write_bytes(b)
        elif name.startswith("procedures/"):
            p=STAGE/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        elif name.startswith("evidence/source02/") and not name.startswith("evidence/source02/sources/"):
            p=STAGE/"SOURCE_EVIDENCE"/name.removeprefix("evidence/source02/"); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        elif name.startswith("history/"):
            p=STAGE/"SOURCE_EVIDENCE"/name.split("/",1)[1]; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        elif name.startswith("validation/"):
            p=STAGE/"DIRECTOR_VALIDATION"/name.split("/",1)[1]; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
    (STAGE/"DIRECTOR_RETURN_ARCHIVE.zip").write_bytes(rawzip)
    (STAGE/"DIRECTOR_RETURN_DELIVERY.json").write_bytes(DELIVERY.read_bytes())
    (STAGE/"GPT_DIRECTOR_DECISION.json").write_bytes(jb(decision_record))
    (STAGE/"EXACT_ACCEPTANCE.json").write_bytes(receipt_bytes)
    (STAGE/"SOURCE_CONFERENCE_ARCHIVE.zip").write_bytes(SRCZIP.read_bytes())
    (STAGE/"SOURCE_CONFERENCE_CANDIDATE.json").write_bytes(SRC.read_bytes())
    with (STAGE/"CASEBOOK.json.gz").open("wb") as out:
        with gzip.GzipFile(fileobj=out,mode="wb",mtime=0) as gz: gz.write(casebook)
    with gzip.open(STAGE/"CASEBOOK.json.gz","rb") as f: assert f.read()==casebook
    model["casebookSourceMemberBinding"]={"path":"CASEBOOK.json","bytes":len(casebook),"sha256":sha(casebook)}
    wj(STAGE/"MODEL.json",model)
    excl={"MODEL.json","CANDIDATE_PACKAGE_MANIFEST.json"}; files=[]
    for p in sorted(STAGE.rglob("*")):
        if p.is_file() and p.name not in excl:
            b=p.read_bytes(); files.append({"path":p.relative_to(STAGE).as_posix(),"bytes":len(b),"sha256":sha(b)})
    pm={"id":"RANK8-CONTROL5-CANDIDATE-PACKAGE-MANIFEST-148","sourceArchive":{"name":ZIP.name,"bytes":len(rawzip),"sha256":zsha},
        "files":files,"excludedFromBindings":sorted(excl),"selfExcluded":"CANDIDATE_PACKAGE_MANIFEST.json"}
    wj(STAGE/"CANDIDATE_PACKAGE_MANIFEST.json",pm)
    pmb=bind(STAGE/"CANDIDATE_PACKAGE_MANIFEST.json",CAND.relative_to(ROOT).as_posix()+"/CANDIDATE_PACKAGE_MANIFEST.json")
    model["candidatePackageManifestBinding"]=pmb; wj(STAGE/"MODEL.json",model)
    modelb=bind(STAGE/"MODEL.json",CAND.relative_to(ROOT).as_posix()+"/MODEL.json")
    shutil.move(str(STAGE),str(CAND)); MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True); MANUSCRIPT.write_bytes(md["STANDALONE_PROCEDURES.md"])

    app={"id":"RANK8-CONTROL5-APPLICATION-148","recordedAtUtc":now(),"status":"APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS",
        "reviewId":RID,"ownerInstruction":"Apply each exact accepted ordinary-spell scope and continue through the remaining pending ordinary spell identities.",
        "acceptedIds":IDS,"directorAcceptance":bind(RECEIPT),"directorDecision":bind(DECISION),
        "directorReturn":bind(RECEIVED/ZIP.name,f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/{ZIP.name}"),
        "directorReturnDelivery":bind(RECEIVED/"DIRECTOR_RETURN_DELIVERY.json",f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/DIRECTOR_RETURN_DELIVERY.json"),
        "candidateEnvelope":modelb,"candidatePackageManifest":pmb,"indexBefore":bind(INDEX,data=before_bytes),
        "counts":{"before":{"reviewed":695,"pending":153,"acceptedUnapplied":0},"after":{"reviewed":700,"pending":148,"acceptedUnapplied":0}},
        "acceptedCases":counts["cases"],"events":counts["events"],"newHolds":10,"retainedComparisonHolds":13,
        "sourceStatusPreservedAsBlocked":True,"catalogChanged":False,"runtimeSelectionEnabled":False,"closedCohortsReopened":False}
    wj(APP,app); appb=bind(APP)
    after=copy.deepcopy(before); operations=[]
    for i,old in enumerate(before["entries"]):
        sid=old["id"]
        if sid not in IDS: continue
        n=IDS.index(sid); new=copy.deepcopy(old); srcptr=old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"]
        new.update({"authoredStatus":"reviewed-authored-operational-playtest","procedureFile":"../spell_candidates/rank8control5_reviewed_148/MODEL.json",
            "procedurePointer":f"/spells/{n}/procedure","wholeCardPointer":f"/spells/{n}","sourceCatalogWholeCardPointer":srcptr,"wholeCardIdField":"id",
            "procedureTextPointer":f"/spells/{n}/procedure","directorProcedureRecordPointer":f"/spells/{n}/directorProcedureRecord","sharedRulesPointer":"/sharedRules",
            "manuscript":"../../../docs/spells/candidates/RANK8_CONTROL5_REVIEWED_148.md","reviewId":"RANK8-CONTROL5-APPLICATION-148",
            "runtimeSelectionEnabled":False,"completeEnvelopeBinding":modelb,"historicalCandidateLabelsPreserved":True,
            "casebookBinding":bind(CAND/"CASEBOOK.json.gz",CAND.relative_to(ROOT).as_posix()+"/CASEBOOK.json.gz"),
            "casebookEncoding":"gzip; exact decompression reproduces the director return CASEBOOK.json member",
            "casebookSourceArchiveMemberBinding":model["casebookSourceMemberBinding"],
            "sourceArchiveBinding":bind(RECEIVED/ZIP.name,f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/{ZIP.name}"),
            "sourceConferenceArchiveBinding":bind(CAND/"SOURCE_CONFERENCE_ARCHIVE.zip",CAND.relative_to(ROOT).as_posix()+"/SOURCE_CONFERENCE_ARCHIVE.zip"),
            "sourceCandidateBinding":bind(CAND/"SOURCE_CONFERENCE_CANDIDATE.json",CAND.relative_to(ROOT).as_posix()+"/SOURCE_CONFERENCE_CANDIDATE.json"),
            "candidatePackageManifestBinding":pmb,"retainedHoldsBinding":bind(CAND/"HOLD_REGISTER.json",CAND.relative_to(ROOT).as_posix()+"/HOLD_REGISTER.json"),
            "procedureSourceBinding":bind(CAND/"PROCEDURES.json",CAND.relative_to(ROOT).as_posix()+"/PROCEDURES.json"),
            "proposalOperationsBinding":bind(CAND/"PROPOSAL_OPERATIONS.json",CAND.relative_to(ROOT).as_posix()+"/PROPOSAL_OPERATIONS.json"),
            "completeEvidenceRoot":CAND.relative_to(ROOT).as_posix(),"acceptedSharedRuleScope":scope,
            "authoredAcceptanceReceipt":bind(RECEIPT),"authoredApplicationReceipt":appb})
        operations.append({"op":"replace-entry","identity":sid,"index":i,"before":copy.deepcopy(old),"after":copy.deepcopy(new)})
        after["entries"][i]=new
    after["additionalStandaloneEnvelopes"].append({"file":"../spell_candidates/rank8control5_reviewed_148/MODEL.json","binding":modelb,
        "reviewId":RID,"acceptedIds":IDS,"excludedPendingIds":excluded,"authority":bind(RECEIPT),
        "applicationReceipt":f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APP.name}",
        "sourceArchive":bind(RECEIVED/ZIP.name,f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIVED.name}/{ZIP.name}"),
        "casebookBinding":bind(CAND/"CASEBOOK.json.gz",CAND.relative_to(ROOT).as_posix()+"/CASEBOOK.json.gz"),
        "holdsBinding":bind(CAND/"HOLD_REGISTER.json",CAND.relative_to(ROOT).as_posix()+"/HOLD_REGISTER.json"),
        "candidatePackageManifestBinding":pmb,"scope":scope,"runtimeSelectionEnabled":False})
    after["authoredCounts"]={"reviewed":700,"pending":148}; after["representationCounts"]["completeReviewedStandaloneProcedures"]=424
    rev=copy.deepcopy(after)
    for op in operations: rev["entries"][op["index"]]=op["before"]
    rev["additionalStandaloneEnvelopes"]=rev["additionalStandaloneEnvelopes"][:-1]
    rev["authoredCounts"]=copy.deepcopy(before["authoredCounts"]); rev["representationCounts"]=copy.deepcopy(before["representationCounts"])
    assert rev==before and len(operations)==5
    afterbytes=jb(after); BACKUP.write_bytes(before_bytes)
    opsdoc={"id":"RANK8-CONTROL5-INDEX-OPERATIONS-148","before":bind(BACKUP),
        "after":{"path":INDEX.relative_to(ROOT).as_posix(),"bytes":len(afterbytes),"sha256":sha(afterbytes)},
        "operations":operations,"inverse":{"semanticExact":True,"restores":"five prior entries and aggregate counts/envelope"},
        "onlyIdentityIds":IDS}
    tmp=INDEX.with_suffix(".json.application148.tmp"); tmp.write_bytes(afterbytes); os.replace(tmp,INDEX)
    assert INDEX.read_bytes()==afterbytes; opsdoc["after"]=bind(INDEX); wj(OPS,opsdoc)

    authority=copy.deepcopy(qb["currentAuthority"]); authority.update({"reviewedApplied":700,"pending":148,"acceptedUnapplied":0,"completeReviewedStandaloneProcedures":424})
    qafter=copy.deepcopy(qb); qafter.update({"id":"SPELL-REVIEW-QUEUE-148","recordedAtUtc":now(),"currentAuthority":authority,
        "currentPendingGroups":groups,"nextSuggestedGroups":groups[:5],"nextGroup":groups[0],
        "justAppliedBatch":{"reviewId":RID,"ids":IDS,"count":5,"applicationReceipt":f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APP.name}"},
        "pendingIdentityAudit":{"path":PA.name,"pending":148,"indexSha256":sha(INDEX.read_bytes())},
        "next":{"group":groups[0]["group"],"pendingCount":groups[0]["pendingCount"],"archive":groups[0]["archive"],"candidate":groups[0]["candidate"]}})
    wj(QA,qafter)
    pa={"id":"CURRENT148-PENDING-IDENTITY-AUDIT-148","recordedAtUtc":now(),"status":"PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding":bind(INDEX),"catalogBinding":bind(CATALOG),"authoredCounts":after["authoredCounts"],"pendingCount":148,
        "pendingIds":sorted(pending),"allPendingExistInSourceCatalog":all(any(x.get("id")==s for x in catalog["spells"]) for s in pending),
        "closed335AndCompletedCohortsReopened":False,"acceptedUnapplied":0}
    assert pa["allPendingExistInSourceCatalog"]; wj(PA,pa)
    ha=copy.deepcopy(hb); ha.update({"id":"CURRENT-HANDOFF-148","recordedAtUtc":now(),"status":"RANK8_CONTROL5_APPLIED_NEXT_148_PENDING",
        "currentAuthority":authority,"currentIndexBinding":bind(INDEX,"authority/authored_review_index.json"),
        "currentCatalogBinding":bind(CATALOG,"authority/catalog.json"),
        "pendingIdentityAudit":{"id":pa["id"],"path":PA.name,"pendingCount":148,"sha256":sha(PA.read_bytes())},
        "appliedThisStep":{"reviewId":RID,"ids":IDS,"count":5,"applicationReceipt":f"docs/audit/2026-10-08/full-game/director-spell-review-129/{APP.name}",
            "directorAcceptance":f"docs/audit/2026-10-08/full-game/director-spell-review-129/{RECEIPT.name}"},
        "nextGroup":groups[0]["group"],"resumePriority":"Prepare and submit the next source-queue group against 700/148, then apply only after GPT director acceptance. Preserve closed feat335 and completed spell cohorts.",
        "nextPreparedRequest":{"group":groups[0]["group"],"candidate":groups[0]["candidate"],"archive":groups[0]["archive"],
            "request":"Prepare a fresh request bound to current 700/148 authority before director review."}})
    wj(HA,ha)
    validation={"id":"RANK8-CONTROL5-APPLICATION-VALIDATION-148","status":"PASS","checksPassed":len(checks),"checksFailed":0,"checks":checks,
        "beforeIndex":bind(BACKUP),"afterIndex":bind(INDEX),"changedIdentityIds":IDS,"onlyFivePendingEntriesChanged":True,
        "authoredCounts":after["authoredCounts"],"representationCounts":after["representationCounts"],
        "sourceStatusStillBlockedForAllFive":True,"sourceCatalogHashUnchanged":CATALOG.read_bytes()==cat_bytes,
        "runtimeSelectionEnabled":False,"closed335AndCompletedCohortsReopened":False,"inverseSemanticReplayExact":rev==before,
        "backupByteExact":BACKUP.read_bytes()==before_bytes,"all245ReturnMembersVerified":True,
        "acceptedUnapplied":0,"nextGroup":groups[0]["group"],"nextPendingCount":groups[0]["pendingCount"],
        "applicationReceipt":bind(APP),"directorAcceptanceReceipt":bind(RECEIPT)}
    wj(VALIDATION,validation)
    current=START.read_text(encoding="utf-8-sig"); marker="**Latest checkpoint: [128]"
    tail=current[current.find(marker):] if marker in current else current
    if marker in current:
        top=("# Active ordinary spell review148 — Calibration review part6\n\n"
            "Return148 is director accepted and applied for five identities in the authored procedure index: **700 applied-reviewed / 148 pending / 0 accepted-unapplied**. "
            "GPT passed 36,451 independent data checks, 985 package checks and 743 ZIP round-trip checks with zero failures; all 10 new holds and 13 retained comparison holds remain. "
            "Runtime selection, implementation, human play, balance, cosmology, release and domain-closure approval remain separate.\n\n"
            "Continue in the current source queue with **rank8-ward5** (five identities), preparing a fresh packet against the 700/148 authority. Apply only after independent exact review and director acceptance. Preserve the closed feat335 and completed spell cohorts.\n\n"
            f"Read [CURRENT-HANDOFF-148](docs/audit/2026-10-08/full-game/director-spell-review-129/{HA.name}), "
            f"[the 148-pending audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PA.name}), and "
            f"[the application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n\n")
        START.write_text(top+tail,encoding="utf-8",newline="\n")
    assert CATALOG.read_bytes()==cat_bytes and rj(INDEX)["authoredCounts"]=={"reviewed":700,"pending":148}
    assert len({e["id"] for e in rj(INDEX)["entries"] if e["authoredStatus"]=="pending-authored-procedure"})==148
    print(json.dumps({"status":"APPLIED_AND_VALIDATED","acceptedIds":IDS,"authority":authority,
        "nextGroup":groups[0]["group"],"nextPendingIds":groups[0]["pendingIds"],
        "checksPassed":len(checks),"indexSha256":sha(INDEX.read_bytes()),"catalogUnchanged":True},indent=2))

if __name__=="__main__": main("--apply" in sys.argv)
