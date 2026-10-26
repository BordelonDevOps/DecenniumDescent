from __future__ import annotations
import copy,gzip,hashlib,json,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECV=AUDIT/'planar5_return166_received'
PACKAGE=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8planar5_reviewed_166'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
BEFORE=AUDIT/'authored_review_index.before_planar5_167.json'
OPS=AUDIT/'PLANAR5_INDEX_OPERATIONS_167.json'
APP=AUDIT/'PLANAR5_APPLICATION_167.json'
ACCEPTANCE=AUDIT/'PLANAR5_EXACT_ACCEPTANCE_166.json'
DECISION=AUDIT/'GPT_DIRECTOR_DECISION_PLANAR5_166.json'
RETURN=RECV/'DD_Rank8_Planar5_Director_Return166.zip'
PACKET=ROOT/'docs/audit/2026-10-08/full-game/DD_Rank8_Planar_5_Source_Conference_02.zip'
LOCAL_RETURN=RECV/'PLANAR5_RETURN166_LOCAL_AUDIT.json'
PENDING=AUDIT/'CURRENT113_PENDING_IDENTITY_AUDIT_167.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_167.json'
HANDOFF=AUDIT/'CURRENT_HANDOFF_167.json'
VALIDATION=AUDIT/'PLANAR5_APPLICATION_VALIDATION_167.json'
START=ROOT/'START_HERE.md'
SNAPSHOT=ROOT/'SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_167.md'
IDS=['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
AUTH={'reviewedApplied':735,'pending':113,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':459,'scopedInterfaces':173}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def check(name,ok):checks.append({'check':name,'passed':bool(ok)});failures.extend([name] if not ok else [])
checks=[];failures=[]
index_raw=INDEX.read_bytes();catalog_raw=CATALOG.read_bytes();before_raw=BEFORE.read_bytes()
index=json.loads(index_raw.decode('utf-8-sig'));before=json.loads(before_raw.decode('utf-8-sig'));catalog=json.loads(catalog_raw.decode('utf-8-sig'))
ops=read(OPS);app=read(APP);acceptance=read(ACCEPTANCE);decision=read(DECISION);local_return=read(LOCAL_RETURN);pending=read(PENDING);queue=read(QUEUE);handoff=read(HANDOFF)
check('Independent Planar5 return audit passed all 32 checks',local_return['status']=='PASS' and local_return['checkCount']==local_return['checksPassed']==32 and local_return['checksFailed']==0)
check('Return ZIP is bound exactly in the application and acceptance receipts',sha(RETURN.read_bytes())==decision['acceptedArchive']['sha256']==app['directorReturn']['sha256'] and RETURN.stat().st_size==app['directorReturn']['bytes'] and acceptance['directorReturn']['sha256']==sha(RETURN.read_bytes()))
check('GPT accepted exactly five IDs, unapplied at decision time, with no blockers',decision['accepted'] is True and decision['appliedAtDecision'] is False and decision['acceptedIds']==IDS and decision['rejectedIds']==[] and decision['remainingBlockingDefects']==[] and acceptance['acceptedIds']==IDS)
check('Application advances authority 730/118 to 735/113 with zero accepted-unapplied',app['counts']['before']['reviewed']==730 and app['counts']['before']['pending']==118 and app['counts']['after']['reviewed']==735 and app['counts']['after']['pending']==113 and app['counts']['after']['acceptedUnapplied']==0 and acceptance['countsAfter']==app['counts']['after'])
check('Standalone procedure count advances 454 to 459',app['completeReviewedStandaloneProcedures']=={'before':454,'after':459} and index['representationCounts']['completeReviewedStandaloneProcedures']==459)
check('Live authored count is 735 reviewed and 113 pending',index['authoredCounts']=={'reviewed':735,'pending':113})
check('Catalog bytes remain equal to the submitted Conference02 authority',catalog_raw==zipfile.ZipFile(PACKET).read('sources/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'))
check('Exact pre-application index backup hash and size match operation record',len(before_raw)==ops['before']['bytes'] and sha(before_raw)==ops['before']['sha256'])
check('Applied index hash and size match operation record',len(index_raw)==ops['after']['bytes'] and sha(index_raw)==ops['after']['sha256'])
index_rows={r['id']:r for r in index['entries']};before_rows={r['id']:r for r in before['entries']};catalog_rows={r['id']:r for r in catalog['spells']}
changed=sorted(sid for sid in index_rows if index_rows[sid]!=before_rows[sid])
check('Only the five director-accepted identity rows changed',changed==sorted(IDS) and ops['onlyIdentityIds']==IDS)
check('Exactly five before/after index operations exist',len(ops['operations'])==5 and {o['identity'] for o in ops['operations']}==set(IDS))
model=read(PACKAGE/'MODEL.json')
for op in ops['operations']:
    sid=op['identity'];row=index_rows[sid];pos=IDS.index(sid)
    check(f'Before and after operation rows bind live entry for {sid}',op['before']==before_rows[sid] and op['after']==row)
    check(f'Accepted native source status remains blocked and runtime disabled for {sid}',row['sourceStatus']=='blocked-pending-operational-review' and row['runtimeSelectionEnabled'] is False and catalog_rows[sid]['status']=='blocked-pending-operational-review')
    check(f'Index procedure pointers resolve to the accepted native ID for {sid}',model['spells'][pos]['id']==sid and row['wholeCardPointer']==f'/spells/{pos}' and row['procedurePointer']==f'/spells/{pos}/procedure' and model['spells'][pos]['procedure']=={'common':model['sharedRules']['perSpellCommon'][sid],'rules':model['spells'][pos]['directorProcedureRecord']['localRules']})
inverse=copy.deepcopy(index)
for op in ops['operations']:inverse['entries'][op['index']]=copy.deepcopy(op['before'])
inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]
inverse['authoredCounts']=copy.deepcopy(before['authoredCounts']);inverse['representationCounts']=copy.deepcopy(before['representationCounts'])
check('Inverse semantic replay restores the complete previous index object',inverse==before and ops['inverse']['semanticExact'] is True)
check('Catalog remains unchanged by application',catalog_raw==zipfile.ZipFile(PACKET).read('sources/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'))
package_manifest=read(PACKAGE/'CANDIDATE_PACKAGE_MANIFEST.json')
manifest_ok=True
for item in package_manifest['files']:
    path=PACKAGE.joinpath(*PurePosixPath(item['path']).parts);raw=path.read_bytes();manifest_ok &= len(raw)==item['bytes'] and sha(raw)==item['sha256']
check('Candidate package manifest binds every extracted return and evidence file',manifest_ok and len(package_manifest['files'])>=35)
check('Normalized model contains exactly the five accepted IDs',model['acceptedIds']==IDS and [s['id'] for s in model['spells']]==IDS and model['returnCounts']['procedures']==5)
with zipfile.ZipFile(RETURN) as z:
    return_names=set(z.namelist())
    omitted=model['returnArchiveOnlyMembers'];extracted={p.relative_to(PACKAGE/'DIRECTOR_RETURN').as_posix() for p in (PACKAGE/'DIRECTOR_RETURN').rglob('*') if p.is_file()}
    check('All six long accepted-comparison snapshots remain in the byte-exact return archive',len(omitted)==6 and all(n in return_names for n in omitted) and all(n.startswith('accepted-comparisons/') for n in omitted))
    check('Every remaining return member is extracted byte-exactly to the review package',return_names-set(omitted)==extracted and all((PACKAGE/'DIRECTOR_RETURN'/Path(*PurePosixPath(n).parts)).read_bytes()==z.read(n) for n in extracted))
    returned={sid:json.loads(z.read(f'procedures/{sid}.json')) for sid in IDS}
check('Normalized model preserves each complete GPT procedure record',all(model['spells'][IDS.index(sid)]['directorProcedureRecord']==returned[sid] for sid in IDS))
check('Each native card and class-access record equals the unchanged live catalog',all(model['spells'][IDS.index(sid)]['nativeCardAndAccessUnchanged']==catalog_rows[sid] for sid in IDS))
casebook=(PACKAGE/'DIRECTOR_RETURN/CASEBOOK.json').read_bytes()
check('Compressed casebook round-trips byte-for-byte',gzip.decompress((PACKAGE/'CASEBOOK.json.gz').read_bytes())==casebook)
case_rows=read(PACKAGE/'DIRECTOR_RETURN/CASEBOOK.json');holds=read(PACKAGE/'DIRECTOR_RETURN/HOLD_REGISTER.json')
check('All 29 cases, 10 whole-case holds and 17 retained hold categories remain',len(case_rows)==29 and sum(c['wholeCaseHeld'] for c in case_rows)==10 and len(holds)==17 and all(h['status']=='retained' for h in holds))
check('Both Gloom Bind main cases and destination-dependent branches remain held',all(next(c for c in case_rows if c['id']==sid)['wholeCaseHeld'] for sid in ['P5-GLOOM-A','P5-GLOOM-B','P5-GLOOM-A/corpse-source-expiry','P5-GLOOM-B/actual-freeing']))
check('No runtime, human-play, balance, cosmology, domain closure or release approval was added',all(model[k] is False for k in ['runtimeSelectionEnabled','runtimeTestsExecuted','sourceProgramsExecuted','humanPlaytested','balanceApproved','cosmologyModified','releaseApproved','domainClosure']))
check('No completed feat or prior spell cohort was reopened',app['closedCohortsReopened'] is False and pending['closed335AndCompletedCohortsReopened'] is False)
pending_ids=set(pending['pendingIds']);live_pending={e['id'] for e in index['entries'] if e['authoredStatus']=='pending-authored-procedure'}
check('Current pending audit has exactly 113 identities and matches live index',pending['pendingCount']==113 and len(pending_ids)==113 and pending_ids==live_pending and pending['acceptedUnapplied']==0)
check('All pending identities still exist in unchanged native catalog',pending['allPendingExistInSourceCatalog'] is True and all(sid in catalog_rows for sid in pending_ids))
check('Queue authority and total pending groups equal 735/113',queue['currentAuthority']==AUTH and sum(g['pendingCount'] for g in queue['currentPendingGroups'])==113)
check('Rank8 remaining4 is next and requires a fresh current-authority packet',queue['nextGroup']=='rank8-remaining4' and queue['currentPendingGroups'][0]['group']=='rank8-remaining4' and queue['next']['freshPacketRequiredForCurrentAuthority'] is True and queue['currentPendingGroups'][0]['pendingCount']==4)
check('Handoff binds current authority, index, catalog, queue and pending audit',handoff['currentAuthority']==AUTH and handoff['currentIndexBinding']['sha256']==sha(index_raw) and handoff['currentCatalogBinding']['sha256']==sha(catalog_raw) and handoff['currentQueueBinding']['sha256']==sha(QUEUE.read_bytes()) and handoff['pendingIdentityAudit']['sha256']==sha(PENDING.read_bytes()))
check('Start and snapshot report current authority and next group',all(x in START.read_text(encoding='utf-8') for x in ['735 reviewed / 113 pending / 0 accepted-unapplied','rank8-remaining4']) and all(x in SNAPSHOT.read_text(encoding='utf-8') for x in ['735 reviewed / 113 pending / 0 accepted-unapplied','rank8-remaining4']))
result={'id':'PLANAR5-APPLICATION-VERIFICATION-167','status':'PASS' if not failures else 'FAIL','checkCount':len(checks),'failures':len(failures),'failedChecks':failures,'checks':checks,'acceptedIds':IDS,'authority':AUTH,'nextGroup':queue['nextGroup'],'index':{'bytes':len(index_raw),'sha256':sha(index_raw)},'catalog':{'bytes':len(catalog_raw),'sha256':sha(catalog_raw)},'directorReturn':{'bytes':RETURN.stat().st_size,'sha256':sha(RETURN.read_bytes())}}
VALIDATION.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:result[k] for k in ['id','status','checkCount','failures','failedChecks','acceptedIds','authority','nextGroup']},indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
