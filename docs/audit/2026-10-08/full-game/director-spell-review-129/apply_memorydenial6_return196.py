from __future__ import annotations
import copy, gzip, hashlib, json, shutil, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
REC=AUDIT/'rank9_memorydenial6_return196_received'
ZIP=REC/'DD_Rank9_MemoryDenial6_Director_Return196.zip'
DELIVERY=REC/'DD_Rank9_MemoryDenial6_Director_Return196_DELIVERY.json'
AUDIT_JSON=AUDIT/'RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
Q0=AUDIT/'CURRENT_SPELL_QUEUE_195.json'
H0=AUDIT/'CURRENT_HANDOFF_195.json'
P0=AUDIT/'CURRENT66_PENDING_IDENTITY_AUDIT_195.json'
BACKUP=AUDIT/'authored_review_index.before_memorydenial6_196.json'
PKG_REL=Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196')
PKG=ROOT/PKG_REL
STAGE=PKG.with_name(PKG.name+'.staging')
MAN=ROOT/'DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_MEMORYDENIAL6_REVIEWED_196.md'
ACCEPTED=['mass-willbreaker','mind-prison-mass','mind-wipe','unmake-spell']
UNACCEPTED=['mind-collapse','unravel-identity']
GROUP=ACCEPTED+UNACCEPTED
NEXT='rank9-knowledge-revelation5'
NEXT_IDS=['cosmic-awareness','cosmic-revelation','divine-truth','oracle-of-eternity','faction-omniscience-supreme']
BEFORE={'reviewed':782,'pending':66}
AFTER={'reviewed':786,'pending':62}
COMPLETE0,COMPLETE1=506,510
REVIEW='RANK9-MEMORYDENIAL6-EXACT-AUTHORED-ACCEPTANCE-196'
APP='RANK9-MEMORYDENIAL6-APPLICATION-196'
DEC=AUDIT/'RANK9_MEMORYDENIAL6_DIRECTOR_DECISION_196.json'
ACC=AUDIT/'RANK9_MEMORYDENIAL6_EXACT_ACCEPTANCE_196.json'
RCPT=AUDIT/'RANK9_MEMORYDENIAL6_RETURN196_RECEIPT.json'
APPFILE=AUDIT/'RANK9_MEMORYDENIAL6_APPLICATION_196.json'
OPS=AUDIT/'RANK9_MEMORYDENIAL6_INDEX_OPERATIONS_196.json'
P1=AUDIT/'CURRENT62_PENDING_IDENTITY_AUDIT_196.json'
Q1=AUDIT/'CURRENT_SPELL_QUEUE_196.json'
H1=AUDIT/'CURRENT_HANDOFF_196.json'
VALID=AUDIT/'RANK9_MEMORYDENIAL6_APPLICATION_VALIDATION_196.json'
SNAP=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_196.md'
PREP_PACKET=AUDIT/'rank9_memorydenial6_current_source_195_prepared/DD_Rank9_MemoryDenial6_CurrentSource_195.zip'

