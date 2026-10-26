from __future__ import annotations
import copy,hashlib,json,zipfile
from datetime import datetime,timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
OLD_ARCHIVE=FULL/'DD_Rank8_Remaining_4_Source_Conference_01.zip'
OLD_PREPARATION=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_01_PREPARATION.json'
OLD_CANDIDATE_PATH=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_01.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_167.json'
HANDOFF=AUDIT/'CURRENT_HANDOFF_167.json'
PENDING=AUDIT/'CURRENT113_PENDING_IDENTITY_AUDIT_167.json'
LATEST=[
 AUDIT/'PLANAR5_APPLICATION_167.json',AUDIT/'GPT_DIRECTOR_DECISION_PLANAR5_166.json',AUDIT/'PLANAR5_EXACT_ACCEPTANCE_166.json',AUDIT/'PLANAR5_APPLICATION_VALIDATION_167.json',
 AUDIT/'INFORMATION_TIME4_APPLICATION_164.json',AUDIT/'GPT_DIRECTOR_DECISION_INFORMATION_TIME4_162.json',AUDIT/'INFORMATION_TIME4_EXACT_ACCEPTANCE_162.json',AUDIT/'INFORMATION_TIME4_APPLICATION_VALIDATION_164.json',
]
IDS=['prismatic-wall','faction-convergence','divine-intervention-lesser','reality-patch']
AUTH={'reviewedApplied':735,'pending':113,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':459,'scopedInterfaces':173}
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_02.json'
OUTPUT=FULL/'rank8-remaining4-source-conference-02-168'
ARCHIVE=FULL/'DD_Rank8_Remaining_4_Source_Conference_02.zip'
CHECK=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_CHECK.json'
PREPARATION=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_PREPARATION.json'
REQUEST=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_REQUEST.txt'
QUEUE_AFTER=AUDIT/'CURRENT_SPELL_QUEUE_168.json'
HANDOFF_AFTER=AUDIT/'CURRENT_HANDOFF_168.json'

def read(p:Path)->Any:return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v:Any)->bytes:return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def binding(p:Path)->dict:
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def write(p:Path,v:Any)->None:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(v))
def writeb(p:Path,b:bytes)->None:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def main():
 final=[ARCHIVE,CHECK,PREPARATION,QUEUE_AFTER,HANDOFF_AFTER]
 exists=[str(p) for p in final if p.exists()]
 assert not exists, f'Conference02 outputs already exist; inspect: {exists}'
 assert not CANDIDATE.exists(), f'Fresh candidate already exists: {CANDIDATE}'
 assert not OUTPUT.exists(), f'Fresh output directory already exists: {OUTPUT}'
 with zipfile.ZipFile(OLD_ARCHIVE) as z:
  assert z.testzip() is None
  old_raw=z.read('CANDIDATE.json');old_candidate=json.loads(old_raw.decode('utf-8-sig'))
  old_manifest=z.read('MANIFEST.json');old_check=z.read('SOURCE_CHECK.json');old_readme=z.read('README.md')
 old_prep=read(OLD_PREPARATION);old_archive_raw=OLD_ARCHIVE.read_bytes()
 assert len(old_raw)==old_prep['candidate']['bytes'] and sha(old_raw)==old_prep['candidate']['sha256']
 assert len(old_archive_raw)==old_prep['archive']['bytes'] and sha(old_archive_raw)==old_prep['archive']['sha256']
 index=read(INDEX);catalog=read(CATALOG);queue_before=read(QUEUE);handoff_before=read(HANDOFF);pending_before=read(PENDING)
 assert queue_before['currentAuthority']==handoff_before['currentAuthority']==AUTH
 assert queue_before['nextGroup']=='rank8-remaining4'
 group=queue_before['currentPendingGroups'][0]
 assert group['group']=='rank8-remaining4' and group['pendingIds']==IDS and group['pendingCount']==4
 live_pending={r['id'] for r in index['entries'] if r['authoredStatus']=='pending-authored-procedure'}
 assert len(live_pending)==113 and set(pending_before['pendingIds'])==live_pending and pending_before['pendingCount']==113
 assert pending_before['indexBinding']['sha256']==sha(INDEX.read_bytes())
 catalog_by={r['id']:r for r in catalog['spells']};index_by={r['id']:r for r in index['entries']}
 assert set(IDS)<=live_pending and all(s in catalog_by and index_by[s]['authoredStatus']=='pending-authored-procedure' for s in IDS)
 assert len(old_candidate['questions'])==22 and all(q['decisionSelected'] is False for q in old_candidate['questions'])
 assert [r['spellId'] for r in old_candidate['records']]==IDS
 source_files={}
 for row in old_candidate['sourceBindings']:
  rel=row['path'];p=ROOT/rel
  assert p.is_file(),f'Old conference current-source file no longer exists: {rel}'
  source_files[rel]=p
 for p in [INDEX,CATALOG,QUEUE,HANDOFF,PENDING,*LATEST]:
  assert p.is_file(),f'Missing current authority source {p}'
  source_files[p.relative_to(ROOT).as_posix()]=p
 current_sources=[{'path':rel,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for rel,p in sorted(source_files.items())]
 old_source_bindings=copy.deepcopy(old_candidate['sourceBindings'])
 now=datetime.now(timezone.utc).isoformat()
 candidate=copy.deepcopy(old_candidate)
 candidate.update({
  'id':'RANK8-REMAINING4-SOURCE-CONFERENCE02-168','recordedAtUtc':now,'status':'SOURCE_CONFERENCE_PREPARED_UNSENT',
  'developmentDirection':'Fresh Conference02 source context for the exact four Rank8 Remaining4 spell identities. Current authority is 735 applied-reviewed / 113 pending / 0 accepted-unapplied. Conference01 remains historical context only.',
  'supersedes':'Conference02 is freshly bound to current 735 applied-reviewed / 113 pending / 0 accepted-unapplied authority. Conference01 and its 525/323 labels remain historical only and do not authorize current decisions.',
  'currentAuthority':{**AUTH,'index':binding(INDEX),'catalog':binding(CATALOG),'currentQueue':binding(QUEUE),'pendingIdentityAudit':binding(PENDING),'priorHandoff':binding(HANDOFF),'latestAppliedBatch':binding(LATEST[0]),'latestDirectorDecision':binding(LATEST[1]),'latestExactAcceptance':binding(LATEST[2]),'latestApplicationValidation':binding(LATEST[3])},
  'countsUnchanged':{'reviewed':735,'pending':113,'acceptedUnapplied':0},
  'historicalConference01':{'authority':old_candidate['countsUnchanged'],'candidate':{'path':OLD_CANDIDATE_PATH.relative_to(ROOT).as_posix(),'bytes':len(old_raw),'sha256':sha(old_raw)},'archive':{'path':OLD_ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(old_archive_raw),'sha256':sha(old_archive_raw)},'qualification':'Full source context only; all decisions remain unselected, and old 525/323 authority labels are superseded.'},
  'historicalSourceBindingsConference01':old_source_bindings,'sourceBindings':current_sources,
  'currentPendingIds':IDS,'currentQueueGroup':copy.deepcopy(group),
  'currentPendingIdentityAudit':{'id':pending_before['id'],**binding(PENDING),'pendingCount':113,'pendingIds':pending_before['pendingIds']},
  'priorConferenceQuestionSetPreserved':{'questionCount':22,'allStillUnselected':True},
  'gptCommunication':'Fresh Rank8 Remaining4 source conference for current 735 applied-reviewed / 113 pending / 0 accepted-unapplied authority. Review only prismatic-wall, faction-convergence, divine-intervention-lesser, and reality-patch. Resolve all 22 preserved source questions. Preserve original source, native-card, class-access, accepted-interface, lifecycle, information, action, geometry, target and cosmology distinctions; retain every unsupported runtime, playtest, balance and release hold. Do not reopen completed/applied cohorts or the closed feat review.',
  'nonAcceptanceOfLaterSourceChanges':'This packet is current source context only. It adopts no rule, global interface, cosmology, runtime behavior, balance, or release state. Historical Conference01 and older authority are superseded for the current pending count; prior accepted/applied spell cohorts remain closed.',
  'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'wholeGameComplete':False,
 })
 assert len(candidate['questions'])==22 and all(q['decisionSelected'] is False for q in candidate['questions'])
 assert set().union(*(set(q['spellIds']) for q in candidate['questions']))==set(IDS)
 assert len(candidate['records'])==4
 for record in candidate['records']:
  sid=record['spellId'];assert sid in IDS
  record['completeCurrentCatalogSourceAndAccess']=copy.deepcopy(catalog_by[sid])
  record['currentIndexEntry']=copy.deepcopy(index_by[sid])
  record['currentQueueStatus']={'identity':sid,'group':'rank8-remaining4','pending':True,'reviewedApplied':735,'pendingCount':113}
  record['status']='Fresh Conference02 source context; no choices adopted.'
 candidate_raw=enc(candidate);writeb(CANDIDATE,candidate_raw)
 request=f'''GPT — review the attached and published Rank8 Remaining4 Conference02 packet against the current branch.\n\nPacket: DD_Rank8_Remaining_4_Source_Conference_02.zip\nAuthority: 735 applied-reviewed / 113 pending / 0 accepted-unapplied; 459 complete authored procedures.\nExact scope: prismatic-wall, faction-convergence, divine-intervention-lesser, reality-patch only.\n\nResolve all 22 preserved source questions. Return complete source-faithful authored procedures, question dispositions, cases and branches, explicit accepted IDs, retained holds, and a semantic failure check. Preserve original source/access and recorded accepted-interface boundaries, unresolved cosmology and all runtime, human-play, balance, and release qualifications. Do not edit canonical files; do not reopen accepted/applied spell cohorts or the closed feat review. If any identity is blocked, say so exactly. For any passing subset, state accepted=true and applied=false only for those exact IDs, with exact blockers and audit counts.\n'''
 writeb(REQUEST,request.encode('utf-8'))
 write(OUTPUT/'CANDIDATE.json',candidate);writeb(OUTPUT/'REQUEST.txt',request.encode('utf-8'))
 writeb(OUTPUT/'historical/Conference01_ARCHIVE.zip',old_archive_raw)
 writeb(OUTPUT/'historical/Conference01_CANDIDATE.json',old_raw)
 writeb(OUTPUT/'historical/Conference01_MANIFEST.json',old_manifest)
 writeb(OUTPUT/'historical/Conference01_SOURCE_CHECK.json',old_check)
 writeb(OUTPUT/'historical/Conference01_README.md',old_readme)
 write(OUTPUT/'CURRENT_AUTHORITY_UPDATE.json',{'id':'REMAINING4-CURRENT-AUTHORITY-UPDATE-168','recordedAtUtc':now,'authority':AUTH,'pendingIds':pending_before['pendingIds'],'group':'rank8-remaining4','scopeIds':IDS,'index':binding(INDEX),'catalog':binding(CATALOG),'queue':binding(QUEUE),'handoff':binding(HANDOFF),'pendingAudit':binding(PENDING),'exactAppliedBatch':binding(LATEST[0]),'qualification':'Current source review only; no runtime, play, balance, cosmology, global rules or release approval.'})
 for rel,p in source_files.items():writeb(OUTPUT/'sources'/Path(*rel.split('/')),p.read_bytes())
 readme='''# Rank8 Remaining4 Source Conference02\n\nFresh source context bound to 735 applied-reviewed / 113 pending / 0 accepted-unapplied authority, with 459 complete authored procedures. Exact scope: prismatic-wall, faction-convergence, divine-intervention-lesser, and reality-patch. All 22 historical source questions remain unselected. Conference01 and its earlier 525/323 authority are preserved as historical context only. No rules, runtime behavior, balance, cosmology, human-play or release approval is granted.\n'''
 writeb(OUTPUT/'README.md',readme.encode('utf-8'))
 checks=[]
 def ck(name,ok):checks.append({'check':name,'passed':bool(ok)});assert ok,name
 ck('Current authority equals 735/113/0 with 459 authored procedures and 173 scoped interfaces',queue_before['currentAuthority']==AUTH)
 ck('Current pending audit exactly equals live index pending set',pending_before['pendingCount']==113 and set(pending_before['pendingIds'])==live_pending)
 ck('Only the exact four current Rank8 Remaining4 identities are selected',candidate['currentPendingIds']==IDS and set(IDS)<=live_pending)
 ck('All 22 original source questions remain unselected',len(candidate['questions'])==22 and all(q['decisionSelected'] is False for q in candidate['questions']))
 ck('All four records bind the exact live catalog cards and index rows',all(r['completeCurrentCatalogSourceAndAccess']==catalog_by[r['spellId']] and r['currentIndexEntry']==index_by[r['spellId']] for r in candidate['records']))
 ck('No accepted-unapplied identity exists',AUTH['acceptedUnapplied']==pending_before['acceptedUnapplied']==0)
 ck('No authored choices, global rule, runtime, playtest or release state adopted',candidate['newRuleAdoptions']==candidate['runtimeTestsExecuted']==candidate['humanPlaytests']==0 and candidate['wholeGameComplete'] is False)
 ck('All current source bindings match exact local files',len(current_sources)>=108 and all((ROOT/r['path']).read_bytes()==(OUTPUT/'sources'/Path(*r['path'].split('/'))).read_bytes() and len((ROOT/r['path']).read_bytes())==r['bytes'] and sha((ROOT/r['path']).read_bytes())==r['sha256'] for r in current_sources))
 ck('Conference01 archive and candidate retained byte-exactly', (OUTPUT/'historical/Conference01_ARCHIVE.zip').read_bytes()==old_archive_raw and (OUTPUT/'historical/Conference01_CANDIDATE.json').read_bytes()==old_raw)
 ck('Fresh candidate preserves all 22 source questions and supersedes earlier authority',candidate['priorConferenceQuestionSetPreserved']=={'questionCount':22,'allStillUnselected':True} and candidate['historicalConference01']['authority']=={'reviewed':525,'pending':323} and candidate['countsUnchanged']=={'reviewed':735,'pending':113,'acceptedUnapplied':0})
 check_doc={'id':'RANK8-REMAINING4-SOURCE-CONFERENCE02-CHECK-168','recordedAtUtc':now,'failures':0,'candidate':{'path':CANDIDATE.relative_to(ROOT).as_posix(),'bytes':len(candidate_raw),'sha256':sha(candidate_raw)},'checks':checks,'questionCount':22,'reviewIds':IDS,'currentAuthority':AUTH}
 write(CHECK,check_doc);write(OUTPUT/'SOURCE_CHECK.json',check_doc)
 manifest={'id':'RANK8-REMAINING4-SOURCE-CONFERENCE02-MANIFEST-168','candidate':{'path':'CANDIDATE.json','bytes':len(candidate_raw),'sha256':sha(candidate_raw)},'check':{'path':'SOURCE_CHECK.json','bytes':len(enc(check_doc)),'sha256':sha(enc(check_doc))},'request':{'path':'REQUEST.txt','bytes':len(request.encode('utf-8')),'sha256':sha(request.encode('utf-8'))},'historicalConference01Archive':{'path':'historical/Conference01_ARCHIVE.zip','bytes':len(old_archive_raw),'sha256':sha(old_archive_raw)},'historicalConference01Candidate':{'path':'historical/Conference01_CANDIDATE.json','bytes':len(old_raw),'sha256':sha(old_raw)},'currentAuthority':AUTH,'currentSourceBindings':current_sources}
 write(OUTPUT/'MANIFEST.json',manifest)
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(OUTPUT.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(OUTPUT).as_posix())
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names));assert z.read('CANDIDATE.json')==candidate_raw and json.loads(z.read('SOURCE_CHECK.json'))['failures']==0
  assert z.read('historical/Conference01_ARCHIVE.zip')==old_archive_raw and z.read('historical/Conference01_CANDIDATE.json')==old_raw
  for row in current_sources:assert z.read('sources/'+row['path'])==(ROOT/row['path']).read_bytes()
 archive_binding={'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':ARCHIVE.stat().st_size,'sha256':sha(ARCHIVE.read_bytes())}
 prep={'id':'RANK8-REMAINING4-SOURCE-CONFERENCE02-PREPARATION-168','recordedAtUtc':now,'status':'PREPARED_UNSENT','candidate':check_doc['candidate'],'archive':archive_binding,'check':binding(CHECK),'questionCount':22,'sourceBindingCount':len(current_sources),'archiveMemberCount':len(names),'currentAuthority':AUTH,'reviewIds':IDS}
 write(PREPARATION,prep);write(OUTPUT/'PREPARATION.json',prep);write(OUTPUT/'MANIFEST.json',manifest)
 q=copy.deepcopy(queue_before);q.update({'id':'SPELL-REVIEW-QUEUE-168','recordedAtUtc':now,'packetStatus':'FRESH_REMAINING4_PACKET_PREPARED_UNSENT'})
 q['currentPendingGroups'][0].update({'candidate':check_doc['candidate'],'archive':archive_binding,'freshPacketRequiredForCurrentAuthority':False,'status':'FRESH_PACKET_PREPARED_UNSENT'})
 q['next']={'group':'rank8-remaining4','pendingCount':4,'candidate':check_doc['candidate'],'archive':archive_binding,'freshPacketRequiredForCurrentAuthority':False,'status':'FRESH_PACKET_PREPARED_UNSENT'}
 q['sourceConferencePrepared']={'candidate':check_doc['candidate'],'archive':archive_binding,'check':binding(CHECK),'preparation':binding(PREPARATION),'request':binding(REQUEST),'status':'prepared-unsent'};q['nextPreparedRequest']=q['sourceConferencePrepared'];write(QUEUE_AFTER,q)
 h=copy.deepcopy(handoff_before);h.update({'id':'CURRENT-HANDOFF-168','recordedAtUtc':now,'status':'REMAINING4_FRESH_PACKET_PREPARED_UNSENT','currentQueueBinding':binding(QUEUE_AFTER)});h['nextPreparedRequest']=q['sourceConferencePrepared'];h['directorSubmission']={'status':'prepared-unsent','group':'rank8-remaining4','reviewIds':IDS,'candidate':check_doc['candidate'],'archive':archive_binding,'request':binding(REQUEST)};write(HANDOFF_AFTER,h)
 print(json.dumps({'status':'PASS_PREPARED_UNSENT','candidate':check_doc['candidate'],'archive':archive_binding,'checkCount':len(checks),'archiveMemberCount':len(names),'sourceBindingCount':len(current_sources),'questionCount':22,'currentAuthority':AUTH,'reviewIds':IDS},indent=2))
if __name__=='__main__':main()
