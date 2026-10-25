import datetime,hashlib,json,zipfile
from pathlib import Path
BASE=Path(r'C:\Github\DecenniumDescent')
AUDIT=BASE/'docs/audit/2026-10-08/full-game/director-spell-review-129'
ZIP= AUDIT/'DD_Information8_Director_Return03_131.zip'
AUDIT_REPORT=AUDIT/'INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json'
INDEX=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
MODEL_OUT=AUDIT/'INFORMATION8_FINDPATH_EXACT_REFERENCE_MODEL_129.json'
ACCEPT_OUT=AUDIT/'INFORMATION8_EXACT_ACCEPTANCE_129.json'
def sha(b): return hashlib.sha256(b).hexdigest()
report=json.loads(AUDIT_REPORT.read_text(encoding='utf-8-sig'))
assert report['status']=='PASS' and report['checksPassed']==199 and report['failed']==0
assert sha(ZIP.read_bytes())==report['archive']['sha256']
idx_bytes=INDEX.read_bytes(); idx=json.loads(idx_bytes.decode('utf-8-sig'))
assert sha(idx_bytes)=='44fec30864c5836b9d07ef3ee26b2aa63dfe89cda9bdaf824ff040e434ec1f72'
assert idx['authoredCounts']=={'reviewed':635,'pending':213}
pending=next(e for e in idx['entries'] if e['id']=='find-the-path')
assert pending['authoredStatus']=='pending-authored-procedure' and pending['procedurePointer'] is None
with zipfile.ZipFile(ZIP) as z:
    procedures=json.loads(z.read('PROCEDURES.json'))['spells']
    proc=next(x for x in procedures if x['spellId']=='find-the-path')
    rules=json.loads(z.read('SHARED_RULES.json'))
    review=json.loads(z.read('REVIEW_STATUS.json'))
    assert review['pendingCorrectionIds']==['find-the-path']
    assert proc['sharedRuleIds']==[x['id'] for x in rules]
    prior=['arcane-eye','faction-destiny','legend-lore','prophetic-frenzy','concordant-mindlink','faction-prophecy','resonance-prophecy']
    model={'id':'INFORMATION8-FINDTHEPATH-EXACT-REFERENCE-MODEL-129','acceptedIds':['find-the-path'],'excludedPendingIds':[],'previouslyAppliedIds':prior,'completeProcedures':[proc],'sharedRules':rules,'assemblyOnly':True}
    model_bytes=(json.dumps(model,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    MODEL_OUT.write_bytes(model_bytes)
    manifest_bytes=z.read('MANIFEST.json')
    case_rows=[]
    for cid in ['DI6-04-A','DI6-04-B']:
        member=f'cases/{cid}.json'; b=z.read(member); obj=json.loads(b)
        assert obj['spellId']=='find-the-path'
        case_rows.append({'id':cid,'archiveMember':member,'bytes':len(b),'sha256':sha(b),'branches':[x['id'] for x in obj.get('branches',[])]})
    event=json.loads(z.read('cases/DI6-04-B.json'))['branches'][0]['timeline'][12]
    source=proc['source']; source_path=BASE/source['path']; source_bytes=source_path.read_bytes()
    assert len(source_bytes)==source['bytes'] and sha(source_bytes)==source['sha256']
    receipt={'id':'INFORMATION8-FINDTHEPATH-EXACT-AUTHORED-ACCEPTANCE-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ACCEPTED_FOR_AUTHORED_OPERATIONAL_PLAYTEST_WITH_RETAINED_TOPOLOGY_HOLD','ownerInstruction':'Continue until all originally pending ordinary spell identities are accepted and applied; apply each exact accepted batch and continue in Calibration Review Part 6.','scope':{'acceptedIds':['find-the-path'],'previouslyAppliedIdsExcluded':prior,'acceptedCaseIds':['DI6-04-A','DI6-04-B'],'acceptedQuestions':['INFO8-Q09','INFO8-Q10','INFO8-126-PATH-AND-LORE-ANCHORS','INFO8-126-INFORMATION-VIEWS-AND-HISTORY'],'sharedRuleIds':proc['sharedRuleIds'],'exactProcedureObject':{'sourceArchiveMember':'PROCEDURES.json#/spells/4','spellId':'find-the-path','sourcePath':source['path'],'sourcePointer':proc['pointer'],'sourceBytes':source['bytes'],'sourceSha256':source['sha256']},'caseFiles':case_rows},'sourceArchive':{'path':str(ZIP),'bytes':ZIP.stat().st_size,'sha256':report['archive']['sha256'],'members':report['archive']['members'],'manifestBytes':len(manifest_bytes),'manifestSha256':sha(manifest_bytes)},'independentAudit':{'path':str(AUDIT_REPORT),'bytes':AUDIT_REPORT.stat().st_size,'sha256':sha(AUDIT_REPORT.read_bytes()),'checksPassed':report['checksPassed'],'status':report['status']},'acceptedReferenceModel':{'path':str(MODEL_OUT),'bytes':len(model_bytes),'sha256':sha(model_bytes),'completeProcedureCount':1,'sharedRuleCount':len(rules)},'priorReturn02':{'bytes':482654646,'sha256':'f8a5f7ee9125a45c12f3bf5caa1907294207b986877eb354dd69895930d32c7c','semanticReview':'INFORMATION8_RETURN02_SEMANTIC_REVIEW_129.json','priorReturnedProcedureAndSharedRulesUnchanged':True},'recipientViewCorrection':{'eventId':'DI6-04-B/actual-crossbar-after-snapshot:12','outputExactly':'Indeterminate','beforeStateSha256':event['beforeStateSha256'],'afterStateSha256':event['afterStateSha256'],'forwardAndInverseVerified':True,'privateMissingTopologyAndUnprovedShortestQualificationPreserved':True},'retainedHolds':['PROTECTED-SHORTER-TERRAIN','GENERIC-CAMPAIGN-CONTENT','all other original source/content/runtime/human/balance/cosmology/temporal/release holds'], 'explicitUnresolvedBoundary':'Only Find the Path authored procedure and its actual two source cases are accepted. The postbar 120-foot route remains a possible traversable detour; incomplete surrounding topology does not prove global shortest. The actual protected-indispensable-shorter-terrain case remains a whole-case hold. No protected route fixture, runtime, human play, balance, cosmology, temporal or release approval is claimed.', 'currentIndexBefore':{'path':str(INDEX),'bytes':len(idx_bytes),'sha256':sha(idx_bytes),'reviewed':635,'pending':213,'acceptedUnapplied':0},'application':'Authorized by the owner after exact independent review; will apply only find-the-path and preserve seven Information identities already applied.' ,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'classOrGlobalRuleAmendment':False,'closedCohortsReopened':False}
ACCEPT_OUT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'acceptance':str(ACCEPT_OUT),'status':receipt['status'],'acceptedIds':receipt['scope']['acceptedIds'],'modelSha256':receipt['acceptedReferenceModel']['sha256'],'archiveSha256':receipt['sourceArchive']['sha256'],'caseIds':receipt['scope']['acceptedCaseIds'],'retainedHolds':receipt['retainedHolds'],'currentBefore':receipt['currentIndexBefore']},ensure_ascii=False,indent=2))
