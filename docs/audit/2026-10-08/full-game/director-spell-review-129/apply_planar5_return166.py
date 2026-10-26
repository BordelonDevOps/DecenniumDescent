from __future__ import annotations
import copy, gzip, hashlib, json, os, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
RECV=AUDIT/'planar5_return166_received'
RETURN=RECV/'DD_Rank8_Planar5_Director_Return166.zip'
DELIVERY=RECV/'DD_Rank8_Planar5_Director_Return166_DELIVERY.json'
RETURN_AUDIT=RECV/'PLANAR5_RETURN166_LOCAL_AUDIT.json'
PACKET=FULL/'DD_Rank8_Planar_5_Source_Conference_02.zip'
PACKET_AUDIT=AUDIT/'PLANAR5_PACKET_INDEPENDENT_VERIFICATION_165.json'
SOURCE_CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_planar_5_source_conference_02.json'
SOURCE_REQUEST=FULL/'RANK8_PLANAR_5_SOURCE_CONFERENCE_02_REQUEST.txt'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE_BEFORE=AUDIT/'CURRENT_SPELL_QUEUE_165.json'
HANDOFF_BEFORE=AUDIT/'CURRENT_HANDOFF_165.json'
PENDING_BEFORE=AUDIT/'CURRENT118_PENDING_IDENTITY_AUDIT_164.json'
IDS=['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
ID_SET=set(IDS)
BEFORE={'reviewed':730,'pending':118,'acceptedUnapplied':0}
AFTER={'reviewed':735,'pending':113,'acceptedUnapplied':0}
COMPLETE_BEFORE=454
COMPLETE_AFTER=459
REVIEW_ID='PLANAR5-GPT-EXACT-ACCEPTANCE-166'
APP_ID='PLANAR5-APPLICATION-167'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8planar5_reviewed_166'
STAGING=CANDIDATE.with_name(CANDIDATE.name+'.staging')
MANUSCRIPT=ROOT/'DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK8_PLANAR5_REVIEWED_166.md'
BACKUP=AUDIT/'authored_review_index.before_planar5_167.json'
DECISION=AUDIT/'GPT_DIRECTOR_DECISION_PLANAR5_166.json'
ACCEPTANCE=AUDIT/'PLANAR5_EXACT_ACCEPTANCE_166.json'
APPLICATION=AUDIT/'PLANAR5_APPLICATION_167.json'
OPERATIONS=AUDIT/'PLANAR5_INDEX_OPERATIONS_167.json'
PENDING_AFTER=AUDIT/'CURRENT113_PENDING_IDENTITY_AUDIT_167.json'
QUEUE_AFTER=AUDIT/'CURRENT_SPELL_QUEUE_167.json'
HANDOFF_AFTER=AUDIT/'CURRENT_HANDOFF_167.json'
VALIDATION=AUDIT/'PLANAR5_APPLICATION_VALIDATION_167.json'
START=ROOT/'START_HERE.md'
SNAPSHOT=ROOT/'SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_167.md'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def json_bytes(v)->bytes:return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def readj(p:Path):return json.loads(p.read_text(encoding='utf-8-sig'))
def writej(p:Path,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json_bytes(v))
def binding(p:Path,rel:str|None=None,raw:bytes|None=None):
    b=p.read_bytes() if raw is None else raw
    return {'path':rel or p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def now():return datetime.now(timezone.utc).isoformat()

def load_inputs():
    assert readj(RETURN_AUDIT)['status']=='PASS' and readj(RETURN_AUDIT)['checksFailed']==0
    assert readj(PACKET_AUDIT)['status']=='PASS' and readj(PACKET_AUDIT)['failures']==0
    delivery=readj(DELIVERY); archive_bytes=RETURN.read_bytes(); packet_bytes=PACKET.read_bytes()
    assert len(archive_bytes)==delivery['archive']['bytes']==26763529 and sha(archive_bytes)==delivery['archive']['sha256']=='a400fbb5388ab24fb9b8645d2eca1277e56fa8b9b992f81e6ce0afceec23c52b'
    assert delivery['accepted'] is True and delivery['applied'] is False and delivery['acceptedIds']==IDS
    with zipfile.ZipFile(RETURN) as z:
        members={n:z.read(n) for n in z.namelist()}
    decision_source=json.loads(members['DIRECTOR_DECISION.json'])
    procedures={sid:json.loads(members[f'procedures/{sid}.json']) for sid in IDS}
    casebook=json.loads(members['CASEBOOK.json']); holds=json.loads(members['HOLD_REGISTER.json'])
    counts=json.loads(members['COUNTS.json'])
    before_bytes=INDEX.read_bytes(); catalog_bytes=CATALOG.read_bytes()
    before=json.loads(before_bytes.decode('utf-8-sig')); catalog=readj(CATALOG)
    queue=readj(QUEUE_BEFORE); handoff=readj(HANDOFF_BEFORE); pending_before=readj(PENDING_BEFORE)
    assert decision_source['accepted'] is True and decision_source['applied'] is False
    assert decision_source['acceptedIds']==IDS and decision_source['rejectedIds']==[] and decision_source['knownBlockingDefects']==[]
    assert decision_source['authorityUsed']=={'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454}
    assert decision_source['canonicalAuthorityAfterThisWork'].startswith('Unchanged')
    assert decision_source['sourceArchive']['sha256']==sha(packet_bytes) and decision_source['sourceArchive']['bytes']==len(packet_bytes)
    assert counts['procedures']==5 and counts['totalCases']==29 and counts['wholeCaseHeld']==10 and counts['events']==213 and counts['eventOperations']==852 and counts['retainedHolds']==17
    assert all(q['selectedOptionIndex'] is not None for q in json.loads(members['QUESTION_DISPOSITIONS.json']))
    rows={e['id']:e for e in before['entries']}; catalog_rows={e['id']:e for e in catalog['spells']}
    live_pending={e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure'}
    assert before['authoredCounts']=={'reviewed':730,'pending':118} and before['representationCounts']['completeReviewedStandaloneProcedures']==454
    assert len(live_pending)==118 and ID_SET<=live_pending
    assert all(procedures[sid]['nativeCardAndAccessUnchanged']==catalog_rows[sid] for sid in IDS)
    assert all(rows[sid]['authoredStatus']=='pending-authored-procedure' for sid in IDS)
    assert queue['currentAuthority']==handoff['currentAuthority']=={'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454,'scopedInterfaces':173}
    assert queue['packetStatus']=='SUBMITTED_AWAITING_DIRECTOR_RETURN' and queue['currentPendingGroups'][0]['pendingIds']==IDS
    assert handoff['status']=='PLANAR5_SUBMITTED_AWAITING_DIRECTOR_RETURN'
    assert handoff['currentIndexBinding']['sha256']==sha(before_bytes) and pending_before['indexBinding']['sha256']==sha(before_bytes)
    assert pending_before['pendingCount']==118 and ID_SET<=set(pending_before['pendingIds'])
    output=[CANDIDATE,STAGING,MANUSCRIPT,BACKUP,DECISION,ACCEPTANCE,APPLICATION,OPERATIONS,PENDING_AFTER,QUEUE_AFTER,HANDOFF_AFTER,VALIDATION,SNAPSHOT]
    assert not [str(p) for p in output if p.exists()], 'Application output already exists; inspect before retrying.'
    assert CATALOG.read_bytes()==catalog_bytes
    return locals()

def apply():
    d=load_inputs();ts=now();before=d['before'];catalog=d['catalog'];queue=d['queue'];handoff_before=d['handoff'];members=d['members'];decision_source=d['decision_source'];counts=d['counts'];before_bytes=d['before_bytes'];catalog_bytes=d['catalog_bytes'];live_pending=d['live_pending'];archive_bytes=d['archive_bytes'];packet_bytes=d['packet_bytes'];holds=d['holds']
    excluded_pending=sorted(live_pending-ID_SET)
    STAGING.mkdir(parents=True,exist_ok=False)
    director_dir=STAGING/'DIRECTOR_RETURN'
    extraction_omitted=sorted(n for n in members if n.startswith('accepted-comparisons/'))
    for name,raw in members.items():
        if name in extraction_omitted: continue
        target=director_dir/PurePosixPath(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    (STAGING/'DIRECTOR_RETURN_ARCHIVE.zip').write_bytes(archive_bytes)
    (STAGING/'SOURCE_CONFERENCE_ARCHIVE.zip').write_bytes(packet_bytes)
    (STAGING/'SOURCE_CONFERENCE_CANDIDATE.json').write_bytes(SOURCE_CANDIDATE.read_bytes())
    (STAGING/'SOURCE_CONFERENCE_REQUEST.txt').write_bytes(SOURCE_REQUEST.read_bytes())
    (STAGING/'SOURCE_PACKET_VERIFICATION.json').write_bytes(PACKET_AUDIT.read_bytes())
    (STAGING/'RETURN_INDEPENDENT_AUDIT.json').write_bytes(RETURN_AUDIT.read_bytes())
    (STAGING/'DIRECTOR_DELIVERY.json').write_bytes(DELIVERY.read_bytes())
    casebook_bytes=members['CASEBOOK.json']
    with (STAGING/'CASEBOOK.json.gz').open('wb') as out:
        with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as gz:gz.write(casebook_bytes)
    assert gzip.decompress((STAGING/'CASEBOOK.json.gz').read_bytes())==casebook_bytes
    procedure_rows=[]
    for pos,sid in enumerate(IDS):
        p=d['procedures'][sid];native=p['nativeCardAndAccessUnchanged'];old=next(x for x in before['entries'] if x['id']==sid)
        assert native['id']==sid and native['name']==old['name']
        procedure_rows.append({'id':sid,'name':native['name'],'procedure':{'common':copy.deepcopy(p['commonRules']),'rules':copy.deepcopy(p['localRules'])},'directorProcedureRecord':copy.deepcopy(p),'nativeCardAndAccessUnchanged':copy.deepcopy(native),'questionDispositions':copy.deepcopy(p['questionDispositions']),'runtimeSelectionEnabled':False})
    hold_ids=[h['id'] for h in holds]
    model={
      'schemaVersion':1,'moduleId':'rank8-planar5-reviewed-166','status':'EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS',
      'scope':'Exactly the five GPT-accepted Planar5 static authored procedures. Native cards, catalog rows, class access, and source statuses remain unchanged. All 17 hold categories and ten whole-case holds remain. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, domain-closure or release approval is granted.',
      'acceptedIds':IDS,'excludedPendingIds':excluded_pending,
      'sharedRules':{'scope':'The ten per-spell common-rule fields remain local procedure data; no global interface or shared rule is changed.','perSpellCommon':{sid:copy.deepcopy(d['procedures'][sid]['commonRules']) for sid in IDS}},
      'spells':procedure_rows,'questionDispositions':json.loads(members['QUESTION_DISPOSITIONS.json']),'originalObligations':json.loads(members['ORIGINAL_OBLIGATIONS.json']),'futureCaseDispositions':json.loads(members['FUTURE_CASE_DISPOSITIONS.json']),
      'returnCounts':counts,'holdIds':hold_ids,'holdRegisterFile':'DIRECTOR_RETURN/HOLD_REGISTER.json','proposalOperationsFile':'DIRECTOR_RETURN/PROPOSED_CHANGES.json','casebookFile':'CASEBOOK.json.gz','casebookEncoding':'gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json','casebookSourceArchiveMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},
      'directorReturnArchive':'DIRECTOR_RETURN_ARCHIVE.zip','returnArchiveOnlyMembers':extraction_omitted,'returnArchiveOnlyRationale':'Long accepted-comparison snapshot filenames exceed Windows extraction path limits under the candidate package. All six comparison snapshots remain byte-exact in DIRECTOR_RETURN_ARCHIVE.zip and were independently verified in the source ZIP.','sourceConferenceArchive':'SOURCE_CONFERENCE_ARCHIVE.zip','sourceConferenceCandidate':'SOURCE_CONFERENCE_CANDIDATE.json','standaloneProcedures':'DIRECTOR_RETURN/STANDALONE_PROCEDURES.md','directorDecisionFile':'DIRECTOR_RETURN/DIRECTOR_DECISION.json',
      'directorReturnDeliveryObservation':{'source':'GPT Library delivery JSON cross-checked with DIRECTOR_DECISION.json and MEMBER_MANIFEST.json','archiveBytes':len(archive_bytes),'archiveSha256':sha(archive_bytes),'accepted':True,'applied':False,'memberCount':67,'passedValidationChecks':7770,'failedValidationChecks':0,'passedPackageChecks':274,'failedPackageChecks':0},
      'directorReturnBinding':binding(RETURN,f'{RECV.relative_to(ROOT).as_posix()}/{RETURN.name}',archive_bytes),'directorDeliveryBinding':binding(DELIVERY),
      'sourceConferencePacketVerification':binding(PACKET_AUDIT),'independentReturnAudit':binding(RETURN_AUDIT),
      'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,'domainClosure':False
    }
    package_files=[]
    for path in sorted(STAGING.rglob('*')):
        rel=path.relative_to(STAGING).as_posix()
        if path.is_file() and rel not in {'MODEL.json','CANDIDATE_PACKAGE_MANIFEST.json'}:
            raw=path.read_bytes();package_files.append({'path':rel,'bytes':len(raw),'sha256':sha(raw)})
    package_manifest={'id':'RANK8-PLANAR5-CANDIDATE-PACKAGE-MANIFEST-167','sourceArchive':{'name':RETURN.name,'bytes':len(archive_bytes),'sha256':sha(archive_bytes)},'files':package_files,'excludedFromBindings':['CANDIDATE_PACKAGE_MANIFEST.json','MODEL.json'],'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'}
    writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',package_manifest)
    model['candidatePackageManifestBinding']=binding(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/CANDIDATE_PACKAGE_MANIFEST.json')
    writej(STAGING/'MODEL.json',model)
    model_binding=binding(STAGING/'MODEL.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/MODEL.json')
    casebook_binding=binding(STAGING/'CASEBOOK.json.gz',f'{CANDIDATE.relative_to(ROOT).as_posix()}/CASEBOOK.json.gz')
    archive_binding=binding(RETURN,f'{RECV.relative_to(ROOT).as_posix()}/{RETURN.name}',archive_bytes)
    packet_binding=binding(STAGING/'SOURCE_CONFERENCE_ARCHIVE.zip',f'{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_ARCHIVE.zip')
    source_candidate_binding=binding(STAGING/'SOURCE_CONFERENCE_CANDIDATE.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/SOURCE_CONFERENCE_CANDIDATE.json')
    hold_binding=binding(director_dir/'HOLD_REGISTER.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/HOLD_REGISTER.json')
    proposal_binding=binding(director_dir/'PROPOSED_CHANGES.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/PROPOSED_CHANGES.json')
    procedure_source_binding=binding(director_dir/'DIRECTOR_DECISION.json',f'{CANDIDATE.relative_to(ROOT).as_posix()}/DIRECTOR_RETURN/DIRECTOR_DECISION.json')
    decision_record={'id':'GPT-DIRECTOR-DECISION-PLANAR5-166','recordedAtUtc':ts,'source':{'product':'ChatGPT','project':'Dungeon Crawler','conversation':'Calibration review part 6','conversationId':'6adc506d-8770-83ea-b64c-0345d9b9b682'},'decisionId':decision_source['id'],'accepted':True,'appliedAtDecision':False,'acceptedIds':IDS,'rejectedIds':[],'remainingBlockingDefects':[],'verification':{'directorChecksPassed':7770,'directorChecksFailed':0,'directorPackageChecksPassed':274,'independentReturnAudit':readj(RETURN_AUDIT),'sourcePacketVerification':readj(PACKET_AUDIT),'returnArchiveMembers':67,'sourceArchiveMembers':98,'sourceQuestions':24,'historicalIndividualQuestionsPreserved':5,'futureObligations':7,'cases':29,'wholeHeldCases':10,'events':213,'eventOperations':852,'proposalOperations':20,'retainedHolds':17},'acceptedArchive':{'name':RETURN.name,'bytes':len(archive_bytes),'sha256':sha(archive_bytes)},'sourceArchive':{'name':PACKET.name,'bytes':len(packet_bytes),'sha256':sha(packet_bytes)},'scope':decision_source['decisionScope'],'holdScope':'All 17 source, access, cosmology, content, physical, equipment, lifecycle, information, structure, naming, site, visitor, tether, runtime, human-play, balance and release holds remain. Ten whole cases remain held, including both Gloom Bind main cases and their destination-dependent branches. No runtime, human-play, balance, cosmology, domain-closure or release approval is granted.','excludedClaims':{'runtime':False,'humanPlay':False,'balance':False,'cosmology':False,'domainClosure':False,'release':False,'canonicalApplication':False},'directorMadeNoCanonicalChanges':True}
    writej(DECISION,decision_record)
    acceptance={'id':REVIEW_ID,'recordedAtUtc':ts,'status':'DIRECTOR_ACCEPTED_EXACT_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS','decision':'ACCEPTED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','directorDecision':decision_record,'directorReturn':{'path':f'{RECV.relative_to(ROOT).as_posix()}/{RETURN.name}','bytes':len(archive_bytes),'sha256':sha(archive_bytes)},'acceptedIds':IDS,'countsBefore':{**BEFORE,'scopedInterfaces':173},'countsAfter':{**AFTER,'scopedInterfaces':173},'completeReviewedStandaloneProceduresBefore':454,'completeReviewedStandaloneProceduresAfter':459,'acceptedCases':29,'acceptedMainCases':10,'acceptedBranches':19,'wholeHeldCases':10,'acceptedEvents':213,'eventOperations':852,'retainedHolds':17,'sourceStatusPreserved':'blocked-pending-operational-review for all five identities; static authored procedure review only.','runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,'canonicalApplicationPerformed':False}
    writej(ACCEPTANCE,acceptance)
    os.replace(STAGING,CANDIDATE)
    manuscript_text=(CANDIDATE/'DIRECTOR_RETURN'/'STANDALONE_PROCEDURES.md').read_text(encoding='utf-8-sig')
    MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True);MANUSCRIPT.write_text(manuscript_text,encoding='utf-8',newline='\n')
    app={'id':APP_ID,'recordedAtUtc':ts,'status':'APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS','reviewId':REVIEW_ID,'ownerInstruction':'Apply each exact accepted ordinary-spell batch, push it to GitHub, and continue until no pending spell identities remain.','acceptedIds':IDS,'directorAcceptance':binding(ACCEPTANCE),'directorDecision':binding(DECISION),'directorReturn':archive_binding,'candidateEnvelope':model_binding,'candidatePackageManifest':binding(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json'),'indexBefore':binding(BACKUP,raw=before_bytes),'counts':{'before':{**BEFORE,'scopedInterfaces':173},'after':{**AFTER,'scopedInterfaces':173}},'completeReviewedStandaloneProcedures':{'before':454,'after':459},'cases':29,'completeStaticFixtures':19,'wholeHeldCases':10,'events':213,'eventOperations':852,'retainedHolds':17,'sourceStatusPreservedAsBlocked':True,'catalogChanged':False,'runtimeSelectionEnabled':False,'closedCohortsReopened':False}
    writej(APPLICATION,app);app_binding=binding(APPLICATION)
    after=copy.deepcopy(before);ops=[]
    for pos,sid in enumerate(IDS):
        idx=next(i for i,row in enumerate(before['entries']) if row['id']==sid);old=before['entries'][idx];new=copy.deepcopy(old)
        new.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank8planar5_reviewed_166/MODEL.json','procedurePointer':f'/spells/{pos}/procedure','wholeCardPointer':f'/spells/{pos}','sourceCatalogWholeCardPointer':old.get('sourceCatalogWholeCardPointer') or old['wholeCardPointer'],'wholeCardIdField':'id','procedureTextPointer':f'/spells/{pos}/procedure','directorProcedureRecordPointer':f'/spells/{pos}/directorProcedureRecord','sharedRulesPointer':'/sharedRules/perSpellCommon','manuscript':'../../../docs/spells/candidates/RANK8_PLANAR5_REVIEWED_166.md','reviewId':APP_ID,'runtimeSelectionEnabled':False,'historicalCandidateLabelsPreserved':True,'completeEvidenceRoot':CANDIDATE.relative_to(ROOT).as_posix(),'completeEnvelopeBinding':model_binding,'casebookBinding':casebook_binding,'casebookEncoding':'gzip; exact decompression reproduces DIRECTOR_RETURN/CASEBOOK.json','casebookSourceArchiveMemberBinding':model['casebookSourceArchiveMemberBinding'],'sourceArchiveBinding':archive_binding,'sourceConferenceArchiveBinding':packet_binding,'sourceCandidateBinding':source_candidate_binding,'candidatePackageManifestBinding':binding(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json'),'retainedHoldsBinding':hold_binding,'procedureSourceBinding':procedure_source_binding,'proposalOperationsBinding':proposal_binding,'acceptedSharedRuleScope':acceptance['decision'],'authoredAcceptanceReceipt':binding(ACCEPTANCE),'authoredApplicationReceipt':app_binding})
        ops.append({'op':'replace-entry','identity':sid,'index':idx,'before':copy.deepcopy(old),'after':copy.deepcopy(new)});after['entries'][idx]=new
    after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/rank8planar5_reviewed_166/MODEL.json','binding':model_binding,'reviewId':REVIEW_ID,'acceptedIds':IDS,'excludedPendingIds':excluded_pending,'authority':binding(ACCEPTANCE),'applicationReceipt':f'{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}','sourceArchive':archive_binding,'sourceConferenceArchive':packet_binding,'casebookBinding':casebook_binding,'holdsBinding':hold_binding,'candidatePackageManifestBinding':binding(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json'),'scope':acceptance['decision'],'runtimeSelectionEnabled':False})
    after['authoredCounts']={'reviewed':735,'pending':113};after['representationCounts']['completeReviewedStandaloneProcedures']=459
    pending_after={e['id'] for e in after['entries'] if e['authoredStatus']=='pending-authored-procedure'}
    assert len(ops)==5 and len(pending_after)==113 and pending_after==live_pending-ID_SET
    assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in after['entries'])==735
    inverse=copy.deepcopy(after)
    for op in ops:inverse['entries'][op['index']]=copy.deepcopy(op['before'])
    inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]
    inverse['authoredCounts']=copy.deepcopy(before['authoredCounts']);inverse['representationCounts']=copy.deepcopy(before['representationCounts'])
    assert inverse==before
    after_bytes=json_bytes(after);BACKUP.write_bytes(before_bytes)
    writej(OPERATIONS,{'id':'PLANAR5-INDEX-OPERATIONS-167','before':binding(BACKUP,raw=before_bytes),'after':{'path':INDEX.relative_to(ROOT).as_posix(),'bytes':len(after_bytes),'sha256':sha(after_bytes)},'operations':ops,'inverse':{'semanticExact':True,'restores':'five prior entries, aggregate authored counts, standalone-envelope array and representation count'},'onlyIdentityIds':IDS})
    tmp=INDEX.with_suffix('.json.planar5-167.tmp');tmp.write_bytes(after_bytes);os.replace(tmp,INDEX)
    assert CATALOG.read_bytes()==catalog_bytes
    authority={'reviewedApplied':735,'pending':113,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':459,'scopedInterfaces':173}
    remaining_groups=[]
    for group in queue['currentPendingGroups']:
        left=[sid for sid in group['pendingIds'] if sid in pending_after]
        if left:
            row=copy.deepcopy(group);row['pendingIds']=left;row['pendingCount']=len(left);row['freshPacketRequiredForCurrentAuthority']=True;row.pop('submission',None);row['status']='PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY';remaining_groups.append(row)
    assert remaining_groups[0]['group']=='rank8-remaining4' and sum(g['pendingCount'] for g in remaining_groups)==113
    pending_doc={'id':'CURRENT113-PENDING-IDENTITY-AUDIT-167','recordedAtUtc':now(),'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':binding(INDEX),'catalogBinding':binding(CATALOG),'authoredCounts':after['authoredCounts'],'pendingCount':113,'pendingIds':sorted(pending_after),'allPendingExistInSourceCatalog':all(any(card.get('id')==sid for card in catalog['spells']) for sid in pending_after),'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0}
    assert pending_doc['allPendingExistInSourceCatalog'];writej(PENDING_AFTER,pending_doc)
    queue_after=copy.deepcopy(queue);queue_after.update({'id':'SPELL-REVIEW-QUEUE-167','recordedAtUtc':now(),'currentAuthority':authority,'currentPendingGroups':remaining_groups,'nextSuggestedGroups':remaining_groups[:5],'nextGroup':remaining_groups[0]['group'],'justAppliedBatch':{'reviewId':REVIEW_ID,'ids':IDS,'count':len(IDS),'applicationReceipt':f'{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}'},'pendingIdentityAudit':{'path':PENDING_AFTER.name,'pending':113,'sha256':sha(PENDING_AFTER.read_bytes())},'next':{'group':remaining_groups[0]['group'],'pendingCount':remaining_groups[0]['pendingCount'],'archive':remaining_groups[0]['archive'],'freshPacketRequiredForCurrentAuthority':True,'status':'PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY'},'packetStatus':'PLANAR5_RETURN166_APPLIED_735_113'});writej(QUEUE_AFTER,queue_after)
    handoff=copy.deepcopy(handoff_before);handoff.update({'id':'CURRENT-HANDOFF-167','recordedAtUtc':now(),'status':'PLANAR5_APPLIED_NEXT_113_PENDING','currentAuthority':authority,'currentIndexBinding':binding(INDEX,'authority/authored_review_index.json'),'currentCatalogBinding':binding(CATALOG,'authority/catalog.json'),'currentQueueBinding':binding(QUEUE_AFTER),'pendingIdentityAudit':{'id':pending_doc['id'],'path':PENDING_AFTER.name,'pendingCount':113,'sha256':sha(PENDING_AFTER.read_bytes())},'appliedThisStep':{'reviewId':REVIEW_ID,'ids':IDS,'count':5,'applicationReceipt':f'{AUDIT.relative_to(ROOT).as_posix()}/{APPLICATION.name}','directorAcceptance':f'{AUDIT.relative_to(ROOT).as_posix()}/{ACCEPTANCE.name}'},'nextGroup':remaining_groups[0]['group'],'retainedBoundary':'Do not redo feats, completed spell cohorts, or previously accepted/applied spell batches. Runtime, source, access, cosmology, content, lifecycle and release holds remain separate and active.','resumePriority':f"Prepare a fresh {remaining_groups[0]['group']} packet against current 735/113 authority, submit it to the same GPT director, independently audit the exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.",'nextPreparedRequest':{'group':remaining_groups[0]['group'],'candidate':remaining_groups[0].get('candidate'),'historicalArchive':remaining_groups[0].get('archive'),'freshPacketRequiredForCurrentAuthority':True,'request':'Build a fresh source packet and archive bound to current 735/113 authority before director review.'}});writej(HANDOFF_AFTER,handoff)
    old_start=START.read_text(encoding='utf-8-sig') if START.exists() else '';marker='**Prior checkpoint: [';at=old_start.find(marker);historic=old_start[at:] if at>=0 else ''
    START.write_text(f"# Active ordinary spell review167 — Calibration review part 6\n\nPlanar5 Return166 was accepted by the GPT director, independently audited, and applied to exactly five identities: **735 reviewed / 113 pending / 0 accepted-unapplied**. All 17 hold categories and ten whole-case holds remain; no runtime, human-play, balance, cosmology, domain closure or release approval is included.\n\nContinue with **{remaining_groups[0]['group']}** using a fresh packet against 735/113 authority. Apply only exact accepted IDs, pushing each applied batch to GitHub. Preserve completed feat and spell cohorts.\n\nRead [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{ACCEPTANCE.name}), and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n\n"+historic,encoding='utf-8',newline='\n')
    SNAPSHOT.write_text(f"# Ordinary spell review snapshot — Planar5 Return166\n\nAs of 2026-10-25, authored ordinary-spell authority is **735 reviewed / 113 pending / 0 accepted-unapplied**. The GPT director accepted and this application records exactly demiplane, maze, planar-seal, seal-of-banishment and gloom-bind.\n\nThe return ZIP is {len(archive_bytes):,} bytes with SHA-256 `{sha(archive_bytes)}`. The director reports 7,770 validation checks and 274 packaging checks passed; independent local verification passed 32 checks across all 67 return members, source bindings, cases and retained holds.\n\nAll 17 hold categories and ten whole-case holds remain, including four held Gloom Bind cases. Native catalog data, class access and source status are unchanged; the procedures remain blocked from runtime selection. This static review gives no runtime, human-play, balance, cosmology, domain-closure or release approval.\n\nThe next pending group is {remaining_groups[0]['group']} with {remaining_groups[0]['pendingCount']} identities and requires a fresh packet against 735/113 authority. Continue until pending reaches zero.\n\nSee [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{HANDOFF_AFTER.name}), [pending identity audit](docs/audit/2026-10-08/full-game/director-spell-review-129/{PENDING_AFTER.name}), [exact acceptance](docs/audit/2026-10-08/full-game/director-spell-review-129/{ACCEPTANCE.name}), and [application validation](docs/audit/2026-10-08/full-game/director-spell-review-129/{VALIDATION.name}).\n",encoding='utf-8',newline='\n')
    assert CATALOG.read_bytes()==catalog_bytes
    print(json.dumps({'status':'APPLIED_READY_FOR_INDEPENDENT_VERIFICATION','acceptedIds':IDS,'authority':authority,'nextGroup':remaining_groups[0]['group'],'nextPendingCount':remaining_groups[0]['pendingCount'],'returnArchive':binding(RETURN),'indexSha256':sha(INDEX.read_bytes())},indent=2))

if __name__=='__main__':
    if '--apply' in sys.argv:apply()
    else:
        d=load_inputs();print(json.dumps({'status':'PREFLIGHT_PASS','acceptedIds':IDS,'authorityBefore':{'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454,'scopedInterfaces':173},'authorityAfter':{'reviewedApplied':735,'pending':113,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':459,'scopedInterfaces':173},'nextGroupAfterApply':'rank8-remaining4','returnBytes':RETURN.stat().st_size,'outputAbsent':not CANDIDATE.exists(),'catalogUnchanged':True},indent=2))