def sha(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def jb(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(jb(v))
def bind(p,raw=None):
    b=p.read_bytes() if raw is None else raw
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def copy_member(z,name,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with z.open(name,'r') as src,target.open('wb') as dst:
        shutil.copyfileobj(src,dst,1024*1024)

def main():
    outputs=[BACKUP,MAN,DEC,ACC,RCPT,APPFILE,OPS,P1,Q1,H1,VALID,SNAP]
    assert not PKG.exists() and not STAGE.exists() and all(not p.exists() for p in outputs)
    audit=read(AUDIT_JSON); delivery=read(DELIVERY)
    assert audit['status']=='PASS' and audit['checksPassed']==20 and audit['checksFailed']==0 and audit['applied'] is False
    assert audit['acceptedIds']==ACCEPTED and audit['unacceptedIds']==UNACCEPTED
    assert sha_file(ZIP)==delivery['archive']['sha256']==audit['returnArchive']['sha256']=='bc00b730c195ae835c560fd06945d04ae58359a5cbf8dccf6f72f7873d078ee4'
    assert ZIP.stat().st_size==delivery['archive']['bytes']==234272866
    assert delivery['applied'] is False and delivery['acceptedIds']==ACCEPTED and delivery['unacceptedIds']==UNACCEPTED
    baseline={'reviewedApplied':782,'pending':66,'acceptedUnapplied':0,'completeStandaloneProcedures':506,'scopedInterfaces':173}
    before_raw,catalog_raw=INDEX.read_bytes(),CATALOG.read_bytes()
    before,catalog=read(INDEX),read(CATALOG)
    q0,h0,p0=map(read,(Q0,H0,P0))
    rows={x['id']:x for x in before['entries']}
    cats={x['id']:x for x in catalog['spells']}
    live={x['id'] for x in before['entries'] if x['authoredStatus']=='pending-authored-procedure'}
    assert before['authoredCounts']==BEFORE and before['representationCounts']['completeReviewedStandaloneProcedures']==COMPLETE0
    assert len(live)==66 and set(GROUP)<=live and set(p0['pendingIds'])==live and p0['indexBinding']['sha256']==sha(before_raw)
    assert q0['currentAuthority']==baseline and q0['pendingCount']==66
    assert h0['currentAuthority']==baseline and h0['status']=='RANK9_MEMORY_DENIAL6_PACKET_195_SUBMITTED_AWAITING_GPT_RETURN_782_66'
    assert all(rows[s]['sourceStatus']=='blocked-pending-operational-review' for s in GROUP)
    timestamp=datetime.now(timezone.utc).isoformat()

    with zipfile.ZipFile(ZIP) as z:
        director=json.loads(z.read('DIRECTOR_DECISION.json'))
        model_src=json.loads(z.read('MODEL.json'))
        decisions={x['id']:x for x in director['decisions']}
        procs={s:json.loads(z.read(f'procedures/{s}.json')) for s in GROUP}
        blocks=delivery['blockers']
        assert director['acceptedIds']==ACCEPTED and director['unacceptedIds']==UNACCEPTED
        assert director['authorityBaseline']==baseline
        assert director['nextQueueGroup']['group']==NEXT and director['nextQueueGroup']['pendingIds']==NEXT_IDS
        assert set(decisions)==set(procs)==set(GROUP)
        assert all(decisions[s]['accepted'] and not decisions[s]['applied'] and not decisions[s]['blockerIds'] for s in ACCEPTED)
        assert all(not decisions[s]['accepted'] and not decisions[s]['applied'] and decisions[s]['blockerIds'] for s in UNACCEPTED)
        assert all(procs[s]['accepted'] and not procs[s]['applied'] and procs[s]['completeSourceAndAccess']==cats[s] for s in ACCEPTED)
        assert all(not procs[s]['accepted'] and not procs[s]['applied'] for s in UNACCEPTED)
        assert model_src['applied'] is False and model_src['acceptedIds']==ACCEPTED and model_src['unacceptedIds']==UNACCEPTED
        for s in GROUP:
            assert procs[s]['currentIndexEntryUnchanged']==rows[s]
        prior_packet=q0['currentPacket']
        assert prior_packet['path']==PREP_PACKET.relative_to(ROOT).as_posix() and prior_packet['bytes']==PREP_PACKET.stat().st_size and prior_packet['sha256']==sha_file(PREP_PACKET)=='d836a1588168384d947f720e0f253745cc4b3eb33f975a8af7d48c357f73b66c'

        STAGE.mkdir(parents=True)
        for name in z.namelist():
            if name.endswith('/') or name in ('CASEBOOK.json','SOURCE_PACKET_195.zip') or name.startswith(('cases/','additional_sources/')):
                continue
            copy_member(z,name,STAGE/name)
        source_map=[]
        for pos,binding in enumerate(json.loads(z.read('SOURCE_VERIFICATION.json'))['additionalBindings']):
            member='additional_sources/'+binding['path']
            short=str(pos).zfill(2)+'_'+binding['sha256'][:12]+'_'+binding['path'].rsplit('/',1)[-1]
            target=STAGE/'supplemental_sources'/short
            copy_member(z,member,target)
            raw=target.read_bytes()
            assert len(raw)==binding['bytes'] and sha(raw)==binding['sha256']
            source_map.append({'sourcePath':binding['path'],'packagePath':(PKG_REL/'supplemental_sources'/short).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
        write(STAGE/'SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json',{'sourceCommit':audit['sourceCommit'],'count':len(source_map),'sources':source_map})
        source_map_bind=bind(STAGE/'SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json')
        with z.open('CASEBOOK.json','r') as src:
            with (STAGE/'CASEBOOK.json.gz').open('wb') as raw:
                with gzip.GzipFile(fileobj=raw,mode='wb',filename='',mtime=0,compresslevel=6) as gz:
                    shutil.copyfileobj(src,gz,1024*1024)
        (STAGE/'DIRECTOR_DELIVERY_OBSERVATION.json').write_bytes(DELIVERY.read_bytes())
        (STAGE/'INDEPENDENT_RETURN_AUDIT.json').write_bytes(AUDIT_JSON.read_bytes())
        arc_bind,del_bind,audit_bind=bind(ZIP),bind(DELIVERY),bind(AUDIT_JSON)
        packet_bind=bind(PREP_PACKET)
        pkg_casebook_bind=bind(PKG/'CASEBOOK.json.gz',(STAGE/'CASEBOOK.json.gz').read_bytes())
        case_index=json.loads(z.read('CASE_INDEX.json'))
        case_rows={s:[x for x in case_index['cases'] if x['spellId']==s] for s in GROUP}
        case_ids={s:[x['id'] for x in case_rows[s]] for s in GROUP}
        accepted_case_ids={c for s in ACCEPTED for c in case_ids[s]}
        accepted_events=sum(x['events'] for s in ACCEPTED for x in case_rows[s])
        spells=[]
        for pos,s in enumerate(ACCEPTED):
            proc=procs[s]
            spells.append({
                'id':s,'name':rows[s]['name'],'position':pos,
                'procedure':{
                    'id':'MD196-STATIC-'+s.upper().replace('-','_'),
                    'spellId':s,
                    'status':'director-accepted static authored procedure; applied to authored review index; runtime disabled',
                    'accepted':True,'applied':False,
                    'nativeCardUnchanged':copy.deepcopy(proc['completeSourceAndAccess']),
                    'procedureContent':proc['procedure'],
                    'sharedRequirements':proc['commonProcedure'],
                    'newChoices':proc['newChoices'],
                    'qualifications':copy.deepcopy(proc['qualifications']),
                    'caseIds':case_ids[s],
                    'questionIds':copy.deepcopy(proc['questionIds']),
                    'holdIds':copy.deepcopy(proc['holdIds']),
                    'directorDecisionId':director['id']},
                'directorProcedureRecord':copy.deepcopy(proc),
                'nativeCardUnchanged':copy.deepcopy(proc['completeSourceAndAccess']),
                'caseIds':case_ids[s],
                'questionIds':copy.deepcopy(proc['questionIds']),
                'holdIds':copy.deepcopy(proc['holdIds']),
                'runtimeSelectionEnabled':False})
        blocker_map={s:{'blockerIds':decisions[s]['blockerIds'],'holdIds':copy.deepcopy(procs[s]['holdIds']),
                        'blockerRecords':[copy.deepcopy(b) for b in blocks if s in b['blockingForIds']]}
                     for s in UNACCEPTED}
        for s,v in blocker_map.items(): assert v['blockerRecords'] and v['blockerIds']

        model={
          'schemaVersion':1,'moduleId':'rank9memorydenial6-reviewed-196',
          'status':'FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_TWO_BLOCKERS',
          'scope':'Only the four individually accepted static procedures are applied. Mind Collapse and Unravel Identity remain pending under MD196-B01 and MD196-B02. Native cards and class routes remain unchanged; runtime and downstream approval gates stay disabled.',
          'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'excludedPendingIds':sorted(live-set(ACCEPTED)),
          'unacceptedHolds':blocker_map,
          'inheritedNamedBlockers':director['carriedNamedBlockersUnchanged'],
          'sharedRequirements':{'scope':'No global/shared rule changes; native cards and class routes unchanged.','runtimeSelectionEnabled':False},
          'spells':spells,
          'caseCoverage':{'caseCount':case_index['events'] and len(case_index['cases']),
                          'acceptedCaseCount':len(accepted_case_ids),'acceptedEventCount':accepted_events,
                          'caseIndexBinding':next(x for x in delivery['members'] if x['path']=='CASE_INDEX.json')},
          'returnCounts':delivery['counts'],
          'sourceArchive':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,
          'submittedSourcePacket':packet_bind,
          'casebookFile':'CASEBOOK.json.gz','casebookSourceArchiveMemberBinding':next(x for x in delivery['members'] if x['path']=='CASEBOOK.json'),
          'casebookBinding':pkg_casebook_bind,
          'supplementalSourcePackageMap':source_map_bind,
          'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,
          'implementationApproved':False,'humanPlaytested':False,'balanceApproved':False,
          'cosmologyModified':False,'releaseApproved':False,'domainClosure':False}
        write(STAGE/'MODEL.json',model)
        pkg_manifest={'id':'RANK9-MEMORYDENIAL6-PACKAGE-MANIFEST-196','sourceArchive':arc_bind,
                      'deliveryManifest':del_bind,'independentAudit':audit_bind,
                      'sourceAnchorCommit':audit['sourceCommit'],'files':[]}
        for f in sorted(x for x in STAGE.rglob('*') if x.is_file()):
            b=f.read_bytes()
            pkg_manifest['files'].append({'path':(PKG_REL/f.relative_to(STAGE)).as_posix(),'bytes':len(b),'sha256':sha(b)})
        write(STAGE/'CANDIDATE_PACKAGE_MANIFEST.json',pkg_manifest)
        manifest_bind=bind(STAGE/'CANDIDATE_PACKAGE_MANIFEST.json')
        shutil.move(str(STAGE),str(PKG))
        model_bind=bind(PKG/'MODEL.json')
        manifest_bind=bind(PKG/'CANDIDATE_PACKAGE_MANIFEST.json')
        pkg_casebook_bind=bind(PKG/'CASEBOOK.json.gz')
        MAN.parent.mkdir(parents=True,exist_ok=True)
        MAN.write_bytes((PKG/'STANDALONE_PROCEDURES.md').read_bytes())
        shutil.copyfile(INDEX,BACKUP)
        assert BACKUP.read_bytes()==before_raw

        write(DEC,{
          'id':director['id'],'recordedAtUtc':timestamp,'decision':'PARTIAL_EXACT_IDENTITY_ACCEPTANCE',
          'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'blockers':blocker_map,
          'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,
          'authorityAtDecision':baseline,'exactDirectorDecisions':director['decisions'],
          'inheritedNamedBlockersCarriedForward':director['carriedNamedBlockersUnchanged'],
          'scope':'Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.',
          'canonicalFilesChangedByDirector':False})
        acceptance={
          'id':REVIEW,'recordedAtUtc':timestamp,
          'status':'FOUR_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_BLOCKERS',
          'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'directorDecision':bind(DEC),'directorReturn':arc_bind,'deliveryManifest':del_bind,
          'independentAudit':audit_bind,'candidateEnvelope':model_bind,
          'candidatePackageManifest':manifest_bind,'countsBefore':BEFORE,'countsAfter':AFTER,
          'completeReviewedStandaloneProceduresBefore':COMPLETE0,'completeReviewedStandaloneProceduresAfter':COMPLETE1,
          'blockers':blocker_map,'runtimeSelectionEnabled':False,'canonicalApplicationPerformedByOwner':False}
        write(ACC,acceptance)
        write(RCPT,{
          'id':'RANK9-MEMORYDENIAL6-RETURN196-RECEIPT',
          'recordedAtUtc':timestamp,'status':'FOUR_ACCEPTED_TWO_BLOCKED_INDEPENDENT_AUDIT_PASSED',
          'reviewedIds':GROUP,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'blockers':blocker_map,
          'inheritedNamedBlockers':director['carriedNamedBlockersUnchanged'],
          'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,
          'sourceAuthority':baseline,'counts':delivery['counts'],'decisionId':director['id']})
        write(APPFILE,{
          'id':APP,'recordedAtUtc':timestamp,'status':'APPLIED_FOUR_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS',
          'ownerInstruction':'Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.',
          'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'directorAcceptance':bind(ACC),'directorDecision':bind(DEC),'directorReturnReceipt':bind(RCPT),
          'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,
          'candidateEnvelope':model_bind,'candidatePackageManifest':manifest_bind,'manuscript':bind(MAN),
          'indexBefore':bind(BACKUP,before_raw),'countsBefore':BEFORE,'countsAfter':AFTER,
          'completeReviewedStandaloneProcedures':{'before':COMPLETE0,'after':COMPLETE1},
          'sourceStatusPreservedAsBlocked':True,'catalogChanged':False,'runtimeSelectionEnabled':False})

        app_bind=bind(APPFILE)
        after=copy.deepcopy(before)
        ops=[]
        for pos,s in enumerate(ACCEPTED):
            ix=next(i for i,x in enumerate(before['entries']) if x['id']==s)
            old=before['entries'][ix]
            new=copy.deepcopy(old)
            new.update({
              'authoredStatus':'reviewed-authored-operational-playtest',
              'procedureFile':'../spell_candidates/rank9memorydenial6_reviewed_196/MODEL.json',
              'procedurePointer':f'/spells/{pos}/procedure',
              'wholeCardPointer':f'/spells/{pos}',
              'sourceCatalogWholeCardPointer':old.get('sourceCatalogWholeCardPointer') or old['wholeCardPointer'],
              'wholeCardIdField':'id','procedureTextPointer':f'/spells/{pos}/procedure/procedureContent',
              'directorProcedureRecordPointer':f'/spells/{pos}/directorProcedureRecord',
              'sharedRulesPointer':f'/spells/{pos}/procedure/sharedRequirements',
              'manuscript':'../../../docs/spells/candidates/RANK9_MEMORYDENIAL6_REVIEWED_196.md',
              'reviewId':APP,'runtimeSelectionEnabled':False,'historicalCandidateLabelsPreserved':True,
              'completeEvidenceRoot':PKG_REL.as_posix(),'completeEnvelopeBinding':model_bind,
              'casebookBinding':pkg_casebook_bind,
          'supplementalSourcePackageMap':source_map_bind,
              'casebookEncoding':'Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the director return archive.',
              'casebookSourceArchiveMemberBinding':model['casebookSourceArchiveMemberBinding'],
              'sourceArchiveBinding':arc_bind,'deliveryManifestBinding':del_bind,
              'candidatePackageManifestBinding':manifest_bind,'procedureSourceBinding':bind(DEC),
              'authoredAcceptanceReceipt':bind(ACC),'authoredApplicationReceipt':app_bind})
            assert old['sourceStatus']==new['sourceStatus']=='blocked-pending-operational-review'
            ops.append({'op':'replace-entry','identity':s,'index':ix,'before':copy.deepcopy(old),'after':copy.deepcopy(new)})
            after['entries'][ix]=new
        after['additionalStandaloneEnvelopes'].append({
          'file':'../spell_candidates/rank9memorydenial6_reviewed_196/MODEL.json',
          'binding':model_bind,'reviewId':REVIEW,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'excludedPendingIds':sorted(live-set(ACCEPTED)),'authority':bind(ACC),
          'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),'sourceArchive':arc_bind,
          'deliveryManifest':del_bind,'casebookBinding':pkg_casebook_bind,
          'candidatePackageManifestBinding':manifest_bind,'scope':acceptance['status'],
          'runtimeSelectionEnabled':False})
        after['authoredCounts']=AFTER
        after['representationCounts']['completeReviewedStandaloneProcedures']=COMPLETE1
        pending={x['id'] for x in after['entries'] if x['authoredStatus']=='pending-authored-procedure'}
        assert pending==live-set(ACCEPTED) and len(pending)==62
        inverse=copy.deepcopy(after)
        for op in ops: inverse['entries'][op['index']]=copy.deepcopy(op['before'])
        inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]
        inverse['authoredCounts']=copy.deepcopy(before['authoredCounts'])
        inverse['representationCounts']=copy.deepcopy(before['representationCounts'])
        assert inverse==before
        after_raw=jb(after)
        tmp=INDEX.with_suffix('.json.memorydenial196.tmp')
        tmp.write_bytes(after_raw)
        tmp.replace(INDEX)
        assert CATALOG.read_bytes()==catalog_raw
        write(OPS,{
          'id':'RANK9-MEMORYDENIAL6-INDEX-OPERATIONS-196',
          'before':bind(BACKUP,before_raw),'after':bind(INDEX,after_raw),
          'operations':ops,'inverseSemanticExact':True,'onlyIdentityIds':ACCEPTED})

        groups=[]
        for oldg in q0['currentPendingGroups']:
            left=[s for s in oldg['pendingIds'] if s in pending]
            if not left: continue
            g=copy.deepcopy(oldg);g['pendingIds']=left;g['pendingCount']=len(left)
            if g['group']=='rank9-memory-denial6':
                g.update({'status':'PARTIAL_RETURN196_FOUR_ACCEPTED_APPLIED_TWO_BLOCKED',
                          'freshPacketRequiredForCurrentAuthority':True,
                          'blockingReturn':{'ids':UNACCEPTED,
                                            'blockers':{s:decisions[s]['blockerIds'] for s in UNACCEPTED},
                                            'receipt':RCPT.relative_to(ROOT).as_posix()}})
            if g['group']==NEXT:
                g.update({'status':'PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY',
                          'freshPacketRequiredForCurrentAuthority':True})
            groups.append(g)
        ng=next(g for g in groups if g['group']==NEXT)
        authority={'reviewedApplied':786,'pending':62,'acceptedUnapplied':0,'completeStandaloneProcedures':510,'scopedInterfaces':173}
        inherited=p0
        pending_doc={
          'id':'CURRENT62-PENDING-IDENTITY-AUDIT-196','recordedAtUtc':timestamp,
          'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET',
          'indexBinding':bind(INDEX,after_raw),'catalogBinding':bind(CATALOG,catalog_raw),
          'authoredCounts':AFTER,'pendingCount':62,'pendingIds':sorted(pending),
          'allPendingExistInSourceCatalog':pending<=set(cats),'acceptedUnapplied':0,
          'retainedReturn188Blockers':inherited.get('retainedReturn188Blockers',{}),
          'retainedReturn190Blockers':inherited.get('retainedReturn190Blockers',{}),
          'retainedReturn192Blockers':inherited.get('retainedReturn192Blockers',{}),
          'retainedReturn194Blockers':inherited.get('retainedReturn194Blockers',{}),
          'retainedReturn196Blockers':{
            s:{'blockerIds':decisions[s]['blockerIds'],'holdIds':procs[s]['holdIds'],
               'reason':next(b['missing'] for b in blocks if s in b['blockingForIds'])}
            for s in UNACCEPTED},
          'closed335AndCompletedCohortsReopened':False}
        write(P1,pending_doc)
        next_req={'group':NEXT,'pendingIds':NEXT_IDS,'pendingCount':5,
                 'status':'PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY',
                 'freshPacketRequiredForCurrentAuthority':True,
                 'candidate':ng.get('candidate'),'archive':ng.get('archive')}
        q1=copy.deepcopy(q0)
        q1.update({
          'id':'SPELL-REVIEW-QUEUE-196','recordedAtUtc':timestamp,
          'currentAuthority':authority,'pendingCount':62,'currentPendingGroups':groups,
          'justAppliedBatch':{'reviewId':REVIEW,'ids':ACCEPTED,'count':4,
                              'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),
                              'directorAcceptance':ACC.relative_to(ROOT).as_posix(),
                              'independentAudit':AUDIT_JSON.relative_to(ROOT).as_posix()},
          'pendingIdentityAudit':{'path':P1.relative_to(ROOT).as_posix(),'pending':62,'sha256':sha(P1.read_bytes())},
          'nextGroup':NEXT,'next':next_req,'nextPreparedRequest':next_req,
          'packetStatus':'RANK9_MEMORYDENIAL6_RETURN196_FOUR_APPLIED_TWO_HELD_786_62_NEXT_RANK9_KNOWLEDGE_REVELATION5',
          'currentReturnBinding':arc_bind,'currentReturnAudit':audit_bind})
        for k in ('sourceConferencePrepared','currentPacket','currentPacketDelivery','currentPreparation'):
            q1.pop(k,None)
        q1['currentSubmission']=bind(RCPT)
        q1['currentSubmissionBinding']=bind(RCPT)
        q1['currentReturnBinding']=arc_bind
        q1['currentReturnAudit']=audit_bind
        write(Q1,q1)

        h1=copy.deepcopy(h0)
        h1.update({
          'id':'CURRENT-HANDOFF-196',
          'recordedAtUtc':timestamp,
          'status':'RANK9_MEMORYDENIAL6_FOUR_APPLIED_TWO_HELD_NEXT_RANK9_KNOWLEDGE_REVELATION5_62_PENDING',
          'currentAuthority':authority,
          'currentIndexBinding':bind(INDEX,after_raw),
          'currentCatalogBinding':bind(CATALOG,catalog_raw),
          'pendingIdentityAudit':{'id':pending_doc['id'],'path':P1.relative_to(ROOT).as_posix(),
                                  'pendingCount':62,'sha256':sha(P1.read_bytes())},
          'appliedThisStep':{'reviewId':REVIEW,'ids':ACCEPTED,'count':4,
                             'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),
                             'directorAcceptance':ACC.relative_to(ROOT).as_posix(),
                             'independentAudit':AUDIT_JSON.relative_to(ROOT).as_posix(),
                             'applicationValidation':{'path':VALID.relative_to(ROOT).as_posix()}},
          'unacceptedThisStep':{'ids':UNACCEPTED,
                                'blockers':{s:decisions[s]['blockerIds'] for s in UNACCEPTED},
                                'retainedInPendingSet':True},
          'nextGroup':NEXT,'nextPendingCount':5,'nextPreparedRequest':next_req,
          'currentQueueBinding':bind(Q1),'currentReturnBinding':arc_bind,
          'independentAuditBinding':audit_bind,'parentHandoff':H0.relative_to(ROOT).as_posix(),
          'currentSubmissionBinding':bind(RCPT),'currentReturnAudit':audit_bind,
          'resumePriority':'Prepare a fresh Rank9 Knowledge/Revelation5 packet at 786/62 for GPT; submit, independently audit, apply and push only exact accepted IDs, and continue until pending is zero.'})
        for k in ('sourceConferencePrepared','currentPacket','currentPacketDelivery','currentPreparation'):
            h1.pop(k,None)
        write(H1,h1)
        shutil.copyfile(MAN,AUDIT/'RANK9_MEMORYDENIAL6_REVIEWED_196.md')
        snap=(
          '# Current ordinary spell-review checkpoint 196\\n\\n'
          f'Return196 passed {audit["checksPassed"]} independent checks, including all 80 cases, '
          f'{audit["checks"][16]["detail"]["events"]} events, and exact reversible event/state verification. '
          f'Applied exactly {", ".join(ACCEPTED)} as static authored procedures. '
          'Mind Collapse and Unravel Identity remain pending under MD196-B01 and MD196-B02. '
          'Authority: **786 reviewed / 62 pending / 0 accepted-unapplied**, 510 complete procedures. '
          'Next: Rank9 Knowledge/Revelation5. Runtime and downstream approval gates remain disabled.\\n')
        SNAP.write_text(snap,encoding='utf-8',newline='\n')
        start=ROOT/'START_HERE.md'
        old=start.read_text(encoding='utf-8-sig') if start.exists() else ''
        start.write_text(
          f'**Current ordinary spell-review handoff [196](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_196.json):** Applied exactly {", ".join(ACCEPTED)}. Authority is **786 reviewed / 62 pending / 0 accepted-unapplied**. Mind Collapse and Unravel Identity remain pending under MD196-B01 and MD196-B02. Next group: Rank9 Knowledge/Revelation5.\\n\\n'+old,
          encoding='utf-8',newline='\n')

        checks=[
          {'check':'Return archive, delivery manifest, and independent audit bindings match','passed':audit['status']=='PASS' and sha_file(ZIP)==arc_bind['sha256'] and sha_file(DELIVERY)==del_bind['sha256']},
          {'check':'Exactly four accepted IDs applied; both blocked IDs remain pending','passed':[o['identity'] for o in ops]==ACCEPTED and set(UNACCEPTED)<=pending},
          {'check':'Authority advanced 782/66/506 to 786/62/510','passed':after['authoredCounts']==AFTER and after['representationCounts']['completeReviewedStandaloneProcedures']==COMPLETE1},
          {'check':'Pending set is the exact prior set minus four acceptances','passed':pending==live-set(ACCEPTED)},
          {'check':'Index inverse restores original index and canonical catalog is byte-identical','passed':inverse==before and CATALOG.read_bytes()==catalog_raw},
          {'check':'Every candidate package file matches its manifest binding','passed':all((ROOT/r['path']).is_file() and (ROOT/r['path']).stat().st_size==r['bytes'] and sha_file(ROOT/r['path'])==r['sha256'] for r in pkg_manifest['files'])},
          {'check':'Next group and all five IDs match GPT director instructions','passed':q1['nextGroup']==NEXT and ng['pendingIds']==NEXT_IDS},
          {'check':'Runtime and downstream gates remain disabled','passed':all(model[k] is False for k in ('runtimeSelectionEnabled','runtimeTestsExecuted','sourceProgramsExecuted','implementationApproved','humanPlaytested','balanceApproved','cosmologyModified','releaseApproved','domainClosure'))},
          {'check':'No closed feat or completed cohort was reopened','passed':pending_doc['closed335AndCompletedCohortsReopened'] is False and set(ACCEPTED)<=set(p0['pendingIds'])}
        ]
        validation={
          'id':'RANK9-MEMORYDENIAL6-APPLICATION-VALIDATION-196',
          'recordedAtUtc':timestamp,'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL',
          'checksPassed':sum(x['passed'] for x in checks),'checksFailed':sum(not x['passed'] for x in checks),
          'checks':checks,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'countsBefore':{**BEFORE,'completeReviewedStandaloneProcedures':COMPLETE0},
          'countsAfter':{**AFTER,'completeReviewedStandaloneProcedures':COMPLETE1},
          'indexBefore':bind(BACKUP,before_raw),'indexAfter':bind(INDEX),'catalog':bind(CATALOG),
          'application':bind(APPFILE),'independentAudit':audit_bind,'pendingIdentityAudit':bind(P1),
          'queueAfter':bind(Q1),'handoffAfter':bind(H1),'nextGroup':NEXT,'runtimeSelectionEnabled':False}
        write(VALID,validation)
        assert validation['status']=='PASS',checks
        print(json.dumps({
          'status':'APPLIED_AND_VALIDATED','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,
          'authority':authority,'nextGroup':NEXT,'independentAudit':audit['status'],
          'validation':validation['status'],'indexSha256':sha_file(INDEX),
          'candidateManifest':manifest_bind,'candidateFiles':len(pkg_manifest['files'])},indent=2))
if __name__=='__main__':
    main()
